"""CA-M020 acceptance tests for first-class, cryptographically verifiable receipts.

These tests intentionally are not executed during bundle creation per the
execution-agent instruction.  They are designed for the repository's actual
InterviewRepository/Application persistence boundary.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
for p in reversed(
    [
        ROOT / "packages/ca_contracts/src",
        ROOT / "packages/ca_runtime/src",
        ROOT / "services/interview/src",
    ]
):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

from ca_contracts import bytes_sha256
from conscious_activations_interview_expression.application import (
    InterviewExpressionApplication,
)
from conscious_activations_interview_expression.domain import make_media_asset
from conscious_activations_interview_expression.errors import ValidationError
from conscious_activations_interview_expression.reaction_receipts import (
    CA_M020,
    FR_020,
    HASH_ALGORITHM,
    ReactionReceiptEvidenceService,
)


_FIXTURE_MEDIA = b"ca-m020-sovereign-interview-media"
_FIXTURE_TIMESTAMP = "2026-09-08T08:30:00Z"


def _ref(stored: dict) -> dict[str, str]:
    obj = stored["object"] if "object" in stored else stored
    return {
        "object_id": obj["object_id"],
        "version": obj["version"],
        "sha256": obj["sha256"],
    }


def _make_app(tmp_path: Path) -> InterviewExpressionApplication:
    app = InterviewExpressionApplication(tmp_path / "ca_m020.sqlite3")
    app.initialize()
    return app


def _media_asset() -> dict:
    return make_media_asset(
        logical_uri="workspace://fixture/ca-m020-interview.mp4",
        sha256=bytes_sha256(_FIXTURE_MEDIA),
        bytes_count=len(_FIXTURE_MEDIA),
        media_type="video/mp4",
        technical={
            "probe_status": "DECLARED_TEST",
            "duration_us": 6_000_000,
            "duration_ms": 6_000,
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "fixture",
                    "time_base": {"numerator": 1, "denominator": 90_000},
                    "width": 1920,
                    "height": 1080,
                }
            ],
            "limitations": ["TEST_FIXTURE"],
        },
    )


def _package(app: InterviewExpressionApplication, media: dict) -> dict:
    return app.source_packages.admit(
        {
            "workspace_id": "ws-m020",
            "project_id": "project-m020",
            "admission_mode": "IMPORTED",
            "source_kind": "INTERVIEW_EXPRESSION",
            "media_assets": [media],
            "source_authority": {
                "operator_id": "operator-m020",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-m020",
            },
            "planning_lineage": {"state": "ABSENT_NOT_CREATED"},
        },
        idempotency_key="m020:package",
    )


def _coordinates(media: dict, *, start_us: int = 1_000_000, end_us: int = 2_000_000) -> dict:
    # 30 fps fixture, expressed using the exact CA-M021 coordinate shape.  The
    # byte span is intentionally within the declared fixture byte count.
    return {
        "media_asset_id": media["asset_id"],
        "media_sha256": media["sha256"],
        "byte_offset_start": 1,
        "byte_offset_end": min(len(_FIXTURE_MEDIA), 10),
        "frame_number_start": 30,
        "frame_number_end": 59,
        "microsecond_start": start_us,
        "microsecond_end": end_us,
    }


def _service_and_package(tmp_path: Path):
    app = _make_app(tmp_path)
    media = _media_asset()
    admitted = _package(app, media)
    return app, media, _ref(admitted), ReactionReceiptEvidenceService(app.repository)


def _admit_receipt(service: ReactionReceiptEvidenceService, package_ref: dict, media: dict, **overrides):
    kwargs = {
        "source_package_ref": package_ref,
        "actor_id": "actor-m020",
        "actor_timestamp_utc": _FIXTURE_TIMESTAMP,
        "reaction_kind": "MICRO_EXPRESSION",
        "reaction": {"cue": "brow_raise", "intensity": 0.7},
        "media_coordinates": _coordinates(media),
        "observation_refs": [],
        "idempotency_key": "m020:receipt",
    }
    kwargs.update(overrides)
    return service.admit(**kwargs)


# ---------------------------------------------------------------------------
# SCHEMA / invariant surface
# ---------------------------------------------------------------------------


def test_receipt_schema_contains_first_class_identity_timestamp_and_media_proof(tmp_path):
    _, media, package_ref, service = _service_and_package(tmp_path)
    result = _admit_receipt(service, package_ref, media)
    payload = result["object"]["payload"]

    assert payload["reaction_receipt_id"].startswith("ie:reaction-receipt:")
    assert payload["version"] == "1.0.0"
    assert payload["evidence_class"] == "FIRST_CLASS_REACTION_RECEIPT"
    assert payload["mandate_id"] == CA_M020
    assert payload["invariant_id"] == FR_020
    assert payload["actor_id"] == "actor-m020"
    assert payload["actor_timestamp_utc"] == _FIXTURE_TIMESTAMP
    assert payload["media_coordinates"]["media_sha256"] == media["sha256"]
    assert payload["proof"]["algorithm"] == HASH_ALGORITHM
    assert len(payload["proof"]["proof_sha256"]) == 64


# ---------------------------------------------------------------------------
# EXECUTABLE positive path / real persistence boundary
# ---------------------------------------------------------------------------


def test_valid_reaction_is_admitted_and_verifies_against_exact_source_revision(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    result = _admit_receipt(service, package_ref, media)

    verification = service.verify(_ref(result))

    assert result["object"]["object_type"] == "reaction_receipt"
    assert result["object"]["lifecycle_state"] == "VERIFIED"
    assert verification["status"] == "VERIFIED"
    assert verification["cryptographic_proof_verified"] is True
    assert verification["first_class_evidence"] is True
    assert verification["source_package_ref"] == package_ref

    descendants = app.repository.descendants(package_ref["object_id"])
    assert any(
        edge["child_id"] == result["object"]["object_id"]
        and edge["relation"] == "source_of_reaction_receipt"
        for edge in descendants
    )

    bound = app.source_packages.bind_component(
        package_ref["object_id"],
        "reaction_receipts",
        _ref(result),
        idempotency_key="m020:bind-receipt",
    )
    component = bound["object"]["payload"]["components"]["reaction_receipts"]
    assert component["state"] == "BOUND"
    assert component["ref"] == _ref(result)


def test_receipt_ref_is_content_addressed_and_survives_idempotent_replay(tmp_path):
    _, media, package_ref, service = _service_and_package(tmp_path)
    first = _admit_receipt(service, package_ref, media)
    second = _admit_receipt(service, package_ref, media)

    assert first["object"]["object_id"] == second["object"]["object_id"]
    assert first["object"]["sha256"] == second["object"]["sha256"]
    assert second["idempotent_replay"] is True


# ---------------------------------------------------------------------------
# EXECUTABLE negative path / fail closed
# ---------------------------------------------------------------------------


def test_unlinked_reaction_annotation_cannot_be_upgraded_by_a_boolean_flag(tmp_path):
    """False-proof countercase: a label is not evidence without coordinates."""
    app = _make_app(tmp_path)
    media = _media_asset()
    admitted = _package(app, media)
    package_ref = _ref(admitted)
    service = ReactionReceiptEvidenceService(app.repository)

    with pytest.raises(ValidationError, match="media_coordinates"):
        service.admit(
            source_package_ref=package_ref,
            actor_id="actor-m020",
            actor_timestamp_utc=_FIXTURE_TIMESTAMP,
            reaction_kind="PAUSE",
            reaction={"linked": True, "description": "pause"},
            media_coordinates=None,  # type: ignore[arg-type]
            idempotency_key="m020:no-coordinates",
        )

    assert app.repository.list_objects("reaction_receipt") == []


def test_mismatched_media_digest_is_rejected_before_persistence(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    coords = _coordinates(media)
    coords["media_sha256"] = "a" * 64

    with pytest.raises(ValidationError, match="media coordinates"):
        _admit_receipt(
            service,
            package_ref,
            media,
            media_coordinates=coords,
            idempotency_key="m020:wrong-media-digest",
        )

    assert app.repository.list_objects("reaction_receipt") == []


def test_out_of_bounds_coordinates_are_rejected_fail_closed(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    coords = _coordinates(media, start_us=5_500_000, end_us=6_500_000)

    with pytest.raises(ValidationError, match="exceeds raw source duration"):
        _admit_receipt(
            service,
            package_ref,
            media,
            media_coordinates=coords,
            idempotency_key="m020:duration-fail",
        )

    assert app.repository.list_objects("reaction_receipt") == []


def test_tampered_actor_timestamp_cannot_verify_as_the_original_receipt(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    result = _admit_receipt(service, package_ref, media)

    # Deliberately bypass the service boundary to model database-level tamper;
    # verification must detect the mismatch rather than trust a linked flag.
    tampered = dict(result["object"]["payload"])
    tampered["actor_timestamp_utc"] = "2026-09-08T08:31:00Z"
    app.repository.store_object(
        "reaction_receipt",
        tampered,
        object_id=result["object"]["object_id"],
        idempotency_key="m020:tamper-timestamp",
        expected_revision=result["object"]["revision"],
        lifecycle_state="VERIFIED",
    )

    with pytest.raises(ValidationError, match="content address"):
        service.verify(_ref(app.repository.get_object(result["object"]["object_id"])))


def test_tampered_coordinates_cannot_verify_as_the_original_receipt(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    result = _admit_receipt(service, package_ref, media)

    tampered = dict(result["object"]["payload"])
    tampered["media_coordinates"] = dict(tampered["media_coordinates"])
    tampered["media_coordinates"]["microsecond_start"] += 1
    app.repository.store_object(
        "reaction_receipt",
        tampered,
        object_id=result["object"]["object_id"],
        idempotency_key="m020:tamper-coordinates",
        expected_revision=result["object"]["revision"],
        lifecycle_state="VERIFIED",
    )

    with pytest.raises(ValidationError, match="content address"):
        service.verify(_ref(app.repository.get_object(result["object"]["object_id"])))


def test_source_media_dissociation_is_rejected_even_when_a_link_flag_is_present(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    coords = _coordinates(media)
    coords["media_asset_id"] = "ie:media:different-asset"

    with pytest.raises(ValidationError, match="not bound to a media asset"):
        _admit_receipt(
            service,
            package_ref,
            media,
            media_coordinates=coords,
            idempotency_key="m020:dissociated-media",
        )

    assert app.repository.list_objects("reaction_receipt") == []


# ---------------------------------------------------------------------------
# Regression / evidence-chain behavior
# ---------------------------------------------------------------------------


def test_observation_refs_are_first_class_supporting_edges_not_substitutes_for_media_binding(tmp_path):
    app, media, package_ref, service = _service_and_package(tmp_path)
    fake_observation = {
        "object_id": "ie:reaction-observation:test-support",
        "version": "1.0.0",
        "sha256": "b" * 64,
    }
    result = _admit_receipt(
        service,
        package_ref,
        media,
        observation_refs=[fake_observation],
        idempotency_key="m020:with-observation",
    )

    assert result["object"]["payload"]["observation_state"] == "SUPPORTED_BY_OBSERVATIONS"
    assert result["object"]["payload"]["media_coordinates"]["media_sha256"] == media["sha256"]
    assert any(
        edge["child_id"] == result["object"]["object_id"]
        and edge["relation"] == "supports_reaction_receipt"
        for edge in app.repository.descendants(fake_observation["object_id"])
    )


def test_legacy_boolean_metadata_cannot_replace_required_coordinate_proof(tmp_path):
    _, media, package_ref, service = _service_and_package(tmp_path)
    coords = _coordinates(media)
    result = _admit_receipt(
        service,
        package_ref,
        media,
        reaction={"linked": False, "cue": "vocal_pitch_change"},
        media_coordinates=coords,
        idempotency_key="m020:boolean-ignored",
    )

    verified = service.verify(_ref(result))
    assert verified["cryptographic_proof_verified"] is True
    assert verified["media_coordinates"] == coords | {
        "stream_metadata_fingerprint": [
            {
                "index": 0,
                "codec_type": "video",
                "time_base": {"numerator": 1, "denominator": 90_000},
            }
        ]
    }
