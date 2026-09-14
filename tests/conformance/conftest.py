"""Shared fixtures for content-leak conformance (ASR01-EVD-09, DAT-03)."""

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"
CLEAN_DIR = FIXTURES_DIR / "clean"
DIRTY_DIR = FIXTURES_DIR / "dirty"


@pytest.fixture
def forbidden_content() -> list[str]:
    """Question-content strings that must never appear in logs or audit."""
    with open(FIXTURES_DIR / "forbidden_content.json", encoding="utf-8") as fh:
        data = json.load(fh)
    return data["stems"] + data["options"] + data["explanations"]
