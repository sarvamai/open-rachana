"""Content-leak conformance scan (ASR01-EVD-09, DAT-03).

Scans log, audit, and exception fixtures for question content.  Invariant 3
requires audit events to be content-free; this scan enforces the same rule
across every artefact CI can reach.
"""

import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
CLEAN = FIXTURES / "clean"
DIRTY = FIXTURES / "dirty"


def _read(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.dumps(json.loads(raw), ensure_ascii=False)
    return raw


def _scan(text: str, forbidden: list[str]) -> list[str]:
    lowered = text.lower()
    return [p for p in forbidden if p.lower() in lowered]


def test_asr01evd09_clean_audit_event_has_no_content(
    forbidden_content: list[str],
) -> None:
    found = _scan(_read(CLEAN / "audit_event.json"), forbidden_content)
    assert not found, f"question content in audit fixture: {found}"


def test_asr01evd09_clean_log_entries_have_no_content(
    forbidden_content: list[str],
) -> None:
    found = _scan(_read(CLEAN / "log_entries.json"), forbidden_content)
    assert not found, f"question content in log fixture: {found}"


def test_dat03_clean_exception_has_no_content(
    forbidden_content: list[str],
) -> None:
    found = _scan(_read(CLEAN / "exception_message.txt"), forbidden_content)
    assert not found, f"question content in exception fixture: {found}"


def test_dat03_dirty_fixture_is_detected(
    forbidden_content: list[str],
) -> None:
    found = _scan(_read(DIRTY / "audit_event_with_leak.json"), forbidden_content)
    assert found, "scanner failed to detect leaked content in dirty fixture"
