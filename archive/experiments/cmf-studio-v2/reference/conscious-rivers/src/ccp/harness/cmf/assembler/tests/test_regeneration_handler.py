"""
Regeneration Handler + Gate H Test Suite — FR-VID-05

Tests 3-mode regeneration logic, cascade enforcement, seed preservation,
revision-to-prompt mapping, history integrity, Gate H violations, and
regeneration limits.

Maps to FR-VID-05 §8 AC2-AC5, §10 Testing Strategy.
"""

import tempfile
from pathlib import Path

from regeneration_handler import (
    validate_regeneration_request,
    map_revision_to_blocks,
    enhance_prompt_with_revision,
    compute_seed_locks,
    build_regeneration_plan,
    execute_regeneration,
    check_regeneration_limit,
    merge_regeneration_requests,
    VALID_MODES,
)
from gates.gate_h import (
    check_cascade_completeness,
    check_seed_preservation,
    check_revision_note_specificity,
    check_budget_impact,
    check_history_integrity,
    run_gate_h,
)
from fingerprint_tracker import (
    create_fingerprint_from_t2i,
    update_fingerprint_with_i2v,
    create_beat_fingerprint_map,
)


# ===================================================================
# Helpers
# ===================================================================


def _make_t2i(seed=42891, beat=0):
    return {
        "workflow_id": "RH-WF-CMF-T2I-FLUX-001",
        "prompt_used": "Close-up of hands gripping a journal",
        "negative_prompt": "blurry",
        "seed": seed,
        "model": "flux-dev-fp8",
        "pssl_params": {},
        "output_image_url": f"https://r2.cmf-assets.com/t2i/b{beat}.png",
        "quality_score": 0.79,
    }


def _make_i2v(beat=0, seed=77204):
    return {
        "workflow_id": "RH-WF-CMF-I2V-SVD-001",
        "input_keyframe_url": f"https://r2.cmf-assets.com/t2i/b{beat}.png",
        "motion_parameters_applied": {
            "motion_bucket_id": 127, "camera_motion": "slow_zoom_in",
        },
        "output_video_url": f"https://r2.cmf-assets.com/i2v/b{beat}.mp4",
        "seed_used": seed,
        "vram_tier_used": "48GB",
    }


def _make_12_beat_map():
    """Build a 12-beat fingerprint map for testing."""
    entries = []
    for i in range(12):
        e = create_fingerprint_from_t2i(i, _make_t2i(seed=1000 + i, beat=i), "20260321", 1)
        e = update_fingerprint_with_i2v(e, _make_i2v(beat=i, seed=2000 + i))
        entries.append(e)
    return create_beat_fingerprint_map(
        "CMF-VID-20260321-001", "03_50-12", "BC-WITNESS-42", entries
    )


# ===================================================================
# Revision Note → Block Mapping — §3 Technical Decision 6
# ===================================================================


class TestRevisionNoteMapping:
    def test_lighting_keyword(self):
        result = map_revision_to_blocks("make the lighting warmer")
        assert 4 in result["target_blocks"]
        assert not result["unmappable"]

    def test_color_maps_two_blocks(self):
        result = map_revision_to_blocks("change the color palette")
        assert 4 in result["target_blocks"]
        assert 6 in result["target_blocks"]

    def test_character_keyword(self):
        result = map_revision_to_blocks("change the character's expression")
        assert 1 in result["target_blocks"]

    def test_environment_keyword(self):
        result = map_revision_to_blocks("different background setting")
        assert 2 in result["target_blocks"]

    def test_cinematography_keyword(self):
        result = map_revision_to_blocks("wider angle shot")
        assert 3 in result["target_blocks"]

    def test_motion_triggers_i2v_redirect(self):
        result = map_revision_to_blocks("slower camera motion")
        assert result["i2v_redirect"] is True

    def test_vague_note_unmappable(self):
        result = map_revision_to_blocks("make it better")
        assert result["unmappable"] is True

    def test_empty_note_unmappable(self):
        result = map_revision_to_blocks("")
        assert result["unmappable"] is True

    def test_multiple_keywords(self):
        result = map_revision_to_blocks("warmer lighting and different background")
        assert 2 in result["target_blocks"]
        assert 4 in result["target_blocks"]


# ===================================================================
# Prompt Enhancement
# ===================================================================


class TestPromptEnhancement:
    def test_targeted_enhancement(self):
        enhanced = enhance_prompt_with_revision(
            "Original prompt text", "warmer amber tones", [4]
        )
        assert "REVISION (Lighting): warmer amber tones." in enhanced

    def test_multi_block_enhancement(self):
        enhanced = enhance_prompt_with_revision(
            "Original", "change color palette", [4, 6]
        )
        assert "REVISION (Lighting, Technical)" in enhanced

    def test_no_blocks_appends_at_end(self):
        enhanced = enhance_prompt_with_revision("Original", "general fix", [])
        assert enhanced == "Original. REVISION: general fix."


