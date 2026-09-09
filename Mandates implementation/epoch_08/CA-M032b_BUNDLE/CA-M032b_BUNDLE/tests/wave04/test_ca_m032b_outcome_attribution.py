from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SRC = ROOT / "packages" / "ca_runtime" / "src"
if str(RUNTIME_SRC) not in sys.path:
    sys.path.insert(0, str(RUNTIME_SRC))

MODULE_PATH = RUNTIME_SRC / "ca_runtime" / "outcome_attribution.py"
spec = importlib.util.spec_from_file_location("ca_runtime.outcome_attribution", MODULE_PATH)
assert spec is not None and spec.loader is not None
outcome_module = importlib.util.module_from_spec(spec)
sys.modules["ca_runtime.outcome_attribution"] = outcome_module
spec.loader.exec_module(outcome_module)

AttributedOutcome = outcome_module.AttributedOutcome
CausalReference = outcome_module.CausalReference
OutcomeAttributionConflictError = outcome_module.OutcomeAttributionConflictError
OutcomeAttributionEngine = outcome_module.OutcomeAttributionEngine
OutcomeAttributionStore = outcome_module.OutcomeAttributionStore
OutcomeIntegrityError = outcome_module.OutcomeIntegrityError
OutcomeValidationError = outcome_module.OutcomeValidationError
UnresolvedAttributionError = outcome_module.UnresolvedAttributionError
UnknownReleaseError = outcome_module.UnknownReleaseError
OutcomeEvent = outcome_module.OutcomeEvent
OutcomeMetrics = outcome_module.OutcomeMetrics


def _sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


ANCHOR_A = CausalReference("collision:tension-a", "rev-3", _sha({"anchor": "a"}))
ANCHOR_B = CausalReference("collision:tension-b", "rev-4", _sha({"anchor": "b"}))
COMP_A = CausalReference("creative:hook-a", "rev-7", _sha({"creative": "a"}))
COMP_B = CausalReference("creative:hook-b", "rev-8", _sha({"creative": "b"}))
AUDIENCE = CausalReference("audience:hypothesis-1", "rev-2", _sha({"audience": 1}))


@pytest.fixture
def manifest() -> dict:
    return {
        "release_id": "release:campaign-1:v1",
        "release_version": "1.0.0",
        "release_state": "RELEASE_SEALED",
        "manifest_sha256": _sha({"release": "v1"}),
        "composition_ref": COMP_A.to_dict(),
        "semantic_refs": [ANCHOR_A.to_dict(), ANCHOR_B.to_dict(), AUDIENCE.to_dict()],
        "source_refs": [],
        "authorization_refs": [],
        "provenance_tree": {
            "node_id": "creative:root",
            "node_type": "release",
            "revision": "rev-1",
            "sha256": _sha({"root": 1}),
            "children": [COMP_B.to_dict() | {"node_id": COMP_B.object_id, "node_type": "creative"}],
        },
    }


@pytest.fixture
def receipt(manifest: dict) -> dict:
    return {
        "receipt_id": "receipt:dist-1",
        "release_id": manifest["release_id"],
        "release_manifest_sha256": manifest["manifest_sha256"],
        "delivery_status": "DELIVERED",
        "destination": {"destination_id": "cdn:1"},
    }


def _event(manifest: dict, receipt: dict, *, event_id="event-1", anchors=(ANCHOR_A,), components=(COMP_A,)) -> OutcomeEvent:
    return OutcomeEvent(
        event_id=event_id,
        release_id=manifest["release_id"],
        release_manifest_sha256=manifest["manifest_sha256"],
        distribution_receipt_id=receipt["receipt_id"],
        campaign_id="campaign-1",
        tension_collision_anchor_refs=anchors,
        creative_component_refs=components,
        audience_hypothesis_refs=(AUDIENCE,),
        metrics=OutcomeMetrics(
            performance={"watch_completion": 0.8, "save_rate": 0.6},
            conversions={"qualified_conversion_rate": 0.4, "signup_rate": 0.2},
        ),
        observed_at="2026-09-08T15:00:00Z",
        source="platform:telemetry",
    )


def test_positive_exact_release_attribution_links_anchor_component_and_audience(manifest, receipt):
    engine = OutcomeAttributionEngine()
    record = engine.ingest(_event(manifest, receipt), release_manifest=manifest, distribution_receipt=receipt)

    assert record.release_id == manifest["release_id"]
    assert record.release_manifest_sha256 == manifest["manifest_sha256"]
    assert record.distribution_receipt_id == receipt["receipt_id"]
    assert record.tension_collision_anchor_refs == (ANCHOR_A,)
    assert record.creative_component_refs == (COMP_A,)
    assert record.audience_hypothesis_refs == (AUDIENCE,)
    assert record.performance_yield == pytest.approx(0.7)
    assert record.conversion_yield == pytest.approx(0.3)
    assert record.outcome_yield == pytest.approx(0.5)
    record.verify()
    assert record.causal_interpretation_allowed is False


