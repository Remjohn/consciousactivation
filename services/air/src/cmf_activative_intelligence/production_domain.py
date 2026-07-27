from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any, Callable

from .domain import (
    ActivationDomain,
    EpistemicState,
    LifecycleState,
    ResponsibleLayer,
    _authority,
    _base,
    _boolean,
    _enum,
    _integer,
    _is_sequence,
    _mapping_list,
    _ref,
    _refs,
    _strict_fields,
    _string,
    _strings,
)

_SHA256 = re.compile(r"^[a-f0-9]{64}$")


HYPOTHESIS_GATES = (
    "SOURCE_FIDELITY",
    "EPISTEMIC_LEGALITY",
    "IDENTITY_FIT",
    "DOMAIN_FIT",
    "OPERATOR_CONSTRAINTS",
    "FATAL_PRIMITIVE_CONFLICT",
    "WRONG_READING_LOCKS",
    "LINEAGE_COMPLETE",
    "CURRENT_VERSION",
    "SEMANTIC_DUPLICATE",
)

EVALUATION_DIMENSIONS = (
    "source_fidelity",
    "role_tension_integrity",
    "primitive_coalition_fitness",
    "archetype_fit",
    "edge_integrity",
    "anti_centroid_distinctiveness",
    "execution_feasibility",
)

TRANSFER_CHECKPOINTS = (
    "SOURCE_TO_EXPRESSION_MOMENT",
    "EXPRESSION_MOMENT_TO_FINAL_SCRIPT",
    "FINAL_SCRIPT_TO_COMPOSITION",
    "COMPOSITION_TO_RENDER",
    "RENDER_TO_PLATFORM",
)


def _sha(value: Any, field: str, issues: list[str]) -> None:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        issues.append(f"{field} must be 64 lowercase hex characters")


def _optional_ref(payload: Mapping[str, Any], field: str, issues: list[str]) -> None:
    if field in payload:
        _ref(payload.get(field), field, issues, nullable=True)


def _strict_nested(
    value: Any,
    field: str,
    issues: list[str],
    *,
    required: Sequence[str],
    optional: Sequence[str] = (),
) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an object")
        return None
    _strict_fields(value, required=required, optional=optional, issues=issues)
    return value


def _string_mapping(
    value: Any,
    field: str,
    issues: list[str],
    *,
    minimum: int = 0,
    integer_values: bool = False,
) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an object")
        return {}
    result: dict[str, Any] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            issues.append(f"{field} keys must be non-empty strings")
            continue
        if integer_values:
            if not isinstance(item, int) or isinstance(item, bool):
                issues.append(f"{field}[{key!r}] must be an integer")
                continue
        else:
            if not isinstance(item, str) or not item.strip():
                issues.append(f"{field}[{key!r}] must be a non-empty string")
                continue
        result[key] = item
    if len(result) < minimum:
        issues.append(f"{field} must contain at least {minimum} item(s)")
    return result


def _validate_search_budget(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=(
            "maximum_candidate_count",
            "maximum_round_count",
            "maximum_model_tokens",
            "maximum_provider_cost_micros",
            "consumed_candidate_count",
            "consumed_round_count",
            "consumed_model_tokens",
            "consumed_provider_cost_micros",
        ),
    )
    if obj is None:
        return
    for name in (
        "maximum_candidate_count",
        "maximum_round_count",
        "maximum_model_tokens",
        "maximum_provider_cost_micros",
        "consumed_candidate_count",
        "consumed_round_count",
        "consumed_model_tokens",
        "consumed_provider_cost_micros",
    ):
        minimum = 1 if name in {"maximum_candidate_count", "maximum_round_count"} else 0
        _integer(obj, name, issues, minimum=minimum)
    pairs = (
        ("consumed_candidate_count", "maximum_candidate_count"),
        ("consumed_round_count", "maximum_round_count"),
        ("consumed_model_tokens", "maximum_model_tokens"),
        ("consumed_provider_cost_micros", "maximum_provider_cost_micros"),
    )
    for consumed, maximum in pairs:
        if isinstance(obj.get(consumed), int) and isinstance(obj.get(maximum), int):
            if int(obj[consumed]) > int(obj[maximum]):
                issues.append(f"{field}.{consumed} cannot exceed {maximum}")


def _validate_counteractivation(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("risk", "trigger", "mitigation", "evidence_refs"),
    )
    if obj is None:
        return
    _string(obj, "risk", issues)
    _string(obj, "trigger", issues)
    _string(obj, "mitigation", issues)
    _refs(obj, "evidence_refs", issues, minimum=1)


def _validate_diversity_signature(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("signature_id", "axes", "proof_sha256"),
        optional=("compared_candidate_refs",),
    )
    if obj is None:
        return
    _string(obj, "signature_id", issues)
    axes = _string_mapping(obj.get("axes"), f"{field}.axes", issues, minimum=1)
    permitted = {
        "psychological_role",
        "tension",
        "activation_direction_set",
        "pressure_path",
        "primitive_coalition_hypothesis_ref",
        "relationship_move",
        "stance",
        "counteractivation_strategy",
        "smallest_commitment",
    }
    unknown = set(axes) - permitted
    if unknown:
        issues.append(f"{field}.axes contains unsupported diversity axes: {sorted(unknown)}")
    _sha(obj.get("proof_sha256"), f"{field}.proof_sha256", issues)
    if "compared_candidate_refs" in obj:
        refs = obj.get("compared_candidate_refs")
        if not _is_sequence(refs):
            issues.append(f"{field}.compared_candidate_refs must be an array")
        else:
            for index, ref in enumerate(refs):
                _ref(ref, f"{field}.compared_candidate_refs[{index}]", issues)


def _validate_activation_hypothesis(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="hypothesis_id",
        extra_required=(
            "activation_domain",
            "source_kind",
            "source_refs",
            "canonical_interview_source_package_refs",
            "identity_dna_ref",
            "context_premise_ref",
            "matrix_of_edging_ref",
            "edge_product_candidate_ref",
            "objective_ref",
            "psychological_role",
            "tension",
            "activation_directions",
            "pressure_path",
            "stance",
            "stakes",
            "pressure_dose",
            "participation_design",
            "smallest_useful_commitment",
            "counteractivation_hypotheses",
            "inherited_wrong_reading_locks",
            "additional_wrong_reading_locks",
            "primitive_application_refs",
            "diversity_signature",
            "proposal_binding_ref",
            "proposal_attempt_ref",
        ),
        extra_optional=("interview_provenance", "repairs_hypothesis_ref"),
    )
    _enum(payload, "activation_domain", {item.value for item in ActivationDomain}, issues)
    source_kind = _enum(
        payload,
        "source_kind",
        {
            "interview_expression",
            "public_comment",
            "direct_message_reply",
            "authored_source",
            "live_premise",
            "research_synthesis",
            "operator_supplied",
            "legacy_migrated",
        },
        issues,
    )
    _refs(payload, "source_refs", issues, minimum=1)
    packages = _refs(payload, "canonical_interview_source_package_refs", issues)
    for field in (
        "identity_dna_ref",
        "context_premise_ref",
        "matrix_of_edging_ref",
        "edge_product_candidate_ref",
        "objective_ref",
        "proposal_binding_ref",
        "proposal_attempt_ref",
    ):
        _ref(payload.get(field), field, issues)
    _optional_ref(payload, "repairs_hypothesis_ref", issues)
    role = _string(payload, "psychological_role", issues)
    tension = _string(payload, "tension", issues)
    if role and tension and role.strip().lower() == tension.strip().lower():
        issues.append("psychological_role and tension must be distinct")
    _strings(payload, "activation_directions", issues, minimum=1, unique=True)
    permitted_dirs = {"MIRROR", "TARGET", "MORAL", "ASPIRATION", "CONTRADICTION", "CURIOSITY"}
    for value in payload.get("activation_directions", ()) if _is_sequence(payload.get("activation_directions")) else ():
        if value not in permitted_dirs:
            issues.append(f"activation_directions contains unsupported value: {value}")
    for field in (
        "pressure_path",
        "stance",
        "participation_design",
        "smallest_useful_commitment",
    ):
        _string(payload, field, issues)
    _strings(payload, "stakes", issues, minimum=1)
    _integer(payload, "pressure_dose", issues, minimum=0, maximum=5)
    for index, item in enumerate(_mapping_list(payload, "counteractivation_hypotheses", issues, minimum=1)):
        _validate_counteractivation(item, f"counteractivation_hypotheses[{index}]", issues)
    _refs(payload, "inherited_wrong_reading_locks", issues, minimum=1)
    _strings(payload, "additional_wrong_reading_locks", issues)
    _refs(payload, "primitive_application_refs", issues)
    _validate_diversity_signature(payload.get("diversity_signature"), "diversity_signature", issues)
    if payload.get("epistemic_state") not in {EpistemicState.PLANNED.value, EpistemicState.INFERRED.value}:
        issues.append("activation hypothesis epistemic_state must be planned or inferred")
    provenance = payload.get("interview_provenance")
    if source_kind == "interview_expression":
        if not packages:
            issues.append("interview_expression hypothesis requires canonical interview source package refs")
        obj = _strict_nested(
            provenance,
            "interview_provenance",
            issues,
            required=("reaction_receipt_refs", "expression_moment_refs"),
        )
        if obj is not None:
            _refs(obj, "reaction_receipt_refs", issues, minimum=1)
            _refs(obj, "expression_moment_refs", issues, minimum=1)
    elif provenance is not None:
        obj = _strict_nested(
            provenance,
            "interview_provenance",
            issues,
            required=("reaction_receipt_refs", "expression_moment_refs"),
        )
        if obj is not None:
            _refs(obj, "reaction_receipt_refs", issues, minimum=1)
            _refs(obj, "expression_moment_refs", issues, minimum=1)


