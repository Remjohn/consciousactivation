from pathlib import Path

from scene_intelligence_loader import (
    build_scene_intelligence_runtime,
    load_compiled_scene_intelligence_runtime_asset,
    load_component_package,
    load_container_package,
)


def test_load_container_package_validates_schema_contract():
    package = load_container_package("HOOK")

    assert package["contract"]["schema_id"] == "cmf.container.contract/v1"
    assert package["rules"]["schema_id"] == "cmf.container.rules/v1"
    assert package["contract"]["container_id"] == "HOOK"
    assert package["rules"]["container_id"] == "HOOK"
    assert package["contract"]["transportation_state"]["phase"] == "admission"
    assert package["contract"]["prediction_error_budget"]["strategy"] == "pattern_interrupt"


def test_load_component_package_validates_schema_contract():
    package = load_component_package("THE_VISION")

    assert package["spec"]["schema_id"] == "cmf.component.spec/v1"
    assert package["rules"]["schema_id"] == "cmf.component.rules/v1"
    assert package["spec"]["component_id"] == "THE_VISION"
    assert package["rules"]["component_id"] == "THE_VISION"
    assert package["spec"]["audio_profile"]["score_role"] == "fuse_cta"


def test_build_scene_intelligence_runtime_filters_by_stage():
    scene_runtime = build_scene_intelligence_runtime("scene_builder")
    regen_runtime = build_scene_intelligence_runtime("editor_regeneration")

    assert scene_runtime["active_containers"] == [
        "CHALLENGE",
        "HOOK",
        "RESOLUTION",
        "SETUP",
        "TURNING_POINT",
        "VISION",
    ]
    assert "HOOK" in scene_runtime["active_components"]
    assert "THE_VISION" in scene_runtime["active_components"]
    assert scene_runtime["container_component_index"]["VISION"][0] == "THE_VISION"

    assert regen_runtime["active_containers"] == scene_runtime["active_containers"]
    assert "THE_PAUSE" in regen_runtime["active_components"]
    assert "HOOK" not in regen_runtime["active_components"]
    assert regen_runtime["validation_contract"]["component_rules_schema_id"] == "cmf.component.rules/v1"
    assert "HOOK-1-AB-2" in scene_runtime["scene_templates"]
    assert "EFFECT-M-04" in scene_runtime["effect_library"]
    assert scene_runtime["container_template_index"]["HOOK"]
    assert scene_runtime["cognitive_rhythm_validator"]["validator_id"] == "CRV-SCENE-BUILDER-v1"


def test_load_compiled_scene_intelligence_runtime_asset_writes_runtime_json():
    asset = load_compiled_scene_intelligence_runtime_asset("scene_builder")

    assert asset["schema_id"] == "cmf.scene.intelligence.runtime/v1"
    assert asset["asset_id"] == "SIRT-SCENE-BUILDER-v1"
    assert asset["arc_stage_container_map"]["HOOK"] == "HOOK"
    assert asset["arc_stage_container_map"]["CLIMAX"] == "TURNING_POINT"
    assert asset["container_component_index"]["RESOLUTION"]
    assert asset["containers"]["VISION"]["contract"]["default_component"] == "THE_VISION"
    assert asset["containers"]["HOOK"]["contract"]["transportation_state"]["phase"] == "admission"
    assert asset["containers"]["TURNING_POINT"]["contract"]["prediction_error_budget"]["strategy"] == "revelation_violation"
    assert asset["components"]["THE_VISION"]["spec"]["audio_profile"]["score_role"] == "fuse_cta"
    assert asset["components"]["THE_VISION"]["rules"]["warn_conditions"][0]["metric"] == "cta_overlap_seconds"
    assert asset["scene_templates"]["HOOK-1-AB-2"]["target_attention_mode"] == "orienting"
    assert asset["scene_templates"]["VISION-2-C-1"]["peak_end_weight"] == "high"
    assert asset["effect_library"]["EFFECT-M-04"]["attention_role"] == "signal"
    assert asset["cognitive_rhythm_validator"]["asset_path"].endswith("cognitive_rhythm_validator.scene_builder.runtime.json")
    assert Path(asset["asset_path"]).exists()