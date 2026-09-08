from __future__ import annotations

import hashlib

import pytest

from ._support import imported_app, make_source_span, ref, build_transcript
from conscious_activations_interview_expression.errors import ValidationError


RAW_TRANSCRIPT = "I thought success meant control. Um then I learned to listen."
EXACT_QUOTE = "Um then I learned to listen."


def _transcript_sha() -> str:
    return hashlib.sha256(RAW_TRANSCRIPT.encode("utf-8")).hexdigest()


def _prepare(tmp_path):
    app, package_ref, admitted = imported_app(tmp_path)
    aligned, packed, alignment_ref, phrase_pack_ref = build_transcript(app, package_ref)
    phrase = packed["object"]["payload"]["phrases"][-1]
    phrase_obj = {
        "phrase_id": phrase["phrase_id"],
        "version": "1.0.0",
        **phrase,
    }
    phrase_stored = app.repository.store_object(
        "packed_phrase",
        phrase_obj,
        object_id=phrase["phrase_id"],
        idempotency_key="m015:phrase",
        lifecycle_state="VALIDATED",
    )
    phrase_ref = ref(phrase_stored)
    media = admitted["object"]["payload"]["media_assets"][0]
    start = RAW_TRANSCRIPT.index(EXACT_QUOTE)
    end = start + len(EXACT_QUOTE)
    span = make_source_span(
        source_ref=package_ref,
        start_ms=1500,
        end_ms=3240,
        speaker_id="guest",
    )
    return {
        "app": app,
        "package_ref": package_ref,
        "aligned": aligned,
        "alignment_ref": alignment_ref,
        "phrase_pack_ref": phrase_pack_ref,
        "phrase_ref": phrase_ref,
        "media": media,
        "span": span,
        "start": start,
        "end": end,
    }


def _admit(ctx, *, key: str = "m015:verbatim", quote_text: str = EXACT_QUOTE, **overrides):
    values = {
        "source_package_ref": ctx["package_ref"],
        "alignment_ref": ctx["alignment_ref"],
        "phrase_refs": [ctx["phrase_ref"]],
        "source_media_asset_id": ctx["media"]["asset_id"],
        "source_media_sha256": ctx["media"]["sha256"],
        "source_span": ctx["span"],
        "transcript_text": RAW_TRANSCRIPT,
        "transcript_sha256": _transcript_sha(),
        "character_start": ctx["start"],
        "character_end": ctx["end"],
        "quote_text": quote_text,
        "actor_id": "m015-extractor",
        "limitations": ["DEVELOPMENT_FIXTURE_TRANSCRIPT"],
        "idempotency_key": key,
    }
    values.update(overrides)
    return ctx["app"].verbatim.admit(**values)


def test_exact_spoken_capture_preserves_disfluency_and_source_lineage(tmp_path):
    ctx = _prepare(tmp_path)
    result = _admit(ctx)
    payload = result["object"]["payload"]

    assert payload["quote_text"] == EXACT_QUOTE
    assert payload["quote_text"].startswith("Um")
    assert payload["transcript_ref"] == {
        "sha256": _transcript_sha(),
        "character_start": ctx["start"],
        "character_end": ctx["end"],
    }
    assert payload["source_span"] == ctx["span"]
    assert payload["source_media_ref"]["sha256"] == ctx["media"]["sha256"]
    assert payload["validation"]["exact_character_slice"] is True
    assert payload["validation"]["semantic_similarity_used"] is False
    assert payload["admission_receipt"]["mandate_id"] == "CA-M015"
    assert result["receipt"]["object_ref"]["sha256"] == result["object"]["sha256"]


def test_same_meaning_grammar_cleanup_is_rejected_as_editorial_drift(tmp_path):
    ctx = _prepare(tmp_path)
    cleaned = "Then I learned to listen."

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, quote_text=cleaned)

    assert exc_info.value.context["classification"] == "EDITORIAL_DRIFT"


def test_material_punctuation_change_is_rejected_even_when_character_span_is_valid(tmp_path):
    ctx = _prepare(tmp_path)
    changed = "Um then I learned to listen!"

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, quote_text=changed)

    assert exc_info.value.context["classification"] == "EDITORIAL_DRIFT"


def test_stale_transcript_digest_is_rejected_before_admission(tmp_path):
    ctx = _prepare(tmp_path)

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, transcript_sha256="0" * 64)

    assert exc_info.value.context["classification"] == "PROVENANCE_ERROR"


def test_stale_character_span_is_rejected_from_current_transcript(tmp_path):
    ctx = _prepare(tmp_path)
    start = ctx["start"] + 1

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, character_start=start)

    assert exc_info.value.context["classification"] == "EDITORIAL_DRIFT"


def test_source_media_digest_mismatch_is_rejected(tmp_path):
    ctx = _prepare(tmp_path)

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, source_media_sha256="f" * 64)

    assert exc_info.value.context["classification"] == "PROVENANCE_ERROR"


def test_source_span_lineage_mismatch_is_rejected(tmp_path):
    ctx = _prepare(tmp_path)
    forged = dict(ctx["span"])
    forged["source_sha256"] = "e" * 64

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, source_span=forged)

    assert exc_info.value.context["classification"] == "PROVENANCE_ERROR"


