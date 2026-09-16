"""Provider registry: resolves SPI bindings from configuration (ADR-0003).

The platform never imports a provider directly. Bindings live in
per-environment `platform.yaml`; the registry loads them at startup and
refuses unknown or malformed bindings. A capability with no binding is
refused at call time — the same rule as a model removed from the approved
list.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any

import yaml

from mulyankan_platform.observability.providers import ObservedProvider


class RegistryError(Exception):
    """A binding is missing, malformed, or unloadable."""


@dataclass(frozen=True)
class Binding:
    """One resolved SPI binding."""

    spi: str
    provider: str  # "module:attr" target as written in configuration
    config: dict
    instance: Any
    descriptor: dict | None  # `describe()` resolved once, at bind time
    observed: Any  # the instance wrapped for provider-call spans (spec §4.5)


class ProviderRegistry:
    """Loads and resolves provider bindings; the only path to a provider."""

    def __init__(self, bindings: dict[str, Binding]) -> None:
        self._bindings = bindings

    @classmethod
    def from_mapping(cls, config: dict) -> ProviderRegistry:
        """Build a registry from a parsed configuration mapping."""
        bindings: dict[str, Binding] = {}
        for spi, entry in (config.get("providers") or {}).items():
            if not isinstance(entry, dict):
                raise RegistryError(f"binding for spi '{spi}' must be a mapping")
            target = entry.get("provider")
            if not isinstance(target, str) or ":" not in target:
                raise RegistryError(
                    f"binding for spi '{spi}' must be 'module:attr', got {target!r}"
                )
            module_name, attr = target.split(":", 1)
            try:
                module = importlib.import_module(module_name)
                factory = getattr(module, attr)
            except (ImportError, AttributeError) as exc:
                raise RegistryError(
                    f"cannot load provider '{target}' for spi '{spi}': {exc}"
                ) from exc
            provider_config = entry.get("config") or {}
            try:
                instance = factory(provider_config)
            except Exception as exc:
                raise RegistryError(
                    f"provider '{target}' for spi '{spi}' failed to initialise: {exc}"
                ) from exc
            describe = getattr(instance, "describe", None)
            descriptor = describe().as_dict() if callable(describe) else None
            bindings[spi] = Binding(
                spi=spi,
                provider=target,
                config=provider_config,
                instance=instance,
                descriptor=descriptor,
                observed=ObservedProvider(spi, instance, descriptor, target),
            )
        return cls(bindings)

    @classmethod
    def from_file(cls, path: str) -> ProviderRegistry:
        """Build a registry from a `platform.yaml` file."""
        with open(path, encoding="utf-8") as handle:
            config = yaml.safe_load(handle) or {}
        return cls.from_mapping(config)

    def get(self, spi: str) -> Any:
        """Return the bound provider for `spi`, wrapped so every call is a
        content-free span (spec §4.5); refuse unbound capabilities."""
        binding = self._bindings.get(spi)
        if binding is None:
            raise RegistryError(f"no provider bound for spi '{spi}'")
        return binding.observed

    def describe(self) -> dict[str, dict]:
        """Report every binding with its descriptor, for /healthz and audits."""
        report: dict[str, dict] = {}
        for spi, binding in self._bindings.items():
            report[spi] = {
                "provider": binding.provider,
                "descriptor": binding.descriptor,
            }
        return report
