"""
T2I Quality Gate — Multi-dimensional keyframe scoring for I2V pipeline protection.

FR-VID-04: Scores every keyframe before it proceeds to I2V. Keyframes scoring
≥ threshold proceed; below-threshold keyframes trigger T2I regeneration
(up to 2 retries) or operator manual review.

Pipeline Stages:
  Stage 1: T2I_QUALITY_SCORING — CLIP + composition + PSSL + artifact scoring
  Stage 2: T2I_QUALITY_VERDICT — threshold comparison → verdict emission

Produces: DEP-VID-012 (T2I Quality Score Result)
Consumes: DEP-VID-008 (T2I Generation Result), DEP-VID-006 (Visual Prompt Array),
          DEP-VID-013 (Quality Gate Configuration)
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
except ImportError:
    from receipt_chain import write_receipt


# ---------------------------------------------------------------------------
# Default Configuration (DEP-VID-013)
# ---------------------------------------------------------------------------

DEFAULT_GATE_CONFIG = {
    "threshold": 0.6,
    "max_retries": 2,
    "weights": {
        "prompt_adherence": 0.40,
        "composition_quality": 0.20,
        "pssl_coherence": 0.25,
        "artifact_detection": 0.15,
    },
    "clip_model": "ViT-L/14",
}


# ---------------------------------------------------------------------------
# Scoring Functions
# ---------------------------------------------------------------------------


def score_prompt_adherence(
    image_path: str, prompt_text: str, clip_model: Any = None
) -> float:
    """
    FR-VID-04 §4 Stage 1 Step 2a: Compute CLIP cosine similarity between
    visual prompt text and keyframe image. Range: 0.0-1.0.

    If clip_model is None, attempts to load CLIP. Returns -1.0 on failure.
    """
    try:
        import torch
        import clip
        from PIL import Image

        device = "cuda" if torch.cuda.is_available() else "cpu"

        if clip_model is None:
            model, preprocess = clip.load("ViT-L/14", device=device)
        else:
            model, preprocess = clip_model

        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        text = clip.tokenize([prompt_text], truncate=True).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text)

            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)

            similarity = (image_features @ text_features.T).item()

        return max(0.0, min(1.0, similarity))
    except Exception:
        return -1.0


def score_composition_quality(image_path: str) -> float:
    """
    FR-VID-04 §4 Stage 1 Step 2b: Analyze rule-of-thirds alignment,
    focal point detection, visual weight balance. Range: 0.0-1.0.
    """
    try:
        import numpy as np
        from PIL import Image

        img = np.array(Image.open(image_path).convert("RGB"))
        h, w = img.shape[:2]

        gray = np.mean(img, axis=2)

        # Local contrast via standard deviation in 3×3 grid cells
        grid_scores = []
        for i in range(3):
            for j in range(3):
                r_start, r_end = i * h // 3, (i + 1) * h // 3
                c_start, c_end = j * w // 3, (j + 1) * w // 3
                cell = gray[r_start:r_end, c_start:c_end]
                grid_scores.append(float(np.std(cell)))

        # Interest at intersection points (corner cells of grid)
        corner_interests = [grid_scores[0], grid_scores[2], grid_scores[6], grid_scores[8]]
        max_interest = max(grid_scores) if max(grid_scores) > 0 else 1.0

        thirds_score = sum(corner_interests) / (4 * max_interest) if max_interest > 0 else 0.5

        # Visual weight balance: left vs right half
        left_weight = float(np.mean(gray[:, : w // 2]))
        right_weight = float(np.mean(gray[:, w // 2 :]))
        max_weight = max(left_weight, right_weight, 1.0)
        balance_score = 1.0 - abs(left_weight - right_weight) / max_weight

        # Focal point: presence of clear focal area (high contrast region)
        focal_score = min(1.0, float(np.std(gray)) / 80.0)

        composite = 0.4 * thirds_score + 0.3 * balance_score + 0.3 * focal_score
        return max(0.0, min(1.0, composite))
    except Exception:
        return -1.0


def score_pssl_coherence(image_path: str, pssl_params: dict) -> float:
    """
    FR-VID-04 §4 Stage 1 Step 2c: Extract dominant color from keyframe,
    compare to PSSL foundation_hue. Compare estimated lighting temperature
    to PSSL temperature parameter. Range: 0.0-1.0.
    """
    try:
        import numpy as np
        from PIL import Image

        img = np.array(Image.open(image_path).convert("RGB"))

        foundation_hue = pssl_params.get("foundation_hue")
        temperature = pssl_params.get("temperature")

        if not foundation_hue and not temperature:
            return 1.0

        scores = []

        if foundation_hue:
            hue_hex = foundation_hue.lstrip("#")
            if len(hue_hex) == 6:
                target_r = int(hue_hex[0:2], 16)
                target_g = int(hue_hex[2:4], 16)
                target_b = int(hue_hex[4:6], 16)

                mean_r = float(np.mean(img[:, :, 0]))
                mean_g = float(np.mean(img[:, :, 1]))
                mean_b = float(np.mean(img[:, :, 2]))

                distance = (
                    (mean_r - target_r) ** 2
                    + (mean_g - target_g) ** 2
                    + (mean_b - target_b) ** 2
                ) ** 0.5
                max_distance = (255**2 * 3) ** 0.5
                hue_score = 1.0 - (distance / max_distance)
                scores.append(hue_score)

        if temperature:
            temp_lower = str(temperature).lower()
            mean_r = float(np.mean(img[:, :, 0]))
            mean_b = float(np.mean(img[:, :, 2]))

            warmth_ratio = mean_r / max(mean_b, 1.0)

            if temp_lower == "warm":
                temp_score = min(1.0, warmth_ratio / 1.5)
            elif temp_lower == "cool":
                temp_score = min(1.0, (1.0 / max(warmth_ratio, 0.1)) / 1.5)
            else:
                temp_score = 0.7

            scores.append(temp_score)

        return max(0.0, min(1.0, sum(scores) / len(scores))) if scores else 1.0
    except Exception:
        return -1.0


def score_artifact_detection(image_path: str) -> float:
    """
    FR-VID-04 §4 Stage 1 Step 2d: Compute Laplacian variance for blur detection,
    check for banding patterns, detect deformation via edge analysis.
    Range: 0.0 (many artifacts) to 1.0 (clean).
    """
    try:
        import numpy as np
        from PIL import Image

        img = np.array(Image.open(image_path).convert("L"), dtype=np.float64)

        # Laplacian variance for blur detection
        laplacian = (
            img[:-2, 1:-1]
            + img[2:, 1:-1]
            + img[1:-1, :-2]
            + img[1:-1, 2:]
            - 4 * img[1:-1, 1:-1]
        )
        lap_var = float(np.var(laplacian))
        blur_score = min(1.0, lap_var / 500.0)

        # Banding detection: repeating horizontal patterns
        row_means = np.mean(img, axis=1)
        row_diffs = np.abs(np.diff(row_means))
        banding_variance = float(np.var(row_diffs))
        banding_score = (
            min(1.0, 1.0 - (banding_variance / 1000.0))
            if banding_variance < 1000
            else 0.0
        )

        # Edge deformation: Sobel-like gradient magnitude
        gx = img[1:-1, 2:] - img[1:-1, :-2]
        gy = img[2:, 1:-1] - img[:-2, 1:-1]
        min_h = min(gx.shape[0], gy.shape[0])
        min_w = min(gx.shape[1], gy.shape[1])
        gradient_mag = np.sqrt(gx[:min_h, :min_w] ** 2 + gy[:min_h, :min_w] ** 2)
        edge_consistency = float(np.std(gradient_mag))
        edge_score = min(1.0, edge_consistency / 50.0)

        composite = 0.5 * blur_score + 0.25 * banding_score + 0.25 * edge_score
        return max(0.0, min(1.0, composite))
    except Exception:
        return -1.0


# ---------------------------------------------------------------------------
# Composite Scoring
# ---------------------------------------------------------------------------


def compute_composite_score(
    dimension_scores: dict[str, float],
    weights: dict[str, float],
) -> float:
    """
    FR-VID-04 §4 Stage 1 Step 3: Compute weighted composite score.
    total = 0.40 × prompt + 0.20 × composition + 0.25 × pssl + 0.15 × artifacts
    """
    total = 0.0
    for dim, weight in weights.items():
        score = dimension_scores.get(dim, 0.0)
        total += weight * score
    return round(total, 4)


# ---------------------------------------------------------------------------
# Verdict Logic
# ---------------------------------------------------------------------------


def determine_verdict(
    composite_score: float,
    threshold: float,
    retry_count: int,
    max_retries: int,
    operator_override: bool = False,
) -> str:
    """
    FR-VID-04 §4 Stage 1 Step 4 + AC5:
    - APPROVED: score ≥ threshold, OR operator_override is True
    - REGENERATE: score < threshold AND retries < max
    - MANUAL_REVIEW: score < threshold AND retries ≥ max
    """
    if operator_override:
        return "APPROVED"
    if composite_score >= threshold:
        return "APPROVED"
    if retry_count < max_retries:
        return "REGENERATE"
    return "MANUAL_REVIEW"


# ---------------------------------------------------------------------------
# Feedback Generation
# ---------------------------------------------------------------------------


def generate_feedback(
    dimension_scores: dict[str, float],
    verdict: str,
    pssl_params: dict | None = None,
) -> str | None:
    """
    FR-VID-04 §4 Stage 2 Step 2 + AC3: For REGENERATE/MANUAL_REVIEW verdicts,
    identify the lowest-scoring dimension and construct specific divergence feedback.
    """
    if verdict == "APPROVED":
        return None

    lowest_dim = min(dimension_scores, key=dimension_scores.get)
    lowest_score = dimension_scores[lowest_dim]

    dim_labels = {
        "prompt_adherence": "Prompt adherence",
        "composition_quality": "Composition quality",
        "pssl_coherence": "PSSL coherence",
        "artifact_detection": "Artifact detection",
    }

    label = dim_labels.get(lowest_dim, lowest_dim)

    feedback_parts = [f"{label} failed (score: {lowest_score:.2f})"]

    if lowest_dim == "pssl_coherence" and pssl_params:
        hue = pssl_params.get("foundation_hue", "")
        temp = pssl_params.get("temperature", "")
        if hue:
            feedback_parts.append(
                f"keyframe foundation hue diverges from specified {hue}"
            )
        if temp:
            feedback_parts.append(
                f"lighting temperature does not match '{temp}' specification"
            )
    elif lowest_dim == "prompt_adherence":
        feedback_parts.append("scene composition does not match prompt description")
    elif lowest_dim == "composition_quality":
        feedback_parts.append(
            "framing or visual weight distribution is suboptimal"
        )
    elif lowest_dim == "artifact_detection":
        feedback_parts.append(
            "image contains blur, banding, or deformation artifacts"
        )

    return " — ".join(feedback_parts)


# ---------------------------------------------------------------------------
# Stage 1: Keyframe Scoring
# ---------------------------------------------------------------------------


def score_keyframes(
    keyframes: list[dict],
    visual_prompts: list[dict],
    gate_config: dict | None = None,
    clip_model: Any = None,
) -> list[dict]:
    """
    FR-VID-04 §4 Stage 1: Score all keyframes against their originating
    visual prompts across 4 dimensions.

    Args:
        keyframes: List of DEP-VID-008 results (beat_index, keyframe_url/keyframe_path).
        visual_prompts: List of DEP-VID-006 entries (beat_index, visual_prompt_text, pssl_params).
        gate_config: DEP-VID-013 configuration (threshold, weights, max_retries, clip_model).
        clip_model: Pre-loaded CLIP model tuple (model, preprocess) or None.

    Returns:
        List of per-beat score dicts.
    """
    config = gate_config or DEFAULT_GATE_CONFIG
    weights = config.get("weights", DEFAULT_GATE_CONFIG["weights"])

    prompt_map = {vp["beat_index"]: vp for vp in visual_prompts}

    scored_results = []
    for kf in keyframes:
        beat_idx = kf["beat_index"]
        image_path = kf.get("keyframe_path") or kf.get("keyframe_url", "")
        vp = prompt_map.get(beat_idx, {})
        prompt_text = vp.get("visual_prompt_text", "")
        pssl_params = vp.get("pssl_params", {})
        retry_count = kf.get("retry_count", 0)

        pa_score = score_prompt_adherence(image_path, prompt_text, clip_model)
        comp_score = score_composition_quality(image_path)
        pssl_score = score_pssl_coherence(image_path, pssl_params)
        artifact_score = score_artifact_detection(image_path)

        if pa_score < 0:
            scored_results.append(
                {
                    "beat_index": beat_idx,
                    "keyframe_url": kf.get("keyframe_url", image_path),
                    "scores": None,
                    "verdict": "QUALITY_GATE_UNAVAILABLE",
                    "retry_count": retry_count,
                    "feedback": "CLIP model failed to score this keyframe.",
                }
            )
            continue

        dimension_scores = {
            "prompt_adherence": pa_score,
            "composition_quality": max(0.0, comp_score),
            "pssl_coherence": max(0.0, pssl_score),
            "artifact_detection": max(0.0, artifact_score),
        }

        composite = compute_composite_score(dimension_scores, weights)

        scored_results.append(
            {
                "beat_index": beat_idx,
                "keyframe_url": kf.get("keyframe_url", image_path),
                "scores": {
                    **dimension_scores,
                    "composite": composite,
                },
                "retry_count": retry_count,
                "pssl_params": pssl_params,
            }
        )

    return scored_results


# ---------------------------------------------------------------------------
# Stage 2: Verdict Emission
# ---------------------------------------------------------------------------


def emit_verdicts(
    scored_results: list[dict],
    gate_config: dict | None = None,
) -> dict:
    """
    FR-VID-04 §4 Stage 2: Compare each beat's composite score to threshold,
    emit per-beat verdicts as DEP-VID-012.

    Args:
        scored_results: Output from score_keyframes().
        gate_config: DEP-VID-013 configuration.

    Returns:
        DEP-VID-012 compliant dict.
    """
    config = gate_config or DEFAULT_GATE_CONFIG
    threshold = config.get("threshold", 0.6)
    max_retries = config.get("max_retries", 2)
    project_id = config.get("project_id", "unknown")

    results = []
    approved_count = 0
    regenerate_count = 0
    manual_review_count = 0
    total_composite = 0.0

    for sr in scored_results:
        if sr.get("verdict") == "QUALITY_GATE_UNAVAILABLE":
            results.append(sr)
            continue

        composite = sr["scores"]["composite"]
        retry_count = sr.get("retry_count", 0)
        pssl_params = sr.pop("pssl_params", None)
        operator_override = sr.get("operator_override", False)

        verdict = determine_verdict(
            composite, threshold, retry_count, max_retries, operator_override
        )

        dimension_scores_only = {
            k: v for k, v in sr["scores"].items() if k != "composite"
        }
        feedback = generate_feedback(dimension_scores_only, verdict, pssl_params)

        sr["verdict"] = verdict
        sr["feedback"] = feedback

        if verdict == "APPROVED":
            approved_count += 1
        elif verdict == "REGENERATE":
            regenerate_count += 1
        elif verdict == "MANUAL_REVIEW":
            manual_review_count += 1

        total_composite += composite
        results.append(sr)

    total_scored = len(results)

    return {
        "gate_batch_id": f"QG-T2I-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
        "project_id": project_id,
        "threshold": threshold,
        "results": results,
        "batch_summary": {
            "total_scored": total_scored,
            "approved": approved_count,
            "regenerate": regenerate_count,
            "manual_review": manual_review_count,
            "average_composite": round(total_composite / total_scored, 2)
            if total_scored > 0
            else 0.0,
        },
    }


# ---------------------------------------------------------------------------
# Orchestrator — Full Quality Gate Pipeline
# ---------------------------------------------------------------------------


def run_quality_gate(
    keyframes: list[dict],
    visual_prompts: list[dict],
    gate_config: dict | None = None,
    clip_model: Any = None,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: str = "./receipts",
) -> tuple[dict, dict]:
    """
    FR-VID-04 full pipeline: score keyframes → emit verdicts → write receipts.

    Returns:
        (dep_vid_012, last_receipt) — the quality score result and the final receipt.
    """
    config = gate_config or DEFAULT_GATE_CONFIG

    # Stage 1: Keyframe Scoring
    scored_results = score_keyframes(keyframes, visual_prompts, config, clip_model)

    receipt_1 = write_receipt(
        stage_name="T2I_QUALITY_SCORING",
        agent_name="t2i_quality_gate",
        input_payload={"keyframes": keyframes, "visual_prompts": visual_prompts},
        output_payload=scored_results,
        previous_receipt=previous_receipt,
        output_dir=receipt_output_dir,
    )

    # Stage 2: Verdict Emission
    dep_vid_012 = emit_verdicts(scored_results, config)

    receipt_2 = write_receipt(
        stage_name="T2I_QUALITY_VERDICT",
        agent_name="t2i_quality_gate",
        input_payload=scored_results,
        output_payload=dep_vid_012,
        previous_receipt=receipt_1,
        output_dir=receipt_output_dir,
    )

    return dep_vid_012, receipt_2