# ===================================================================
# Regeneration Request Validation
# ===================================================================


class TestRequestValidation:
    def setup_method(self):
        self.fp_map = _make_12_beat_map()

    def test_valid_request(self):
        req = {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "warmer lighting"}
        valid, err = validate_regeneration_request(req, self.fp_map)
        assert valid

    def test_invalid_mode(self):
        req = {"beat_index": 3, "mode": "INVALID", "revision_note": "test"}
        valid, err = validate_regeneration_request(req, self.fp_map)
        assert not valid
        assert "invalid mode" in err

    def test_missing_beat_index(self):
        req = {"mode": "T2I_ONLY", "revision_note": "test"}
        valid, err = validate_regeneration_request(req, self.fp_map)
        assert not valid

    def test_invalid_beat_index(self):
        """§10 Safety Test: beat index 99 in a 12-beat video → error."""
        req = {"beat_index": 99, "mode": "T2I_ONLY", "revision_note": "test"}
        valid, err = validate_regeneration_request(req, self.fp_map)
        assert not valid
        assert "INVALID_BEAT_INDEX" in err

    def test_empty_revision_note(self):
        req = {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": ""}
        valid, err = validate_regeneration_request(req, self.fp_map)
        assert not valid


# ===================================================================
# T2I_ONLY Regeneration — AC2
# ===================================================================


class TestT2IOnlyRegeneration:
    def test_ac2_cascade_i2v_mandatory(self):
        """AC2: T2I_ONLY → cascade_i2v: true, FR-VID-03 in pipeline."""
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][3]
        plan = build_regeneration_plan(
            {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "warmer lighting"},
            fp_map, entry,
        )
        assert plan["cascade_i2v"] is True
        assert "FR-VID-03" in plan["pipeline_calls"]
        assert "FR-VID-02" in plan["pipeline_calls"]
        assert "FR-VID-04" in plan["pipeline_calls"]

    def test_ac2_enhanced_prompt_present(self):
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][3]
        plan = build_regeneration_plan(
            {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "warmer lighting"},
            fp_map, entry,
        )
        assert plan["enhanced_prompt"] is not None
        assert "REVISION" in plan["enhanced_prompt"]

    def test_ac2_history_logged_on_execute(self):
        """AC2: Old fingerprint logged in history after execution."""
        fp_map = _make_12_beat_map()
        req = {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "warmer lighting"}
        with tempfile.TemporaryDirectory() as tmpdir:
            plan, updated_entry, receipt = execute_regeneration(
                req, fp_map, date_str="20260321", receipt_output_dir=tmpdir,
            )
        assert len(updated_entry["regeneration_history"]) == 1
        assert updated_entry["regeneration_history"][0]["mode"] == "T2I_ONLY"


# ===================================================================
# I2V_ONLY Regeneration — AC3
# ===================================================================


class TestI2VOnlyRegeneration:
    def test_ac3_reuses_keyframe(self):
        """AC3: I2V_ONLY → same keyframe reused."""
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][5]
        plan = build_regeneration_plan(
            {"beat_index": 5, "mode": "I2V_ONLY", "revision_note": "slower camera motion"},
            fp_map, entry,
        )
        assert plan["reuse_keyframe"] is True
        assert plan["reuse_keyframe_url"].endswith("b5.png")

    def test_ac3_only_calls_fr_vid_03(self):
        """AC3: I2V_ONLY → only FR-VID-03 called."""
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][5]
        plan = build_regeneration_plan(
            {"beat_index": 5, "mode": "I2V_ONLY", "revision_note": "slower movement"},
            fp_map, entry,
        )
        assert plan["pipeline_calls"] == ["FR-VID-03"]
        assert plan["cascade_i2v"] is False

    def test_ac3_stage1_unchanged(self):
        """AC3: I2V_ONLY → no enhanced prompt (stage_1_t2i unchanged)."""
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][5]
        plan = build_regeneration_plan(
            {"beat_index": 5, "mode": "I2V_ONLY", "revision_note": "slower movement"},
            fp_map, entry,
        )
        assert plan["enhanced_prompt"] is None


# ===================================================================
# Seed Preservation — AC4
# ===================================================================