def _validate_candidate_state_record(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("candidate_ref", "state", "reason_codes"),
        optional=("caused_by_receipt_ref", "prior_state_record_ref"),
    )
    if obj is None:
        return
    _ref(obj.get("candidate_ref"), f"{field}.candidate_ref", issues)
    _enum(
        obj,
        "state",
        {"PROPOSED", "GATE_REJECTED", "ELIGIBLE", "REPAIRED", "SUPERSEDED", "SELECTED", "PROMOTED"},
        issues,
    )
    _strings(obj, "reason_codes", issues)
    if "caused_by_receipt_ref" in obj:
        _ref(obj.get("caused_by_receipt_ref"), f"{field}.caused_by_receipt_ref", issues, nullable=True)
    if "prior_state_record_ref" in obj:
        _ref(obj.get("prior_state_record_ref"), f"{field}.prior_state_record_ref", issues, nullable=True)


def _validate_hypothesis_portfolio(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="portfolio_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "search_policy_ref",
            "search_budget",
            "upstream_snapshot_refs",
            "candidate_refs",
            "candidate_state_records",
            "gate_result_refs",
            "comparative_evaluation_refs",
            "portfolio_state",
        ),
        extra_optional=("stopping_receipt_ref", "selected_hypothesis_ref", "promotion_ref"),
    )
    _ref(payload.get("search_policy_ref"), "search_policy_ref", issues)
    _validate_search_budget(payload.get("search_budget"), "search_budget", issues)
    _refs(payload, "upstream_snapshot_refs", issues, minimum=1)
    candidates = _refs(payload, "candidate_refs", issues, minimum=1)
    records = _mapping_list(payload, "candidate_state_records", issues, minimum=1)
    for index, record in enumerate(records):
        _validate_candidate_state_record(record, f"candidate_state_records[{index}]", issues)
    record_ids = [str(item.get("candidate_ref", {}).get("object_id")) for item in records if isinstance(item.get("candidate_ref"), Mapping)]
    if candidates and sorted(ref["object_id"] for ref in candidates) != sorted(record_ids):
        issues.append("candidate_state_records must cover every candidate exactly once")
    _refs(payload, "gate_result_refs", issues)
    _refs(payload, "comparative_evaluation_refs", issues)
    state = _enum(payload, "portfolio_state", {"OPEN", "GATED", "COMPARED", "STOPPED", "PROMOTED", "CANCELLED", "SUPERSEDED"}, issues)
    _optional_ref(payload, "stopping_receipt_ref", issues)
    _optional_ref(payload, "selected_hypothesis_ref", issues)
    _optional_ref(payload, "promotion_ref", issues)
    if state in {"STOPPED", "PROMOTED"} and payload.get("stopping_receipt_ref") is None:
        issues.append(f"portfolio_state {state} requires stopping_receipt_ref")
    if state == "PROMOTED" and (payload.get("selected_hypothesis_ref") is None or payload.get("promotion_ref") is None):
        issues.append("PROMOTED portfolio requires selected_hypothesis_ref and promotion_ref")
    if state not in {"STOPPED", "PROMOTED"} and payload.get("promotion_ref") is not None:
        issues.append("promotion_ref is only valid for PROMOTED portfolio")


def _validate_gate_check(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("gate", "applicability", "verdict", "reason", "evidence_refs"),
    )
    if obj is None:
        return
    _enum(
        obj,
        "gate",
        {
            "SOURCE_FIDELITY",
            "EPISTEMIC_LEGALITY",
            "IDENTITY_FIT",
            "DOMAIN_FIT",
            "OPERATOR_CONSTRAINTS",
            "FATAL_PRIMITIVE_CONFLICT",
            "WRONG_READING_LOCKS",
            "LINEAGE_COMPLETE",
            "CURRENT_VERSION",
            "SEMANTIC_DUPLICATE",
        },
        issues,
    )
    applicability = _enum(obj, "applicability", {"APPLIES", "NOT_APPLICABLE"}, issues)
    verdict = _enum(obj, "verdict", {"PASS", "FAIL"}, issues)
    _string(obj, "reason", issues)
    refs = _refs(obj, "evidence_refs", issues)
    if applicability == "NOT_APPLICABLE" and not refs:
        issues.append(f"{field} NOT_APPLICABLE requires evidence")
    if applicability == "NOT_APPLICABLE" and verdict == "FAIL":
        issues.append(f"{field} cannot FAIL when NOT_APPLICABLE")


def _validate_hypothesis_gate_result(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "portfolio_ref",
            "hypothesis_ref",
            "gate_profile_ref",
            "evaluator_actor_id",
            "producer_actor_id",
            "checks",
            "overall",
            "input_hashes",
            "limitations",
        ),
    )
    for field in ("portfolio_ref", "hypothesis_ref", "gate_profile_ref"):
        _ref(payload.get(field), field, issues)
    evaluator = _string(payload, "evaluator_actor_id", issues)
    producer = _string(payload, "producer_actor_id", issues)
    if evaluator and producer and evaluator == producer:
        issues.append("hypothesis producer and gate evaluator must differ")
    checks = _mapping_list(payload, "checks", issues, minimum=1)
    for index, item in enumerate(checks):
        _validate_gate_check(item, f"checks[{index}]", issues)
    _enum(payload, "overall", {"ELIGIBLE", "INELIGIBLE"}, issues)
    hashes = _strings(payload, "input_hashes", issues, minimum=1, unique=True)
    for index, sha in enumerate(hashes):
        _sha(sha, f"input_hashes[{index}]", issues)
    _strings(payload, "limitations", issues)
    if payload.get("overall") == "ELIGIBLE":
        for item in checks:
            if item.get("applicability") == "APPLIES" and item.get("verdict") != "PASS":
                issues.append("ELIGIBLE gate result requires every applicable check to PASS")


def _validate_candidate_score(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("hypothesis_ref", "dimension_scores_micros", "total_micros", "eligible"),
    )
    if obj is None:
        return
    _ref(obj.get("hypothesis_ref"), f"{field}.hypothesis_ref", issues)
    scores = _string_mapping(obj.get("dimension_scores_micros"), f"{field}.dimension_scores_micros", issues, minimum=1, integer_values=True)
    for key, score in scores.items():
        if score < 0 or score > 1_000_000:
            issues.append(f"{field}.dimension_scores_micros[{key!r}] must be 0..1_000_000")
    _integer(obj, "total_micros", issues, minimum=0)
    _boolean(obj, "eligible", issues)


