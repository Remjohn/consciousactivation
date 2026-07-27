from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.domain.context_manifest import MinimumCompleteContextGraph


SKILL_REGISTRY_INPUT_PATH = (
    "development-capsules/ST-05.01/"
    "SYNTHETIC_SKILL_REGISTRY_CONSUMPTION_INPUT.json"
)
SKILL_REGISTRY_INPUT_SHA256 = (
    "f99236ce99477995510c913ee193f45d17433049f87deb318524b79672f7f86d"
)
SKILL_REGISTRY_INPUT_SCHEMA = (
    "cmf-builder-synthetic-skill-registry-consumption-input/v1"
)
SKILL_REGISTRY_SCOPE = (
    "ST-05.01_SYNTHETIC_EMPTY_SKILL_REGISTRY_CONSUMPTION_ONLY"
)
SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID = "cmf-builder-synthetic-skill-registry-snapshot/v1"
SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION = "1.0.0"
SKILL_REGISTRY_RECEIPT_SCHEMA_ID = "cmf-builder-skill-registry-consumption-receipt/v1"
MINIMUM_CONTEXT_CONTRACT = "cmf-builder-minimum-complete-context-graph/v1@1.0.0"

REGISTRY_ID = "builder-core-synthetic-empty-skill-registry"
REGISTRY_VERSION = "1.0.0"
REGISTRY_REF = f"{REGISTRY_ID}@{REGISTRY_VERSION}"
REGISTRY_FIXTURE_PATH = "governance/fixtures/synthetic-core/empty-skill-registry.yaml"
REGISTRY_FIXTURE_SHA256 = (
    "a4a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114"
)
REGISTRY_POLICY_ID = "builder-core-empty-skill-registry-policy-v1"
REGISTRY_POLICY_VERSION = "1.0.0"
REGISTRY_POLICY_PATH = "governance/EMPTY_SKILL_REGISTRY_POLICY.yaml"
REGISTRY_POLICY_SHA256 = (
    "260df1cb40655fe4f42d264bb73f3e6bda012b9fe6bd015a1b6ae153615f985c"
)
REGISTRY_SCHEMA_PATH = "governance/schemas/empty-skill-registry.schema.json"
REGISTRY_SCHEMA_SHA256 = (
    "e76be265d96df3c902a26989fa2c08309f6964bf96e4ac17ce850684de44f1c7"
)
REGISTRY_VALIDATION_RECEIPT_PATH = (
    "governance/EMPTY_SKILL_REGISTRY_VALIDATION_RECEIPT.json"
)
REGISTRY_VALIDATION_RECEIPT_SHA256 = (
    "79164fa7418d3750ffefee116264b1ca44533c8073afb5485b84089ebd945ee1"
)
REGISTRY_VALIDATION_RECEIPT_ID = (
    "builder-core-empty-skill-registry-validation-2026-07-15"
)

CAPABILITY_IDS = (
    "deterministic_contract_validation",
    "governed_run_lifecycle",
    "governed_task_acceptance",
    "immutable_receipt_emission",
    "synthetic_target_profile_binding",
)
AUTHORITY_LANES = (
    "agent_draft_only",
    "builder_code_validation",
    "human_approval",
    "independent_evaluator_evidence",
)
MATURITY_STATES = (
    "DRAFT",
    "PROTOTYPE",
    "EVALUATED",
    "STABLE",
    "DEPRECATED",
    "REVOKED",
)
PLASTICITY_STATES = ("LOCKED", "CONTROLLED", "EXPERIMENTAL")
ALLOWED_OPERATIONS = (
    "classify_code_owned_capabilities",
    "consume_exact_registry",
    "emit_immutable_consumption_receipt",
    "validate_empty_registry",
)
PROHIBITED_OPERATIONS = (
    "compile_jit_capsule",
    "compile_recipe",
    "deprecate_skill",
    "discover_skill",
    "execute_skill",
    "promote_skill",
    "register_skill",
    "revoke_skill",
)

SKILL_NECESSITY_INPUT_PATH = (
    "development-capsules/ST-05.02/SYNTHETIC_SKILL_NECESSITY_INPUT.json"
)
SKILL_NECESSITY_INPUT_SHA256 = (
    "c940d6c5ef049bfc4ee72de3f560a5a776fc1df5ace9ffb14dfa00e07a56f25e"
)
SKILL_NECESSITY_INPUT_SCHEMA = "cmf-builder-synthetic-skill-necessity-input/v1"
SKILL_NECESSITY_SCOPE = "ST-05.02_SYNTHETIC_NO_SKILL_NECESSITY_ONLY"
SKILL_NECESSITY_DECISION_SCHEMA_ID = "cmf-builder-skill-necessity-decision/v1"
SKILL_NECESSITY_DECISION_SCHEMA_VERSION = "1.0.0"
SKILL_NECESSITY_RECEIPT_SCHEMA_ID = "cmf-builder-skill-necessity-receipt/v1"
GOVERNED_ALTERNATIVE_ORDER = (
    "deterministic_code",
    "schema_or_validator",
    "tool",
    "inline_instruction",
    "external_reference",
    "human_decision",
    "exact_canonical_reuse",
    "harness_local_adaptation",
    "adapter_composition",
    "new_canonical_skill",
)
SKILL_NECESSITY_ALLOWED_OPERATIONS = (
    "evaluate_skill_necessity",
    "emit_no_skill_decision",
    "validate_capability_gap_evidence",
)
SKILL_NECESSITY_PROHIBITED_OPERATIONS = (
    "adapt_skill",
    "design_skill",
    "discover_skill",
    "evaluate_skill",
    "execute_skill",
    "package_skill",
    "register_skill",
)


class SkillRegistryError(Exception):
    code = "SkillRegistryError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class SkillRegistryInputInvalid(SkillRegistryError):
    code = "SkillRegistryInputInvalid"


class SkillRegistryContractInvalid(SkillRegistryError):
    code = "SkillRegistryContractInvalid"


class SkillRegistryAuthorityInvalid(SkillRegistryError):
    code = "SkillRegistryAuthorityInvalid"


class SkillRegistryLineageInvalid(SkillRegistryError):
    code = "SkillRegistryLineageInvalid"


