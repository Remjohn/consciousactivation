"""
Tests for gates/gate_l.py — FR-VID-09 Gate L Pre-Pipeline Constraint Network.

6 questions × pass + fail scenarios = comprehensive gate coverage.
Q6 (resume detection) is informational — never blocks.
"""

import pytest

from gates.gate_l import (
    MIN_DISK_SPACE_GB,
    REQUIRED_MODULES,
    check_concurrent_budget,
    check_disk_space,
    check_module_health,
    check_resume_detection,
    check_runninghub_availability,
    check_upstream_assets,
    run_gate_l,
)


# ---------------------------------------------------------------------------
# TestGateLQ1UpstreamAssets
# ---------------------------------------------------------------------------


class TestGateLQ1UpstreamAssets:
    """Q1: Beat cluster + voiceover + music all present."""

    def test_all_present_passes(self):
        passed, detail = check_upstream_assets(
            {"beats": [1, 2]}, "/audio/vo.mp3", "/audio/music.mp3"
        )
        assert passed is True
        assert detail == "OK"

    def test_missing_beat_cluster(self):
        passed, detail = check_upstream_assets(None, "/vo.mp3", "/music.mp3")
        assert passed is False
        assert "beat_cluster_json" in detail

    def test_missing_voiceover(self):
        passed, detail = check_upstream_assets({"beats": []}, None, "/music.mp3")
        assert passed is False
        assert "voiceover_path" in detail

    def test_missing_music(self):
        passed, detail = check_upstream_assets({"beats": []}, "/vo.mp3", "")
        assert passed is False
        assert "music_path" in detail

    def test_all_missing(self):
        passed, detail = check_upstream_assets(None, None, None)
        assert passed is False
        assert "beat_cluster_json" in detail
        assert "voiceover_path" in detail
        assert "music_path" in detail


# ---------------------------------------------------------------------------
# TestGateLQ2RunningHubAvailability
# ---------------------------------------------------------------------------


class TestGateLQ2RunningHubAvailability:
    """Q2: Both RunningHub endpoints reachable."""

    def test_both_reachable(self):
        passed, detail = check_runninghub_availability(True, True)
        assert passed is True

    def test_t2i_unreachable(self):
        passed, detail = check_runninghub_availability(False, True)
        assert passed is False
        assert "T2I_proxy" in detail

    def test_i2v_unreachable(self):
        passed, detail = check_runninghub_availability(True, False)
        assert passed is False
        assert "I2V_proxy_plus" in detail

    def test_both_unreachable(self):
        passed, detail = check_runninghub_availability(False, False)
        assert passed is False
        assert "T2I_proxy" in detail
        assert "I2V_proxy_plus" in detail


# ---------------------------------------------------------------------------
# TestGateLQ3ConcurrentBudget
# ---------------------------------------------------------------------------


class TestGateLQ3ConcurrentBudget:
    """Q3: Within concurrent processing limit."""

    def test_within_limit(self):
        passed, detail = check_concurrent_budget(2, concurrent_limit=3)
        assert passed is True

    def test_at_limit(self):
        passed, detail = check_concurrent_budget(3, concurrent_limit=3)
        assert passed is False
        assert "CONCURRENT_LIMIT_REACHED" in detail

    def test_over_limit(self):
        passed, detail = check_concurrent_budget(5, concurrent_limit=3)
        assert passed is False

    def test_zero_processing(self):
        passed, detail = check_concurrent_budget(0)
        assert passed is True


# ---------------------------------------------------------------------------
# TestGateLQ4DiskSpace
# ---------------------------------------------------------------------------


class TestGateLQ4DiskSpace:
    """Q4: ≥10GB free disk space."""

    def test_sufficient_space(self):
        passed, detail = check_disk_space(50.0)
        assert passed is True

    def test_exactly_at_minimum(self):
        passed, detail = check_disk_space(10.0)
        assert passed is True

    def test_insufficient_space(self):
        passed, detail = check_disk_space(5.0)
        assert passed is False
        assert "INSUFFICIENT_DISK" in detail

    def test_minimum_constant(self):
        assert MIN_DISK_SPACE_GB == 10


# ---------------------------------------------------------------------------
# TestGateLQ5ModuleHealth
# ---------------------------------------------------------------------------


