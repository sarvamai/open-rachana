"""Domain instruments (spec §3.2). Names are `mulyankan.*`; attributes are
low-cardinality and content-free. Instruments are created on the API's
global meter, so they bind to whichever provider `register_providers`
installs, the in-memory one in tests included.
"""

from __future__ import annotations

import weakref
from collections.abc import Iterable
from typing import TYPE_CHECKING

from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation

if TYPE_CHECKING:  # registry imports this package; keep the edge type-only
    from mulyankan_platform.registry import ProviderRegistry

_meter = metrics.get_meter("mulyankan_platform.observability")

attributes_dropped = _meter.create_counter(
    "mulyankan.observability.attributes_dropped",
    unit="1",
    description="Attributes removed by the content-free guard, by signal and key",
)
audit_events = _meter.create_counter(
    "mulyankan.audit.events", unit="{event}", description="Audit events appended"
)
audit_append_duration = _meter.create_histogram(
    "mulyankan.audit.append.duration",
    unit="s",
    description="Time to append one audit event",
)

_registries: weakref.WeakSet[ProviderRegistry] = weakref.WeakSet()


def _bindings(options: CallbackOptions) -> Iterable[Observation]:
    for registry in list(_registries):
        for spi, info in registry.describe().items():
            descriptor = info.get("descriptor") or {}
            yield Observation(
                1,
                {
                    "spi": spi,
                    "provider.name": descriptor.get("name", info["provider"]),
                    "provider.version": descriptor.get("version", ""),
                },
            )


_meter.create_observable_gauge(
    "mulyankan.registry.bindings",
    callbacks=[_bindings],
    unit="{binding}",
    description="Provider bindings the registry resolved",
)


def observe_registry_bindings(registry: ProviderRegistry) -> None:
    """Include `registry` in the bindings gauge."""
    _registries.add(registry)
