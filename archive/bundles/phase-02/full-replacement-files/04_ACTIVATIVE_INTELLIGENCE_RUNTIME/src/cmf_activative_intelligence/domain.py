from __future__ import annotations

import copy
import re
from enum import Enum
from typing import Any, Callable, Mapping, Sequence

from ca_contracts import canonical_sha256

_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]{1,191}$")


class AirValidationError(ValueError):
    def __init__(self, object_type: str, issues: Sequence[str]):
        self.object_type = object_type
        self.issues = tuple(issues)
        super().__init__(f"{object_type} validation failed: " + "; ".join(self.issues))


class ActivationDomain(str, Enum):
    SOURCE = "source"
    RELATIONSHIP = "relationship"
    AUDIENCE = "audience"
    CAMPAIGN = "campaign"
    DERIVATIVE = "derivative"


class EpistemicState(str, Enum):
    PLANNED = "planned"
    OBSERVED = "observed"
    INFERRED = "inferred"
    OPERATOR_CONFIRMED = "operator_confirmed"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class LifecycleState(str, Enum):
    PROPOSED = "proposed"
    VALIDATED = "validated"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class PrimitiveRole(str, Enum):
    PRIMARY = "primary"
    SUPPORT = "support"
    SUPPRESSION = "suppression"


class ResponsibleLayer(str, Enum):
    AIR_CONTEXT = "air.context"
    AIR_MATRIX = "air.matrix_of_edging"
    AIR_PRIMITIVE_BINDING = "air.primitive_binding"
    AIR_PRIMITIVE_COALITION = "air.primitive_coalition"
    AIR_ARCHETYPE = "air.archetype_coalition"
    AIR_BRAND = "air.brand_context"
    AIR_VOICE = "air.voice_dna"
    AIR_VISUAL = "air.visual_dna"
    AIR_LEARNING = "air.human_resolution"
    INTERVIEW_SOURCE = "interview.source"
    INTERVIEW_REACTION = "interview.reaction"
    PIPELINE_EXECUTION = "pipeline.execution"
    VAE_PRODUCTION = "vae.production"
    DELEGATION_TRANSPORT = "delegation.transport"
    INDEPENDENT_EVALUATION = "evaluation.independent"
    HUMAN_DECISION = "human.decision"
    UNRESOLVED = "unresolved"


AIR_OWNED_LAYERS = frozenset(
    {
        ResponsibleLayer.AIR_CONTEXT.value,
        ResponsibleLayer.AIR_MATRIX.value,
        ResponsibleLayer.AIR_PRIMITIVE_BINDING.value,
        ResponsibleLayer.AIR_PRIMITIVE_COALITION.value,
        ResponsibleLayer.AIR_ARCHETYPE.value,
        ResponsibleLayer.AIR_BRAND.value,
        ResponsibleLayer.AIR_VOICE.value,
        ResponsibleLayer.AIR_VISUAL.value,
        ResponsibleLayer.AIR_LEARNING.value,
    }
)

_LAYER_OWNER = {
    ResponsibleLayer.AIR_CONTEXT.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_MATRIX.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_PRIMITIVE_BINDING.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_PRIMITIVE_COALITION.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_ARCHETYPE.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_BRAND.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_VOICE.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_VISUAL.value: "activative-intelligence-runtime",
    ResponsibleLayer.AIR_LEARNING.value: "activative-intelligence-runtime",
    ResponsibleLayer.INTERVIEW_SOURCE.value: "interview-expression",
    ResponsibleLayer.INTERVIEW_REACTION.value: "interview-expression",
    ResponsibleLayer.PIPELINE_EXECUTION.value: "atomic-harness-pipeline",
    ResponsibleLayer.VAE_PRODUCTION.value: "visual-asset-editor",
    ResponsibleLayer.DELEGATION_TRANSPORT.value: "delegation-protocol",
    ResponsibleLayer.INDEPENDENT_EVALUATION.value: "independent-evaluation",
    ResponsibleLayer.HUMAN_DECISION.value: "human-operator",
    ResponsibleLayer.UNRESOLVED.value: "unresolved",
}


_ALLOWED_EPISTEMIC_TRANSITIONS: dict[str, frozenset[str]] = {
    EpistemicState.PLANNED.value: frozenset(
        {EpistemicState.REJECTED.value, EpistemicState.SUPERSEDED.value}
    ),
    EpistemicState.OBSERVED.value: frozenset(
        {
            EpistemicState.OPERATOR_CONFIRMED.value,
            EpistemicState.REJECTED.value,
            EpistemicState.SUPERSEDED.value,
        }
    ),
    EpistemicState.INFERRED.value: frozenset(
        {
            EpistemicState.OPERATOR_CONFIRMED.value,
            EpistemicState.REJECTED.value,
            EpistemicState.SUPERSEDED.value,
        }
    ),
    EpistemicState.OPERATOR_CONFIRMED.value: frozenset(
        {EpistemicState.SUPERSEDED.value}
    ),
    EpistemicState.REJECTED.value: frozenset(
        {EpistemicState.SUPERSEDED.value}
    ),
    EpistemicState.SUPERSEDED.value: frozenset(),
}