class SkillRegistryStateInvalid(SkillRegistryError):
    code = "SkillRegistryStateInvalid"


class SkillRegistryInvalidatedError(SkillRegistryError):
    code = "SkillRegistryInvalidated"


class UndeclaredSkillRequirement(SkillRegistryError):
    code = "UndeclaredSkillRequirement"


class SkillNecessityEvidenceInvalid(SkillRegistryError):
    code = "SkillNecessityEvidenceInvalid"


class SkillNecessityAuthorityInvalid(SkillRegistryError):
    code = "SkillNecessityAuthorityInvalid"


class MissingRequiredSkill(SkillRegistryError):
    code = "MissingRequiredSkill"


class SkillDesignBriefRequired(SkillRegistryError):
    code = "SkillDesignBriefRequired"


class SkillNecessityInvalidatedError(SkillRegistryError):
    code = "SkillNecessityInvalidated"


class CapabilityClassification(str, Enum):
    BUILDER_OWNED_CODE = "BUILDER_OWNED_CODE"
    EXTERNAL_SKILL_REQUIRED = "EXTERNAL_SKILL_REQUIRED"
    PROHIBITED = "PROHIBITED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SkillNecessityVerdict(str, Enum):
    BUILDER_OWNED_CODE = "BUILDER_OWNED_CODE"
    REGISTERED_REUSABLE_SKILL_REQUIRED = "REGISTERED_REUSABLE_SKILL_REQUIRED"
    ADAPTATION_OR_EXPERIMENT_REQUIRED = "ADAPTATION_OR_EXPERIMENT_REQUIRED"
    PROHIBITED = "PROHIBITED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SkillDesignBriefDisposition(str, Enum):
    NOT_APPLICABLE_NO_GAP = "NOT_APPLICABLE_NO_GAP"
    REQUIRED_FOR_GAP = "REQUIRED_FOR_GAP"
    PRESENT_AND_HUMAN_AUTHORIZED = "PRESENT_AND_HUMAN_AUTHORIZED"


@dataclass(frozen=True, slots=True)
class GovernedAlternativeAssessment:
    alternative_id: str
    order: int
    adequacy: str
    selected: bool
    evidence_refs: tuple[str, ...]

    def validate(self) -> None:
        if (
            self.alternative_id not in GOVERNED_ALTERNATIVE_ORDER
            or self.order != GOVERNED_ALTERNATIVE_ORDER.index(self.alternative_id) + 1
            or self.adequacy not in {
                "COMPLETE",
                "INADEQUATE",
                "NOT_REQUIRED_AFTER_ADEQUATE_PRIOR_ALTERNATIVE",
            }
            or not self.evidence_refs
            or any(not value.strip() for value in self.evidence_refs)
            or self.evidence_refs != tuple(sorted(set(self.evidence_refs)))
            or (self.selected and self.adequacy != "COMPLETE")
        ):
            raise SkillNecessityEvidenceInvalid(
                "A governed alternative assessment is incomplete or unordered.",
                alternative_id=self.alternative_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "alternative_id": self.alternative_id,
            "order": self.order,
            "adequacy": self.adequacy,
            "selected": self.selected,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True, slots=True)
class SkillDesignBrief:
    brief_id: str
    capability_id: str
    proposed_skill_id: str
    target_failure_evidence_refs: tuple[str, ...]
    alternatives_exhausted: tuple[str, ...]
    authority_receipt_id: str

    def validate(self) -> None:
        if (
            not all(value.strip() for value in (
                self.brief_id,
                self.capability_id,
                self.proposed_skill_id,
                self.authority_receipt_id,
            ))
            or self.capability_id not in CAPABILITY_IDS
            or not self.target_failure_evidence_refs
            or any(not item.strip() for item in self.target_failure_evidence_refs)
            or self.alternatives_exhausted != GOVERNED_ALTERNATIVE_ORDER[:-1]
        ):
            raise SkillDesignBriefRequired(
                "A skill gap requires a complete typed brief and human authority.",
                capability_id=self.capability_id,
            )


