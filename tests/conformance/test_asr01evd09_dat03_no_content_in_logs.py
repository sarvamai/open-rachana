"""Content-leak conformance scan (ASR01-EVD-09, DAT-03).

Scans platform source, test fixtures, and conformance fixtures for question
body content.  Invariant 3 requires audit events to be content-free; this
scan enforces the same rule across every artefact CI can reach.

Two scanning strategies work together:

1. **Structural scan** — JSON files are parsed and flagged when a key named
   ``stem``, ``options``, ``explanation``, or ``distractors`` carries a
   non-empty string value.  A ``payload_hash`` or ``stem_len`` is fine; an
   actual question sentence is not.

2. **Source scan** — Python files are checked for log or exception statements
   that interpolate body-content attributes.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Sequence

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_FIXTURES_DIR = Path(__file__).parent / "fixtures"
_DIRTY_DIR = _FIXTURES_DIR / "dirty"

_PLATFORM_SRC = _REPO_ROOT / "platform" / "core" / "src"
_PLATFORM_TESTS = _REPO_ROOT / "platform" / "core" / "tests"

_BODY_CONTENT_KEYS = frozenset({"stem", "options", "explanation", "distractors"})

_SCAN_TARGETS = [
    _PLATFORM_SRC,
    _PLATFORM_TESTS,
    _FIXTURES_DIR / "clean",
]

_LOG_RAISE_PATTERN = re.compile(
    r"^\s*(?:log(?:ger)?\.\w+|raise\s+\w+)\s*\(.*\{[^}]*\."
    + "|".join(_BODY_CONTENT_KEYS)
    + r"\b",
)


def _is_excluded(path: Path) -> bool:
    """True for paths inside the dirty-fixture directory."""
    try:
        path.relative_to(_DIRTY_DIR)
        return True
    except ValueError:
        return False


def _collect_files(roots: Sequence[Path], suffix: str) -> list[Path]:
    """Gather files with the given suffix under each root, excluding dirty."""
    paths: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob(f"*{suffix}"):
            if not _is_excluded(p):
                paths.append(p)
    return paths


def _scan_json_for_body_keys(path: Path) -> list[str]:
    """Flag JSON files whose stored objects contain body-content keys."""
    findings: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return findings
    _walk(data, path, findings)
    return findings


def _walk(obj: object, source: Path, findings: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in _BODY_CONTENT_KEYS:
                if isinstance(value, str) and value:
                    findings.append(f"{source}: body key '{key}' has content")
                elif isinstance(value, list) and any(
                    isinstance(item, str) and item for item in value
                ):
                    findings.append(f"{source}: body key '{key}' has content")
            _walk(value, source, findings)
    elif isinstance(obj, list):
        for item in obj:
            _walk(item, source, findings)


def _scan_source_for_leaks(path: Path) -> list[str]:
    """Flag Python source that interpolates body fields into logs/errors."""
    findings: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return findings
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(("#", "assert", "def test_", '"""', "'''")):
            continue
        if _LOG_RAISE_PATTERN.search(line):
            findings.append(f"{path}:{lineno}: {stripped}")
    return findings


def test_asr01evd09_no_body_keys_in_json_fixtures() -> None:
    """Stored audit events and log fixtures must not carry body content."""
    json_files = _collect_files(_SCAN_TARGETS, ".json")
    assert json_files, "no JSON files found to scan"
    all_findings: list[str] = []
    for path in json_files:
        all_findings.extend(_scan_json_for_body_keys(path))
    assert not all_findings, (
        "body-content keys found in fixtures:\n" + "\n".join(all_findings)
    )


def test_asr01evd09_no_content_interpolation_in_source() -> None:
    """Platform source must not interpolate body fields into logs/errors."""
    py_files = _collect_files([_PLATFORM_SRC], ".py")
    assert py_files, "no Python source files found to scan"
    all_findings: list[str] = []
    for path in py_files:
        all_findings.extend(_scan_source_for_leaks(path))
    assert not all_findings, (
        "body-content interpolation in log/raise:\n" + "\n".join(all_findings)
    )


def test_dat03_dirty_fixture_is_detected() -> None:
    """The dirty fixture must trigger the structural scanner (control)."""
    dirty = _DIRTY_DIR / "audit_event_with_leak.json"
    findings = _scan_json_for_body_keys(dirty)
    assert findings, "scanner failed to detect leaked content in dirty fixture"