class TestSeedPreservation:
    def test_ac4_non_target_beats_locked(self):
        """AC4: Regenerate beat 3 → beats 0-2, 4-11 have seed locks."""
        fp_map = _make_12_beat_map()
        locks = compute_seed_locks(fp_map, {3})
        assert len(locks) == 11
        assert 3 not in locks
        for i in range(12):
            if i != 3:
                assert i in locks
                assert locks[i]["t2i_seed"] == 1000 + i
                assert locks[i]["i2v_seed"] == 2000 + i

    def test_multi_beat_target_union(self):
        """§3 TD5: Multi-beat targets are the union — both excluded from locks."""
        fp_map = _make_12_beat_map()
        locks = compute_seed_locks(fp_map, {3, 7})
        assert len(locks) == 10
        assert 3 not in locks
        assert 7 not in locks


# ===================================================================
# History Integrity — AC5
# ===================================================================


class TestHistoryIntegrity:
    def test_ac5_five_regenerations_chronological(self):
        """§10 Unit Test: Regenerate 5 times → history length 5, chronological."""
        fp_map = _make_12_beat_map()
        for i in range(5):
            req = {"beat_index": 0, "mode": "T2I_ONLY", "revision_note": f"change {i+1}"}
            with tempfile.TemporaryDirectory() as tmpdir:
                execute_regeneration(req, fp_map, date_str="20260321", receipt_output_dir=tmpdir)

        entry = fp_map["fingerprints"][0]
        assert len(entry["regeneration_history"]) == 5
        for i, hist in enumerate(entry["regeneration_history"]):
            assert hist["reason"] == f"change {i+1}"

    def test_history_not_overwritten(self):
        fp_map = _make_12_beat_map()
        req1 = {"beat_index": 0, "mode": "T2I_ONLY", "revision_note": "warmer lighting"}
        req2 = {"beat_index": 0, "mode": "I2V_ONLY", "revision_note": "slower movement"}
        with tempfile.TemporaryDirectory() as tmpdir:
            execute_regeneration(req1, fp_map, date_str="20260321", receipt_output_dir=tmpdir)
            execute_regeneration(req2, fp_map, date_str="20260321", receipt_output_dir=tmpdir)
        entry = fp_map["fingerprints"][0]
        assert len(entry["regeneration_history"]) == 2
        assert entry["regeneration_history"][0]["mode"] == "T2I_ONLY"
        assert entry["regeneration_history"][1]["mode"] == "I2V_ONLY"


# ===================================================================
# Regeneration Limit — §10 Safety Test
# ===================================================================


class TestRegenerationLimit:
    def test_limit_exceeded(self):
        """§10: 100 regenerations → limit enforced at 10."""
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][0]
        # Manually add 10 history entries
        for i in range(10):
            entry["regeneration_history"].append({
                "superseded_fingerprint_id": f"fp-{i}",
                "superseded_at": "2026-03-21T00:00:00Z",
                "reason": f"test {i}",
                "mode": "T2I_ONLY",
                "new_fingerprint_id": f"fp-{i+1}",
            })
        within, msg = check_regeneration_limit(entry)
        assert not within
        assert "REGENERATION_LIMIT_EXCEEDED" in msg

    def test_within_limit(self):
        fp_map = _make_12_beat_map()
        entry = fp_map["fingerprints"][0]
        within, msg = check_regeneration_limit(entry)
        assert within


# ===================================================================
# Multi-Beat Merge
# ===================================================================


class TestMultiBeatMerge:
    def test_merge_requests(self):
        requests = [
            {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "a"},
            {"beat_index": 7, "mode": "I2V_ONLY", "revision_note": "b"},
        ]
        target_set = merge_regeneration_requests(requests)
        assert target_set == {3, 7}


# ===================================================================
# Gate H Violations
# ===================================================================


class TestGateHCascadeCompleteness:
    def test_q1_violation_no_cascade(self):
        plan = {"cascade_i2v": False, "pipeline_calls": ["FR-VID-02"]}
        passed, diag = check_cascade_completeness("T2I_ONLY", plan)
        assert not passed
        assert "I2V_CASCADE_MISSING" in diag

    def test_q1_violation_missing_fr_vid_03(self):
        plan = {"cascade_i2v": True, "pipeline_calls": ["FR-VID-02", "FR-VID-04"]}
        passed, diag = check_cascade_completeness("T2I_ONLY", plan)
        assert not passed

    def test_q1_passes_correct_cascade(self):
        plan = {"cascade_i2v": True, "pipeline_calls": ["FR-VID-02", "FR-VID-04", "FR-VID-03"]}
        passed, _ = check_cascade_completeness("T2I_ONLY", plan)
        assert passed

    def test_q1_passes_i2v_only_mode(self):
        """I2V_ONLY doesn't need cascade check."""
        plan = {"cascade_i2v": False, "pipeline_calls": ["FR-VID-03"]}
        passed, _ = check_cascade_completeness("I2V_ONLY", plan)
        assert passed