@dataclass(frozen=True, slots=True)
class CapabilityGapEvidence:
    capability_id: str
    capability_version_or_hash: str
    owning_module_id: str
    owning_phase_id: str
    required_behavior: str
    implementation_evidence_refs: tuple[str, ...]
    reliability_evidence_refs: tuple[str, ...]
    authority_boundary: str
    context_requirement_refs: tuple[str, ...]
    failure_responsibility: str
    target_failure_observed: bool
    current_owner_kind: str
    alternative_assessments: tuple[GovernedAlternativeAssessment, ...]
    verdict: SkillNecessityVerdict
    justification: str
    policy_ref: str
    validation_status: str
    registered_skill_ref: str | None = None

    def validate(
        self,
        *,
        registry_skill_ids: tuple[str, ...] = (),
        brief: SkillDesignBrief | None = None,
    ) -> None:
        for assessment in self.alternative_assessments:
            assessment.validate()
        if (
            self.capability_id not in CAPABILITY_IDS
            or not self.capability_version_or_hash.startswith("sha256:")
            or not all(value.strip() for value in (
                self.owning_module_id,
                self.owning_phase_id,
                self.required_behavior,
                self.authority_boundary,
                self.failure_responsibility,
                self.justification,
                self.policy_ref,
                self.validation_status,
            ))
            or self.validation_status != "PASS"
            or not self.implementation_evidence_refs
            or not self.reliability_evidence_refs
            or not self.context_requirement_refs
            or any(
                not value.strip()
                for value in (
                    *self.implementation_evidence_refs,
                    *self.reliability_evidence_refs,
                    *self.context_requirement_refs,
                )
            )
            or any(
                values != tuple(sorted(set(values)))
                for values in (
                    self.implementation_evidence_refs,
                    self.reliability_evidence_refs,
                    self.context_requirement_refs,
                )
            )
            or tuple(item.alternative_id for item in self.alternative_assessments)
            != GOVERNED_ALTERNATIVE_ORDER
            or sum(item.selected for item in self.alternative_assessments) != 1
        ):
            raise SkillNecessityEvidenceInvalid(
                "Capability necessity evidence is incomplete, duplicated, or unordered.",
                capability_id=self.capability_id,
            )
        selected = next(item for item in self.alternative_assessments if item.selected)
        if self.verdict is SkillNecessityVerdict.BUILDER_OWNED_CODE:
            if (
                self.target_failure_observed
                or self.current_owner_kind != "builder_code"
                or selected.alternative_id != "deterministic_code"
                or self.registered_skill_ref is not None
                or brief is not None
            ):
                raise SkillNecessityEvidenceInvalid(
                    "Builder-code satisfaction requires verified code ownership and no target failure.",
                    capability_id=self.capability_id,
                )
            return
        if self.verdict is SkillNecessityVerdict.REGISTERED_REUSABLE_SKILL_REQUIRED:
            if not self.target_failure_observed or not self.registered_skill_ref:
                raise MissingRequiredSkill(
                    "A demonstrated capability gap has no registered reusable skill.",
                    capability_id=self.capability_id,
                )
            if self.registered_skill_ref not in registry_skill_ids:
                raise UndeclaredSkillRequirement(
                    "The required reusable skill is absent from the governed registry.",
                    capability_id=self.capability_id,
                    skill_ref=self.registered_skill_ref,
                )
            return
        if self.verdict is SkillNecessityVerdict.ADAPTATION_OR_EXPERIMENT_REQUIRED:
            if brief is None:
                raise SkillDesignBriefRequired(
                    "A material adaptation or experiment requires a typed brief.",
                    capability_id=self.capability_id,
                )
            brief.validate()
            return
        if self.verdict is SkillNecessityVerdict.PROHIBITED and selected.alternative_id.endswith("skill"):
            raise SkillNecessityAuthorityInvalid(
                "A prohibited capability cannot be satisfied through a skill.",
                capability_id=self.capability_id,
            )
        if self.verdict is SkillNecessityVerdict.NOT_APPLICABLE and not self.justification.strip():
            raise SkillNecessityEvidenceInvalid(
                "NOT_APPLICABLE requires explicit justification.",
                capability_id=self.capability_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "capability_version_or_hash": self.capability_version_or_hash,
            "owning_module_id": self.owning_module_id,
            "owning_phase_id": self.owning_phase_id,
            "required_behavior": self.required_behavior,
            "implementation_evidence_refs": list(self.implementation_evidence_refs),
            "reliability_evidence_refs": list(self.reliability_evidence_refs),
            "authority_boundary": self.authority_boundary,
            "context_requirement_refs": list(self.context_requirement_refs),
            "failure_responsibility": self.failure_responsibility,
            "target_failure_observed": self.target_failure_observed,
            "current_owner_kind": self.current_owner_kind,
            "alternative_assessments": [
                item.canonical_dict() for item in self.alternative_assessments
            ],
            "verdict": self.verdict.value,
            "justification": self.justification,
            "policy_ref": self.policy_ref,
            "validation_status": self.validation_status,
            "registered_skill_ref": self.registered_skill_ref,
        }


@dataclass(frozen=True, slots=True)
class CapabilityDeclaration:
    capability_id: str
    classification: CapabilityClassification
    owner_kind: str
    owner_id: str
    authority_boundary: str
    module_refs: tuple[str, ...]
    phase_refs: tuple[str, ...]
    context_manifest_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    determinism: str
    skill_required: bool
    external_skill_required: bool

    def validate(self) -> None:
        if (
            self.capability_id not in CAPABILITY_IDS
            or self.classification is not CapabilityClassification.BUILDER_OWNED_CODE
            or self.owner_kind != "builder_code"
            or not self.owner_id.strip()
            or self.authority_boundary != "builder_code_validation"
            or not self.module_refs
            or not self.phase_refs
            or not self.context_manifest_refs
            or not self.evidence_refs
            or any(not value.strip() for value in (
                *self.module_refs,
                *self.phase_refs,
                *self.context_manifest_refs,
                *self.evidence_refs,
            ))
            or self.determinism != "deterministic"
            or self.skill_required
            or self.external_skill_required
        ):
            raise SkillRegistryContractInvalid(
                "Synthetic capability ownership must be explicit deterministic Builder code.",
                capability_id=self.capability_id,
            )
        for values in (
            self.module_refs,
            self.phase_refs,
            self.context_manifest_refs,
            self.evidence_refs,
        ):
            if values != tuple(sorted(set(values))):
                raise SkillRegistryContractInvalid(
                    "Capability evidence must be unique and canonically ordered.",
                    capability_id=self.capability_id,
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "capability_id": self.capability_id,
            "classification": self.classification.value,
            "owner_kind": self.owner_kind,
            "owner_id": self.owner_id,
            "authority_boundary": self.authority_boundary,
            "module_refs": list(self.module_refs),
            "phase_refs": list(self.phase_refs),
            "context_manifest_refs": list(self.context_manifest_refs),
            "evidence_refs": list(self.evidence_refs),
            "determinism": self.determinism,
            "skill_required": self.skill_required,
            "external_skill_required": self.external_skill_required,
        }


@dataclass(frozen=True, slots=True)
class SkillClassificationTaxonomy:
    authority_lanes: tuple[str, ...]
    maturity_states: tuple[str, ...]
    plasticity_states: tuple[str, ...]
    canonical_skills: tuple[str, ...]
    harness_local_adaptations: tuple[str, ...]
    experimental_capabilities: tuple[str, ...]
    recipes: tuple[str, ...]
    jit_capsules: tuple[str, ...]

    def validate(self) -> None:
        if (
            self.authority_lanes != AUTHORITY_LANES
            or self.maturity_states != MATURITY_STATES
            or self.plasticity_states != PLASTICITY_STATES
            or any((
                self.canonical_skills,
                self.harness_local_adaptations,
                self.experimental_capabilities,
                self.recipes,
                self.jit_capsules,
            ))
        ):
            raise SkillRegistryContractInvalid(
                "Skill taxonomy was broadened or collapsed under the synthetic policy."
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "authority_lanes": list(self.authority_lanes),
            "maturity_states": list(self.maturity_states),
            "plasticity_states": list(self.plasticity_states),
            "canonical_skills": list(self.canonical_skills),
            "harness_local_adaptations": list(self.harness_local_adaptations),
            "experimental_capabilities": list(self.experimental_capabilities),
            "recipes": list(self.recipes),
            "jit_capsules": list(self.jit_capsules),
        }