def _validate_comparative_evaluation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "portfolio_ref",
            "evaluation_profile_ref",
            "evaluator_actor_id",
            "producer_actor_ids",
            "candidate_scores",
            "decision",
            "decisive_margin_micros",
            "limitations",
        ),
        extra_optional=("selected_hypothesis_ref",),
    )
    _ref(payload.get("portfolio_ref"), "portfolio_ref", issues)
    _ref(payload.get("evaluation_profile_ref"), "evaluation_profile_ref", issues)
    evaluator = _string(payload, "evaluator_actor_id", issues)
    producers = _strings(payload, "producer_actor_ids", issues, minimum=1, unique=True)
    if evaluator and evaluator in producers:
        issues.append("comparative evaluator must differ from every producer")
    scores = _mapping_list(payload, "candidate_scores", issues, minimum=2)
    for index, item in enumerate(scores):
        _validate_candidate_score(item, f"candidate_scores[{index}]", issues)
    decision = _enum(payload, "decision", {"DECISIVE_WINNER", "AMBIGUOUS", "NO_ELIGIBLE_CANDIDATE"}, issues)
    _integer(payload, "decisive_margin_micros", issues, minimum=0)
    _optional_ref(payload, "selected_hypothesis_ref", issues)
    _strings(payload, "limitations", issues)
    if decision == "DECISIVE_WINNER" and payload.get("selected_hypothesis_ref") is None:
        issues.append("DECISIVE_WINNER requires selected_hypothesis_ref")
    if decision != "DECISIVE_WINNER" and payload.get("selected_hypothesis_ref") is not None:
        issues.append("selected_hypothesis_ref is forbidden without DECISIVE_WINNER")


def _validate_hypothesis_stopping(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("portfolio_ref", "stop_reason", "evidence_refs", "remaining_budget", "limitations"),
        extra_optional=("selected_hypothesis_ref", "operator_question"),
    )
    _ref(payload.get("portfolio_ref"), "portfolio_ref", issues)
    reason = _enum(
        payload,
        "stop_reason",
        {"DECISIVE_ELIGIBLE_WINNER", "SHARED_DEFECT", "DIVERSITY_EXHAUSTED", "BUDGET_BOUNDARY", "OPERATOR_OWNED_AMBIGUITY"},
        issues,
    )
    _refs(payload, "evidence_refs", issues, minimum=1)
    _validate_search_budget(payload.get("remaining_budget"), "remaining_budget", issues)
    _optional_ref(payload, "selected_hypothesis_ref", issues)
    if "operator_question" in payload and payload.get("operator_question") is not None:
        _string(payload, "operator_question", issues)
    _strings(payload, "limitations", issues)
    if reason == "DECISIVE_ELIGIBLE_WINNER" and payload.get("selected_hypothesis_ref") is None:
        issues.append("decisive winner stop requires selected_hypothesis_ref")
    if reason != "DECISIVE_ELIGIBLE_WINNER" and payload.get("selected_hypothesis_ref") is not None:
        issues.append("non-decisive stop cannot select a hypothesis")
    if reason == "OPERATOR_OWNED_AMBIGUITY" and not payload.get("operator_question"):
        issues.append("operator-owned ambiguity requires operator_question")


def _validate_planned_pack(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="pack_id",
        extra_required=(
            "portfolio_ref",
            "selected_hypothesis_ref",
            "matrix_of_edging_ref",
            "role_tension_ref",
            "source_refs",
            "limitations",
        ),
    )
    for field in ("portfolio_ref", "selected_hypothesis_ref", "matrix_of_edging_ref", "role_tension_ref"):
        _ref(payload.get(field), field, issues)
    _refs(payload, "source_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)
    if payload.get("epistemic_state") != EpistemicState.PLANNED.value:
        issues.append("planned activative intelligence pack must remain planned")


def _validate_hypothesis_promotion(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("portfolio_ref", "selected_hypothesis_ref", "stopping_receipt_ref", "planned_pack_ref", "authority_decision_ref"),
    )
    for field in ("portfolio_ref", "selected_hypothesis_ref", "stopping_receipt_ref", "planned_pack_ref", "authority_decision_ref"):
        _ref(payload.get(field), field, issues)


def _validate_derivative_input_manifest(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="manifest_id",
        extra_required=(
            "source_kind",
            "source_package_refs",
            "expression_moment_refs",
            "reaction_receipt_refs",
            "observed_activative_pack_ref",
            "selected_hypothesis_ref",
            "matrix_of_edging_ref",
            "role_tension_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "brand_context_ref",
            "voice_dna_ref",
            "visual_dna_ref",
            "objective_ref",
            "campaign_role",
            "category_id",
            "profile_id",
            "format_harness_ref",
            "wrong_reading_lock_refs",
            "limitations",
        ),
    )
    kind = _enum(payload, "source_kind", {"interview_expression", "operator_supplied", "authored_source", "research_synthesis"}, issues)
    _refs(payload, "source_package_refs", issues, minimum=1)
    moments = _refs(payload, "expression_moment_refs", issues)
    reactions = _refs(payload, "reaction_receipt_refs", issues)
    if kind == "interview_expression" and (not moments or not reactions):
        issues.append("interview_expression derivative input requires Expression Moment and Reaction Receipt refs")
    for field in (
        "observed_activative_pack_ref",
        "selected_hypothesis_ref",
        "matrix_of_edging_ref",
        "role_tension_ref",
        "primitive_coalition_ref",
        "archetype_coalition_ref",
        "brand_context_ref",
        "voice_dna_ref",
        "visual_dna_ref",
        "objective_ref",
        "format_harness_ref",
    ):
        _ref(payload.get(field), field, issues)
    for field in ("campaign_role", "category_id", "profile_id"):
        _string(payload, field, issues)
    if "format02" in str(payload.get("profile_id", "")).lower():
        issues.append("Format 02 remains deferred")
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_derivative_program(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="program_id",
        extra_required=(
            "input_manifest_ref",
            "derivative_type",
            "category_id",
            "profile_id",
            "source_ingredient_refs",
            "role_tension_ref",
            "matrix_of_edging_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "brand_context_ref",
            "voice_dna_ref",
            "visual_dna_ref",
            "allowed_transformation_classes",
            "maximum_claim",
            "wrong_reading_lock_refs",
            "evaluation_profile_ref",
            "allowed_tools",
            "denied_tools",
            "composition_authorized",
            "limitations",
        ),
    )
    for field in (
        "input_manifest_ref",
        "role_tension_ref",
        "matrix_of_edging_ref",
        "primitive_coalition_ref",
        "archetype_coalition_ref",
        "brand_context_ref",
        "voice_dna_ref",
        "visual_dna_ref",
        "evaluation_profile_ref",
    ):
        _ref(payload.get(field), field, issues)
    dtype = _enum(payload, "derivative_type", {"SOURCE_LED_SHORT", "CAROUSEL", "SUPERVISUAL", "ANIMATION_SCENE_PACKAGE", "ANIMATION_SHORT"}, issues)
    for field in ("category_id", "profile_id", "maximum_claim"):
        _string(payload, field, issues)
    if "format02" in str(payload.get("profile_id", "")).lower():
        issues.append("Format 02 remains deferred")
    _refs(payload, "source_ingredient_refs", issues, minimum=1)
    transforms = _strings(payload, "allowed_transformation_classes", issues, minimum=1, unique=True)
    permitted = {"VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE"}
    if set(transforms) - permitted:
        issues.append("allowed_transformation_classes contains unsupported class")
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    allowed = set(_strings(payload, "allowed_tools", issues, unique=True))
    denied = set(_strings(payload, "denied_tools", issues, unique=True))
    if allowed & denied:
        issues.append("allowed_tools and denied_tools must be disjoint")
    authorized = _boolean(payload, "composition_authorized", issues)
    if authorized is True:
        issues.append("Derivative Activation Program cannot authorize composition before Final Script approval")
    _strings(payload, "limitations", issues)
    if dtype == "ANIMATION_SHORT" and "ANIMATION_SCENE_PACKAGE" not in str(payload.get("allowed_tools", ())):
        # Only a soft structural signal; no issue because tools are implementation-specific.
        pass


def _validate_jit_authoring_request(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="request_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "program_ref",
            "authoring_role",
            "approved_ingredient_refs",
            "voice_dna_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "category_id",
            "profile_id",
            "allowed_transformation_classes",
            "maximum_claim",
            "wrong_reading_lock_refs",
            "allowed_tools",
            "denied_tools",
            "context_sha256",
        ),
    )
    for field in ("program_ref", "voice_dna_ref", "primitive_coalition_ref", "archetype_coalition_ref"):
        _ref(payload.get(field), field, issues)
    _enum(payload, "authoring_role", {"WRITER", "COMPOSER"}, issues)
    _refs(payload, "approved_ingredient_refs", issues, minimum=1)
    for field in ("category_id", "profile_id", "maximum_claim"):
        _string(payload, field, issues)
    _strings(payload, "allowed_transformation_classes", issues, minimum=1, unique=True)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    allowed = set(_strings(payload, "allowed_tools", issues, unique=True))
    denied = set(_strings(payload, "denied_tools", issues, unique=True))
    if allowed & denied:
        issues.append("JIT authoring allowed and denied tools must be disjoint")
    _sha(payload.get("context_sha256"), "context_sha256", issues)


