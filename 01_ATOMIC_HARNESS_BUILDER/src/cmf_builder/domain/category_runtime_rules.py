from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.category_syntax import (
    ACTIVATION_FIRST,
    CATEGORY_PROFILE_CONTRACTS,
    MATURITY_STATUS,
    NOT_APPLICABLE,
    VISUAL_SYNTAX_FIRST,
    ActivativeSequenceProgram,
    CategoryNativeSyntax,
    GovernedRef,
)


RULESET_MATURITY = "OFFLINE_DECLARATIVE_IMPLEMENTED_EXTERNAL_EVIDENCE_PENDING"
STRUCTURAL_COMPATIBILITY = "STRUCTURAL_UNCERTIFIED_EXTERNAL_VALIDATION_PENDING"


class CategoryPolicyError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class CategoryPolicyInput:
    ruleset_name: str
    ruleset_version: str
    syntax: CategoryNativeSyntax
    sequence: ActivativeSequenceProgram
    evaluator_owner_ref: GovernedRef | None
    repair_owner_ref: GovernedRef | None
    migration_authority_ref: GovernedRef | None
    compatibility_authority_ref: GovernedRef | None
    requested_external_execution: bool = False
    requested_certification: bool = False

    def canonical_dict(self) -> dict[str, object]:
        return {
            "ruleset_name": self.ruleset_name,
            "ruleset_version": self.ruleset_version,
            "syntax_hash": self.syntax.syntax_hash,
            "sequence_hash": self.sequence.sequence_hash,
            "evaluator_owner_ref": _optional_ref(self.evaluator_owner_ref),
            "repair_owner_ref": _optional_ref(self.repair_owner_ref),
            "migration_authority_ref": _optional_ref(self.migration_authority_ref),
            "compatibility_authority_ref": _optional_ref(
                self.compatibility_authority_ref
            ),
            "requested_external_execution": self.requested_external_execution,
            "requested_certification": self.requested_certification,
        }


@dataclass(frozen=True, slots=True)
class DiagnosticRoute:
    diagnostic_code: str
    detection: str
    owner: str
    repair_unit: str | None
    stop_condition: str

    def canonical_dict(self) -> dict[str, object]:
        return {
            "diagnostic_code": self.diagnostic_code,
            "detection": self.detection,
            "owner": self.owner,
            "repair_unit": self.repair_unit,
            "stop_condition": self.stop_condition,
        }


@dataclass(frozen=True, slots=True)
class ExternalHandoffBoundary:
    mode: str
    external_validation_status: str
    allowed: tuple[str, ...]
    prohibited: tuple[str, ...]

    def canonical_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode,
            "external_validation_status": self.external_validation_status,
            "allowed": list(self.allowed),
            "prohibited": list(self.prohibited),
        }