_ALLOWED_LIFECYCLE_TRANSITIONS: dict[str, frozenset[str]] = {
    LifecycleState.PROPOSED.value: frozenset(
        {
            LifecycleState.VALIDATED.value,
            LifecycleState.REJECTED.value,
            LifecycleState.SUPERSEDED.value,
        }
    ),
    LifecycleState.VALIDATED.value: frozenset(
        {
            LifecycleState.APPROVED.value,
            LifecycleState.REJECTED.value,
            LifecycleState.SUPERSEDED.value,
        }
    ),
    LifecycleState.APPROVED.value: frozenset(
        {LifecycleState.SUPERSEDED.value}
    ),
    LifecycleState.REJECTED.value: frozenset(
        {LifecycleState.SUPERSEDED.value}
    ),
    LifecycleState.SUPERSEDED.value: frozenset(),
}


def require_epistemic_transition(
    current: str,
    target: str,
    *,
    evidence_refs: Sequence[Mapping[str, Any]] = (),
    operator_decision_ref: Mapping[str, Any] | None = None,
) -> None:
    if target not in _ALLOWED_EPISTEMIC_TRANSITIONS.get(current, frozenset()):
        raise AirValidationError(
            "epistemic_transition",
            [f"transition is not allowed: {current} -> {target}"],
        )
    if current in {EpistemicState.OBSERVED.value, EpistemicState.INFERRED.value}:
        if target == EpistemicState.OPERATOR_CONFIRMED.value and operator_decision_ref is None:
            raise AirValidationError(
                "epistemic_transition",
                ["operator confirmation requires operator_decision_ref"],
            )
    if target in {
        EpistemicState.OBSERVED.value,
        EpistemicState.OPERATOR_CONFIRMED.value,
    } and not evidence_refs:
        raise AirValidationError(
            "epistemic_transition",
            [f"{target} requires non-empty evidence_refs"],
        )


def require_lifecycle_transition(current: str, target: str) -> None:
    if target not in _ALLOWED_LIFECYCLE_TRANSITIONS.get(current, frozenset()):
        raise AirValidationError(
            "lifecycle_transition",
            [f"transition is not allowed: {current} -> {target}"],
        )


def expected_owner_for_layer(layer: str) -> str:
    try:
        return _LAYER_OWNER[layer]
    except KeyError as exc:
        raise AirValidationError("responsible_layer", [f"unknown layer: {layer}"]) from exc


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _strict_fields(
    payload: Mapping[str, Any],
    *,
    required: Sequence[str],
    optional: Sequence[str] = (),
    issues: list[str],
) -> None:
    keys = set(payload)
    missing = set(required) - keys
    unknown = keys - set(required) - set(optional)
    if missing:
        issues.append(f"missing fields: {sorted(missing)}")
    if unknown:
        issues.append(f"unknown fields: {sorted(unknown)}")


def _string(
    payload: Mapping[str, Any],
    field: str,
    issues: list[str],
    *,
    allow_empty: bool = False,
    pattern: re.Pattern[str] | None = None,
) -> str | None:
    value = payload.get(field)
    if not isinstance(value, str):
        issues.append(f"{field} must be a string")
        return None
    if not allow_empty and not value.strip():
        issues.append(f"{field} must not be empty")
    if pattern is not None and not pattern.fullmatch(value):
        issues.append(f"{field} has invalid format")
    return value