def _validate_script_segment(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=(
            "segment_id",
            "order",
            "final_text",
            "transformation_class",
            "source_text",
            "source_span_refs",
            "transformation_operations",
            "voice_dna_applied",
            "claim_state",
            "epistemic_state",
            "sequence_role",
        ),
    )
    if obj is None:
        return
    _string(obj, "segment_id", issues)
    _integer(obj, "order", issues, minimum=0)
    final_text = _string(obj, "final_text", issues)
    transform = _enum(obj, "transformation_class", {"VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE"}, issues)
    source_text = obj.get("source_text")
    if source_text is not None and not isinstance(source_text, str):
        issues.append(f"{field}.source_text must be string or null")
    spans = _refs(obj, "source_span_refs", issues)
    operations = _strings(obj, "transformation_operations", issues)
    voice_applied = _boolean(obj, "voice_dna_applied", issues)
    _enum(obj, "claim_state", {"DIRECT_QUOTE", "SOURCE_GROUNDED_CONDENSATION", "DERIVED_BRIDGE", "INFERRED"}, issues)
    _enum(obj, "epistemic_state", {"observed", "planned", "inferred", "operator_confirmed"}, issues)
    _string(obj, "sequence_role", issues)
    if transform == "VERBATIM":
        if source_text is None or final_text != source_text:
            issues.append(f"{field} VERBATIM final_text must exactly equal source_text")
        if not spans:
            issues.append(f"{field} VERBATIM requires source_span_refs")
        if operations:
            issues.append(f"{field} VERBATIM cannot declare transformation operations")
    if transform in {"CONDENSATION", "VOICE_DNA_REWRITE"} and not spans:
        issues.append(f"{field} {transform} requires source_span_refs")
    if transform == "VOICE_DNA_REWRITE" and voice_applied is not True:
        issues.append(f"{field} VOICE_DNA_REWRITE requires voice_dna_applied=true")
    if transform != "VERBATIM" and not operations:
        issues.append(f"{field} transformed segment requires transformation_operations")


def _validate_script_proposal(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="proposal_id",
        extra_required=("authoring_request_ref", "program_ref", "producer_actor_id", "segments", "rejected_alternative_refs", "limitations"),
    )
    _ref(payload.get("authoring_request_ref"), "authoring_request_ref", issues)
    _ref(payload.get("program_ref"), "program_ref", issues)
    _string(payload, "producer_actor_id", issues)
    segments = _mapping_list(payload, "segments", issues, minimum=1)
    for index, segment in enumerate(segments):
        _validate_script_segment(segment, f"segments[{index}]", issues)
    orders = [item.get("order") for item in segments]
    if orders != list(range(len(orders))):
        issues.append("script segment order must be contiguous from zero")
    _refs(payload, "rejected_alternative_refs", issues)
    _strings(payload, "limitations", issues)


def _validate_final_script(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="script_id",
        extra_required=(
            "program_ref",
            "proposal_ref",
            "segments",
            "script_sha256",
            "evaluation_receipt_refs",
            "operator_approved",
            "source_lineage_refs",
            "role_tension_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "brand_context_ref",
            "voice_dna_ref",
            "distillation_receipt_refs",
            "ccv_axes",
            "wrong_reading_lock_refs",
            "maximum_claim",
            "composition_eligible",
            "limitations",
        ),
        extra_optional=("approval_receipt_ref",),
    )
    for field in (
        "program_ref",
        "proposal_ref",
        "role_tension_ref",
        "primitive_coalition_ref",
        "archetype_coalition_ref",
        "brand_context_ref",
        "voice_dna_ref",
    ):
        _ref(payload.get(field), field, issues)
    segments = _mapping_list(payload, "segments", issues, minimum=1)
    for index, segment in enumerate(segments):
        _validate_script_segment(segment, f"segments[{index}]", issues)
    _sha(payload.get("script_sha256"), "script_sha256", issues)
    _refs(payload, "evaluation_receipt_refs", issues, minimum=1)
    approved = _boolean(payload, "operator_approved", issues)
    _refs(payload, "source_lineage_refs", issues, minimum=1)
    _refs(payload, "distillation_receipt_refs", issues, minimum=1)
    _string_mapping(payload.get("ccv_axes"), "ccv_axes", issues, minimum=1)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _string(payload, "maximum_claim", issues)
    eligible = _boolean(payload, "composition_eligible", issues)
    _optional_ref(payload, "approval_receipt_ref", issues)
    _strings(payload, "limitations", issues)
    if approved and payload.get("approval_receipt_ref") is None:
        issues.append("operator-approved Final Script requires approval_receipt_ref")
    if eligible is True and not approved:
        issues.append("composition_eligible requires operator_approved=true")
    if payload.get("lifecycle_state") == LifecycleState.APPROVED.value and not approved:
        issues.append("approved Final Script lifecycle requires operator approval")


def _validate_final_script_approval(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "candidate_script_ref",
            "approved_script_sha256",
            "operator_id",
            "operator_decision_ref",
            "decision",
            "exact_bytes_approved",
            "evaluation_refs",
            "resulting_script_ref",
            "rationale",
        ),
    )
    for field in ("candidate_script_ref", "operator_decision_ref"):
        _ref(payload.get(field), field, issues)
    _sha(payload.get("approved_script_sha256"), "approved_script_sha256", issues)
    _string(payload, "operator_id", issues)
    decision = _enum(payload, "decision", {"APPROVE", "AMEND", "REJECT"}, issues)
    exact = _boolean(payload, "exact_bytes_approved", issues)
    _refs(payload, "evaluation_refs", issues, minimum=1)
    _ref(payload.get("resulting_script_ref"), "resulting_script_ref", issues, nullable=True)
    _string(payload, "rationale", issues)
    if decision == "APPROVE" and exact is not True:
        issues.append("APPROVE requires exact_bytes_approved=true")
    if decision == "APPROVE" and payload.get("resulting_script_ref") is None:
        issues.append("APPROVE requires resulting_script_ref")


def _validate_bbox_intent(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("intent_id", "semantic_target_ref", "attention_function", "why", "allowed_variation", "forbidden_outcomes"),
    )
    if obj is None:
        return
    _string(obj, "intent_id", issues)
    _ref(obj.get("semantic_target_ref"), f"{field}.semantic_target_ref", issues)
    _string(obj, "attention_function", issues)
    _string(obj, "why", issues)
    _strings(obj, "allowed_variation", issues)
    _strings(obj, "forbidden_outcomes", issues, minimum=1)