@dataclass(frozen=True, slots=True)
class CategoryOperatingRules:
    ruleset_id: str
    ruleset_name: str
    ruleset_version: str
    applicability: str
    category_id: str | None
    profile_id: str | None
    atomic_owner_category_id: str | None
    category_constitution_version: str | None
    syntax_hash: str
    sequence_hash: str
    runtime_law: str
    development_law: str
    runtime_plan_requirements: tuple[str, ...]
    validation_gates: tuple[str, ...]
    evaluation_dimensions: tuple[str, ...]
    evaluator_owner_ref: GovernedRef | None
    diagnostic_routes: tuple[DiagnosticRoute, ...]
    repair_units: tuple[str, ...]
    repair_owner_ref: GovernedRef | None
    selective_rerun_rules: tuple[str, ...]
    migration_policy: tuple[str, ...]
    migration_authority_ref: GovernedRef | None
    compatibility_policy: tuple[str, ...]
    compatibility_authority_ref: GovernedRef | None
    invalidation_triggers: tuple[str, ...]
    rollback_policy: tuple[str, ...]
    external_handoff_boundary: ExternalHandoffBoundary
    maturity_status: str
    compatibility_status: str
    production_ready: bool
    certified: bool
    ruleset_hash: str
    canonical_bytes: bytes

    def canonical_dict(self) -> dict[str, object]:
        content = json.loads(self.canonical_bytes.decode("utf-8"))
        content["ruleset_hash"] = self.ruleset_hash
        return content

    def validate_repair_request(
        self,
        *,
        category_id: str,
        repair_unit: str,
        evaluator_owner_id: str,
        repair_owner_id: str,
    ) -> None:
        if self.applicability == NOT_APPLICABLE:
            raise CategoryPolicyError("Generic tasks have no category repair contract.")
        if category_id != self.atomic_owner_category_id:
            raise CategoryPolicyError("Cross-category repair is prohibited.")
        if repair_unit not in self.repair_units:
            raise CategoryPolicyError("Repair unit is not category-owned.")
        if (
            self.evaluator_owner_ref is None
            or evaluator_owner_id != self.evaluator_owner_ref.object_id
        ):
            raise CategoryPolicyError("Evaluator ownership is missing or mismatched.")
        if self.repair_owner_ref is None or repair_owner_id != self.repair_owner_ref.object_id:
            raise CategoryPolicyError("Repair ownership is missing or mismatched.")

    def validate_selective_rerun(
        self, *, category_id: str, affected_units: tuple[str, ...]
    ) -> None:
        if category_id != self.atomic_owner_category_id:
            raise CategoryPolicyError("Selective rerun cannot cross category ownership.")
        if not affected_units or any(unit not in self.repair_units for unit in affected_units):
            raise CategoryPolicyError("Selective rerun contains an undeclared unit.")

    def validate_migration(
        self,
        *,
        target_category_id: str,
        target_profile_id: str | None,
        target_ruleset_version: str,
        inherit_certification: bool,
        transfer_atomic_ownership: bool,
    ) -> None:
        if self.applicability == NOT_APPLICABLE:
            raise CategoryPolicyError("Generic tasks have no category profile migration.")
        if target_category_id != self.category_id:
            raise CategoryPolicyError("Cross-category migration is prohibited.")
        if transfer_atomic_ownership:
            raise CategoryPolicyError("Atomic creative ownership cannot transfer by migration.")
        if target_ruleset_version == self.ruleset_version:
            raise CategoryPolicyError("Migration requires a new immutable ruleset version.")
        governed_profiles = CATEGORY_PROFILE_CONTRACTS[target_category_id]
        if governed_profiles and target_profile_id not in governed_profiles:
            raise CategoryPolicyError("Target profile is not owned by the category.")
        if not governed_profiles and target_profile_id is not None:
            raise CategoryPolicyError("The category has no registered profile to migrate to.")
        if inherit_certification:
            raise CategoryPolicyError("Certification cannot be inherited through migration.")


