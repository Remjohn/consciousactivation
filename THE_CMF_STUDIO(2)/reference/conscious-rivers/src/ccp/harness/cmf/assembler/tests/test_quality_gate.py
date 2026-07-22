"""
T2I Quality Gate Test Suite — FR-VID-04

Tests composite scoring, verdict logic, feedback generation, retry enforcement,
and operator override — all testable without CLIP model or real images.

Maps to FR-VID-04 §8 Acceptance Criteria AC1-AC5 and §10 Testing Strategy.
"""

import tempfile
from unittest.mock import patch

from t2i_quality_gate import (
    compute_composite_score,
    determine_verdict,
    generate_feedback,
    emit_verdicts,
    score_keyframes,
    run_quality_gate,
    DEFAULT_GATE_CONFIG,
)


# ===================================================================
# Composite Score Calculation — §10 Unit Test
# ===================================================================


class TestCompositeScore:
    def test_default_weights_exact_computation(self):
        """§10 Unit Test: composite equals exact weighted sum."""
        scores = {
            "prompt_adherence": 0.80,
            "composition_quality": 0.70,
            "pssl_coherence": 0.60,
            "artifact_detection": 0.90,
        }
        weights = DEFAULT_GATE_CONFIG["weights"]
        result = compute_composite_score(scores, weights)
        expected = 0.40 * 0.80 + 0.20 * 0.70 + 0.25 * 0.60 + 0.15 * 0.90
        assert result == round(expected, 4)

    def test_all_perfect_scores(self):
        scores = {
            "prompt_adherence": 1.0,
            "composition_quality": 1.0,
            "pssl_coherence": 1.0,
            "artifact_detection": 1.0,
        }
        weights = DEFAULT_GATE_CONFIG["weights"]
        result = compute_composite_score(scores, weights)
        assert result == 1.0

    def test_all_zero_scores(self):
        scores = {
            "prompt_adherence": 0.0,
            "composition_quality": 0.0,
            "pssl_coherence": 0.0,
            "artifact_detection": 0.0,
        }
        weights = DEFAULT_GATE_CONFIG["weights"]
        result = compute_composite_score(scores, weights)
        assert result == 0.0

    def test_custom_weights(self):
        scores = {
            "prompt_adherence": 0.50,
            "composition_quality": 0.50,
            "pssl_coherence": 0.0,
            "artifact_detection": 0.50,
        }
        weights = {
            "prompt_adherence": 0.50,
            "composition_quality": 0.30,
            "pssl_coherence": 0.0,
            "artifact_detection": 0.20,
        }
        result = compute_composite_score(scores, weights)
        expected = 0.50 * 0.50 + 0.30 * 0.50 + 0.0 * 0.0 + 0.20 * 0.50
        assert result == round(expected, 4)

    def test_missing_dimension_treated_as_zero(self):
        scores = {"prompt_adherence": 1.0}
        weights = DEFAULT_GATE_CONFIG["weights"]
        result = compute_composite_score(scores, weights)
        assert result == round(0.40 * 1.0, 4)


# ===================================================================
# Verdict Logic — §10 Unit Test + AC2, AC4, AC5
# ===================================================================


class TestVerdictLogic:
    def test_above_threshold_approved(self):
        """§10: score above threshold → APPROVED."""
        verdict = determine_verdict(0.65, 0.6, retry_count=0, max_retries=2)
        assert verdict == "APPROVED"

    def test_exactly_at_threshold_approved(self):
        verdict = determine_verdict(0.6, 0.6, retry_count=0, max_retries=2)
        assert verdict == "APPROVED"

    def test_below_threshold_retry_available_regenerate(self):
        """§10: below threshold retry 0 → REGENERATE."""
        verdict = determine_verdict(0.58, 0.6, retry_count=0, max_retries=2)
        assert verdict == "REGENERATE"

    def test_below_threshold_retry_1_regenerate(self):
        verdict = determine_verdict(0.55, 0.6, retry_count=1, max_retries=2)
        assert verdict == "REGENERATE"

    def test_below_threshold_retries_exhausted_manual_review(self):
        """§10: below threshold retry 2 → MANUAL_REVIEW."""
        verdict = determine_verdict(0.55, 0.6, retry_count=2, max_retries=2)
        assert verdict == "MANUAL_REVIEW"

    def test_ac2_score_058_threshold_06_regenerate(self):
        """AC2: keyframe scoring 0.58 with threshold 0.6 → REGENERATE."""
        verdict = determine_verdict(0.58, 0.6, retry_count=0, max_retries=2)
        assert verdict == "REGENERATE"

    def test_ac2_score_058_threshold_05_approved(self):
        """AC2: same keyframe with threshold 0.5 → APPROVED."""
        verdict = determine_verdict(0.58, 0.5, retry_count=0, max_retries=2)
        assert verdict == "APPROVED"

    def test_ac4_three_failures_manual_review(self):
        """AC4: 3 failures (retry_count=2, max_retries=2) → MANUAL_REVIEW."""
        verdict = determine_verdict(0.45, 0.6, retry_count=2, max_retries=2)
        assert verdict == "MANUAL_REVIEW"

    def test_ac5_operator_override_approves(self):
        """AC5: operator override → APPROVED despite below-threshold score."""
        verdict = determine_verdict(
            0.30, 0.6, retry_count=2, max_retries=2, operator_override=True
        )
        assert verdict == "APPROVED"

    def test_operator_override_with_good_score(self):
        verdict = determine_verdict(
            0.80, 0.6, retry_count=0, max_retries=2, operator_override=True
        )
        assert verdict == "APPROVED"