def _integer(
    payload: Mapping[str, Any],
    field: str,
    issues: list[str],
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int | None:
    value = payload.get(field)
    if not isinstance(value, int) or isinstance(value, bool):
        issues.append(f"{field} must be an integer")
        return None
    if minimum is not None and value < minimum:
        issues.append(f"{field} must be >= {minimum}")
    if maximum is not None and value > maximum:
        issues.append(f"{field} must be <= {maximum}")
    return value


def _boolean(payload: Mapping[str, Any], field: str, issues: list[str]) -> bool | None:
    value = payload.get(field)
    if not isinstance(value, bool):
        issues.append(f"{field} must be boolean")
        return None
    return value


def _enum(
    payload: Mapping[str, Any],
    field: str,
    allowed: set[str] | frozenset[str],
    issues: list[str],
) -> str | None:
    value = payload.get(field)
    if not isinstance(value, str) or value not in allowed:
        issues.append(f"{field} must be one of {sorted(allowed)}")
        return None
    return value


def _strings(
    payload: Mapping[str, Any],
    field: str,
    issues: list[str],
    *,
    minimum: int = 0,
    unique: bool = False,
) -> tuple[str, ...]:
    value = payload.get(field)
    if not _is_sequence(value):
        issues.append(f"{field} must be an array")
        return ()
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            issues.append(f"{field}[{index}] must be a non-empty string")
        else:
            result.append(item)
    if len(result) < minimum:
        issues.append(f"{field} must contain at least {minimum} item(s)")
    if unique and len(result) != len(set(result)):
        issues.append(f"{field} must contain unique values")
    return tuple(result)


def _mapping_list(
    payload: Mapping[str, Any],
    field: str,
    issues: list[str],
    *,
    minimum: int = 0,
) -> tuple[Mapping[str, Any], ...]:
    value = payload.get(field)
    if not _is_sequence(value):
        issues.append(f"{field} must be an array")
        return ()
    result: list[Mapping[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            issues.append(f"{field}[{index}] must be an object")
        else:
            result.append(item)
    if len(result) < minimum:
        issues.append(f"{field} must contain at least {minimum} item(s)")
    return tuple(result)


def _ref(value: Any, field: str, issues: list[str], *, nullable: bool = False) -> dict[str, str] | None:
    if value is None and nullable:
        return None
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an immutable reference")
        return None
    expected = {"object_id", "version", "sha256"}
    if set(value) != expected:
        issues.append(f"{field} must contain exactly {sorted(expected)}")
        return None
    object_id = value.get("object_id")
    version = value.get("version")
    sha = value.get("sha256")
    if not isinstance(object_id, str) or not _ID.fullmatch(object_id):
        issues.append(f"{field}.object_id has invalid format")
    if not isinstance(version, str) or not version.strip():
        issues.append(f"{field}.version must be non-empty")
    if not isinstance(sha, str) or not _SHA256.fullmatch(sha):
        issues.append(f"{field}.sha256 must be 64 lowercase hex characters")
    if issues and (
        not isinstance(object_id, str)
        or not isinstance(version, str)
        or not isinstance(sha, str)
    ):
        return None
    return {"object_id": str(object_id), "version": str(version), "sha256": str(sha)}


def _refs(
    payload: Mapping[str, Any],
    field: str,
    issues: list[str],
    *,
    minimum: int = 0,
) -> tuple[dict[str, str], ...]:
    values = payload.get(field)
    if not _is_sequence(values):
        issues.append(f"{field} must be an array")
        return ()
    result: list[dict[str, str]] = []
    for index, value in enumerate(values):
        ref = _ref(value, f"{field}[{index}]", issues)
        if ref:
            result.append(ref)
    if len(result) < minimum:
        issues.append(f"{field} must contain at least {minimum} item(s)")
    return tuple(result)


def _authority(value: Any, field: str, issues: list[str]) -> dict[str, str] | None:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an authority reference")
        return None
    expected = {
        "authority_id",
        "authority_version",
        "authority_sha256",
        "authority_state",
    }
    if set(value) != expected:
        issues.append(f"{field} must contain exactly {sorted(expected)}")
        return None
    for name in ("authority_id", "authority_version", "authority_state"):
        if not isinstance(value.get(name), str) or not str(value[name]).strip():
            issues.append(f"{field}.{name} must be a non-empty string")
    if not isinstance(value.get("authority_sha256"), str) or not _SHA256.fullmatch(
        str(value.get("authority_sha256", ""))
    ):
        issues.append(f"{field}.authority_sha256 must be 64 lowercase hex characters")
    return {key: str(value[key]) for key in expected} if all(key in value for key in expected) else None


def _base(
    payload: Mapping[str, Any],
    issues: list[str],
    *,
    id_field: str,
    lifecycle_required: bool = True,
    epistemic_required: bool = True,
    extra_required: Sequence[str] = (),
    extra_optional: Sequence[str] = (),
) -> None:
    required = [id_field, "version", "authority", *extra_required]
    if lifecycle_required:
        required.append("lifecycle_state")
    if epistemic_required:
        required.append("epistemic_state")
    optional = ["supersedes_ref", *extra_optional]
    _strict_fields(payload, required=required, optional=optional, issues=issues)
    _string(payload, id_field, issues, pattern=_ID)
    _string(payload, "version", issues)
    _authority(payload.get("authority"), "authority", issues)
    if lifecycle_required:
        _enum(payload, "lifecycle_state", {item.value for item in LifecycleState}, issues)
    if epistemic_required:
        _enum(payload, "epistemic_state", {item.value for item in EpistemicState}, issues)
    if "supersedes_ref" in payload:
        _ref(payload.get("supersedes_ref"), "supersedes_ref", issues, nullable=True)


def _validate_matrix(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="matrix_id",
        extra_required=(
            "broad_signal",
            "hidden_pressure",
            "surviving_edge",
            "identity_gap",
            "audience_reality",
            "desired_recognition",
            "smallest_useful_movement",
            "counteractivation_risks",
            "source_refs",
        ),
    )
    for field in (
        "broad_signal",
        "hidden_pressure",
        "surviving_edge",
        "identity_gap",
        "audience_reality",
        "desired_recognition",
        "smallest_useful_movement",
    ):
        _string(payload, field, issues)
    _strings(payload, "counteractivation_risks", issues)
    _refs(payload, "source_refs", issues, minimum=1)


def _validate_context(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="context_id",
        extra_required=(
            "identity_dna_ref",
            "audience_context_ref",
            "live_premise",
            "matrix_of_edging_ref",
            "evidence_refs",
        ),
        extra_optional=("interviewer_resonance_ref", "relationship_state_ref"),
    )
    _ref(payload.get("identity_dna_ref"), "identity_dna_ref", issues)
    _ref(payload.get("audience_context_ref"), "audience_context_ref", issues)
    _ref(payload.get("matrix_of_edging_ref"), "matrix_of_edging_ref", issues)
    if "interviewer_resonance_ref" in payload:
        _ref(payload.get("interviewer_resonance_ref"), "interviewer_resonance_ref", issues, nullable=True)
    if "relationship_state_ref" in payload:
        _ref(payload.get("relationship_state_ref"), "relationship_state_ref", issues, nullable=True)
    _string(payload, "live_premise", issues)
    _refs(payload, "evidence_refs", issues, minimum=1)


def _validate_identity_observation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="observation_id",
        lifecycle_required=False,
        extra_required=(
            "identity_dna_ref",
            "proposed_dimension",
            "proposed_value",
            "evidence_refs",
            "recurrence_count",
            "contradictions",
            "applicability",
            "profile_resolution_status",
        ),
    )
    _ref(payload.get("identity_dna_ref"), "identity_dna_ref", issues)
    _enum(
        payload,
        "proposed_dimension",
        {
            "identity_role",
            "stance",
            "edge",
            "emotional_range",
            "visual_world",
            "negative_space",
            "lived_proof",
        },
        issues,
    )
    _string(payload, "proposed_value", issues)
    _refs(payload, "evidence_refs", issues, minimum=1)
    _integer(payload, "recurrence_count", issues, minimum=1)
    _strings(payload, "contradictions", issues)
    if not isinstance(payload.get("applicability"), Mapping):
        issues.append("applicability must be an object")
    _enum(
        payload,
        "profile_resolution_status",
        {"pending", "approved", "rejected", "superseded"},
        issues,
    )


def _validate_relation(value: Mapping[str, Any], field: str, issues: list[str]) -> None:
    _strict_fields(
        value,
        required=("relation_type", "target_primitive_id", "explanation"),
        issues=issues,
    )
    _enum(value, "relation_type", {"synergizes_with", "conflicts_with", "suppresses", "precedes"}, issues)
    _string(value, "target_primitive_id", issues, pattern=_ID)
    _string(value, "explanation", issues)


def _validate_primitive_binding(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="binding_id",
        extra_required=(
            "primitive_ref",
            "target_ref",
            "role_tension_ref",
            "governed_role",
            "local_function",
            "intended_effect",
            "execution_surface",
            "evidence_refs",
            "allowed_adaptations",
            "suppression_conditions",
            "relation_set",
            "misuse_risk_refs",
        ),
    )
    _ref(payload.get("primitive_ref"), "primitive_ref", issues)
    _ref(payload.get("target_ref"), "target_ref", issues)
    _ref(payload.get("role_tension_ref"), "role_tension_ref", issues)
    _enum(payload, "governed_role", {item.value for item in PrimitiveRole}, issues)
    for field in ("local_function", "intended_effect", "execution_surface"):
        _string(payload, field, issues)
    _refs(payload, "evidence_refs", issues, minimum=1)
    _strings(payload, "allowed_adaptations", issues)
    _strings(payload, "suppression_conditions", issues)
    for index, relation in enumerate(_mapping_list(payload, "relation_set", issues)):
        _validate_relation(relation, f"relation_set[{index}]", issues)
    _refs(payload, "misuse_risk_refs", issues)


def _validate_misuse_risk(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="risk_id",
        lifecycle_required=False,
        extra_required=(
            "primitive_ref",
            "misuse_mode",
            "trigger_condition",
            "probable_wrong_reading",
            "severity",
            "prevention_gate",
            "evidence_refs",
        ),
    )
    _ref(payload.get("primitive_ref"), "primitive_ref", issues)
    for field in ("misuse_mode", "trigger_condition", "probable_wrong_reading", "prevention_gate"):
        _string(payload, field, issues)
    _enum(payload, "severity", {"low", "moderate", "high", "fatal"}, issues)
    _refs(payload, "evidence_refs", issues)


def _validate_signature(value: Any, field: str, issues: list[str]) -> None:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an object")
        return
    _strict_fields(
        value,
        required=(
            "signature_id",
            "dominant_pressure_path",
            "recognition_move",
            "tension_release_pattern",
            "psychological_role_transition",
            "participation_threshold",
            "canonical_fingerprint",
        ),
        optional=("visual_attention_logic", "experiential_progression"),
        issues=issues,
    )
    for name in (
        "signature_id",
        "dominant_pressure_path",
        "recognition_move",
        "tension_release_pattern",
        "psychological_role_transition",
        "participation_threshold",
    ):
        _string(value, name, issues)
    _string(value, "canonical_fingerprint", issues, pattern=_SHA256)
    for name in ("visual_attention_logic", "experiential_progression"):
        if name in value and value[name] is not None:
            _string(value, name, issues)


def _validate_edge_product(value: Any, field: str, issues: list[str]) -> None:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an object")
        return
    _strict_fields(
        value,
        required=(
            "edge_product_id",
            "broad_signal_ref",
            "matrix_of_edging_ref",
            "hidden_pressure",
            "surviving_edge",
            "stance",
            "psychological_role",
            "tension",
            "consequence",
            "counteractivation_risks",
            "evidence_refs",
            "epistemic_state",
        ),
        issues=issues,
    )
    _string(value, "edge_product_id", issues, pattern=_ID)
    _ref(value.get("broad_signal_ref"), f"{field}.broad_signal_ref", issues)
    _ref(value.get("matrix_of_edging_ref"), f"{field}.matrix_of_edging_ref", issues)
    for name in (
        "hidden_pressure",
        "surviving_edge",
        "stance",
        "psychological_role",
        "tension",
        "consequence",
    ):
        _string(value, name, issues)
    _strings(value, "counteractivation_risks", issues)
    _refs(value, "evidence_refs", issues, minimum=1)
    _enum(value, "epistemic_state", {item.value for item in EpistemicState}, issues)


def _validate_coalition(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="coalition_id",
        epistemic_required=False,
        extra_required=(
            "source_context_refs",
            "binding_refs",
            "execution_order",
            "compatibility_explanation",
            "conflict_resolutions",
            "suppressed_binding_ids",
            "signature",
            "edge_product",
            "misuse_risk_refs",
            "evaluation_profile_ref",
        ),
    )
    _refs(payload, "source_context_refs", issues, minimum=1)
    bindings = _refs(payload, "binding_refs", issues, minimum=2)
    order = _strings(payload, "execution_order", issues, minimum=2, unique=True)
    binding_ids = {item["object_id"] for item in bindings}
    if set(order) != binding_ids:
        issues.append("execution_order must contain every binding object_id exactly once")
    _string(payload, "compatibility_explanation", issues)
    _strings(payload, "conflict_resolutions", issues)
    _strings(payload, "suppressed_binding_ids", issues, unique=True)
    _validate_signature(payload.get("signature"), "signature", issues)
    _validate_edge_product(payload.get("edge_product"), "edge_product", issues)
    _refs(payload, "misuse_risk_refs", issues)
    _ref(payload.get("evaluation_profile_ref"), "evaluation_profile_ref", issues)


def _validate_role_tension(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="contract_id",
        epistemic_required=False,
        extra_required=(
            "activation_domain",
            "psychological_role",
            "tension",
            "recognition_path",
            "stance",
            "participation_threshold",
            "counteractivation_roles",
            "transfer_invariants",
            "evidence_refs",
        ),
    )
    _enum(payload, "activation_domain", {item.value for item in ActivationDomain}, issues)
    for field in (
        "psychological_role",
        "tension",
        "recognition_path",
        "stance",
        "participation_threshold",
    ):
        _string(payload, field, issues)
    role = payload.get("psychological_role")
    tension = payload.get("tension")
    if isinstance(role, str) and isinstance(tension, str) and role.strip() == tension.strip():
        issues.append("psychological_role and tension must be distinct")
    _strings(payload, "counteractivation_roles", issues)
    _strings(payload, "transfer_invariants", issues, minimum=1)
    _refs(payload, "evidence_refs", issues, minimum=1)


def _validate_archetype_binding(value: Any, field: str, issues: list[str]) -> None:
    if not isinstance(value, Mapping):
        issues.append(f"{field} must be an object")
        return
    _strict_fields(
        value,
        required=(
            "binding_id",
            "archetype_ref",
            "current_validation_ref",
            "local_function",
            "source_fit",
            "category_geometry",
            "primitive_binding_ids",
            "rejection_conditions",
        ),
        issues=issues,
    )
    _string(value, "binding_id", issues, pattern=_ID)
    _ref(value.get("archetype_ref"), f"{field}.archetype_ref", issues)
    _ref(value.get("current_validation_ref"), f"{field}.current_validation_ref", issues)
    for name in ("local_function", "source_fit", "category_geometry"):
        _string(value, name, issues)
    _strings(value, "primitive_binding_ids", issues, minimum=1, unique=True)
    _strings(value, "rejection_conditions", issues)


def _validate_archetype_coalition(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="program_id",
        epistemic_required=False,
        extra_required=(
            "role_tension_contract_ref",
            "primitive_coalition_ref",
            "primary_archetype",
            "supporting_archetypes",
            "source_expression_refs",
            "category_target",
            "sequence_or_reading_logic",
            "anti_centroid_locks",
            "wrong_reading_locks",
            "rejected_alternatives",
        ),
    )
    _ref(payload.get("role_tension_contract_ref"), "role_tension_contract_ref", issues)
    _ref(payload.get("primitive_coalition_ref"), "primitive_coalition_ref", issues)
    _validate_archetype_binding(payload.get("primary_archetype"), "primary_archetype", issues)
    bindings = _mapping_list(payload, "supporting_archetypes", issues)
    for index, binding in enumerate(bindings):
        _validate_archetype_binding(binding, f"supporting_archetypes[{index}]", issues)
    _refs(payload, "source_expression_refs", issues, minimum=1)
    _string(payload, "category_target", issues)
    _string(payload, "sequence_or_reading_logic", issues)
    _strings(payload, "anti_centroid_locks", issues, minimum=1)
    _strings(payload, "wrong_reading_locks", issues, minimum=1)
    _strings(payload, "rejected_alternatives", issues)


def _validate_brand_context(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="brand_context_id",
        extra_required=(
            "brand_genesis_session_ref",
            "identity_truths",
            "audience_relationship",
            "positioning_tension",
            "source_refs",
        ),
    )
    _ref(payload.get("brand_genesis_session_ref"), "brand_genesis_session_ref", issues)
    _strings(payload, "identity_truths", issues, minimum=1)
    _string(payload, "audience_relationship", issues)
    _string(payload, "positioning_tension", issues)
    _refs(payload, "source_refs", issues, minimum=1)


def _validate_voice_dna(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="voice_dna_id",
        extra_required=(
            "brand_context_ref",
            "vocabulary_patterns",
            "rhythm_patterns",
            "sentence_pressure_patterns",
            "stance_patterns",
            "specificity_patterns",
            "metaphor_range",
            "emotional_distance",
            "prohibited_centroid_patterns",
            "source_evidence_refs",
        ),
    )
    _ref(payload.get("brand_context_ref"), "brand_context_ref", issues)
    for field in (
        "vocabulary_patterns",
        "rhythm_patterns",
        "sentence_pressure_patterns",
        "stance_patterns",
        "specificity_patterns",
        "metaphor_range",
        "prohibited_centroid_patterns",
    ):
        _strings(payload, field, issues)
    _string(payload, "emotional_distance", issues)
    _refs(payload, "source_evidence_refs", issues, minimum=1)


def _validate_visual_dna(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="visual_dna_id",
        extra_required=(
            "brand_context_ref",
            "real_life_reference_refs",
            "subject_treatment",
            "visual_temperature",
            "materiality",
            "composition_tendencies",
            "negative_space_functions",
            "edge_behaviors",
            "typographic_posture",
            "motion_character",
            "prohibited_centroid_defaults",
        ),
    )
    _ref(payload.get("brand_context_ref"), "brand_context_ref", issues)
    _refs(payload, "real_life_reference_refs", issues, minimum=1)
    for field in (
        "subject_treatment",
        "visual_temperature",
        "materiality",
        "composition_tendencies",
        "negative_space_functions",
        "edge_behaviors",
        "typographic_posture",
        "motion_character",
        "prohibited_centroid_defaults",
    ):
        _strings(payload, field, issues)


def _validate_distillation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "layer",
            "input_refs",
            "output_refs",
            "decisions",
            "edge_product_preserved",
            "role_tension_preserved",
            "voice_dna_preserved",
            "visual_dna_preserved",
            "rejection_refs",
        ),
    )
    _enum(payload, "layer", {"saturation", "collision", "compression", "evaluation", "recursion"}, issues)
    _refs(payload, "input_refs", issues, minimum=1)
    _refs(payload, "output_refs", issues, minimum=1)
    _strings(payload, "decisions", issues, minimum=1)
    _boolean(payload, "edge_product_preserved", issues)
    _boolean(payload, "role_tension_preserved", issues)
    if payload.get("voice_dna_preserved") is not None:
        _boolean(payload, "voice_dna_preserved", issues)
    if payload.get("visual_dna_preserved") is not None:
        _boolean(payload, "visual_dna_preserved", issues)
    _refs(payload, "rejection_refs", issues)


