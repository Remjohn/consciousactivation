"""
Timeline Generator — Asset Resolution & Remotion Manifest Assembly

FR-VID-01 §4 Stages 2-3: Asset URL Resolution + Audio Overlay + Manifest Assembly

Resolves video clip and fallback image URLs from the Beat Fingerprint Map
(DEP-VID-014), embeds the audio layer (voiceover, music, ducking curve from
FR-VID-06), and assembles the complete Remotion Video Manifest (DEP-VID-002).

Technical Decision 4: Manifest is declarative, not imperative.
Technical Decision 5: Partial update for regeneration — only affected beats change.
"""

import re
from datetime import datetime, timezone
from typing import Any, Optional

try:
    from .receipt_chain import write_receipt
    from .scene_intelligence_loader import load_compiled_scene_intelligence_runtime_asset
    from .subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset
    from .subsystem_decisions import (
        apply_cognitive_rhythm_validator_decision as _apply_cognitive_rhythm_validator_rules_decision,
        apply_rhythm_generator_decision as _apply_rhythm_generator_rules_decision,
        apply_scene_type_selector_decision as _apply_scene_type_selector_rules_decision,
        apply_shot_duration_enforcer_decision as _apply_shot_duration_rules_decision,
    )
    from .legitimacy_runner import (
        build_scene_legitimacy_context,
        run_legitimacy_check,
    )
