"""
CMF Legitimacy Runner — Layered Questions and CBAR pre-commit executor.

Loads the schema-backed runtime assets for Scene Builder and editor
regeneration, evaluates the available context, emits a DEP-VID-034
Constraint Resolution Manifest, and writes a receipt-chain proof for the
legitimacy stage.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

try:
    from .receipt_chain import write_receipt
    from .subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset
except ImportError:
    from receipt_chain import write_receipt
    from subsystem_loader import STAGE_SUBSYSTEM_ID_MAP, load_compiled_subsystem_runtime_asset


REPO_ROOT = Path(__file__).resolve().parents[2]

COMPILE_TARGET_CONFIG = {
    "SCENE_BUILDER": {
        "framework_path": REPO_ROOT / "intelligence" / "frameworks" / "layered_questions_scene_builder.runtime.json",
        "gate_pack_path": REPO_ROOT / "intelligence" / "gates" / "cbar_scene_builder_gate_pack.runtime.json",
        "proof_stage_name": "SCENE_LEGITIMACY_GATE",
        "target_type": "SCENE_CANDIDATE",
        "runtime_stage": "scene_builder",
        "subsystem_ids": STAGE_SUBSYSTEM_ID_MAP["scene_builder"],
    },
    "EDITOR_REGENERATION": {
        "framework_path": REPO_ROOT / "intelligence" / "frameworks" / "layered_questions_editor_regeneration.runtime.json",
        "gate_pack_path": REPO_ROOT / "intelligence" / "gates" / "cbar_editor_regeneration_gate_pack.runtime.json",
        "proof_stage_name": "EDITOR_REGEN_LEGITIMACY_GATE",
        "target_type": "REGENERATION_REQUEST",
        "runtime_stage": "editor_regeneration",
        "subsystem_ids": STAGE_SUBSYSTEM_ID_MAP["editor_regeneration"],
    },
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _constraint_manifest_id(compile_target: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"CRM-{compile_target}-{stamp}-{uuid4().hex[:8].upper()}"


def _get_by_path(payload: Any, dotted_path: str) -> Any:
    current = payload
    for part in dotted_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        return None
    return current


def _resolve_expected(value: Any, context: dict) -> Any:
    if isinstance(value, str) and "." in value:
        resolved = _get_by_path(context, value)
        if resolved is not None:
            return resolved
    if isinstance(value, list):
        return [_resolve_expected(item, context) for item in value]
    return value


def _compare(operator: str, actual: Any, expected: Any) -> Optional[bool]:
    if actual is None:
        return None
    if operator == "contains_all":
        if not isinstance(actual, list):
            return None
        return all(item in actual for item in expected)
    if operator == "non_empty":
        if isinstance(actual, str):
            return bool(actual.strip()) == bool(expected)
        return bool(actual) == bool(expected)
    if expected is None:
        return None
    if operator == ">=":
        return actual >= expected
    if operator == "<=":
        return actual <= expected
    if operator == "==":
        return actual == expected
    if operator == "between":
        return expected[0] <= actual <= expected[1]
    if operator == "subset_of":
        if not isinstance(actual, list) or not isinstance(expected, list):
            return None
        return set(actual).issubset(set(expected))
    if operator == "within_target_band":
        if not isinstance(expected, list) or len(expected) != 2:
            return None
        return expected[0] <= actual <= expected[1]
    return None


def _expand_allowed_paths(paths: list[str], target_beat_index: Optional[int]) -> list[str]:
    if target_beat_index is None:
        return paths
    target = str(target_beat_index)
    return [path.replace("{target}", target) for path in paths]


def _derive_scene_mode(scene_packet: dict) -> tuple[str, float]:
    stage = str(scene_packet.get("arc_stage") or scene_packet.get("scene_type") or "").upper()
    if stage in {"HOOK", "TURNING_POINT", "CLIMAX", "TENSION"}:
        return "TENSION", 0.75
    if stage in {"SETUP", "CHALLENGE", "VULNERABILITY"}:
        return "VULNERABILITY", 0.75
    if stage in {"RESOLUTION", "VISION", "RECOGNITION"}:
        return "RECOGNITION", 0.75
    return "TENSION", 0.65


def _derive_regen_mode(revision_note: str, beat_context: dict) -> tuple[str, float]:
    note = revision_note.lower()
    if any(token in note for token in ["contrast", "shock", "surprise", "intense", "tension"]):
        return "TENSION", 0.72
    if any(token in note for token in ["warm", "soft", "human", "intimate", "vulnerab"]):
        return "VULNERABILITY", 0.72
    if any(token in note for token in ["specific", "real", "recogn", "authentic", "detail"]):
        return "RECOGNITION", 0.72
    return _derive_scene_mode(beat_context)


def _derive_scene_changed_axes(scene_packet: dict, neighbor_context: dict) -> list[str]:
    provided = neighbor_context.get("changed_axes")
    if isinstance(provided, list):
        return provided

    changed = []
    previous = neighbor_context.get("previous", {})
    comparisons = {
        "color_temperature_k": "color_temperature",
        "motion_profile": "motion_profile",
        "pace_profile": "pace_profile",
        "framing": "framing",
    }
    for field, axis_name in comparisons.items():
        previous_value = previous.get(field)
        current_value = scene_packet.get(field)
        if previous_value is not None and current_value is not None and previous_value != current_value:
            changed.append(axis_name)
    return changed


def _derive_layered_context(compile_target: str, context: dict, framework: dict) -> dict:
    if compile_target == "SCENE_BUILDER":
        scene_packet = context.setdefault("scene_packet", {})
        evidence = context.setdefault("project_evidence", {})
        neighbor_context = context.setdefault("neighbor_context", {})

        if "source_types" not in evidence:
            evidence["source_types"] = ["transcript", "project_dna", "subsystem_evidence"]

        dominant_mode, confidence = _derive_scene_mode(scene_packet)
        directive_count = scene_packet.get("directive_count", 3)
        density = scene_packet.get("directive_density_score")
        if density is None:
            density = 1.0 if directive_count <= 3 else 0.6

        changed_axes = _derive_scene_changed_axes(scene_packet, neighbor_context)

        context["dominant_detection_mode"] = {
            "mode": dominant_mode,
            "confidence": confidence,
        }
        context["compression_density_score"] = density
        context["parameter_delta_from_previous"] = {
            "changed_axes": len(changed_axes),
            "axes": changed_axes,
        }
        return {
            "asset_id": framework["asset_id"],
            "dominant_mode": dominant_mode,
        }

    beat_context = context.setdefault("beat_context", {})
    manifest_patch_request = context.setdefault("manifest_patch_request", {})
    revision_note = context.get("revision_note", "")
    dominant_mode, confidence = _derive_regen_mode(revision_note, beat_context)

    changed_paths = manifest_patch_request.get("changed_paths", [])
    mutation_score = manifest_patch_request.get("mutation_compression_score")
    if mutation_score is None:
        mutation_score = 1.0 if len(changed_paths) <= 5 else 0.6

    target_beat_index = manifest_patch_request.get("target_beat_index")
    off_target = manifest_patch_request.get("off_target_drift_count")
    if off_target is None:
        off_target = 0
        for path in changed_paths:
            if target_beat_index is None or f"/beats/{target_beat_index}/" not in path:
                off_target += 1

    context["dominant_detection_mode"] = {
        "mode": dominant_mode,
        "confidence": confidence,
    }
    context["mutation_compression_score"] = mutation_score
    context["off_target_drift_count"] = off_target
    return {
        "asset_id": framework["asset_id"],
        "dominant_mode": dominant_mode,
    }


def _evaluate_check(check: dict, context: dict) -> tuple[Optional[bool], str]:
    field = check["field"]
    actual = _get_by_path(context, field)
    expected = _resolve_expected(check.get("value"), context)
    if check["operator"] == "subset_of" and isinstance(expected, list):
        target_beat_index = _get_by_path(context, "manifest_patch_request.target_beat_index")
        expected = _expand_allowed_paths(expected, target_beat_index)
    result = _compare(check["operator"], actual, expected)
    if result is None:
        return None, f"PARTIAL_PROOF: {check['check_id']} could not be fully evaluated from available context"
    if result:
        return True, f"PASS: {check['check_id']}"
    return False, f"{check['failure_code']}: {check['repair_hint']}"


def _evaluate_layered_questions(compile_target: str, framework: dict, context: dict) -> tuple[dict, list[str], bool, bool]:
    meta = _derive_layered_context(compile_target, context, framework)
    law_results = []
    required_actions = []
    hard_fail = False
    has_partial = False
    weighted_score = 0.0

    for law in framework["laws"]:
        diagnostics = []
        law_passed = True
        law_partial = False
        for check in law["checks"]:
            result, diagnostic = _evaluate_check(check, context)
            diagnostics.append(diagnostic)
            if result is False:
                law_passed = False
                hard_fail = True
                required_actions.append(check["repair_hint"])
            elif result is None:
                law_partial = True
                has_partial = True
                required_actions.append(f"Supply context for {check['check_id']}")

        if law_passed:
            if law_partial:
                weighted_score += framework["scoring"]["weights"][law["law_id"]] * 0.5
            else:
                weighted_score += framework["scoring"]["weights"][law["law_id"]]

        law_results.append(
            {
                "law_id": law["law_id"],
                "passed": law_passed,
                "diagnostics": diagnostics,
            }
        )

    score = round(weighted_score, 4)
    return (
        {
            "asset_id": meta["asset_id"],
            "score": score,
            "dominant_mode": meta["dominant_mode"],
            "law_results": law_results,
        },
        sorted(set(required_actions)),
        hard_fail,
        has_partial,
    )


def _default_precedence(question: dict, passed: bool, partial: bool) -> dict:
    constraint_a = question["constraint_a"]["rule_id"]
    constraint_b = question["constraint_b"]["rule_id"]
    if passed:
        winner = constraint_a
        reasoning = (
            f"{constraint_a} can proceed because the available runtime evidence does not show a conflict that would force {constraint_b} to override it."
        )
        action = "Proceed with the resolved candidate and preserve the downstream contract."
    elif partial:
        winner = constraint_b
        reasoning = (
            f"{constraint_b} temporarily governs because the current context is incomplete and audit safety must dominate until stronger proof is attached."
        )
        action = "Proceed with caution, attach missing proof, and preserve rollback-safe outputs."
    else:
        winner = constraint_b
        reasoning = (
            f"{constraint_b} overrides because the automated check shows the current candidate would violate a required safety or continuity boundary."
        )
        action = "Block commit until the repair hint is satisfied."
    return {
        "winning_constraint": winner,
        "precedence_rule_id": winner,
        "precedence_reasoning": reasoning,
        "chosen_action": action,
        "downstream_impact": question["downstream_consumer"]["expected_input"],
    }


def _evaluate_cbar_gate_pack(gate_pack: dict, context: dict) -> tuple[list[dict], dict, list[str], bool, bool]:
    results = []
    contradictions = []
    required_actions = []
    hard_fail = False
    has_partial = False

    for gate in gate_pack["gates"]:
        gate_passed = True
        question_results = []
        for question in gate["questions"]:
            diagnostics = []
            question_passed = True
            question_partial = False
            for check in question.get("automated_checks", []):
                result, diagnostic = _evaluate_check(check, context)
                diagnostics.append(diagnostic)
                if result is False:
                    question_passed = False
                    gate_passed = False
                    hard_fail = True
                    contradictions.append(question["question_id"])
                    required_actions.append(check["repair_hint"])
                elif result is None:
                    question_partial = True
                    has_partial = True
                    required_actions.append(f"Supply context for {check['check_id']}")

            precedence = _default_precedence(question, question_passed and not question_partial, question_partial)
            proof_status = "PRESENT"
            if question_partial and question_passed:
                proof_status = "PARTIAL"
            elif not question_passed:
                proof_status = "MISSING"

            question_results.append(
                {
                    "question_id": question["question_id"],
                    "passed": question_passed,
                    "diagnostic": " | ".join(diagnostics) if diagnostics else "PASS",
                    "proof_status": proof_status,
                    **precedence,
                }
            )

        results.append({
            "gate_id": gate["gate_id"],
            "passed": gate_passed,
            "questions": question_results,
        })

    cascade_lock = {
        "passed": not hard_fail,
        "consistency_verdict": (
            "INCONSISTENT" if hard_fail else "PARTIAL_CONTEXT" if has_partial else "CONSISTENT"
        ),
        "contradiction_list": contradictions,
        "secondary_resolution_required": hard_fail or has_partial,
        "constraint_manifest_ready": True,
    }
    return results, cascade_lock, sorted(set(required_actions)), hard_fail, has_partial


def _attach_subsystem_runtime(compile_target: str, context: dict) -> dict:
    config = COMPILE_TARGET_CONFIG[compile_target]
    runtime = load_compiled_subsystem_runtime_asset(
        config["runtime_stage"],
        config.get("subsystem_ids"),
    )
    context["subsystem_runtime"] = {
        "stage": runtime["runtime_stage"],
        "active_subsystems": runtime["active_subsystems"],
        "thresholds": runtime["thresholds"],
        "validation_contract": runtime["validation_contract"],
        "asset_path": runtime["asset_path"],
    }
    context.setdefault("evidence_refs", [])
    context["evidence_refs"] = sorted(set(context["evidence_refs"] + runtime["evidence_refs"] + [runtime["asset_path"]]))

    if compile_target == "SCENE_BUILDER":
        context.setdefault("scene_packet", {})["selected_subsystems"] = runtime["active_subsystems"]
        context.setdefault("project_evidence", {}).setdefault(
            "source_types",
            ["transcript", "project_dna", "subsystem_evidence"],
        )
    else:
        context.setdefault("beat_context", {})["active_subsystems"] = runtime["active_subsystems"]

    return runtime


def run_legitimacy_check(
    compile_target: str,
    project_id: str,
    target_ref: dict,
    context: dict,
    previous_receipt: Optional[dict] = None,
    receipt_output_dir: Optional[str] = None,
) -> tuple[dict, dict]:
    """
    Execute the legitimacy stage and emit DEP-VID-034 plus a receipt.

    Returns:
        (constraint_manifest, legitimacy_receipt)
    """
    if compile_target not in COMPILE_TARGET_CONFIG:
        raise ValueError(f"Unsupported compile target: {compile_target}")

    config = COMPILE_TARGET_CONFIG[compile_target]
    subsystem_runtime = _attach_subsystem_runtime(compile_target, context)
    framework = _load_json(config["framework_path"])
    gate_pack = _load_json(config["gate_pack_path"])

    layered_questions, lq_actions, lq_fail, lq_partial = _evaluate_layered_questions(
        compile_target, framework, context
    )
    cbar_results, cascade_lock, cbar_actions, cbar_fail, cbar_partial = _evaluate_cbar_gate_pack(
        gate_pack, context
    )

    decision = "PASS"
    if lq_fail or cbar_fail:
        decision = "BLOCK"
    elif lq_partial or cbar_partial:
        decision = "REVISE"

    output_dir = Path(receipt_output_dir or ".")
    output_dir.mkdir(parents=True, exist_ok=True)

    constraint_manifest_id = _constraint_manifest_id(compile_target)
    manifest_path = output_dir / f"constraint_manifest_{constraint_manifest_id}.json"

    evidence_refs = context.get("evidence_refs", [])
    required_actions = sorted(set(lq_actions + cbar_actions))
    if decision == "BLOCK" and not required_actions:
        required_actions.append("Resolve failing legitimacy checks before commit.")

    manifest = {
        "constraint_manifest_id": constraint_manifest_id,
        "project_id": project_id,
        "compile_target": compile_target,
        "target_type": config["target_type"],
        "target_ref": target_ref,
        "decision": decision,
        "layered_questions": layered_questions,
        "cbar_results": cbar_results,
        "cascade_lock": cascade_lock,
        "proof_receipt": {
            "stage_name": config["proof_stage_name"],
            "agent_name": "legitimacy_runner",
            "receipt_id": "PENDING",
            "previous_receipt_hash": "PENDING",
        },
        "output_files": [
            {"kind": "constraint_manifest", "path": str(manifest_path)}
        ],
        "required_actions": required_actions,
        "evidence_refs": evidence_refs,
        "subsystem_runtime": {
            "stage": subsystem_runtime["runtime_stage"],
            "active_subsystems": subsystem_runtime["active_subsystems"],
            "validation_contract": subsystem_runtime["validation_contract"],
            "asset_path": subsystem_runtime["asset_path"],
        },
        "timestamp": _timestamp(),
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    receipt = write_receipt(
        stage_name=config["proof_stage_name"],
        agent_name="legitimacy_runner",
        input_payload={
            "compile_target": compile_target,
            "project_id": project_id,
            "target_ref": target_ref,
        },
        output_payload=manifest,
        previous_receipt=previous_receipt,
        output_dir=str(output_dir),
    )

    receipt_path = output_dir / f"receipt_{config['proof_stage_name']}_{receipt['receipt_id'][:8]}.json"
    manifest["proof_receipt"] = {
        "stage_name": receipt["stage_name"],
        "agent_name": receipt["agent_name"],
        "receipt_id": receipt["receipt_id"],
        "previous_receipt_hash": receipt["previous_receipt_hash"],
    }
    manifest["output_files"].append({"kind": "receipt", "path": str(receipt_path)})
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return manifest, receipt


def _extract_cognitive_rhythm_metrics(manifest_candidate: Optional[dict]) -> dict:
    """Extract cognitive rhythm validator metrics from a manifest candidate if available."""
    if not manifest_candidate:
        return {}
    crv = manifest_candidate.get("assembly_decisions", {}).get("cognitive_rhythm_validator", {})
    if not crv:
        return {}
    metrics = crv.get("metrics", {})
    return {
        "recovery_ratio": metrics.get("recovery_ratio"),
        "mismatch_resolution_ratio": metrics.get("mismatch_resolution_ratio"),
        "peak_end_focus_score": metrics.get("peak_end_focus_score"),
        "continuity_anchor_ratio": metrics.get("continuity_anchor_ratio"),
        "reset_space_ratio": metrics.get("reset_space_ratio"),
        "overall_score": crv.get("score"),
    }


def build_scene_legitimacy_context(
    parsed_result: dict,
    resolved_beats: list[dict],
    manifest_candidate: Optional[dict] = None,
) -> tuple[dict, dict, str]:
    """Build the minimal runtime context needed for Scene Builder legitimacy."""
    subsystem_runtime = load_compiled_subsystem_runtime_asset(
        "scene_builder",
        STAGE_SUBSYSTEM_ID_MAP["scene_builder"],
    )
    project_id = parsed_result.get("project_id", "")
    beats = manifest_candidate.get("beats", resolved_beats) if manifest_candidate else resolved_beats
    last_beat = beats[-1] if beats else {}
    previous_beat = beats[-2] if len(beats) > 1 else {}
    total_duration = parsed_result.get("total_duration_sec", 0.0)

    scene_packet = {
        "arc_stage": str(last_beat.get("arc_stage") or "VISION").upper(),
        "directive_count": 3,
        "directive_density_score": 0.9,
        "color_temperature_k": last_beat.get("color_temperature_k", 5600),
        "motion_profile": last_beat.get("motion_profile", "breathing"),
        "pace_profile": last_beat.get("pace_profile", "measured"),
        "framing": last_beat.get("framing", "mcu"),
        "target_arousal_band": [0.4, 1.0],
        "cls_budget_remaining": 2,
        "selected_subsystems": subsystem_runtime["active_subsystems"],
    }
    neighbor_context = {
        "previous": {
            "color_temperature_k": previous_beat.get("color_temperature_k", 4200),
            "motion_profile": previous_beat.get("motion_profile", "static"),
            "pace_profile": previous_beat.get("pace_profile", "slow"),
            "framing": previous_beat.get("framing", "wide"),
        }
    }
    context = {
        "scene_packet": scene_packet,
        "neighbor_context": neighbor_context,
        "project_evidence": {
            "source_types": parsed_result.get(
                "evidence_source_types",
                ["transcript", "project_dna", "subsystem_evidence"],
            )
        },
        "subsystem_evidence": {
            "active_subsystems": subsystem_runtime["active_subsystems"],
            "thresholds": subsystem_runtime["thresholds"],
            "validation_contract": subsystem_runtime["validation_contract"],
        },
        "resolved_color": {
            "pad_arousal": parsed_result.get("resolved_pad_arousal", 0.72),
            "kelvin_delta_from_previous": abs(
                scene_packet["color_temperature_k"] - neighbor_context["previous"]["color_temperature_k"]
            ),
        },
        "resolved_motion": {
            "cls_cost": parsed_result.get("motion_cls_cost", 1)
        },
        "audio_sync_plan": {
            "max_offset_ms": parsed_result.get("max_audio_offset_ms", 20)
        },
        "sequence_metrics": {
            "vision_duration_sec": parsed_result.get("vision_duration_sec", max(10.0, total_duration * 0.25)),
            "hook_asl_target_sec": subsystem_runtime["thresholds"].get("CS-025", {}).get("target_hook_asl_seconds"),
            "peak_end_budget_multiplier": subsystem_runtime["thresholds"].get("CS-011", {}).get("peak_end_budget_multiplier", 2.0),
            "cognitive_rhythm": _extract_cognitive_rhythm_metrics(manifest_candidate),
        },
        "evidence_refs": sorted(set([
            parsed_result.get("beat_cluster_id", ""),
            parsed_result.get("arc_type", ""),
            subsystem_runtime["asset_path"],
            *subsystem_runtime["evidence_refs"],
        ])),
    }
    target_ref = {
        "beat_cluster_id": parsed_result.get("beat_cluster_id", ""),
        "manifest_id": (manifest_candidate or {}).get("manifest_id"),
        "arc_type": parsed_result.get("arc_type", ""),
    }
    return context, target_ref, project_id


def _build_prediction_error_gate_diagnosis(plan: dict) -> dict:
    gate = plan.get("regeneration_decisions", {}).get("prediction_error_gate", {})
    if gate.get("removed_surprise"):
        surprise_failure_mode = "SURPRISE_COLLAPSE"
    elif gate.get("over_amplified_surprise"):
        surprise_failure_mode = "SURPRISE_OVERLOAD"
    else:
        surprise_failure_mode = None
    return {
        "subsystem_id": "CS-033",
        "verdict": gate.get("verdict"),
        "surprise_failure_mode": surprise_failure_mode,
        "surprise_delta": gate.get("surprise_delta"),
        "legibility_loss": gate.get("legibility_loss"),
    }


def build_regeneration_legitimacy_context(
    request: dict,
    plan: dict,
    fingerprint_entry: dict,
) -> tuple[dict, dict, str]:
    """Build the minimal runtime context needed for editor regeneration legitimacy."""
    subsystem_runtime = load_compiled_subsystem_runtime_asset(
        "editor_regeneration",
        STAGE_SUBSYSTEM_ID_MAP["editor_regeneration"],
    )
    beat_index = request["beat_index"]
    mode = request["mode"]
    changed_paths = request.get("changed_paths")
    if changed_paths is None:
        changed_paths = [f"/beats/{beat_index}/video_clip_url"]
        if mode in {"T2I_ONLY", "BOTH"}:
            changed_paths.append(f"/beats/{beat_index}/fallback_image_url")
        if mode == "I2V_ONLY":
            changed_paths.append(f"/beats/{beat_index}/motion_profile")

    context = {
        "manifest_patch_request": {
            "target_beat_index": beat_index,
            "changed_paths": changed_paths,
            "off_target_drift_count": request.get("off_target_drift_count"),
            "mutation_compression_score": request.get("mutation_compression_score"),
        },
        "beat_context": {
            "arc_stage": request.get("arc_stage", "CHALLENGE"),
            "sequence_pad_delta_valid": request.get("sequence_pad_delta_valid", True),
            "post_regen_sync_offset_ms": request.get("post_regen_sync_offset_ms", 10),
            "active_subsystems": subsystem_runtime["active_subsystems"],
        },
        "subsystem_evidence": {
            "active_subsystems": subsystem_runtime["active_subsystems"],
            "thresholds": subsystem_runtime["thresholds"],
            "validation_contract": subsystem_runtime["validation_contract"],
        },
        "fingerprint_entry": {
            "history_step_present": len(fingerprint_entry.get("regeneration_history", [])) > 0,
            "active_fingerprint_id": fingerprint_entry.get("active_fingerprint_id"),
        },
        "patch_selection": plan.get("patch_selection", {}),
        "regeneration_decisions": plan.get("regeneration_decisions", {}),
        "prediction_error_gate_diagnosis": _build_prediction_error_gate_diagnosis(plan),
        "revision_note": request.get("revision_note", ""),
        "evidence_refs": sorted(set([
            fingerprint_entry.get("fingerprint", {}).get("fingerprint_id", ""),
            request.get("revision_note", ""),
            subsystem_runtime["asset_path"],
            *subsystem_runtime["evidence_refs"],
        ])),
    }
    target_ref = {
        "beat_index": beat_index,
        "mode": mode,
        "fingerprint_id": fingerprint_entry.get("fingerprint", {}).get("fingerprint_id", ""),
    }
    return context, target_ref, ""