def _validate_change(value: Mapping[str, Any], field: str, issues: list[str]) -> None:
    _strict_fields(
        value,
        required=("operation", "target_ref", "parameter_changes"),
        issues=issues,
    )
    _string(value, "operation", issues)
    _ref(value.get("target_ref"), f"{field}.target_ref", issues)
    parameter_changes = value.get("parameter_changes")
    if not isinstance(parameter_changes, Mapping):
        issues.append(f"{field}.parameter_changes must be an object")
    else:
        for key, item in parameter_changes.items():
            if not isinstance(key, str) or not key.strip():
                issues.append(f"{field}.parameter_changes keys must be non-empty strings")
            if item is not None and not isinstance(item, (str, int, bool)):
                issues.append(
                    f"{field}.parameter_changes[{key!r}] must be string, integer, boolean, or null"
                )


def _validate_human_resolution(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="episode_id",
        extra_required=(
            "before_state_refs",
            "operator_request",
            "interpreted_target",
            "exact_changes",
            "tools_invoked",
            "models_or_runtimes",
            "context_refs",
            "invariants",
            "required_transformations",
            "creative_freedom",
            "wrong_reading_locks",
            "result_refs",
            "evaluation_refs",
            "operator_verdict",
            "applicability_scope",
            "programming_material_dispositions",
            "promotion_status",
        ),
    )
    _refs(payload, "before_state_refs", issues, minimum=1)
    _string(payload, "operator_request", issues)
    _string(payload, "interpreted_target", issues)
    for index, change in enumerate(_mapping_list(payload, "exact_changes", issues, minimum=1)):
        _validate_change(change, f"exact_changes[{index}]", issues)
    _strings(payload, "tools_invoked", issues)
    _strings(payload, "models_or_runtimes", issues)
    _refs(payload, "context_refs", issues)
    _strings(payload, "invariants", issues, minimum=1)
    _strings(payload, "required_transformations", issues)
    _strings(payload, "creative_freedom", issues)
    _strings(payload, "wrong_reading_locks", issues)
    _refs(payload, "result_refs", issues)
    _refs(payload, "evaluation_refs", issues)
    _enum(payload, "operator_verdict", {"approved", "rejected", "amended", "deferred"}, issues)
    if not isinstance(payload.get("applicability_scope"), Mapping):
        issues.append("applicability_scope must be an object")
    _strings(
        payload,
        "programming_material_dispositions",
        issues,
        minimum=1,
    )
    _enum(payload, "promotion_status", {"captured_not_promoted"}, issues)


