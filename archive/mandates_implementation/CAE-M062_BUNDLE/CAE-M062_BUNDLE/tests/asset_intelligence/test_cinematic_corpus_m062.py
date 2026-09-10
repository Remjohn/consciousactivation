import hashlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "services" / "asset-intelligence" / "src"))

from cae_asset_intelligence.corpus import (  # noqa: E402
    AuthorizationError,
    CorpusIntegrityError,
    CinematicCorpusEngine,
    CorpusState,
    MediaAuthorization,
    SceneProposal,
    SceneIndex,
    TranscriptCue,
)
from cae_asset_intelligence.corpus_store import SceneCorpusStore  # noqa: E402
from cae_asset_intelligence.domain import RightsMetadata, RightsStatus, SourceType, EditorialInsertRole  # noqa: E402


def _fixture():
    media = (ROOT / "tests" / "api" / "fixtures" / "synthetic_interview.mp4").read_bytes()
    sha = hashlib.sha256(media).hexdigest()
    auth = MediaAuthorization(
        authorization_id="AUTH-M062-001",
        workspace_id="WS-M062",
        source_sha256=sha,
        source_version="v1",
        approved=True,
        authority_ref="operator-approval:M062-fixture",
    )
    rights = RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC-M062-001", copyright_holder="Owned Archive")
    scenes = [
        SceneProposal(
            start_time=0.0,
            end_time=3.0,
            contextual_caption="Owned dawn sequence establishes the operational setting before the human decision point.",
            semantic_role="SETTING_ESTABLISHMENT",
            insert_role=EditorialInsertRole.WORLD_BUILDING,
            source_type=SourceType.REAL_WORLD,
            transcript=(TranscriptCue(start_time=1.0, end_time=2.0, text="We opened before sunrise.", speaker="HOST"),),
        ),
        SceneProposal(
            start_time=3.0,
            end_time=6.0,
            contextual_caption="Control-room reaction visually reinforces the pressure surrounding the decisive operational choice.",
            semantic_role="DECISION_PRESSURE",
            insert_role=EditorialInsertRole.EMOTIONAL_AMPLIFICATION,
            source_type=SourceType.REAL_WORLD,
        ),
    ]
    return media, auth, rights, scenes


def test_authorized_real_media_fixture_ingests_stable_scene_ids_and_receipt():
    media, auth, rights, scenes = _fixture()
    engine = CinematicCorpusEngine(actor="test-agent")
    records_a, receipt_a = engine.ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    records_b, receipt_b = engine.ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    assert receipt_a.state == CorpusState.INGESTED
    assert receipt_a.receipt_id == receipt_b.receipt_id
    assert [r.scene_id for r in records_a] == [r.scene_id for r in records_b]
    assert all(r.annotation.source_sha256 == hashlib.sha256(media).hexdigest() for r in records_a)
    assert records_a[0].transcript[0].text == "We opened before sunrise."


def test_deterministic_reindex_is_idempotent_and_searchable(tmp_path):
    media, auth, rights, scenes = _fixture()
    records, receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    store = SceneCorpusStore(tmp_path)
    for record in records:
        store.put_scene(record)
    store.put_receipt(receipt)
    first = store.reindex().read_text()
    second = store.reindex().read_text()
    assert first == second
    assert store.search("control room pressure") == (records[1].scene_id,)


def test_false_proof_wrong_media_bytes_is_quarantined_and_receipt_preserved():
    media, auth, rights, scenes = _fixture()
    tampered = media[:-1] + bytes([media[-1] ^ 0xFF])
    records, receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=tampered,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    assert records == ()
    assert receipt.state == CorpusState.QUARANTINED
    assert receipt.error_code == "ASSETBYTEHASHMISMATCH"
    assert receipt.source_sha256 == hashlib.sha256(tampered).hexdigest()


def test_cross_workspace_authorization_is_rejected_without_writing_scene():
    media, auth, rights, scenes = _fixture()
    records, receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-OTHER", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    assert records == ()
    assert receipt.state == CorpusState.QUARANTINED
    assert receipt.error_code == "AUTHORIZATION"


def test_overlapping_scene_boundaries_are_rejected():
    media, auth, rights, _ = _fixture()
    scenes = [
        SceneProposal(start_time=0, end_time=5, contextual_caption="First contextual sequence establishes the setting before action.", semantic_role="SETTING"),
        SceneProposal(start_time=4.9, end_time=7, contextual_caption="Second contextual sequence covers the decision pressure and response beat.", semantic_role="PRESSURE"),
    ]
    records, receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    assert records == ()
    assert receipt.state == CorpusState.QUARANTINED
    assert receipt.error_code == "SCENEBOUNDARY"


