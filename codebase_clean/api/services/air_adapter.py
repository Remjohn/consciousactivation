from __future__ import annotations

from typing import Any, Mapping

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.repositories.air_repository import ObjectNotFound, StoredAirObject


class PortfolioNotFound(Exception):
    pass


class ScriptNotFound(Exception):
    pass


class PortfolioNotOpen(Exception):
    pass


class CandidateJudgmentsIncomplete(Exception):
    def __init__(self, missing: set[str], extra: set[str]):
        self.missing, self.extra = missing, extra
        super().__init__(f"missing={sorted(missing)} extra={sorted(extra)}")


class UnknownCandidate(Exception):
    pass


class SelectionNotSupportedByScores(Exception):
    def __init__(self, decision: str, actual_selected: Mapping[str, Any] | None):
        self.decision, self.actual_selected = decision, actual_selected
        super().__init__(f"decision={decision} actual_selected={actual_selected}")


class ScriptAlreadyApproved(Exception):
    pass


class ScriptNotApproved(Exception):
    pass


def _get_typed(air: AirApplication, object_id: str, expected_type: str, not_found_exc: type[Exception]) -> StoredAirObject:
    try:
        stored = air.repository.get_object(object_id)
    except ObjectNotFound as exc:
        raise not_found_exc(object_id) from exc
    if stored.object_type != expected_type:
        raise not_found_exc(object_id)
    return stored


def get_portfolio(air: AirApplication, portfolio_id: str) -> StoredAirObject:
    return _get_typed(air, portfolio_id, "activation_hypothesis_portfolio", PortfolioNotFound)


def get_script(air: AirApplication, script_id: str) -> StoredAirObject:
    return _get_typed(air, script_id, "final_script_package", ScriptNotFound)


def resolve_batch_refs(air: AirApplication, script: StoredAirObject) -> dict[str, Any]:
    """Returns either a full BatchCompilationRefs dict or {"reason": ...}."""
    if not script.payload["operator_approved"]:
        return {"reason": "SCRIPT_NOT_APPROVED"}
    script_ref = script.immutable_ref()
    edges = air.repository.list_edges(script.object_id, outgoing=False)
    contracts: list[StoredAirObject] = []
    for edge in edges:
        if edge["relation_type"] != "governs_transfer_of":
            continue
        try:
            source = air.repository.get_object(edge["source_object_id"])
        except ObjectNotFound:
            continue
        if source.object_type != "activation_transfer_contract":
            continue
        if dict(source.payload["final_script_ref"]) != script_ref:
            continue  # governs a different revision of this same object_id
        contracts.append(source)
    if not contracts:
        return {"reason": "NO_TRANSFER_CONTRACT_YET"}
    chosen = max(contracts, key=lambda c: c.created_at_utc)
    return {
        "final_script_ref": script_ref,
        "semantic_program_ref": dict(script.payload["program_ref"]),  # AIR name -> Pipeline name projection
        "archetype_coalition_ref": dict(script.payload["archetype_coalition_ref"]),
        "primitive_coalition_ref": dict(script.payload["primitive_coalition_ref"]),
        "activation_transfer_contract_ref": chosen.immutable_ref(),
    }


def _matches_existing_promotion(air: AirApplication, promoted: StoredAirObject, request: Mapping[str, Any]) -> bool:
    """True only if `request` would have produced exactly the promotion
    already recorded on `promoted` -- not just the same selected_hypothesis_id
    and authority_decision_ref, but the same per-candidate gate outcomes and
    dimension scores too. Without this, a genuinely different request that
    happens to name the same winner and reuse (or collide on) the same
    authority_decision_ref would be silently treated as a replay and handed
    the stale cached result instead of being evaluated -- confirmed as a real
    gap by direct testing, not merely a theoretical one."""
    p = promoted.payload
    promotion_ref = p.get("promotion_ref")
    already_selected = p.get("selected_hypothesis_ref") or {}
    if promotion_ref is None or already_selected.get("object_id") != request["selected_hypothesis_id"]:
        return False
    try:
        promotion = air.repository.get_object(promotion_ref["object_id"])
    except ObjectNotFound:
        return False
    if dict(promotion.payload.get("authority_decision_ref") or {}) != dict(request["authority_decision_ref"]):
        return False

    judgments = {j["hypothesis_id"]: j for j in request["candidate_judgments"]}
    candidate_ids = {ref["object_id"] for ref in p["candidate_refs"]}
    if set(judgments) != candidate_ids:
        return False

    for gate_ref in p.get("gate_result_refs", []):
        try:
            gate = air.repository.get_object(gate_ref["object_id"])
        except ObjectNotFound:
            return False
        hid = gate.payload["hypothesis_ref"]["object_id"]
        judgment = judgments.get(hid)
        if judgment is None:
            return False
        expected_outcomes = judgment["gate_outcomes"]
        for check in gate.payload["checks"]:
            if expected_outcomes.get(check["gate"]) != (check["verdict"] == "PASS"):
                return False

    comparison_ref = (p.get("comparative_evaluation_refs") or [None])[0]
    if comparison_ref is None:
        return False
    try:
        comparison = air.repository.get_object(comparison_ref["object_id"])
    except ObjectNotFound:
        return False
    for row in comparison.payload["candidate_scores"]:
        hid = row["hypothesis_ref"]["object_id"]
        judgment = judgments.get(hid)
        if judgment is None or dict(row["dimension_scores_micros"]) != dict(judgment["dimension_scores_micros"]):
            return False

    return True