class TestGateHSeedPreservation:
    def test_q2_violation_missing_locks(self):
        passed, diag = check_seed_preservation({3}, {0: {}, 1: {}, 2: {}}, 12)
        assert not passed
        assert "SEED_PRESERVATION_FAILED" in diag

    def test_q2_violation_target_in_locks(self):
        locks = {i: {} for i in range(12)}  # Target 3 is also locked
        passed, diag = check_seed_preservation({3}, locks, 12)
        assert not passed
        assert "SEED_LOCK_CONFLICT" in diag

    def test_q2_passes(self):
        locks = {i: {} for i in range(12) if i != 3}
        passed, _ = check_seed_preservation({3}, locks, 12)
        assert passed


class TestGateHRevisionSpecificity:
    def test_q3_violation_vague(self):
        passed, diag = check_revision_note_specificity("make it better")
        assert not passed
        assert "REVISION_NOTE_VAGUE" in diag

    def test_q3_violation_empty(self):
        passed, diag = check_revision_note_specificity("")
        assert not passed
        assert "REVISION_NOTE_EMPTY" in diag

    def test_q3_passes_specific(self):
        passed, _ = check_revision_note_specificity("warmer lighting")
        assert passed


class TestGateHBudgetImpact:
    def test_q4_violation_budget_exceeded(self):
        entry = {"beat_index": 0, "regeneration_history": []}
        passed, diag = check_budget_impact(
            entry, regen_cost_estimate=3.0, per_video_budget=5.0, total_spent=4.0
        )
        assert not passed
        assert "BUDGET_EXCEEDED" in diag

    def test_q4_violation_excessive_regens(self):
        entry = {"beat_index": 0, "regeneration_history": [{}, {}, {}]}
        passed, diag = check_budget_impact(entry, regen_warn_threshold=3)
        assert not passed
        assert "REGENERATION_EXCESSIVE" in diag

    def test_q4_passes(self):
        entry = {"beat_index": 0, "regeneration_history": []}
        passed, _ = check_budget_impact(entry)
        assert passed


class TestGateHHistoryIntegrity:
    def test_q5_violation_no_history_step(self):
        entry = {"beat_index": 0, "regeneration_history": []}
        passed, diag = check_history_integrity(entry, plan_has_history_step=False)
        assert not passed
        assert "HISTORY_LOGGING_MISSING" in diag

    def test_q5_passes(self):
        entry = {"beat_index": 0, "regeneration_history": []}
        passed, _ = check_history_integrity(entry, plan_has_history_step=True)
        assert passed


# ===================================================================
# Gate H Full Runner
# ===================================================================


class TestGateHRunner:
    def test_all_pass(self):
        entry = {"beat_index": 0, "regeneration_history": []}
        plan = {"cascade_i2v": True, "pipeline_calls": ["FR-VID-02", "FR-VID-04", "FR-VID-03"]}
        locks = {i: {} for i in range(1, 12)}
        result = run_gate_h(
            mode="T2I_ONLY", plan=plan,
            target_beat_indices={0}, seed_locks=locks, total_beats=12,
            revision_note="warmer lighting", fingerprint_entry=entry,
        )
        assert result["passed"] is True
        assert result["gate"] == "H"
        assert all(r["passed"] for r in result["results"])

    def test_multiple_failures(self):
        entry = {"beat_index": 0, "regeneration_history": [{}, {}, {}]}
        plan = {"cascade_i2v": False, "pipeline_calls": ["FR-VID-02"]}
        result = run_gate_h(
            mode="T2I_ONLY", plan=plan,
            target_beat_indices={0}, seed_locks={}, total_beats=12,
            revision_note="make it better", fingerprint_entry=entry,
            plan_has_history_step=False,
        )
        assert result["passed"] is False
        failed_qs = [r["question"] for r in result["results"] if not r["passed"]]
        assert 1 in failed_qs  # Cascade
        assert 2 in failed_qs  # Seed preservation
        assert 3 in failed_qs  # Revision note
        assert 4 in failed_qs  # Budget (3 regens → excessive)
        assert 5 in failed_qs  # History


# ===================================================================
# Execute Regeneration — Receipt
# ===================================================================


