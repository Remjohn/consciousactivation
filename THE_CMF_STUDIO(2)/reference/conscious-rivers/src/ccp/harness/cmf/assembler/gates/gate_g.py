"""
Gate G — Quality Gate Self-Calibration Network

FR-VID-04 §6 Skill Definition

Four validation questions that MUST all pass before processing a new project's
batch through the quality gate. If ANY answer is NO, the agent must calibrate
before scoring.

Each function returns: (passed: bool, diagnostic: str)

Build Prompt Rule 7: These are executable validation functions, NOT
documentation-only comments.
"""


# ---------------------------------------------------------------------------
# Q1: Threshold Appropriateness
# FR-VID-04 §6 Gate G Q1
# ---------------------------------------------------------------------------

ABSTRACT_STYLES = frozenset(
    [
        "abstract",
        "artistic",
        "impressionist",
        "expressionist",
        "surreal",
        "stylized",
        "painterly",
        "watercolor",
    ]
)


def check_threshold_appropriateness(
    threshold: float,
    visual_style: str = "photorealistic",
) -> tuple[bool, str]:
    """
    Gate G Q1: Is the threshold appropriate for this project's visual style?

    Highly stylized or abstract visual prompts systematically score lower on
    CLIP adherence — the threshold may need adjustment to 0.5 for artistic
    projects.
    """
    style_lower = visual_style.lower()
    is_abstract = any(s in style_lower for s in ABSTRACT_STYLES)

    if is_abstract and threshold > 0.55:
        return (
            False,
            f"Threshold {threshold} is too strict for '{visual_style}' style. "
            f"Abstract/stylized prompts systematically score lower on CLIP adherence. "
            f"Recommend threshold ≤ 0.55 for artistic projects.",
        )

    if threshold < 0.3:
        return (
            False,
            f"Threshold {threshold} is dangerously low — nearly all keyframes will pass "
            f"regardless of quality. Minimum recommended threshold is 0.3.",
        )

    if threshold > 0.9:
        return (
            False,
            f"Threshold {threshold} is extremely strict — most CLIP similarity scores "
            f"fall below 0.9 even for well-matched image-prompt pairs. "
            f"Recommend threshold ≤ 0.85 at most.",
        )

    return (True, f"Threshold {threshold} is appropriate for '{visual_style}' style.")


# ---------------------------------------------------------------------------
# Q2: CLIP Model Currency
# FR-VID-04 §6 Gate G Q2
# ---------------------------------------------------------------------------

VALID_CLIP_MODELS = frozenset(
    [
        "ViT-L/14",
        "ViT-B/32",
        "ViT-B/16",
        "ViT-L/14@336px",
        "RN50",
        "RN101",
        "RN50x4",
        "RN50x16",
        "RN50x64",
    ]
)

PHOTOREALISTIC_MODELS = frozenset(["ViT-L/14", "ViT-L/14@336px"])
ABSTRACT_MODELS = frozenset(["ViT-B/32", "ViT-B/16"])


def check_clip_model_currency(
    clip_model_name: str,
    visual_style: str = "photorealistic",
) -> tuple[bool, str]:
    """
    Gate G Q2: Is the loaded CLIP model the correct variant for this
    project's imagery domain?

    ViT-L/14 excels at photorealistic prompts; ViT-B/32 handles abstract
    prompts better. Wrong model → wrong scores.
    """
    if clip_model_name not in VALID_CLIP_MODELS:
        return (
            False,
            f"CLIP model '{clip_model_name}' is not a recognized variant. "
            f"Valid models: {', '.join(sorted(VALID_CLIP_MODELS))}.",
        )

    style_lower = visual_style.lower()
    abstract_keywords = ["abstract", "artistic", "stylized", "painterly"]
    is_abstract = any(kw in style_lower for kw in abstract_keywords)

    if is_abstract and clip_model_name in PHOTOREALISTIC_MODELS:
        return (
            False,
            f"CLIP model '{clip_model_name}' is optimized for photorealistic imagery "
            f"but project style is '{visual_style}'. Consider ViT-B/32 for abstract content.",
        )

    return (
        True,
        f"CLIP model '{clip_model_name}' is appropriate for '{visual_style}' style.",
    )


# ---------------------------------------------------------------------------
# Q3: Regeneration Budget
# FR-VID-04 §6 Gate G Q3
# ---------------------------------------------------------------------------


