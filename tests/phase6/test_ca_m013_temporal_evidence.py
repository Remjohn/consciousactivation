from __future__ import annotations

import json
from fractions import Fraction
from math import ceil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from ._support import ref
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import (
    PipelineSourceIntegrityError,
    PipelineSourceLineageError,
    PipelineValidationError,
)
from ca_contracts import canonical_sha256
from cmf_pipeline.media import SourceMediaService, ffprobe_media


SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "services" / "pipeline" / "contracts" / "schemas"


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8"))


def _register(app: PipelineApplication, source: Path) -> tuple[dict, dict]:
    registration = app.source_media.register(
        source_path=source,
        logical_uri="media/temporal-anchor.mp4",
        source_package_ref=ref("source-package:temporal", "package:temporal"),
        transcript_alignment_ref=ref("transcript:temporal", "transcript:temporal"),
        visual_index_ref=ref("visual:temporal", "visual:temporal"),
        restrictions=["operator_source_authority"],
        idempotency_key="register:temporal",
    )["object"]["payload"]
    return registration, SourceMediaService.registration_ref(registration)


def _exact_microseconds_for_ticks(ticks: int, timebase: dict[str, int]) -> int:
    value = Fraction(
        ticks * timebase["numerator"] * 1_000_000,
        timebase["denominator"],
    )
    assert value.denominator == 1
    return int(value)


def _exact_tick_step(timebase: dict[str, int]) -> int:
    microseconds_per_tick = Fraction(
        timebase["numerator"] * 1_000_000,
        timebase["denominator"],
    )
    return microseconds_per_tick.denominator


def _representable_interval(stream: dict) -> tuple[int, int]:
    timebase = stream["time_base"]
    step_ticks = _exact_tick_step(timebase)
    start_us = _exact_microseconds_for_ticks(step_ticks, timebase)
    end_us = _exact_microseconds_for_ticks(step_ticks * 2, timebase)
    return start_us, end_us