def _validate_animation_scene(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=(
            "scene_id",
            "segment_refs",
            "source_refs",
            "role_tension_movement",
            "sequence_role",
            "timing_intent",
            "bbox_intents",
            "composition_intent",
            "identity_continuity_refs",
            "visual_requirement_intents",
            "wrong_reading_lock_refs",
            "reuse_roles",
        ),
    )
    if obj is None:
        return
    _string(obj, "scene_id", issues)
    _refs(obj, "segment_refs", issues, minimum=1)
    _refs(obj, "source_refs", issues, minimum=1)
    for name in ("role_tension_movement", "sequence_role", "timing_intent", "composition_intent"):
        _string(obj, name, issues)
    bboxes = _mapping_list(obj, "bbox_intents", issues, minimum=1)
    for index, bbox in enumerate(bboxes):
        _validate_bbox_intent(bbox, f"{field}.bbox_intents[{index}]", issues)
    _refs(obj, "identity_continuity_refs", issues)
    intents = _mapping_list(obj, "visual_requirement_intents", issues, minimum=1)
    for index, intent in enumerate(intents):
        _validate_visual_requirement_intent_fields(intent, f"{field}.visual_requirement_intents[{index}]", issues)
    _refs(obj, "wrong_reading_lock_refs", issues, minimum=1)
    roles = _strings(obj, "reuse_roles", issues, minimum=1, unique=True)
    permitted = {"SHORT_BROLL", "CAROUSEL_SLIDE", "SUPERVISUAL_ELEMENT", "ANIMATION_SHORT", "CAMPAIGN_ASSET"}
    if set(roles) - permitted:
        issues.append(f"{field}.reuse_roles contains unsupported role")


def _validate_animation_scene_package(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="package_id",
        extra_required=("final_script_ref", "scenes", "render_disposition", "format02_activated", "limitations"),
    )
    _ref(payload.get("final_script_ref"), "final_script_ref", issues)
    scenes = _mapping_list(payload, "scenes", issues, minimum=1)
    for index, scene in enumerate(scenes):
        _validate_animation_scene(scene, f"scenes[{index}]", issues)
    _enum(payload, "render_disposition", {"DEFER_RENDER_PRESERVE_PACKAGE", "FULL_RENDER_REQUIRED", "PARTIAL_RENDER_ALLOWED"}, issues)
    format02 = _boolean(payload, "format02_activated", issues)
    if format02 is True:
        issues.append("Animation Scene Package cannot activate Format 02")
    _strings(payload, "limitations", issues)