def compile_category_operating_rules(source: CategoryPolicyInput) -> CategoryOperatingRules:
    _require_text(source.ruleset_name, "ruleset_name")
    _require_text(source.ruleset_version, "ruleset_version")
    _validate_source_artifacts(source.syntax, source.sequence)
    if source.requested_external_execution:
        raise CategoryPolicyError("External runtime execution is outside the Builder boundary.")
    if source.requested_certification:
        raise CategoryPolicyError("The offline branch cannot claim certification.")
    if source.syntax.applicability == NOT_APPLICABLE:
        _validate_generic_owners(source)
        return _compile_generic(source)
    owners = _validate_owners(source)
    category_id = source.syntax.category_id
    if category_id is None:
        raise CategoryPolicyError("An applicable ruleset requires category ownership.")
    local = _CATEGORY_RULES[category_id]
    diagnostic_routes = (
        DiagnosticRoute(
            "CATEGORY_SYNTAX_DRIFT",
            "syntax hash or category-native grammar mismatch",
            owners[0].object_id,
            local[3][0],
            "STOP_BEFORE_RUNTIME_PLAN",
        ),
        DiagnosticRoute(
            "ACTIVATIVE_SEQUENCE_DRIFT",
            "sequence linkage or semantic progression mismatch",
            owners[0].object_id,
            local[3][1],
            "STOP_BEFORE_RUNTIME_PLAN",
        ),
        DiagnosticRoute(
            "AUTHORITY_OR_OWNERSHIP_CONFLICT",
            "category evaluator repair or migration owner mismatch",
            owners[2].object_id,
            None,
            "STOP_AND_REQUIRE_GOVERNED_AUTHORITY",
        ),
    )
    external_boundary = ExternalHandoffBoundary(
        mode="BUILDER_CONTRACT_ONLY",
        external_validation_status="BD-014:EXTERNAL_VALIDATION_PENDING",
        allowed=(
            "immutable_request_contract",
            "immutable_result_contract",
            "local_deterministic_test_double",
            "typed_failure_mapping",
        ),
        prohibited=(
            "external_runtime_execution",
            "network_transport",
            "external_product_internal_behavior",
            "production_acceptance_claim",
        ),
    )
    content: dict[str, object] = {
        "schema_version": "cmf-builder-category-operating-rules/v1",
        "ruleset_name": source.ruleset_name,
        "ruleset_version": source.ruleset_version,
        "applicability": "REQUIRED",
        "category_id": category_id,
        "profile_id": source.syntax.profile_id,
        "atomic_owner_category_id": category_id,
        "category_constitution_version": source.syntax.category_constitution_version,
        "syntax_hash": source.syntax.syntax_hash,
        "sequence_hash": source.sequence.sequence_hash,
        "runtime_law": ACTIVATION_FIRST,
        "development_law": VISUAL_SYNTAX_FIRST,
        "runtime_plan_requirements": list(local[0]),
        "validation_gates": list(_COMMON_VALIDATION_GATES + local[1]),
        "evaluation_dimensions": list(_COMMON_EVALUATION_DIMENSIONS + local[2]),
        "evaluator_owner_ref": owners[0].canonical_dict(),
        "diagnostic_routes": [route.canonical_dict() for route in diagnostic_routes],
        "repair_units": list(local[3]),
        "repair_owner_ref": owners[1].canonical_dict(),
        "selective_rerun_rules": list(_SELECTIVE_RERUN_RULES),
        "migration_policy": list(_MIGRATION_POLICY),
        "migration_authority_ref": owners[2].canonical_dict(),
        "compatibility_policy": list(_COMPATIBILITY_POLICY),
        "compatibility_authority_ref": owners[3].canonical_dict(),
        "invalidation_triggers": list(_INVALIDATION_TRIGGERS),
        "rollback_policy": list(_ROLLBACK_POLICY),
        "external_handoff_boundary": external_boundary.canonical_dict(),
        "maturity_status": RULESET_MATURITY,
        "compatibility_status": STRUCTURAL_COMPATIBILITY,
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return CategoryOperatingRules(
        ruleset_id=f"category-operating-rules_{digest}",
        ruleset_name=source.ruleset_name,
        ruleset_version=source.ruleset_version,
        applicability="REQUIRED",
        category_id=category_id,
        profile_id=source.syntax.profile_id,
        atomic_owner_category_id=category_id,
        category_constitution_version=source.syntax.category_constitution_version,
        syntax_hash=source.syntax.syntax_hash,
        sequence_hash=source.sequence.sequence_hash,
        runtime_law=ACTIVATION_FIRST,
        development_law=VISUAL_SYNTAX_FIRST,
        runtime_plan_requirements=local[0],
        validation_gates=_COMMON_VALIDATION_GATES + local[1],
        evaluation_dimensions=_COMMON_EVALUATION_DIMENSIONS + local[2],
        evaluator_owner_ref=owners[0],
        diagnostic_routes=diagnostic_routes,
        repair_units=local[3],
        repair_owner_ref=owners[1],
        selective_rerun_rules=_SELECTIVE_RERUN_RULES,
        migration_policy=_MIGRATION_POLICY,
        migration_authority_ref=owners[2],
        compatibility_policy=_COMPATIBILITY_POLICY,
        compatibility_authority_ref=owners[3],
        invalidation_triggers=_INVALIDATION_TRIGGERS,
        rollback_policy=_ROLLBACK_POLICY,
        external_handoff_boundary=external_boundary,
        maturity_status=RULESET_MATURITY,
        compatibility_status=STRUCTURAL_COMPATIBILITY,
        production_ready=False,
        certified=False,
        ruleset_hash=f"sha256:{digest}",
        canonical_bytes=canonical_bytes,
    )


_COMMON_VALIDATION_GATES = (
    "exact_category_identity",
    "exact_profile_ownership",
    "syntax_and_sequence_hash_validity",
    "immutable_rich_lineage",
    "non_empty_wrong_reading_locks",
    "authority_owner_match",
    "activation_first_conformance",
    "no_certification_inheritance",
)
_COMMON_EVALUATION_DIMENSIONS = (
    "category_identity_preservation",
    "activative_sequence_integrity",
    "rich_lineage_completeness",
    "wrong_reading_resistance",
    "output_contract_compliance",
)
_SELECTIVE_RERUN_RULES = (
    "rerun_only_declared_category_owned_units",
    "preserve_valid_independent_units",
    "changed_input_requires_new_immutable_ruleset",
    "never_cross_atomic_category_ownership",
)
_MIGRATION_POLICY = (
    "same_category_only",
    "new_immutable_version_required",
    "target_profile_must_be_category_owned",
    "impact_report_required",
    "certification_never_inherited",
    "atomic_ownership_never_transferred",
)
_COMPATIBILITY_POLICY = (
    "category_identity_is_invariant",
    "profile_maturity_dimensions_are_independent",
    "structural_support_does_not_imply_certification",
    "external_contract_validation_remains_pending",
)
_INVALIDATION_TRIGGERS = (
    "category_constitution_version_changed",
    "category_native_syntax_hash_changed",
    "activative_sequence_hash_changed",
    "profile_identity_or_version_changed",
    "owner_authority_invalidated",
)
_ROLLBACK_POLICY = (
    "never_mutate_predecessor_artifacts",
    "discard_uncommitted_rules_atomically",
    "preserve_historical_ruleset_bytes",
    "reactivation_requires_hash_valid_governed_inputs",
)


_CATEGORY_RULES: Mapping[
    str, tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...], tuple[str, ...]]
] = {
    "short_form_edited_video": (
        (
            "ordered_time_state_plan",
            "edited_transition_plan",
            "reading_order_plan",
            "activative_sequence_reference",
        ),
        ("edited_timeline_not_animation_alias",),
        ("temporal_coherence", "reading_order_integrity", "payoff_integrity"),
        ("time_state_unit", "sequence_transition_unit", "reading_order_unit"),
    ),
    "2d_character_animation": (
        (
            "character_performance_registry_plan",
            "staging_and_framing_plan",
            "character_state_continuity_plan",
            "activative_sequence_reference",
        ),
        ("animation_performance_not_edited_video_alias",),
        ("performance_continuity", "character_state_integrity", "staging_integrity"),
        ("performance_unit", "sequence_transition_unit", "staging_unit"),
    ),
    "carousels": (
        (
            "slide_role_plan",
            "swipe_order_plan",
            "cross_slide_continuity_plan",
            "activative_sequence_reference",
        ),
        ("static_slides_never_frame_time_motion",),
        ("slide_role_integrity", "swipe_progression", "cross_slide_continuity"),
        ("slide_role_unit", "sequence_transition_unit", "swipe_order_unit"),
    ),
    "supervisuals": (
        (
            "single_frame_hierarchy_plan",
            "feed_size_legibility_plan",
            "reading_order_plan",
            "activative_sequence_reference",
        ),
        ("single_frame_never_timeline",),
        ("attention_hierarchy", "feed_legibility", "static_reading_order"),
        ("hierarchy_unit", "sequence_transition_unit", "reading_order_unit"),
    ),
    "conversational_activation_expression": (
        (
            "turn_relationship_plan",
            "activative_call_contract",
            "human_reaction_reference_gate",
            "consent_policy_reference_gate",
            "activative_sequence_reference",
        ),
        (
            "conversation_never_timeline_or_generic_document",
            "human_reaction_is_reference_only",
        ),
        ("turn_integrity", "human_authority_preservation", "commitment_integrity"),
        ("turn_contract_unit", "sequence_transition_unit", "call_contract_unit"),
    ),
}