def test_unknown_release_is_rejected_even_when_campaign_name_matches(manifest, receipt):
    event = _event(manifest, receipt)
    tampered = replace(event, release_id="release:campaign-1:v2")
    with pytest.raises(UnknownReleaseError):
        OutcomeAttributionEngine().ingest(tampered, release_manifest=manifest, distribution_receipt=receipt)


def test_mutated_manifest_digest_is_rejected(manifest, receipt):
    event = _event(manifest, receipt)
    mutated_event = OutcomeEvent(
        event_id=event.event_id,
        release_id=event.release_id,
        release_manifest_sha256=_sha({"release": "mutated"}),
        distribution_receipt_id=event.distribution_receipt_id,
        campaign_id=event.campaign_id,
        tension_collision_anchor_refs=event.tension_collision_anchor_refs,
        creative_component_refs=event.creative_component_refs,
        audience_hypothesis_refs=event.audience_hypothesis_refs,
        metrics=event.metrics,
        observed_at=event.observed_at,
        source=event.source,
    )
    with pytest.raises(OutcomeIntegrityError):
        OutcomeAttributionEngine().ingest(mutated_event, release_manifest=manifest, distribution_receipt=receipt)


def test_two_releases_under_one_campaign_remain_partitioned():
    manifest_v1 = {
        "release_id": "release:shared-campaign:v1",
        "manifest_sha256": _sha({"v": 1}),
        "composition_ref": COMP_A.to_dict(),
        "semantic_refs": [ANCHOR_A.to_dict(), AUDIENCE.to_dict()],
        "provenance_tree": {"node_id": "root-1", "revision": "r1", "sha256": _sha({"root": 1}), "children": []},
    }
    manifest_v2 = {
        "release_id": "release:shared-campaign:v2",
        "manifest_sha256": _sha({"v": 2}),
        "composition_ref": COMP_B.to_dict(),
        "semantic_refs": [ANCHOR_B.to_dict(), AUDIENCE.to_dict()],
        "provenance_tree": {"node_id": "root-2", "revision": "r2", "sha256": _sha({"root": 2}), "children": []},
    }
    receipt_v1 = {"receipt_id": "receipt:v1", "release_id": manifest_v1["release_id"], "release_manifest_sha256": manifest_v1["manifest_sha256"], "delivery_status": "DELIVERED"}
    receipt_v2 = {"receipt_id": "receipt:v2", "release_id": manifest_v2["release_id"], "release_manifest_sha256": manifest_v2["manifest_sha256"], "delivery_status": "DELIVERED"}

    engine = OutcomeAttributionEngine()
    store = OutcomeAttributionStore()
    r1 = store.append(engine.ingest(_event(manifest_v1, receipt_v1, event_id="e-v1", anchors=(ANCHOR_A,), components=(COMP_A,)), release_manifest=manifest_v1, distribution_receipt=receipt_v1))
    r2 = store.append(engine.ingest(_event(manifest_v2, receipt_v2, event_id="e-v2", anchors=(ANCHOR_B,), components=(COMP_B,)), release_manifest=manifest_v2, distribution_receipt=receipt_v2))

    assert {r.release_id for r in store.all()} == {manifest_v1["release_id"], manifest_v2["release_id"]}
    assert store.query_by_release(manifest_v1["release_id"]) == (r1,)
    assert store.query_by_release(manifest_v2["release_id"]) == (r2,)
    assert store.query_by_anchor(ANCHOR_A) == (r1,)
    assert store.query_by_anchor(ANCHOR_B) == (r2,)


def test_unresolved_anchor_reference_fails_closed(manifest, receipt):
    unknown_anchor = CausalReference("collision:unknown", "rev-1", _sha({"unknown": 1}))
    with pytest.raises(UnresolvedAttributionError):
        OutcomeAttributionEngine().ingest(
            _event(manifest, receipt, anchors=(unknown_anchor,)),
            release_manifest=manifest,
            distribution_receipt=receipt,
        )


def test_unresolved_component_reference_fails_closed(manifest, receipt):
    unknown_component = CausalReference("creative:unknown", "rev-9", _sha({"unknown": 9}))
    with pytest.raises(UnresolvedAttributionError):
        OutcomeAttributionEngine().ingest(
            _event(manifest, receipt, components=(unknown_component,)),
            release_manifest=manifest,
            distribution_receipt=receipt,
        )


