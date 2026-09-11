import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "asset-intelligence" / "src"))

from cae_asset_intelligence.corpus import (  # noqa: E402
    CinematicCorpusEngine,
    CorpusState,
    MediaAuthorization,
    SceneProposal,
    TranscriptCue,
)
from cae_asset_intelligence.domain import EditorialInsertRole, RightsMetadata, RightsStatus, SourceType  # noqa: E402
from cae_asset_intelligence.research_session import (  # noqa: E402
    AssetResearchMode,
    AssetResearchRequest,
    AssetResearchSessionFactory,
    AssetResearchSessionState,
    CandidateSelectionError,
    RangeMode,
)
from cae_asset_intelligence.retrieval import RightsPolicy  # noqa: E402


def _corpus():
    media = b"m0086 governed media fixture"
    sha = hashlib.sha256(media).hexdigest()
    auth = MediaAuthorization(
        authorization_id="AUTH-M0086",
        workspace_id="WS-M0086",
        source_sha256=sha,
        source_version="v1",
        approved=True,
        authority_ref="operator-approval:M0086-fixture",
    )
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-M0086")
    scenes = [
        SceneProposal(
            start_time=0,
            end_time=5,
            contextual_caption="Dawn location establishment precedes the speaker's decisive operational choice.",
            semantic_role="SETTING_ESTABLISHMENT",
            insert_role=EditorialInsertRole.WORLD_BUILDING,
            source_type=SourceType.ARCHIVAL,
            transcript=(
                TranscriptCue(start_time=0.5, end_time=1.5, text="We opened before sunrise.", speaker="A"),
                TranscriptCue(start_time=1.6, end_time=2.5, text="The place was already awake.", speaker="A"),
            ),
        ),
        SceneProposal(
            start_time=5,
            end_time=10,
            contextual_caption="A control-room reaction shows operational pressure after an important failed decision.",
            semantic_role="DECISION_PRESSURE",
            insert_role=EditorialInsertRole.EMOTIONAL_AMPLIFICATION,
            source_type=SourceType.MOVIE,
            transcript=(
                TranscriptCue(start_time=6.0, end_time=7.0, text="We opened the console at midnight.", speaker="B"),
            ),
        ),
    ]
    records, ingest_receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M0086",
        candidate_id="CND-M0086",
        source_version="v1",
        source_bytes=media,
        media_duration=10.0,
        authorization=auth,
        rights=rights,
        scenes=scenes,
    )
    index_sha = hashlib.sha256(b"governed-index-m0086-v1").hexdigest()
    indexed_receipt = ingest_receipt.model_copy(
        update={
            "state": CorpusState.INDEXED,
            "receipt_id": "RCPT-M0086-INDEXED",
            "scene_ids": tuple(r.scene_id for r in records),
        }
    )
    return records, index_sha, indexed_receipt


def _factory(uri=True):
    def resolve(record):
        return f"https://media.test/{record.media_id}.mp4" if uri else None

    return AssetResearchSessionFactory(
        source_uri_resolver=resolve,
        preview_mime_resolver=lambda record: "video/mp4",
        actor="operator-test",
    )


def test_phrase_session_resolves_exact_temporal_match_and_playable_preview():
    records, _, _ = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="opened before sunrise",
        mode=AssetResearchMode.PHRASE,
        context_before_seconds=1.0,
        context_after_seconds=2.0,
        range_mode=RangeMode.MATCH,
    )
    session = _factory().open(request, records)

    assert session.state == AssetResearchSessionState.CANDIDATES
    assert len(session.candidates) == 1
    candidate = session.candidates[0]
    assert candidate.match_range.start_time == 0.5
    assert candidate.match_range.end_time == 1.5
    assert candidate.selected_range.start_time == 0.5
    assert candidate.selected_range.end_time == 1.5
    assert candidate.preview.playable is True
    assert candidate.preview.uri.endswith(".mp4")
    assert candidate.source.source_sha256 == records[0].source_sha256
    assert candidate.rights_status == RightsStatus.CLEARED
    assert "EXACT_TRANSCRIPT_PHRASE" in candidate.match_basis


def test_phrase_session_returns_context_and_transcript_window_without_losing_match_range():
    records, _, _ = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="opened before sunrise",
        mode=AssetResearchMode.PHRASE,
        context_before_seconds=0.2,
        context_after_seconds=1.0,
        range_mode=RangeMode.CONTEXT,
    )
    session = _factory().open(request, records)
    candidate = session.candidates[0]

    assert candidate.match_range is not None
    assert candidate.context_range.start_time == 0.3
    assert candidate.context_range.end_time == 2.5
    assert [cue.text for cue in candidate.transcript] == [
        "We opened before sunrise.",
        "The place was already awake.",
    ]
    assert candidate.selected_range == candidate.context_range


def test_semantic_session_reuses_governed_retriever_and_role_constraints_block_good_looking_wrong_candidate():
    records, index_sha, receipt = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="place before the operational choice",
        mode=AssetResearchMode.SEMANTIC_CINEMATIC,
        insert_roles=(EditorialInsertRole.WORLD_BUILDING,),
        min_confidence=0.01,
        expected_index_sha256=index_sha,
    )
    session = _factory().open(request, records, index_sha256=index_sha, indexed_receipt=receipt)

    assert session.state == AssetResearchSessionState.CANDIDATES
    assert session.candidates
    assert all(candidate.insert_role == EditorialInsertRole.WORLD_BUILDING for candidate in session.candidates)
    assert records[1].scene_id not in {candidate.source.scene_id for candidate in session.candidates}
    assert session.candidates[0].retrieval_mode == AssetResearchMode.SEMANTIC_CINEMATIC