def _validate_failure(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="failure_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "failed_object_ref",
            "observed_symptom",
            "responsible_layer",
            "owner_product",
            "evidence_refs",
            "preserved_property_refs",
            "invalidated_descendant_refs",
            "confidence_bps",
            "status",
        ),
    )
    _ref(payload.get("failed_object_ref"), "failed_object_ref", issues)
    _string(payload, "observed_symptom", issues)
    layer = _enum(payload, "responsible_layer", {item.value for item in ResponsibleLayer}, issues)
    owner = _string(payload, "owner_product", issues)
    if layer and owner and expected_owner_for_layer(layer) != owner:
        issues.append(
            f"owner_product {owner!r} does not own responsible_layer {layer!r}; "
            f"expected {expected_owner_for_layer(layer)!r}"
        )
    _refs(payload, "evidence_refs", issues, minimum=1)
    _refs(payload, "preserved_property_refs", issues)
    _refs(payload, "invalidated_descendant_refs", issues)
    _integer(payload, "confidence_bps", issues, minimum=0, maximum=10000)
    _enum(payload, "status", {"proposed", "confirmed", "disputed", "resolved"}, issues)


def _validate_repair(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="repair_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "failure_ref",
            "responsible_layer",
            "owner_product",
            "repair_mode",
            "target_refs",
            "allowed_operations",
            "protected_refs",
            "rerun_node_refs",
        ),
    )
    _ref(payload.get("failure_ref"), "failure_ref", issues)
    layer = _enum(payload, "responsible_layer", {item.value for item in ResponsibleLayer}, issues)
    owner = _string(payload, "owner_product", issues)
    mode = _enum(payload, "repair_mode", {"local_repair", "owner_referral"}, issues)
    if layer and owner and expected_owner_for_layer(layer) != owner:
        issues.append("repair owner_product does not match responsible_layer owner")
    if layer and mode:
        expected_mode = "local_repair" if layer in AIR_OWNED_LAYERS else "owner_referral"
        if mode != expected_mode:
            issues.append(
                f"repair_mode for {layer} must be {expected_mode}"
            )
    _refs(payload, "target_refs", issues, minimum=1)
    _strings(payload, "allowed_operations", issues, minimum=1)
    _refs(payload, "protected_refs", issues)
    _refs(payload, "rerun_node_refs", issues)



