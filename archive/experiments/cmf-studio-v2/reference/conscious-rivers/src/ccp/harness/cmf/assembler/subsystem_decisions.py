from __future__ import annotations

from typing import Any


SCENE_TYPE_VEHICLE_MAP = {
    "OPENING": "OUT_OF_CONTEXT_TALKING_HEAD",
    "HOOK": "OUT_OF_CONTEXT_TALKING_HEAD",
    "RISING_ACTION": "EVIDENCE_ESCALATION",
    "SETUP": "CONFESSIONAL_SETUP",
    "CHALLENGE": "PROOF_CONFRONTATION",
    "TENSION": "PROOF_CONFRONTATION",
    "TURNING_POINT": "REVELATION_PAYOFF",
    "CLIMAX": "REVELATION_PAYOFF",
    "RESOLUTION": "RELEASE_INTEGRATION",
    "VISION": "FUTURE_SELF_IMAGE",
    "ENDING": "FUTURE_SELF_IMAGE",
    "OUTRO": "FUTURE_SELF_IMAGE",
}

FALLBACK_CONTAINER_ID = "CHALLENGE"

PREDICTION_ERROR_COMPONENT_SCORES = {
    "HOOK": 0.85,
    "THE_TEASE": 0.74,
    "THE_VIBE": 0.28,
    "JUXTAPOSITION": 0.95,
    "ZEIGARNIK_LOOP": 0.88,
    "SETUP": 0.22,
    "CHALLENGE": 0.62,
    "FRAME_AND_CONTRAST": 0.71,
    "DEMONSTRATION": 0.42,
    "THE_EVIDENCE": 0.33,
    "THE_COMMUNITY": 0.41,
    "TURNING_POINT": 1.0,
    "VOICE_OF_TRUTH": 0.54,
    "ARCHETYPAL_MOMENT": 0.78,
    "SYMBOLIC_ECHO": 0.24,
    "ENCOURAGING_CHANGE": 0.34,
    "RESOLUTION": 0.18,
    "THE_PAUSE": 0.08,
    "THE_VISION": 0.46,
}

TRANSPORTATION_PHASE_COMPONENT_MAP = {
    "admission": {"HOOK", "THE_TEASE", "JUXTAPOSITION", "ZEIGARNIK_LOOP"},
    "orientation": {"SETUP", "VOICE_OF_TRUTH", "THE_VIBE", "ARCHETYPAL_MOMENT"},
    "immersion": {"CHALLENGE", "FRAME_AND_CONTRAST", "THE_EVIDENCE", "DEMONSTRATION", "THE_VIBE", "ZEIGARNIK_LOOP"},
    "rupture": {"TURNING_POINT", "JUXTAPOSITION", "ARCHETYPAL_MOMENT", "VOICE_OF_TRUTH"},
    "consolidation": {"RESOLUTION", "SYMBOLIC_ECHO", "THE_PAUSE", "ENCOURAGING_CHANGE"},
    "prospection": {"THE_VISION", "THE_COMMUNITY", "ENCOURAGING_CHANGE", "THE_VIBE", "ARCHETYPAL_MOMENT"},
}

SURPRISE_REDUCTION_KEYWORDS = (
    "clearer",
    "cleaner",
    "simpler",
    "safer",
    "smoother",
    "less intense",
    "reduce contrast",
    "less dramatic",
)

SURPRISE_AMPLIFICATION_KEYWORDS = (
    "more dramatic",
    "more surprising",
    "harder contrast",
    "shock",
    "punchier",
    "bigger reveal",
    "stronger twist",
)

# Per-container audio archetype affinity for CS-031 tiebreak scoring
CONTAINER_AUDIO_AFFINITY: dict[str, dict[str, set]] = {
    "HOOK": {
        "score_roles": {"punctuate", "destabilize", "withhold"},
        "energy_bands": {"high", "medium_high"},
        "modes": {"tense", "confrontational", "suspense"},
    },
    "SETUP": {
        "score_roles": {"ground", "clarify", "atmosphere"},
        "energy_bands": {"low", "low_medium"},
        "modes": {"intimate", "immersive", "procedural"},
    },
    "CHALLENGE": {
        "score_roles": {"escalate", "destabilize", "polarize"},
        "energy_bands": {"medium_high", "high"},
        "modes": {"confrontational", "tense", "adversarial"},
    },
    "TURNING_POINT": {
        "score_roles": {"peak", "mythologize", "suspend"},
        "energy_bands": {"high", "medium_high", "medium"},
        "modes": {"revelatory", "transcendent", "mythic"},
    },
    "RESOLUTION": {
        "score_roles": {"land", "recall", "reflect"},
        "energy_bands": {"low", "low_medium", "minimal"},
        "modes": {"relieved", "reflective", "near_silent", "contemplative"},
    },
    "VISION": {
        "score_roles": {"fuse_cta", "propel", "bond", "atmosphere"},
        "energy_bands": {"medium", "low_medium"},
        "modes": {"aspirational", "hopeful", "warm_collective", "immersive"},
    },
}


def _get_package(subsystem_runtime: dict[str, Any], subsystem_id: str) -> dict[str, Any]:
    return subsystem_runtime.get("packages", {}).get(subsystem_id, {})


def _get_rules(package: dict[str, Any]) -> dict[str, Any]:
    return package.get("rules", {})


def _find_warn_condition(package: dict[str, Any], metric: str) -> dict[str, Any]:
    for condition in _get_rules(package).get("warn_conditions", []):
        if condition.get("metric") == metric:
            return condition
    return {}


def _score_audio_profile_affinity(container_id: str, component_package: dict[str, Any]) -> float:
    """Return a small tiebreak bonus [0..0.18] based on audio_profile match with container archetype."""
    spec = component_package.get("spec", {})
    audio_profile = spec.get("audio_profile", {})
    if not audio_profile:
        return 0.0
    affinity = CONTAINER_AUDIO_AFFINITY.get(container_id, {})
    if not affinity:
        return 0.0
    bonus = 0.0
    if audio_profile.get("score_role") in affinity.get("score_roles", set()):
        bonus += 0.08
    if audio_profile.get("energy_band") in affinity.get("energy_bands", set()):
        bonus += 0.06
    if audio_profile.get("mode") in affinity.get("modes", set()):
        bonus += 0.04
    return round(min(0.18, bonus), 3)


def _evaluate_selection_conditions(
    component_rules: dict[str, Any],
    metric_context: dict[str, Any],
) -> str | None:
    """Evaluate selection_conditions and return the first matching variant, or None."""
    for condition in component_rules.get("selection_conditions", []):
        if_clause = condition.get("if", {})
        metric = if_clause.get("metric")
        if metric not in metric_context:
            continue
        if _condition_triggered(
            metric_context[metric],
            if_clause.get("operator", "eq"),
            if_clause.get("value"),
        ):
            return condition.get("then", {}).get("variant")
    return None


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


