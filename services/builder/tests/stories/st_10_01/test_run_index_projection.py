import pytest

from cmf_builder.application.run_index_projection import (
    GateState,
    RunEvidenceRecord,
    RunIndexError,
    RunLifecycleState,
    build_run_index,
    detect_stale_records,
)


def record(run="run:1", **overrides):
    values = {
        "run_identity": run,
        "workflow_profile_identity": "profile:dev",
        "harness_identity": "harness:synthetic_text_normalization_v1",
        "category_identity": "category:generic",
        "target_identity": "target:local",
        "maturity_state": "development_validated",
        "implementation_status": GateState.PASS_,
        "evidence_status": GateState.PENDING,
        "authority_status": GateState.PASS_,
        "production_status": GateState.PENDING,
        "certification_status": GateState.PENDING,
        "current_phase": "phase:workflow",
        "current_node": "node:validation",
        "lifecycle_state": RunLifecycleState.ACTIVE,
        "latest_checkpoint_ref": "checkpoint:1",
        "receipt_refs": ("receipt:implementation",),
        "evidence_refs": ("evidence:offline",),
        "updated_at_utc": "2026-07-17T00:00:00Z",
        "freshness_ref": "freshness:active",
        "source_receipt_hash": "a" * 64,
    }
    values.update(overrides)
    return RunEvidenceRecord(**values)


def test_run_index_projects_traceable_entries_with_separate_status_gates():
    projection = build_run_index((record("run:b"), record("run:a")), page_size=10)

    assert [item.run_identity for item in projection.records] == ["run:a", "run:b"]
    assert projection.total_records == 2
    assert projection.projection_identity
    first = projection.as_dict()["records"][0]
    assert first["implementation_status"] == "PASS"
    assert first["evidence_status"] == "PENDING"
    assert first["production_status"] == "PENDING"
    assert first["certification_status"] == "PENDING"


def test_run_index_filtering_sorting_and_pagination_are_deterministic():
    records = (
        record("run:1", category_identity="category:generic"),
        record("run:2", category_identity="category:activative"),
        record("run:3", category_identity="category:generic"),
    )

    projection = build_run_index(records, filters={"category_identity": "category:generic"}, sort_key="run_identity", page=2, page_size=1)

    assert projection.total_records == 2
    assert [item.run_identity for item in projection.records] == ["run:3"]


def test_run_index_rejects_false_production_or_certification_claims():
    with pytest.raises(RunIndexError) as production:
        record(production_status=GateState.PASS_)
    assert production.value.code == "FALSE_PRODUCTION_OR_CERTIFICATION_CLAIM"

    with pytest.raises(RunIndexError) as certified:
        record(certification_status=GateState.PASS_)
    assert certified.value.code == "FALSE_PRODUCTION_OR_CERTIFICATION_CLAIM"


def test_partial_and_redacted_records_remain_explicit():
    redacted = record(partial=True, redacted_fields=("authority_detail",))
    projection = build_run_index((redacted,))

    projected = projection.as_dict()["records"][0]
    assert projected["partial"] is True
    assert projected["redacted_fields"] == ["authority_detail"]


def test_stale_detection_uses_active_receipt_hashes_without_mutating_history():
    active = record("run:active", source_receipt_hash="a" * 64)
    stale = record("run:stale", source_receipt_hash="b" * 64)
    explicitly_stale = record("run:explicit", lifecycle_state=RunLifecycleState.STALE, source_receipt_hash="a" * 64)

    stale_refs = detect_stale_records((active, stale, explicitly_stale), {"a" * 64})

    assert stale.record_identity in stale_refs
    assert explicitly_stale.record_identity in stale_refs
    assert active.record_identity not in stale_refs


def test_unsupported_filters_and_sorts_fail_closed():
    with pytest.raises(RunIndexError) as filtering:
        build_run_index((record(),), filters={"secret": "value"})
    assert filtering.value.code == "UNSUPPORTED_RUN_INDEX_FILTER"

    with pytest.raises(RunIndexError) as sorting:
        build_run_index((record(),), sort_key="absolute_path")
    assert sorting.value.code == "UNSUPPORTED_RUN_INDEX_SORT"