@dataclass(frozen=True, slots=True)
class SyntheticSkillRegistrySnapshot:
    snapshot_id: str
    snapshot_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    registry_id: str
    registry_version: str
    registry_ref: str
    registry_hash: str
    registry_status: str
    registry_skill_count: int
    policy_id: str
    policy_version: str
    policy_hash: str
    schema_hash: str
    validation_receipt_id: str
    validation_receipt_hash: str
    input_hash: str
    minimum_context_graph_id: str
    minimum_context_graph_hash: str
    phase_graph_id: str
    phase_graph_hash: str
    module_graph_id: str
    module_graph_hash: str
    capability_graph_id: str
    capability_graph_hash: str
    handoff_graph_id: str
    handoff_graph_hash: str
    accepted_handoff_id: str
    acceptance_decision_id: str
    ir_id: str
    ir_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    authority_identity: str
    provenance: tuple[str, ...]
    capability_classifications: tuple[CapabilityDeclaration, ...]
    taxonomy: SkillClassificationTaxonomy
    required_external_skill_count: int
    external_skills_required: bool
    dynamic_skill_discovery_allowed: bool
    undeclared_skill_use: str
    later_external_skill_effect: str
    allowed_operations: tuple[str, ...]
    prohibited_operations: tuple[str, ...]
    compatibility_status: str
    validation_status: str
    real_profile_registry_subscope: str
    production_eligible: bool
    certified: bool

    @classmethod
    def create(
        cls,
        *,
        context: MinimumCompleteContextGraph,
        authority_identity: str,
        capability_classifications: tuple[CapabilityDeclaration, ...],
        taxonomy: SkillClassificationTaxonomy,
    ) -> "SyntheticSkillRegistrySnapshot":
        candidate = cls(
            snapshot_id="pending",
            snapshot_hash="pending",
            schema_id=SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID,
            schema_version=SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION,
            scope=SKILL_REGISTRY_SCOPE,
            run_id=context.run_id,
            target_profile_ref=context.target_profile_ref,
            registry_id=REGISTRY_ID,
            registry_version=REGISTRY_VERSION,
            registry_ref=REGISTRY_REF,
            registry_hash=f"sha256:{REGISTRY_FIXTURE_SHA256}",
            registry_status="ACTIVE_SYNTHETIC_PROOF_ONLY",
            registry_skill_count=0,
            policy_id=REGISTRY_POLICY_ID,
            policy_version=REGISTRY_POLICY_VERSION,
            policy_hash=f"sha256:{REGISTRY_POLICY_SHA256}",
            schema_hash=f"sha256:{REGISTRY_SCHEMA_SHA256}",
            validation_receipt_id=REGISTRY_VALIDATION_RECEIPT_ID,
            validation_receipt_hash=f"sha256:{REGISTRY_VALIDATION_RECEIPT_SHA256}",
            input_hash=f"sha256:{SKILL_REGISTRY_INPUT_SHA256}",
            minimum_context_graph_id=context.graph_id,
            minimum_context_graph_hash=context.graph_hash,
            phase_graph_id=context.phase_graph_id,
            phase_graph_hash=context.phase_graph_hash,
            module_graph_id=context.module_graph_id,
            module_graph_hash=context.module_graph_hash,
            capability_graph_id=context.capability_graph_id,
            capability_graph_hash=context.capability_graph_hash,
            handoff_graph_id=context.handoff_graph_id,
            handoff_graph_hash=context.handoff_graph_hash,
            accepted_handoff_id=context.accepted_handoff_id,
            acceptance_decision_id=context.acceptance_decision_id,
            ir_id=context.ir_id,
            ir_hash=context.ir_hash,
            source_lock_ref=context.source_lock_ref,
            boundary_ref=context.boundary_ref,
            ratification_ref=context.ratification_ref,
            model_ref=context.model_ref,
            artifact_set_id=context.artifact_set_id,
            constitutional_report_id=context.constitutional_report_id,
            constitutional_report_hash=context.constitutional_report_hash,
            authority_identity=authority_identity,
            provenance=tuple(sorted((
                context.graph_id,
                context.graph_hash,
                REGISTRY_REF,
                f"sha256:{REGISTRY_FIXTURE_SHA256}",
                REGISTRY_POLICY_ID,
                f"sha256:{REGISTRY_POLICY_SHA256}",
                REGISTRY_VALIDATION_RECEIPT_ID,
            ))),
            capability_classifications=tuple(
                sorted(capability_classifications, key=lambda item: item.capability_id)
            ),
            taxonomy=taxonomy,
            required_external_skill_count=0,
            external_skills_required=False,
            dynamic_skill_discovery_allowed=False,
            undeclared_skill_use="FAIL_CLOSED",
            later_external_skill_effect="NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED",
            allowed_operations=ALLOWED_OPERATIONS,
            prohibited_operations=PROHIBITED_OPERATIONS,
            compatibility_status="COMPATIBLE_SYNTHETIC_PROOF_ONLY",
            validation_status="PASS",
            real_profile_registry_subscope="DEFERRED_BLOCKED_BY_EXISTING_GATES",
            production_eligible=False,
            certified=False,
        )
        candidate.validate(context, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            snapshot_id=f"synthetic-skill-registry-snapshot_{digest}",
            snapshot_hash=f"sha256:{digest}",
        )
        result.validate(context)
        return result

    @property
    def capability_ids(self) -> tuple[str, ...]:
        return tuple(item.capability_id for item in self.capability_classifications)

    def validate(
        self,
        context: MinimumCompleteContextGraph,
        *,
        verify_identity: bool = True,
    ) -> None:
        for declaration in self.capability_classifications:
            declaration.validate()
        self.taxonomy.validate()
        if (
            self.schema_id != SKILL_REGISTRY_SNAPSHOT_SCHEMA_ID
            or self.schema_version != SKILL_REGISTRY_SNAPSHOT_SCHEMA_VERSION
            or self.scope != SKILL_REGISTRY_SCOPE
            or self.run_id != context.run_id
            or self.target_profile_ref != context.target_profile_ref
            or self.registry_id != REGISTRY_ID
            or self.registry_version != REGISTRY_VERSION
            or self.registry_ref != REGISTRY_REF
            or self.registry_hash != f"sha256:{REGISTRY_FIXTURE_SHA256}"
            or self.registry_status != "ACTIVE_SYNTHETIC_PROOF_ONLY"
            or self.registry_skill_count != 0
            or self.policy_id != REGISTRY_POLICY_ID
            or self.policy_version != REGISTRY_POLICY_VERSION
            or self.policy_hash != f"sha256:{REGISTRY_POLICY_SHA256}"
            or self.schema_hash != f"sha256:{REGISTRY_SCHEMA_SHA256}"
            or self.validation_receipt_id != REGISTRY_VALIDATION_RECEIPT_ID
            or self.validation_receipt_hash != f"sha256:{REGISTRY_VALIDATION_RECEIPT_SHA256}"
            or self.input_hash != f"sha256:{SKILL_REGISTRY_INPUT_SHA256}"
            or self.minimum_context_graph_id != context.graph_id
            or self.minimum_context_graph_hash != context.graph_hash
            or self.phase_graph_id != context.phase_graph_id
            or self.phase_graph_hash != context.phase_graph_hash
            or self.module_graph_id != context.module_graph_id
            or self.module_graph_hash != context.module_graph_hash
            or self.capability_graph_id != context.capability_graph_id
            or self.capability_graph_hash != context.capability_graph_hash
            or self.handoff_graph_id != context.handoff_graph_id
            or self.handoff_graph_hash != context.handoff_graph_hash
            or self.accepted_handoff_id != context.accepted_handoff_id
            or self.acceptance_decision_id != context.acceptance_decision_id
            or self.ir_id != context.ir_id
            or self.ir_hash != context.ir_hash
            or self.source_lock_ref != context.source_lock_ref
            or self.boundary_ref != context.boundary_ref
            or self.ratification_ref != context.ratification_ref
            or self.model_ref != context.model_ref
            or self.artifact_set_id != context.artifact_set_id
            or self.constitutional_report_id != context.constitutional_report_id
            or self.constitutional_report_hash != context.constitutional_report_hash
            or not self.authority_identity.strip()
            or self.capability_ids != CAPABILITY_IDS
            or self.required_external_skill_count != 0
            or self.external_skills_required
            or self.dynamic_skill_discovery_allowed
            or self.undeclared_skill_use != "FAIL_CLOSED"
            or self.later_external_skill_effect != "NEW_IMMUTABLE_HARNESS_VERSION_REQUIRED"
            or self.allowed_operations != ALLOWED_OPERATIONS
            or self.prohibited_operations != PROHIBITED_OPERATIONS
            or self.compatibility_status != "COMPATIBLE_SYNTHETIC_PROOF_ONLY"
            or self.validation_status != "PASS"
            or self.real_profile_registry_subscope != "DEFERRED_BLOCKED_BY_EXISTING_GATES"
            or self.production_eligible
            or self.certified
        ):
            raise SkillRegistryLineageInvalid(
                "Synthetic skill-registry snapshot identity, zero-skill state, or lineage is invalid."
            )
        manifest_ids = {item.manifest_id for item in context.manifests}
        module_ids = {item.module_ref for item in context.manifests}
        phase_ids = {item.phase_ref for item in context.manifests}
        for declaration in self.capability_classifications:
            if (
                not set(declaration.context_manifest_refs) <= manifest_ids
                or not set(declaration.module_refs) <= module_ids
                or not set(declaration.phase_refs) <= phase_ids
            ):
                raise SkillRegistryLineageInvalid(
                    "Capability classification references context outside the active graph.",
                    capability_id=declaration.capability_id,
                )
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.snapshot_id != f"synthetic-skill-registry-snapshot_{digest}"
                or self.snapshot_hash != f"sha256:{digest}"
            ):
                raise SkillRegistryContractInvalid("Skill snapshot identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "registry_id": self.registry_id,
            "registry_version": self.registry_version,
            "registry_ref": self.registry_ref,
            "registry_hash": self.registry_hash,
            "registry_status": self.registry_status,
            "registry_skill_count": self.registry_skill_count,
            "policy_id": self.policy_id,
            "policy_version": self.policy_version,
            "policy_hash": self.policy_hash,
            "schema_hash": self.schema_hash,
            "validation_receipt_id": self.validation_receipt_id,
            "validation_receipt_hash": self.validation_receipt_hash,
            "input_hash": self.input_hash,
            "minimum_context_graph_id": self.minimum_context_graph_id,
            "minimum_context_graph_hash": self.minimum_context_graph_hash,
            "phase_graph_id": self.phase_graph_id,
            "phase_graph_hash": self.phase_graph_hash,
            "module_graph_id": self.module_graph_id,
            "module_graph_hash": self.module_graph_hash,
            "capability_graph_id": self.capability_graph_id,
            "capability_graph_hash": self.capability_graph_hash,
            "handoff_graph_id": self.handoff_graph_id,
            "handoff_graph_hash": self.handoff_graph_hash,
            "accepted_handoff_id": self.accepted_handoff_id,
            "acceptance_decision_id": self.acceptance_decision_id,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "authority_identity": self.authority_identity,
            "provenance": list(self.provenance),
            "capability_classifications": [
                item.canonical_dict() for item in self.capability_classifications
            ],
            "taxonomy": self.taxonomy.canonical_dict(),
            "required_external_skill_count": self.required_external_skill_count,
            "external_skills_required": self.external_skills_required,
            "dynamic_skill_discovery_allowed": self.dynamic_skill_discovery_allowed,
            "undeclared_skill_use": self.undeclared_skill_use,
            "later_external_skill_effect": self.later_external_skill_effect,
            "allowed_operations": list(self.allowed_operations),
            "prohibited_operations": list(self.prohibited_operations),
            "compatibility_status": self.compatibility_status,
            "validation_status": self.validation_status,
            "real_profile_registry_subscope": self.real_profile_registry_subscope,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class SkillRegistryConsumptionReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    snapshot_id: str
    snapshot_hash: str
    registry_ref: str
    registry_hash: str
    policy_hash: str
    minimum_context_graph_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    capability_count: int
    registered_skill_count: int
    required_external_skill_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        snapshot: SyntheticSkillRegistrySnapshot,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "SkillRegistryConsumptionReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=SKILL_REGISTRY_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=snapshot.run_id,
            snapshot_id=snapshot.snapshot_id,
            snapshot_hash=snapshot.snapshot_hash,
            registry_ref=snapshot.registry_ref,
            registry_hash=snapshot.registry_hash,
            policy_hash=snapshot.policy_hash,
            minimum_context_graph_id=snapshot.minimum_context_graph_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            capability_count=len(snapshot.capability_classifications),
            registered_skill_count=snapshot.registry_skill_count,
            required_external_skill_count=snapshot.required_external_skill_count,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            receipt_id=f"skill-registry-consumption-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )

    def validate(self, snapshot: SyntheticSkillRegistrySnapshot) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != SKILL_REGISTRY_RECEIPT_SCHEMA_ID
            or self.run_id != snapshot.run_id
            or self.snapshot_id != snapshot.snapshot_id
            or self.snapshot_hash != snapshot.snapshot_hash
            or self.registry_ref != snapshot.registry_ref
            or self.registry_hash != snapshot.registry_hash
            or self.policy_hash != snapshot.policy_hash
            or self.minimum_context_graph_id != snapshot.minimum_context_graph_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.capability_count != 5
            or self.registered_skill_count != 0
            or self.required_external_skill_count != 0
            or self.outcome != "PASS"
            or self.receipt_id != f"skill-registry-consumption-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise SkillRegistryStateInvalid(
                "Skill-registry consumption receipt does not match its snapshot."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "schema_id": self.schema_id,
            "command_id": self.command_id,
            "run_id": self.run_id,
            "snapshot_id": self.snapshot_id,
            "snapshot_hash": self.snapshot_hash,
            "registry_ref": self.registry_ref,
            "registry_hash": self.registry_hash,
            "policy_hash": self.policy_hash,
            "minimum_context_graph_id": self.minimum_context_graph_id,
            "authority_identity": self.authority_identity,
            "event_ids": list(self.event_ids),
            "stream_version": self.stream_version,
            "capability_count": self.capability_count,
            "registered_skill_count": self.registered_skill_count,
            "required_external_skill_count": self.required_external_skill_count,
            "outcome": self.outcome,
        })