def _evaluate_rule(package: dict[str, Any], metric: str, metric_value: Any) -> dict[str, Any]:
    condition = _find_warn_condition(package, metric)
    if not condition:
        return {
            "metric": metric,
            "value": metric_value,
            "triggered": False,
        }

    triggered = _condition_triggered(metric_value, condition.get("operator", "eq"), condition.get("value"))
    return {
        "metric": metric,
        "value": metric_value,
        "operator": condition.get("operator"),
        "threshold": condition.get("value"),
        "triggered": triggered,
    }


def _decision_verdict(package: dict[str, Any], violations: list[dict[str, Any]]) -> str:
    if not violations:
        return "PASS"
    enforcement = package.get("enforcement", {})
    return enforcement.get("default_result") or package.get("default_action_on_fail", "REVISE")


def _evaluate_warn_conditions(rules: dict[str, Any], metric_values: dict[str, Any]) -> list[dict[str, Any]]:
    evaluations = []
    for condition in rules.get("warn_conditions", []):
        metric = condition.get("metric")
        if metric not in metric_values:
            continue
        evaluations.append(
            {
                "metric": metric,
                "value": metric_values[metric],
                "operator": condition.get("operator"),
                "threshold": condition.get("value"),
                "triggered": _condition_triggered(
                    metric_values[metric],
                    condition.get("operator", "eq"),
                    condition.get("value"),
                ),
            }
        )
    return evaluations


def _evaluate_block_conditions(rules: dict[str, Any], metric_values: dict[str, Any]) -> list[dict[str, Any]]:
    evaluations = []
    for condition in rules.get("block_conditions", []):
        metric = condition.get("metric")
        if metric not in metric_values:
            continue

        triggered = _condition_triggered(
            metric_values[metric],
            condition.get("operator", "eq"),
            condition.get("value"),
        )
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


def _clamp_score(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 3)


CONTAINER_ATTENTION_MODE = {
    "HOOK": "orienting",
    "SETUP": "guided_focus",
    "CHALLENGE": "guided_focus",
    "TURNING_POINT": "emotional_peak",
    "RESOLUTION": "reflective_release",
    "VISION": "emotional_peak",
}

EFFECT_ATTENTION_COMPATIBILITY = {
    "orienting": {"orient", "signal", "punctuate"},
    "guided_focus": {"signal", "immerse", "resolve"},
    "schema_building": {"signal", "resolve", "immerse"},
    "emotional_peak": {"intensify", "immerse", "punctuate", "signal"},
    "reflective_release": {"resolve", "immerse", "signal"},
}

TEXT_POLICY_COMPATIBILITY = {
    "none": {"low": 1.0, "medium": 0.55, "high": 0.1},
    "keyword_only": {"low": 1.0, "medium": 0.75, "high": 0.35},
    "guided_labels": {"low": 1.0, "medium": 0.85, "high": 0.6},
    "explanatory": {"low": 0.8, "medium": 0.95, "high": 0.8},
}

TEXT_POLICY_LOAD_MODIFIER = {
    "none": 0.0,
    "keyword_only": 0.1,
    "guided_labels": 0.35,
    "explanatory": 0.7,
}


def _duration_fit_score(duration_sec: float, duration_band: dict[str, Any]) -> float:
    minimum = float(duration_band.get("min", duration_sec))
    maximum = float(duration_band.get("max", duration_sec))
    if minimum <= duration_sec <= maximum:
        return 1.0
    span = max(maximum - minimum, 0.5)
    if duration_sec < minimum:
        return _clamp_score(1.0 - ((minimum - duration_sec) / span))
    return _clamp_score(1.0 - ((duration_sec - maximum) / span))


def _scene_cls_fit_score(template_base_cls: float, container_package: dict[str, Any]) -> float:
    cls_budget = container_package.get("contract", {}).get("cls_budget", {})
    target = float(cls_budget.get("target", template_base_cls))
    maximum = float(cls_budget.get("max", max(target, template_base_cls)))
    distance = abs(template_base_cls - target)
    return _clamp_score(1.0 - (distance / max(maximum, 1.0)))


def _memory_fit_score(beat_index: int, total_beats: int, arc_stage: str, template: dict[str, Any]) -> float:
    memory_role = template.get("memory_role")
    peak_weight = template.get("peak_end_weight", "low")
    final_index = max(total_beats - 1, 0)
    if beat_index == 0 and memory_role == "hook_imprint":
        return 1.0
    if arc_stage in {"TURNING_POINT", "CLIMAX"} and memory_role == "peak_snapshot":
        return 1.0
    if beat_index == final_index and memory_role in {"end_snapshot", "transfer_prompt"}:
        return 1.0
    if peak_weight == "high" and arc_stage in {"RESOLUTION", "VISION", "ENDING", "OUTRO"}:
        return 0.9
    if memory_role == "context_encoding":
        return 0.85
    if memory_role == "tension_storage":
        return 0.8
    return 0.7


def _scene_attention_fit_score(container_id: str, template: dict[str, Any]) -> float:
    expected_mode = CONTAINER_ATTENTION_MODE.get(container_id)
    if not expected_mode:
        return 0.75
    if template.get("target_attention_mode") == expected_mode:
        return 1.0
    return 0.7


def _score_scene_template_candidate(
    beat: dict[str, Any],
    beat_index: int,
    total_beats: int,
    arc_stage: str,
    container_id: str,
    selected_component: str,
    container_package: dict[str, Any],
    template_id: str,
    template: dict[str, Any],
    scoring_models: dict[str, Any],
) -> tuple[float, dict[str, Any]]:
    weights = scoring_models.get("scene_selection", {})
    duration_sec = float(beat.get("duration_sec", 0.0))
    component_affinity = 1.0 if selected_component in template.get("preferred_components", []) else 0.65
    duration_fit = _duration_fit_score(duration_sec, template.get("recommended_duration_seconds", {}))
    cls_fit = _scene_cls_fit_score(float(template.get("base_cls", 2.0)), container_package)
    attention_fit = _scene_attention_fit_score(container_id, template)
    memory_fit = _memory_fit_score(beat_index, total_beats, arc_stage, template)
    weighted = (
        component_affinity * float(weights.get("component_affinity_weight", 0.3))
        + duration_fit * float(weights.get("duration_fit_weight", 0.2))
        + cls_fit * float(weights.get("cls_fit_weight", 0.2))
        + attention_fit * float(weights.get("attention_fit_weight", 0.15))
        + memory_fit * float(weights.get("memory_fit_weight", 0.15))
    )
    return _clamp_score(weighted), {
        "template_id": template_id,
        "component_affinity": _clamp_score(component_affinity),
        "duration_fit": duration_fit,
        "cls_fit": cls_fit,
        "attention_fit": attention_fit,
        "memory_fit": memory_fit,
    }