def _validate_must_survive_property(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(
        value,
        field,
        issues,
        required=("property_id", "property_kind", "statement", "evidence_refs", "hard_gate"),
    )
    if obj is None:
        return
    _string(obj, "property_id", issues)
    _enum(obj, "property_kind", {"SOURCE_MEANING", "ROLE_TENSION", "EDGE_PRODUCT", "VOICE", "VISUAL", "WRONG_READING_LOCK", "IDENTITY_CONTINUITY", "SEQUENCE_FUNCTION"}, issues)
    _string(obj, "statement", issues)
    _refs(obj, "evidence_refs", issues, minimum=1)
    _boolean(obj, "hard_gate", issues)


def _validate_transformation_rule(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(value, field, issues, required=("operation_class", "allowed", "constraints"))
    if obj is None:
        return
    _enum(obj, "operation_class", {"VERBATIM", "CONDENSATION", "REWRITE", "REORDER", "VISUAL_TRANSLATION", "AUDIO_REUSE", "ANIMATION_TRANSLATION"}, issues)
    _boolean(obj, "allowed", issues)
    _strings(obj, "constraints", issues)


def _validate_required_change(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(value, field, issues, required=("change_id", "reason", "target_property_ids", "required_operations"))
    if obj is None:
        return
    _string(obj, "change_id", issues)
    _string(obj, "reason", issues)
    _strings(obj, "target_property_ids", issues, minimum=1)
    _strings(obj, "required_operations", issues, minimum=1)


def _validate_transfer_contract(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="contract_id",
        extra_required=(
            "source_expression_refs",
            "source_package_refs",
            "expression_moment_refs",
            "reaction_receipt_refs",
            "selected_hypothesis_ref",
            "role_tension_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "final_script_ref",
            "must_survive_properties",
            "transformation_rules",
            "required_changes",
            "wrong_reading_lock_refs",
            "evaluation_profile_ref",
            "limitations",
        ),
    )
    _refs(payload, "source_expression_refs", issues, minimum=1)
    _refs(payload, "source_package_refs", issues, minimum=1)
    _refs(payload, "expression_moment_refs", issues, minimum=1)
    _refs(payload, "reaction_receipt_refs", issues, minimum=1)
    for field in ("selected_hypothesis_ref", "role_tension_ref", "primitive_coalition_ref", "archetype_coalition_ref", "final_script_ref", "evaluation_profile_ref"):
        _ref(payload.get(field), field, issues)
    properties = _mapping_list(payload, "must_survive_properties", issues, minimum=1)
    for index, prop in enumerate(properties):
        _validate_must_survive_property(prop, f"must_survive_properties[{index}]", issues)
    ids = [item.get("property_id") for item in properties]
    if len(ids) != len(set(ids)):
        issues.append("must_survive_properties property_id values must be unique")
    for index, rule in enumerate(_mapping_list(payload, "transformation_rules", issues, minimum=1)):
        _validate_transformation_rule(rule, f"transformation_rules[{index}]", issues)
    for index, change in enumerate(_mapping_list(payload, "required_changes", issues)):
        _validate_required_change(change, f"required_changes[{index}]", issues)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_source_transformation_lineage(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="lineage_id",
        lifecycle_required=False,
        extra_required=(
            "source_refs",
            "target_ref",
            "transformation_class",
            "operations",
            "source_text",
            "target_text",
            "source_span_refs",
            "claim_state",
            "exact_quote_match",
            "limitations",
        ),
        extra_optional=("voice_dna_ref",),
    )
    _refs(payload, "source_refs", issues, minimum=1)
    _ref(payload.get("target_ref"), "target_ref", issues)
    transform = _enum(payload, "transformation_class", {"VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE", "VISUAL_TRANSLATION", "ANIMATION_TRANSLATION"}, issues)
    _strings(payload, "operations", issues)
    source_text = _string(payload, "source_text", issues, allow_empty=True)
    target_text = _string(payload, "target_text", issues, allow_empty=True)
    _refs(payload, "source_span_refs", issues)
    _enum(payload, "claim_state", {"DIRECT_QUOTE", "SOURCE_GROUNDED", "DERIVED", "INFERRED"}, issues)
    exact = _boolean(payload, "exact_quote_match", issues)
    _optional_ref(payload, "voice_dna_ref", issues)
    _strings(payload, "limitations", issues)
    if transform == "VERBATIM" and (source_text != target_text or exact is not True):
        issues.append("VERBATIM lineage requires exact source/target text match")
    if transform == "VOICE_DNA_REWRITE" and payload.get("voice_dna_ref") is None:
        issues.append("VOICE_DNA_REWRITE requires voice_dna_ref")


def _validate_transfer_property_result(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(value, field, issues, required=("property_id", "result", "evidence_refs", "reason"))
    if obj is None:
        return
    _string(obj, "property_id", issues)
    result = _enum(obj, "result", {"PASS", "FAIL", "NOT_APPLICABLE"}, issues)
    refs = _refs(obj, "evidence_refs", issues)
    _string(obj, "reason", issues)
    if result == "NOT_APPLICABLE" and not refs:
        issues.append(f"{field} NOT_APPLICABLE requires evidence")


def _validate_transfer_checkpoint(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("contract_ref", "checkpoint", "target_ref", "property_results", "wrong_reading_results", "deterministic_pass", "limitations"),
        extra_optional=("independent_evaluator_ref",),
    )
    _ref(payload.get("contract_ref"), "contract_ref", issues)
    _enum(payload, "checkpoint", {"SCRIPT", "SCENE", "COMPOSITION", "RENDER"}, issues)
    _ref(payload.get("target_ref"), "target_ref", issues)
    results = _mapping_list(payload, "property_results", issues, minimum=1)
    for index, result in enumerate(results):
        _validate_transfer_property_result(result, f"property_results[{index}]", issues)
    wrong = _mapping_list(payload, "wrong_reading_results", issues, minimum=1)
    for index, result in enumerate(wrong):
        _validate_transfer_property_result(result, f"wrong_reading_results[{index}]", issues)
    passed = _boolean(payload, "deterministic_pass", issues)
    _optional_ref(payload, "independent_evaluator_ref", issues)
    _strings(payload, "limitations", issues)
    if passed is True:
        if any(item.get("result") == "FAIL" for item in [*results, *wrong]):
            issues.append("deterministic_pass cannot be true when a result fails")


def _validate_transfer_evaluation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("contract_ref", "checkpoint_refs", "deterministic_gate_passed", "independent_evaluation_ref", "verdict", "failed_property_ids", "limitations"),
    )
    _ref(payload.get("contract_ref"), "contract_ref", issues)
    _refs(payload, "checkpoint_refs", issues, minimum=1)
    passed = _boolean(payload, "deterministic_gate_passed", issues)
    _ref(payload.get("independent_evaluation_ref"), "independent_evaluation_ref", issues)
    verdict = _enum(payload, "verdict", {"PASS", "FAIL", "INSUFFICIENT_EVIDENCE"}, issues)
    failed = _strings(payload, "failed_property_ids", issues, unique=True)
    _strings(payload, "limitations", issues)
    if verdict == "PASS" and (passed is not True or failed):
        issues.append("transfer evaluation PASS requires deterministic gate pass and no failed properties")


def _validate_transfer_failure(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="failure_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("contract_ref", "checkpoint_ref", "responsible_layer", "owner_product", "failed_property_ids", "observed_symptom", "evidence_refs", "preserved_property_ids", "status"),
    )
    _ref(payload.get("contract_ref"), "contract_ref", issues)
    _ref(payload.get("checkpoint_ref"), "checkpoint_ref", issues)
    _enum(payload, "responsible_layer", {item.value for item in ResponsibleLayer}, issues)
    _string(payload, "owner_product", issues)
    _strings(payload, "failed_property_ids", issues, minimum=1, unique=True)
    _string(payload, "observed_symptom", issues)
    _refs(payload, "evidence_refs", issues, minimum=1)
    _strings(payload, "preserved_property_ids", issues, unique=True)
    _enum(payload, "status", {"PROPOSED", "CONFIRMED", "DISPUTED", "RESOLVED"}, issues)


def _validate_transfer_repair(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="repair_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=("failure_ref", "owner_product", "repair_scope", "allowed_operations", "protected_property_ids", "target_refs", "rerun_node_refs", "status"),
    )
    _ref(payload.get("failure_ref"), "failure_ref", issues)
    _string(payload, "owner_product", issues)
    _string(payload, "repair_scope", issues)
    _strings(payload, "allowed_operations", issues, minimum=1)
    _strings(payload, "protected_property_ids", issues, unique=True)
    _refs(payload, "target_refs", issues, minimum=1)
    _refs(payload, "rerun_node_refs", issues)
    _enum(payload, "status", {"PROPOSED", "AUTHORIZED", "EXECUTED", "REJECTED"}, issues)


def _validate_visual_requirement_intent_fields(value: Mapping[str, Any], field: str, issues: list[str]) -> None:
    _strict_fields(
        value,
        required=(
            "intent_id",
            "asset_family",
            "semantic_role",
            "sequence_role",
            "composition_intent_ref",
            "feature_contract_refs",
            "identity_continuity_refs",
            "geometry_need",
            "permitted_variation",
            "preservation_lock_refs",
            "source_reference_refs",
            "evaluation_profile_ref",
            "priority",
            "limitations",
            "authority_class",
        ),
        issues=issues,
    )
    for name in ("intent_id", "asset_family", "semantic_role", "sequence_role", "geometry_need", "permitted_variation"):
        _string(value, name, issues)
    _ref(value.get("composition_intent_ref"), f"{field}.composition_intent_ref", issues)
    _refs(value, "feature_contract_refs", issues, minimum=1)
    _refs(value, "identity_continuity_refs", issues)
    _refs(value, "preservation_lock_refs", issues, minimum=1)
    _refs(value, "source_reference_refs", issues, minimum=1)
    _ref(value.get("evaluation_profile_ref"), f"{field}.evaluation_profile_ref", issues)
    _integer(value, "priority", issues, minimum=0)
    _strings(value, "limitations", issues)
    _enum(value, "authority_class", {"NONAUTHORITATIVE_REQUIREMENT_INTENT"}, issues)
    forbidden = {"provider", "model", "lora_id", "workflow", "conditioning", "price", "deadline"}
    if forbidden & set(value):
        issues.append(f"{field} contains VAE-owned production fields")


def _validate_visual_activation_case(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="case_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "state",
            "source_package_refs",
            "expression_moment_refs",
            "semantic_production_package_ref",
            "approved_final_script_ref",
            "activation_transfer_contract_ref",
            "primitive_coalition_ref",
            "archetype_coalition_ref",
            "brand_context_ref",
            "voice_dna_ref",
            "visual_dna_ref",
            "category_id",
            "profile_id",
            "format_harness_ref",
            "evaluation_profile_ref",
            "operator_source_authority_ref",
            "wrong_reading_lock_refs",
            "limitations",
        ),
    )
    _enum(payload, "state", {"OPEN", "REFERENCED", "CANDIDATES_COMPILED", "SELECTED", "HANDOFF_PUBLISHED", "SUPERSEDED", "CANCELLED"}, issues)
    _refs(payload, "source_package_refs", issues, minimum=1)
    _refs(payload, "expression_moment_refs", issues)
    for field in (
        "semantic_production_package_ref",
        "approved_final_script_ref",
        "activation_transfer_contract_ref",
        "primitive_coalition_ref",
        "archetype_coalition_ref",
        "brand_context_ref",
        "voice_dna_ref",
        "visual_dna_ref",
        "format_harness_ref",
        "evaluation_profile_ref",
        "operator_source_authority_ref",
    ):
        _ref(payload.get(field), field, issues)
    for field in ("category_id", "profile_id"):
        _string(payload, field, issues)
    if "format02" in str(payload.get("profile_id", "")).lower():
        issues.append("Format 02 remains deferred")
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_visual_reference_evidence(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="evidence_id",
        lifecycle_required=False,
        extra_required=("reference_kind", "source_ref", "locator", "provenance_ref", "observed_properties", "applicability_statement", "permitted_semantic_uses", "prohibited_uses", "captured_by", "owner_product", "limitations", "generated_approximation"),
    )
    kind = _enum(payload, "reference_kind", {"SPECIMEN", "REAL_ENVIRONMENT", "HUMAN_REFERENCE", "OBJECT_BEHAVIOR", "DOCUMENTED_VISUAL_SYSTEM", "SOURCE_FRAME", "GENERATED_APPROXIMATION"}, issues)
    _ref(payload.get("source_ref"), "source_ref", issues)
    _string(payload, "locator", issues)
    _ref(payload.get("provenance_ref"), "provenance_ref", issues)
    _strings(payload, "observed_properties", issues, minimum=1)
    _string(payload, "applicability_statement", issues)
    _strings(payload, "permitted_semantic_uses", issues, minimum=1)
    _strings(payload, "prohibited_uses", issues)
    _string(payload, "captured_by", issues)
    _string(payload, "owner_product", issues)
    _strings(payload, "limitations", issues)
    generated = _boolean(payload, "generated_approximation", issues)
    if generated is True and kind != "GENERATED_APPROXIMATION":
        issues.append("generated approximation cannot claim a real-life reference kind")
    if generated is False and kind == "GENERATED_APPROXIMATION":
        issues.append("GENERATED_APPROXIMATION must set generated_approximation=true")


def _validate_visual_semantic_candidate(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="candidate_id",
        extra_required=(
            "case_ref",
            "recognition_intent",
            "viewer_role",
            "role_tension_ref",
            "recognition_carrier",
            "activation_directions",
            "visual_world_refs",
            "reference_evidence_refs",
            "metaphor_relations",
            "source_evidence_bindings",
            "primitive_binding_refs",
            "archetype_coalition_ref",
            "voice_dna_ref",
            "visual_dna_ref",
            "transfer_property_ids",
            "category_profile_ref",
            "composition_potential",
            "wrong_reading_lock_refs",
            "wrong_reading_risks",
            "producer_binding_ref",
            "limitations",
        ),
    )
    _ref(payload.get("case_ref"), "case_ref", issues)
    for field in ("recognition_intent", "viewer_role", "recognition_carrier", "composition_potential"):
        _string(payload, field, issues)
    _ref(payload.get("role_tension_ref"), "role_tension_ref", issues)
    _strings(payload, "activation_directions", issues, minimum=1, unique=True)
    for field in ("visual_world_refs", "reference_evidence_refs", "primitive_binding_refs"):
        _refs(payload, field, issues, minimum=1)
    _strings(payload, "metaphor_relations", issues, minimum=1)
    _refs(payload, "source_evidence_bindings", issues, minimum=1)
    for field in ("archetype_coalition_ref", "voice_dna_ref", "visual_dna_ref", "category_profile_ref", "producer_binding_ref"):
        _ref(payload.get(field), field, issues)
    _strings(payload, "transfer_property_ids", issues, minimum=1, unique=True)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "wrong_reading_risks", issues)
    _strings(payload, "limitations", issues)


def _validate_visual_semantic_pack(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="pack_id",
        extra_required=("case_ref", "selected_candidate_ref", "rejected_candidate_refs", "deterministic_validation_receipt_ref", "independent_evaluation_receipt_ref", "selection_reason_refs", "evaluation_profile_ref", "upstream_refs", "wrong_reading_lock_refs", "limitations"),
    )
    for field in ("case_ref", "selected_candidate_ref", "deterministic_validation_receipt_ref", "independent_evaluation_receipt_ref", "evaluation_profile_ref"):
        _ref(payload.get(field), field, issues)
    _refs(payload, "rejected_candidate_refs", issues)
    _refs(payload, "selection_reason_refs", issues, minimum=1)
    _refs(payload, "upstream_refs", issues, minimum=1)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_visual_beat(value: Any, field: str, issues: list[str]) -> None:
    obj = _strict_nested(value, field, issues, required=("beat_id", "order", "attention_state", "visual_job", "recognition_carrier_ref", "viewer_role_before", "viewer_role_after", "source_support_refs", "feature_contract_refs", "bbox_intent_refs", "expected_payoff", "wrong_reading_lock_refs"))
    if obj is None:
        return
    _string(obj, "beat_id", issues)
    _integer(obj, "order", issues, minimum=0)
    for name in ("attention_state", "visual_job", "viewer_role_before", "viewer_role_after", "expected_payoff"):
        _string(obj, name, issues)
    _ref(obj.get("recognition_carrier_ref"), f"{field}.recognition_carrier_ref", issues)
    _refs(obj, "source_support_refs", issues, minimum=1)
    _refs(obj, "feature_contract_refs", issues, minimum=1)
    _refs(obj, "bbox_intent_refs", issues, minimum=1)
    _refs(obj, "wrong_reading_lock_refs", issues, minimum=1)


def _validate_visual_narrative(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="program_id",
        extra_required=("visual_semantic_pack_ref", "activation_transfer_contract_ref", "format_harness_ref", "category_profile_ref", "activation_directions", "viewer_role_progression", "pattern_match", "pattern_interrupt", "attention_state_sequence", "beats", "prediction_gap", "payoff", "feature_contract_intent_refs", "bbox_intent_refs", "wrong_reading_lock_refs", "evaluation_profile_ref", "limitations"),
    )
    for field in ("visual_semantic_pack_ref", "activation_transfer_contract_ref", "format_harness_ref", "category_profile_ref", "evaluation_profile_ref"):
        _ref(payload.get(field), field, issues)
    _strings(payload, "activation_directions", issues, minimum=1, unique=True)
    for field in ("viewer_role_progression", "pattern_match", "pattern_interrupt", "prediction_gap", "payoff"):
        _string(payload, field, issues)
    _strings(payload, "attention_state_sequence", issues, minimum=1)
    beats = _mapping_list(payload, "beats", issues, minimum=1)
    for index, beat in enumerate(beats):
        _validate_visual_beat(beat, f"beats[{index}]", issues)
    if [item.get("order") for item in beats] != list(range(len(beats))):
        issues.append("visual narrative beats must have contiguous order from zero")
    _refs(payload, "feature_contract_intent_refs", issues, minimum=1)
    _refs(payload, "bbox_intent_refs", issues, minimum=1)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_composition_intent(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="composition_intent_id",
        extra_required=("program_ref", "sequence_role", "semantic_hierarchy", "reading_path", "subject_relationships", "spatial_psychology", "negative_space_intents", "bbox_intents", "depth_relationships", "intended_viewer_state", "identity_continuity_refs", "feature_contract_refs", "allowed_variation", "forbidden_collapses", "wrong_reading_lock_refs", "evaluation_profile_ref", "limitations"),
    )
    _ref(payload.get("program_ref"), "program_ref", issues)
    _string(payload, "sequence_role", issues)
    _strings(payload, "semantic_hierarchy", issues, minimum=1)
    _strings(payload, "reading_path", issues, minimum=1)
    _strings(payload, "subject_relationships", issues, minimum=1)
    _string(payload, "spatial_psychology", issues)
    _strings(payload, "negative_space_intents", issues, minimum=1)
    bboxes = _mapping_list(payload, "bbox_intents", issues, minimum=1)
    for index, bbox in enumerate(bboxes):
        _validate_bbox_intent(bbox, f"bbox_intents[{index}]", issues)
    _strings(payload, "depth_relationships", issues)
    _string(payload, "intended_viewer_state", issues)
    _refs(payload, "identity_continuity_refs", issues)
    _refs(payload, "feature_contract_refs", issues, minimum=1)
    _strings(payload, "allowed_variation", issues)
    _strings(payload, "forbidden_collapses", issues, minimum=1)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _ref(payload.get("evaluation_profile_ref"), "evaluation_profile_ref", issues)
    _strings(payload, "limitations", issues)
    forbidden = {"x", "y", "width", "height", "provider", "model", "workflow"}
    if forbidden & set(payload):
        issues.append("AIR Composition Intent cannot own final pixel geometry or production strategy")


def _validate_feature_contract(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="feature_contract_id",
        extra_required=("feature_kind", "semantic_job", "required_state", "prohibited_states", "source_support_refs", "composition_intent_ref", "applicability", "allowed_variation", "wrong_reading_lock_refs", "deterministic_checks", "judgment_profile_dimension_refs", "feasibility_owner", "realization_owner", "semantic_owner", "limitations"),
    )
    _enum(payload, "feature_kind", {"GAZE", "HANDS", "FACIAL_EXPRESSION", "POSTURE", "WITNESS", "PROP", "OBJECT_PUNCTUM", "EVIDENCE", "TEXT", "SCALE", "DEPTH", "MOTION", "SONIC_CUE", "NEGATIVE_SPACE", "IDENTITY_CONTINUITY"}, issues)
    _string(payload, "semantic_job", issues)
    _string(payload, "required_state", issues)
    _strings(payload, "prohibited_states", issues)
    _refs(payload, "source_support_refs", issues, minimum=1)
    _ref(payload.get("composition_intent_ref"), "composition_intent_ref", issues)
    applicability = payload.get("applicability")
    obj = _strict_nested(applicability, "applicability", issues, required=("state", "rule", "evidence_refs"))
    if obj is not None:
        state = _enum(obj, "state", {"REQUIRED", "NOT_APPLICABLE"}, issues)
        _string(obj, "rule", issues)
        refs = _refs(obj, "evidence_refs", issues)
        if state == "NOT_APPLICABLE" and not refs:
            issues.append("FeatureContract NOT_APPLICABLE requires evidence")
    _strings(payload, "allowed_variation", issues)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _strings(payload, "deterministic_checks", issues, minimum=1)
    _refs(payload, "judgment_profile_dimension_refs", issues, minimum=1)
    if payload.get("feasibility_owner") != "visual-asset-editor":
        issues.append("feature feasibility owner must be visual-asset-editor")
    if payload.get("realization_owner") != "visual-asset-editor":
        issues.append("feature realization owner must be visual-asset-editor")
    if payload.get("semantic_owner") != "activative-intelligence-runtime":
        issues.append("feature semantic owner must be activative-intelligence-runtime")
    _strings(payload, "limitations", issues)


def _validate_visual_requirement_intent(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(payload, issues, id_field="intent_id", extra_required=("asset_family", "semantic_role", "sequence_role", "composition_intent_ref", "feature_contract_refs", "identity_continuity_refs", "geometry_need", "permitted_variation", "preservation_lock_refs", "source_reference_refs", "evaluation_profile_ref", "priority", "limitations", "authority_class"))
    _validate_visual_requirement_intent_fields(payload, "visual_requirement_intent", issues)


def _validate_visual_handoff(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="handoff_id",
        extra_required=("case_ref", "semantic_pack_ref", "narrative_program_ref", "composition_intent_ref", "feature_contract_refs", "requirement_intent_refs", "category_id", "profile_id", "format_harness_ref", "source_lineage_refs", "voice_dna_ref", "visual_dna_ref", "activation_transfer_contract_ref", "wrong_reading_lock_refs", "evaluation_profile_ref", "producer_receipt_refs", "independent_evaluation_receipt_refs", "compatibility_requirements", "limitations", "owner_product"),
    )
    for field in ("case_ref", "semantic_pack_ref", "narrative_program_ref", "composition_intent_ref", "format_harness_ref", "voice_dna_ref", "visual_dna_ref", "activation_transfer_contract_ref", "evaluation_profile_ref"):
        _ref(payload.get(field), field, issues)
    _refs(payload, "feature_contract_refs", issues, minimum=1)
    _refs(payload, "requirement_intent_refs", issues, minimum=1)
    for field in ("category_id", "profile_id"):
        _string(payload, field, issues)
    _refs(payload, "source_lineage_refs", issues, minimum=1)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _refs(payload, "producer_receipt_refs", issues, minimum=1)
    _refs(payload, "independent_evaluation_receipt_refs", issues, minimum=1)
    _strings(payload, "compatibility_requirements", issues, minimum=1)
    _strings(payload, "limitations", issues)
    if payload.get("owner_product") != "activative-intelligence-runtime":
        issues.append("visual activation handoff owner_product must be activative-intelligence-runtime")
    forbidden = {"visual_asset_demand", "provider", "model", "lora_id", "workflow", "conditioning"}
    if forbidden & set(payload):
        issues.append("AIR visual handoff contains Pipeline/VAE-owned production fields")


def _validate_visual_result_observation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(payload, issues, id_field="observation_id", lifecycle_required=False, extra_required=("demand_ref", "asset_result_ref", "render_ref", "production_acceptance_ref", "artifact_hashes", "measured_geometry_refs", "observation_evidence_refs", "limitations"))
    for field in ("demand_ref", "asset_result_ref", "render_ref", "production_acceptance_ref"):
        _ref(payload.get(field), field, issues)
    hashes = _strings(payload, "artifact_hashes", issues, minimum=1, unique=True)
    for index, sha in enumerate(hashes):
        _sha(sha, f"artifact_hashes[{index}]", issues)
    _refs(payload, "measured_geometry_refs", issues)
    _refs(payload, "observation_evidence_refs", issues, minimum=1)
    _strings(payload, "limitations", issues)


def _validate_visual_reparse(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(payload, issues, id_field="receipt_id", lifecycle_required=False, epistemic_required=False, extra_required=("visual_activation_handoff_ref", "result_observation_ref", "observed_hierarchy", "bbox_relationships", "gaze_findings", "reading_order_findings", "timing_findings", "feature_outcomes", "lock_outcomes", "role_tension_comparison", "deterministic_findings", "independent_judgment_refs", "decision", "responsible_owner", "repair_scope_refs", "limitations"))
    _ref(payload.get("visual_activation_handoff_ref"), "visual_activation_handoff_ref", issues)
    _ref(payload.get("result_observation_ref"), "result_observation_ref", issues)
    for field in ("observed_hierarchy", "bbox_relationships", "gaze_findings", "reading_order_findings", "timing_findings", "feature_outcomes", "lock_outcomes", "deterministic_findings"):
        _strings(payload, field, issues)
    _string(payload, "role_tension_comparison", issues)
    _refs(payload, "independent_judgment_refs", issues, minimum=1)
    _enum(payload, "decision", {"CONFORMS", "REPAIR_REQUIRED", "REJECTED", "CONTESTED"}, issues)
    _string(payload, "responsible_owner", issues)
    _refs(payload, "repair_scope_refs", issues)
    _strings(payload, "limitations", issues)


def _validate_semantic_production_package(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="package_id",
        extra_required=("derivative_program_ref", "approved_final_script_ref", "animation_scene_package_ref", "activation_transfer_contract_ref", "source_lineage_refs", "observed_activative_pack_ref", "matrix_of_edging_ref", "role_tension_ref", "primitive_coalition_ref", "archetype_coalition_ref", "brand_context_ref", "voice_dna_ref", "visual_dna_ref", "distillation_receipt_refs", "approval_receipt_ref", "rejected_candidate_refs", "wrong_reading_lock_refs", "evaluation_profile_ref", "claim_ceiling", "downstream_consumers", "limitations"),
    )
    for field in ("derivative_program_ref", "approved_final_script_ref", "animation_scene_package_ref", "activation_transfer_contract_ref", "observed_activative_pack_ref", "matrix_of_edging_ref", "role_tension_ref", "primitive_coalition_ref", "archetype_coalition_ref", "brand_context_ref", "voice_dna_ref", "visual_dna_ref", "approval_receipt_ref", "evaluation_profile_ref"):
        _ref(payload.get(field), field, issues)
    _refs(payload, "source_lineage_refs", issues, minimum=1)
    _refs(payload, "distillation_receipt_refs", issues, minimum=1)
    _refs(payload, "rejected_candidate_refs", issues)
    _refs(payload, "wrong_reading_lock_refs", issues, minimum=1)
    _string(payload, "claim_ceiling", issues)
    _strings(payload, "downstream_consumers", issues, minimum=1, unique=True)
    _strings(payload, "limitations", issues)


PRODUCTION_VALIDATORS: dict[str, Callable[[Mapping[str, Any], list[str]], None]] = {
    "activation_hypothesis": _validate_activation_hypothesis,
    "activation_hypothesis_portfolio": _validate_hypothesis_portfolio,
    "hypothesis_gate_result": _validate_hypothesis_gate_result,
    "comparative_evaluation_receipt": _validate_comparative_evaluation,
    "hypothesis_stopping_receipt": _validate_hypothesis_stopping,
    "hypothesis_promotion_receipt": _validate_hypothesis_promotion,
    "planned_activative_intelligence_pack": _validate_planned_pack,
    "derivative_input_manifest": _validate_derivative_input_manifest,
    "derivative_activation_program": _validate_derivative_program,
    "jit_authoring_request": _validate_jit_authoring_request,
    "script_proposal_artifact": _validate_script_proposal,
    "final_script_package": _validate_final_script,
    "final_script_approval_receipt": _validate_final_script_approval,
    "animation_scene_package": _validate_animation_scene_package,
    "semantic_production_package": _validate_semantic_production_package,
    "activation_transfer_contract": _validate_transfer_contract,
    "source_transformation_lineage": _validate_source_transformation_lineage,
    "transfer_checkpoint": _validate_transfer_checkpoint,
    "activation_transfer_evaluation_receipt": _validate_transfer_evaluation,
    "transfer_failure": _validate_transfer_failure,
    "transfer_repair_request": _validate_transfer_repair,
}

PRODUCTION_ID_FIELDS: dict[str, str] = {
    "activation_hypothesis": "hypothesis_id",
    "activation_hypothesis_portfolio": "portfolio_id",
    "hypothesis_gate_result": "receipt_id",
    "comparative_evaluation_receipt": "receipt_id",
    "hypothesis_stopping_receipt": "receipt_id",
    "hypothesis_promotion_receipt": "receipt_id",
    "planned_activative_intelligence_pack": "pack_id",
    "derivative_input_manifest": "manifest_id",
    "derivative_activation_program": "program_id",
    "jit_authoring_request": "request_id",
    "script_proposal_artifact": "proposal_id",
    "final_script_package": "script_id",
    "final_script_approval_receipt": "receipt_id",
    "animation_scene_package": "package_id",
    "semantic_production_package": "package_id",
    "activation_transfer_contract": "contract_id",
    "source_transformation_lineage": "lineage_id",
    "transfer_checkpoint": "receipt_id",
    "activation_transfer_evaluation_receipt": "receipt_id",
    "transfer_failure": "failure_id",
    "transfer_repair_request": "repair_id",
}