# ===================================================================
# Feedback Generation — AC3
# ===================================================================


class TestFeedbackGeneration:
    def test_approved_returns_none(self):
        scores = {
            "prompt_adherence": 0.80,
            "composition_quality": 0.70,
            "pssl_coherence": 0.60,
            "artifact_detection": 0.90,
        }
        feedback = generate_feedback(scores, "APPROVED")
        assert feedback is None

    def test_ac3_pssl_failure_named(self):
        """AC3: feedback names 'PSSL coherence' as failing dimension."""
        scores = {
            "prompt_adherence": 0.70,
            "composition_quality": 0.65,
            "pssl_coherence": 0.25,
            "artifact_detection": 0.80,
        }
        pssl_params = {"foundation_hue": "#2C3E50", "temperature": "cool"}
        feedback = generate_feedback(scores, "REGENERATE", pssl_params)
        assert feedback is not None
        assert "PSSL coherence" in feedback
        assert "#2C3E50" in feedback

    def test_prompt_adherence_failure(self):
        scores = {
            "prompt_adherence": 0.20,
            "composition_quality": 0.65,
            "pssl_coherence": 0.70,
            "artifact_detection": 0.80,
        }
        feedback = generate_feedback(scores, "REGENERATE")
        assert "Prompt adherence" in feedback
        assert "prompt description" in feedback.lower()

    def test_composition_failure(self):
        scores = {
            "prompt_adherence": 0.70,
            "composition_quality": 0.15,
            "pssl_coherence": 0.70,
            "artifact_detection": 0.80,
        }
        feedback = generate_feedback(scores, "REGENERATE")
        assert "Composition quality" in feedback

    def test_artifact_failure(self):
        scores = {
            "prompt_adherence": 0.70,
            "composition_quality": 0.65,
            "pssl_coherence": 0.70,
            "artifact_detection": 0.10,
        }
        feedback = generate_feedback(scores, "REGENERATE")
        assert "Artifact detection" in feedback
        assert any(
            kw in feedback.lower() for kw in ["blur", "banding", "deformation"]
        )

    def test_manual_review_also_gets_feedback(self):
        scores = {
            "prompt_adherence": 0.30,
            "composition_quality": 0.40,
            "pssl_coherence": 0.50,
            "artifact_detection": 0.60,
        }
        feedback = generate_feedback(scores, "MANUAL_REVIEW")
        assert feedback is not None
        assert "Prompt adherence" in feedback


# ===================================================================
# Verdict Emission — emit_verdicts()
# ===================================================================


class TestEmitVerdicts:
    def _make_scored(self, beat_idx, pa, comp, pssl, artifact, retry=0):
        scores = {
            "prompt_adherence": pa,
            "composition_quality": comp,
            "pssl_coherence": pssl,
            "artifact_detection": artifact,
            "composite": compute_composite_score(
                {
                    "prompt_adherence": pa,
                    "composition_quality": comp,
                    "pssl_coherence": pssl,
                    "artifact_detection": artifact,
                },
                DEFAULT_GATE_CONFIG["weights"],
            ),
        }
        return {
            "beat_index": beat_idx,
            "keyframe_url": f"test/img_{beat_idx}.png",
            "scores": scores,
            "retry_count": retry,
            "pssl_params": {},
        }

    def test_batch_summary_counts(self):
        scored = [
            self._make_scored(0, 0.80, 0.75, 0.70, 0.90),  # APPROVED
            self._make_scored(1, 0.30, 0.40, 0.35, 0.50),  # REGENERATE
            self._make_scored(2, 0.30, 0.40, 0.35, 0.50, retry=2),  # MANUAL_REVIEW
        ]
        result = emit_verdicts(scored)
        assert result["batch_summary"]["approved"] == 1
        assert result["batch_summary"]["regenerate"] == 1
        assert result["batch_summary"]["manual_review"] == 1
        assert result["batch_summary"]["total_scored"] == 3

    def test_all_approved(self):
        scored = [self._make_scored(i, 0.85, 0.80, 0.75, 0.95) for i in range(5)]
        result = emit_verdicts(scored)
        assert result["batch_summary"]["approved"] == 5
        assert result["batch_summary"]["regenerate"] == 0
        assert all(r["verdict"] == "APPROVED" for r in result["results"])

    def test_gate_batch_id_format(self):
        scored = [self._make_scored(0, 0.80, 0.70, 0.60, 0.90)]
        result = emit_verdicts(scored)
        assert result["gate_batch_id"].startswith("QG-T2I-")

    def test_threshold_from_config(self):
        scored = [self._make_scored(0, 0.80, 0.70, 0.60, 0.90)]
        config = {**DEFAULT_GATE_CONFIG, "threshold": 0.5}
        result = emit_verdicts(scored, config)
        assert result["threshold"] == 0.5

    def test_quality_gate_unavailable_passed_through(self):
        scored = [
            {
                "beat_index": 0,
                "keyframe_url": "test/img_0.png",
                "scores": None,
                "verdict": "QUALITY_GATE_UNAVAILABLE",
                "retry_count": 0,
                "feedback": "CLIP model failed.",
            }
        ]
        result = emit_verdicts(scored)
        assert result["results"][0]["verdict"] == "QUALITY_GATE_UNAVAILABLE"