def _effect_congruence_fit(template_mode: str, effect_mode: str) -> float:
    if template_mode == "strict":
        return {"default_safe": 1.0, "conditional": 0.75, "mismatch_only": 0.15}.get(effect_mode, 0.5)
    if template_mode == "relaxed":
        return {"default_safe": 1.0, "conditional": 0.9, "mismatch_only": 0.5}.get(effect_mode, 0.65)
    return {"default_safe": 0.65, "conditional": 0.9, "mismatch_only": 1.0}.get(effect_mode, 0.6)


def _effect_text_fit(text_policy: str, text_risk: str) -> float:
    return _clamp_score(TEXT_POLICY_COMPATIBILITY.get(text_policy, TEXT_POLICY_COMPATIBILITY["keyword_only"]).get(text_risk, 0.6))


def _effect_attention_fit(target_attention_mode: str, attention_role: str) -> float:
    compatible = EFFECT_ATTENTION_COMPATIBILITY.get(target_attention_mode, {"signal", "immerse"})
    return 1.0 if attention_role in compatible else 0.55


def _effect_cls_fit(effect_payload: dict[str, Any], template: dict[str, Any], container_package: dict[str, Any]) -> float:
    cls_budget = container_package.get("contract", {}).get("cls_budget", {})
    maximum = float(cls_budget.get("max", template.get("base_cls", 2.0)))
    available = max(1.0, maximum - float(template.get("base_cls", 2.0)) + 1.0)
    cls_impact = float(effect_payload.get("cls_impact", 1.0))
    return _clamp_score(1.0 - max(0.0, cls_impact - available) / 4.0)


def _score_effect_candidate(
    container_id: str,
    template: dict[str, Any],
    container_package: dict[str, Any],
    effect_id: str,
    effect_payload: dict[str, Any],
    scoring_models: dict[str, Any],
) -> tuple[float, dict[str, Any]]:
    weights = scoring_models.get("effect_selection", {})
    stage_fit = 1.0 if container_id in set(effect_payload.get("best_for", [])) else 0.5
    cls_fit = _effect_cls_fit(effect_payload, template, container_package)
    congruence_fit = _effect_congruence_fit(
        str(template.get("av_congruence_mode", "strict")),
        str(effect_payload.get("congruence_mode", "default_safe")),
    )
    text_fit = _effect_text_fit(
        str(template.get("text_policy", "keyword_only")),
        str(effect_payload.get("text_competition_risk", "medium")),
    )
    attention_fit = _effect_attention_fit(
        str(template.get("target_attention_mode", "guided_focus")),
        str(effect_payload.get("attention_role", "signal")),
    )
    score = (
        stage_fit * float(weights.get("stage_fit_weight", 0.3))
        + cls_fit * float(weights.get("cls_fit_weight", 0.25))
        + congruence_fit * float(weights.get("congruence_fit_weight", 0.2))
        + text_fit * float(weights.get("text_fit_weight", 0.1))
        + attention_fit * float(weights.get("attention_fit_weight", 0.15))
    )
    return _clamp_score(score), {
        "effect_id": effect_id,
        "stage_fit": _clamp_score(stage_fit),
        "cls_fit": cls_fit,
        "congruence_fit": _clamp_score(congruence_fit),
        "text_fit": text_fit,
        "attention_fit": attention_fit,
    }


def _estimate_scene_cls(
    template: dict[str, Any],
    selected_effects: list[dict[str, Any]],
    scoring_models: dict[str, Any],
) -> float:
    load_model = scoring_models.get("load_estimation", {})
    base_cls = float(template.get("base_cls", 2.0))
    top_effects = selected_effects[:2]
    average_arousal = (
        sum(float(effect.get("arousal", 0.0)) for effect in top_effects) / len(top_effects)
        if top_effects else 0.0
    )
    arousal_modifier = average_arousal / float(load_model.get("arousal_scale_divisor", 12.0))
    max_units = int(template.get("max_primary_visual_units", 2))
    if max_units >= int(load_model.get("high_density_element_threshold", 3)):
        information_density_modifier = float(load_model.get("high_density_modifier", 0.6))
    elif max_units == 2:
        information_density_modifier = float(load_model.get("medium_density_modifier", 0.25))
    else:
        information_density_modifier = 0.0
    text_policy_modifier = float(TEXT_POLICY_LOAD_MODIFIER.get(str(template.get("text_policy", "keyword_only")), 0.1))
    risk_lookup = load_model.get("text_competition_modifier", {"low": 0.0, "medium": 0.2, "high": 0.5})
    max_text_risk = "low"
    for effect in selected_effects:
        risk = str(effect.get("text_competition_risk", "low"))
        if risk_lookup.get(risk, 0.0) > risk_lookup.get(max_text_risk, 0.0):
            max_text_risk = risk
    text_competition_modifier = float(risk_lookup.get(max_text_risk, 0.0)) + text_policy_modifier
    estimated = base_cls + arousal_modifier + information_density_modifier + text_competition_modifier
    estimated = max(float(load_model.get("min_scene_cls", 1.0)), min(float(load_model.get("max_scene_cls", 5.0)), estimated))
    return round(estimated, 3)


def _evaluate_validator_gate(actual: float, operator: str, expected: float) -> bool:
    if operator == ">=":
        return actual >= expected
    if operator == "<=":
        return actual <= expected
    if operator == "==":
        return actual == expected
    return False


def _score_prediction_error_fit(container_package: dict[str, Any], component_id: str) -> dict[str, Any]:
    contract = container_package.get("contract", {})
    budget = contract.get("prediction_error_budget", {})
    target = float(budget.get("target", 0.5))
    maximum = max(target, float(budget.get("max", 1.0)))
    component_score = PREDICTION_ERROR_COMPONENT_SCORES.get(component_id, 0.5)
    distance = abs(component_score - target)
    fit_score = _clamp_score(1.0 - (distance / max(maximum, 0.1)))
    exceeds_budget = component_score > maximum
    if exceeds_budget:
        fit_score = _clamp_score(fit_score - 0.2)
    return {
        "target": round(target, 3),
        "max": round(maximum, 3),
        "component_score": round(component_score, 3),
        "fit_score": fit_score,
        "exceeds_budget": exceeds_budget,
        "strategy": budget.get("strategy"),
    }