class TestGateLQ5ModuleHealth:
    """Q5: All 8 downstream modules healthy."""

    def test_all_healthy(self):
        status = {mod: True for mod in REQUIRED_MODULES}
        passed, detail = check_module_health(status)
        assert passed is True

    def test_one_unhealthy(self):
        status = {mod: True for mod in REQUIRED_MODULES}
        status["audio_engine"] = False
        passed, detail = check_module_health(status)
        assert passed is False
        assert "audio_engine" in detail

    def test_multiple_unhealthy(self):
        status = {mod: True for mod in REQUIRED_MODULES}
        status["audio_engine"] = False
        status["render_orchestrator"] = False
        passed, detail = check_module_health(status)
        assert passed is False
        assert "audio_engine" in detail
        assert "render_orchestrator" in detail

    def test_missing_module_in_status_fails(self):
        """If a module isn't reported at all, it's considered unhealthy."""
        status = {"beat_cluster_parser": True}  # Only 1 of 9
        passed, detail = check_module_health(status)
        assert passed is False

    def test_required_modules_count(self):
        assert len(REQUIRED_MODULES) == 9


# ---------------------------------------------------------------------------
# TestGateLQ6ResumeDetection
# ---------------------------------------------------------------------------


class TestGateLQ6ResumeDetection:
    """Q6: Resume detection — informational, never blocks."""

    def test_no_checkpoint(self):
        passed, detail = check_resume_detection(None)
        assert passed is True
        assert detail == "NO_CHECKPOINT"

    def test_checkpoint_found(self):
        passed, detail = check_resume_detection("/checkpoints/pipe-001.json")
        assert passed is True
        assert "CHECKPOINT_FOUND" in detail
        assert "pipe-001.json" in detail


# ---------------------------------------------------------------------------
# TestGateLRunner
# ---------------------------------------------------------------------------


class TestGateLRunner:
    """Full Gate L runner — all 6 questions."""

    def test_all_pass(self):
        result = run_gate_l(
            beat_cluster_json={"beats": [1, 2, 3]},
            voiceover_path="/audio/vo.mp3",
            music_path="/audio/music.mp3",
            t2i_reachable=True,
            i2v_reachable=True,
            current_processing=0,
            free_space_gb=50.0,
        )
        assert result["gate"] == "L"
        assert result["passed"] is True
        assert len(result["results"]) == 6

    def test_single_failure(self):
        result = run_gate_l(
            beat_cluster_json=None,
            voiceover_path="/vo.mp3",
            music_path="/music.mp3",
        )
        assert result["passed"] is False
        q1 = result["results"][0]
        assert q1["question"] == 1
        assert q1["passed"] is False

    def test_multiple_failures(self):
        result = run_gate_l(
            beat_cluster_json=None,
            voiceover_path=None,
            music_path=None,
            t2i_reachable=False,
            i2v_reachable=False,
            current_processing=10,
            free_space_gb=2.0,
            module_status={"audio_engine": False},
        )
        assert result["passed"] is False
        failed_qs = [r["question"] for r in result["results"] if not r["passed"]]
        assert 1 in failed_qs  # Assets
        assert 2 in failed_qs  # RunningHub
        assert 3 in failed_qs  # Concurrent
        assert 4 in failed_qs  # Disk
        assert 5 in failed_qs  # Modules
        # Q6 never fails
        assert 6 not in failed_qs

    def test_q6_never_blocks(self):
        """Q6 is informational — gate passes even with checkpoint found."""
        result = run_gate_l(
            beat_cluster_json={"beats": [1]},
            voiceover_path="/vo.mp3",
            music_path="/music.mp3",
            checkpoint_path="/checkpoints/old.json",
        )
        assert result["passed"] is True
        q6 = result["results"][5]
        assert q6["passed"] is True
        assert "CHECKPOINT_FOUND" in q6["detail"]

    def test_result_structure(self):
        result = run_gate_l(
            beat_cluster_json={"beats": []},
            voiceover_path="/vo.mp3",
            music_path="/music.mp3",
        )
        assert "gate" in result
        assert "passed" in result
        assert "results" in result
        for r in result["results"]:
            assert "question" in r
            assert "name" in r
            assert "passed" in r
            assert "detail" in r