class TestExecuteRegeneration:
    def test_produces_plan_and_receipt(self):
        fp_map = _make_12_beat_map()
        req = {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "brighter lighting"}
        with tempfile.TemporaryDirectory() as tmpdir:
            plan, entry, receipt = execute_regeneration(
                req, fp_map, date_str="20260321", receipt_output_dir=tmpdir,
            )
        assert plan["mode"] == "T2I_ONLY"
        assert "regeneration_decisions" in plan
        assert "patch_selection" in plan
        assert "commander_dispatch" in plan
        assert receipt["stage_name"] == "REGENERATION_EXECUTE"
        assert receipt["agent_name"] == "regeneration_handler"

    def test_produces_constraint_manifest_and_chained_receipt(self):
        fp_map = _make_12_beat_map()
        req = {"beat_index": 3, "mode": "T2I_ONLY", "revision_note": "brighter lighting"}
        with tempfile.TemporaryDirectory() as tmpdir:
            plan, entry, receipt = execute_regeneration(
                req, fp_map, date_str="20260321", receipt_output_dir=tmpdir,
            )

            assert "constraint_manifest" in plan
            assert plan["regeneration_decisions"]["shot_duration"]["subsystem_id"] == "CS-015"
            assert plan["regeneration_decisions"]["rhythm_generator"]["subsystem_id"] == "CS-023"
            assert plan["regeneration_decisions"]["prediction_error_gate"]["subsystem_id"] == "CS-033"
            assert plan["patch_selection"]["target_beat_index"] == 3
            assert receipt["previous_receipt_hash"] != "GENESIS"
            assert Path(plan["constraint_manifest"]["path"]).exists()

    def test_patch_selection_moves_to_timing_rebalance_when_rules_fail(self):
        fp_map = _make_12_beat_map()
        req = {
            "beat_index": 3,
            "mode": "I2V_ONLY",
            "revision_note": "tighten pacing and extend the moment",
            "current_shot_duration_sec": 0.5,
            "local_shot_duration_vector": [3.8, 0.5, 3.7],
            "arc_stage": "CHALLENGE",
        }
        plan = build_regeneration_plan(req, fp_map, fp_map["fingerprints"][3])
        assert plan["regeneration_decisions"]["shot_duration"]["verdict"] == "REVISE"
        assert plan["regeneration_decisions"]["rhythm_generator"]["verdict"] == "REVISE"
        assert plan["patch_selection"]["patch_profile"] == "TIMING_REBALANCE_PATCH"
        assert plan["commander_dispatch"]["patch_profile"] == "TIMING_REBALANCE_PATCH"
        assert plan["commander_dispatch"]["module_dispatch"]["FR-VID-03"]["operation"] == "retime_neighbors"
        assert "retime_neighbor_window" in plan["patch_selection"]["corrective_moves"]
        assert "/beats/3/duration_sec" in plan["patch_selection"]["targeted_fields"]
        assert "/beats/3/transition" in plan["patch_selection"]["targeted_fields"]

    def test_prediction_error_gate_restores_surprise_when_revision_note_smooths_beat(self):
        fp_map = _make_12_beat_map()
        req = {
            "beat_index": 1,
            "mode": "I2V_ONLY",
            "revision_note": "make it cleaner and smoother",
            "arc_stage": "HOOK",
            "current_prediction_error_score": 0.5,
        }
        plan = build_regeneration_plan(req, fp_map, fp_map["fingerprints"][1])

        assert plan["regeneration_decisions"]["prediction_error_gate"]["verdict"] == "REVISE"
        assert plan["patch_selection"]["surprise_patch_required"] is True
        assert plan["patch_selection"]["surprise_adjustment"] == "restore_surprise"
        assert "escalate_schema_break" in plan["patch_selection"]["corrective_moves"]
        assert "/beats/1/transition" in plan["patch_selection"]["targeted_fields"]

    def test_legitimacy_blocks_off_target_patch(self):
        fp_map = _make_12_beat_map()
        req = {
            "beat_index": 3,
            "mode": "T2I_ONLY",
            "revision_note": "brighter lighting",
            "changed_paths": [
                "/beats/3/video_clip_url",
                "/beats/4/video_clip_url",
            ],
        }
        import pytest
        with pytest.raises(ValueError, match="EDITOR_REGEN_LEGITIMACY_BLOCKED"):
            with tempfile.TemporaryDirectory() as tmpdir:
                execute_regeneration(req, fp_map, date_str="20260321", receipt_output_dir=tmpdir)

    def test_invalid_request_raises(self):
        fp_map = _make_12_beat_map()
        req = {"beat_index": 99, "mode": "T2I_ONLY", "revision_note": "test"}
        import pytest
        with pytest.raises(ValueError, match="INVALID_BEAT_INDEX"):
            with tempfile.TemporaryDirectory() as tmpdir:
                execute_regeneration(req, fp_map, receipt_output_dir=tmpdir)
