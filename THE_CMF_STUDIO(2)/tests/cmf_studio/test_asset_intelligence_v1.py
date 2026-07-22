import pytest

from ccp_studio.contracts.asset_intelligence import (
    AssetClass,
    AssetKind,
    AssetOrigin,
    AssetRecord,
    AssetRetrievalQuery,
    AssetRole,
    AssetUseMode,
    AssetVersion,
    ProductionRole,
    RequestingComponent,
    ReviewStatus,
    RightsProvenanceProfile,
    RightsTier,
)
from ccp_studio.services.asset_intelligence_adapters import AssetIntelligenceAdapters
from ccp_studio.services.asset_intelligence_service import AssetIntelligenceService


def test_asset_record_requires_brand_id():
    with pytest.raises(Exception):
        AssetRecord(
            brand_id="",
            asset_kind=AssetKind.SOURCE_PHOTO,
            asset_origin=AssetOrigin.BRAND_UPLOADED,
            display_name="Notebook",
        )


def test_asset_version_requires_hash():
    with pytest.raises(Exception):
        AssetVersion(asset_id="asset_1", sha256="")


def test_unknown_rights_cannot_be_direct_use():
    with pytest.raises(Exception):
        RightsProvenanceProfile(
            asset_id="asset_1",
            rights_tier=RightsTier.UNKNOWN,
            direct_use_allowed=True,
        )


def test_reference_only_asset_can_be_style_reference():
    rights = RightsProvenanceProfile(
        asset_id="asset_1",
        rights_tier=RightsTier.REFERENCE_ONLY,
        direct_use_allowed=False,
        style_reference_allowed=True,
    )
    assert rights.allows(AssetUseMode.STYLE_REFERENCE_ONLY)
    assert not rights.allows(AssetUseMode.DIRECT_USE)


def test_blocked_asset_is_not_retrieved():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.SOURCE_PHOTO,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Blocked object",
    )
    service.fingerprint_asset(asset.asset_id, content_bytes=b"blocked")
    service.attach_rights_profile(
        asset.asset_id,
        rights_tier=RightsTier.OWNED,
        direct_use_allowed=True,
    )
    service.block_asset(asset.asset_id, reason="test")

    query = AssetRetrievalQuery(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        required_use_mode=AssetUseMode.DIRECT_USE,
        max_candidates=10,
    )
    assert service.retrieve_candidates(query) == []


def test_micro_semiotic_anchor_adapts_to_creative_ingredient():
    ingredient = AssetIntelligenceAdapters.adapt_micro_semiotic_anchor(
        {
            "anchor_id": "anchor_1",
            "display_name": "Worn notebook",
            "description": "ordinary-life proof object",
        },
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    assert ingredient.ingredient_kind == "micro_semiotic_anchor"
    assert ingredient.brand_context_version_id == "bcv_1"
    assert "asset_from_anchor_anchor_1" in ingredient.source_asset_ids


def test_visual_candidate_adapts_with_rights_profile():
    asset, rights = AssetIntelligenceAdapters.adapt_visual_candidate(
        {
            "candidate_id": "candidate_1",
            "title": "Kitchen table reference",
            "source_url": "https://example.invalid/kitchen.jpg",
            "licensing": "reference_only",
        },
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
    )
    assert asset.asset_kind == AssetKind.VISUAL_REFERENCE
    assert rights.rights_tier == RightsTier.REFERENCE_ONLY
    assert rights.reference_use_allowed


def test_asset_retrieval_respects_brand_context_version():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_right",
        asset_kind=AssetKind.SOURCE_PHOTO,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Approved object",
    )
    service.fingerprint_asset(asset.asset_id, content_bytes=b"approved")
    service.attach_rights_profile(
        asset.asset_id,
        rights_tier=RightsTier.OWNED,
        direct_use_allowed=True,
    )

    wrong_query = AssetRetrievalQuery(
        brand_id="brand_1",
        brand_context_version_id="bcv_wrong",
        requesting_component=RequestingComponent.SUPERVISUAL,
        required_use_mode=AssetUseMode.DIRECT_USE,
    )
    assert service.retrieve_candidates(wrong_query) == []


