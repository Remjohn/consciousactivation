from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from ._support import ref
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.domain.errors import (
    PipelineSourceIntegrityError,
    PipelineSourceLineageError,
)
from cmf_pipeline.media import (
    FFmpegSourceLedRenderer,
    RenderedVideoEvaluator,
    SourceMediaService,
)


SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "services" / "pipeline" / "contracts" / "schemas"


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / f"{name}.schema.json").read_text(encoding="utf-8"))


def _register(app: PipelineApplication, source: Path, *, label: str = "source") -> tuple[dict, dict]:
    registration = app.source_media.register(
        source_path=source,
        logical_uri=f"media/{label}.mp4",
        source_package_ref=ref(f"source-package:{label}", f"package:{label}"),
        transcript_alignment_ref=ref(f"transcript:{label}", f"transcript:{label}"),
        visual_index_ref=ref(f"visual:{label}", f"visual:{label}"),
        restrictions=["operator_source_authority"],
        idempotency_key=f"register:{label}",
    )["object"]["payload"]
    return registration, SourceMediaService.registration_ref(registration)


def _words_and_selections() -> tuple[list[dict], list[dict]]:
    words = [
        {"word_id": "w1", "text": "A", "start_ms": 100, "end_ms": 700, "speaker_id": "speaker", "protected_tail_ms": 0},
        {"word_id": "w2", "text": "B", "start_ms": 1100, "end_ms": 1800, "speaker_id": "speaker", "protected_tail_ms": 0},
    ]
    selections = [
        {"selection_id": "sel-1", "start_word_id": "w1", "end_word_id": "w1", "function": "HOOK", "cut_in_class": "WORD_BOUNDARY", "cut_out_class": "WORD_BOUNDARY", "authorized_reorder": False},
        {"selection_id": "sel-2", "start_word_id": "w2", "end_word_id": "w2", "function": "CLAIM", "cut_in_class": "WORD_BOUNDARY", "cut_out_class": "WORD_BOUNDARY", "authorized_reorder": False},
    ]
    return words, selections


def _compile_edl(app: PipelineApplication, source: Path, source_ref: dict) -> dict:
    words, selections = _words_and_selections()
    return app.edls.compile(
        source_registration_ref=source_ref,
        source_path=source,
        expression_moment_ref=ref("moment", "m"),
        words=words,
        selections=selections,
        allow_reorder=False,
        idempotency_key="compile:edl",
    )["object"]["payload"]


