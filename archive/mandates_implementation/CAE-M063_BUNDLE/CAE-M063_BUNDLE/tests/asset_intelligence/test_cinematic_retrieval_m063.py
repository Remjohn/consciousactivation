import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "asset-intelligence" / "src"))

from cae_asset_intelligence.corpus import CinematicCorpusEngine, CorpusState, MediaAuthorization, SceneProposal  # noqa: E402
from cae_asset_intelligence.domain import EditorialInsertRole, RightsMetadata, RightsStatus, SourceType  # noqa: E402
from cae_asset_intelligence.retrieval import (  # noqa: E402
    DeterministicSemanticEncoder,
    RetrievalQuery,
    RetrievalState,
    RightsPolicy,
    SemanticCinematicRetriever,
)


def _corpus():
    media = (ROOT / "tests" / "api" / "fixtures" / "synthetic_interview.mp4").read_bytes()
    sha = hashlib.sha256(media).hexdigest()
    auth = MediaAuthorization(
        authorization_id="AUTH-M063",
        workspace_id="WS-M063",
        source_sha256=sha,
        source_version="v1",
        approved=True,
        authority_ref="operator-approval:M063-fixture",
    )
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-M063")
    scenes = [
        SceneProposal(
            start_time=0,
            end_time=3,
            contextual_caption="Wide dawn exterior establishes the location before the operational choice and team response.",
            semantic_role="SETTING_ESTABLISHMENT",
            insert_role=EditorialInsertRole.WORLD_BUILDING,
            source_type=SourceType.ARCHIVAL,
        ),
        SceneProposal(
            start_time=3,
            end_time=6,
            contextual_caption="Control-room reaction shows mounting pressure after an operational failure and decisive choice.",
            semantic_role="DECISION_PRESSURE",
            insert_role=EditorialInsertRole.EMOTIONAL_AMPLIFICATION,
            source_type=SourceType.MOVIE,
        ),
    ]
    records, ingest_receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M063", candidate_id="CND-M063", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    index_sha = hashlib.sha256(b"governed-test-index-v1").hexdigest()
    indexed_receipt = ingest_receipt.model_copy(update={"state": CorpusState.INDEXED, "receipt_id": "RCPT-M063-INDEXED", "scene_ids": tuple(r.scene_id for r in records)})
    return records, index_sha, indexed_receipt


def test_paraphrase_retrieval_returns_exact_timestamp_and_context():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="morning place before the choice", min_confidence=0.30)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert proof.state == RetrievalState.RANKED
    assert candidates[0].scene_id == records[0].scene_id
    assert (candidates[0].start_time, candidates[0].end_time) == (0.0, 3.0)
    assert "SETTING_ESTABLISHMENT" == candidates[0].semantic_role
    assert "WORLD_BUILDING" == candidates[0].insert_role.value
    assert "matches" in candidates[0].contextual_explanation.lower()


def test_exact_terminology_is_ranked_and_returns_rights_proof():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="control-room pressure operational failure", min_confidence=0.30)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert proof.state == RetrievalState.RANKED
    assert candidates[0].scene_id == records[1].scene_id
    assert candidates[0].rights_status == RightsStatus.CLEARED
    assert candidates[0].source_sha256 == records[1].source_sha256
    assert candidates[0].source_version == "v1"


def test_role_filter_is_hard_constraint():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(
        workspace_id="WS-M063", query="pressure", insert_roles=(EditorialInsertRole.WORLD_BUILDING,), min_confidence=0.01
    )
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert proof.state in {RetrievalState.RANKED, RetrievalState.ABSTAIN}
    assert all(c.insert_role == EditorialInsertRole.WORLD_BUILDING for c in candidates)


def test_rights_filter_excludes_unlicensed_scene():
    records, index_sha, receipt = _corpus()
    restricted = records[1].model_copy(update={"annotation": records[1].annotation.model_copy(update={"rights": RightsMetadata(status=RightsStatus.RESTRICTED)})})
    query = RetrievalQuery(workspace_id="WS-M063", query="control room pressure", rights_policy=RightsPolicy.CLEARED_ONLY, min_confidence=0.01)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, [records[0], restricted], index_sha256=index_sha, indexed_receipt=receipt)
    assert proof.state == RetrievalState.ABSTAIN
    assert candidates == ()


def test_low_confidence_query_abstains_without_candidates():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="quantum submarine dessert", min_confidence=0.99)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert candidates == ()
    assert proof.state == RetrievalState.ABSTAIN
    assert proof.error_code == "LOW_CONFIDENCE"


def test_wrong_workspace_is_filtered_closed():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-OTHER", query="control room pressure", min_confidence=0.01)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert candidates == ()
    assert proof.state == RetrievalState.BLOCKED


def test_stale_index_hash_blocks_retrieval():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="pressure", expected_index_sha256="b" * 64)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert candidates == ()
    assert proof.state == RetrievalState.BLOCKED
    assert proof.error_code == "RETRIEVAL"


def test_embedding_binding_is_explicit_and_deterministic():
    model = DeterministicSemanticEncoder()
    assert model.model_id == "cae-deterministic-semantic-v1"
    assert model.embed("sunrise pressure") == model.embed("sunrise pressure")
    assert len(model.embed("sunrise pressure")) == model.dimension


def test_false_proof_cosine_nearest_is_not_accepted_below_threshold():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="a beautiful place with no operational choice", min_confidence=0.95)
    candidates, proof = SemanticCinematicRetriever().retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert candidates == ()
    assert proof.state == RetrievalState.ABSTAIN


def test_semantically_close_but_narratively_wrong_candidate_is_rejected_by_role_filter():
    records, index_sha, receipt = _corpus()
    # The pressure scene shares "choice" and "operational" semantics with the query,
    # but the request explicitly asks for a world-building establishing insert.
    query = RetrievalQuery(
        workspace_id="WS-M063",
        query="establish the place before the operational choice",
        insert_roles=(EditorialInsertRole.WORLD_BUILDING,),
        min_confidence=0.01,
    )
    candidates, proof = SemanticCinematicRetriever().retrieve(
        query, records, index_sha256=index_sha, indexed_receipt=receipt
    )
    assert proof.state == RetrievalState.RANKED
    assert candidates
    assert all(candidate.insert_role == EditorialInsertRole.WORLD_BUILDING for candidate in candidates)
    assert records[1].scene_id not in [candidate.scene_id for candidate in candidates]


def test_query_receipt_is_stable_for_same_inputs():
    records, index_sha, receipt = _corpus()
    query = RetrievalQuery(workspace_id="WS-M063", query="control room pressure", min_confidence=0.30)
    retriever = SemanticCinematicRetriever(actor="test")
    _, first = retriever.retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    _, second = retriever.retrieve(query, records, index_sha256=index_sha, indexed_receipt=receipt)
    assert first.receipt_id == second.receipt_id
