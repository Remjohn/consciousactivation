from ccp_studio.services.avatar_asset_production_service import AvatarAssetProductionService
from ccp_studio.services.avatar_performance_service import AvatarPerformanceLayerService


def test_avatar_asset_stack_covers_performance_expression_and_stays_no_lipsync():
    asset_service = AvatarAssetProductionService()
    spec = asset_service.create_character_spec(
        avatar_id="coach_avatar_v1",
        brand_id="brand_avatar_demo",
        brand_context_version_id="bcv_avatar_demo_v1",
    )
    asset_stack = asset_service.compile_default_asset_stack(spec)

    performance_plan = AvatarPerformanceLayerService().compile_performance_plan(
        avatar_id=spec.avatar_id,
        scene_id="scene_1",
    )

    approved_expression_values = {
        plate.expression_name.value
        for plate in asset_stack["face_plate_approval_set"].face_plates
    }
    performance_expression_values = {
        state.expression_name.value
        for state in performance_plan.performance_states
    }

    assert performance_expression_values.issubset(approved_expression_values)
    assert not performance_plan.lip_sync_enabled
    assert not asset_stack["action_timeline"].lip_sync_enabled
    assert all(not clip.lip_sync_enabled and not clip.mouth_flap for clip in asset_stack["action_timeline"].clips)
