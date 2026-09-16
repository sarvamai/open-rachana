"""Domain instruments (spec §3.2).

Instruments are created through the API's global meter, so they bind to
whichever provider `register_providers` installs, including the in-memory
one the tests use. Task 4 of the plan adds the audit and registry
instruments here.
"""

from opentelemetry import metrics

_meter = metrics.get_meter("mulyankan_platform.observability")

attributes_dropped = _meter.create_counter(
    "mulyankan.observability.attributes_dropped",
    unit="1",
    description="Attributes removed by the content-free guard, by signal and key",
)
