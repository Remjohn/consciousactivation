"""Unit tests for CA-IMPL-02 one-aggregate authority cutover (MC-CAE-MED-001).

Covers the deterministic pure layer of the staged cutover verifier: disposable
fixture construction, the contract Section 4 / crosswalk Section 2.5 transform
rules, deterministic CAE identity derivation, and the field/scope-aware
reconciliation engine including its adversarial swapped-scope detection.
"""

from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts" / "cae" / "implementation"))

from verify_ca_impl_02_staging import (  # noqa: E402
    ReconciliationMismatch,
    TransformValidationError,
    build_disposable_source_fixture,
    derive_cae_identity,
    reconcile_media_records,
    transform_manifest,
)


WS_A = "11111111-1111-1111-1111-111111111111"
WS_B = "22222222-2222-2222-2222-222222222222"


def _fixture() -> dict:
    return build_disposable_source_fixture(b"unit-seed" * 8)


def _registered(
    asset_id: str,
    workspace_id: str,
    fixture: dict,
    *,
    storage_path: str = "p/a.bin",
    has_receipt: bool = True,
) -> dict:
    return {
        "media_asset_id": asset_id,
        "workspace_id": workspace_id,
        "canonical_sha256": fixture["sha256"],
        "byte_size": fixture["byte_size"],
        "mime_type": fixture["media_type"],
        "storage_path": storage_path,
        "lifecycle_state": "VERIFIED",
        "has_receipt": has_receipt,
    }


def test_fixture_is_deterministic_and_self_consistent() -> None:
    f1 = build_disposable_source_fixture(b"seed")
    f2 = build_disposable_source_fixture(b"seed")
    assert f1["raw_bytes"] == f2["raw_bytes"]
    assert f1["sha256"] == f2["sha256"]
    assert f1["byte_size"] == len(f1["raw_bytes"]) > 0


def test_transform_recomputes_hash_from_raw_bytes() -> None:
    fixture = _fixture()
    transformed = transform_manifest(
        workspace_id=WS_A, project_id="proj-1", filename="intake.wav", fixture=fixture
    )
    assert transformed["logical_uri"] == f"workspace://{WS_A}/proj-1/intake.wav"
    assert transformed["byte_size"] == fixture["byte_size"]
    assert transformed["media_type"] == fixture["media_type"]


def test_transform_rejects_empty_scope() -> None:
    fixture = _fixture()
    with pytest.raises(TransformValidationError):
        transform_manifest(workspace_id="", project_id="proj-1", filename="x.wav", fixture=fixture)
    with pytest.raises(TransformValidationError):
        transform_manifest(workspace_id=WS_A, project_id="   ", filename="x.wav", fixture=fixture)


def test_transform_rejects_corrupt_bytes_quar_med_001() -> None:
    fixture = _fixture()
    bad = {**fixture, "sha256": "f" * 64}
    with pytest.raises(TransformValidationError):
        transform_manifest(workspace_id=WS_A, project_id="proj-1", filename="x.wav", fixture=bad)
    bad_size = {**fixture, "byte_size": fixture["byte_size"] + 1}
    with pytest.raises(TransformValidationError):
        transform_manifest(workspace_id=WS_A, project_id="proj-1", filename="x.wav", fixture=bad_size)


def test_identity_is_deterministic_and_workspace_scoped() -> None:
    fixture = _fixture()
    a1 = derive_cae_identity(WS_A, fixture["sha256"], fixture["media_type"])
    a2 = derive_cae_identity(WS_A, fixture["sha256"], fixture["media_type"])
    b = derive_cae_identity(WS_B, fixture["sha256"], fixture["media_type"])
    assert a1 == a2 and a1 != b and len(a1) == 32


def _observed(record: dict) -> dict:
    return dict(record)


def test_reconciliation_honest_match_passes() -> None:
    fixture = _fixture()
    expected = [_registered(str(uuid4()), WS_A, fixture)]
    mismatches = reconcile_media_records(expected, [_observed(expected[0])])
    assert mismatches == []


def test_reconciliation_detects_swapped_scope_despite_equal_counts() -> None:
    fixture = _fixture()
    rec_a = _registered(str(uuid4()), WS_A, fixture)
    swapped_target = {**rec_a, "workspace_id": WS_B}  # same row id, wrong tenant
    mismatches = reconcile_media_records([rec_a], [swapped_target])
    assert any(m.check_name == "SCOPE_SWAPPED" for m in mismatches)


def test_reconciliation_flags_missing_receipt_lineage() -> None:
    fixture = _fixture()
    record = _registered(str(uuid4()), WS_A, fixture, has_receipt=True)
    observed = {**record, "has_receipt": False}
    mismatches = reconcile_media_records([record], [observed])
    assert any(m.check_name == "LINEAGE_MISSING_RECEIPT" for m in mismatches)


def test_reconciliation_flags_unexpected_target_row() -> None:
    fixture = _fixture()
    ghost = _registered(str(uuid4()), WS_A, fixture)
    mismatches = reconcile_media_records([], [ghost])
    assert any(m.check_name == "UNEXPECTED_TARGET_ROW" for m in mismatches)


def test_reconciliation_reports_field_mismatch_detail() -> None:
    fixture = _fixture()
    record = _registered(str(uuid4()), WS_A, fixture)
    tampered = {**record, "canonical_sha256": "a" * 64}
    mismatches = reconcile_media_records([record], [tampered])
    assert any(m.check_name == "FIELD_MISMATCH:canonical_sha256" for m in mismatches)
    assert all(isinstance(m, ReconciliationMismatch) for m in mismatches)
