"""Audit chain: verification, tamper detection, content-freedom (ASR01-EVD)."""

import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from mulyankan_platform.audit import (
    AuditLog,
    canonical_bytes,
    verify,
)
from mulyankan_platform.audit.verify_hook import (
    _EXIT_CHAIN_BROKEN,
    _EXIT_OK,
    run_verification,
)
from mulyankan_platform.core_api.main import build_app
from mulyankan_platform.registry import ProviderRegistry


def _log_with_three_events() -> AuditLog:
    log = AuditLog()
    log.append(
        actor="author-001",
        action="draft.created",
        object_refs=("artefact-a1",),
        payload={"stem_len": 42},
    )
    log.append(
        actor="author-001",
        action="draft.submitted",
        object_refs=("artefact-a1", "version-v1"),
        payload={"content_hash": "ab" * 32},
    )
    log.append(
        actor="reviewer-002", action="review.approved", object_refs=("version-v1",)
    )
    return log


def test_asrevd02_chain_verifies_after_appends() -> None:
    log = _log_with_three_events()
    result = log.verify()
    assert result.ok is True
    assert result.events == 3
    assert result.first_bad_seq is None


def test_asrevd03_tampered_event_detected() -> None:
    log = _log_with_three_events()
    tampered = list(log.events)
    # Mutate event at index 1 (seq=1); the hash it carries was computed over
    # the original action, so recomputing it yields a different digest.
    tampered[1] = replace(tampered[1], action="review.approved")
    result = verify(tampered)
    assert result.ok is False
    assert result.first_bad_seq == 1  # verifier catches it at the mutated position
    assert result.reason == "hash mismatch"


def test_asrevd03_removed_event_detected() -> None:
    log = _log_with_three_events()
    with_removed = list(log.events)
    del with_removed[1]
    result = verify(with_removed)
    assert result.ok is False
    assert result.reason == "sequence gap"


def test_events_are_content_free() -> None:
    log = _log_with_three_events()
    payload = {"stem": "What is the capital of India?"}
    event = log.append(
        actor="author-001",
        action="draft.autosaved",
        object_refs=("artefact-a1",),
        payload=payload,
    )
    stored = log.events[-1]
    assert stored is event
    # The payload itself must not appear anywhere on the event.
    assert "stem" not in event.link_bytes().decode("utf-8")
    assert event.payload_hash != ""
    assert len(event.payload_hash) == 64


def test_hashing_is_deterministic_and_unicode_stable() -> None:
    payload = {"question": "मूल्यांकन ☺", "n": 3}
    first = canonical_bytes(payload)
    second = canonical_bytes(dict(reversed(list(payload.items()))))
    assert first == second  # key order never changes the canonical form


def test_asrevd02_concurrent_appends_keep_the_chain_verifiable() -> None:
    """Concurrent writers must not corrupt the chain.

    Starlette runs sync handlers on the anyio threadpool, so real requests
    race on append.  Without the lock, two writers can read the same tail
    and produce two events with identical seq and prev_hash.  That break is
    permanent — the log is append-only and verify reports it forever.
    """
    log = AuditLog()
    writers, per_writer = 8, 50

    def write(worker: int) -> None:
        for _ in range(per_writer):
            log.append(actor=f"author-{worker}", action="draft.autosaved")

    with ThreadPoolExecutor(max_workers=writers) as pool:
        for future in [pool.submit(write, worker) for worker in range(writers)]:
            future.result()

    events = log.events
    assert len(events) == writers * per_writer
    assert [event.seq for event in events] == list(range(writers * per_writer))
    assert len({event.prev_hash for event in events}) == len(events)
    assert log.verify().ok


# ---------------------------------------------------------------------------
# GET /v1/audit/verify endpoint (ASR01-EVD-02/03)
# ---------------------------------------------------------------------------


@pytest.fixture()
def audit_client() -> TestClient:
    """TestClient wired to an app whose audit log has three events."""
    app = build_app(ProviderRegistry.from_mapping({}))
    client = TestClient(app)
    # Populate the audit log via the session surface so the log is not empty.
    r = client.post("/v1/sessions", json={"actor": "author-001"})
    assert r.status_code == 201
    return client


def test_asrevd02_verify_endpoint_returns_ok_on_intact_chain(
    audit_client: TestClient,
) -> None:
    response = audit_client.get("/v1/audit/verify")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["events"] >= 1
    assert "first_bad_seq" not in body
    assert "reason" not in body


def test_asrevd02_verify_endpoint_response_is_content_free(
    audit_client: TestClient,
) -> None:
    """The verify response must never contain question content or identifiers."""
    response = audit_client.get("/v1/audit/verify")
    assert response.status_code == 200
    raw = response.text
    # Structural keys only — no actor names, no object refs, no payload data.
    for forbidden in ("author-001", "artefact", "stem", "question"):
        assert forbidden not in raw


# ---------------------------------------------------------------------------
# Daily verification hook (ASR01-EVD-02/03)
# ---------------------------------------------------------------------------


def test_asrevd02_verify_hook_exits_ok_on_intact_chain() -> None:
    log = _log_with_three_events()
    assert run_verification(log.events) == _EXIT_OK


def test_asrevd03_verify_hook_exits_broken_on_tampered_event() -> None:
    log = _log_with_three_events()
    tampered = list(log.events)
    tampered[1] = replace(tampered[1], action="review.approved")
    assert run_verification(tampered) == _EXIT_CHAIN_BROKEN


def test_asrevd03_verify_hook_exits_broken_on_removed_event() -> None:
    log = _log_with_three_events()
    with_removed = list(log.events)
    del with_removed[1]
    assert run_verification(with_removed) == _EXIT_CHAIN_BROKEN


def test_asrevd03_verify_hook_log_contains_no_question_content(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Alert messages must carry no question content (ASR01-EVD-09, DAT-03)."""
    log = AuditLog()
    log.append(
        actor="author-001",
        action="draft.created",
        object_refs=("artefact-a1",),
        payload={"stem": "What is the capital of India?"},
    )
    tampered = list(log.events)
    tampered[0] = replace(tampered[0], action="tampered.action")

    with caplog.at_level(logging.ERROR, logger="mulyankan_platform.audit.verify_hook"):
        run_verification(tampered)

    for record in caplog.records:
        assert "capital" not in record.message
        assert "India" not in record.message
        assert "stem" not in record.message