def test_non_delivered_distribution_receipt_is_not_eligible(manifest, receipt):
    failed_receipt = {**receipt, "delivery_status": "FAILED"}
    with pytest.raises(OutcomeIntegrityError, match="DELIVERED"):
        OutcomeAttributionEngine().ingest(_event(manifest, failed_receipt), release_manifest=manifest, distribution_receipt=failed_receipt)


def test_duplicate_event_is_idempotent_and_conflict_is_rejected(manifest, receipt):
    engine = OutcomeAttributionEngine()
    store = OutcomeAttributionStore()
    record = engine.ingest(_event(manifest, receipt), release_manifest=manifest, distribution_receipt=receipt)
    assert store.append(record) is record
    assert store.append(record) is record

    altered_record = replace(record, event_sha256=_sha({"changed": True}))
    altered_record = replace(
        altered_record,
        record_sha256=outcome_module._payload_digest(altered_record.unsigned_payload()),
    )
    with pytest.raises(OutcomeAttributionConflictError):
        store.append(altered_record)


def test_json_persistence_reload_preserves_records_and_digest(manifest, receipt, tmp_path):
    engine = OutcomeAttributionEngine()
    store = OutcomeAttributionStore()
    original = store.append(engine.ingest(_event(manifest, receipt), release_manifest=manifest, distribution_receipt=receipt))
    path = store.save(tmp_path / "outcomes.json")
    reloaded = OutcomeAttributionStore.load(path)
    restored = reloaded.get(original.event_id)
    assert restored is not None
    assert restored.to_dict() == original.to_dict()
    restored.verify()


def test_trace_proves_exact_causal_chain_without_claiming_causality(manifest, receipt):
    engine = OutcomeAttributionEngine()
    store = OutcomeAttributionStore()
    record = store.append(engine.ingest(_event(manifest, receipt), release_manifest=manifest, distribution_receipt=receipt))
    trace = store.trace(record.event_id)

    assert trace["release"]["release_id"] == manifest["release_id"]
    assert trace["distribution"]["receipt_id"] == receipt["receipt_id"]
    assert trace["causal_lineage"]["tension_collision_anchors"][0]["object_id"] == ANCHOR_A.object_id
    assert trace["causal_lineage"]["creative_components"][0]["object_id"] == COMP_A.object_id
    assert trace["observed_metrics"]["causal_interpretation_allowed"] is False


def test_anchor_and_component_aggregate_math_and_correlation(manifest, receipt):
    engine = OutcomeAttributionEngine()
    store = OutcomeAttributionStore()
    e1 = _event(manifest, receipt, event_id="e-1", anchors=(ANCHOR_A,), components=(COMP_A,))
    e2 = _event(manifest, receipt, event_id="e-2", anchors=(ANCHOR_A, ANCHOR_B), components=(COMP_A, COMP_B))
    # Change only normalized metrics so the release/causal identity stays exact.
    e2 = OutcomeEvent(
        event_id=e2.event_id,
        release_id=e2.release_id,
        release_manifest_sha256=e2.release_manifest_sha256,
        distribution_receipt_id=e2.distribution_receipt_id,
        campaign_id=e2.campaign_id,
        tension_collision_anchor_refs=e2.tension_collision_anchor_refs,
        creative_component_refs=e2.creative_component_refs,
        audience_hypothesis_refs=e2.audience_hypothesis_refs,
        metrics=OutcomeMetrics(performance={"watch_completion": 1.0}, conversions={"qualified_conversion_rate": 1.0}),
        observed_at=e2.observed_at,
        source=e2.source,
    )
    store.append(engine.ingest(e1, release_manifest=manifest, distribution_receipt=receipt))
    store.append(engine.ingest(e2, release_manifest=manifest, distribution_receipt=receipt))

    anchor_agg = store.aggregate_for_reference(ANCHOR_A, reference_kind="ANCHOR")
    component_agg = store.aggregate_for_reference(COMP_A, reference_kind="COMPONENT")
    assert anchor_agg.observation_count == 2
    assert anchor_agg.attributed_weight == pytest.approx(1.5)
    assert anchor_agg.weighted_outcome_yield == pytest.approx((1.0 * 0.5 + 0.5 * 1.0) / 1.5)
    assert component_agg.observation_count == 2
    assert component_agg.correlation_with_outcome_yield == pytest.approx(-1.0)


def test_metrics_must_be_normalized_to_avoid_hidden_scale_weighting():
    with pytest.raises(OutcomeValidationError):
        OutcomeMetrics(performance={"views": 1000.0}, conversions={"conversion_rate": 0.2})
