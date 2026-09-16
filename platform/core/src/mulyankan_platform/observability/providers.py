"""Provider-call spans (spec §4.5). The registry is the only path to a
provider, so wrapping here makes every interaction visible and content-free:
arguments and return values are not recorded, which matters most for the kms
SPI, which handles plaintext.
"""

from __future__ import annotations

import functools
import inspect
from typing import Any

from opentelemetry import trace

_tracer = trace.get_tracer("mulyankan_platform.registry")


class ObservedProvider:
    """Wraps every public method of `instance` in a span; forwards the rest.

    Methods are found statically (`inspect.getattr_static`) so a property is
    not evaluated and a nested class is not rebound, and they are bound as
    instance attributes eagerly because Python 3.12's `isinstance` against a
    runtime-checkable Protocol uses `getattr_static`, which ignores
    `__getattr__`. Everything else, attributes and properties included, is
    forwarded on read. Built once per binding by the registry.
    """

    def __init__(
        self, spi: str, instance: Any, descriptor: dict | None, target: str
    ) -> None:
        self._spi = spi
        self._instance = instance
        descriptor = descriptor or {}
        self._attributes = {
            "mulyankan.spi": spi,
            "mulyankan.provider.name": descriptor.get("name", target),
            "mulyankan.provider.version": descriptor.get("version", ""),
        }
        for name in dir(instance):
            if name.startswith("_"):
                continue
            static = inspect.getattr_static(instance, name, None)
            if isinstance(static, (staticmethod, classmethod)):
                static = static.__func__
            if inspect.isfunction(static) or inspect.ismethoddescriptor(static):
                setattr(self, name, self._observed(name, getattr(instance, name)))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._instance, name)

    def _observed(self, name: str, method: Any) -> Any:
        span_name = f"{self._spi}.{name}"

        if inspect.iscoroutinefunction(method):

            @functools.wraps(method)
            async def observed_async(*args: Any, **kwargs: Any) -> Any:
                with _tracer.start_as_current_span(
                    span_name, attributes=self._attributes
                ):
                    return await method(*args, **kwargs)

            return observed_async

        @functools.wraps(method)
        def observed(*args: Any, **kwargs: Any) -> Any:
            with _tracer.start_as_current_span(span_name, attributes=self._attributes):
                return method(*args, **kwargs)

        return observed