def _representable_past_end(stream: dict) -> tuple[int, int]:
    timebase = stream["time_base"]
    duration_us = stream["duration_ms"] * 1_000
    step_ticks = _exact_tick_step(timebase)
    minimum_end_ticks = ceil(
        Fraction(duration_us * timebase["denominator"], 1_000_000 * timebase["numerator"])
    ) + 1
    end_ticks = ((minimum_end_ticks + step_ticks - 1) // step_ticks) * step_ticks
    end_us = _exact_microseconds_for_ticks(end_ticks, timebase)
    start_ticks = max(step_ticks, end_ticks - step_ticks)
    start_us = _exact_microseconds_for_ticks(start_ticks, timebase)
    return start_us, end_us


def test_evidence_moment_schema_and_projection_are_executable(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    stream = registration["technical"]["streams"][0]
    start_us, end_us = _representable_interval(stream)
    stored = app.evidence_moments.create(
        source_registration_ref=source_ref,
        source_path=source_video,
        stream_ordinal=0,
        timebase=stream["time_base"],
        start_offset_us=start_us,
        end_offset_us=end_us,
        transcript_span={
            "alignment_ref": ref("transcript-alignment:temporal", "alignment"),
            "start_word_id": "w1",
            "end_word_id": "w2",
            "start_char": 4,
            "end_char": 18,
        },
        idempotency_key="evidence:create:schema",
    )
    moment = stored["object"]["payload"]
    Draft202012Validator(_schema("evidence_moment")).validate(moment)
    projection = app.evidence_moments.projection(moment["evidence_moment_id"], source_path=source_video)
    assert projection["read_only"] is True
    assert projection["source_resolution"]["status"] == "RESOLVED"
    assert projection["source_resolution"]["resolved_exactly"] is True


def test_exact_boundary_resolves_to_native_source_ticks(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    stream = registration["technical"]["streams"][0]
    step_ticks = _exact_tick_step(stream["time_base"])
    start_ticks = step_ticks
    end_ticks = step_ticks * 2
    start_us = _exact_microseconds_for_ticks(start_ticks, stream["time_base"])
    end_us = _exact_microseconds_for_ticks(end_ticks, stream["time_base"])

    stored = app.evidence_moments.create(
        source_registration_ref=source_ref,
        source_path=source_video,
        stream_ordinal=0,
        timebase=stream["time_base"],
        start_offset_us=start_us,
        end_offset_us=end_us,
        idempotency_key="evidence:create:boundary",
    )["object"]["payload"]

    assert stored["start_source_tick"] == start_ticks
    assert stored["end_source_tick"] == end_ticks
    resolved = app.evidence_moments.resolve(
        evidence_moment_ref={
            "object_id": stored["evidence_moment_id"],
            "version": stored["evidence_moment_version"],
            "sha256": canonical_sha256(stored),
        },
        source_path=source_video,
    )
    assert resolved["status"] == "RESOLVED"
    assert resolved["start_source_tick"] == start_ticks
    assert resolved["end_source_tick"] == end_ticks


def test_multi_stream_anchors_are_explicit_and_resolve_independently(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    streams = registration["technical"]["streams"]
    assert len(streams) >= 2

    for ordinal, stream in enumerate(streams[:2]):
        step_ticks = _exact_tick_step(stream["time_base"])
        start_us = _exact_microseconds_for_ticks(step_ticks, stream["time_base"])
        end_us = _exact_microseconds_for_ticks(step_ticks * 2, stream["time_base"])
        moment = app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=ordinal,
            timebase=stream["time_base"],
            start_offset_us=start_us,
            end_offset_us=end_us,
            idempotency_key=f"evidence:create:stream:{ordinal}",
        )["object"]["payload"]
        resolved = app.evidence_moments.resolve(
            evidence_moment_ref={
                "object_id": moment["evidence_moment_id"],
                "version": moment["evidence_moment_version"],
                "sha256": canonical_sha256(moment),
            },
            source_path=source_video,
        )
        assert resolved["stream"]["ordinal"] == ordinal
        assert resolved["timebase"] == stream["time_base"]


def test_missing_source_fails_closed(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    stream = ffprobe_media(source_video)["streams"][0]
    with pytest.raises(PipelineSourceIntegrityError, match="source media is missing"):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=tmp_path / "missing.mp4",
            stream_ordinal=0,
            timebase=stream["time_base"],
            start_offset_us=0,
            end_offset_us=1_000,
            idempotency_key="evidence:missing-source",
        )


@pytest.mark.parametrize(
    ("start_us", "end_us"),
    [(None, 1_000), (0, None), (-1, 1_000), (1_000, 1_000), (2_000, 1_000)],
)
def test_missing_negative_and_reversed_coordinates_fail_closed(
    source_video, tmp_path, start_us, end_us
):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    stream = ffprobe_media(source_video)["streams"][0]
    with pytest.raises(PipelineValidationError):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=0,
            timebase=stream["time_base"],
            start_offset_us=start_us,
            end_offset_us=end_us,
            idempotency_key=f"evidence:coords:{start_us}:{end_us}",
        )


def test_invalid_timebase_fails_closed(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    stream = ffprobe_media(source_video)["streams"][0]
    invalid_timebase = {
        "numerator": stream["time_base"]["numerator"] + 1,
        "denominator": stream["time_base"]["denominator"],
    }
    with pytest.raises(PipelineSourceLineageError, match="timebase"):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=0,
            timebase=invalid_timebase,
            start_offset_us=0,
            end_offset_us=1_000,
            idempotency_key="evidence:invalid-timebase",
        )


def test_unrepresentable_microsecond_coordinate_fails_without_rounding(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    stream = ffprobe_media(source_video)["streams"][0]
    timebase = stream["time_base"]
    with pytest.raises(PipelineValidationError, match="represented exactly"):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=0,
            timebase=timebase,
            start_offset_us=1,
            end_offset_us=1_000_001,
            idempotency_key="evidence:precision",
        )


def test_out_of_bounds_anchor_fails_closed(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    stream = ffprobe_media(source_video)["streams"][0]
    start_us, end_us = _representable_past_end(stream)
    with pytest.raises(PipelineValidationError, match="outside source stream duration"):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=0,
            timebase=stream["time_base"],
            start_offset_us=start_us,
            end_offset_us=end_us,
            idempotency_key="evidence:bounds",
        )


def test_source_mismatch_is_rejected_after_canonical_object_is_forged(source_video, tmp_path):
    from ca_contracts import canonical_sha256

    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    stream = registration["technical"]["streams"][0]
    start_us, end_us = _representable_interval(stream)
    moment = app.evidence_moments.create(
        source_registration_ref=source_ref,
        source_path=source_video,
        stream_ordinal=0,
        timebase=stream["time_base"],
        start_offset_us=start_us,
        end_offset_us=end_us,
        idempotency_key="evidence:create:source-mismatch",
    )["object"]["payload"]

    forged = dict(moment)
    forged["source_media_sha256"] = "0" * 64
    forged["provenance"] = dict(moment["provenance"])
    forged["provenance"]["source_media_sha256"] = "0" * 64
    current = app.repository.get_object(moment["evidence_moment_id"])
    app.repository.store_object(
        "evidence_moment",
        forged,
        idempotency_key="evidence:forge:source-mismatch",
        object_id=moment["evidence_moment_id"],
        expected_revision=current["revision"],
        lifecycle_state="VERIFIED",
    )
    forged_ref = {
        "object_id": moment["evidence_moment_id"],
        "version": forged["evidence_moment_version"],
        "sha256": canonical_sha256(forged),
    }

    with pytest.raises(PipelineSourceLineageError, match="digest does not match verified source"):
        app.evidence_moments.resolve(
            evidence_moment_ref=forged_ref,
            source_path=source_video,
        )


def test_false_proof_quote_without_anchor_is_unadmissible(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    with pytest.raises(PipelineValidationError):
        app.evidence_moments.create(
            source_registration_ref=source_ref,
            source_path=source_video,
            stream_ordinal=0,
            timebase=None,
            start_offset_us=None,
            end_offset_us=None,
            idempotency_key="evidence:false-proof-floating-quote",
        )