def _score_transportation_fit(container_package: dict[str, Any], component_id: str) -> dict[str, Any]:
    contract = container_package.get("contract", {})
    transportation_state = contract.get("transportation_state", {})
    phase = transportation_state.get("phase", "orientation")
    target_depth = float(transportation_state.get("target_depth", 0.5))
    compatible_components = TRANSPORTATION_PHASE_COMPONENT_MAP.get(phase, set())
    phase_match = component_id in compatible_components
    fit_score = 0.95 if phase_match else 0.62
    if transportation_state.get("reentry_required") and component_id in {"TURNING_POINT", "JUXTAPOSITION"}:
        fit_score = min(1.0, fit_score + 0.05)
    fit_score = _clamp_score((fit_score * 0.7) + (target_depth * 0.3))
    return {
        "phase": phase,
        "target_depth": round(target_depth, 3),
        "fit_score": fit_score,
        "reentry_required": bool(transportation_state.get("reentry_required", False)),
    }


def _infer_surprise_delta(request: dict[str, Any]) -> float:
    if "predicted_surprise_delta" in request:
        return float(request["predicted_surprise_delta"])

    revision_note = str(request.get("revision_note", "")).lower()
    delta = 0.0
    for keyword in SURPRISE_REDUCTION_KEYWORDS:
        if keyword in revision_note:
            delta -= 0.2
    for keyword in SURPRISE_AMPLIFICATION_KEYWORDS:
        if keyword in revision_note:
            delta += 0.2
    if request.get("mode") == "I2V_ONLY" and any(token in revision_note for token in ("timing", "smooth", "pace")):
        delta -= 0.05
    return round(delta, 3)


def _resolve_container_id(arc_stage: str, scene_intelligence_runtime: dict[str, Any] | None) -> str:
    if scene_intelligence_runtime:
        container_map = scene_intelligence_runtime.get("arc_stage_container_map", {})
        if arc_stage in container_map:
            return container_map[arc_stage]
    return FALLBACK_CONTAINER_ID


def _build_component_metric_context(
    parsed_result: dict[str, Any],
    beat: dict[str, Any],
    container_id: str,
    container_package: dict[str, Any],
    component_id: str,
) -> dict[str, Any]:
    duration_sec = round(float(beat.get("duration_sec", 0.0)), 3)
    cls_observed = container_package.get("contract", {}).get("cls_budget", {}).get("target", 1.5)
    arc_stage = str(beat.get("arc_stage", "")).upper()
    return {
        "asl_observed": duration_sec,
        "cls_observed": cls_observed,
        "stakes_clarity_score": 0.9 if container_id == "HOOK" else 1.0,
        "problem_clarity_score": 0.9 if container_id == "CHALLENGE" else 1.0,
        "peak_signal_score": 0.9 if container_id == "TURNING_POINT" else 1.0,
        "closure_signal_score": 0.9 if container_id == "RESOLUTION" else 1.0,
        "cta_overlap_seconds": max(0.5, float(parsed_result.get("cta_duration_sec") or 0.5)),
        "tribe_specificity_score": 0.8 if component_id == "THE_COMMUNITY" else 1.0,
        "arc_stage": arc_stage,
        "beat_index": int(beat.get("beat_index", 0)),
    }


def _score_component_candidate(
    beat: dict[str, Any],
    beat_index: int,
    total_beats: int,
    container_id: str,
    container_package: dict[str, Any],
    component_id: str,
    component_package: dict[str, Any],
    previous_arc_stage: str | None,
) -> tuple[float, dict[str, Any]]:
    selection_priority = component_package.get("rules", {}).get("selection_priority", {})
    rank = selection_priority.get("rank", 999)
    score = max(0.0, 3.0 - (rank / 10.0))

    if component_id == container_package.get("contract", {}).get("default_component"):
        score += 3.0
    if component_id in container_package.get("rules", {}).get("route_hints", {}).get("preferred_components", []):
        score += 2.0
    if container_id == "VISION" and component_id == "THE_VISION":
        score += 2.5
    if container_id == "RESOLUTION" and previous_arc_stage in {"TURNING_POINT", "CLIMAX"} and component_id == "THE_PAUSE":
        score += 3.0
    if container_id == "HOOK" and beat_index == 0 and component_id == "HOOK":
        score += 1.0
    if container_id == "CHALLENGE" and component_id in {"CHALLENGE", "THE_EVIDENCE", "FRAME_AND_CONTRAST"}:
        score += 0.5
    if total_beats and beat_index == total_beats - 1 and component_id == "THE_VISION":
        score += 1.0
    if beat.get("minimum_hold_compliant") is False and component_id == "THE_PAUSE":
        score -= 1.0

    prediction_error_fit = _score_prediction_error_fit(container_package, component_id)
    transportation_fit = _score_transportation_fit(container_package, component_id)
    audio_affinity_score = _score_audio_profile_affinity(container_id, component_package)
    score += prediction_error_fit["fit_score"] * 2.0
    score += transportation_fit["fit_score"] * 1.5
    score += audio_affinity_score
    if prediction_error_fit["exceeds_budget"]:
        score -= 0.75

    return round(score, 3), {
        "prediction_error": prediction_error_fit,
        "transportation": transportation_fit,
        "audio_affinity_score": audio_affinity_score,
    }


