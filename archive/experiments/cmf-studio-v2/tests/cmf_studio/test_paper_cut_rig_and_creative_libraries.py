from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.acting_library import ActingReferenceStatus  # noqa: E402
from ccp_studio.contracts.brand_genesis import (  # noqa: E402
    BrandGenesisSessionStatus,
    BrandSourceInput,
    NegativeSpaceInput,
    VisualConstitutionInput,
    new_brand_genesis_session,
)
from ccp_studio.contracts.creative_libraries import (  # noqa: E402
    CreativeEvaluationState,
    CreativeItemStatus,
    MotionBeat,
)
from ccp_studio.contracts.rig_manifest import RigLayer, RigPreviewTest  # noqa: E402
from ccp_studio.repositories.brand_genesis_sessions import InMemoryBrandGenesisRepository  # noqa: E402
from ccp_studio.services.acting_library_service import ActingLibraryService  # noqa: E402
from ccp_studio.services.creative_library_service import CreativeLibraryService, CreativeLibraryServiceError  # noqa: E402


BODY_LAYERS = [
    "torso",
    "head",
    "neck",
    "left_upper_arm",
    "left_forearm",
    "left_hand",
    "right_upper_arm",
    "right_forearm",
    "right_hand",
    "left_leg",
    "right_leg",
    "feet",
    "shadow",
]

PREVIEW_TESTS = [
    "blink",
    "nod",
    "open_hands_explanation",
    "pointing",
    "shrug",
    "expression_swap",
    "mouth_flap",
    "subtle_stop_motion_jitter",
]


def _locked_acting_library_context():
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    source_artifact_id = uuid4()
    source_input = BrandSourceInput(
        schema_version="cmf.brand_source_input.v1",
        source_artifact_ids=[source_artifact_id],
        consent_record_version_id=uuid4(),
        source_quality_receipt_ids=[uuid4()],
    )
    genesis_session = new_brand_genesis_session(
        organization_id=org_id,
        brand_id=brand_id,
        brand_notes="Paper-cut explainer brand substrate",
        audience_summary="Expert audience needing warm clarity",
        offer_summary="Interview-first CMF content system",
        forbidden_tone=["hype"],
        visual_preferences=["editorial paper-cut"],
        voice_dna_references=[],
        source_inputs=[source_input],
        visual_constitution_input=VisualConstitutionInput(
            schema_version="cmf.visual_constitution_input.v1",
            visual_preferences=["editorial paper-cut"],
            paper_cut_direction="2.5D paper gently coming alive",
            composition_preferences=["caption-safe vertical layout"],
            style_constraints=["restrained motion"],
        ),
        negative_space_input=NegativeSpaceInput(
            schema_version="cmf.negative_space_input.v1",
            forbidden_tone=["hype"],
            forbidden_visual_motifs=["generic AI neon"],
            avoided_claims=["guaranteed virality"],
            style_boundaries=["no cartoon sticker bounce"],
        ),
        created_by_actor_id=actor_id,
    ).model_copy(update={"status": BrandGenesisSessionStatus.running})
    genesis_repository = InMemoryBrandGenesisRepository()
    genesis_repository.put_session(genesis_session)
    acting = ActingLibraryService(genesis_repository)
    version = acting.generate_reference_grid(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=genesis_session.brand_genesis_session_id,
        source_artifact_ids=[source_artifact_id],
        provider_name="GPT Image 2",
    )
    for reference_id in version.acting_reference_ids:
        acting.evaluate_reference(
            organization_id=org_id,
            brand_id=brand_id,
            acting_reference_id=reference_id,
            likeness_score=0.95,
            gesture_clarity_score=0.95,
            hand_quality_score=0.95,
            paper_texture_score=0.95,
            style_adherence_score=0.95,
            negative_space_score=0.95,
            production_usability_score=0.95,
        )
        acting.approve_reference(
            organization_id=org_id,
            brand_id=brand_id,
            acting_reference_id=reference_id,
        )
    locked = acting.lock_library_version(
        organization_id=org_id,
        brand_id=brand_id,
        acting_library_version_id=version.acting_library_version_id,
    )
    creative = CreativeLibraryService(acting.repository)
    return creative, org_id, brand_id, genesis_session.brand_genesis_session_id, locked, source_artifact_id


def _rig_layers(brand_id):
    return [
        RigLayer(
            schema_version="cmf.rig_layer.v1",
            layer_name=layer,
            asset_uri=f"brands/{brand_id}/rigs/papercut_avatar/{layer}.png",
            pivot_points={"anchor": (0.5, 0.5)},
            layer_hash=f"sha256-{layer}",
            z_index=index * 10,
            parent_layer_name="torso" if layer not in {"torso", "shadow"} else None,
        )
        for index, layer in enumerate(BODY_LAYERS, start=1)
    ]