def _validate_epistemic_transition_receipt(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "object_ref",
            "from_state",
            "to_state",
            "evidence_refs",
            "operator_decision_ref",
            "reason",
        ),
    )
    _ref(payload.get("object_ref"), "object_ref", issues)
    current = _enum(payload, "from_state", {item.value for item in EpistemicState}, issues)
    target = _enum(payload, "to_state", {item.value for item in EpistemicState}, issues)
    evidence = _refs(payload, "evidence_refs", issues)
    operator_ref = _ref(
        payload.get("operator_decision_ref"),
        "operator_decision_ref",
        issues,
        nullable=True,
    )
    _string(payload, "reason", issues)
    if current and target:
        try:
            require_epistemic_transition(
                current,
                target,
                evidence_refs=evidence,
                operator_decision_ref=operator_ref,
            )
        except AirValidationError as exc:
            issues.extend(exc.issues)


def _validate_primitive_evaluation_receipt(payload: Mapping[str, Any], issues: list[str]) -> None:
    _base(
        payload,
        issues,
        id_field="receipt_id",
        lifecycle_required=False,
        epistemic_required=False,
        extra_required=(
            "coalition_ref",
            "binding_results",
            "conflict_gate_passed",
            "misuse_gate_passed",
            "coalition_signature_preserved",
            "edge_product_preserved",
            "evidence_refs",
            "verdict",
        ),
    )
    _ref(payload.get("coalition_ref"), "coalition_ref", issues)
    binding_results = _mapping_list(payload, "binding_results", issues, minimum=1)
    seen: set[str] = set()
    all_pass = True
    for index, item in enumerate(binding_results):
        _strict_fields(
            item,
            required=("binding_ref", "result"),
            optional=("reason",),
            issues=issues,
        )
        ref = _ref(item.get("binding_ref"), f"binding_results[{index}].binding_ref", issues)
        result = _enum(
            item,
            "result",
            {"pass", "fail", "not_applicable"},
            issues,
        )
        if ref:
            if ref["object_id"] in seen:
                issues.append("binding_results must contain each binding once")
            seen.add(ref["object_id"])
        if result not in {"pass", "not_applicable"}:
            all_pass = False
        if "reason" in item:
            _string(item, "reason", issues)
    gates = []
    for field in (
        "conflict_gate_passed",
        "misuse_gate_passed",
        "coalition_signature_preserved",
        "edge_product_preserved",
    ):
        gates.append(_boolean(payload, field, issues))
    _refs(payload, "evidence_refs", issues, minimum=1)
    verdict = _enum(payload, "verdict", {"pass", "fail", "insufficient_evidence"}, issues)
    if verdict == "pass" and (not all_pass or not all(item is True for item in gates)):
        issues.append("Primitive evaluation cannot pass when a hard gate or binding fails")