def _validate_source_artifacts(
    syntax: CategoryNativeSyntax, sequence: ActivativeSequenceProgram
) -> None:
    if syntax.syntax_hash != f"sha256:{sha256(syntax.canonical_bytes).hexdigest()}":
        raise CategoryPolicyError("Category syntax hash is invalid or altered.")
    if sequence.sequence_hash != f"sha256:{sha256(sequence.canonical_bytes).hexdigest()}":
        raise CategoryPolicyError("Activative sequence hash is invalid or altered.")
    if sequence.category_syntax_ref != syntax.syntax_hash:
        raise CategoryPolicyError("Sequence does not reference the exact category syntax.")
    if (syntax.harness_id, syntax.harness_version) != (
        sequence.harness_id,
        sequence.harness_version,
    ):
        raise CategoryPolicyError("Syntax and sequence Harness lineage does not match.")
    if syntax.applicability != sequence.applicability:
        raise CategoryPolicyError("Syntax and sequence applicability does not match.")
    if syntax.runtime_law != ACTIVATION_FIRST or sequence.runtime_law != ACTIVATION_FIRST:
        raise CategoryPolicyError("Activation First is required as runtime law.")
    if (
        syntax.development_law != VISUAL_SYNTAX_FIRST
        or sequence.development_law != VISUAL_SYNTAX_FIRST
    ):
        raise CategoryPolicyError("Visual Syntax First is required as development law.")
    if syntax.maturity_status != MATURITY_STATUS or sequence.maturity_status != MATURITY_STATUS:
        raise CategoryPolicyError("Only the active ST-06.03 offline artifacts may compile.")
    if syntax.production_ready or sequence.production_ready or syntax.certified or sequence.certified:
        raise CategoryPolicyError("Unsupported readiness or certification claim detected.")