# ===================================================================
# Score Keyframes with Mocked Scoring
# ===================================================================


class TestScoreKeyframesMocked:
    @patch("t2i_quality_gate.score_prompt_adherence", return_value=0.85)
    @patch("t2i_quality_gate.score_composition_quality", return_value=0.75)
    @patch("t2i_quality_gate.score_pssl_coherence", return_value=0.70)
    @patch("t2i_quality_gate.score_artifact_detection", return_value=0.90)
    def test_scoring_pipeline(self, mock_art, mock_pssl, mock_comp, mock_pa):
        keyframes = [{"beat_index": 0, "keyframe_path": "img.png", "retry_count": 0}]
        prompts = [
            {"beat_index": 0, "visual_prompt_text": "forest", "pssl_params": {}}
        ]
        results = score_keyframes(keyframes, prompts)
        assert len(results) == 1
        assert results[0]["scores"]["prompt_adherence"] == 0.85
        assert results[0]["scores"]["composite"] > 0

    @patch("t2i_quality_gate.score_prompt_adherence", return_value=-1.0)
    def test_clip_failure_returns_unavailable(self, mock_pa):
        keyframes = [{"beat_index": 0, "keyframe_path": "img.png"}]
        prompts = [
            {"beat_index": 0, "visual_prompt_text": "forest", "pssl_params": {}}
        ]
        results = score_keyframes(keyframes, prompts)
        assert results[0]["verdict"] == "QUALITY_GATE_UNAVAILABLE"


# ===================================================================
# Full Pipeline with Mocked Scoring
# ===================================================================


class TestRunQualityGateMocked:
    @patch("t2i_quality_gate.score_prompt_adherence", return_value=0.85)
    @patch("t2i_quality_gate.score_composition_quality", return_value=0.75)
    @patch("t2i_quality_gate.score_pssl_coherence", return_value=0.70)
    @patch("t2i_quality_gate.score_artifact_detection", return_value=0.90)
    def test_full_pipeline_produces_dep_vid_012(
        self, mock_art, mock_pssl, mock_comp, mock_pa
    ):
        with tempfile.TemporaryDirectory() as tmpdir:
            keyframes = [
                {"beat_index": 0, "keyframe_path": "img.png", "retry_count": 0}
            ]
            prompts = [
                {"beat_index": 0, "visual_prompt_text": "forest", "pssl_params": {}}
            ]
            result, receipt = run_quality_gate(
                keyframes,
                prompts,
                receipt_output_dir=tmpdir,
            )
            assert "gate_batch_id" in result
            assert "batch_summary" in result
            assert result["batch_summary"]["total_scored"] == 1
            assert receipt["stage_name"] == "T2I_QUALITY_VERDICT"
            assert receipt["agent_name"] == "t2i_quality_gate"

    @patch("t2i_quality_gate.score_prompt_adherence", return_value=0.85)
    @patch("t2i_quality_gate.score_composition_quality", return_value=0.75)
    @patch("t2i_quality_gate.score_pssl_coherence", return_value=0.70)
    @patch("t2i_quality_gate.score_artifact_detection", return_value=0.90)
    def test_receipts_chain_linked(self, mock_art, mock_pssl, mock_comp, mock_pa):
        with tempfile.TemporaryDirectory() as tmpdir:
            keyframes = [{"beat_index": 0, "keyframe_path": "img.png"}]
            prompts = [
                {"beat_index": 0, "visual_prompt_text": "forest", "pssl_params": {}}
            ]
            result, receipt = run_quality_gate(
                keyframes,
                prompts,
                receipt_output_dir=tmpdir,
            )
            # Last receipt (Stage 2) should chain from Stage 1, not GENESIS
            assert receipt["previous_receipt_hash"] != "GENESIS"