@dataclass(frozen=True, slots=True)
class SkillRegistrySnapshotInvalidation:
    invalidation_id: str
    invalidation_hash: str
    snapshot_ref: str
    minimum_context_ref: str
    upstream_invalidation_ref: str
    affected_capability_ids: tuple[str, ...]
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        snapshot_ref: str,
        minimum_context_ref: str,
        upstream_invalidation_ref: str,
        affected_capability_ids: tuple[str, ...],
        reason: str,
        authority_identity: str,
    ) -> "SkillRegistrySnapshotInvalidation":
        if affected_capability_ids != CAPABILITY_IDS:
            raise SkillRegistryStateInvalid(
                "Snapshot invalidation must cover all five classified capabilities."
            )
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            snapshot_ref=snapshot_ref,
            minimum_context_ref=minimum_context_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            affected_capability_ids=affected_capability_ids,
            reason=reason,
            authority_identity=authority_identity,
        )
        if any(not value.strip() for value in (
            invalidation_id,
            snapshot_ref,
            minimum_context_ref,
            upstream_invalidation_ref,
            reason,
            authority_identity,
        )):
            raise SkillRegistryStateInvalid("Skill snapshot invalidation identity is incomplete.")
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "invalidation_id": self.invalidation_id,
            "snapshot_ref": self.snapshot_ref,
            "minimum_context_ref": self.minimum_context_ref,
            "upstream_invalidation_ref": self.upstream_invalidation_ref,
            "affected_capability_ids": list(self.affected_capability_ids),
            "reason": self.reason,
            "authority_identity": self.authority_identity,
        })