def _preview_tests(failing=None):
    failing = set(failing or [])
    return [
        RigPreviewTest(
            schema_version="cmf.rig_preview_test.v1",
            test_name=test_name,
            passed=test_name not in failing,
            failure_category=f"{test_name}_failed" if test_name in failing else None,
            evidence_refs=[f"preview:{test_name}"],
        )
        for test_name in PREVIEW_TESTS
    ]


def _valid_rig(creative, org_id, brand_id, session_id, locked_version, failing=None):
    return creative.create_rig_manifest(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        acting_library_version_id=locked_version.acting_library_version_id,
        layers=_rig_layers(brand_id),
        mouth_shape_refs=["closed", "small_open", "wide_open", "smile_open", "oo", "ee", "mbp", "frown"],
        eye_brow_variant_refs=["neutral", "happy", "wide", "skeptical", "concerned", "blink", "focused"],
        gesture_variant_refs=["point_left", "point_right", "open_hands", "chin", "crossed", "one_hand", "celebrate", "shrug"],
        body_layer_refs=BODY_LAYERS,
        preview_tests=_preview_tests(failing=failing),
    )


def _passed_eval():
    return CreativeEvaluationState(
        schema_version="cmf.creative_evaluation_state.v1",
        score=0.91,
        passed=True,
        failure_notes=[],
    )


def test_rig_manifest_includes_layers_pivots_mouth_variants_body_layers_and_preview_tests_before_lock():
    creative, org_id, brand_id, session_id, locked_version, _source_id = _locked_acting_library_context()
    manifest = _valid_rig(creative, org_id, brand_id, session_id, locked_version)

    approved = creative.approve_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=manifest.rig_manifest_id)
    locked = creative.lock_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=manifest.rig_manifest_id)

    assert approved.status == CreativeItemStatus.approved
    assert locked.status == CreativeItemStatus.locked
    assert len(locked.layers) == len(BODY_LAYERS)
    assert all(layer.pivot_points for layer in locked.layers)
    assert "mouth_flap" in {test.test_name for test in locked.preview_tests}
    assert locked.version_hash != "missing"
    assert all(
        creative.acting_repository.references[reference_id].status == ActingReferenceStatus.locked
        for reference_id in locked_version.acting_reference_ids
    )


def test_failed_rig_preview_can_be_repaired_or_rejected_before_lock():
    creative, org_id, brand_id, session_id, locked_version, _source_id = _locked_acting_library_context()
    failed = _valid_rig(creative, org_id, brand_id, session_id, locked_version, failing={"mouth_flap"})

    with pytest.raises(CreativeLibraryServiceError) as exc:
        creative.approve_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=failed.rig_manifest_id)
    assert exc.value.code == "RIG_PREVIEW_FAILED"
    assert creative.rig_repository.manifests[failed.rig_manifest_id].status == CreativeItemStatus.evaluation_failed

    repaired = creative.repair_rig_manifest(
        organization_id=org_id,
        brand_id=brand_id,
        rig_manifest_id=failed.rig_manifest_id,
        preview_tests=_preview_tests(),
        repair_note="fixed mouth flap timing and pivots",
    )
    assert repaired.status == CreativeItemStatus.draft
    approved = creative.approve_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=failed.rig_manifest_id)
    assert approved.status == CreativeItemStatus.approved

    rejected_source = _valid_rig(creative, org_id, brand_id, session_id, locked_version, failing={"pointing"})
    rejected = creative.reject_rig(
        organization_id=org_id,
        brand_id=brand_id,
        rig_manifest_id=rejected_source.rig_manifest_id,
        reason="pointing gesture remains broken",
    )
    assert rejected.status == CreativeItemStatus.rejected


def test_creative_library_items_store_source_version_constraints_and_evaluation_state():
    creative, org_id, brand_id, session_id, _locked_version, _source_id = _locked_acting_library_context()
    anchor = creative.create_micro_semiotic_anchor(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="messy calendar",
        category="ordinary_life_object",
        cultural_context="busy expert operators balancing calls and creation",
        audience_signal="specific daily work pressure",
        recognition_effects=["relatability", "comment_trigger"],
        visual_description="small paper calendar with crossed-out calls",
        preferred_placement=["desk", "corner detail"],
        subtlety_score=0.82,
        comment_potential_score=0.86,
        brand_fit_score=0.9,
        distraction_risk_score=0.12,
        legal_risk_score=0.05,
        use_constraints=["never central subject"],
        source_refs=["Brand Genesis V3 micro-semiotic doctrine"],
    )
    motion = creative.create_motion_recipe(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="myth_busted_reel_v1",
        motion_language="paper_gently_coming_alive",
        motion_intensity="restrained",
        max_simultaneous_moving_layers=4,
        beats=[MotionBeat(beat="hook", duration_seconds=3, actions=["headline_strip_slide_in"])],
        source_refs=["Brand Genesis V3 motion constitution"],
        use_constraints=["must direct attention or reveal meaning"],
        evaluation_state=_passed_eval(),
    )
    sfx = creative.create_sfx_asset(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        category="marker_underline",
        event_mapping="underline draws",
        asset_uri=f"brands/{brand_id}/brand-genesis/{session_id}/sfx/marker_underline.wav",
        use_context="educational emphasis",
        source_refs=["Brand Genesis V3 SFX mapping"],
        evaluation_state=_passed_eval(),
    )

    approved_anchor = creative.approve_creative_item(organization_id=org_id, brand_id=brand_id, item_id=anchor.micro_semiotic_anchor_id)
    approved_motion = creative.approve_creative_item(organization_id=org_id, brand_id=brand_id, item_id=motion.motion_recipe_id)
    approved_sfx = creative.approve_creative_item(organization_id=org_id, brand_id=brand_id, item_id=sfx.sfx_asset_id)

    assert approved_anchor.status == CreativeItemStatus.approved
    assert approved_motion.version_hash
    assert approved_motion.evaluation_state.passed is True
    assert approved_sfx.source_refs
    assert "must direct attention" in approved_motion.use_constraints[0]