def test_derived_scene_is_compatible_with_asset_annotation_doctrine():
    media, auth, rights, scenes = _fixture()
    records, _ = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    scene = records[0]
    assert scene.annotation.candidate_id == "CND-M062"
    assert scene.annotation.workspace_id == scene.workspace_id
    assert scene.annotation.insert_role == scene.insert_role
    assert scene.annotation.start_time == scene.start_time
    assert scene.annotation.end_time == scene.end_time


def test_scene_index_is_contrastive_not_generic():
    a = "Archival control-room response makes an operational failure visible under pressure."
    b = "Wide exterior sunrise footage establishes the location before the decision."
    from cae_asset_intelligence.corpus import SceneRecord
    from cae_asset_intelligence.annotator import AssetAnnotator
    from cae_asset_intelligence.domain import MediaType
    common = dict(candidate_id="CND", workspace_id="WS", source_type=SourceType.ARCHIVAL, media_type=MediaType.VIDEO_CLIP,
                  source_sha256="a"*64, rights=RightsMetadata(status=RightsStatus.CLEARED, license_id="LIC"))
    ann_a = AssetAnnotator.annotate_insert(start_time=0, end_time=4, contextual_caption=a, semantic_role="FAILURE_RESPONSE", insert_role=EditorialInsertRole.CONTRAST, **common)
    ann_b = AssetAnnotator.annotate_insert(start_time=4, end_time=6, contextual_caption=b, semantic_role="SETTING", insert_role=EditorialInsertRole.WORLD_BUILDING, **common)
    records = [SceneRecord(scene_id="A", media_id="M", workspace_id="WS", source_version="v1", source_sha256="a"*64,
                           start_time=0, end_time=4, contextual_caption=a, semantic_role="FAILURE_RESPONSE", insert_role=EditorialInsertRole.CONTRAST, annotation=ann_a),
               SceneRecord(scene_id="B", media_id="M", workspace_id="WS", source_version="v1", source_sha256="a"*64,
                           start_time=4, end_time=6, contextual_caption=b, semantic_role="SETTING", insert_role=EditorialInsertRole.WORLD_BUILDING, annotation=ann_b)]
    index = SceneIndex.build(records)
    assert SceneIndex.search(index, "control-room failure") == ("A",)
    assert SceneIndex.search(index, "sunrise location") == ("B",)


def test_indexed_state_has_separate_immutable_receipt_and_exact_source_verification(tmp_path):
    media, auth, rights, scenes = _fixture()
    records, receipt = CinematicCorpusEngine(actor="test-agent").ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    store = SceneCorpusStore(tmp_path)
    for record in records:
        store.put_scene(record)
    store.put_receipt(receipt)
    index_path = store.reindex()
    index_sha = hashlib.sha256(index_path.read_bytes()).hexdigest()
    indexed = CinematicCorpusEngine(actor="test-agent").index_receipt(receipt, [r.scene_id for r in records], index_sha)
    store.put_receipt(indexed)
    assert indexed.state == CorpusState.INDEXED
    assert indexed.receipt_id != receipt.receipt_id
    assert all(store.verify_scene(record, media, 8.5) for record in records)


def test_wrong_bytes_or_stale_time_range_is_rejected_by_scene_verifier(tmp_path):
    media, auth, rights, scenes = _fixture()
    records, _ = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    store = SceneCorpusStore(tmp_path)
    with pytest.raises(CorpusIntegrityError, match="source hash"):
        store.verify_scene(records[0], b"wrong bytes", 8.5)
    with pytest.raises(CorpusIntegrityError, match="time range"):
        store.verify_scene(records[1], media, 4.0)


def test_immutable_receipt_collision_is_rejected(tmp_path):
    media, auth, rights, scenes = _fixture()
    _, receipt = CinematicCorpusEngine().ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    store = SceneCorpusStore(tmp_path)
    store.put_receipt(receipt)
    with pytest.raises(ValueError, match="Immutable record collision"):
        store._put_immutable(store.receipts_dir / f"{receipt.receipt_id}.json", {"tampered": True})


def test_contextual_captioner_hook_and_cinematic_source_type_are_persisted():
    media, auth, rights, _ = _fixture()
    scenes = [SceneProposal(
        start_time=0, end_time=3, contextual_caption="Placeholder description is replaced by the governed captioner output for retrieval.",
        semantic_role="CINEMATIC_PARALLEL", insert_role=EditorialInsertRole.SEMANTIC_SIMILE, source_type=SourceType.MOVIE,
    )]
    engine = CinematicCorpusEngine(captioner=lambda proposal: "Cinematic archival parallel shows the same pressure pattern through a decisive close-up.")
    records, receipt = engine.ingest(
        workspace_id="WS-M062", candidate_id="CND-M062", source_version="v1", source_bytes=media,
        media_duration=6.0, authorization=auth, rights=rights, scenes=scenes,
    )
    assert receipt.state == CorpusState.INGESTED
    assert records[0].annotation.source_type == SourceType.MOVIE
    assert records[0].contextual_caption.startswith("Cinematic archival parallel")