@dataclass(frozen=True, slots=True)
class SkillNecessityDecision:
    decision_id: str
    decision_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    snapshot_id: str
    snapshot_hash: str
    registry_ref: str
    registry_hash: str
    policy_id: str
    policy_hash: str
    necessity_input_hash: str
    minimum_context_graph_id: str
    minimum_context_graph_hash: str
    capability_graph_id: str
    capability_graph_hash: str
    module_graph_id: str
    module_graph_hash: str
    phase_graph_id: str
    phase_graph_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    ir_id: str
    ir_hash: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    accepted_handoff_id: str
    authority_identity: str
    provenance: tuple[str, ...]
    capability_evidence: tuple[CapabilityGapEvidence, ...]
    outcome: str
    external_skills_required_count: int
    missing_required_skills_count: int
    adaptations_required_count: int
    experiments_required_count: int
    jit_capsules_required_count: int
    skill_execution_required: bool
    production_skill_certification: bool
    brief_disposition: SkillDesignBriefDisposition
    skill_design_brief_count: int
    production_eligible: bool
    certified: bool

    @classmethod
    def create(
        cls,
        *,
        snapshot: SyntheticSkillRegistrySnapshot,
        context: MinimumCompleteContextGraph,
        authority_identity: str,
        capability_evidence: tuple[CapabilityGapEvidence, ...],
    ) -> "SkillNecessityDecision":
        candidate = cls(
            decision_id="pending",
            decision_hash="pending",
            schema_id=SKILL_NECESSITY_DECISION_SCHEMA_ID,
            schema_version=SKILL_NECESSITY_DECISION_SCHEMA_VERSION,
            scope=SKILL_NECESSITY_SCOPE,
            run_id=snapshot.run_id,
            target_profile_ref=snapshot.target_profile_ref,
            snapshot_id=snapshot.snapshot_id,
            snapshot_hash=snapshot.snapshot_hash,
            registry_ref=snapshot.registry_ref,
            registry_hash=snapshot.registry_hash,
            policy_id=snapshot.policy_id,
            policy_hash=snapshot.policy_hash,
            necessity_input_hash=f"sha256:{SKILL_NECESSITY_INPUT_SHA256}",
            minimum_context_graph_id=context.graph_id,
            minimum_context_graph_hash=context.graph_hash,
            capability_graph_id=context.capability_graph_id,
            capability_graph_hash=context.capability_graph_hash,
            module_graph_id=context.module_graph_id,
            module_graph_hash=context.module_graph_hash,
            phase_graph_id=context.phase_graph_id,
            phase_graph_hash=context.phase_graph_hash,
            source_lock_ref=context.source_lock_ref,
            boundary_ref=context.boundary_ref,
            ratification_ref=context.ratification_ref,
            model_ref=context.model_ref,
            ir_id=context.ir_id,
            ir_hash=context.ir_hash,
            artifact_set_id=context.artifact_set_id,
            constitutional_report_id=context.constitutional_report_id,
            constitutional_report_hash=context.constitutional_report_hash,
            accepted_handoff_id=context.accepted_handoff_id,
            authority_identity=authority_identity,
            provenance=tuple(sorted((
                snapshot.snapshot_id,
                snapshot.snapshot_hash,
                snapshot.registry_ref,
                snapshot.registry_hash,
                snapshot.policy_id,
                snapshot.policy_hash,
                context.graph_id,
                context.graph_hash,
            ))),
            capability_evidence=tuple(
                sorted(capability_evidence, key=lambda item: item.capability_id)
            ),
            outcome="NO_NEW_SKILL_REQUIRED",
            external_skills_required_count=0,
            missing_required_skills_count=0,
            adaptations_required_count=0,
            experiments_required_count=0,
            jit_capsules_required_count=0,
            skill_execution_required=False,
            production_skill_certification=False,
            brief_disposition=SkillDesignBriefDisposition.NOT_APPLICABLE_NO_GAP,
            skill_design_brief_count=0,
            production_eligible=False,
            certified=False,
        )
        candidate.validate(snapshot, context, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            decision_id=f"skill-necessity-decision_{digest}",
            decision_hash=f"sha256:{digest}",
        )
        result.validate(snapshot, context)
        return result

    @property
    def capability_ids(self) -> tuple[str, ...]:
        return tuple(item.capability_id for item in self.capability_evidence)

    @property
    def alternative_assessment_count(self) -> int:
        return sum(len(item.alternative_assessments) for item in self.capability_evidence)

    @property
    def target_failure_count(self) -> int:
        return sum(item.target_failure_observed for item in self.capability_evidence)

    def validate(
        self,
        snapshot: SyntheticSkillRegistrySnapshot,
        context: MinimumCompleteContextGraph,
        *,
        verify_identity: bool = True,
    ) -> None:
        for evidence in self.capability_evidence:
            evidence.validate(registry_skill_ids=())
        declarations = {
            item.capability_id: item
            for item in snapshot.capability_classifications
        }
        for evidence in self.capability_evidence:
            declaration = declarations.get(evidence.capability_id)
            if (
                declaration is None
                or evidence.owning_module_id not in declaration.module_refs
                or evidence.owning_phase_id not in declaration.phase_refs
                or not set(evidence.context_requirement_refs)
                <= set(declaration.context_manifest_refs)
                or declaration.owner_id not in evidence.implementation_evidence_refs
            ):
                raise SkillNecessityEvidenceInvalid(
                    "Capability necessity evidence escapes its governed ownership or context lineage.",
                    capability_id=evidence.capability_id,
                )
        expected_provenance = tuple(sorted((
            snapshot.snapshot_id,
            snapshot.snapshot_hash,
            snapshot.registry_ref,
            snapshot.registry_hash,
            snapshot.policy_id,
            snapshot.policy_hash,
            context.graph_id,
            context.graph_hash,
        )))
        if (
            self.schema_id != SKILL_NECESSITY_DECISION_SCHEMA_ID
            or self.schema_version != SKILL_NECESSITY_DECISION_SCHEMA_VERSION
            or self.scope != SKILL_NECESSITY_SCOPE
            or self.run_id != snapshot.run_id
            or self.target_profile_ref != snapshot.target_profile_ref
            or self.snapshot_id != snapshot.snapshot_id
            or self.snapshot_hash != snapshot.snapshot_hash
            or self.registry_ref != snapshot.registry_ref
            or self.registry_hash != snapshot.registry_hash
            or self.policy_id != snapshot.policy_id
            or self.policy_hash != snapshot.policy_hash
            or self.necessity_input_hash != f"sha256:{SKILL_NECESSITY_INPUT_SHA256}"
            or self.minimum_context_graph_id != context.graph_id
            or self.minimum_context_graph_hash != context.graph_hash
            or self.capability_graph_id != context.capability_graph_id
            or self.capability_graph_hash != context.capability_graph_hash
            or self.module_graph_id != context.module_graph_id
            or self.module_graph_hash != context.module_graph_hash
            or self.phase_graph_id != context.phase_graph_id
            or self.phase_graph_hash != context.phase_graph_hash
            or self.source_lock_ref != context.source_lock_ref
            or self.boundary_ref != context.boundary_ref
            or self.ratification_ref != context.ratification_ref
            or self.model_ref != context.model_ref
            or self.ir_id != context.ir_id
            or self.ir_hash != context.ir_hash
            or self.artifact_set_id != context.artifact_set_id
            or self.constitutional_report_id != context.constitutional_report_id
            or self.constitutional_report_hash != context.constitutional_report_hash
            or self.accepted_handoff_id != context.accepted_handoff_id
            or not self.authority_identity.strip()
            or self.provenance != expected_provenance
            or self.capability_ids != CAPABILITY_IDS
            or len(set(self.capability_ids)) != len(self.capability_ids)
            or any(
                item.verdict is not SkillNecessityVerdict.BUILDER_OWNED_CODE
                for item in self.capability_evidence
            )
            or self.outcome != "NO_NEW_SKILL_REQUIRED"
            or any((
                self.external_skills_required_count,
                self.missing_required_skills_count,
                self.adaptations_required_count,
                self.experiments_required_count,
                self.jit_capsules_required_count,
                self.skill_design_brief_count,
            ))
            or self.skill_execution_required
            or self.production_skill_certification
            or self.brief_disposition
            is not SkillDesignBriefDisposition.NOT_APPLICABLE_NO_GAP
            or self.production_eligible
            or self.certified
        ):
            raise SkillNecessityEvidenceInvalid(
                "The synthetic no-skill conclusion is unsupported, incomplete, or broadened."
            )
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.decision_id != f"skill-necessity-decision_{digest}"
                or self.decision_hash != f"sha256:{digest}"
            ):
                raise SkillNecessityEvidenceInvalid(
                    "Skill necessity decision identity is not reproducible."
                )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "snapshot_id": self.snapshot_id,
            "snapshot_hash": self.snapshot_hash,
            "registry_ref": self.registry_ref,
            "registry_hash": self.registry_hash,
            "policy_id": self.policy_id,
            "policy_hash": self.policy_hash,
            "necessity_input_hash": self.necessity_input_hash,
            "minimum_context_graph_id": self.minimum_context_graph_id,
            "minimum_context_graph_hash": self.minimum_context_graph_hash,
            "capability_graph_id": self.capability_graph_id,
            "capability_graph_hash": self.capability_graph_hash,
            "module_graph_id": self.module_graph_id,
            "module_graph_hash": self.module_graph_hash,
            "phase_graph_id": self.phase_graph_id,
            "phase_graph_hash": self.phase_graph_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "accepted_handoff_id": self.accepted_handoff_id,
            "authority_identity": self.authority_identity,
            "provenance": list(self.provenance),
            "capability_evidence": [
                item.canonical_dict() for item in self.capability_evidence
            ],
            "outcome": self.outcome,
            "external_skills_required_count": self.external_skills_required_count,
            "missing_required_skills_count": self.missing_required_skills_count,
            "adaptations_required_count": self.adaptations_required_count,
            "experiments_required_count": self.experiments_required_count,
            "jit_capsules_required_count": self.jit_capsules_required_count,
            "skill_execution_required": self.skill_execution_required,
            "production_skill_certification": self.production_skill_certification,
            "brief_disposition": self.brief_disposition.value,
            "skill_design_brief_count": self.skill_design_brief_count,
            "production_eligible": self.production_eligible,
            "certified": self.certified,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class SkillNecessityReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    decision_id: str
    decision_hash: str
    snapshot_id: str
    snapshot_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    capability_count: int
    alternative_assessment_count: int
    external_skills_required_count: int
    adaptations_required_count: int
    experiments_required_count: int
    jit_capsules_required_count: int
    brief_disposition: SkillDesignBriefDisposition
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        decision: SkillNecessityDecision,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "SkillNecessityReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=SKILL_NECESSITY_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=decision.run_id,
            decision_id=decision.decision_id,
            decision_hash=decision.decision_hash,
            snapshot_id=decision.snapshot_id,
            snapshot_hash=decision.snapshot_hash,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            capability_count=len(decision.capability_evidence),
            alternative_assessment_count=decision.alternative_assessment_count,
            external_skills_required_count=decision.external_skills_required_count,
            adaptations_required_count=decision.adaptations_required_count,
            experiments_required_count=decision.experiments_required_count,
            jit_capsules_required_count=decision.jit_capsules_required_count,
            brief_disposition=decision.brief_disposition,
            outcome=decision.outcome,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(
            candidate,
            receipt_id=f"skill-necessity-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )

    def validate(self, decision: SkillNecessityDecision) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != SKILL_NECESSITY_RECEIPT_SCHEMA_ID
            or self.run_id != decision.run_id
            or self.decision_id != decision.decision_id
            or self.decision_hash != decision.decision_hash
            or self.snapshot_id != decision.snapshot_id
            or self.snapshot_hash != decision.snapshot_hash
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.capability_count != len(decision.capability_evidence)
            or self.alternative_assessment_count != decision.alternative_assessment_count
            or self.external_skills_required_count != 0
            or self.adaptations_required_count != 0
            or self.experiments_required_count != 0
            or self.jit_capsules_required_count != 0
            or self.brief_disposition
            is not SkillDesignBriefDisposition.NOT_APPLICABLE_NO_GAP
            or self.outcome != "NO_NEW_SKILL_REQUIRED"
            or self.receipt_id != f"skill-necessity-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise SkillNecessityEvidenceInvalid(
                "Skill necessity receipt does not match its immutable decision."
            )

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "schema_id": self.schema_id,
            "command_id": self.command_id,
            "run_id": self.run_id,
            "decision_id": self.decision_id,
            "decision_hash": self.decision_hash,
            "snapshot_id": self.snapshot_id,
            "snapshot_hash": self.snapshot_hash,
            "authority_identity": self.authority_identity,
            "event_ids": list(self.event_ids),
            "stream_version": self.stream_version,
            "capability_count": self.capability_count,
            "alternative_assessment_count": self.alternative_assessment_count,
            "external_skills_required_count": self.external_skills_required_count,
            "adaptations_required_count": self.adaptations_required_count,
            "experiments_required_count": self.experiments_required_count,
            "jit_capsules_required_count": self.jit_capsules_required_count,
            "brief_disposition": self.brief_disposition.value,
            "outcome": self.outcome,
        })


