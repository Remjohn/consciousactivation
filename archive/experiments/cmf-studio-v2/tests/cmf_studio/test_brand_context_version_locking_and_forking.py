from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.acting_library import (  # noqa: E402
    ActingLibraryVersion,
    ActingProviderReceipt,
    ActingReference,
    ActingReferenceStatus,
    acting_reference_content_hash,
    acting_state_matrix,
)
from ccp_studio.contracts.brand_context import BrandContextAssetBundle, BrandContextStatus  # noqa: E402
from ccp_studio.contracts.creative_libraries import (  # noqa: E402
    CompositionPreference,
    CreativeEvaluationState,
    CreativeItemStatus,
    MicroSemioticAnchor,
    MotionBeat,
    MotionRecipe,
    PlatformProfile,
    SfxAsset,
    creative_hash,
)
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.rig_manifest import RigLayer, RigManifest, RigPreviewTest  # noqa: E402
from ccp_studio.repositories.acting_library import InMemoryActingLibraryRepository  # noqa: E402
from ccp_studio.repositories.creative_library_items import InMemoryCreativeLibraryRepository  # noqa: E402
from ccp_studio.repositories.rig_manifests import InMemoryRigManifestRepository  # noqa: E402
from ccp_studio.services.brand_context_service import BrandContextService, BrandContextServiceError  # noqa: E402


