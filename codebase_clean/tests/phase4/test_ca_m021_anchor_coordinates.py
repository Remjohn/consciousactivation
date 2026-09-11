"""
CA-M021 — Anchor Hits as Exact Coordinate References
Tests for FR-ANCH-001

Verification matrix
===================
SCHEMA
  test_anchor_coordinate_schema_fields_are_present
  test_anchor_coordinate_mandate_id_stamped

EXECUTABLE — positive path
  test_exact_coordinates_with_known_duration_are_accepted
  test_exact_coordinates_audio_only_stream_no_frame_numbers_accepted_when_same_frame
  test_multiple_evidence_refs_are_accepted_and_sorted
  test_limitations_are_forwarded_when_caller_supplies_them
  test_duration_in_microseconds_is_preferred_over_milliseconds
  test_idempotent_admission_returns_same_object

EXECUTABLE — negative path (fail-closed)
  test_approximate_millisecond_span_is_rejected
  test_free_text_interpretive_string_is_rejected
  test_missing_byte_offset_field_is_rejected
  test_missing_frame_number_field_is_rejected
  test_missing_microsecond_field_is_rejected
  test_inverted_byte_span_is_rejected
  test_inverted_microsecond_span_is_rejected
  test_frame_number_end_less_than_start_is_rejected
  test_microsecond_end_exceeds_source_duration_is_rejected
  test_coordinate_referencing_wrong_media_asset_id_is_rejected
  test_coordinate_referencing_wrong_media_sha256_is_rejected
  test_extra_field_in_coordinates_is_rejected
  test_non_sha256_media_digest_is_rejected
  test_zero_length_byte_span_is_rejected
  test_zero_length_microsecond_span_is_rejected
  test_stale_source_package_ref_is_rejected
  test_anchor_kind_empty_string_is_rejected

REGRESSION — adjacent behaviour not broken
  test_existing_anchor_hit_via_expression_service_still_works
  test_verbatim_evidence_service_still_works

INTEGRATION — real domain boundary
  test_list_for_source_returns_all_committed_coordinates
  test_get_by_ref_returns_exact_payload
  test_validation_block_records_exact_coordinate_flags
  test_receipt_contains_exact_object_ref

FALSE-PROOF countercase
  test_millisecond_start_end_pair_labelled_anchor_is_explicitly_rejected
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path bootstrap (mirrors tests/phase4/_support.py)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
for _p in reversed(
    [
        ROOT / "packages/ca_contracts/src",
        ROOT / "packages/ca_runtime/src",
        ROOT / "services/air/src",
        ROOT / "services/pipeline/src",
        ROOT / "services/interview/src",
    ]
):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)

from ca_contracts import bytes_sha256
from conscious_activations_interview_expression.application import (
    InterviewExpressionApplication,
)
from conscious_activations_interview_expression.anchor_coordinates import (
    ANCHOR_COORDINATE_MANDATE,
    ANCHOR_COORDINATE_SCHEMA_VERSION,
    reject_approximate_anchor,
    require_exact_anchor_coordinates,
)
from conscious_activations_interview_expression.domain import make_media_asset, make_source_span
from conscious_activations_interview_expression.errors import ValidationError

# ---------------------------------------------------------------------------
# Shared fixture helpers
# ---------------------------------------------------------------------------

_FIXTURE_MEDIA_BYTES = b"fixture-talking-head-media"
_FIXTURE_DURATION_MS = 6000
_FIXTURE_DURATION_US = _FIXTURE_DURATION_MS * 1000  # 6_000_000 µs


def _make_app(tmp_path: Path) -> InterviewExpressionApplication:
    app = InterviewExpressionApplication(tmp_path / "ie_m021.sqlite3")
    app.initialize()
    return app


def _make_media_asset_with_us(duration_us: int = _FIXTURE_DURATION_US) -> dict:
    """Return a media asset whose technical block carries duration_us."""
    data = _FIXTURE_MEDIA_BYTES
    return make_media_asset(
        logical_uri="workspace://fixture/interview.mp4",
        sha256=bytes_sha256(data),
        bytes_count=len(data),
        media_type="video/mp4",
        technical={
            "probe_status": "DECLARED_TEST",
            "duration_us": duration_us,
            "duration_ms": duration_us // 1000,
            "streams": [
                {
                    "index": 0,
                    "codec_type": "video",
                    "codec_name": "fixture",
                    "width": 1080,
                    "height": 1920,
                    "frame_rate": {"numerator": 30, "denominator": 1},
                }
            ],
            "limitations": ["TEST_FIXTURE"],
        },
    )


def _admit_package(app: InterviewExpressionApplication, media: dict) -> dict:
    admitted = app.source_packages.admit(
        {
            "workspace_id": "ws",
            "project_id": "prj",
            "admission_mode": "IMPORTED",
            "source_kind": "INTERVIEW_EXPRESSION",
            "media_assets": [media],
            "source_authority": {
                "operator_id": "op",
                "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-m021",
            },
            "planning_lineage": {"state": "ABSENT_NOT_CREATED"},
        },
        idempotency_key="admit-m021",
    )
    return admitted


def _ref(stored: dict) -> dict:
    obj = stored["object"] if "object" in stored else stored
    return {
        "object_id": obj["object_id"],
        "version": obj["version"],
        "sha256": obj["sha256"],
    }


def _exact_coords(media: dict, *, us_start: int = 1_000_000, us_end: int = 2_500_000) -> dict:
    """Build a minimal valid exact coordinate block from a media asset."""
    # 30 fps — derive frame numbers from microseconds
    fps = 30
    frame_start = int(us_start * fps / 1_000_000)
    frame_end = int((us_end - 1) * fps / 1_000_000)
    # Byte offsets are declared (sovereign container values would come from
    # ffprobe index; here we use plausible declared values for the test fixture)
    byte_start = us_start * 512 // 1_000_000  # ~512 bytes/µs placeholder
    byte_end = us_end * 512 // 1_000_000
    return {
        "media_asset_id": media["asset_id"],
        "media_sha256": media["sha256"],
        "byte_offset_start": byte_start,
        "byte_offset_end": byte_end,
        "frame_number_start": frame_start,
        "frame_number_end": frame_end,
        "microsecond_start": us_start,
        "microsecond_end": us_end,
    }


def _admit_coord(
    app: InterviewExpressionApplication,
    package_ref: dict,
    media: dict,
    *,
    key: str = "m021:coord",
    **overrides,
) -> dict:
    coords = _exact_coords(media)
    coords.update(overrides.pop("coords_override", {}))
    return app.anchor_coordinates.admit(
        source_package_ref=package_ref,
        anchor_kind="VERBATIM_QUOTE",
        anchor_coordinates=coords,
        evidence_refs=[],
        actor_id="m021-test-actor",
        idempotency_key=key,
        **overrides,
    )


# ===========================================================================
# SCHEMA tests
# ===========================================================================


def test_anchor_coordinate_schema_fields_are_present(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media)
    payload = result["object"]["payload"]

    assert payload["anchor_coordinate_id"].startswith("ie:anchor-coordinate:")
    assert payload["version"] == ANCHOR_COORDINATE_SCHEMA_VERSION
    assert payload["mandate_id"] == ANCHOR_COORDINATE_MANDATE
    assert payload["schema_version"] == ANCHOR_COORDINATE_SCHEMA_VERSION
    assert payload["anchor_kind"] == "VERBATIM_QUOTE"
    assert "anchor_coordinates" in payload
    coords = payload["anchor_coordinates"]
    for field in (
        "media_asset_id",
        "media_sha256",
        "byte_offset_start",
        "byte_offset_end",
        "frame_number_start",
        "frame_number_end",
        "microsecond_start",
        "microsecond_end",
    ):
        assert field in coords, f"missing coord field: {field}"


def test_anchor_coordinate_mandate_id_stamped(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media)
    payload = result["object"]["payload"]

    assert payload["mandate_id"] == "CA-M021"
    assert result["receipt"]["mandate_id"] == "CA-M021"


# ===========================================================================
# EXECUTABLE — positive path
# ===========================================================================


def test_exact_coordinates_with_known_duration_are_accepted(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media)
    payload = result["object"]["payload"]

    assert payload["validation"]["status"] == "PASS"
    assert payload["validation"]["exact_coordinates"] is True
    assert payload["validation"]["duration_bound_checked"] is True
    assert payload["lifecycle_state"] == "VALIDATED"


def test_exact_coordinates_audio_only_stream_no_frame_numbers_accepted_when_same_frame(tmp_path):
    """
    Audio-only streams have no video frame number concept.  Frame start == end
    is permitted (single-frame or no-frame anchor).
    """
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    coords = _exact_coords(media)
    coords["frame_number_start"] = 45
    coords["frame_number_end"] = 45  # same frame — valid for audio

    result = app.anchor_coordinates.admit(
        source_package_ref=pkg_ref,
        anchor_kind="EMOTIONAL_CUE",
        anchor_coordinates=coords,
        evidence_refs=[],
        actor_id="m021-audio-actor",
        idempotency_key="m021:audio-coord",
    )
    assert result["object"]["payload"]["validation"]["status"] == "PASS"


def test_multiple_evidence_refs_are_accepted_and_sorted(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    ev1 = {"object_id": "ie:ev:aaaa", "version": "1.0.0", "sha256": "a" * 64}
    ev2 = {"object_id": "ie:ev:bbbb", "version": "1.0.0", "sha256": "b" * 64}

    coords = _exact_coords(media)
    result = app.anchor_coordinates.admit(
        source_package_ref=pkg_ref,
        anchor_kind="REACTION_ANCHOR",
        anchor_coordinates=coords,
        evidence_refs=[ev2, ev1],  # deliberately reversed
        actor_id="m021-multi-ev",
        idempotency_key="m021:multi-ev",
    )
    payload = result["object"]["payload"]
    stored_ids = [r["object_id"] for r in payload["evidence_refs"]]
    assert stored_ids == sorted(stored_ids), "evidence_refs must be stored in sorted order"


def test_limitations_are_forwarded_when_caller_supplies_them(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = app.anchor_coordinates.admit(
        source_package_ref=pkg_ref,
        anchor_kind="VERBATIM_QUOTE",
        anchor_coordinates=_exact_coords(media),
        evidence_refs=[],
        actor_id="m021-lim",
        limitations=["DEVELOPMENT_FIXTURE"],
        idempotency_key="m021:lim",
    )
    assert "DEVELOPMENT_FIXTURE" in result["object"]["payload"]["limitations"]


def test_duration_in_microseconds_is_preferred_over_milliseconds(tmp_path):
    """
    When both duration_us and duration_ms are present, duration_us is
    authoritative.  An anchor within duration_us but exceeding duration_ms
    (if the two were inconsistent) should still pass.
    """
    app = _make_app(tmp_path)
    # Set duration_us = 5_500_000 µs, duration_ms = 5000 ms (slightly
    # inconsistent — duration_us wins)
    data = _FIXTURE_MEDIA_BYTES
    media = make_media_asset(
        logical_uri="workspace://fixture/interview.mp4",
        sha256=bytes_sha256(data),
        bytes_count=len(data),
        media_type="video/mp4",
        technical={
            "probe_status": "DECLARED_TEST",
            "duration_us": 5_500_000,
            "duration_ms": 5000,
            "streams": [],
            "limitations": ["TEST_FIXTURE"],
        },
    )
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    # Anchor end = 5_300_000 µs — within duration_us but "beyond" duration_ms*1000
    coords = _exact_coords(media, us_start=1_000_000, us_end=5_300_000)
    result = app.anchor_coordinates.admit(
        source_package_ref=pkg_ref,
        anchor_kind="VERBATIM_QUOTE",
        anchor_coordinates=coords,
        evidence_refs=[],
        actor_id="m021-dur-us",
        idempotency_key="m021:dur-us",
    )
    assert result["object"]["payload"]["validation"]["status"] == "PASS"


def test_idempotent_admission_returns_same_object(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    first = _admit_coord(app, pkg_ref, media, key="m021:idem")
    second = _admit_coord(app, pkg_ref, media, key="m021:idem")

    assert first["object"]["object_id"] == second["object"]["object_id"]
    assert first["object"]["sha256"] == second["object"]["sha256"]


# ===========================================================================
# EXECUTABLE — negative path (fail-closed)
# ===========================================================================


def test_approximate_millisecond_span_is_rejected():
    """
    An object carrying only start_ms / end_ms is an approximate anchor.
    The explicit guard must fire before any structural validation.
    """
    approximate = {"start_ms": 1000, "end_ms": 3000}
    with pytest.raises(ValidationError) as exc_info:
        reject_approximate_anchor(approximate, name="test_candidate")
    assert exc_info.value.context["classification"] == "FR_ANCH_001_APPROXIMATE_ANCHOR_REJECTED"


def test_free_text_interpretive_string_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        reject_approximate_anchor("The moment when the subject showed fear", name="test_candidate")
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INTERPRETIVE_ANCHOR_REJECTED"


def test_missing_byte_offset_field_is_rejected():
    incomplete = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        # byte_offset_start and byte_offset_end missing
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError):
        require_exact_anchor_coordinates(incomplete)


def test_missing_frame_number_field_is_rejected():
    incomplete = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        # frame_number_start / frame_number_end missing
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError):
        require_exact_anchor_coordinates(incomplete)


def test_missing_microsecond_field_is_rejected():
    incomplete = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 0,
        "frame_number_end": 30,
        # microsecond_start / microsecond_end missing
    }
    with pytest.raises(ValidationError):
        require_exact_anchor_coordinates(incomplete)


def test_inverted_byte_span_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 2048,
        "byte_offset_end": 1024,  # inverted
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError) as exc_info:
        require_exact_anchor_coordinates(coords)
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INVERTED_BYTE_SPAN"


def test_inverted_microsecond_span_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 2_000_000,
        "microsecond_end": 1_000_000,  # inverted
    }
    with pytest.raises(ValidationError) as exc_info:
        require_exact_anchor_coordinates(coords)
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INVERTED_MICROSECOND_SPAN"


def test_frame_number_end_less_than_start_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 60,
        "frame_number_end": 30,  # end < start
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError) as exc_info:
        require_exact_anchor_coordinates(coords)
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INVERTED_FRAME_SPAN"


def test_microsecond_end_exceeds_source_duration_is_rejected(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us(duration_us=5_000_000)  # 5 s
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    coords = _exact_coords(media, us_start=1_000_000, us_end=5_500_001)  # > 5 s

    with pytest.raises(ValidationError) as exc_info:
        app.anchor_coordinates.admit(
            source_package_ref=pkg_ref,
            anchor_kind="VERBATIM_QUOTE",
            anchor_coordinates=coords,
            evidence_refs=[],
            actor_id="m021-overflow",
            idempotency_key="m021:overflow",
        )
    assert exc_info.value.context["classification"] == "FR_ANCH_001_EXCEEDS_SOURCE_DURATION"


def test_coordinate_referencing_wrong_media_asset_id_is_rejected(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    coords = _exact_coords(media)
    coords["media_asset_id"] = "ie:media:does-not-exist"

    with pytest.raises(ValidationError) as exc_info:
        app.anchor_coordinates.admit(
            source_package_ref=pkg_ref,
            anchor_kind="VERBATIM_QUOTE",
            anchor_coordinates=coords,
            evidence_refs=[],
            actor_id="m021-wrong-id",
            idempotency_key="m021:wrong-id",
        )
    assert exc_info.value.context["classification"] == "FR_ANCH_001_MEDIA_NOT_IN_PACKAGE"


def test_coordinate_referencing_wrong_media_sha256_is_rejected(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    coords = _exact_coords(media)
    coords["media_sha256"] = "b" * 64  # wrong digest

    with pytest.raises(ValidationError) as exc_info:
        app.anchor_coordinates.admit(
            source_package_ref=pkg_ref,
            anchor_kind="VERBATIM_QUOTE",
            anchor_coordinates=coords,
            evidence_refs=[],
            actor_id="m021-wrong-sha",
            idempotency_key="m021:wrong-sha",
        )
    assert exc_info.value.context["classification"] == "FR_ANCH_001_MEDIA_NOT_IN_PACKAGE"


def test_extra_field_in_coordinates_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
        "extra_unknown_field": "should fail",  # not in schema
    }
    with pytest.raises(ValidationError):
        require_exact_anchor_coordinates(coords)


def test_non_sha256_media_digest_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "not-a-hex-sha",  # invalid
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError):
        require_exact_anchor_coordinates(coords)


def test_zero_length_byte_span_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 512,
        "byte_offset_end": 512,  # zero length (end == start)
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 0,
        "microsecond_end": 1_000_000,
    }
    with pytest.raises(ValidationError) as exc_info:
        require_exact_anchor_coordinates(coords)
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INVERTED_BYTE_SPAN"


def test_zero_length_microsecond_span_is_rejected():
    coords = {
        "media_asset_id": "ie:media:abc",
        "media_sha256": "a" * 64,
        "byte_offset_start": 0,
        "byte_offset_end": 1024,
        "frame_number_start": 0,
        "frame_number_end": 30,
        "microsecond_start": 1_000_000,
        "microsecond_end": 1_000_000,  # zero length (end == start)
    }
    with pytest.raises(ValidationError) as exc_info:
        require_exact_anchor_coordinates(coords)
    assert exc_info.value.context["classification"] == "FR_ANCH_001_INVERTED_MICROSECOND_SPAN"


def test_stale_source_package_ref_is_rejected(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()

    stale_ref = {
        "object_id": "ie:source-package:does-not-exist",
        "version": "1.0.0",
        "sha256": "c" * 64,
    }

    with pytest.raises(ValidationError) as exc_info:
        app.anchor_coordinates.admit(
            source_package_ref=stale_ref,
            anchor_kind="VERBATIM_QUOTE",
            anchor_coordinates=_exact_coords(media),
            evidence_refs=[],
            actor_id="m021-stale",
            idempotency_key="m021:stale",
        )
    assert exc_info.value.context["classification"] == "FR_ANCH_001_PROVENANCE_ERROR"


def test_anchor_kind_empty_string_is_rejected(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    with pytest.raises(ValidationError):
        app.anchor_coordinates.admit(
            source_package_ref=pkg_ref,
            anchor_kind="",  # empty
            anchor_coordinates=_exact_coords(media),
            evidence_refs=[],
            actor_id="m021-no-kind",
            idempotency_key="m021:no-kind",
        )


# ===========================================================================
# FALSE-PROOF countercase
# The mandate demands an explicit test that proves approximate millisecond
# pairs are not silently accepted when labelled as "anchor".
# ===========================================================================


def test_millisecond_start_end_pair_labelled_anchor_is_explicitly_rejected(tmp_path):
    """
    Countercase: a dict with only start_ms and end_ms — the classic
    approximate time-range representation — must be REJECTED by the service.

    Storing a start/end second (or millisecond) pair and labelling it an
    'anchor' proves only approximate timing, not exact byte/frame coordinates.
    The mandate is fail-closed: this form must never be admitted.
    """
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    # Classic approximate anchor — only ms span, no exact coordinates
    approximate_anchor = {"start_ms": 1000, "end_ms": 3000}

    with pytest.raises(ValidationError) as exc_info:
        app.anchor_coordinates.admit(
            source_package_ref=pkg_ref,
            anchor_kind="VERBATIM_QUOTE",
            anchor_coordinates=approximate_anchor,
            evidence_refs=[],
            actor_id="m021-countercase",
            idempotency_key="m021:countercase",
        )

    assert exc_info.value.context["classification"] == "FR_ANCH_001_APPROXIMATE_ANCHOR_REJECTED", (
        "Approximate millisecond anchor must be rejected with "
        "FR_ANCH_001_APPROXIMATE_ANCHOR_REJECTED — not admitted"
    )


# ===========================================================================
# REGRESSION — adjacent behaviour must not be broken
# ===========================================================================


def test_existing_anchor_hit_via_expression_service_still_works(tmp_path):
    """
    The pre-existing `ExpressionGovernanceService.create_anchor_hit` must
    continue to function after the CA-M021 changes — we must not break Wave 02
    callers.
    """
    from tests.phase4._support import imported_app, build_transcript, ref as support_ref, make_source_span

    app, pkg_ref, admitted = imported_app(tmp_path)
    aligned, packed, alignment_ref, phrase_pack_ref = build_transcript(app, pkg_ref)
    phrase = packed["object"]["payload"]["phrases"][0]
    phrase_obj = {"phrase_id": phrase["phrase_id"], "version": "1.0.0", **phrase}
    phrase_stored = app.repository.store_object(
        "packed_phrase",
        phrase_obj,
        object_id=phrase["phrase_id"],
        idempotency_key="m021-reg:phrase",
        lifecycle_state="VALIDATED",
    )
    phrase_ref = support_ref(phrase_stored)

    span = make_source_span(
        source_ref=pkg_ref,
        start_ms=0,
        end_ms=1000,
        speaker_id="guest",
    )
    result = app.expression.create_anchor_hit(
        source_package_ref=pkg_ref,
        phrase_refs=[phrase_ref],
        source_spans=[span],
        anchor_kind="VERBATIM_QUOTE",
        epistemic_state="OBSERVED",
        evidence_refs=[],
        actor_id="m021-regression",
        idempotency_key="m021-reg:anchor-hit",
    )
    assert result["object"]["payload"]["anchor_hit_id"].startswith("ie:anchor-hit:")


def test_verbatim_evidence_service_still_works(tmp_path):
    """
    VerbatimEvidenceService must continue to work after CA-M021 changes.
    """
    from tests.phase4._support import imported_app, build_transcript, ref as support_ref, make_source_span

    app, pkg_ref, admitted = imported_app(tmp_path)
    aligned, packed, ar, pr = build_transcript(app, pkg_ref)

    raw_transcript = "I thought success meant control. Um then I learned to listen."
    exact_quote = "Um then I learned to listen."
    transcript_sha = hashlib.sha256(raw_transcript.encode("utf-8")).hexdigest()

    phrase = packed["object"]["payload"]["phrases"][-1]
    phrase_obj = {"phrase_id": phrase["phrase_id"], "version": "1.0.0", **phrase}
    phrase_stored = app.repository.store_object(
        "packed_phrase",
        phrase_obj,
        object_id=phrase["phrase_id"],
        idempotency_key="m021-reg:v-phrase",
        lifecycle_state="VALIDATED",
    )
    phrase_ref = support_ref(phrase_stored)

    media = admitted["object"]["payload"]["media_assets"][0]
    start = raw_transcript.index(exact_quote)
    end = start + len(exact_quote)
    span = make_source_span(
        source_ref=pkg_ref,
        start_ms=1500,
        end_ms=3240,
        speaker_id="guest",
    )
    result = app.verbatim.admit(
        source_package_ref=pkg_ref,
        alignment_ref=ar,
        phrase_refs=[phrase_ref],
        source_media_asset_id=media["asset_id"],
        source_media_sha256=media["sha256"],
        source_span=span,
        transcript_text=raw_transcript,
        transcript_sha256=transcript_sha,
        character_start=start,
        character_end=end,
        quote_text=exact_quote,
        actor_id="m021-reg:verbatim",
        limitations=["DEVELOPMENT_FIXTURE_TRANSCRIPT"],
        idempotency_key="m021-reg:verbatim",
    )
    assert result["object"]["payload"]["quote_text"] == exact_quote
    assert result["object"]["payload"]["validation"]["exact_character_slice"] is True


# ===========================================================================
# INTEGRATION — real domain boundary
# ===========================================================================


def test_list_for_source_returns_all_committed_coordinates(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    c1 = _admit_coord(app, pkg_ref, media, key="m021:list-1")
    c2 = app.anchor_coordinates.admit(
        source_package_ref=pkg_ref,
        anchor_kind="EMOTIONAL_CUE",
        anchor_coordinates=_exact_coords(media, us_start=2_000_000, us_end=3_500_000),
        evidence_refs=[],
        actor_id="m021-list-2",
        idempotency_key="m021:list-2",
    )

    records = app.anchor_coordinates.list_for_source(
        pkg_ref["object_id"]
    )
    ids = {r["payload"]["anchor_coordinate_id"] for r in records}
    assert c1["object"]["object_id"] in ids
    assert c2["object"]["object_id"] in ids


def test_get_by_ref_returns_exact_payload(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media, key="m021:get")
    stored_ref = {
        "object_id": result["object"]["object_id"],
        "version": result["object"]["version"],
        "sha256": result["object"]["sha256"],
    }
    fetched = app.anchor_coordinates.get(stored_ref)
    assert fetched["payload"]["anchor_coordinate_id"] == result["object"]["object_id"]
    assert fetched["sha256"] == result["object"]["sha256"]


def test_validation_block_records_exact_coordinate_flags(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media, key="m021:val-block")
    val = result["object"]["payload"]["validation"]

    assert val["exact_coordinates"] is True
    assert val["approximate_anchor_rejected"] is True
    assert val["source_digest_bound"] is True
    assert val["duration_bound_checked"] is True
    assert val["mandate_id"] == "CA-M021"


def test_receipt_contains_exact_object_ref(tmp_path):
    app = _make_app(tmp_path)
    media = _make_media_asset_with_us()
    admitted = _admit_package(app, media)
    pkg_ref = _ref(admitted)

    result = _admit_coord(app, pkg_ref, media, key="m021:receipt")
    receipt = result["receipt"]

    assert receipt["object_ref"]["object_id"] == result["object"]["object_id"]
    assert receipt["object_ref"]["sha256"] == result["object"]["sha256"]
    assert receipt["exact_coordinates"] is True
    assert receipt["mandate_id"] == "CA-M021"
    assert receipt["validation_status"] == "PASS"