def test_stable_content_addressed_identity_and_retrieval(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    first, first_ref = _register(app, source_video, label="first")
    copied_source = tmp_path / "different-filename.mp4"
    shutil.copyfile(source_video, copied_source)
    second, second_ref = _register(app, copied_source, label="second")

    assert first["registration_id"] != second["registration_id"]
    assert first["source_media_ref"] == second["source_media_ref"]
    media_id = first["source_media_ref"]["object_id"]
    media = app.repository.get_object(media_id)
    assert media["object_type"] == "source_media_identity"
    assert media["payload"]["media_sha256"] == first["source_media_sha256"]
    assert media["payload"]["media_id"] == media_id
    assert first_ref["sha256"] == app.repository.get_object(first_ref["object_id"])["canonical_sha256"]
    assert second_ref["sha256"] == app.repository.get_object(second_ref["object_id"])["canonical_sha256"]


def test_source_identity_schema_and_registration_schema_are_executable(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    identity = app.repository.get_object(registration["source_media_ref"]["object_id"])["payload"]
    Draft202012Validator(_schema("source_media_identity")).validate(identity)
    Draft202012Validator(_schema("source_media_registration")).validate(registration)
    assert source_ref["object_id"] == registration["registration_id"]


def test_changed_source_bytes_fail_closed_before_derivative_processing(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    mutated = tmp_path / "mutated.mp4"
    shutil.copyfile(source_video, mutated)
    with mutated.open("ab") as handle:
        handle.write(b"mutation")

    with pytest.raises(PipelineSourceIntegrityError, match="source media integrity mismatch"):
        app.source_media.verify_source(source_registration_ref=source_ref, source_path=mutated)
    with pytest.raises(PipelineSourceIntegrityError, match="source media integrity mismatch"):
        _compile_edl(app, mutated, source_ref)
    assert app.repository.has_object(registration["registration_id"])


def test_registration_digest_mismatch_is_rejected_even_when_reference_shape_is_valid(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    tampered = dict(registration)
    tampered["source_media_sha256"] = "0" * 64
    app.repository.store_object(
        "source_media_registration",
        tampered,
        idempotency_key="tamper:registration",
        object_id=registration["registration_id"],
        lifecycle_state="VERIFIED",
    )
    with pytest.raises(PipelineSourceLineageError, match="source registration reference digest mismatch"):
        app.source_media.verify_source(source_registration_ref=source_ref, source_path=source_video)


def test_derivative_without_source_lineage_is_rejected(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, _ = _register(app, source_video)
    renderer = FFmpegSourceLedRenderer(app.repository)
    incomplete_edl = {"edl_id": "edl:missing-source", "edl_version": "1.0.0", "entries": []}
    with pytest.raises(PipelineSourceLineageError, match="missing source lineage fields"):
        renderer.render(
            source_path=source_video,
            edl=incomplete_edl,
            output_dir=tmp_path / "out",
            logical_output_uri="video/output.mp4",
        )


def test_proxy_substitution_fails_against_registered_content_digest(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    proxy = tmp_path / "proxy.mp4"
    shutil.copyfile(source_video, proxy)
    with proxy.open("r+b") as handle:
        handle.seek(0)
        original = handle.read(1)
        handle.seek(0)
        handle.write(bytes([(original[0] ^ 0x01) if original else 1]))

    with pytest.raises(PipelineSourceIntegrityError):
        _compile_edl(app, proxy, source_ref)


def test_stale_derivative_binding_is_blocked_at_render_time(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    _, source_ref = _register(app, source_video)
    edl = _compile_edl(app, source_video, source_ref)
    mutated = tmp_path / "changed-after-ingest.mp4"
    shutil.copyfile(source_video, mutated)
    with mutated.open("ab") as handle:
        handle.write(b"post-ingest-change")

    renderer = FFmpegSourceLedRenderer(app.repository)
    with pytest.raises(PipelineSourceIntegrityError):
        renderer.render(
            source_path=mutated,
            edl=edl,
            output_dir=tmp_path / "render",
            logical_output_uri="video/stale.mp4",
        )
    assert not (tmp_path / "render/stale.mp4").exists()


def test_historical_source_reference_survives_supersession(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    first, first_ref = _register(app, source_video, label="v1")
    replacement = tmp_path / "v2.mp4"
    shutil.copyfile(source_video, replacement)
    with replacement.open("ab") as handle:
        handle.write(b"superseded-source")
    second, second_ref = _register(app, replacement, label="v2")

    assert first["source_media_ref"] != second["source_media_ref"]
    old_media = app.repository.get_object(first["source_media_ref"]["object_id"])
    old_registration = app.repository.get_object(first_ref["object_id"])
    assert old_media["current"] is True
    assert old_registration["current"] is True
    assert app.repository.get_object(second_ref["object_id"])["payload"]["source_media_ref"] == second["source_media_ref"]


def test_operator_provenance_projection_distinguishes_source_from_derivative(source_video, tmp_path):
    app = PipelineApplication(tmp_path / "db.sqlite3")
    app.initialize()
    registration, source_ref = _register(app, source_video)
    fake_derivative_ref = {
        "object_id": "derivative:example",
        "version": "1.0.0",
        "sha256": ref("seed", "derivative")["sha256"],
    }
    inspection = app.source_media.provenance(
        source_registration_ref=source_ref,
        derivative_ref=fake_derivative_ref,
        source_path=source_video,
    )
    assert inspection["source_kind"] == "SOVEREIGN_SOURCE_BYTES"
    assert inspection["source_media_ref"] == registration["source_media_ref"]
    assert inspection["derivative_kind"] == "DERIVATIVE_OUTPUT"
    assert inspection["derivative_is_sovereign_source"] is False
    assert inspection["integrity"]["status"] == "VERIFIED"
