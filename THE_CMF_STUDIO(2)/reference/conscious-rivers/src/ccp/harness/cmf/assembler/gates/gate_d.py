"""
Gate D — Pre-Generation Constraint Network (T2I Quality Assurance)

FR-VID-02 §6 Skill Definition

Five validation questions that MUST all pass before any T2I generation batch
is submitted to RunningHub. If ANY answer is False, the batch is rejected
and the pipeline HALTS with the failing question's diagnostic.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""


# ---------------------------------------------------------------------------
# Q1: Prompt-PSSL Coherence
# FR-VID-02 §6 Gate D Q1
# ---------------------------------------------------------------------------

# Temperature-prompt contradiction keywords
WARM_DESCRIPTORS = frozenset([
    "warm", "golden hour", "amber", "sunset", "firelight", "candlelight",
    "orange glow", "golden light", "warm tones",
])
COOL_DESCRIPTORS = frozenset([
    "cold", "icy", "blue hour", "moonlight", "frigid", "cool blue",
    "winter light", "steel gray", "silver light",
])


def check_prompt_pssl_coherence(visual_prompts: list[dict]) -> tuple[bool, str]:
    """
    Gate D Q1: Does every visual prompt's described lighting, color temperature,
    and spatial density match the PSSL parameters attached to that beat?

    A prompt describing "bright afternoon sunlight" with PSSL temperature: cool
    is a contradiction that wastes GPU time.
    """
    for vp in visual_prompts:
        prompt_text = vp.get("visual_prompt_text", "").lower()
        pssl = vp.get("pssl_params", {})
        beat_idx = vp.get("beat_index", "?")
        temperature = str(pssl.get("temperature", "")).lower()

        if temperature == "cool":
            matches = [w for w in WARM_DESCRIPTORS if w in prompt_text]
            if matches:
                return (
                    False,
                    f"Beat {beat_idx}: PSSL temperature='cool' contradicts prompt "
                    f"containing warm lighting descriptors: {matches[:3]}. "
                    f"Fix the visual prompt or PSSL parameters before submission.",
                )
        if temperature == "warm":
            matches = [w for w in COOL_DESCRIPTORS if w in prompt_text]
            if matches:
                return (
                    False,
                    f"Beat {beat_idx}: PSSL temperature='warm' contradicts prompt "
                    f"containing cold lighting descriptors: {matches[:3]}.",
                )

    return (True, "All prompts have coherent PSSL-to-text alignment.")


# ---------------------------------------------------------------------------
# Q2: Negative Prompt Completeness
# FR-VID-02 §6 Gate D Q2
# ---------------------------------------------------------------------------

FLUX_FAILURE_MODES = [
    "blurry", "text", "watermark", "logo", "low quality",
    "deformed", "disfigured", "bad anatomy", "extra limbs",
]
SDXL_FAILURE_MODES = [
    "blurry", "text", "watermark", "logo", "low quality",
    "cartoon", "anime", "illustration", "painting", "drawing",
]


def check_negative_prompt_completeness(
    visual_prompts: list[dict], model: str
) -> tuple[bool, str]:
    """
    Gate D Q2: Does every negative prompt explicitly exclude the failure modes
    of the target model?

    Flux requires different negative prompts than SDXL — generic negatives
    produce generic failures.
    """
    required_modes = FLUX_FAILURE_MODES if "flux" in model.lower() else SDXL_FAILURE_MODES

    for vp in visual_prompts:
        neg_prompt = vp.get("negative_prompt", "").lower()
        beat_idx = vp.get("beat_index", "?")
        missing = [mode for mode in required_modes if mode not in neg_prompt]

        if len(missing) > len(required_modes) // 2:
            return (
                False,
                f"Beat {beat_idx}: Negative prompt missing {len(missing)} of "
                f"{len(required_modes)} model-specific failure modes for {model}: "
                f"{', '.join(missing[:5])}. Add model-specific negatives before submission.",
            )

    return (
        True,
        f"All negative prompts contain sufficient failure mode exclusions for {model}.",
    )


# ---------------------------------------------------------------------------
# Q3: Seed Strategy Justification
# FR-VID-02 §6 Gate D Q3
# ---------------------------------------------------------------------------


def check_seed_strategy(
    visual_prompts: list[dict], is_regeneration: bool
) -> tuple[bool, str]:
    """
    Gate D Q3: Is the seed strategy appropriate for this batch?

    Random seeds for initial generation, preserved seeds for style-consistent
    regeneration — never random when regenerating a beat the operator already
    approved neighboring beats for.
    """
    if is_regeneration:
        for vp in visual_prompts:
            beat_idx = vp.get("beat_index", "?")
            if vp.get("seed") is None:
                return (
                    False,
                    f"Beat {beat_idx}: Regeneration mode but no seed provided. "
                    f"Regeneration must specify the target seed to preserve style "
                    f"consistency with approved neighboring beats.",
                )

    return (True, "Seed strategy is appropriate for this batch type.")


# ---------------------------------------------------------------------------
# Q4: Resolution-Aspect Ratio Match
# FR-VID-02 §6 Gate D Q4
# ---------------------------------------------------------------------------


def check_resolution_aspect_ratio(
    visual_prompts: list[dict],
    target_width: int,
    target_height: int,
) -> tuple[bool, str]:
    """
    Gate D Q4: Does the requested generation resolution match the project's
    target aspect ratio?

    Generating at 1024x1024 for a 9:16 video wastes compute and introduces
    cropping artifacts.
    """
    from math import gcd

    g = gcd(target_width, target_height)
    aspect_w = target_width // g
    aspect_h = target_height // g

    if target_width == target_height:
        ratio_str = "1:1"
    elif aspect_w == 9 and aspect_h == 16:
        ratio_str = "9:16"
    elif aspect_w == 16 and aspect_h == 9:
        ratio_str = "16:9"
    else:
        ratio_str = f"{aspect_w}:{aspect_h}"

    # CMF videos are 9:16 — landscape is always wrong
    if target_width > target_height:
        return (
            False,
            f"Resolution {target_width}x{target_height} is landscape ({ratio_str}). "
            f"CMF videos require 9:16 portrait orientation. "
            f"Generating landscape wastes compute and requires cropping.",
        )

    return (
        True,
        f"Resolution {target_width}x{target_height} ({ratio_str}) is correct for the project.",
    )


# ---------------------------------------------------------------------------
# Q5: Concurrent Limit Awareness
# FR-VID-02 §6 Gate D Q5
# ---------------------------------------------------------------------------

VRAM_TIER_CONCURRENT_LIMITS = {
    "24GB": 5,
    "48GB": 12,
}


def check_concurrent_limit(
    batch_size: int, vram_tier: str, max_concurrent: int
) -> tuple[bool, str]:
    """
    Gate D Q5: Is the batch size within RunningHub's concurrent task limit
    for the selected VRAM tier?

    Submitting 20 concurrent jobs to a 24GB tier that supports 5 concurrent
    tasks will queue 15 jobs, creating false timeout alerts.
    """
    tier_limit = VRAM_TIER_CONCURRENT_LIMITS.get(vram_tier, 5)
    effective_limit = min(tier_limit, max_concurrent)

    if batch_size > effective_limit * 3:
        return (
            False,
            f"Batch size {batch_size} is {batch_size / effective_limit:.1f}x the "
            f"concurrent limit ({effective_limit} for {vram_tier}). This will create "
            f"excessive queuing and timeout risks. Consider splitting into smaller batches.",
        )

    return (
        True,
        f"Batch size {batch_size} is within acceptable range for {vram_tier} "
        f"(concurrent limit: {effective_limit}).",
    )


# ---------------------------------------------------------------------------
# Gate D Runner — executes all 5 questions
# ---------------------------------------------------------------------------


def run_gate_d(
    visual_prompts: list[dict],
    model: str,
    is_regeneration: bool,
    target_width: int,
    target_height: int,
    batch_size: int,
    vram_tier: str,
    max_concurrent: int,
) -> tuple[bool, list[dict]]:
    """
    Run all 5 Gate D questions. Returns (all_passed, results_list).

    If ANY question returns False, all_passed is False and the batch
    MUST NOT be submitted to RunningHub. The pipeline HALTS with the
    failing question's diagnostic.

    FR-VID-02 §6: "If ANY answer is NO, the agent must revise the visual
    prompt array before submission — never submit and hope."
    """
    results = []

    q1_pass, q1_diag = check_prompt_pssl_coherence(visual_prompts)
    results.append({
        "question": 1,
        "name": "Prompt-PSSL Coherence",
        "passed": q1_pass,
        "diagnostic": q1_diag,
    })

    q2_pass, q2_diag = check_negative_prompt_completeness(visual_prompts, model)
    results.append({
        "question": 2,
        "name": "Negative Prompt Completeness",
        "passed": q2_pass,
        "diagnostic": q2_diag,
    })

    q3_pass, q3_diag = check_seed_strategy(visual_prompts, is_regeneration)
    results.append({
        "question": 3,
        "name": "Seed Strategy Justification",
        "passed": q3_pass,
        "diagnostic": q3_diag,
    })

    q4_pass, q4_diag = check_resolution_aspect_ratio(
        visual_prompts, target_width, target_height
    )
    results.append({
        "question": 4,
        "name": "Resolution-Aspect Ratio Match",
        "passed": q4_pass,
        "diagnostic": q4_diag,
    })

    q5_pass, q5_diag = check_concurrent_limit(batch_size, vram_tier, max_concurrent)
    results.append({
        "question": 5,
        "name": "Concurrent Limit Awareness",
        "passed": q5_pass,
        "diagnostic": q5_diag,
    })

    all_passed = all(r["passed"] for r in results)
    return (all_passed, results)