def _validate_owners(source: CategoryPolicyInput) -> tuple[GovernedRef, ...]:
    values = (
        (source.evaluator_owner_ref, "evaluation_owner"),
        (source.repair_owner_ref, "repair_owner"),
        (source.migration_authority_ref, "migration_authority"),
        (source.compatibility_authority_ref, "compatibility_authority"),
    )
    result: list[GovernedRef] = []
    for ref, expected_role in values:
        if ref is None:
            raise CategoryPolicyError(f"{expected_role} is required.")
        ref.validate()
        if ref.lineage_role != expected_role:
            raise CategoryPolicyError(f"{expected_role} has a conflicting owner role.")
        result.append(ref)
    if len({ref.object_id for ref in result}) != len(result):
        raise CategoryPolicyError("Operating-rule ownership identities must be explicit.")
    return tuple(result)


def _validate_generic_owners(source: CategoryPolicyInput) -> None:
    if any(
        ref is not None
        for ref in (
            source.evaluator_owner_ref,
            source.repair_owner_ref,
            source.migration_authority_ref,
            source.compatibility_authority_ref,
        )
    ):
        raise CategoryPolicyError("Generic NOT_APPLICABLE rules cannot claim category owners.")


def _compile_generic(source: CategoryPolicyInput) -> CategoryOperatingRules:
    boundary = ExternalHandoffBoundary(
        mode=NOT_APPLICABLE,
        external_validation_status=NOT_APPLICABLE,
        allowed=(),
        prohibited=("category_external_handoff",),
    )
    content: dict[str, object] = {
        "schema_version": "cmf-builder-category-operating-rules/v1",
        "ruleset_name": source.ruleset_name,
        "ruleset_version": source.ruleset_version,
        "applicability": NOT_APPLICABLE,
        "category_id": None,
        "profile_id": None,
        "atomic_owner_category_id": None,
        "category_constitution_version": None,
        "syntax_hash": source.syntax.syntax_hash,
        "sequence_hash": source.sequence.sequence_hash,
        "runtime_law": ACTIVATION_FIRST,
        "development_law": VISUAL_SYNTAX_FIRST,
        "runtime_plan_requirements": [],
        "validation_gates": [],
        "evaluation_dimensions": [],
        "evaluator_owner_ref": None,
        "diagnostic_routes": [],
        "repair_units": [],
        "repair_owner_ref": None,
        "selective_rerun_rules": [],
        "migration_policy": [],
        "migration_authority_ref": None,
        "compatibility_policy": ["GENERIC_NON_ACTIVATIVE_TASK"],
        "compatibility_authority_ref": None,
        "invalidation_triggers": ["source_syntax_or_sequence_changed"],
        "rollback_policy": ["discard_uncommitted_rules_atomically"],
        "external_handoff_boundary": boundary.canonical_dict(),
        "maturity_status": RULESET_MATURITY,
        "compatibility_status": NOT_APPLICABLE,
        "production_ready": False,
        "certified": False,
    }
    canonical_bytes = _canonical_json(content)
    digest = sha256(canonical_bytes).hexdigest()
    return CategoryOperatingRules(
        ruleset_id=f"category-operating-rules_{digest}",
        ruleset_name=source.ruleset_name,
        ruleset_version=source.ruleset_version,
        applicability=NOT_APPLICABLE,
        category_id=None,
        profile_id=None,
        atomic_owner_category_id=None,
        category_constitution_version=None,
        syntax_hash=source.syntax.syntax_hash,
        sequence_hash=source.sequence.sequence_hash,
        runtime_law=ACTIVATION_FIRST,
        development_law=VISUAL_SYNTAX_FIRST,
        runtime_plan_requirements=(),
        validation_gates=(),
        evaluation_dimensions=(),
        evaluator_owner_ref=None,
        diagnostic_routes=(),
        repair_units=(),
        repair_owner_ref=None,
        selective_rerun_rules=(),
        migration_policy=(),
        migration_authority_ref=None,
        compatibility_policy=("GENERIC_NON_ACTIVATIVE_TASK",),
        compatibility_authority_ref=None,
        invalidation_triggers=("source_syntax_or_sequence_changed",),
        rollback_policy=("discard_uncommitted_rules_atomically",),
        external_handoff_boundary=boundary,
        maturity_status=RULESET_MATURITY,
        compatibility_status=NOT_APPLICABLE,
        production_ready=False,
        certified=False,
        ruleset_hash=f"sha256:{digest}",
        canonical_bytes=canonical_bytes,
    )


def _optional_ref(ref: GovernedRef | None) -> dict[str, str] | None:
    return None if ref is None else ref.canonical_dict()


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CategoryPolicyError(f"{field} must be a non-empty string.")
    return value.strip()


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