except ImportError:
    from receipt_chain import write_receipt
    from scene_intelligence_loader import load_compiled_scene_intelligence_runtime_asset
    from subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset
    from subsystem_decisions import (
        apply_cognitive_rhythm_validator_decision as _apply_cognitive_rhythm_validator_rules_decision,
        apply_rhythm_generator_decision as _apply_rhythm_generator_rules_decision,
        apply_scene_type_selector_decision as _apply_scene_type_selector_rules_decision,
        apply_shot_duration_enforcer_decision as _apply_shot_duration_rules_decision,
    )
    from legitimacy_runner import (
        build_scene_legitimacy_context,
        run_legitimacy_check,
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HTTPS_URL_PATTERN = re.compile(r"^https://")
VALID_ASSET_STATUSES = {"RESOLVED", "ASSET_MISSING", "KEN_BURNS_FALLBACK"}

FOCUS_SCENE_ALIASES = {
    "TURNING_POINT": {"TURNING_POINT", "CLIMAX", "TENSION", "RISING_ACTION"},
    "VISION": {"VISION", "RESOLUTION", "ENDING", "OUTRO", "CLIMAX"},
}



def _decision_verdict_from_package(package: dict, violations: list[dict]) -> str:
    if not violations:
        return "PASS"
    return package.get("enforcement", {}).get("default_result", "REVISE")


def _condition_triggered(metric_value: Any, operator: str, expected: Any) -> bool:
    if operator == "lt":
        return float(metric_value) < float(expected)
    if operator == "gt":
        return float(metric_value) > float(expected)
    if operator == "outside_range":
        return float(metric_value) < float(expected["min"]) or float(metric_value) > float(expected["max"])
    if operator == "eq":
        return metric_value == expected
    return False


def _evaluate_rules(rules: dict, metric_values: dict[str, Any], key: str) -> list[dict]:
    evaluations = []
    for condition in rules.get(key, []):
        metric = condition.get("metric")
        if metric not in metric_values:
            continue
        triggered = _condition_triggered(metric_values[metric], condition.get("operator", "eq"), condition.get("value"))
        when_condition = condition.get("when")
        if triggered and when_condition:
            when_metric = when_condition.get("metric")
            if when_metric not in metric_values:
                triggered = False
            else:
                triggered = _condition_triggered(
                    metric_values[when_metric],
                    when_condition.get("operator", "eq"),
                    when_condition.get("value"),
                )
        evaluations.append(
            {
                "metric": metric,
                "value": metric_values[metric],
                "operator": condition.get("operator"),
                "threshold": condition.get("value"),
                "triggered": triggered,
            }
        )
    return evaluations


def _resolve_per_beat_value(raw_value: Any, beat_index: int, default: float) -> float:
    if isinstance(raw_value, dict):
        candidate = raw_value.get(beat_index, raw_value.get(str(beat_index), default))
        return float(candidate)
    if raw_value is None:
        return float(default)
    return float(raw_value)


def _build_beat_timing_index(parsed_result: dict, key: str) -> dict[int, float]:
    """Build a beat_index -> value lookup from parsed_result["beat_audio_timing"] list."""
    index: dict[int, float] = {}
    for entry in parsed_result.get("beat_audio_timing", []):
        bi = entry.get("beat_index")
        val = entry.get(key)
        if bi is not None and val is not None:
            index[int(bi)] = float(val)
    return index


def _collect_audio_profiles(manifest: dict, scene_intelligence_runtime: Optional[dict]) -> list[dict]:
    if not scene_intelligence_runtime:
        return []
    component_map = scene_intelligence_runtime.get("components", {})
    profiles = []
    for beat in manifest.get("beats", []):
        component_id = beat.get("selected_component")
        component_package = component_map.get(component_id, {})
        audio_profile = component_package.get("spec", {}).get("audio_profile", {})
        if not audio_profile:
            continue
        profiles.append(
            {
                "beat_index": beat.get("beat_index"),
                "arc_stage": str(beat.get("arc_stage", "")).upper(),
                "component_id": component_id,
                "audio_profile": audio_profile,
            }
        )
    return profiles


def _ideal_audio_preload(audio_profile: dict) -> float:
    score_role = audio_profile.get("score_role")
    if score_role in {"peak", "punctuate", "destabilize"}:
        return 180.0
    if score_role in {"suspend", "recall", "land"}:
        return 260.0
    return 220.0


def _ideal_av_sync_offset(audio_profile: dict) -> float:
    score_role = audio_profile.get("score_role")
    if score_role in {"peak", "punctuate", "destabilize"}:
        return 18.0
    if score_role in {"clarify", "authenticate", "ground"}:
        return 42.0
    return 30.0


def _ideal_binding_offset(audio_profile: dict) -> float:
    prosodic_hint = audio_profile.get("prosodic_hint", "")
    if "clipped" in prosodic_hint or "syncopated" in prosodic_hint:
        return 28.0
    if "stepwise" in prosodic_hint or "precise" in prosodic_hint:
        return 55.0
    return 70.0


def _alignment_score(actual: float, ideal: float, tolerance: float) -> float:
    return max(0.0, min(1.0, 1.0 - (abs(actual - ideal) / tolerance)))


def _apply_audio_primer_decision(
    parsed_result: dict,
    manifest: dict,
    subsystem_runtime: dict,
    scene_intelligence_runtime: Optional[dict] = None,
) -> dict:
    package = subsystem_runtime["packages"].get("CS-010", {})
    rules = package.get("rules", {})
    profiles = _collect_audio_profiles(manifest, scene_intelligence_runtime)
    evaluations = []
    triggered_rules = []
    congruence_scores = []
    timing_index = _build_beat_timing_index(parsed_result, "audio_preload_ms")
    preload_source = parsed_result.get("audio_preload_ms")
    real_timing_used = False

    for profile_entry in profiles:
        beat_index = profile_entry["beat_index"]
        ideal_preload = _ideal_audio_preload(profile_entry["audio_profile"])
        if beat_index in timing_index:
            actual_preload = timing_index[beat_index]
            timing_source = "measured"
            real_timing_used = True
        else:
            actual_preload = _resolve_per_beat_value(preload_source, beat_index, ideal_preload)
            timing_source = "profile_derived"
        congruence = round(_alignment_score(actual_preload, ideal_preload, 220.0), 3)
        congruence_scores.append(congruence)
        metric_values = {"audio_preload_ms": actual_preload}
        rule_evals = _evaluate_rules(rules, metric_values, "warn_conditions")
        triggered_rules.extend([entry for entry in rule_evals if entry["triggered"]])
        evaluations.append(
            {
                "beat_index": beat_index,
                "component_id": profile_entry["component_id"],
                "score_role": profile_entry["audio_profile"].get("score_role"),
                "mode": profile_entry["audio_profile"].get("mode"),
                "ideal_preload_ms": round(ideal_preload, 1),
                "audio_preload_ms": round(actual_preload, 1),
                "congruence_score": congruence,
                "timing_source": timing_source,
            }
        )

    integrity_score = round(sum(congruence_scores) / len(congruence_scores), 3) if congruence_scores else 1.0
    evaluation_mode = "beat_audio_timing" if real_timing_used else "profile_derived"
    return {
        "subsystem_id": "CS-010",
        "verdict": _decision_verdict_from_package(package, triggered_rules),
        "integrity_score": integrity_score,
        "evaluation_mode": evaluation_mode,
        "route_hints": rules.get("route_hints", {}).get("prime", []),
        "beat_evaluations": evaluations,
        "triggered_rules": triggered_rules,
    }


def _apply_av_sync_decision(
    parsed_result: dict,
    manifest: dict,
    subsystem_runtime: dict,
    scene_intelligence_runtime: Optional[dict] = None,
) -> dict:
    package = subsystem_runtime["packages"].get("CS-022", {})
    rules = package.get("rules", {})
    profiles = _collect_audio_profiles(manifest, scene_intelligence_runtime)
    evaluations = []
    triggered_rules = []
    offsets = []
    timing_index = _build_beat_timing_index(parsed_result, "audio_visual_event_offset_ms")
    offset_source = parsed_result.get("audio_visual_event_offset_ms")
    real_timing_used = False

    for profile_entry in profiles:
        beat_index = profile_entry["beat_index"]
        ideal_offset = _ideal_av_sync_offset(profile_entry["audio_profile"])
        if beat_index in timing_index:
            actual_offset = timing_index[beat_index]
            timing_source = "measured"
            real_timing_used = True
        else:
            actual_offset = _resolve_per_beat_value(offset_source, beat_index, ideal_offset)
            timing_source = "profile_derived"
        sync_score = round(_alignment_score(actual_offset, ideal_offset, 120.0), 3)
        offsets.append(sync_score)
        metric_values = {"timing_offset_ms": actual_offset}
        rule_evals = _evaluate_rules(rules, metric_values, "warn_conditions")
        triggered_rules.extend([entry for entry in rule_evals if entry["triggered"]])
        evaluations.append(
            {
                "beat_index": beat_index,
                "component_id": profile_entry["component_id"],
                "energy_band": profile_entry["audio_profile"].get("energy_band"),
                "ideal_offset_ms": round(ideal_offset, 1),
                "timing_offset_ms": round(actual_offset, 1),
                "sync_score": sync_score,
                "timing_source": timing_source,
            }
        )

    integrity_score = round(sum(offsets) / len(offsets), 3) if offsets else 1.0
    evaluation_mode = "beat_audio_timing" if real_timing_used else "profile_derived"
    return {
        "subsystem_id": "CS-022",
        "verdict": _decision_verdict_from_package(package, triggered_rules),
        "integrity_score": integrity_score,
        "evaluation_mode": evaluation_mode,
        "route_hints": rules.get("route_hints", {}).get("correct", []),
        "beat_evaluations": evaluations,
        "triggered_rules": triggered_rules,
    }


def _apply_temporal_binding_decision(
    parsed_result: dict,
    manifest: dict,
    subsystem_runtime: dict,
    scene_intelligence_runtime: Optional[dict] = None,
) -> dict:
    package = subsystem_runtime["packages"].get("CS-027", {})
    rules = package.get("rules", {})
    profiles = _collect_audio_profiles(manifest, scene_intelligence_runtime)
    evaluations = []
    triggered_rules = []
    block_rules = []
    binding_scores = []
    timing_index = _build_beat_timing_index(parsed_result, "phonetic_visual_offset_ms")
    offset_source = parsed_result.get("phonetic_visual_offset_ms")
    real_timing_used = False

    for profile_entry in profiles:
        beat_index = profile_entry["beat_index"]
        ideal_offset = _ideal_binding_offset(profile_entry["audio_profile"])
        if beat_index in timing_index:
            actual_offset = timing_index[beat_index]
            timing_source = "measured"
            real_timing_used = True
        else:
            actual_offset = _resolve_per_beat_value(offset_source, beat_index, ideal_offset)
            timing_source = "profile_derived"
        binding_score = round(_alignment_score(actual_offset, ideal_offset, 180.0), 3)
        binding_scores.append(binding_score)
        metric_values = {"timing_offset_ms": actual_offset}
        warn_evals = _evaluate_rules(rules, metric_values, "warn_conditions")
        block_evals = _evaluate_rules(rules, metric_values, "block_conditions")
        triggered_rules.extend([entry for entry in warn_evals if entry["triggered"]])
        block_rules.extend([entry for entry in block_evals if entry["triggered"]])
        evaluations.append(
            {
                "beat_index": beat_index,
                "component_id": profile_entry["component_id"],
                "prosodic_hint": profile_entry["audio_profile"].get("prosodic_hint"),
                "ideal_offset_ms": round(ideal_offset, 1),
                "timing_offset_ms": round(actual_offset, 1),
                "binding_score": binding_score,
                "timing_source": timing_source,
            }
        )

    integrity_score = round(sum(binding_scores) / len(binding_scores), 3) if binding_scores else 1.0
    violations = block_rules or triggered_rules
    verdict = "BLOCK" if block_rules else _decision_verdict_from_package(package, violations)
    evaluation_mode = "beat_audio_timing" if real_timing_used else "profile_derived"
    return {
        "subsystem_id": "CS-027",
        "verdict": verdict,
        "integrity_score": integrity_score,
        "evaluation_mode": evaluation_mode,
        "route_hints": rules.get("route_hints", {}).get("preferred_fix", []),
        "beat_evaluations": evaluations,
        "triggered_rules": triggered_rules,
        "block_rules": block_rules,
    }


def _apply_schema_activation_decision(
    parsed_result: dict,
    manifest: dict,
    subsystem_runtime: dict,
) -> dict:
    package = subsystem_runtime["packages"].get("CS-034", {})
    rules = package.get("rules", {})

    beats = manifest.get("beats", [])
    total_beats = len(beats) or 1

    ORIENTATION_STAGES = {"HOOK", "SETUP", "OPENING"}
    VIOLATION_STAGES = {"TURNING_POINT", "CLIMAX", "JUXTAPOSITION"}
    BOUNDARY_STAGES = {"HOOK", "TURNING_POINT", "CLIMAX", "RESOLUTION", "VISION"}

    first_half = beats[: max(1, total_beats // 2)]
    orientation_count = sum(
        1 for b in first_half
        if str(b.get("arc_stage", "")).upper() in ORIENTATION_STAGES
    )
    violation_count = sum(
        1 for b in first_half
        if str(b.get("arc_stage", "")).upper() in VIOLATION_STAGES
    )
    denom = orientation_count + violation_count
    schema_activation_score = round(
        (orientation_count + 0.1) / max(denom + 0.1, 0.2), 3
    ) if denom > 0 else 0.5

    boundary_count = sum(
        1 for b in beats
        if str(b.get("arc_stage", "")).upper() in BOUNDARY_STAGES
        or b.get("selected_component") == "ZEIGARNIK_LOOP"
    )
    boundary_density_per_beat = round(boundary_count / total_beats, 3)

    metric_values = {
        "schema_activation_score": schema_activation_score,
        "boundary_density_per_beat": boundary_density_per_beat,
    }
    warn_evals = _evaluate_rules(rules, metric_values, "warn_conditions")
    block_evals = _evaluate_rules(rules, metric_values, "block_conditions")
    triggered_warns = [e for e in warn_evals if e["triggered"]]
    triggered_blocks = [e for e in block_evals if e["triggered"]]

    if triggered_blocks:
        verdict = "BLOCK"
        segmentation_advice = (
            rules.get("route_hints", {}).get("establish_schema", [])
            + rules.get("route_hints", {}).get("reduce_density", [])
        )
    elif triggered_warns:
        verdict = _decision_verdict_from_package(package, triggered_warns)
        segmentation_advice = (
            (rules.get("route_hints", {}).get("establish_schema", [])
             if any(e["metric"] == "schema_activation_score" for e in triggered_warns) else [])
            + (rules.get("route_hints", {}).get("reduce_density", [])
               if any(e["metric"] == "boundary_density_per_beat" for e in triggered_warns) else [])
        )
    else:
        verdict = "PASS"
        segmentation_advice = []

    violation_timing_list = [
        b.get("beat_index") for b in first_half
        if str(b.get("arc_stage", "")).upper() in VIOLATION_STAGES
    ]

    return {
        "subsystem_id": "CS-034",
        "verdict": verdict,
        "schema_activation_score": schema_activation_score,
        "boundary_density_per_beat": boundary_density_per_beat,
        "boundary_density_verdict": verdict,
        "segmentation_advice": segmentation_advice,
        "violation_timing_list": violation_timing_list,
        "triggered_warns": triggered_warns,
        "triggered_blocks": triggered_blocks,
    }


def _apply_peak_end_budget_decision(manifest: dict, subsystem_runtime: dict) -> dict:
    cs011 = subsystem_runtime["packages"].get("CS-011", {})
    thresholds = cs011.get("thresholds", {})
    focus_scenes = thresholds.get("default_focus_scenes", ["TURNING_POINT", "VISION"])
    multiplier = thresholds.get("peak_end_budget_multiplier", 2.0)

    boosted_indices = []
    for beat in manifest.get("beats", []):
        arc_stage = str(beat.get("arc_stage", "")).upper()
        should_boost = arc_stage in focus_scenes
        if not should_boost:
            for focus_scene in focus_scenes:
                aliases = FOCUS_SCENE_ALIASES.get(focus_scene, set())
                if arc_stage in aliases:
                    should_boost = True
                    break

        if should_boost:
            beat["effect_budget_multiplier"] = multiplier
            beat["memory_priority"] = "PEAK_END"
            boosted_indices.append(beat.get("beat_index"))

    if not boosted_indices and manifest.get("beats"):
        final_beat = manifest["beats"][-1]
        final_beat["effect_budget_multiplier"] = multiplier
        final_beat["memory_priority"] = "PEAK_END"
        boosted_indices.append(final_beat.get("beat_index"))

    return {
        "subsystem_id": "CS-011",
        "focus_scenes": focus_scenes,
        "budget_multiplier": multiplier,
        "boosted_beat_indices": boosted_indices,
    }


def _compute_isc_quality_decision(manifest: dict, constraint_manifest: dict, subsystem_runtime: dict) -> dict:
    cs029 = subsystem_runtime["packages"].get("CS-029", {})
    thresholds = cs029.get("thresholds", {})
    publish_ready_score = thresholds.get("publish_ready_score", 80)
    revise_score_min = thresholds.get("revise_score_min", 65)

    beats = manifest.get("beats", [])
    total_beats = len(beats) or 1
    resolved_count = sum(1 for beat in beats if beat.get("asset_status") == "RESOLVED")
    peak_end_count = sum(1 for beat in beats if beat.get("memory_priority") == "PEAK_END")
    asset_completeness = resolved_count / total_beats
    peak_end_focus = min(
        1.0,
        peak_end_count / max(1, sum(1 for beat in beats if str(beat.get("arc_stage", "")).upper() in {"TURNING_POINT", "VISION"})),
    )
    legitimacy_score = 1.0 if constraint_manifest.get("decision") == "PASS" else 0.8 if constraint_manifest.get("decision") == "REVISE" else 0.0
    audio_integrity_scores = []
    for decision_key in ("audio_primer", "av_sync", "temporal_binding"):
        decision = manifest.get("assembly_decisions", {}).get(decision_key, {})
        if "integrity_score" in decision:
            audio_integrity_scores.append(float(decision["integrity_score"]))
    if audio_integrity_scores:
        audio_sync_integrity = sum(audio_integrity_scores) / len(audio_integrity_scores)
    else:
        audio_sync_integrity = 1.0 if len(manifest.get("audio", {}).get("ducking_curve", [])) == manifest.get("total_frames", 0) else 0.0

    factors = {
        "structure_legitimacy": legitimacy_score * 100,
        "asset_completeness": asset_completeness * 100,
        "peak_end_focus": peak_end_focus * 100,
        "audio_timing_integrity": audio_sync_integrity * 100,
    }
    score = round(
        factors["structure_legitimacy"] * 0.35
        + factors["asset_completeness"] * 0.25
        + factors["peak_end_focus"] * 0.20
        + factors["audio_timing_integrity"] * 0.20,
        2,
    )
    weakest_dimensions = [
        name for name, value in factors.items() if value < 100
    ]

    verdict = "PUBLISH_READY"
    if score < publish_ready_score:
        verdict = "REVISE"
    if score < revise_score_min:
        verdict = "HIGH_RISK"

    return {
        "subsystem_id": "CS-029",
        "score": score,
        "verdict": verdict,
        "publish_ready_threshold": publish_ready_score,
        "weakest_dimensions": weakest_dimensions,
        "factor_breakdown": factors,
    }


def _apply_cta_fusion_decision(parsed_result: dict, manifest: dict, subsystem_runtime: dict) -> dict:
    cs012 = subsystem_runtime["packages"].get("CS-012", {})
    thresholds = cs012.get("thresholds", {})
    max_gap = thresholds.get("max_cta_gap_seconds", 3.0)

    final_beat = manifest.get("beats", [])[-1] if manifest.get("beats") else {}
    fps = manifest.get("fps", 24)
    final_beat_start_sec = final_beat.get("start_frame", 0) / fps if fps else 0.0
    final_beat_duration_sec = final_beat.get("duration_sec", 0.0)
    end_state_start_sec = parsed_result.get("end_state_start_sec", final_beat_start_sec)
    cta_start_sec = parsed_result.get("cta_start_sec", end_state_start_sec)
    cta_duration_sec = parsed_result.get("cta_duration_sec", min(max_gap, max(1.0, final_beat_duration_sec)))
    detached_outro = bool(parsed_result.get("detached_outro", False))
    gap_duration = max(0.0, round(cta_start_sec - end_state_start_sec, 3))

    verdict = "PASS"
    if detached_outro or gap_duration > max_gap:
        verdict = "REVISE"

    call_to_action = {
        "text": parsed_result.get("cta_text"),
        "start_sec": cta_start_sec,
        "duration_sec": cta_duration_sec,
        "fused_with_end_state": verdict == "PASS",
    }
    manifest["call_to_action"] = call_to_action

    return {
        "subsystem_id": "CS-012",
        "verdict": verdict,
        "max_gap_seconds": max_gap,
        "end_state_start_sec": end_state_start_sec,
        "cta_start_sec": cta_start_sec,
        "gap_duration_seconds": gap_duration,
        "detached_outro": detached_outro,
        "call_to_action": call_to_action,
    }


def _apply_scene_type_selector_decision(
    parsed_result: dict,
    manifest: dict,
    subsystem_runtime: dict,
    scene_intelligence_runtime: Optional[dict] = None,
) -> dict:
    return _apply_scene_type_selector_rules_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
        scene_intelligence_runtime,
    )


def _apply_rhythm_generator_decision(manifest: dict, subsystem_runtime: dict) -> dict:
    return _apply_rhythm_generator_rules_decision(manifest.get("beats", []), subsystem_runtime)


def _apply_shot_duration_enforcer_decision(manifest: dict, subsystem_runtime: dict) -> dict:
    return _apply_shot_duration_rules_decision(manifest.get("beats", []), subsystem_runtime)


def _apply_cognitive_rhythm_validator_decision(
    manifest: dict,
    scene_intelligence_runtime: Optional[dict] = None,
) -> dict:
    return _apply_cognitive_rhythm_validator_rules_decision(
        manifest.get("beats", []),
        scene_intelligence_runtime,
    )


# ---------------------------------------------------------------------------
# URL Sanitization — §11 Safety Test
# ---------------------------------------------------------------------------


def sanitize_url(url: Optional[str]) -> Optional[str]:
    """
    Reject non-HTTPS URLs to prevent XSS/SSRF.

    FR-VID-01 §11: Reject javascript: URIs and non-HTTPS URLs.
    Returns None for invalid URLs.
    """
    if url is None or not url.strip():
        return None
    url = url.strip()
    if HTTPS_URL_PATTERN.match(url):
        return url
    return None


# ---------------------------------------------------------------------------
# Stage 2: Asset URL Resolution
# ---------------------------------------------------------------------------


def resolve_asset_urls(
    canonical_beats: list[dict],
    fingerprint_map: Optional[dict] = None,
) -> list[dict]:
    """
    Resolve asset URLs for each beat from the fingerprint map.

    FR-VID-01 §4 Stage 2:
    - video_clip_url from fingerprint.stage_2_i2v.output_video_url
    - fallback_image_url from fingerprint.stage_1_t2i.output_image_url
    - ASSET_MISSING if both are null

    Returns list of asset-resolved beats.
    """
    # Build fingerprint lookup by beat_index
    fp_lookup = {}
    if fingerprint_map:
        for entry in fingerprint_map.get("fingerprints", []):
            fp_lookup[entry["beat_index"]] = entry

    resolved_beats = []
    for beat in canonical_beats:
        beat = dict(beat)
        beat_idx = beat["beat_index"]

        fp_entry = fp_lookup.get(beat_idx)

        video_url = None
        fallback_url = None
        fingerprint_id = None

        if fp_entry:
            fp = fp_entry.get("fingerprint", {})
            fingerprint_id = fp.get("fingerprint_id")

            i2v = fp.get("stage_2_i2v", {})
            if i2v.get("status") == "GENERATED":
                video_url = sanitize_url(i2v.get("output_video_url"))

            t2i = fp.get("stage_1_t2i", {})
            if t2i.get("status") == "GENERATED":
                fallback_url = sanitize_url(t2i.get("output_image_url"))

        beat["video_clip_url"] = video_url
        beat["fallback_image_url"] = fallback_url
        beat["fingerprint_id"] = fingerprint_id

        if video_url is None and fallback_url is None:
            beat["asset_status"] = "ASSET_MISSING"
        elif video_url is None and fallback_url is not None:
            beat["asset_status"] = "KEN_BURNS_FALLBACK"
        else:
            beat["asset_status"] = "RESOLVED"

        resolved_beats.append(beat)

    return resolved_beats


# ---------------------------------------------------------------------------
# Stage 3: Audio Overlay & Manifest Assembly
# ---------------------------------------------------------------------------


def validate_ducking_curve(
    ducking_curve: list[float],
    total_frames: int,
) -> tuple[bool, str]:
    """
    Validate ducking curve length matches total_frames.

    FR-VID-01 §4 Stage 3 Step 2: Mismatch → DUCKING_CURVE_MISMATCH.
    """
    if len(ducking_curve) != total_frames:
        return False, (
            f"DUCKING_CURVE_MISMATCH: curve has {len(ducking_curve)} values, "
            f"expected {total_frames} (total_frames)"
        )

    # Validate all values are 0.0-1.0
    for i, val in enumerate(ducking_curve):
        if not (0.0 <= val <= 1.0):
            return False, (
                f"DUCKING_CURVE_INVALID: value at index {i} is {val}, "
                f"must be between 0.0 and 1.0"
            )

    return True, ""


def assemble_manifest(
    parsed_result: dict,
    resolved_beats: list[dict],
    voiceover_path: Optional[str] = None,
    music_path: Optional[str] = None,
    ducking_curve: Optional[list[float]] = None,
    ducking_target_db: int = -18,
    music_fade_out_frames: int = 48,
    width: int = 1080,
    height: int = 1920,
    aspect_ratio: str = "9:16",
    manifest_id: Optional[str] = None,
) -> dict:
    """
    Assemble the complete Remotion Video Manifest (DEP-VID-002).

    FR-VID-01 §4 Stage 3: Audio overlay + composition metadata + final assembly.
    """
    fps = parsed_result.get("fps", 24)
    total_frames = parsed_result.get("total_frames", 0)
    total_duration = parsed_result.get("total_duration_sec", 0.0)

    # Determine overall manifest status
    has_missing = any(b.get("asset_status") == "ASSET_MISSING" for b in resolved_beats)
    status = "ASSEMBLED_WITH_GAPS" if has_missing else "ASSEMBLED"

    # Build audio section
    audio = {
        "voiceover_path": voiceover_path,
        "music_path": music_path,
        "ducking_curve": ducking_curve or [],
        "ducking_target_db": ducking_target_db,
        "music_start_frame": 0,
        "music_fade_out_frames": music_fade_out_frames,
    }

    if manifest_id is None:
        manifest_id = f"MAN-VID-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001"

    manifest = {
        "manifest_id": manifest_id,
        "project_id": parsed_result.get("project_id", ""),
        "beat_cluster_id": parsed_result.get("beat_cluster_id", ""),
        "arc_type": parsed_result.get("arc_type", ""),
        "composition_template": f"cmf-{parsed_result.get('arc_type', 'default')}",
        "fps": fps,
        "width": width,
        "height": height,
        "aspect_ratio": aspect_ratio,
        "total_frames": total_frames,
        "total_duration_sec": total_duration,
        "beats": resolved_beats,
        "audio": audio,
        "status": status,
        "warnings": parsed_result.get("warnings", []),
        "generation_timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return manifest


# ---------------------------------------------------------------------------
# Manifest Partial Update — §3 Technical Decision 5
# ---------------------------------------------------------------------------


def update_manifest_beats(
    manifest: dict,
    updated_fingerprint_entries: list[dict],
) -> dict:
    """
    Partial manifest update after regeneration.

    FR-VID-01 §3 TD5: Only affected beat entries are updated.
    Audio, composition metadata, and non-affected beats remain unchanged.
    """
    fp_lookup = {e["beat_index"]: e for e in updated_fingerprint_entries}

    for beat in manifest["beats"]:
        beat_idx = beat["beat_index"]
        if beat_idx not in fp_lookup:
            continue

        fp = fp_lookup[beat_idx].get("fingerprint", {})
        i2v = fp.get("stage_2_i2v", {})
        t2i = fp.get("stage_1_t2i", {})

        video_url = sanitize_url(i2v.get("output_video_url")) if i2v.get("status") == "GENERATED" else None
        fallback_url = sanitize_url(t2i.get("output_image_url")) if t2i.get("status") == "GENERATED" else None

        beat["video_clip_url"] = video_url
        beat["fallback_image_url"] = fallback_url
        beat["fingerprint_id"] = fp.get("fingerprint_id")

        if video_url is None and fallback_url is None:
            beat["asset_status"] = "ASSET_MISSING"
        elif video_url is None:
            beat["asset_status"] = "KEN_BURNS_FALLBACK"
        else:
            beat["asset_status"] = "RESOLVED"

    # Update timestamp and status
    has_missing = any(b.get("asset_status") == "ASSET_MISSING" for b in manifest["beats"])
    manifest["status"] = "ASSEMBLED_WITH_GAPS" if has_missing else "ASSEMBLED"
    manifest["generation_timestamp"] = datetime.now(timezone.utc).isoformat()

    return manifest


# ---------------------------------------------------------------------------
# Pipeline Entry Points with Receipts
# ---------------------------------------------------------------------------


def run_asset_resolution(
    canonical_beats: list[dict],
    fingerprint_map: Optional[dict] = None,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[list[dict], dict]:
    """
    Run asset resolution stage with receipt chain.

    Returns:
        (resolved_beats, receipt)
    """
    resolved = resolve_asset_urls(canonical_beats, fingerprint_map)

    output_dir = receipt_output_dir or "."
    receipt = write_receipt(
        stage_name="ASSET_RESOLUTION",
        agent_name="timeline_generator",
        input_payload={"beat_count": len(canonical_beats)},
        output_payload={"resolved_count": len(resolved)},
        previous_receipt=previous_receipt,
        output_dir=output_dir,
    )

    return resolved, receipt


def run_manifest_assembly(
    parsed_result: dict,
    resolved_beats: list[dict],
    voiceover_path: Optional[str] = None,
    music_path: Optional[str] = None,
    ducking_curve: Optional[list[float]] = None,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
    **kwargs,
) -> tuple[dict, dict]:
    """
    Run manifest assembly stage with receipt chain.

    Returns:
        (manifest, receipt)
    """
    subsystem_runtime = load_compiled_subsystem_runtime_asset(
        "scene_builder",
        STAGE_SUBSYSTEM_ID_MAP["scene_builder"],
    )
    scene_intelligence_runtime = load_compiled_scene_intelligence_runtime_asset("scene_builder")
    manifest = assemble_manifest(
        parsed_result, resolved_beats,
        voiceover_path=voiceover_path,
        music_path=music_path,
        ducking_curve=ducking_curve,
        **kwargs,
    )

    output_dir = receipt_output_dir or "."
    legitimacy_context, legitimacy_target_ref, project_id = build_scene_legitimacy_context(
        parsed_result,
        resolved_beats,
        manifest_candidate=manifest,
    )
    constraint_manifest, legitimacy_receipt = run_legitimacy_check(
        compile_target="SCENE_BUILDER",
        project_id=project_id,
        target_ref=legitimacy_target_ref,
        context=legitimacy_context,
        previous_receipt=previous_receipt,
        receipt_output_dir=output_dir,
    )
    if constraint_manifest["decision"] == "BLOCK":
        raise ValueError(
            "SCENE_LEGITIMACY_BLOCKED: "
            + "; ".join(constraint_manifest.get("required_actions", []))
        )

    manifest["constraint_manifest"] = {
        "constraint_manifest_id": constraint_manifest["constraint_manifest_id"],
        "decision": constraint_manifest["decision"],
        "path": next(
            output["path"]
            for output in constraint_manifest["output_files"]
            if output["kind"] == "constraint_manifest"
        ),
    }
    manifest["subsystem_runtime_asset"] = {
        "asset_id": subsystem_runtime["asset_id"],
        "path": subsystem_runtime["asset_path"],
        "active_subsystems": subsystem_runtime["active_subsystems"],
    }
    manifest["scene_intelligence_runtime_asset"] = {
        "asset_id": scene_intelligence_runtime["asset_id"],
        "path": scene_intelligence_runtime["asset_path"],
        "active_containers": scene_intelligence_runtime["active_containers"],
        "active_components": scene_intelligence_runtime["active_components"],
    }
    manifest.setdefault("assembly_decisions", {})
    manifest["assembly_decisions"]["scene_type_selector"] = _apply_scene_type_selector_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
        scene_intelligence_runtime,
    )
    manifest["assembly_decisions"]["audio_primer"] = _apply_audio_primer_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
        scene_intelligence_runtime,
    )
    manifest["assembly_decisions"]["av_sync"] = _apply_av_sync_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
        scene_intelligence_runtime,
    )
    manifest["assembly_decisions"]["temporal_binding"] = _apply_temporal_binding_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
        scene_intelligence_runtime,
    )
    manifest["assembly_decisions"]["schema_activation"] = _apply_schema_activation_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
    )
    manifest["assembly_decisions"]["rhythm_generator"] = _apply_rhythm_generator_decision(
        manifest,
        subsystem_runtime,
    )
    manifest["assembly_decisions"]["shot_duration"] = _apply_shot_duration_enforcer_decision(
        manifest,
        subsystem_runtime,
    )
    manifest["assembly_decisions"]["peak_end_budget"] = _apply_peak_end_budget_decision(
        manifest,
        subsystem_runtime,
    )
    manifest["assembly_decisions"]["cognitive_rhythm_validator"] = _apply_cognitive_rhythm_validator_decision(
        manifest,
        scene_intelligence_runtime,
    )
    manifest["assembly_decisions"]["cta_fusion"] = _apply_cta_fusion_decision(
        parsed_result,
        manifest,
        subsystem_runtime,
    )
    manifest["assembly_decisions"]["isc_quality"] = _compute_isc_quality_decision(
        manifest,
        constraint_manifest,
        subsystem_runtime,
    )
    receipt = write_receipt(
        stage_name="MANIFEST_ASSEMBLY",
        agent_name="timeline_generator",
        input_payload={"beat_count": len(resolved_beats)},
        output_payload=manifest,
        previous_receipt=legitimacy_receipt,
        output_dir=output_dir,
    )

    return manifest, receipt