def _reconstruct_promoted_selection(air: AirApplication, promoted: StoredAirObject) -> dict[str, Any]:
    """Rebuilds the exact response select_hypothesis returned for the call
    that promoted `promoted`, by reading already-stored objects only -- no
    AIR writes are attempted. See select_hypothesis for why this exists."""
    p = promoted.payload
    comparison_ref = dict(p["comparative_evaluation_refs"][0])
    comparison = air.repository.get_object(comparison_ref["object_id"])
    stopping_ref = dict(p["stopping_receipt_ref"])
    stopping = air.repository.get_object(stopping_ref["object_id"])
    promotion_ref = dict(p["promotion_ref"])
    promotion = air.repository.get_object(promotion_ref["object_id"])
    return {
        "portfolio": promoted.to_dict(),
        "decision": comparison.payload["decision"],
        "stop_reason": stopping.payload["stop_reason"],
        "selected_hypothesis_ref": dict(p["selected_hypothesis_ref"]),
        "comparison_ref": comparison_ref,
        "stopping_receipt_ref": stopping_ref,
        "planned_pack_ref": dict(promotion.payload["planned_pack_ref"]),
        "promotion_ref": promotion_ref,
    }


def select_hypothesis(air: AirApplication, portfolio_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    current = get_portfolio(air, portfolio_id)

    # --- deviation from the spec's literal sample code -----------------
    # The spec's own text raises PortfolioNotOpen unconditionally whenever
    # portfolio_state != "OPEN". That makes AC-004 (identical idempotency_key
    # replay must return the same 200) impossible to satisfy: a successful
    # first call always leaves the portfolio PROMOTED, so the very next call
    # -- even with the exact same idempotency_key and body -- would always
    # hit this guard.
    #
    # A more surgical fix (re-run the same sub-calls against the portfolio's
    # last-OPEN historical revision, relying on AIR's own idempotency-key
    # dedupe to short-circuit) does NOT work either: every AIR write method
    # here calls production_common.py::require_air_ref on portfolio_ref
    # *before* reaching the idempotency-key check inside store_object, and
    # require_air_ref always resolves ref["object_id"] to the object's
    # *current* revision (repository.get_object has no revision pin here).
    # Once the portfolio is at revision 2 (PROMOTED), passing revision 1's
    # ref fails with a hash-mismatch ValueError regardless of idempotency_key
    # -- confirmed by direct execution, not just reading the code.
    #
    # Fix: when portfolio_state isn't OPEN, check whether the *existing*
    # promotion already reflects exactly this request's content (same
    # selected_hypothesis_id, same authority_decision_ref, AND the same
    # per-candidate gate outcomes and dimension scores already stored on the
    # existing gate/comparison objects -- see _matches_existing_promotion).
    # If so, this is a replay of an already-completed selection: reconstruct
    # and return the same response by reading already-stored objects,
    # performing zero AIR writes. If not, this is a genuinely different/new
    # attempt against an already-decided portfolio, and PortfolioNotOpen is
    # the correct, honest answer -- preserving AC-007.
    if current.payload["portfolio_state"] != "OPEN":
        if _matches_existing_promotion(air, current, request):
            return _reconstruct_promoted_selection(air, current)
        raise PortfolioNotOpen(current.payload["portfolio_state"])

    portfolio = current

    candidate_refs = list(portfolio.payload["candidate_refs"])
    candidate_ids = {ref["object_id"] for ref in candidate_refs}
    judgments = {j["hypothesis_id"]: j for j in request["candidate_judgments"]}
    judged_ids = set(judgments)
    if candidate_ids != judged_ids:
        raise CandidateJudgmentsIncomplete(candidate_ids - judged_ids, judged_ids - candidate_ids)
    if request["selected_hypothesis_id"] not in candidate_ids:
        raise UnknownCandidate(request["selected_hypothesis_id"])

    idem = request["idempotency_key"]
    authority = dict(request["authority"])
    portfolio_ref = portfolio.immutable_ref()

    gate_refs: list[dict[str, str]] = []
    for ref in candidate_refs:
        judgment = judgments[ref["object_id"]]
        gate = air.hypotheses.gate_hypothesis(
            receipt_id=f"{portfolio_id}:gate:{ref['object_id']}",
            version="1.0.0",
            authority=authority,
            portfolio_ref=portfolio_ref,
            hypothesis_ref=ref,
            gate_profile_ref=request["gate_profile_ref"],
            evaluator_actor_id=request["evaluator_actor_id"],
            producer_actor_id=judgment["producer_actor_id"],
            outcomes=judgment["gate_outcomes"],
            evidence_refs=request["evidence_refs"],
            idempotency_key=f"{idem}:gate:{ref['object_id']}",
        )["object"]
        gate_refs.append({"object_id": gate["object_id"], "version": gate["semantic_version"], "sha256": gate["canonical_sha256"]})

    comparison = air.hypotheses.compare_portfolio(
        receipt_id=f"{portfolio_id}:comparison",
        version="1.0.0",
        authority=authority,
        portfolio_ref=portfolio_ref,
        evaluation_profile_ref=request["evaluation_profile_ref"],
        evaluator_actor_id=request["evaluator_actor_id"],
        producer_actor_ids=[judgments[ref["object_id"]]["producer_actor_id"] for ref in candidate_refs],
        gate_receipt_refs=gate_refs,
        candidate_scores={rid: dict(j["dimension_scores_micros"]) for rid, j in judgments.items()},
        decisive_margin_micros=request["decisive_margin_micros"],
        idempotency_key=f"{idem}:comparison",
    )["object"]
    comparison_ref = {"object_id": comparison["object_id"], "version": comparison["semantic_version"], "sha256": comparison["canonical_sha256"]}

    decision = comparison["payload"]["decision"]
    actual_selected = comparison["payload"].get("selected_hypothesis_ref")
    if decision != "DECISIVE_WINNER" or (actual_selected or {}).get("object_id") != request["selected_hypothesis_id"]:
        raise SelectionNotSupportedByScores(decision, actual_selected)

    selected_ref = dict(actual_selected)

    stopping = air.hypotheses.stop_search(
        receipt_id=f"{portfolio_id}:stop",
        version="1.0.0",
        authority=authority,
        portfolio_ref=portfolio_ref,
        evaluation_ref=comparison_ref,
        remaining_budget=request.get("remaining_budget") or dict(portfolio.payload["search_budget"]),
        diversity_exhausted=request["diversity_exhausted"],
        idempotency_key=f"{idem}:stop",
    )["object"]
    stopping_ref = {"object_id": stopping["object_id"], "version": stopping["semantic_version"], "sha256": stopping["canonical_sha256"]}

    planned_pack = air.hypotheses.store_planned_pack(
        {
            "pack_id": f"{portfolio_id}:planned-pack",
            "version": "1.0.0",
            "authority": authority,
            "lifecycle_state": "approved",
            "epistemic_state": "planned",
            "portfolio_ref": portfolio_ref,
            "selected_hypothesis_ref": selected_ref,
            "matrix_of_edging_ref": request["matrix_of_edging_ref"],
            "role_tension_ref": request["role_tension_ref"],
            "source_refs": request["source_refs"],
            "limitations": ["development evidence; no real-human activation claim"],
        },
        idempotency_key=f"{idem}:planned-pack",
    )["object"]
    planned_pack_ref = {"object_id": planned_pack["object_id"], "version": planned_pack["semantic_version"], "sha256": planned_pack["canonical_sha256"]}

    promotion = air.hypotheses.promote(
        {
            "receipt_id": f"{portfolio_id}:promotion",
            "version": "1.0.0",
            "authority": authority,
            "portfolio_ref": portfolio_ref,
            "selected_hypothesis_ref": selected_ref,
            "stopping_receipt_ref": stopping_ref,
            "planned_pack_ref": planned_pack_ref,
            "authority_decision_ref": request["authority_decision_ref"],
        },
        idempotency_key=f"{idem}:promotion",
    )["object"]
    promotion_ref = {"object_id": promotion["object_id"], "version": promotion["semantic_version"], "sha256": promotion["canonical_sha256"]}

    current_revision = air.repository.get_object(portfolio_id).revision  # re-read; Governing Decision §3
    promoted = air.hypotheses.store_portfolio(
        {
            **portfolio.payload,
            "supersedes_ref": portfolio_ref,
            "gate_result_refs": gate_refs,
            "comparative_evaluation_refs": [comparison_ref],
            "portfolio_state": "PROMOTED",
            "stopping_receipt_ref": stopping_ref,
            "selected_hypothesis_ref": selected_ref,
            "promotion_ref": promotion_ref,
            "candidate_state_records": [
                {
                    "candidate_ref": ref,
                    "state": "PROMOTED" if ref["object_id"] == selected_ref["object_id"] else "ELIGIBLE",
                    "reason_codes": ["SELECTED_BY_DECISIVE_COMPARISON"] if ref["object_id"] == selected_ref["object_id"] else ["NOT_SELECTED"],
                    "caused_by_receipt_ref": promotion_ref if ref["object_id"] == selected_ref["object_id"] else comparison_ref,
                }
                for ref in candidate_refs
            ],
        },
        idempotency_key=f"{idem}:portfolio-promoted",
        expected_revision=current_revision,
    )["object"]  # ObjectVersionConflict -> 409 CONFLICT, surfaced by the router

    return {
        "portfolio": promoted,
        "decision": decision,
        "stop_reason": stopping["payload"]["stop_reason"],
        "selected_hypothesis_ref": selected_ref,
        "comparison_ref": comparison_ref,
        "stopping_receipt_ref": stopping_ref,
        "planned_pack_ref": planned_pack_ref,
        "promotion_ref": promotion_ref,
    }


def approve_script(air: AirApplication, script_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    script = get_script(air, script_id)
    if script.payload["operator_approved"] is True:
        raise ScriptAlreadyApproved(script_id)
    evaluation_refs = request.get("evaluation_refs") or list(script.payload["evaluation_receipt_refs"])
    idem = request["idempotency_key"]
    result = air.derivatives.approve_script(
        candidate_script_ref=script.immutable_ref(),
        operator_id=request["operator_id"],
        operator_decision_ref=request["operator_decision_ref"],
        evaluation_refs=evaluation_refs,
        rationale=request["rationale"],
        approval_idempotency_key=f"{idem}:approval",
        script_revision_idempotency_key=f"{idem}:script-revision",
    )
    approved_script = air.repository.get_object(script_id)  # re-read current (now-approved) revision
    return {"approval": result["approval"]["object"], "script": approved_script}


def create_transfer_contract(air: AirApplication, script_id: str, request: Mapping[str, Any]) -> dict[str, Any]:
    script = get_script(air, script_id)
    if not script.payload["operator_approved"]:
        raise ScriptNotApproved(script_id)
    result = air.transfer.store_contract(
        {
            "contract_id": f"{script_id}:transfer-contract",
            "version": "1.0.0",
            "authority": dict(request["authority"]),
            # CORRECTED against production_domain.py::_validate_transfer_contract,
            # read directly: it does not override _base()'s lifecycle_required/
            # epistemic_required defaults (both True), so activation_transfer_
            # contract requires lifecycle_state/epistemic_state like every other
            # lifecycle-tracked object. The spec's literal Stage 1 payload omits
            # both, which would make every transfer-contract creation raise
            # AirValidationError. A transfer contract can only be created for an
            # already-approved script (this endpoint's own precondition), so it
            # carries the same governance level as the script it governs --
            # mirroring DerivativeService.approve_script's own successor-revision
            # state ("approved" / "operator_confirmed").
            "lifecycle_state": "approved",
            "epistemic_state": "operator_confirmed",
            "source_expression_refs": request["source_expression_refs"],
            "source_package_refs": request["source_package_refs"],
            "expression_moment_refs": request["expression_moment_refs"],
            "reaction_receipt_refs": request["reaction_receipt_refs"],
            "selected_hypothesis_ref": request["selected_hypothesis_ref"],
            "role_tension_ref": dict(script.payload["role_tension_ref"]),
            "primitive_coalition_ref": dict(script.payload["primitive_coalition_ref"]),
            "archetype_coalition_ref": dict(script.payload["archetype_coalition_ref"]),
            "final_script_ref": script.immutable_ref(),
            "must_survive_properties": request["must_survive_properties"],
            "transformation_rules": request["transformation_rules"],
            "required_changes": request["required_changes"],
            "wrong_reading_lock_refs": list(script.payload["wrong_reading_lock_refs"]),
            "evaluation_profile_ref": request["evaluation_profile_ref"],
            "limitations": request["limitations"],
        },
        idempotency_key=request["idempotency_key"],
    )
    return result["object"]