def test_candidate_match_requires_use_mode_and_scores():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.SOURCE_PHOTO,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Notebook",
    )
    service.fingerprint_asset(asset.asset_id, content_bytes=b"notebook")
    service.attach_rights_profile(
        asset.asset_id,
        rights_tier=RightsTier.OWNED,
        direct_use_allowed=True,
    )
    service.classify_asset(
        asset.asset_id,
        asset_classes=[AssetClass.OBJECT],
        asset_roles=[AssetRole.PROOF_OBJECT],
        production_roles=[ProductionRole.DIRECT_VISUAL],
    )

    query = AssetRetrievalQuery(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        desired_asset_roles=[AssetRole.PROOF_OBJECT],
        required_use_mode=AssetUseMode.DIRECT_USE,
    )
    matches = service.retrieve_candidates(query)
    assert len(matches) == 1
    assert matches[0].use_mode == AssetUseMode.DIRECT_USE
    assert 0 <= matches[0].total_score <= 1


def test_reference_board_reports_missing_required_ingredients():
    service = AssetIntelligenceService()
    query = AssetRetrievalQuery(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        required_use_mode=AssetUseMode.REFERENCE_ONLY,
    )
    board = service.build_reference_board(
        query=query,
        candidates=[],
        required_roles=[AssetRole.PROOF_OBJECT],
        semantic_need="Need a source-grounded proof object.",
    )
    assert len(board.missing_gaps) == 1
    assert board.missing_gaps[0].required_role == AssetRole.PROOF_OBJECT


def test_asset_usage_receipt_records_component_and_composition_role():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.SOURCE_VIDEO,
        asset_origin=AssetOrigin.INTERVIEW_CAPTURED,
        display_name="Interview clip",
    )
    receipt = service.record_usage(
        asset_id=asset.asset_id,
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.VIDEO,
        used_as=AssetUseMode.DIRECT_USE,
        scene_ref="scene_1",
        beat_ref="beat_1",
        timeline_range=(12.0, 15.0),
        composition_role="talking_head_source",
    )
    assert receipt.requesting_component == RequestingComponent.VIDEO
    assert receipt.timeline_range == (12.0, 15.0)


def test_fatigue_record_demotes_overused_asset():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.SOURCE_PHOTO,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Repeated object",
    )
    for i in range(8):
        service.record_usage(
            asset_id=asset.asset_id,
            brand_id="brand_1",
            brand_context_version_id="bcv_1",
            requesting_component=RequestingComponent.SUPERVISUAL,
            used_as=AssetUseMode.REFERENCE_ONLY,
            output_ref=f"output_{i}",
        )
    fatigue = service.compute_fatigue(asset.asset_id)
    assert fatigue.fatigue_score >= 0.7


def test_winner_promotion_requires_performance_threshold():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.SOURCE_PHOTO,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Winner object",
    )
    with pytest.raises(Exception):
        service.promote_winner(asset.asset_id)

    service.update_performance(asset_id=asset.asset_id, brand_id="brand_1", performance_score=0.8)
    winner = service.promote_winner(asset.asset_id)
    assert winner.approved
    assert winner.performance_score >= 0.65


def test_supervisual_can_retrieve_reference_board_from_asset_intelligence():
    service = AssetIntelligenceService()
    asset = service.ingest_asset(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        asset_kind=AssetKind.PROOF_OBJECT,
        asset_origin=AssetOrigin.BRAND_UPLOADED,
        display_name="Receipt on desk",
    )
    service.fingerprint_asset(asset.asset_id, content_bytes=b"receipt")
    service.attach_rights_profile(
        asset.asset_id,
        rights_tier=RightsTier.OWNED,
        direct_use_allowed=True,
    )
    service.classify_asset(
        asset.asset_id,
        asset_classes=[AssetClass.DOCUMENT],
        asset_roles=[AssetRole.PROOF_OBJECT],
        production_roles=[ProductionRole.DIRECT_VISUAL],
    )
    service.compile_semantic_profile(
        asset.asset_id,
        literal_description="A real receipt on a desk.",
        proof_signal="source-backed documentary proof",
    )
    service.create_creative_ingredient(
        asset.asset_id,
        ingredient_kind="proof_object",
        display_name="Receipt proof object",
        semantic_need="source-grounded proof",
        use_modes=[AssetUseMode.DIRECT_USE],
    )

    query = AssetRetrievalQuery(
        brand_id="brand_1",
        brand_context_version_id="bcv_1",
        requesting_component=RequestingComponent.SUPERVISUAL,
        desired_asset_roles=[AssetRole.PROOF_OBJECT],
        required_use_mode=AssetUseMode.DIRECT_USE,
        max_candidates=3,
    )
    candidates = service.retrieve_candidates(query)
    board = service.build_reference_board(
        query=query,
        candidates=candidates,
        required_roles=[AssetRole.PROOF_OBJECT],
    )
    assert len(candidates) == 1
    assert board.missing_gaps == []
    assert AssetRole.PROOF_OBJECT.value in board.grouped_asset_ids