def _approved_context_assets():
    org_id = uuid4()
    brand_id = uuid4()
    session_id = uuid4()
    actor_id = uuid4()
    acting_repo = InMemoryActingLibraryRepository()
    acting_version_id = uuid4()
    provider_receipt = ActingProviderReceipt(
        schema_version="cmf.acting_provider_receipt.v1",
        provider_receipt_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        provider_name="GPT Image 2",
        request_hash="sha256-request",
        artifact_uri=f"brands/{brand_id}/brand-genesis/{session_id}/acting_library/ref.png",
        source_artifact_ids=[uuid4()],
        written_at=utc_now(),
    )
    acting_repo.put_provider_receipt(provider_receipt)
    acting_reference = ActingReference(
        schema_version="cmf.acting_reference.v1",
        acting_reference_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        acting_library_version_id=acting_version_id,
        state_cell=acting_state_matrix()[0],
        source_artifact_ids=provider_receipt.source_artifact_ids,
        provider_receipt_id=provider_receipt.provider_receipt_id,
        artifact_uri=provider_receipt.artifact_uri,
        content_hash=acting_reference_content_hash([provider_receipt.artifact_uri, provider_receipt.request_hash]),
        body_language="open_hands_explaining",
        facial_expression="confident",
        energy_level="medium_high",
        framing="medium_shot",
        orientation="front_3_4",
        layout_bias="right_side_subject",
        status=ActingReferenceStatus.locked,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    acting_repo.put_reference(acting_reference)
    acting_version = ActingLibraryVersion(
        schema_version="cmf.acting_library_version.v1",
        acting_library_version_id=acting_version_id,
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        version_hash="sha256-acting-library",
        acting_reference_ids=[acting_reference.acting_reference_id],
        locked=True,
        locked_at=utc_now(),
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    acting_repo.put_version(acting_version)

    rig_repo = InMemoryRigManifestRepository()
    rig = RigManifest(
        schema_version="cmf.rig_manifest.v1",
        rig_manifest_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        acting_library_version_id=acting_version.acting_library_version_id,
        layers=[
            RigLayer(
                schema_version="cmf.rig_layer.v1",
                layer_name="head",
                asset_uri=f"brands/{brand_id}/rigs/head.png",
                pivot_points={"anchor": (0.5, 0.5)},
                layer_hash="sha256-head",
                z_index=10,
            )
        ],
        mouth_shape_refs=["closed", "small_open", "wide_open", "smile_open"],
        eye_brow_variant_refs=["neutral", "happy", "wide", "focused"],
        gesture_variant_refs=["open_hands", "pointing", "shrug", "one_hand"],
        body_layer_refs=["head"],
        preview_tests=[
            RigPreviewTest(
                schema_version="cmf.rig_preview_test.v1",
                test_name="mouth_flap",
                passed=True,
                evidence_refs=["preview:mouth_flap"],
            )
        ],
        version_hash="sha256-rig",
        status=CreativeItemStatus.locked,
        created_at=utc_now(),
        updated_at=utc_now(),
        locked_at=utc_now(),
    )
    rig_repo.put_manifest(rig)

    creative_repo = InMemoryCreativeLibraryRepository()
    anchor = MicroSemioticAnchor(
        schema_version="cmf.micro_semiotic_anchor.v1",
        micro_semiotic_anchor_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="messy calendar",
        category="ordinary_life_object",
        cultural_context="operator audience",
        audience_signal="daily work pressure",
        recognition_effects=["relatability"],
        visual_description="small paper calendar",
        preferred_placement=["desk"],
        subtlety_score=0.84,
        comment_potential_score=0.81,
        brand_fit_score=0.9,
        distraction_risk_score=0.1,
        legal_risk_score=0.02,
        use_constraints=["never central subject"],
        source_refs=["Brand Genesis V3"],
        version_hash=creative_hash({"anchor": "messy calendar"}),
        status=CreativeItemStatus.approved,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    motion = MotionRecipe(
        schema_version="cmf.motion_recipe.v1",
        motion_recipe_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="myth_busted_reel_v1",
        motion_language="paper_gently_coming_alive",
        motion_intensity="restrained",
        max_simultaneous_moving_layers=4,
        beats=[MotionBeat(beat="hook", duration_seconds=3, actions=["headline_strip_slide_in"])],
        use_constraints=["direct attention"],
        source_refs=["Brand Genesis V3"],
        version_hash=creative_hash({"motion": "myth_busted_reel_v1"}),
        evaluation_state=CreativeEvaluationState(schema_version="cmf.creative_evaluation_state.v1", score=0.9, passed=True),
        status=CreativeItemStatus.approved,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    sfx = SfxAsset(
        schema_version="cmf.sfx_asset.v1",
        sfx_asset_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        category="paper_pop",
        event_mapping="paper card drops",
        asset_uri=f"brands/{brand_id}/brand-genesis/{session_id}/sfx/paper_pop.wav",
        use_context="paper emphasis",
        source_refs=["Brand Genesis V3"],
        version_hash=creative_hash({"sfx": "paper_pop"}),
        evaluation_state=CreativeEvaluationState(schema_version="cmf.creative_evaluation_state.v1", score=0.9, passed=True),
        status=CreativeItemStatus.approved,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    composition = CompositionPreference(
        schema_version="cmf.composition_preference.v1",
        composition_preference_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="caption-safe vertical",
        aspect_ratio="9:16",
        subject_placement="lower_right",
        text_safe_zones=["upper_third"],
        negative_space_rules=["reserve upper third"],
        source_refs=["Brand Genesis V3"],
        version_hash=creative_hash({"composition": "caption-safe vertical"}),
        evaluation_state=CreativeEvaluationState(schema_version="cmf.creative_evaluation_state.v1", score=0.9, passed=True),
        status=CreativeItemStatus.approved,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    platform = PlatformProfile(
        schema_version="cmf.platform_profile.v1",
        platform_profile_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        platform="instagram_reels",
        aspect_ratio="9:16",
        caption_requirements=["captions below face line"],
        negative_space_requirements=["reserve upper third"],
        publishing_requirements=["safe thumbnail"],
        version_hash=creative_hash({"platform": "instagram_reels"}),
        status=CreativeItemStatus.approved,
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    creative_repo.put_anchor(anchor)
    creative_repo.put_motion_recipe(motion)
    creative_repo.put_sfx_asset(sfx)
    creative_repo.put_composition_preference(composition)
    creative_repo.put_platform_profile(platform)
    service = BrandContextService(acting_repo, rig_repo, creative_repo)
    bundle = BrandContextAssetBundle(
        schema_version="cmf.brand_context_asset_bundle.v1",
        acting_library_version_id=acting_version.acting_library_version_id,
        rig_manifest_id=rig.rig_manifest_id,
        micro_semiotic_anchor_ids=[anchor.micro_semiotic_anchor_id],
        motion_recipe_ids=[motion.motion_recipe_id],
        sfx_asset_ids=[sfx.sfx_asset_id],
        composition_preference_ids=[composition.composition_preference_id],
        platform_profile_ids=[platform.platform_profile_id],
        creative_library_receipt_ids=[uuid4()],
        evaluation_receipt_ids=[uuid4()],
    )
    return service, org_id, brand_id, session_id, actor_id, bundle, {
        "acting": acting_version,
        "rig": rig,
        "anchor": anchor,
        "motion": motion,
        "sfx": sfx,
        "composition": composition,
        "platform": platform,
    }


def test_locking_brand_context_writes_genesis_clearance_certificate_after_assets_pass_review():
    service, org_id, brand_id, session_id, actor_id, bundle, assets = _approved_context_assets()
    draft = service.create_draft(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        asset_bundle=bundle,
        created_by_actor_id=actor_id,
    )

    locked = service.lock_version(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=draft.brand_context_version_id,
        approved_by_actor_id=actor_id,
    )
    certificate = service.repository.certificates[locked.clearance_certificate_id]

    assert locked.status == BrandContextStatus.locked
    assert certificate.brand_context_version_id == locked.brand_context_version_id
    assert certificate.acting_library_version_id == assets["acting"].acting_library_version_id
    assert certificate.rig_manifest_id == assets["rig"].rig_manifest_id
    assert certificate.version_hash == locked.version_hash


def test_brand_context_lock_blocks_missing_or_failed_genesis_assets():
    service, org_id, brand_id, session_id, actor_id, bundle, assets = _approved_context_assets()
    failed_rig = assets["rig"].model_copy(
        update={
            "rig_manifest_id": uuid4(),
            "status": CreativeItemStatus.evaluation_failed,
            "version_hash": "sha256-failed-rig",
            "locked_at": None,
        }
    )
    service.rig_repository.put_manifest(failed_rig)
    failed_bundle = bundle.model_copy(update={"rig_manifest_id": failed_rig.rig_manifest_id})

    with pytest.raises(BrandContextServiceError) as exc:
        service.create_draft(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session_id,
            asset_bundle=failed_bundle,
            created_by_actor_id=actor_id,
        )

    assert exc.value.code == "RIG_NOT_APPROVED"


def test_production_selects_only_assets_approved_inside_locked_brand_context():
    service, org_id, brand_id, session_id, actor_id, bundle, assets = _approved_context_assets()
    draft = service.create_draft(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        asset_bundle=bundle,
        created_by_actor_id=actor_id,
    )
    with pytest.raises(BrandContextServiceError) as draft_exc:
        service.assert_context_selectable_for_production(
            organization_id=org_id,
            brand_id=brand_id,
            brand_context_version_id=draft.brand_context_version_id,
        )
    assert draft_exc.value.code == "BRAND_CONTEXT_NOT_LOCKED"

    locked = service.lock_version(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=draft.brand_context_version_id,
        approved_by_actor_id=actor_id,
    )
    service.assert_asset_in_locked_context(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=locked.brand_context_version_id,
        asset_id=assets["anchor"].micro_semiotic_anchor_id,
    )
    with pytest.raises(BrandContextServiceError) as asset_exc:
        service.assert_asset_in_locked_context(
            organization_id=org_id,
            brand_id=brand_id,
            brand_context_version_id=locked.brand_context_version_id,
            asset_id=uuid4(),
        )
    assert asset_exc.value.code == "BRAND_CONTEXT_ASSET_NOT_APPROVED"


def test_core_identity_change_forks_new_context_and_old_render_resolves_original_version():
    service, org_id, brand_id, session_id, actor_id, bundle, assets = _approved_context_assets()
    v1 = service.lock_version(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=service.create_draft(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session_id,
            asset_bundle=bundle,
            created_by_actor_id=actor_id,
        ).brand_context_version_id,
        approved_by_actor_id=actor_id,
    )
    lineage = service.record_lineage_ref(
        organization_id=org_id,
        brand_id=brand_id,
        downstream_object_id=uuid4(),
        downstream_object_type="render_output",
        brand_context_version_id=v1.brand_context_version_id,
    )
    new_motion = assets["motion"].model_copy(
        update={
            "motion_recipe_id": uuid4(),
            "version_hash": creative_hash({"motion": "gentler_myth_busted_reel_v2"}),
            "name": "gentler_myth_busted_reel_v2",
        }
    )
    service.creative_repository.put_motion_recipe(new_motion)
    replacement_bundle = bundle.model_copy(update={"motion_recipe_ids": [new_motion.motion_recipe_id]})

    child = service.fork_version(
        organization_id=org_id,
        brand_id=brand_id,
        parent_brand_context_version_id=v1.brand_context_version_id,
        replacement_asset_bundle=replacement_bundle,
        requested_by_actor_id=actor_id,
        approved_by_actor_id=actor_id,
        approved_change_reason="soften motion recipe for calmer brand posture",
    )
    parent_after_fork = service.repository.versions[v1.brand_context_version_id]
    resolved_old = service.resolve_lineage_ref(lineage.lineage_ref_id)

    assert child.parent_brand_context_version_id == v1.brand_context_version_id
    assert child.version_hash != v1.version_hash
    assert parent_after_fork.status == BrandContextStatus.superseded
    assert resolved_old.brand_context_version_id == v1.brand_context_version_id
    assert resolved_old.version_hash == lineage.brand_context_version_hash


def test_stale_or_cross_brand_context_blocks_scenespec_compilation():
    service, org_id, brand_id, session_id, actor_id, bundle, assets = _approved_context_assets()
    parent = service.lock_version(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=service.create_draft(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session_id,
            asset_bundle=bundle,
            created_by_actor_id=actor_id,
        ).brand_context_version_id,
        approved_by_actor_id=actor_id,
    )
    new_platform = assets["platform"].model_copy(
        update={"platform_profile_id": uuid4(), "version_hash": creative_hash({"platform": "linkedin_video"})}
    )
    service.creative_repository.put_platform_profile(new_platform)
    child = service.fork_version(
        organization_id=org_id,
        brand_id=brand_id,
        parent_brand_context_version_id=parent.brand_context_version_id,
        replacement_asset_bundle=bundle.model_copy(update={"platform_profile_ids": [new_platform.platform_profile_id]}),
        requested_by_actor_id=actor_id,
        approved_by_actor_id=actor_id,
        approved_change_reason="add LinkedIn-safe platform profile",
    )

    with pytest.raises(BrandContextServiceError) as stale_exc:
        service.assert_context_selectable_for_production(
            organization_id=org_id,
            brand_id=brand_id,
            brand_context_version_id=parent.brand_context_version_id,
        )
    assert stale_exc.value.code == "BRAND_CONTEXT_SUPERSEDED_REVIEW_REQUIRED"

    with pytest.raises(BrandContextServiceError) as brand_exc:
        service.assert_context_selectable_for_production(
            organization_id=org_id,
            brand_id=uuid4(),
            brand_context_version_id=child.brand_context_version_id,
        )
    assert brand_exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_repository_prevents_locked_context_mutation():
    service, org_id, brand_id, session_id, actor_id, bundle, _assets = _approved_context_assets()
    locked = service.lock_version(
        organization_id=org_id,
        brand_id=brand_id,
        brand_context_version_id=service.create_draft(
            organization_id=org_id,
            brand_id=brand_id,
            brand_genesis_session_id=session_id,
            asset_bundle=bundle,
            created_by_actor_id=actor_id,
        ).brand_context_version_id,
        approved_by_actor_id=actor_id,
    )

    with pytest.raises(ValueError):
        service.repository.put_version(locked.model_copy(update={"version_hash": "tampered"}))
