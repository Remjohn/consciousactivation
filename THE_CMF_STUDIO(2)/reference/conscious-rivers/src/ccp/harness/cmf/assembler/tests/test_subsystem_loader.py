from pathlib import Path

from subsystem_loader import (
    build_subsystem_runtime,
    load_compiled_subsystem_runtime_asset,
    load_subsystem_package,
)


def test_load_subsystem_package_validates_schema_contract():
    package = load_subsystem_package("CS-001")

    assert package["config"]["schema_id"] == "cmf.subsystem.config/v1"
    assert package["rules"]["schema_id"] == "cmf.subsystem.rules/v1"
    assert package["config"]["subsystem_id"] == "CS-001"
    assert package["rules"]["subsystem_id"] == "CS-001"


def test_build_subsystem_runtime_filters_by_stage():
    scene_runtime = build_subsystem_runtime(
        "scene_builder",
    )
    regen_runtime = build_subsystem_runtime(
        "editor_regeneration",
    )

    assert "CS-001" in scene_runtime["active_subsystems"]
    assert "CS-002" in scene_runtime["active_subsystems"]
    assert "CS-004" in scene_runtime["active_subsystems"]
    assert "CS-005" in scene_runtime["active_subsystems"]
    assert "CS-013" in scene_runtime["active_subsystems"]
    assert "CS-012" in scene_runtime["active_subsystems"]
    assert "CS-015" in scene_runtime["active_subsystems"]
    assert "CS-023" in scene_runtime["active_subsystems"]
    assert "CS-022" in scene_runtime["active_subsystems"]
    assert "CS-025" in scene_runtime["active_subsystems"]
    assert "CS-011" in scene_runtime["active_subsystems"]
    assert "CS-029" in scene_runtime["active_subsystems"]
    assert "CS-031" in scene_runtime["active_subsystems"]
    assert "CS-033" in scene_runtime["active_subsystems"]

    assert "CS-001" not in regen_runtime["active_subsystems"]
    assert "CS-013" not in regen_runtime["active_subsystems"]
    assert "CS-023" in regen_runtime["active_subsystems"]
    assert "CS-031" not in regen_runtime["active_subsystems"]
    assert "CS-025" not in regen_runtime["active_subsystems"]
    assert "CS-004" in regen_runtime["active_subsystems"]
    assert "CS-002" in regen_runtime["active_subsystems"]
    assert "CS-005" in regen_runtime["active_subsystems"]
    assert "CS-012" in regen_runtime["active_subsystems"]
    assert "CS-015" in regen_runtime["active_subsystems"]
    assert "CS-022" in regen_runtime["active_subsystems"]
    assert "CS-029" in regen_runtime["active_subsystems"]
    assert "CS-032" in regen_runtime["active_subsystems"]
    assert "CS-033" in regen_runtime["active_subsystems"]

    assert scene_runtime["validation_contract"]["config_schema_id"] == "cmf.subsystem.config/v1"
    assert regen_runtime["validation_contract"]["rules_schema_id"] == "cmf.subsystem.rules/v1"


def test_load_compiled_subsystem_runtime_asset_writes_runtime_json():
    asset = load_compiled_subsystem_runtime_asset("scene_builder")

    assert asset["asset_id"] == "SSRT-SCENE-BUILDER-v1"
    assert "CS-011" in asset["active_subsystems"]
    assert "CS-005" in asset["active_subsystems"]
    assert "CS-015" in asset["active_subsystems"]
    assert "CS-023" in asset["active_subsystems"]
    assert "CS-022" in asset["active_subsystems"]
    assert "CS-029" in asset["active_subsystems"]
    assert "CS-031" in asset["active_subsystems"]
    assert "CS-033" in asset["active_subsystems"]
    assert asset["packages"]["CS-023"]["rules"]["warn_conditions"][0]["metric"] == "target_asl_seconds"
    assert Path(asset["asset_path"]).exists()