def check_regeneration_budget(
    expected_fail_rate: float,
    batch_size: int,
    max_retries: int = 2,
) -> tuple[bool, str]:
    """
    Gate G Q3: At the current threshold, how many keyframes are expected to fail?

    If >50% of keyframes fail, the threshold is too strict or the storyboard
    composer's Gate C constraint network is not working — DO NOT brute-force
    by regenerating; fix upstream.
    """
    if expected_fail_rate > 0.50:
        expected_failures = int(batch_size * expected_fail_rate)
        total_regenerations = expected_failures * max_retries
        return (
            False,
            f"Expected fail rate {expected_fail_rate:.0%} means {expected_failures} of "
            f"{batch_size} keyframes will fail, requiring up to {total_regenerations} "
            f"regenerations. This indicates upstream quality issues (Gate C or visual "
            f"prompt quality). Fix upstream before brute-forcing with regeneration.",
        )

    return (
        True,
        f"Expected fail rate {expected_fail_rate:.0%} is within acceptable range "
        f"for a {batch_size}-keyframe batch.",
    )


# ---------------------------------------------------------------------------
# Q4: Dimension Weight Appropriateness
# FR-VID-04 §6 Gate G Q4
# ---------------------------------------------------------------------------


def check_dimension_weight_appropriateness(
    weights: dict[str, float],
    has_pssl_specs: bool = True,
) -> tuple[bool, str]:
    """
    Gate G Q4: Are the default scoring weights correct for this project?

    A project with no PSSL specifications should set PSSL weight to 0.0
    and redistribute to other dimensions. Weights must sum to 1.0.
    """
    weight_sum = sum(weights.values())
    if abs(weight_sum - 1.0) > 0.001:
        return (
            False,
            f"Scoring weights sum to {weight_sum:.3f}, not 1.0. "
            f"Weights must sum to exactly 1.0 for valid composite scoring.",
        )

    pssl_weight = weights.get("pssl_coherence", 0.0)

    if not has_pssl_specs and pssl_weight > 0.0:
        return (
            False,
            f"Project has no PSSL specifications but PSSL coherence weight is "
            f"{pssl_weight:.2f}. Set pssl_coherence weight to 0.0 and redistribute "
            f"to other dimensions to avoid penalizing keyframes for missing PSSL data.",
        )

    if has_pssl_specs and pssl_weight == 0.0:
        return (
            False,
            f"Project has PSSL specifications but PSSL coherence weight is 0.0. "
            f"PSSL coherence must be weighted to enforce visual language compliance.",
        )

    return (True, f"Scoring weights are appropriate (sum: {weight_sum:.3f}).")


# ---------------------------------------------------------------------------
# Gate G Runner — executes all 4 questions
# ---------------------------------------------------------------------------


def run_gate_g(
    threshold: float,
    clip_model_name: str,
    visual_style: str,
    expected_fail_rate: float,
    batch_size: int,
    max_retries: int,
    weights: dict[str, float],
    has_pssl_specs: bool,
) -> tuple[bool, list[dict]]:
    """
    Run all 4 Gate G questions. Returns (all_passed, results_list).

    If ANY question returns False, the agent must calibrate the gate
    configuration before scoring.
    """
    results = []

    q1_pass, q1_diag = check_threshold_appropriateness(threshold, visual_style)
    results.append(
        {
            "question": 1,
            "name": "Threshold Appropriateness",
            "passed": q1_pass,
            "diagnostic": q1_diag,
        }
    )

    q2_pass, q2_diag = check_clip_model_currency(clip_model_name, visual_style)
    results.append(
        {
            "question": 2,
            "name": "CLIP Model Currency",
            "passed": q2_pass,
            "diagnostic": q2_diag,
        }
    )

    q3_pass, q3_diag = check_regeneration_budget(
        expected_fail_rate, batch_size, max_retries
    )
    results.append(
        {
            "question": 3,
            "name": "Regeneration Budget",
            "passed": q3_pass,
            "diagnostic": q3_diag,
        }
    )

    q4_pass, q4_diag = check_dimension_weight_appropriateness(weights, has_pssl_specs)
    results.append(
        {
            "question": 4,
            "name": "Dimension Weight Appropriateness",
            "passed": q4_pass,
            "diagnostic": q4_diag,
        }
    )

    all_passed = all(r["passed"] for r in results)
    return (all_passed, results)