@dataclass(frozen=True, slots=True)
class SkillNecessityInvalidation:
    invalidation_id: str
    invalidation_hash: str
    decision_ref: str
    snapshot_ref: str
    upstream_invalidation_ref: str
    affected_capability_ids: tuple[str, ...]
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        decision_ref: str,
        snapshot_ref: str,
        upstream_invalidation_ref: str,
        affected_capability_ids: tuple[str, ...],
        reason: str,
        authority_identity: str,
    ) -> "SkillNecessityInvalidation":
        if affected_capability_ids != CAPABILITY_IDS:
            raise SkillNecessityEvidenceInvalid(
                "Necessity invalidation must cover the complete capability decision."
            )
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            decision_ref=decision_ref,
            snapshot_ref=snapshot_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            affected_capability_ids=affected_capability_ids,
            reason=reason,
            authority_identity=authority_identity,
        )
        if any(not value.strip() for value in (
            invalidation_id,
            decision_ref,
            snapshot_ref,
            upstream_invalidation_ref,
            reason,
            authority_identity,
        )):
            raise SkillNecessityEvidenceInvalid(
                "Skill necessity invalidation identity is incomplete."
            )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "invalidation_id": self.invalidation_id,
            "decision_ref": self.decision_ref,
            "snapshot_ref": self.snapshot_ref,
            "upstream_invalidation_ref": self.upstream_invalidation_ref,
            "affected_capability_ids": list(self.affected_capability_ids),
            "reason": self.reason,
            "authority_identity": self.authority_identity,
        })


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
