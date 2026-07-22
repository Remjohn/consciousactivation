"""
Gate G Violation Tests — FR-VID-04 Constraint Network

Build Prompt Stage 5 Completion Gate 5: "For each gate question, name the
validation function and show a test case that demonstrates it catches a violation."

Tests all 4 Gate G validation functions. Each test demonstrates the gate
correctly catches a specific violation, returning False with a diagnostic.
"""

from gates.gate_g import (
    check_threshold_appropriateness,
    check_clip_model_currency,
    check_regeneration_budget,
    check_dimension_weight_appropriateness,
    run_gate_g,
)


# ---- Q1 Violation: Threshold too strict for abstract style ----


def test_gate_g_q1_violation_abstract_high_threshold():
    """Q1: Abstract art with 0.6 threshold → returns False."""
    passed, diagnostic = check_threshold_appropriateness(0.6, "abstract art")
    assert not passed, "Q1 should FAIL: 0.6 is too strict for abstract style"
    assert "too strict" in diagnostic.lower()


def test_gate_g_q1_violation_dangerously_low():
    """Q1: Threshold 0.2 is too low for any project → returns False."""
    passed, diagnostic = check_threshold_appropriateness(0.2, "photorealistic")
    assert not passed, "Q1 should FAIL: 0.2 is dangerously low"
    assert "dangerously low" in diagnostic.lower()


def test_gate_g_q1_violation_extremely_strict():
    """Q1: Threshold 0.95 is too strict → returns False."""
    passed, diagnostic = check_threshold_appropriateness(0.95, "photorealistic")
    assert not passed, "Q1 should FAIL: 0.95 is unreachable for most images"
    assert "extremely strict" in diagnostic.lower()


def test_gate_g_q1_passes_photorealistic_default():
    """Q1: Photorealistic style with 0.6 threshold → returns True."""
    passed, _ = check_threshold_appropriateness(0.6, "photorealistic")
    assert passed, "Q1 should PASS: 0.6 is appropriate for photorealistic"


def test_gate_g_q1_passes_abstract_low_threshold():
    """Q1: Abstract with 0.5 threshold → returns True."""
    passed, _ = check_threshold_appropriateness(0.5, "abstract art")
    assert passed, "Q1 should PASS: 0.5 is appropriate for abstract"


def test_gate_g_q1_violation_stylized_high_threshold():
    """Q1: Stylized illustration at 0.7 threshold → returns False."""
    passed, _ = check_threshold_appropriateness(0.7, "stylized illustration")
    assert not passed, "Q1 should FAIL: 0.7 is too strict for stylized"


# ---- Q2 Violation: Wrong CLIP model for visual style ----


def test_gate_g_q2_violation_invalid_model():
    """Q2: Unrecognized CLIP model name → returns False."""
    passed, diagnostic = check_clip_model_currency("GPT-4V", "photorealistic")
    assert not passed, "Q2 should FAIL: GPT-4V is not a valid CLIP model"
    assert "not a recognized" in diagnostic.lower()


def test_gate_g_q2_violation_photorealistic_model_for_abstract():
    """Q2: ViT-L/14 for abstract art → returns False."""
    passed, diagnostic = check_clip_model_currency("ViT-L/14", "abstract art")
    assert not passed, "Q2 should FAIL: ViT-L/14 is wrong for abstract"
    assert "ViT-B/32" in diagnostic


def test_gate_g_q2_passes_vit_l14_photorealistic():
    """Q2: ViT-L/14 for photorealistic → returns True."""
    passed, _ = check_clip_model_currency("ViT-L/14", "photorealistic")
    assert passed, "Q2 should PASS: ViT-L/14 is correct for photorealistic"


def test_gate_g_q2_passes_vit_b32_abstract():
    """Q2: ViT-B/32 for abstract art → returns True."""
    passed, _ = check_clip_model_currency("ViT-B/32", "abstract art")
    assert passed, "Q2 should PASS: ViT-B/32 is correct for abstract"


def test_gate_g_q2_passes_vit_b16_stylized():
    """Q2: ViT-B/16 for stylized content → returns True."""
    passed, _ = check_clip_model_currency("ViT-B/16", "stylized")
    assert passed, "Q2 should PASS: ViT-B/16 handles abstract/stylized"


# ---- Q3 Violation: Regeneration budget exceeded ----


def test_gate_g_q3_violation_high_fail_rate():
    """Q3: 60% expected fail rate → returns False."""
    passed, diagnostic = check_regeneration_budget(0.60, 12, 2)
    assert not passed, "Q3 should FAIL: >50% fail rate indicates upstream issues"
    assert "upstream" in diagnostic.lower()


def test_gate_g_q3_violation_51_percent():
    """Q3: 51% fail rate → returns False."""
    passed, _ = check_regeneration_budget(0.51, 10, 2)
    assert not passed, "Q3 should FAIL: 51% > 50% threshold"


def test_gate_g_q3_passes_low_fail_rate():
    """Q3: 15% expected fail rate → returns True."""
    passed, _ = check_regeneration_budget(0.15, 12, 2)
    assert passed, "Q3 should PASS: 15% is within acceptable range"