def apply_scene_type_selector_decision(
    parsed_result: dict[str, Any],
    manifest: dict[str, Any],
    subsystem_runtime: dict[str, Any],
    scene_intelligence_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    package = _get_package(subsystem_runtime, "CS-031")
    thresholds = package.get("thresholds", {})
    rules = _get_rules(package)
    route_hints = rules.get("route_hints", {}).get("select", [])
    weight_bio = thresholds.get("biological_fit_weight", 0.6)
    weight_novelty = thresholds.get("novelty_weight", 0.3)
    weight_preference = thresholds.get("preference_weight", 0.1)

    selected_scene_types = []
    warning_beat_indices = []
    previous_vehicle = None
    previous_arc_stage = None
    total_beats = len(manifest.get("beats", []))

    scene_containers = {}
    scene_components = {}
    container_component_index = {}
    scene_templates = {}
    container_template_index = {}
    effect_library = {}
    scoring_models = {}
    scene_intelligence_asset_id = None
    if scene_intelligence_runtime:
        scene_intelligence_asset_id = scene_intelligence_runtime.get("asset_id")
        scene_containers = scene_intelligence_runtime.get("containers", {})
        scene_components = scene_intelligence_runtime.get("components", {})
        container_component_index = scene_intelligence_runtime.get("container_component_index", {})
        scene_templates = scene_intelligence_runtime.get("scene_templates", {})
        container_template_index = scene_intelligence_runtime.get("container_template_index", {})
        effect_library = scene_intelligence_runtime.get("effect_library", {})
        scoring_models = scene_intelligence_runtime.get("scoring_models", {})

    for beat in manifest.get("beats", []):
        arc_stage = str(beat.get("arc_stage", "")).upper()
        selected_vehicle = SCENE_TYPE_VEHICLE_MAP.get(arc_stage, "NEUTRAL_SUPPORT_BEAT")
        selected_container = _resolve_container_id(arc_stage, scene_intelligence_runtime)
        container_package = scene_containers.get(selected_container, {})
        candidate_components = container_component_index.get(
            selected_container,
            container_package.get("contract", {}).get("compatible_components", []),
        )
        base_biological_fit_score = 0.92 if selected_vehicle != "NEUTRAL_SUPPORT_BEAT" else 0.72
        novelty_score = 0.75 if selected_vehicle == previous_vehicle else 0.9
        preference_score = 0.5 if parsed_result.get("preferred_scene_vehicle") is None else 0.85

        selected_component = container_package.get("contract", {}).get("default_component")
        selected_component_score = 0.0
        component_rule_metrics = []
        selected_fit_breakdown = {
            "prediction_error": {},
            "transportation": {},
        }
        scored_candidates = []
        for component_id in candidate_components:
            component_package = scene_components.get(component_id, {})
            if not component_package:
                continue
            score, fit_breakdown = _score_component_candidate(
                beat,
                int(beat.get("beat_index", 0)),
                total_beats,
                selected_container,
                container_package,
                component_id,
                component_package,
                previous_arc_stage,
            )
            metric_context = _build_component_metric_context(
                parsed_result,
                beat,
                selected_container,
                container_package,
                component_id,
            )
            evaluations = _evaluate_warn_conditions(component_package.get("rules", {}), metric_context)
            penalty = sum(1.5 for evaluation in evaluations if evaluation["triggered"])
            adjusted_score = round(score - penalty, 3)
            scored_candidates.append(
                {
                    "component_id": component_id,
                    "score": adjusted_score,
                    "rank": component_package.get("rules", {}).get("selection_priority", {}).get("rank", 999),
                    "fit_breakdown": fit_breakdown,
                    "triggered_rule_metrics": [
                        evaluation["metric"]
                        for evaluation in evaluations
                        if evaluation["triggered"]
                    ] + (["prediction_error_budget"] if fit_breakdown["prediction_error"].get("exceeds_budget") else []),
                    "metric_context": metric_context,
                    "component_rules": component_package.get("rules", {}),
                }
            )

        biological_fit_score = base_biological_fit_score
        selected_variant = None
        if scored_candidates:
            scored_candidates.sort(key=lambda candidate: (-candidate["score"], candidate["rank"], candidate["component_id"]))
            selected_component = scored_candidates[0]["component_id"]
            selected_component_score = scored_candidates[0]["score"]
            component_rule_metrics = scored_candidates[0]["triggered_rule_metrics"]
            selected_fit_breakdown = scored_candidates[0]["fit_breakdown"]
            biological_fit_score = round(
                base_biological_fit_score * 0.5
                + selected_fit_breakdown["prediction_error"].get("fit_score", 0.8) * 0.3
                + selected_fit_breakdown["transportation"].get("fit_score", 0.8) * 0.2,
                3,
            )
            selected_variant = _evaluate_selection_conditions(
                scored_candidates[0]["component_rules"],
                scored_candidates[0]["metric_context"],
            )

        selected_template_id = None
        selected_template_score = 0.0
        selected_template_breakdown = {}
        candidate_templates = []
        template_candidates = container_template_index.get(selected_container, [])
        for template_id in template_candidates:
            template_payload = scene_templates.get(template_id, {})
            score, breakdown = _score_scene_template_candidate(
                beat,
                int(beat.get("beat_index", 0)),
                total_beats,
                arc_stage,
                selected_container,
                selected_component,
                container_package,
                template_id,
                template_payload,
                scoring_models,
            )
            candidate_templates.append(
                {
                    "template_id": template_id,
                    "score": score,
                    "breakdown": breakdown,
                }
            )
        if candidate_templates:
            candidate_templates.sort(key=lambda candidate: (-candidate["score"], candidate["template_id"]))
            selected_template_id = candidate_templates[0]["template_id"]
            selected_template_score = candidate_templates[0]["score"]
            selected_template_breakdown = candidate_templates[0]["breakdown"]

        selected_template = scene_templates.get(selected_template_id or "", {})
        effect_recommendations = []
        if selected_template:
            for effect_id in selected_template.get("coded_effects", []):
                effect_payload = effect_library.get(effect_id)
                if not effect_payload:
                    continue
                effect_score, effect_breakdown = _score_effect_candidate(
                    selected_container,
                    selected_template,
                    container_package,
                    effect_id,
                    effect_payload,
                    scoring_models,
                )
                effect_recommendations.append(
                    {
                        "effect_id": effect_id,
                        "name": effect_payload.get("name"),
                        "category": effect_payload.get("category"),
                        "mechanical_score": effect_score,
                        "cls_impact": effect_payload.get("cls_impact"),
                        "arousal": effect_payload.get("arousal"),
                        "presence": effect_payload.get("presence"),
                        "attention_role": effect_payload.get("attention_role"),
                        "congruence_mode": effect_payload.get("congruence_mode"),
                        "text_competition_risk": effect_payload.get("text_competition_risk"),
                        "breakdown": effect_breakdown,
                    }
                )
        effect_recommendations.sort(key=lambda effect: (-effect["mechanical_score"], effect["effect_id"]))
        selected_effect_stack = [effect["effect_id"] for effect in effect_recommendations[:3]]
        estimated_scene_cls = _estimate_scene_cls(selected_template, effect_recommendations[:3], scoring_models) if selected_template else None
        scene_research_profile = {
            "target_attention_mode": selected_template.get("target_attention_mode"),
            "isc_priority": selected_template.get("isc_priority"),
            "memory_role": selected_template.get("memory_role"),
            "av_congruence_mode": selected_template.get("av_congruence_mode"),
            "continuity_requirement": selected_template.get("continuity_requirement"),
            "text_policy": selected_template.get("text_policy"),
            "peak_end_weight": selected_template.get("peak_end_weight"),
        } if selected_template else {}

        biological_fit_rule = _evaluate_rule(package, "biological_fit_score", biological_fit_score)
        if biological_fit_rule["triggered"]:
            warning_beat_indices.append(beat.get("beat_index"))
        composite_score = round(
            biological_fit_score * weight_bio
            + novelty_score * weight_novelty
            + preference_score * weight_preference,
            3,
        )

        beat["selected_container"] = selected_container
        beat["selected_component"] = selected_component
        beat["selected_scene_template_id"] = selected_template_id
        beat["selected_effect_stack"] = selected_effect_stack
        beat["effect_recommendations"] = effect_recommendations[:3]
        beat["estimated_scene_cls"] = estimated_scene_cls
        beat["scene_research_profile"] = scene_research_profile

        selection = {
            "beat_index": beat.get("beat_index"),
            "arc_stage": arc_stage,
            "selected_vehicle": selected_vehicle,
            "selected_container": selected_container,
            "selected_component": selected_component,
            "selected_scene_template_id": selected_template_id,
            "candidate_templates": [candidate["template_id"] for candidate in candidate_templates],
            "scene_template_score": selected_template_score,
            "scene_template_breakdown": selected_template_breakdown,
            "selected_effect_stack": selected_effect_stack,
            "effect_recommendations": effect_recommendations[:3],
            "estimated_scene_cls": estimated_scene_cls,
            "scene_research_profile": scene_research_profile,
            "resolved_variant": selected_variant,
            "candidate_components": [
                candidate["component_id"]
                for candidate in scored_candidates
            ] or candidate_components,
            "component_selection_score": selected_component_score,
            "component_rule_metrics": component_rule_metrics,
            "biological_fit_score": biological_fit_score,
            "prediction_error_fit_score": selected_fit_breakdown["prediction_error"].get("fit_score"),
            "prediction_error_strategy": selected_fit_breakdown["prediction_error"].get("strategy"),
            "transportation_fit_score": selected_fit_breakdown["transportation"].get("fit_score"),
            "transportation_phase": selected_fit_breakdown["transportation"].get("phase"),
            "audio_affinity_score": selected_fit_breakdown.get("audio_affinity_score"),
            "novelty_score": novelty_score,
            "preference_score": preference_score,
            "composite_score": composite_score,
            "rule_evaluation": biological_fit_rule,
            "selection_weights": {
                "biological_fit": weight_bio,
                "novelty": weight_novelty,
                "preference": weight_preference,
            },
        }
        beat["selected_scene_vehicle"] = selected_vehicle
        selected_scene_types.append(selection)
        previous_vehicle = selected_vehicle
        previous_arc_stage = arc_stage

    manifest["scene_type_plan"] = selected_scene_types
    manifest["scene_structure_plan"] = selected_scene_types
    return {
        "subsystem_id": "CS-031",
        "verdict": _decision_verdict(package, warning_beat_indices),
        "evaluation_mode": "rules_yaml",
        "scene_intelligence_source": "compiled_runtime_asset" if scene_intelligence_runtime else "subsystem_only",
        "scene_intelligence_asset_id": scene_intelligence_asset_id,
        "route_hints": route_hints,
        "warning_beat_indices": warning_beat_indices,
        "selected_beat_count": len(selected_scene_types),
        "selected_scene_types": selected_scene_types,
    }


def apply_cognitive_rhythm_validator_decision(
    beats: list[dict[str, Any]],
    scene_intelligence_runtime: dict[str, Any] | None,
) -> dict[str, Any]:
    validator = (scene_intelligence_runtime or {}).get("cognitive_rhythm_validator", {})
    if not beats or not validator:
        return {
            "validator_id": validator.get("validator_id", "CRV-SCENE-BUILDER-v1"),
            "verdict": "PASS",
            "score": 1.0,
            "metrics": {},
            "gates": [],
            "repair_hints": [],
        }

    high_cls_indices = [
        index for index, beat in enumerate(beats)
        if float(beat.get("estimated_scene_cls") or 0.0) >= 4.0
    ]
    recovered_count = 0
    for index in high_cls_indices:
        next_beat = beats[index + 1] if index + 1 < len(beats) else None
        if not next_beat:
            continue
        if float(next_beat.get("estimated_scene_cls") or 5.0) <= 2.2 or next_beat.get("rhythm_role") == "reset_space":
            recovered_count += 1
    recovery_ratio = round(recovered_count / len(high_cls_indices), 3) if high_cls_indices else 1.0

    mismatch_indices = []
    resolved_mismatch = 0
    for index, beat in enumerate(beats):
        profile = beat.get("scene_research_profile", {})
        effect_recommendations = beat.get("effect_recommendations", [])
        is_mismatch = profile.get("av_congruence_mode") == "strategic_mismatch" or any(
            effect.get("congruence_mode") == "mismatch_only" for effect in effect_recommendations
        )
        if not is_mismatch:
            continue
        mismatch_indices.append(index)
        next_beat = beats[index + 1] if index + 1 < len(beats) else None
        if next_beat and next_beat.get("scene_research_profile", {}).get("av_congruence_mode") == "strict":
            resolved_mismatch += 1
    mismatch_resolution_ratio = round(resolved_mismatch / len(mismatch_indices), 3) if mismatch_indices else 1.0

    peak_end_stages = set(validator.get("sequence_contract", {}).get("peak_end_stages", []))
    peak_end_candidates = [
        beat for beat in beats
        if str(beat.get("arc_stage", "")).upper() in peak_end_stages
    ]
    peak_end_hits = 0
    for beat in peak_end_candidates:
        profile = beat.get("scene_research_profile", {})
        effect_recommendations = beat.get("effect_recommendations", [])
        if (
            profile.get("peak_end_weight") == "high"
            and beat.get("memory_priority") == "PEAK_END"
            and not any(effect.get("congruence_mode") == "mismatch_only" for effect in effect_recommendations)
        ):
            peak_end_hits += 1
    peak_end_focus_score = round(peak_end_hits / len(peak_end_candidates), 3) if peak_end_candidates else 1.0

    continuity_candidates = [
        beat for beat in beats
        if float(beat.get("estimated_scene_cls") or 0.0) >= 3.0 or beat.get("selected_scene_template_id")
    ]
    continuity_hits = 0
    for index, beat in enumerate(continuity_candidates):
        requirement = beat.get("scene_research_profile", {}).get("continuity_requirement")
        if requirement != "intentional_disruption":
            continuity_hits += 1
            continue
        original_index = beats.index(beat)
        next_beat = beats[original_index + 1] if original_index + 1 < len(beats) else None
        if next_beat and next_beat.get("scene_research_profile", {}).get("av_congruence_mode") == "strict":
            continuity_hits += 1
    continuity_anchor_ratio = round(continuity_hits / len(continuity_candidates), 3) if continuity_candidates else 1.0

    reset_space_count = sum(
        1 for beat in beats
        if beat.get("rhythm_role") in {"reset_space", "bridge"} and float(beat.get("estimated_scene_cls") or 5.0) <= 2.5
    )
    reset_space_ratio = round(reset_space_count / len(beats), 3) if beats else 1.0

    metrics = {
        "recovery_ratio": recovery_ratio,
        "mismatch_resolution_ratio": mismatch_resolution_ratio,
        "peak_end_focus_score": peak_end_focus_score,
        "continuity_anchor_ratio": continuity_anchor_ratio,
        "reset_space_ratio": reset_space_ratio,
    }

    gates = []
    repair_hints = []
    weighted_score = 0.0
    hard_fail = False
    for gate in validator.get("gates", []):
        metric_name = gate.get("metric")
        actual = float(metrics.get(metric_name, 0.0))
        expected = float(gate.get("value", 0.0))
        passed = _evaluate_validator_gate(actual, str(gate.get("operator", ">=")), expected)
        block_below = gate.get("block_below")
        if isinstance(block_below, (int, float)) and actual < float(block_below):
            hard_fail = True
        if not passed:
            repair_hints.append(gate.get("repair_hint", "Revise sequence rhythm."))
        weighted_score += min(actual / expected, 1.0) * float(gate.get("weight", 0.0)) if expected > 0 else 0.0
        gates.append(
            {
                "gate_id": gate.get("gate_id"),
                "name": gate.get("name"),
                "metric": metric_name,
                "actual": round(actual, 3),
                "target": round(expected, 3),
                "passed": passed,
                "repair_hint": gate.get("repair_hint"),
            }
        )

    score = _clamp_score(weighted_score)
    bands = validator.get("score_bands", {})
    if hard_fail:
        verdict = "BLOCK"
    elif score >= float(bands.get("pass", 0.8)):
        verdict = "PASS"
    elif score >= float(bands.get("revise", 0.65)):
        verdict = "REVISE"
    else:
        verdict = "BLOCK"

    return {
        "validator_id": validator.get("validator_id"),
        "verdict": verdict,
        "score": score,
        "metrics": metrics,
        "gates": gates,
        "repair_hints": list(dict.fromkeys(repair_hints)),
    }


def apply_rhythm_generator_decision(beats: list[dict[str, Any]], subsystem_runtime: dict[str, Any]) -> dict[str, Any]:
    package = _get_package(subsystem_runtime, "CS-023")
    thresholds = package.get("thresholds", {})
    rules = _get_rules(package)
    route_hints = rules.get("route_hints", {}).get("generate", [])
    durations = [round(float(beat.get("duration_sec", 0.0)), 3) for beat in beats]
    if not durations:
        return {
            "subsystem_id": "CS-023",
            "verdict": _decision_verdict(package, [{"metric": "target_asl_seconds"}]),
            "evaluation_mode": "rules_yaml",
            "shot_duration_vector": [],
            "tempo_clusters": [],
            "reset_space_indices": [],
            "triggered_rules": [{"metric": "target_asl_seconds", "triggered": True}],
            "route_hints": route_hints,
        }

    average_shot_length = round(sum(durations) / len(durations), 3)
    reset_threshold = average_shot_length * 1.1
    reset_space_indices = [
        beat.get("beat_index")
        for beat in beats
        if float(beat.get("duration_sec", 0.0)) >= reset_threshold
    ]
    tempo_clusters = []
    for beat in beats:
        duration = float(beat.get("duration_sec", 0.0))
        if duration >= reset_threshold:
            cluster = "reset_space"
        elif duration <= average_shot_length * 0.85:
            cluster = "burst"
        else:
            cluster = "bridge"
        beat["rhythm_role"] = cluster
        tempo_clusters.append({
            "beat_index": beat.get("beat_index"),
            "cluster": cluster,
            "duration_sec": round(duration, 3),
        })

    asl_rule = _evaluate_rule(package, "target_asl_seconds", average_shot_length)
    triggered_rules = []
    if asl_rule["triggered"]:
        triggered_rules.append(asl_rule)
    if thresholds.get("require_reset_spaces", False) and not reset_space_indices:
        triggered_rules.append({
            "metric": "require_reset_spaces",
            "value": [],
            "threshold": True,
            "triggered": True,
        })

    return {
        "subsystem_id": "CS-023",
        "verdict": _decision_verdict(package, triggered_rules),
        "evaluation_mode": "rules_yaml",
        "shot_duration_vector": durations,
        "average_shot_length_seconds": average_shot_length,
        "tempo_clusters": tempo_clusters,
        "reset_space_indices": reset_space_indices,
        "triggered_rules": triggered_rules,
        "route_hints": route_hints,
    }


def apply_shot_duration_enforcer_decision(
    beats: list[dict[str, Any]],
    subsystem_runtime: dict[str, Any],
) -> dict[str, Any]:
    package = _get_package(subsystem_runtime, "CS-015")
    thresholds = package.get("thresholds", {})
    rules = _get_rules(package)
    route_hints = rules.get("route_hints", {}).get("corrective_moves", [])
    minimum_inference_duration_ms = thresholds.get("minimum_inference_duration_ms", 750)
    contextless_minimum_duration_ms = thresholds.get("contextless_minimum_duration_ms", 2000)
    allow_hook_microcuts = thresholds.get("allow_hook_microcuts", False)

    noncompliant_beats = []
    recommendations = []
    triggered_rules = []

    for beat in beats:
        beat_index = int(beat.get("beat_index", 0))
        arc_stage = str(beat.get("arc_stage", "")).upper()
        duration_ms = round(float(beat.get("duration_sec", 0.0)) * 1000)
        contextless = beat_index == 0 or beat.get("start_frame", 0) == 0
        recommended_minimum_ms = contextless_minimum_duration_ms if contextless else minimum_inference_duration_ms
        hook_microcut_allowed = allow_hook_microcuts and arc_stage in {"HOOK", "OPENING"} and duration_ms >= minimum_inference_duration_ms
        rule_eval = _evaluate_rule(package, "shot_length_ms", duration_ms)
        triggered = duration_ms < recommended_minimum_ms and not hook_microcut_allowed
        compliant = not triggered

        beat["minimum_hold_compliant"] = compliant
        beat["recommended_minimum_hold_sec"] = round(recommended_minimum_ms / 1000, 3)
        beat["hook_microcut_allowed"] = hook_microcut_allowed

        if triggered:
            noncompliant_beats.append(beat_index)
            recommendations.append(
                {
                    "beat_index": beat_index,
                    "current_duration_sec": round(duration_ms / 1000, 3),
                    "recommended_minimum_hold_sec": round(recommended_minimum_ms / 1000, 3),
                }
            )
            triggered_rules.append(
                {
                    **rule_eval,
                    "threshold": recommended_minimum_ms,
                    "triggered": True,
                }
            )

    return {
        "subsystem_id": "CS-015",
        "verdict": _decision_verdict(package, triggered_rules),
        "evaluation_mode": "rules_yaml",
        "minimum_inference_duration_sec": round(minimum_inference_duration_ms / 1000, 3),
        "contextless_minimum_duration_sec": round(contextless_minimum_duration_ms / 1000, 3),
        "allow_hook_microcuts": allow_hook_microcuts,
        "noncompliant_beats": noncompliant_beats,
        "triggered_rules": triggered_rules,
        "recommendations": recommendations,
        "route_hints": route_hints,
    }


def build_regeneration_patch_selection(
    request: dict[str, Any],
    plan: dict[str, Any],
    subsystem_runtime: dict[str, Any],
    scene_intelligence_runtime: dict[str, Any] | None = None,
) -> dict[str, Any]:
    beat_index = int(request["beat_index"])
    arc_stage = str(request.get("arc_stage", "CHALLENGE")).upper()
    current_duration_sec = round(float(request.get("current_shot_duration_sec", 1.2)), 3)
    local_shot_duration_vector = request.get("local_shot_duration_vector")
    if local_shot_duration_vector:
        durations = [round(float(value), 3) for value in local_shot_duration_vector]
    else:
        durations = [
            round(max(0.75, current_duration_sec * 0.85), 3),
            current_duration_sec,
            round(max(0.9, current_duration_sec * 1.25), 3),
        ]

    timing_window = []
    for offset, duration in enumerate(durations):
        window_index = beat_index + offset - 1
        timing_window.append(
            {
                "beat_index": window_index,
                "arc_stage": arc_stage if window_index == beat_index else request.get("neighbor_arc_stage", "SETUP"),
                "duration_sec": duration,
                "start_frame": 24 * max(0, offset),
            }
        )

    rhythm_decision = apply_rhythm_generator_decision(timing_window, subsystem_runtime)
    shot_duration_decision = apply_shot_duration_enforcer_decision([timing_window[1]], subsystem_runtime)

    container_id = _resolve_container_id(arc_stage, scene_intelligence_runtime)
    container_package = (scene_intelligence_runtime or {}).get("containers", {}).get(container_id, {})
    cs033_package = _get_package(subsystem_runtime, "CS-033")
    cs033_rules = _get_rules(cs033_package)
    cs033_thresholds = cs033_package.get("thresholds", {})
    surprise_delta = _infer_surprise_delta(request)
    base_surprise_score = float(
        request.get(
            "current_prediction_error_score",
            container_package.get("contract", {}).get("prediction_error_budget", {}).get("target", 0.5),
        )
    )
    predicted_surprise_score = _clamp_score(base_surprise_score + surprise_delta)
    legibility_loss = float(request.get("legibility_loss", max(0.0, predicted_surprise_score - 0.75)))
    metric_context = {
        "prediction_error_score": predicted_surprise_score,
        "legibility_loss": legibility_loss,
        "container_budget_exceeded": predicted_surprise_score
        > float(container_package.get("contract", {}).get("prediction_error_budget", {}).get("max", 1.0)),
    }
    cs033_warns = _evaluate_warn_conditions(cs033_rules, metric_context)
    cs033_blocks = _evaluate_block_conditions(cs033_rules, metric_context)
    removed_surprise = predicted_surprise_score < float(cs033_thresholds.get("minimum_prediction_error_score", 0.35))
    over_amplified_surprise = metric_context["container_budget_exceeded"] or legibility_loss > float(
        cs033_thresholds.get("maximum_legibility_loss", 0.25)
    )
    prediction_error_gate_decision = {
        "subsystem_id": "CS-033",
        "verdict": "BLOCK"
        if any(entry["triggered"] for entry in cs033_blocks)
        else "REVISE"
        if removed_surprise or over_amplified_surprise or any(entry["triggered"] for entry in cs033_warns)
        else "PASS",
        "prediction_error_score": predicted_surprise_score,
        "surprise_delta": surprise_delta,
        "legibility_loss": round(legibility_loss, 3),
        "container_id": container_id,
        "container_budget": container_package.get("contract", {}).get("prediction_error_budget", {}),
        "removed_surprise": removed_surprise,
        "over_amplified_surprise": over_amplified_surprise,
        "warn_conditions": cs033_warns,
        "block_conditions": cs033_blocks,
        "route_hints": cs033_rules.get("route_hints", {}),
    }

    regenerate_route_hints = (
        _get_rules(_get_package(subsystem_runtime, "CS-023")).get("route_hints", {}).get("regenerate")
        or rhythm_decision.get("route_hints", [])
    )

    corrective_moves = []
    corrective_moves.extend(shot_duration_decision.get("route_hints", []))
    corrective_moves.extend(regenerate_route_hints)
    if removed_surprise:
        corrective_moves.extend(cs033_rules.get("route_hints", {}).get("amplify", []))
    if over_amplified_surprise:
        corrective_moves.extend(cs033_rules.get("route_hints", {}).get("soften", []))

    targeted_fields = []
    if shot_duration_decision["verdict"] != "PASS":
        targeted_fields.extend([
            f"/beats/{beat_index}/duration_sec",
            f"/beats/{beat_index}/duration_frames",
        ])
    if rhythm_decision["verdict"] != "PASS":
        targeted_fields.extend([
            f"/beats/{beat_index}/transition",
            f"/beats/{beat_index}/motion_profile",
        ])
    if request.get("mode") in {"T2I_ONLY", "BOTH"}:
        targeted_fields.append(f"/beats/{beat_index}/fallback_image_url")
    if request.get("mode") in {"I2V_ONLY", "BOTH", "T2I_ONLY"}:
        targeted_fields.append(f"/beats/{beat_index}/video_clip_url")
    if removed_surprise or over_amplified_surprise:
        targeted_fields.extend(
            [
                f"/beats/{beat_index}/transition",
                f"/beats/{beat_index}/motion_profile",
            ]
        )
        if request.get("mode") in {"T2I_ONLY", "BOTH"}:
            targeted_fields.append(f"/beats/{beat_index}/fallback_image_url")

    if shot_duration_decision["verdict"] != "PASS" and rhythm_decision["verdict"] != "PASS":
        patch_profile = "TIMING_REBALANCE_PATCH"
    elif shot_duration_decision["verdict"] != "PASS":
        patch_profile = "EXTEND_HOLD_PATCH"
    elif rhythm_decision["verdict"] != "PASS":
        patch_profile = "RHYTHM_REBALANCE_PATCH"
    else:
        patch_profile = "TARGETED_VISUAL_PATCH"

    return {
        "regeneration_decisions": {
            "rhythm_generator": rhythm_decision,
            "shot_duration": shot_duration_decision,
            "prediction_error_gate": prediction_error_gate_decision,
        },
        "patch_selection": {
            "target_beat_index": beat_index,
            "patch_profile": patch_profile,
            "timing_patch_required": patch_profile != "TARGETED_VISUAL_PATCH",
            "surprise_patch_required": removed_surprise or over_amplified_surprise,
            "surprise_adjustment": "restore_surprise"
            if removed_surprise
            else "reduce_surprise"
            if over_amplified_surprise
            else None,
            "targeted_fields": sorted(set(targeted_fields)),
            "corrective_moves": list(dict.fromkeys(corrective_moves)),
            "neighbor_consultation_indices": [
                entry["beat_index"]
                for entry in timing_window
                if entry["beat_index"] != beat_index
            ] if rhythm_decision["verdict"] != "PASS" else [],
            "timing_window": timing_window,
            "surprise_score": predicted_surprise_score,
        },
    }