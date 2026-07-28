from __future__ import annotations
from typing import Any
from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, StoredAirObject
from .air_adapter import resolve_batch_refs


def _ref(obj: dict[str, Any]) -> dict[str, str]:
    return {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]}


def project_candidate_summary(air: AirApplication, ref: dict[str, str], portfolio_payload: dict[str, Any]) -> dict[str, Any]:
    hypothesis = air.repository.get_object(ref["object_id"])
    p = hypothesis.payload
    state = next(
        (r["state"] for r in portfolio_payload["candidate_state_records"] if r["candidate_ref"]["object_id"] == ref["object_id"]),
        "PROPOSED",
    )
    gate_result = None
    for gref in portfolio_payload.get("gate_result_refs", []):
        gate = air.repository.get_object(gref["object_id"])
        if gate.payload["hypothesis_ref"]["object_id"] == ref["object_id"]:
            gate_result = {
                "receipt_ref": gref,
                "overall": gate.payload["overall"],
                "checks": [{"gate": c["gate"], "applicability": c["applicability"], "verdict": c["verdict"], "reason": c["reason"]} for c in gate.payload["checks"]],
            }
            break
    comparative_score = None
    for cref in portfolio_payload.get("comparative_evaluation_refs", []):
        comparison = air.repository.get_object(cref["object_id"])
        for row in comparison.payload["candidate_scores"]:
            if row["hypothesis_ref"]["object_id"] == ref["object_id"]:
                comparative_score = {"dimension_scores_micros": row["dimension_scores_micros"], "total_micros": row["total_micros"], "eligible": row["eligible"]}
                break
    return {
        "hypothesis_ref": ref,
        "psychological_role": p["psychological_role"],
        "tension": p["tension"],
        "activation_directions": p["activation_directions"],
        "pressure_path": p["pressure_path"],
        "stance": p["stance"],
        "stakes": p["stakes"],
        "pressure_dose": p["pressure_dose"],
        "participation_design": p["participation_design"],
        "smallest_useful_commitment": p["smallest_useful_commitment"],
        "diversity_signature": p["diversity_signature"],
        "state": state,
        "gate_result": gate_result,
        "comparative_score": comparative_score,
    }


def project_portfolio_detail(air: AirApplication, portfolio: StoredAirObject) -> dict[str, Any]:
    p = portfolio.payload
    return {
        "portfolio_ref": portfolio.immutable_ref(),
        "portfolio_state": p["portfolio_state"],
        "search_policy_ref": p["search_policy_ref"],
        "search_budget": p["search_budget"],
        "upstream_snapshot_refs": p["upstream_snapshot_refs"],
        "candidates": [project_candidate_summary(air, ref, p) for ref in p["candidate_refs"]],
        "gate_result_refs": p["gate_result_refs"],
        "comparative_evaluation_refs": p["comparative_evaluation_refs"],
        "stopping_receipt_ref": p.get("stopping_receipt_ref"),
        "selected_hypothesis_ref": p.get("selected_hypothesis_ref"),
        "promotion_ref": p.get("promotion_ref"),
    }


def project_script_detail(air: AirApplication, script: StoredAirObject) -> dict[str, Any]:
    p = script.payload
    return {
        "script_ref": script.immutable_ref(),
        "lifecycle_state": script.lifecycle_state,
        "epistemic_state": script.epistemic_state,
        "operator_approved": p["operator_approved"],
        "composition_eligible": p["composition_eligible"],
        "program_ref": p["program_ref"],
        "proposal_ref": p["proposal_ref"],
        "segments": p["segments"],
        "script_sha256": p["script_sha256"],
        "evaluation_receipt_refs": p["evaluation_receipt_refs"],
        "source_lineage_refs": p["source_lineage_refs"],
        "role_tension_ref": p["role_tension_ref"],
        "primitive_coalition_ref": p["primitive_coalition_ref"],
        "archetype_coalition_ref": p["archetype_coalition_ref"],
        "brand_context_ref": p["brand_context_ref"],
        "voice_dna_ref": p["voice_dna_ref"],
        "distillation_receipt_refs": p["distillation_receipt_refs"],
        "ccv_axes": p["ccv_axes"],
        "wrong_reading_lock_refs": p["wrong_reading_lock_refs"],
        "maximum_claim": p["maximum_claim"],
        "approval_receipt_ref": p.get("approval_receipt_ref"),
        "limitations": p["limitations"],
        "batch_compilation_refs": resolve_batch_refs(air, script),
    }
