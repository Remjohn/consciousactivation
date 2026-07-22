"""
Fingerprint Tracker Test Suite — FR-VID-05

Tests fingerprint ID generation, T2I/I2V metadata population,
dual-stage lifecycle, seed extraction, and receipt chain.

Maps to FR-VID-05 §8 AC1 (Fingerprint Creation), §10 Testing Strategy.
"""

import re
import tempfile

from fingerprint_tracker import (
    generate_fingerprint_id,
    validate_fingerprint_id,
    create_fingerprint_from_t2i,
    update_fingerprint_with_i2v,
    create_beat_fingerprint_map,
    supersede_fingerprint,
    extract_seeds,
    run_fingerprint_creation,
    FINGERPRINT_ID_REGEX,
    MAX_REGENERATION_PER_BEAT,
)


# ===================================================================
# Helpers
# ===================================================================


def _make_t2i_result(seed=42891, beat=0):
    return {
        "workflow_id": "RH-WF-CMF-T2I-FLUX-001",
        "prompt_used": "Close-up of hands gripping a weathered leather journal...",
        "negative_prompt": "blurry, generic, stock photo",
        "seed": seed,
        "model": "flux-dev-fp8",
        "pssl_params": {"foundation_hue": "#2C3E50", "temperature": "warm"},
        "output_image_url": f"https://r2.cmf-assets.com/t2i/fp-001-b{beat:02d}.png",
        "quality_score": 0.79,
        "generation_timestamp": "2026-03-21T02:15:00Z",
    }


def _make_i2v_result(beat=0, seed=77204):
    return {
        "workflow_id": "RH-WF-CMF-I2V-SVD-001",
        "input_keyframe_url": f"https://r2.cmf-assets.com/t2i/fp-001-b{beat:02d}.png",
        "motion_parameters_applied": {
            "motion_bucket_id": 127,
            "fps": 24,
            "duration_frames": 96,
            "motion_strength": 0.6,
            "camera_motion": "slow_zoom_in",
        },
        "output_video_url": f"https://r2.cmf-assets.com/i2v/fp-001-b{beat:02d}.mp4",
        "seed_used": seed,
        "vram_tier_used": "48GB",
        "generation_timestamp": "2026-03-21T02:16:30Z",
    }


# ===================================================================
# Fingerprint ID Format — §10 Unit Test
# ===================================================================


class TestFingerprintIdFormat:
    def test_basic_format(self):
        fp_id = generate_fingerprint_id("20260321", 1, 0)
        assert fp_id == "FP-VID-20260321-001-B00"

    def test_regex_match(self):
        fp_id = generate_fingerprint_id("20260321", 1, 0)
        assert validate_fingerprint_id(fp_id)

    def test_batch_padding(self):
        fp_id = generate_fingerprint_id("20260321", 42, 7)
        assert fp_id == "FP-VID-20260321-042-B07"
        assert validate_fingerprint_id(fp_id)

    def test_max_values(self):
        fp_id = generate_fingerprint_id("20260321", 999, 99)
        assert fp_id == "FP-VID-20260321-999-B99"
        assert validate_fingerprint_id(fp_id)

    def test_100_ids_no_collision(self):
        """§10 Unit Test: Generate 100 fingerprint IDs, assert no collision."""
        ids = set()
        for batch in range(1, 11):
            for beat in range(10):
                fp_id = generate_fingerprint_id("20260321", batch, beat)
                assert validate_fingerprint_id(fp_id), f"{fp_id} failed regex"
                assert fp_id not in ids, f"Collision: {fp_id}"
                ids.add(fp_id)
        assert len(ids) == 100

    def test_invalid_format_rejected(self):
        assert not validate_fingerprint_id("FP-VID-2026-001-B00")
        assert not validate_fingerprint_id("FP-20260321-001-B00")
        assert not validate_fingerprint_id("random-string")
        assert not validate_fingerprint_id("")


# ===================================================================
# Fingerprint Creation — AC1
# ===================================================================


class TestFingerprintCreation:
    def test_ac1_dual_stage_fingerprint(self):
        """AC1: Fingerprint contains both stage_1_t2i and stage_2_i2v."""
        t2i = _make_t2i_result()
        i2v = _make_i2v_result()

        entry = create_fingerprint_from_t2i(0, t2i, "20260321", 1)
        entry = update_fingerprint_with_i2v(entry, i2v)

        fp = entry["fingerprint"]
        assert fp["fingerprint_id"] == "FP-VID-20260321-001-B00"
        assert validate_fingerprint_id(fp["fingerprint_id"])

        # stage_1_t2i has all fields
        s1 = fp["stage_1_t2i"]
        assert s1["status"] == "GENERATED"
        assert s1["runninghub_workflow_id"] == "RH-WF-CMF-T2I-FLUX-001"
        assert s1["seed"] == 42891
        assert s1["output_image_url"].endswith("b00.png")
        assert s1["quality_score"] == 0.79

        # stage_2_i2v has all fields
        s2 = fp["stage_2_i2v"]
        assert s2["status"] == "GENERATED"
        assert s2["seed_used"] == 77204
        assert s2["output_video_url"].endswith("b00.mp4")
        assert s2["motion_parameters"]["camera_motion"] == "slow_zoom_in"

    def test_t2i_only_sets_i2v_pending(self):
        """After T2I only, stage_2_i2v is PENDING."""
        entry = create_fingerprint_from_t2i(0, _make_t2i_result(), "20260321", 1)
        assert entry["fingerprint"]["stage_2_i2v"]["status"] == "PENDING"

    def test_empty_regeneration_history(self):
        entry = create_fingerprint_from_t2i(0, _make_t2i_result(), "20260321", 1)
        assert entry["regeneration_history"] == []

    def test_active_fingerprint_id_set(self):
        entry = create_fingerprint_from_t2i(3, _make_t2i_result(beat=3), "20260321", 1)
        assert entry["active_fingerprint_id"] == "FP-VID-20260321-001-B03"

    def test_auto_date_when_none(self):
        entry = create_fingerprint_from_t2i(0, _make_t2i_result())
        assert validate_fingerprint_id(entry["fingerprint"]["fingerprint_id"])