_VALIDATORS: dict[str, Callable[[Mapping[str, Any], list[str]], None]] = {
    "epistemic_transition_receipt": _validate_epistemic_transition_receipt,
    "primitive_evaluation_receipt": _validate_primitive_evaluation_receipt,
    "matrix_of_edging": _validate_matrix,
    "activative_context": _validate_context,
    "identity_dna_candidate_observation": _validate_identity_observation,
    "primitive_binding": _validate_primitive_binding,
    "primitive_misuse_risk": _validate_misuse_risk,
    "primitive_coalition_contract": _validate_coalition,
    "psychological_role_tension_contract": _validate_role_tension,
    "archetype_coalition_program": _validate_archetype_coalition,
    "brand_context_version": _validate_brand_context,
    "voice_dna": _validate_voice_dna,
    "visual_dna": _validate_visual_dna,
    "distillation_layer_receipt": _validate_distillation,
    "human_resolution_episode": _validate_human_resolution,
    "failure_attribution": _validate_failure,
    "repair_program": _validate_repair,
}

_ID_FIELDS = {
    "epistemic_transition_receipt": "receipt_id",
    "primitive_evaluation_receipt": "receipt_id",
    "matrix_of_edging": "matrix_id",
    "activative_context": "context_id",
    "identity_dna_candidate_observation": "observation_id",
    "primitive_binding": "binding_id",
    "primitive_misuse_risk": "risk_id",
    "primitive_coalition_contract": "coalition_id",
    "psychological_role_tension_contract": "contract_id",
    "archetype_coalition_program": "program_id",
    "brand_context_version": "brand_context_id",
    "voice_dna": "voice_dna_id",
    "visual_dna": "visual_dna_id",
    "distillation_layer_receipt": "receipt_id",
    "human_resolution_episode": "episode_id",
    "failure_attribution": "failure_id",
    "repair_program": "repair_id",
}


