"""Daily audit-chain verification hook (ASR01-EVD-02/03).

Scheduled by cron or a systemd timer; exits non-zero if the chain is broken
so the calling scheduler can page on-call without reading the log.

Exit codes
----------
0  chain intact
1  chain broken — first_bad_seq and reason are logged at ERROR
2  unexpected error during the verification pass

Content-freedom contract (DAT-03, ASR01-EVD-09)
------------------------------------------------
Every log message emitted here carries only structural facts: event count,
sequence numbers, and short reason codes.  No question text, no actor names,
no object identifiers, no payload data may appear, even in error paths.  The
scheduled alert is intentionally opaque — the Auditor opens the product UI,
not this log, to investigate.

Portability note
----------------
``run_verification`` accepts any ``Sequence[AuditEvent]``, so this module is
store-agnostic.  The in-process M1 log is injected in ``main``; M2+ callers
fetch events from the database and call ``run_verification`` directly without
touching the entry point.
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Sequence

from mulyankan_platform.audit.chain import AuditEvent, VerifyResult, verify

logger = logging.getLogger(__name__)

_EXIT_OK = 0
_EXIT_CHAIN_BROKEN = 1
_EXIT_ERROR = 2


def run_verification(events: Sequence[AuditEvent]) -> int:
    """Verify *events* and return an exit code.

    Logs a single structured line at INFO (ok) or ERROR (broken).  The message
    carries only structural data — no content, no identifiers.
    """
    try:
        result: VerifyResult = verify(events)
    except Exception:
        logger.exception("audit chain verification raised an unexpected error")
        return _EXIT_ERROR

    if result.ok:
        logger.info(
            "audit chain verification passed",
            extra={"events": result.events},
        )
        return _EXIT_OK

    # Broken chain — log structural facts only, never content.
    logger.error(
        "audit chain verification FAILED: reason=%s first_bad_seq=%s events=%s",
        result.reason,
        result.first_bad_seq,
        result.events,
    )
    return _EXIT_CHAIN_BROKEN


def main() -> None:  # pragma: no cover — entry point wired in __main__
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    # M1 uses the in-memory log; replace this import with the persisted store
    # once M2 lands.  The signature of run_verification does not change.
    from mulyankan_platform.audit import AuditLog  # noqa: PLC0415

    log = AuditLog()
    sys.exit(run_verification(log.events))


if __name__ == "__main__":
    main()
