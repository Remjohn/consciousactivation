"""
Gate D Violation Tests — FR-VID-02 Constraint Network

Build Prompt Stage 5 Completion Gate 5: "For each gate question, name the
validation function and show a test case that demonstrates it catches a violation."

Each test demonstrates that the gate correctly catches a specific violation,
returning False with a diagnostic message.
"""

from gates.gate_d import (
    check_prompt_pssl_coherence,
    check_negative_prompt_completeness,
    check_seed_strategy,
    check_resolution_aspect_ratio,
    check_concurrent_limit,
    run_gate_d,
)


# ---- Q1 Violation: PSSL temperature contradicts prompt ----


def test_gate_d_q1_violation_warm_prompt_cool_pssl():
    """Q1: Prompt describes warm golden hour but PSSL says cool → returns False."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "Scene bathed in warm golden hour sunlight, amber tones",
        "pssl_params": {"temperature": "cool"},
    }]
    passed, diagnostic = check_prompt_pssl_coherence(prompts)
    assert not passed, "Q1 should FAIL: warm prompt + cool PSSL is a contradiction"
    assert "contradicts" in diagnostic.lower()
    assert "cool" in diagnostic.lower()


def test_gate_d_q1_violation_cold_prompt_warm_pssl():
    """Q1: Prompt describes icy moonlight but PSSL says warm → returns False."""
    prompts = [{
        "beat_index": 2,
        "visual_prompt_text": "Cold icy landscape under moonlight, blue shadows",
        "pssl_params": {"temperature": "warm"},
    }]
    passed, diagnostic = check_prompt_pssl_coherence(prompts)
    assert not passed, "Q1 should FAIL: cold prompt + warm PSSL"
    assert "contradicts" in diagnostic.lower()


def test_gate_d_q1_passes_coherent():
    """Q1: Cool prompt + cool PSSL → returns True."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "Cool blue twilight scene, steel gray tones",
        "pssl_params": {"temperature": "cool"},
    }]
    passed, _ = check_prompt_pssl_coherence(prompts)
    assert passed, "Q1 should PASS: coherent temperature"


# ---- Q2 Violation: Missing model-specific failure modes ----


def test_gate_d_q2_violation_empty_negative():
    """Q2: Empty negative prompt for Flux model → returns False."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "A dramatic scene",
        "negative_prompt": "",
    }]
    passed, diagnostic = check_negative_prompt_completeness(prompts, "flux-dev-fp8")
    assert not passed, "Q2 should FAIL: empty negative prompt"
    assert "failure mode" in diagnostic.lower()


def test_gate_d_q2_passes_complete_flux():
    """Q2: Full Flux negatives included → returns True."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "A scene",
        "negative_prompt": (
            "blurry, text, watermark, logo, low quality, "
            "deformed, disfigured, bad anatomy, extra limbs"
        ),
    }]
    passed, _ = check_negative_prompt_completeness(prompts, "flux-dev-fp8")
    assert passed, "Q2 should PASS: all Flux failure modes present"


# ---- Q3 Violation: Regeneration without preserved seed ----


def test_gate_d_q3_violation_regen_no_seed():
    """Q3: Regeneration mode but seed is None → returns False."""
    prompts = [{"beat_index": 3, "visual_prompt_text": "A scene", "seed": None}]
    passed, diagnostic = check_seed_strategy(prompts, is_regeneration=True)
    assert not passed, "Q3 should FAIL: regeneration without seed"
    assert "regeneration" in diagnostic.lower()


def test_gate_d_q3_passes_initial_generation():
    """Q3: Initial generation (no seed required) → returns True."""
    prompts = [{"beat_index": 0, "visual_prompt_text": "A scene"}]
    passed, _ = check_seed_strategy(prompts, is_regeneration=False)
    assert passed, "Q3 should PASS: initial generation allows random seeds"


def test_gate_d_q3_passes_regen_with_seed():
    """Q3: Regeneration with preserved seed → returns True."""
    prompts = [{"beat_index": 3, "visual_prompt_text": "A scene", "seed": 42891}]
    passed, _ = check_seed_strategy(prompts, is_regeneration=True)
    assert passed, "Q3 should PASS: regeneration with explicit seed"


# ---- Q4 Violation: Landscape resolution for 9:16 project ----


def test_gate_d_q4_violation_landscape():
    """Q4: 1920x1080 landscape for CMF 9:16 video → returns False."""
    prompts = [{"beat_index": 0}]
    passed, diagnostic = check_resolution_aspect_ratio(prompts, 1920, 1080)
    assert not passed, "Q4 should FAIL: landscape resolution"
    assert "landscape" in diagnostic.lower()


def test_gate_d_q4_passes_portrait():
    """Q4: 1080x1920 portrait → returns True."""
    prompts = [{"beat_index": 0}]
    passed, _ = check_resolution_aspect_ratio(prompts, 1080, 1920)
    assert passed, "Q4 should PASS: correct 9:16 portrait"


# ---- Q5 Violation: Excessive batch size ----


def test_gate_d_q5_violation_oversized_batch():
    """Q5: 50-beat batch on 24GB tier (5 concurrent limit) → returns False."""
    passed, diagnostic = check_concurrent_limit(50, "24GB", 5)
    assert not passed, "Q5 should FAIL: 50 beats >> 5 concurrent × 3 = 15"
    assert "concurrent limit" in diagnostic.lower() or "queuing" in diagnostic.lower()


def test_gate_d_q5_passes_normal_batch():
    """Q5: 12-beat batch on 48GB tier → returns True."""
    passed, _ = check_concurrent_limit(12, "48GB", 12)
    assert passed, "Q5 should PASS: 12 beats <= 12 concurrent × 3 = 36"


# ---- Full Gate D Runner ----


def test_gate_d_full_run_with_violation():
    """Full Gate D returns False when Q1 fails (warm prompt + cool PSSL)."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "Warm golden hour scene with amber tones",
        "pssl_params": {"temperature": "cool"},
        "negative_prompt": (
            "blurry, text, watermark, logo, low quality, "
            "deformed, disfigured, bad anatomy, extra limbs"
        ),
    }]
    all_passed, results = run_gate_d(
        visual_prompts=prompts,
        model="flux-dev-fp8",
        is_regeneration=False,
        target_width=1080,
        target_height=1920,
        batch_size=12,
        vram_tier="48GB",
        max_concurrent=12,
    )
    assert not all_passed, "Gate D should FAIL: Q1 violation present"
    q1 = next(r for r in results if r["question"] == 1)
    assert not q1["passed"]
    assert "contradicts" in q1["diagnostic"].lower()


def test_gate_d_full_run_all_pass():
    """Full Gate D returns True when all 5 questions pass."""
    prompts = [{
        "beat_index": 0,
        "visual_prompt_text": "Cool, misty winter landscape under blue hour light",
        "pssl_params": {"temperature": "cool"},
        "negative_prompt": (
            "blurry, text, watermark, logo, low quality, "
            "deformed, disfigured, bad anatomy, extra limbs"
        ),
        "seed": None,
    }]
    all_passed, results = run_gate_d(
        visual_prompts=prompts,
        model="flux-dev-fp8",
        is_regeneration=False,
        target_width=1080,
        target_height=1920,
        batch_size=12,
        vram_tier="48GB",
        max_concurrent=12,
    )
    assert all_passed, f"Gate D should PASS: {[r for r in results if not r['passed']]}"
    assert all(r["passed"] for r in results)