def supported_object_types() -> tuple[str, ...]:
    return tuple(sorted(_VALIDATORS))


def validate_air_object(object_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if object_type not in _VALIDATORS:
        raise AirValidationError(object_type, [f"unsupported object type; expected one of {supported_object_types()}"])
    if not isinstance(payload, Mapping):
        raise AirValidationError(object_type, ["payload must be an object"])
    issues: list[str] = []
    _VALIDATORS[object_type](payload, issues)
    try:
        canonical_sha256(payload)
    except Exception as exc:
        issues.append(f"payload is not canonical-JSON-safe: {exc}")
    if issues:
        raise AirValidationError(object_type, issues)
    return copy.deepcopy(dict(payload))


def object_identity(object_type: str, payload: Mapping[str, Any]) -> str:
    return str(payload[_ID_FIELDS[object_type]])


def object_semantic_version(payload: Mapping[str, Any]) -> str:
    return str(payload["version"])


def object_epistemic_state(payload: Mapping[str, Any]) -> str | None:
    value = payload.get("epistemic_state")
    return str(value) if value is not None else None


def object_lifecycle_state(payload: Mapping[str, Any]) -> str | None:
    value = payload.get("lifecycle_state")
    return str(value) if value is not None else None


def schema_registry() -> dict[str, Any]:
    """Return strict schema metadata used for documentation and test generation.

    Runtime validation is performed by the exact validators above. The exported
    schemas intentionally describe the common closed envelope and identify the
    object-specific validator rather than pretending these development schemas
    are already a shared cross-product contract release.
    """
    result: dict[str, Any] = {}
    for object_type, id_field in sorted(_ID_FIELDS.items()):
        result[object_type] = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"https://contracts.conscious-activations.local/air-core/0.2.0-dev.1/{object_type}.schema.json",
            "title": object_type,
            "type": "object",
            "additionalProperties": False,
            "x-runtime-validator": f"cmf_activative_intelligence.domain:{_VALIDATORS[object_type].__name__}",
            "x-identity-field": id_field,
            "x-authority-state": "candidate_not_current",
            "x-production-authorized": False,
        }
    return result