def test_gate_g_q3_passes_exactly_50_percent():
    """Q3: Exactly 50% fail rate → returns True (boundary is >50%)."""
    passed, _ = check_regeneration_budget(0.50, 10, 2)
    assert passed, "Q3 should PASS: 50% is boundary, not exceeded"


def test_gate_g_q3_passes_zero_fail_rate():
    """Q3: 0% fail rate → returns True."""
    passed, _ = check_regeneration_budget(0.0, 12, 2)
    assert passed, "Q3 should PASS: no failures expected"


# ---- Q4 Violation: Scoring weights misconfigured ----


def test_gate_g_q4_violation_weights_wrong_sum():
    """Q4: Weights sum to 1.10 → returns False."""
    weights = {
        "prompt_adherence": 0.40,
        "composition_quality": 0.20,
        "pssl_coherence": 0.25,
        "artifact_detection": 0.25,
    }
    passed, diagnostic = check_dimension_weight_appropriateness(weights, has_pssl_specs=True)
    assert not passed, "Q4 should FAIL: weights sum to 1.10"
    assert "sum to" in diagnostic.lower()


def test_gate_g_q4_violation_pssl_nonzero_without_specs():
    """Q4: PSSL weight 0.25 but no PSSL specs → returns False."""
    weights = {
        "prompt_adherence": 0.40,
        "composition_quality": 0.20,
        "pssl_coherence": 0.25,
        "artifact_detection": 0.15,
    }
    passed, diagnostic = check_dimension_weight_appropriateness(weights, has_pssl_specs=False)
    assert not passed, "Q4 should FAIL: PSSL weight nonzero but no PSSL specs"
    assert "no pssl specifications" in diagnostic.lower()


def test_gate_g_q4_violation_pssl_zero_with_specs():
    """Q4: PSSL weight 0.0 but project has PSSL specs → returns False."""
    weights = {
        "prompt_adherence": 0.50,
        "composition_quality": 0.30,
        "pssl_coherence": 0.0,
        "artifact_detection": 0.20,
    }
    passed, diagnostic = check_dimension_weight_appropriateness(weights, has_pssl_specs=True)
    assert not passed, "Q4 should FAIL: PSSL weight is 0 but specs exist"
    assert "must be weighted" in diagnostic.lower()


def test_gate_g_q4_passes_default_with_pssl():
    """Q4: Default weights with PSSL specs → returns True."""
    weights = {
        "prompt_adherence": 0.40,
        "composition_quality": 0.20,
        "pssl_coherence": 0.25,
        "artifact_detection": 0.15,
    }
    passed, _ = check_dimension_weight_appropriateness(weights, has_pssl_specs=True)
    assert passed, "Q4 should PASS: default weights are correct with PSSL"


def test_gate_g_q4_passes_no_pssl_redistributed():
    """Q4: PSSL weight 0.0 redistributed, no PSSL specs → returns True."""
    weights = {
        "prompt_adherence": 0.50,
        "composition_quality": 0.30,
        "pssl_coherence": 0.0,
        "artifact_detection": 0.20,
    }
    passed, _ = check_dimension_weight_appropriateness(weights, has_pssl_specs=False)
    assert passed, "Q4 should PASS: PSSL weight 0 when no specs"


# ---- Full Gate G Runner ----


def test_gate_g_full_run_all_pass():
    """Full Gate G returns True when all 4 questions pass."""
    all_passed, results = run_gate_g(
        threshold=0.6,
        clip_model_name="ViT-L/14",
        visual_style="photorealistic",
        expected_fail_rate=0.15,
        batch_size=12,
        max_retries=2,
        weights={
            "prompt_adherence": 0.40,
            "composition_quality": 0.20,
            "pssl_coherence": 0.25,
            "artifact_detection": 0.15,
        },
        has_pssl_specs=True,
    )
    assert all_passed, f"Gate G should PASS: {[r for r in results if not r['passed']]}"
    assert len(results) == 4
    assert all(r["passed"] for r in results)


def test_gate_g_full_run_one_fail():
    """Full Gate G returns False when Q2 fails (wrong model for style)."""
    all_passed, results = run_gate_g(
        threshold=0.6,
        clip_model_name="ViT-L/14",
        visual_style="abstract",
        expected_fail_rate=0.15,
        batch_size=12,
        max_retries=2,
        weights={
            "prompt_adherence": 0.40,
            "composition_quality": 0.20,
            "pssl_coherence": 0.25,
            "artifact_detection": 0.15,
        },
        has_pssl_specs=True,
    )
    assert not all_passed, "Gate G should FAIL: abstract style + ViT-L/14"


def test_gate_g_full_run_multiple_failures():
    """Full Gate G reports all failures when multiple questions fail."""
    all_passed, results = run_gate_g(
        threshold=0.2,
        clip_model_name="InvalidModel",
        visual_style="abstract",
        expected_fail_rate=0.8,
        batch_size=12,
        max_retries=2,
        weights={
            "prompt_adherence": 0.40,
            "composition_quality": 0.20,
            "pssl_coherence": 0.25,
            "artifact_detection": 0.10,
        },
        has_pssl_specs=True,
    )
    assert not all_passed, "Gate G should FAIL: multiple violations"
    failed = [r for r in results if not r["passed"]]
    assert len(failed) >= 3
