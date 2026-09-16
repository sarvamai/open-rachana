"""The committed local stack under deploy/dev stays consistent with the code:
the Collector's redaction list covers the in-process allowlists, and the
Grafana dashboards are valid, stable and point only at the stack's own
datasources (spec §6.2). Grafana is a development tool; nothing here is a
dependency of the system."""

import json
from pathlib import Path

import yaml
from mulyankan_platform.observability.guard import (
    ALLOWED_LOG_ATTRIBUTES,
    ALLOWED_METRIC_ATTRIBUTES,
    ALLOWED_SPAN_ATTRIBUTES,
)

ROOT = Path(__file__).resolve().parents[3]
DEV = ROOT / "deploy/dev"
DASHBOARDS = sorted((DEV / "grafana/dashboards").glob("*.json"))
DATASOURCE_UIDS = {"prometheus", "tempo", "loki"}  # what grafana/otel-lgtm provisions


def test_collector_redaction_covers_the_python_allowlists() -> None:
    config = yaml.safe_load((DEV / "otel-collector.yaml").read_text(encoding="utf-8"))
    allowed = set(config["processors"]["redaction"]["allowed_keys"])
    ignored = set(config["processors"]["redaction"]["ignored_keys"])

    assert (
        ALLOWED_SPAN_ATTRIBUTES | ALLOWED_LOG_ATTRIBUTES | ALLOWED_METRIC_ATTRIBUTES
        <= allowed
    )
    for key in (
        "url.query",
        "user_agent.original",
        "exception.message",
        "enduser.id",
        "db.query.text",
    ):
        assert key not in allowed
    assert {
        "service.name",
        "service.namespace",
        "deployment.environment.name",
    } <= ignored
    for name in ("traces", "metrics", "logs"):
        assert "redaction" in config["service"]["pipelines"][name]["processors"]


def test_dashboard_provider_points_at_the_mounted_directory() -> None:
    provider = yaml.safe_load(
        (DEV / "grafana/dashboards.yaml").read_text(encoding="utf-8")
    )
    compose = yaml.safe_load((DEV / "compose.yaml").read_text(encoding="utf-8"))

    (entry,) = provider["providers"]
    assert entry["type"] == "file"
    mounts = compose["services"]["lgtm"]["volumes"]
    assert f"./grafana/dashboards:{entry['options']['path']}:ro" in mounts
    assert any(
        m.startswith("./grafana/dashboards.yaml:") and "provisioning/dashboards/" in m
        for m in mounts
    )


def test_dashboards_are_valid_and_self_contained() -> None:
    assert len(DASHBOARDS) == 3
    uids = set()
    for path in DASHBOARDS:
        dashboard = json.loads(path.read_text(encoding="utf-8"))
        assert dashboard["uid"] and dashboard["title"], path.name
        assert dashboard["uid"] not in uids, path.name
        uids.add(dashboard["uid"])
        assert "mulyankan" in dashboard["tags"], path.name
        assert dashboard["panels"], path.name
        for panel in dashboard["panels"]:
            for target in panel.get("targets", []):
                assert target["datasource"]["uid"] in DATASOURCE_UIDS, (
                    path.name,
                    panel["title"],
                )
        text = path.read_text(encoding="utf-8")
        assert (
            "url_path" not in text and "url_query" not in text
        ), path.name  # never keyed on content