def test_platform_profile_drives_caption_negative_space_aspect_and_publishing_requirements():
    creative, org_id, brand_id, _session_id, _locked_version, _source_id = _locked_acting_library_context()
    profile = creative.configure_platform_profile(
        organization_id=org_id,
        brand_id=brand_id,
        platform="instagram_reels",
        aspect_ratio="9:16",
        caption_requirements=["burned-in captions must remain below face line"],
        negative_space_requirements=["reserve upper third for headline strip"],
        publishing_requirements=["safe title and thumbnail required"],
    )

    inherited = creative.render_contract_profile_requirements(
        organization_id=org_id,
        brand_id=brand_id,
        platform_profile_id=profile.platform_profile_id,
    )

    assert inherited["aspect_ratio"] == "9:16"
    assert inherited["caption_requirements"]
    assert inherited["negative_space_requirements"]
    assert inherited["publishing_requirements"]
    assert inherited["profile_version_hash"] == profile.version_hash


def test_cross_brand_creative_item_selection_is_blocked():
    creative, org_id, brand_id, session_id, _locked_version, _source_id = _locked_acting_library_context()
    anchor = creative.create_micro_semiotic_anchor(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="health receipt",
        category="health_object",
        cultural_context="wellness buyers checking real spending",
        audience_signal="ordinary proof object",
        recognition_effects=["trust", "local familiarity"],
        visual_description="small anonymized paper receipt",
        preferred_placement=["desk"],
        subtlety_score=0.8,
        comment_potential_score=0.78,
        brand_fit_score=0.86,
        distraction_risk_score=0.1,
        legal_risk_score=0.02,
        use_constraints=["no real personal data"],
        source_refs=["operator-approved anchor note"],
    )
    approved = creative.approve_creative_item(organization_id=org_id, brand_id=brand_id, item_id=anchor.micro_semiotic_anchor_id)

    with pytest.raises(CreativeLibraryServiceError) as exc:
        creative.select_creative_item(
            organization_id=org_id,
            brand_id=uuid4(),
            item_id=approved.micro_semiotic_anchor_id,
        )

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_flat_avatar_or_missing_source_cannot_enter_locked_creative_library():
    creative, org_id, brand_id, session_id, locked_version, _source_id = _locked_acting_library_context()
    flat = creative.create_rig_manifest(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        acting_library_version_id=locked_version.acting_library_version_id,
        layers=[],
        mouth_shape_refs=[],
        eye_brow_variant_refs=[],
        gesture_variant_refs=[],
        body_layer_refs=[],
        preview_tests=[],
    )
    with pytest.raises(CreativeLibraryServiceError) as approve_exc:
        creative.approve_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=flat.rig_manifest_id)
    assert approve_exc.value.code == "RIG_LAYER_MANIFEST_REQUIRED"
    with pytest.raises(CreativeLibraryServiceError) as lock_exc:
        creative.lock_rig(organization_id=org_id, brand_id=brand_id, rig_manifest_id=flat.rig_manifest_id)
    assert lock_exc.value.code == "RIG_NOT_APPROVED"

    motion = creative.create_motion_recipe(
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=session_id,
        name="avatar_reaction_v1",
        motion_language="paper_gently_coming_alive",
        motion_intensity="restrained",
        max_simultaneous_moving_layers=4,
        beats=[MotionBeat(beat="reaction", duration_seconds=3, actions=["mascot_wave"])],
        source_refs=["Brand Genesis V3"],
        use_constraints=["no childish bounce"],
        evaluation_state=_passed_eval(),
    )
    creative.creative_repository.put_motion_recipe(motion.model_copy(update={"source_refs": []}))
    with pytest.raises(CreativeLibraryServiceError) as source_exc:
        creative.approve_creative_item(organization_id=org_id, brand_id=brand_id, item_id=motion.motion_recipe_id)
    assert source_exc.value.code == "CREATIVE_ITEM_SOURCE_REQUIRED"
