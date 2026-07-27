"""Legitimacy Runner Test Suite — DEP-VID-032/033/034 execution."""

import json
import tempfile
from pathlib import Path

from legitimacy_runner import (
    build_regeneration_legitimacy_context,
    build_scene_legitimacy_context,
    run_legitimacy_check,
)


def test_scene_legitimacy_writes_manifest_and_receipt():
    parsed_result = {
        "project_id": "03_50-12",
        "beat_cluster_id": "BC-WITNESS-42",
        "arc_type": "witness",
        "total_duration_sec": 42.0,
    }
    resolved_beats = [
        {
            "beat_index": 0,
            "arc_stage": "challenge",
            "color_temperature_k": 4200,
            "motion_profile": "static",
            "pace_profile": "slow",
            "framing": "wide",
        },
        {
            "beat_index": 1,
            "arc_stage": "vision",
            "color_temperature_k": 5600,
            "motion_profile": "breathing",
            "pace_profile": "measured",
            "framing": "mcu",
        },
    ]
    manifest_candidate = {"manifest_id": "MAN-VID-20260324-001", "beats": resolved_beats}

    context, target_ref, project_id = build_scene_legitimacy_context(
        parsed_result,
        resolved_beats,
        manifest_candidate=manifest_candidate,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        manifest, receipt = run_legitimacy_check(
            compile_target="SCENE_BUILDER",
            project_id=project_id,
            target_ref=target_ref,
            context=context,
            receipt_output_dir=tmpdir,
        )

        manifest_path = Path(
            next(output["path"] for output in manifest["output_files"] if output["kind"] == "constraint_manifest")
        )
        receipt_path = Path(
            next(output["path"] for output in manifest["output_files"] if output["kind"] == "receipt")
        )

        assert manifest["compile_target"] == "SCENE_BUILDER"
        assert manifest_path.exists()
        assert receipt_path.exists()
        assert "subsystem_runtime" in manifest
        assert "CS-001" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-004" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-005" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-012" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-015" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-023" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-022" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-025" in manifest["subsystem_runtime"]["active_subsystems"]
        assert "CS-031" in manifest["subsystem_runtime"]["active_subsystems"]
        assert Path(manifest["subsystem_runtime"]["asset_path"]).exists()
        disk_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert disk_manifest["proof_receipt"]["receipt_id"] == receipt["receipt_id"]


def test_regen_legitimacy_blocks_off_target_drift():
    request = {
        "beat_index": 3,
        "mode": "T2I_ONLY",
        "revision_note": "warmer lighting",
        "changed_paths": [
            "/beats/3/video_clip_url",
            "/beats/4/video_clip_url",
        ],
    }
    plan = {"mode": "T2I_ONLY"}
    fingerprint_entry = {
        "active_fingerprint_id": "FP-VID-20260324-001-B03",
        "fingerprint": {"fingerprint_id": "FP-VID-20260324-001-B03"},
        "regeneration_history": [{"mode": "T2I_ONLY"}],
    }
    context, target_ref, project_id = build_regeneration_legitimacy_context(
        request,
        plan,
        fingerprint_entry,
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        manifest, _ = run_legitimacy_check(
            compile_target="EDITOR_REGENERATION",
            project_id=project_id,
            target_ref=target_ref,
            context=context,
            receipt_output_dir=tmpdir,
        )

    assert manifest["decision"] == "BLOCK"
    assert "CS-004" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-005" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-012" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-015" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-023" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-022" in manifest["subsystem_runtime"]["active_subsystems"]
    assert "CS-032" in manifest["subsystem_runtime"]["active_subsystems"]
    assert any("Limit the patch" in action for action in manifest["required_actions"])