def test_stale_semantic_index_fails_closed_without_candidates():
    records, index_sha, receipt = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="operational pressure",
        mode=AssetResearchMode.SEMANTIC_CINEMATIC,
        expected_index_sha256="b" * 64,
        min_confidence=0.01,
    )
    session = _factory().open(request, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert session.state == AssetResearchSessionState.BLOCKED
    assert session.candidates == ()


def test_unlicensed_candidates_are_not_returned_even_when_phrase_matches():
    records, _, _ = _corpus()
    restricted = records[0].model_copy(
        update={
            "annotation": records[0].annotation.model_copy(
                update={"rights": RightsMetadata(status=RightsStatus.UNKNOWN_UNLICENSED)}
            )
        }
    )
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="opened before sunrise",
        mode=AssetResearchMode.PHRASE,
        rights_policy=RightsPolicy.CLEARED_ONLY,
    )
    session = _factory().open(request, [restricted, records[1]])
    assert session.state == AssetResearchSessionState.ABSTAIN
    assert session.candidates == ()


def test_selection_and_promotion_are_immutable_operator_projections():
    records, _, _ = _corpus()
    request = AssetResearchRequest(workspace_id="WS-M0086", query="opened before sunrise", mode=AssetResearchMode.PHRASE)
    session = _factory().open(request, records)
    candidate_id = session.candidates[0].research_candidate_id

    selected, selection_receipt = session.select(candidate_id, actor="operator", operator_ref="OP-M0086")
    promotion = selected.request_promotion(
        candidate_id,
        actor="operator",
        operator_ref="OP-M0086",
        storyboard_element_ref="STORY-1-ELEMENT-1",
        revision_ref="REV-1",
        selection_receipt_ref=selection_receipt.receipt_id,
    )

    assert session.selected_candidate_id is None
    assert selected.selected_candidate_id == candidate_id
    assert selection_receipt.selected_candidate == candidate_id
    assert selection_receipt.source_hash == selected.candidates[0].source.source_sha256
    assert selection_receipt.postconditions["canonical_asset_mutation"] == "NOT_PERFORMED"
    assert promotion.selected_candidate == candidate_id
    assert promotion.storyboard_element_ref == "STORY-1-ELEMENT-1"


def test_missing_playable_preview_cannot_be_selected_or_promoted():
    records, _, _ = _corpus()
    request = AssetResearchRequest(workspace_id="WS-M0086", query="opened before sunrise", mode=AssetResearchMode.PHRASE)
    session = _factory(uri=False).open(request, records)
    candidate_id = session.candidates[0].research_candidate_id

    with pytest.raises(CandidateSelectionError, match="source URI"):
        session.select(candidate_id, actor="operator", operator_ref="OP-M0086")


def test_rejected_candidates_are_preserved_and_cannot_be_selected_later():
    records, _, _ = _corpus()
    request = AssetResearchRequest(workspace_id="WS-M0086", query="opened before sunrise", mode=AssetResearchMode.PHRASE)
    session = _factory().open(request, records)
    candidate_id = session.candidates[0].research_candidate_id

    rejected, receipt_id = session.reject(candidate_id, actor="operator", reason="narratively wrong")
    assert rejected.rejected_candidate_ids == (candidate_id,)
    assert receipt_id in rejected.transition_receipt_ids
    with pytest.raises(CandidateSelectionError, match="rejected"):
        rejected.select(candidate_id, actor="operator", operator_ref="OP-M0086")


def test_session_and_selection_receipts_are_deterministic_for_identical_inputs():
    records, _, _ = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="opened before sunrise",
        mode=AssetResearchMode.PHRASE,
        range_mode=RangeMode.MATCH,
    )
    first = _factory().open(request, records)
    second = _factory().open(request, records)
    assert first.session_id == second.session_id
    assert first.request_ref == second.request_ref
    assert first.candidate_set_ref == second.candidate_set_ref
    assert [c.research_candidate_id for c in first.candidates] == [c.research_candidate_id for c in second.candidates]

    first_selected, first_receipt = first.select(first.candidates[0].research_candidate_id, actor="operator", operator_ref="OP-M0086")
    second_selected, second_receipt = second.select(second.candidates[0].research_candidate_id, actor="operator", operator_ref="OP-M0086")
    assert first_selected.model_dump(mode="json") == second_selected.model_dump(mode="json")
    assert first_receipt.receipt_id == second_receipt.receipt_id


def test_phrase_adapter_is_not_an_independent_semantic_authority():
    # Phrase mode only exposes exact transcript evidence attached to governed SceneRecords;
    # an unrelated caption with similar semantics must not create a phrase hit.
    records, _, _ = _corpus()
    request = AssetResearchRequest(
        workspace_id="WS-M0086",
        query="dawn location operational choice",
        mode=AssetResearchMode.PHRASE,
    )
    session = _factory().open(request, records)
    assert session.state == AssetResearchSessionState.ABSTAIN
    assert session.candidates == ()