def test_missing_phrase_lineage_is_rejected(tmp_path):
    ctx = _prepare(tmp_path)
    forged_ref = dict(ctx["phrase_ref"])
    forged_ref["sha256"] = "a" * 64

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, phrase_refs=[forged_ref])

    assert exc_info.value.context["classification"] == "PROVENANCE_ERROR"


def test_exact_whitespace_is_part_of_verbatim_identity(tmp_path):
    ctx = _prepare(tmp_path)
    changed = "Um  then I learned to listen."

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, quote_text=changed)

    assert exc_info.value.context["classification"] == "EDITORIAL_DRIFT"


def test_source_span_beyond_media_duration_is_rejected(tmp_path):
    ctx = _prepare(tmp_path)
    forged = dict(ctx["span"])
    forged["end_ms"] = 999999

    with pytest.raises(ValidationError) as exc_info:
        _admit(ctx, source_span=forged)

    assert exc_info.value.context["classification"] == "PROVENANCE_ERROR"


def test_evidence_revision_preserves_previous_revision(tmp_path):
    ctx = _prepare(tmp_path)
    first = _admit(ctx, key="m015:revision:1")
    second = _admit(
        ctx,
        key="m015:revision:2",
        limitations=["DEVELOPMENT_FIXTURE_TRANSCRIPT", "SECOND_REVIEW_NOTE"],
    )

    assert second["object"]["object_id"] == first["object"]["object_id"]
    assert second["object"]["revision"] == 2
    historical = ctx["app"].repository.get_object(
        first["object"]["object_id"], revision=1
    )
    assert historical["sha256"] == first["object"]["sha256"]
    assert historical["payload"]["validation"]["limitations"] == [
        "DEVELOPMENT_FIXTURE_TRANSCRIPT"
    ]


def test_downstream_inventory_rejects_unanchored_quote_material(tmp_path):
    ctx = _prepare(tmp_path)
    app = ctx["app"]
    from ._support import build_visual

    _, visual_ref = build_visual(app, ctx["package_ref"])
    span = ctx["span"]
    moment = app.expression.propose_moment(
        source_package_ref=ctx["package_ref"],
        phrase_refs=[ctx["phrase_ref"]],
        source_spans=[span],
        keyframe_refs=[],
        reaction_receipt_refs=[],
        candidate_reason="source-backed expression",
        proposer_id="m015-hunter",
        idempotency_key="m015:moment",
    )
    approved = app.expression.decide_moment(
        moment["object"]["object_id"],
        decision="APPROVE",
        operator_id="m015-operator",
        rationale="approved source-backed expression",
        idempotency_key="m015:approve",
    )

    with pytest.raises(ValidationError) as exc_info:
        app.inventory.compile(
            source_package_ref=ctx["package_ref"],
            expression_moment_refs=[ref(approved)],
            phrase_pack_ref=ctx["phrase_pack_ref"],
            visual_index_ref=visual_ref,
            reaction_receipt_refs=[],
            idempotency_key="m015:inventory:no-verbatim",
        )

    assert exc_info.value.context["classification"] == "COMPOSITION_ERROR"


def test_downstream_inventory_consumes_canonical_verbatim_text_not_phrase_text(tmp_path):
    ctx = _prepare(tmp_path)
    app = ctx["app"]
    from ._support import build_visual

    evidence = _admit(ctx)
    _, visual_ref = build_visual(app, ctx["package_ref"])

    # Deliberately make the phrase representation look more editorially polished.
    polished_phrase = app.repository.get_object(ctx["phrase_ref"]["object_id"])
    polished = dict(polished_phrase["payload"])
    polished["text"] = "Then I learned to listen."
    polished_stored = app.repository.store_object(
        "packed_phrase",
        polished,
        object_id=ctx["phrase_ref"]["object_id"],
        idempotency_key="m015:phrase:polished",
        lifecycle_state="VALIDATED",
    )

    moment = app.expression.propose_moment(
        source_package_ref=ctx["package_ref"],
        phrase_refs=[ctx["phrase_ref"]],
        source_spans=[ctx["span"]],
        keyframe_refs=[],
        reaction_receipt_refs=[],
        candidate_reason="source-backed expression",
        proposer_id="m015-hunter",
        idempotency_key="m015:moment:polished",
    )
    approved = app.expression.decide_moment(
        moment["object"]["object_id"],
        decision="APPROVE",
        operator_id="m015-operator",
        rationale="approved source-backed expression",
        idempotency_key="m015:approve:polished",
    )
    inventory = app.inventory.compile(
        source_package_ref=ctx["package_ref"],
        expression_moment_refs=[ref(approved)],
        phrase_pack_ref=ctx["phrase_pack_ref"],
        visual_index_ref=visual_ref,
        reaction_receipt_refs=[],
        idempotency_key="m015:inventory:verbatim",
        verbatim_evidence_refs=[ref(evidence)],
    )

    quote = inventory["object"]["payload"]["quote_candidates"][0]
    assert quote["text"] == EXACT_QUOTE
    assert quote["text"] != polished["text"]
    assert quote["evidence_ref"] == ref(evidence)
    assert quote["transformation_state"] == "SOURCE_VERBATIM"
    assert quote["evidence_ref"] == ref(evidence)