# ===================================================================
# Beat Fingerprint Map — DEP-VID-014
# ===================================================================


class TestBeatFingerprintMap:
    def test_map_structure(self):
        entries = [
            create_fingerprint_from_t2i(i, _make_t2i_result(beat=i), "20260321", 1)
            for i in range(3)
        ]
        fp_map = create_beat_fingerprint_map(
            "CMF-VID-20260321-001", "03_50-12", "BC-WITNESS-42", entries
        )
        assert fp_map["video_id"] == "CMF-VID-20260321-001"
        assert fp_map["summary"]["total_beats"] == 3
        assert fp_map["summary"]["total_regenerations"] == 0
        assert fp_map["summary"]["beats_with_regeneration"] == 0

    def test_map_counts_regenerations(self):
        entry = create_fingerprint_from_t2i(0, _make_t2i_result(), "20260321", 1)
        supersede_fingerprint(entry, "FP-VID-20260321-001-B00", "T2I_ONLY", "reason")
        fp_map = create_beat_fingerprint_map(
            "CMF-VID-20260321-001", "03_50-12", "BC-WITNESS-42", [entry]
        )
        assert fp_map["summary"]["total_regenerations"] == 1
        assert fp_map["summary"]["beats_with_regeneration"] == 1


# ===================================================================
# Supersession & History — AC5
# ===================================================================


class TestSupersession:
    def test_ac5_three_regenerations_chronological(self):
        """AC5: Regenerate 3 times → history has 3 chronological entries."""
        entry = create_fingerprint_from_t2i(3, _make_t2i_result(beat=3), "20260321", 1)

        for i in range(3):
            new_id = f"FP-VID-20260321-00{i+2}-B03"
            supersede_fingerprint(entry, new_id, "T2I_ONLY", f"revision {i+1}")

        assert len(entry["regeneration_history"]) == 3
        for i, hist in enumerate(entry["regeneration_history"]):
            assert hist["mode"] == "T2I_ONLY"
            assert hist["reason"] == f"revision {i+1}"
            assert "superseded_at" in hist

    def test_history_preserves_old_ids(self):
        entry = create_fingerprint_from_t2i(0, _make_t2i_result(), "20260321", 1)
        old_id = entry["fingerprint"]["fingerprint_id"]
        supersede_fingerprint(entry, "FP-VID-20260321-002-B00", "BOTH", "test")
        assert entry["regeneration_history"][0]["superseded_fingerprint_id"] == old_id


# ===================================================================
# Seed Extraction
# ===================================================================


class TestSeedExtraction:
    def test_extract_seeds(self):
        entries = []
        for i in range(3):
            e = create_fingerprint_from_t2i(
                i, _make_t2i_result(seed=1000 + i, beat=i), "20260321", 1
            )
            e = update_fingerprint_with_i2v(e, _make_i2v_result(beat=i, seed=2000 + i))
            entries.append(e)

        fp_map = create_beat_fingerprint_map(
            "CMF-VID-20260321-001", "proj", "bc", entries
        )
        seeds = extract_seeds(fp_map)
        assert seeds[0] == {"t2i_seed": 1000, "i2v_seed": 2000}
        assert seeds[1] == {"t2i_seed": 1001, "i2v_seed": 2001}
        assert seeds[2] == {"t2i_seed": 1002, "i2v_seed": 2002}


# ===================================================================
# Pipeline with Receipt
# ===================================================================


class TestFingerprintCreationPipeline:
    def test_creates_fingerprint_and_receipt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            entry, receipt = run_fingerprint_creation(
                beat_index=0,
                t2i_result=_make_t2i_result(),
                date_str="20260321",
                batch_number=1,
                receipt_output_dir=tmpdir,
            )
            assert entry["fingerprint"]["stage_1_t2i"]["status"] == "GENERATED"
            assert entry["fingerprint"]["stage_2_i2v"]["status"] == "PENDING"
            assert receipt["stage_name"] == "FINGERPRINT_CREATE"
            assert receipt["agent_name"] == "fingerprint_tracker"

    def test_with_i2v_result_sets_complete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            entry, receipt = run_fingerprint_creation(
                beat_index=0,
                t2i_result=_make_t2i_result(),
                i2v_result=_make_i2v_result(),
                date_str="20260321",
                receipt_output_dir=tmpdir,
            )
            assert entry["fingerprint"]["stage_2_i2v"]["status"] == "GENERATED"

    def test_receipt_chains(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            _, r1 = run_fingerprint_creation(
                beat_index=0, t2i_result=_make_t2i_result(),
                receipt_output_dir=tmpdir,
            )
            _, r2 = run_fingerprint_creation(
                beat_index=1, t2i_result=_make_t2i_result(beat=1),
                previous_receipt=r1, receipt_output_dir=tmpdir,
            )
            assert r2["previous_receipt_hash"] != "GENESIS"
