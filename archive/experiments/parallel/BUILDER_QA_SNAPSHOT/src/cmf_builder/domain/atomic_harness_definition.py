from __future__ import annotations

from dataclasses import dataclass, replace
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.domain.atomicity import (
    AtomicityRatification,
    DeclaredAtomicBoundary,
    DraftHarnessModel,
)
from cmf_builder.domain.capability_ownership import CapabilityOwnershipGraph
from cmf_builder.domain.constitutional_validation import ConstitutionalValidationReport
from cmf_builder.domain.context_manifest import MinimumCompleteContextGraph
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.generated_artifacts import ArtifactManifest
from cmf_builder.domain.handoff import (
    InternalHandoff,
    InternalHandoffDecision,
    InternalHandoffDecisionAction,
    PhaseHandoffGraph,
)
from cmf_builder.domain.harness_ir import HarnessIR
from cmf_builder.domain.phase_graph import PhaseGraph
from cmf_builder.domain.responsibility_modules import ResponsibilityModuleGraph
from cmf_builder.domain.run import LifecycleState, Run
from cmf_builder.domain.skill_registry import (
    SkillNecessityDecision,
    SyntheticSkillRegistrySnapshot,
)


DEFINITION_SCHEMA_ID = "cmf-builder-atomic-harness-definition/v1"
DEFINITION_SCHEMA_VERSION = "1.0.0"
DEFINITION_RECEIPT_SCHEMA_ID = "cmf-builder-atomic-harness-definition-receipt/v1"
DEFINITION_INVALIDATION_SCHEMA_ID = "cmf-builder-atomic-harness-definition-invalidation/v1"
DEFINITION_COMPILER_ID = "cmf-builder/generic-atomic-content-harness-compiler"
DEFINITION_COMPILER_VERSION = "1.0.0"
DEFINITION_SCOPE = "ST-07.02_GENERIC_ATOMIC_CONTENT_HARNESS_ONLY"
DEFINITION_INPUT_PATH = (
    "development-capsules/ST-07.02/"
    "SYNTHETIC_ATOMIC_HARNESS_DEFINITION_INPUT.json"
)
DEFINITION_INPUT_SHA256 = (
    "99a7800b80e2258f72bf17abf49213de4f4d8403803bb34379ee1d26f12313e5"
)
TARGET_KIND = "atomic_content_harness"
PROFILE_ID = "synthetic_text_normalization_v1"
CATEGORY_ADAPTER_REF = "NOT_APPLICABLE_SYNTHETIC_PROOF"
CLASSIFICATION = (
    "builder_core_validation_only",
    "category_neutral",
    "non_certified",
    "non_production",
    "repository_owned",
    "synthetic",
    "synthetic_not_certifiable",
)
REQUIRED_SECTIONS = (
    "accepted_internal_handoff",
    "acceptance_test_contracts",
    "atomic_boundary_and_ratification",
    "authority_and_provenance",
    "capability_ownership",
    "compatibility_and_certification",
    "constitutional_precedence",
    "deterministic_artifact_set",
    "draft_harness_model",
    "harness_ir",
    "identity_and_version",
    "input_output_contract",
    "invalidation_and_history",
    "minimum_complete_context",
    "phase_graph_execution_plan",
    "responsibility_modules",
    "skill_necessity_decision",
    "skill_registry_snapshot",
    "source_lock",
    "target_and_source_profile",
)
ACCEPTANCE_TEST_DECLARATIONS = (
    "emits_exactly_one_terminal_newline",
    "invalid_UTF8_fails_closed",
    "normalizes_CRLF_and_CR_to_LF",
    "preserves_non_line_ending_UTF8_content",
    "same_input_produces_same_output_contract_result",
)
FAILURE_STOP_CONDITIONS = (
    "altered_or_hash_invalid_input",
    "authority_conflict",
    "capability_module_phase_context_or_skill_disagreement",
    "external_runtime_or_skill_injection",
    "missing_required_governed_evidence",
    "production_or_certification_claim",
    "stale_superseded_or_invalidated_input",
    "unsupported_NOT_APPLICABLE",
)
VALIDATION_REQUIREMENTS = (
    "active_current_hash_valid_upstream_lineage",
    "canonical_byte_reproduction",
    "complete_required_section_coverage",
    "cross_artifact_semantic_consistency",
    "portable_path_free_definition",
    "synthetic_nonproduction_noncertification_scope",
)
OBSERVABILITY_REQUIREMENTS = (
    "attributable_compilation_receipt",
    "deterministic_identity_and_hashes",
    "failure_context_without_partial_state",
    "lineage_and_authority_references",
    "replay_and_invalidation_state",
)
AUTHORITY_BOUNDARIES = (
    "builder_code_compiles_definition",
    "human_ratification_remains_authoritative",
    "higher_order_constitutional_authority_precedes_local_projection",
    "no_external_product_runtime_authority_absorbed",
)


class AtomicHarnessDefinitionError(Exception):
    code = "AtomicHarnessDefinitionError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class DefinitionInputInvalid(AtomicHarnessDefinitionError):
    code = "DefinitionInputInvalid"


class DefinitionLineageInvalid(AtomicHarnessDefinitionError):
    code = "DefinitionLineageInvalid"


class DefinitionAuthorityInvalid(AtomicHarnessDefinitionError):
    code = "DefinitionAuthorityInvalid"


class DefinitionScopeInvalid(AtomicHarnessDefinitionError):
    code = "DefinitionScopeInvalid"


class DefinitionInvalidatedError(AtomicHarnessDefinitionError):
    code = "DefinitionInvalidated"


@dataclass(frozen=True, slots=True)
class GovernedDefinitionSection:
    section_id: str
    applicability: str
    source_refs: tuple[str, ...]
    basis: str

    def validate(self) -> None:
        if (
            self.section_id not in REQUIRED_SECTIONS
            or self.applicability != "REQUIRED"
            or not self.source_refs
            or tuple(sorted(set(self.source_refs))) != self.source_refs
            or not self.basis.strip()
        ):
            raise DefinitionInputInvalid(
                "Every required definition section needs canonical governed evidence.",
                section_id=self.section_id,
            )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "section_id": self.section_id,
            "applicability": self.applicability,
            "source_refs": list(self.source_refs),
            "basis": self.basis,
        }


@dataclass(frozen=True, slots=True)
class AtomicHarnessDefinition:
    definition_id: str
    definition_hash: str
    schema_id: str
    schema_version: str
    compiler_id: str
    compiler_version: str
    scope: str
    harness_id: str
    harness_version: str
    run_id: str
    target_kind: str
    target_profile_ref: str
    profile_id: str
    profile_source_hash: str
    category_binding: str
    category_adapter_ref: str
    classification: tuple[str, ...]
    definition_input_hash: str
    source_lock_ref: str
    source_lock_hash: str
    boundary_ref: str
    boundary_hash: str
    ratification_ref: str
    ratification_hash: str
    model_ref: str
    model_hash: str
    ir_id: str
    ir_hash: str
    artifact_set_id: str
    artifact_manifest_id: str
    artifact_manifest_hash: str
    constitutional_report_id: str
    constitutional_report_hash: str
    capability_graph_id: str
    capability_graph_hash: str
    module_graph_id: str
    module_graph_hash: str
    phase_graph_id: str
    phase_graph_hash: str
    handoff_graph_id: str
    handoff_graph_hash: str
    accepted_handoff_id: str
    accepted_handoff_hash: str
    minimum_context_graph_id: str
    minimum_context_graph_hash: str
    skill_snapshot_id: str
    skill_snapshot_hash: str
    skill_necessity_decision_id: str
    skill_necessity_decision_hash: str
    task_id: str
    goal: str
    success_condition: str
    input_contract: str
    output_contract: str
    capability_ids: tuple[str, ...]
    module_ids: tuple[str, ...]
    phase_ids: tuple[str, ...]
    context_manifest_ids: tuple[str, ...]
    acceptance_test_declarations: tuple[str, ...]
    authority_identity: str
    authority_boundaries: tuple[str, ...]
    failure_stop_conditions: tuple[str, ...]
    validation_requirements: tuple[str, ...]
    evaluation_requirements: tuple[str, ...]
    observability_requirements: tuple[str, ...]
    workflow_declaration: str
    repair_retry_policy: str
    compatibility_status: str
    external_skill_count: int
    missing_skill_count: int
    adaptation_count: int
    experiment_count: int
    jit_capsule_count: int
    external_runtime_count: int
    dynamic_skill_discovery_allowed: bool
    execution_performed: bool
    development_capsule_generated: bool
    production_eligible: bool
    certified: bool
    synthetic_not_certifiable: bool
    sections: tuple[GovernedDefinitionSection, ...]
    lineage: tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        run: Run,
        source_lock: SourceLock,
        boundary: DeclaredAtomicBoundary,
        ratification: AtomicityRatification,
        model: DraftHarnessModel,
        ir: HarnessIR,
        manifest: ArtifactManifest,
        constitutional: ConstitutionalValidationReport,
        capability: CapabilityOwnershipGraph,
        modules: ResponsibilityModuleGraph,
        phases: PhaseGraph,
        handoff_graph: PhaseHandoffGraph,
        accepted_handoff: InternalHandoff,
        handoff_decision: InternalHandoffDecision,
        context: MinimumCompleteContextGraph,
        snapshot: SyntheticSkillRegistrySnapshot,
        necessity: SkillNecessityDecision,
        authority_identity: str,
    ) -> "AtomicHarnessDefinition":
        supplemental = run.target_profile.supplemental_proof
        if supplemental is None:
            raise DefinitionScopeInvalid("The generic proof requires synthetic profile evidence.")
        source_map: Mapping[str, tuple[str, ...]] = {
            "identity_and_version": (run.run_id, ir.ir_id),
            "target_and_source_profile": (run.target_profile.profile_id, source_lock.source_profile_ref),
            "source_lock": (source_lock.lock_id, source_lock.aggregate_hash),
            "atomic_boundary_and_ratification": (boundary.boundary_id, ratification.ratification_id),
            "draft_harness_model": (model.model_id, model.model_hash),
            "harness_ir": (ir.ir_id, ir.ir_hash),
            "deterministic_artifact_set": (manifest.artifact_set_id, manifest.manifest_hash),
            "constitutional_precedence": (constitutional.report_id, constitutional.report_hash),
            "capability_ownership": (capability.graph_id, capability.graph_hash),
            "responsibility_modules": (modules.graph_id, modules.graph_hash),
            "phase_graph_execution_plan": (phases.graph_id, phases.graph_hash),
            "accepted_internal_handoff": (accepted_handoff.handoff_id, accepted_handoff.handoff_hash),
            "minimum_complete_context": (context.graph_id, context.graph_hash),
            "skill_registry_snapshot": (snapshot.snapshot_id, snapshot.snapshot_hash),
            "skill_necessity_decision": (necessity.decision_id, necessity.decision_hash),
            "input_output_contract": (boundary.boundary_id, model.model_id),
            "acceptance_test_contracts": (ir.ir_id, phases.graph_id),
            "authority_and_provenance": (ratification.ratification_id, constitutional.report_id),
            "compatibility_and_certification": (run.target_profile.profile_id, necessity.decision_id),
            "invalidation_and_history": (run.run_id, necessity.decision_id),
        }
        sections = tuple(
            GovernedDefinitionSection(
                section_id=name,
                applicability="REQUIRED",
                source_refs=tuple(sorted(source_map[name])),
                basis="governed_upstream_evidence",
            )
            for name in REQUIRED_SECTIONS
        )
        lineage = tuple(sorted({
            run.run_id,
            source_lock.lock_id,
            source_lock.aggregate_hash,
            boundary.boundary_id,
            boundary.content_hash,
            ratification.ratification_id,
            ratification.ratification_hash,
            model.model_id,
            model.model_hash,
            ir.ir_id,
            ir.ir_hash,
            manifest.artifact_set_id,
            manifest.manifest_hash,
            constitutional.report_id,
            constitutional.report_hash,
            capability.graph_id,
            capability.graph_hash,
            modules.graph_id,
            modules.graph_hash,
            phases.graph_id,
            phases.graph_hash,
            handoff_graph.graph_id,
            handoff_graph.graph_hash,
            accepted_handoff.handoff_id,
            accepted_handoff.handoff_hash,
            handoff_decision.decision_id,
            handoff_decision.decision_hash,
            context.graph_id,
            context.graph_hash,
            snapshot.snapshot_id,
            snapshot.snapshot_hash,
            necessity.decision_id,
            necessity.decision_hash,
        }))
        candidate = cls(
            definition_id="pending",
            definition_hash="pending",
            schema_id=DEFINITION_SCHEMA_ID,
            schema_version=DEFINITION_SCHEMA_VERSION,
            compiler_id=DEFINITION_COMPILER_ID,
            compiler_version=DEFINITION_COMPILER_VERSION,
            scope=DEFINITION_SCOPE,
            harness_id=PROFILE_ID,
            harness_version="1.0.0",
            run_id=run.run_id,
            target_kind=TARGET_KIND,
            target_profile_ref=ir.target_profile_ref,
            profile_id=run.target_profile.profile_id,
            profile_source_hash=supplemental.profile_source_hash,
            category_binding="none",
            category_adapter_ref=CATEGORY_ADAPTER_REF,
            classification=CLASSIFICATION,
            definition_input_hash=f"sha256:{DEFINITION_INPUT_SHA256}",
            source_lock_ref=source_lock.lock_id,
            source_lock_hash=source_lock.aggregate_hash,
            boundary_ref=boundary.boundary_id,
            boundary_hash=boundary.content_hash,
            ratification_ref=ratification.ratification_id,
            ratification_hash=ratification.ratification_hash,
            model_ref=model.model_id,
            model_hash=model.model_hash,
            ir_id=ir.ir_id,
            ir_hash=ir.ir_hash,
            artifact_set_id=manifest.artifact_set_id,
            artifact_manifest_id=manifest.manifest_id,
            artifact_manifest_hash=manifest.manifest_hash,
            constitutional_report_id=constitutional.report_id,
            constitutional_report_hash=constitutional.report_hash,
            capability_graph_id=capability.graph_id,
            capability_graph_hash=capability.graph_hash,
            module_graph_id=modules.graph_id,
            module_graph_hash=modules.graph_hash,
            phase_graph_id=phases.graph_id,
            phase_graph_hash=phases.graph_hash,
            handoff_graph_id=handoff_graph.graph_id,
            handoff_graph_hash=handoff_graph.graph_hash,
            accepted_handoff_id=accepted_handoff.handoff_id,
            accepted_handoff_hash=accepted_handoff.handoff_hash,
            minimum_context_graph_id=context.graph_id,
            minimum_context_graph_hash=context.graph_hash,
            skill_snapshot_id=snapshot.snapshot_id,
            skill_snapshot_hash=snapshot.snapshot_hash,
            skill_necessity_decision_id=necessity.decision_id,
            skill_necessity_decision_hash=necessity.decision_hash,
            task_id="synthetic_utf8_line_ending_normalization",
            goal="compile a governed deterministic text-normalization Harness definition",
            success_condition="definition is complete deterministic portable and explicitly non-certifiable",
            input_contract="UTF-8 text bytes accepted under the governed Source Lock",
            output_contract="UTF-8 text with LF line endings and exactly one terminal newline",
            capability_ids=tuple(sorted(item.capability_id for item in necessity.capability_evidence)),
            module_ids=tuple(sorted(item.module_id for item in modules.modules)),
            phase_ids=tuple(sorted(item.phase_id for item in phases.phases)),
            context_manifest_ids=tuple(sorted(item.manifest_id for item in context.manifests)),
            acceptance_test_declarations=ACCEPTANCE_TEST_DECLARATIONS,
            authority_identity=authority_identity,
            authority_boundaries=AUTHORITY_BOUNDARIES,
            failure_stop_conditions=FAILURE_STOP_CONDITIONS,
            validation_requirements=VALIDATION_REQUIREMENTS,
            evaluation_requirements=("ST-07.04_post_compilation_validation_required",),
            observability_requirements=OBSERVABILITY_REQUIREMENTS,
            workflow_declaration="PHASE_GRAPH_PLAN_ONLY_NOT_EXECUTED",
            repair_retry_policy="typed_failure_clean_retry_new_version_on_governed_change",
            compatibility_status="synthetic_builder_core_contract_compatible_only",
            external_skill_count=necessity.external_skills_required_count,
            missing_skill_count=necessity.missing_required_skills_count,
            adaptation_count=necessity.adaptations_required_count,
            experiment_count=necessity.experiments_required_count,
            jit_capsule_count=necessity.jit_capsules_required_count,
            external_runtime_count=0,
            dynamic_skill_discovery_allowed=snapshot.dynamic_skill_discovery_allowed,
            execution_performed=False,
            development_capsule_generated=False,
            production_eligible=False,
            certified=False,
            synthetic_not_certifiable=True,
            sections=sections,
            lineage=lineage,
        )
        candidate.validate(
            run=run,
            source_lock=source_lock,
            boundary=boundary,
            ratification=ratification,
            model=model,
            ir=ir,
            manifest=manifest,
            constitutional=constitutional,
            capability=capability,
            modules=modules,
            phases=phases,
            handoff_graph=handoff_graph,
            accepted_handoff=accepted_handoff,
            handoff_decision=handoff_decision,
            context=context,
            snapshot=snapshot,
            necessity=necessity,
            verify_identity=False,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            definition_id=f"atomic-harness-definition_{digest}",
            definition_hash=f"sha256:{digest}",
        )
        result.validate(
            run=run,
            source_lock=source_lock,
            boundary=boundary,
            ratification=ratification,
            model=model,
            ir=ir,
            manifest=manifest,
            constitutional=constitutional,
            capability=capability,
            modules=modules,
            phases=phases,
            handoff_graph=handoff_graph,
            accepted_handoff=accepted_handoff,
            handoff_decision=handoff_decision,
            context=context,
            snapshot=snapshot,
            necessity=necessity,
        )
        return result

    def validate(
        self,
        *,
        run: Run,
        source_lock: SourceLock,
        boundary: DeclaredAtomicBoundary,
        ratification: AtomicityRatification,
        model: DraftHarnessModel,
        ir: HarnessIR,
        manifest: ArtifactManifest,
        constitutional: ConstitutionalValidationReport,
        capability: CapabilityOwnershipGraph,
        modules: ResponsibilityModuleGraph,
        phases: PhaseGraph,
        handoff_graph: PhaseHandoffGraph,
        accepted_handoff: InternalHandoff,
        handoff_decision: InternalHandoffDecision,
        context: MinimumCompleteContextGraph,
        snapshot: SyntheticSkillRegistrySnapshot,
        necessity: SkillNecessityDecision,
        verify_identity: bool = True,
    ) -> None:
        for section in self.sections:
            section.validate()
        supplemental = run.target_profile.supplemental_proof
        expected_sections = tuple(item.section_id for item in self.sections)
        expected_lineage = tuple(sorted({
            run.run_id, source_lock.lock_id, source_lock.aggregate_hash,
            boundary.boundary_id, boundary.content_hash,
            ratification.ratification_id, ratification.ratification_hash,
            model.model_id, model.model_hash, ir.ir_id, ir.ir_hash,
            manifest.artifact_set_id, manifest.manifest_hash,
            constitutional.report_id, constitutional.report_hash,
            capability.graph_id, capability.graph_hash,
            modules.graph_id, modules.graph_hash, phases.graph_id, phases.graph_hash,
            handoff_graph.graph_id, handoff_graph.graph_hash,
            accepted_handoff.handoff_id, accepted_handoff.handoff_hash,
            handoff_decision.decision_id, handoff_decision.decision_hash,
            context.graph_id, context.graph_hash, snapshot.snapshot_id,
            snapshot.snapshot_hash, necessity.decision_id, necessity.decision_hash,
        }))
        if supplemental is None:
            raise DefinitionScopeInvalid("Synthetic proof metadata is missing.")
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or self.schema_id != DEFINITION_SCHEMA_ID
            or self.schema_version != DEFINITION_SCHEMA_VERSION
            or self.compiler_id != DEFINITION_COMPILER_ID
            or self.compiler_version != DEFINITION_COMPILER_VERSION
            or self.scope != DEFINITION_SCOPE
            or self.harness_id != PROFILE_ID
            or self.harness_version != "1.0.0"
            or self.run_id != run.run_id
            or self.target_kind != TARGET_KIND
            or self.target_profile_ref != ir.target_profile_ref
            or self.profile_id != run.target_profile.profile_id
            or self.profile_source_hash != supplemental.profile_source_hash
            or self.category_binding != "none"
            or self.category_adapter_ref != CATEGORY_ADAPTER_REF
            or self.classification != CLASSIFICATION
            or self.definition_input_hash != f"sha256:{DEFINITION_INPUT_SHA256}"
            or self.source_lock_ref != source_lock.lock_id
            or self.source_lock_hash != source_lock.aggregate_hash
            or self.boundary_ref != boundary.boundary_id
            or self.boundary_hash != boundary.content_hash
            or self.ratification_ref != ratification.ratification_id
            or self.ratification_hash != ratification.ratification_hash
            or self.model_ref != model.model_id
            or self.model_hash != model.model_hash
            or self.ir_id != ir.ir_id
            or self.ir_hash != ir.ir_hash
            or self.artifact_set_id != manifest.artifact_set_id
            or self.artifact_manifest_id != manifest.manifest_id
            or self.artifact_manifest_hash != manifest.manifest_hash
            or self.constitutional_report_id != constitutional.report_id
            or self.constitutional_report_hash != constitutional.report_hash
            or self.capability_graph_id != capability.graph_id
            or self.capability_graph_hash != capability.graph_hash
            or self.module_graph_id != modules.graph_id
            or self.module_graph_hash != modules.graph_hash
            or self.phase_graph_id != phases.graph_id
            or self.phase_graph_hash != phases.graph_hash
            or self.handoff_graph_id != handoff_graph.graph_id
            or self.handoff_graph_hash != handoff_graph.graph_hash
            or self.accepted_handoff_id != accepted_handoff.handoff_id
            or self.accepted_handoff_hash != accepted_handoff.handoff_hash
            or handoff_decision.action is not InternalHandoffDecisionAction.ACCEPTED
            or self.minimum_context_graph_id != context.graph_id
            or self.minimum_context_graph_hash != context.graph_hash
            or self.skill_snapshot_id != snapshot.snapshot_id
            or self.skill_snapshot_hash != snapshot.snapshot_hash
            or self.skill_necessity_decision_id != necessity.decision_id
            or self.skill_necessity_decision_hash != necessity.decision_hash
            or self.capability_ids != tuple(sorted(item.capability_id for item in necessity.capability_evidence))
            or self.module_ids != tuple(sorted(item.module_id for item in modules.modules))
            or self.phase_ids != tuple(sorted(item.phase_id for item in phases.phases))
            or self.context_manifest_ids != tuple(sorted(item.manifest_id for item in context.manifests))
            or self.acceptance_test_declarations != ACCEPTANCE_TEST_DECLARATIONS
            or not self.authority_identity.strip()
            or self.authority_boundaries != AUTHORITY_BOUNDARIES
            or self.failure_stop_conditions != FAILURE_STOP_CONDITIONS
            or self.validation_requirements != VALIDATION_REQUIREMENTS
            or self.observability_requirements != OBSERVABILITY_REQUIREMENTS
            or self.workflow_declaration != "PHASE_GRAPH_PLAN_ONLY_NOT_EXECUTED"
            or self.external_skill_count
            or self.missing_skill_count
            or self.adaptation_count
            or self.experiment_count
            or self.jit_capsule_count
            or self.external_runtime_count
            or self.dynamic_skill_discovery_allowed
            or self.execution_performed
            or self.development_capsule_generated
            or self.production_eligible
            or self.certified
            or not self.synthetic_not_certifiable
            or expected_sections != REQUIRED_SECTIONS
            or len(set(expected_sections)) != len(expected_sections)
            or self.lineage != expected_lineage
        ):
            raise DefinitionLineageInvalid(
                "Atomic Harness Definition is incomplete, inconsistent, or outside synthetic authority."
            )
        if any(("\\" in value or ":/" in value.lower()) for value in self.lineage):
            raise DefinitionScopeInvalid("Definition lineage contains a machine-local path.")
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.definition_id != f"atomic-harness-definition_{digest}"
                or self.definition_hash != f"sha256:{digest}"
            ):
                raise DefinitionLineageInvalid("Definition identity is not reproducible.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            name: value
            for name, value in (
                ("schema_id", self.schema_id),
                ("schema_version", self.schema_version),
                ("compiler_id", self.compiler_id),
                ("compiler_version", self.compiler_version),
                ("scope", self.scope),
                ("harness_id", self.harness_id),
                ("harness_version", self.harness_version),
                ("run_id", self.run_id),
                ("target_kind", self.target_kind),
                ("target_profile_ref", self.target_profile_ref),
                ("profile_id", self.profile_id),
                ("profile_source_hash", self.profile_source_hash),
                ("category_binding", self.category_binding),
                ("category_adapter_ref", self.category_adapter_ref),
                ("classification", list(self.classification)),
                ("definition_input_hash", self.definition_input_hash),
                ("source_lock_ref", self.source_lock_ref),
                ("source_lock_hash", self.source_lock_hash),
                ("boundary_ref", self.boundary_ref),
                ("boundary_hash", self.boundary_hash),
                ("ratification_ref", self.ratification_ref),
                ("ratification_hash", self.ratification_hash),
                ("model_ref", self.model_ref),
                ("model_hash", self.model_hash),
                ("ir_id", self.ir_id),
                ("ir_hash", self.ir_hash),
                ("artifact_set_id", self.artifact_set_id),
                ("artifact_manifest_id", self.artifact_manifest_id),
                ("artifact_manifest_hash", self.artifact_manifest_hash),
                ("constitutional_report_id", self.constitutional_report_id),
                ("constitutional_report_hash", self.constitutional_report_hash),
                ("capability_graph_id", self.capability_graph_id),
                ("capability_graph_hash", self.capability_graph_hash),
                ("module_graph_id", self.module_graph_id),
                ("module_graph_hash", self.module_graph_hash),
                ("phase_graph_id", self.phase_graph_id),
                ("phase_graph_hash", self.phase_graph_hash),
                ("handoff_graph_id", self.handoff_graph_id),
                ("handoff_graph_hash", self.handoff_graph_hash),
                ("accepted_handoff_id", self.accepted_handoff_id),
                ("accepted_handoff_hash", self.accepted_handoff_hash),
                ("minimum_context_graph_id", self.minimum_context_graph_id),
                ("minimum_context_graph_hash", self.minimum_context_graph_hash),
                ("skill_snapshot_id", self.skill_snapshot_id),
                ("skill_snapshot_hash", self.skill_snapshot_hash),
                ("skill_necessity_decision_id", self.skill_necessity_decision_id),
                ("skill_necessity_decision_hash", self.skill_necessity_decision_hash),
                ("task_id", self.task_id),
                ("goal", self.goal),
                ("success_condition", self.success_condition),
                ("input_contract", self.input_contract),
                ("output_contract", self.output_contract),
                ("capability_ids", list(self.capability_ids)),
                ("module_ids", list(self.module_ids)),
                ("phase_ids", list(self.phase_ids)),
                ("context_manifest_ids", list(self.context_manifest_ids)),
                ("acceptance_test_declarations", list(self.acceptance_test_declarations)),
                ("authority_identity", self.authority_identity),
                ("authority_boundaries", list(self.authority_boundaries)),
                ("failure_stop_conditions", list(self.failure_stop_conditions)),
                ("validation_requirements", list(self.validation_requirements)),
                ("evaluation_requirements", list(self.evaluation_requirements)),
                ("observability_requirements", list(self.observability_requirements)),
                ("workflow_declaration", self.workflow_declaration),
                ("repair_retry_policy", self.repair_retry_policy),
                ("compatibility_status", self.compatibility_status),
                ("external_skill_count", self.external_skill_count),
                ("missing_skill_count", self.missing_skill_count),
                ("adaptation_count", self.adaptation_count),
                ("experiment_count", self.experiment_count),
                ("jit_capsule_count", self.jit_capsule_count),
                ("external_runtime_count", self.external_runtime_count),
                ("dynamic_skill_discovery_allowed", self.dynamic_skill_discovery_allowed),
                ("execution_performed", self.execution_performed),
                ("development_capsule_generated", self.development_capsule_generated),
                ("production_eligible", self.production_eligible),
                ("certified", self.certified),
                ("synthetic_not_certifiable", self.synthetic_not_certifiable),
                ("sections", [item.canonical_dict() for item in self.sections]),
                ("lineage", list(self.lineage)),
            )
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class AtomicHarnessDefinitionReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    definition_id: str
    definition_hash: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    section_count: int
    capability_count: int
    module_count: int
    phase_count: int
    context_manifest_count: int
    external_skill_count: int
    external_runtime_count: int
    synthetic_not_certifiable: bool
    initial_atomic_harness_definition_milestone: str
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        definition: AtomicHarnessDefinition,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "AtomicHarnessDefinitionReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=DEFINITION_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=definition.run_id,
            definition_id=definition.definition_id,
            definition_hash=definition.definition_hash,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            section_count=len(definition.sections),
            capability_count=len(definition.capability_ids),
            module_count=len(definition.module_ids),
            phase_count=len(definition.phase_ids),
            context_manifest_count=len(definition.context_manifest_ids),
            external_skill_count=definition.external_skill_count,
            external_runtime_count=definition.external_runtime_count,
            synthetic_not_certifiable=definition.synthetic_not_certifiable,
            initial_atomic_harness_definition_milestone="PASS",
            outcome="SYNTHETIC_ATOMIC_HARNESS_DEFINITION_COMPILED",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            receipt_id=f"atomic-harness-definition-receipt_{digest}",
            receipt_hash=f"sha256:{digest}",
        )
        result.validate(definition)
        return result

    def validate(self, definition: AtomicHarnessDefinition) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != DEFINITION_RECEIPT_SCHEMA_ID
            or self.run_id != definition.run_id
            or self.definition_id != definition.definition_id
            or self.definition_hash != definition.definition_hash
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.section_count != len(definition.sections)
            or self.capability_count != len(definition.capability_ids)
            or self.module_count != len(definition.module_ids)
            or self.phase_count != len(definition.phase_ids)
            or self.context_manifest_count != len(definition.context_manifest_ids)
            or self.external_skill_count
            or self.external_runtime_count
            or not self.synthetic_not_certifiable
            or self.initial_atomic_harness_definition_milestone != "PASS"
            or self.outcome != "SYNTHETIC_ATOMIC_HARNESS_DEFINITION_COMPILED"
            or self.receipt_id != f"atomic-harness-definition-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise DefinitionLineageInvalid("Definition receipt does not match its immutable definition.")

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "schema_id": self.schema_id,
            "command_id": self.command_id,
            "run_id": self.run_id,
            "definition_id": self.definition_id,
            "definition_hash": self.definition_hash,
            "authority_identity": self.authority_identity,
            "event_ids": list(self.event_ids),
            "stream_version": self.stream_version,
            "section_count": self.section_count,
            "capability_count": self.capability_count,
            "module_count": self.module_count,
            "phase_count": self.phase_count,
            "context_manifest_count": self.context_manifest_count,
            "external_skill_count": self.external_skill_count,
            "external_runtime_count": self.external_runtime_count,
            "synthetic_not_certifiable": self.synthetic_not_certifiable,
            "initial_atomic_harness_definition_milestone": self.initial_atomic_harness_definition_milestone,
            "outcome": self.outcome,
        })


@dataclass(frozen=True, slots=True)
class AtomicHarnessDefinitionInvalidation:
    invalidation_id: str
    invalidation_hash: str
    schema_id: str
    definition_ref: str
    necessity_decision_ref: str
    upstream_invalidation_ref: str
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        definition_ref: str,
        necessity_decision_ref: str,
        upstream_invalidation_ref: str,
        reason: str,
        authority_identity: str,
    ) -> "AtomicHarnessDefinitionInvalidation":
        if not all(value.strip() for value in (
            invalidation_id,
            definition_ref,
            necessity_decision_ref,
            upstream_invalidation_ref,
            reason,
            authority_identity,
        )):
            raise DefinitionInputInvalid("Definition invalidation evidence is incomplete.")
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            schema_id=DEFINITION_INVALIDATION_SCHEMA_ID,
            definition_ref=definition_ref,
            necessity_decision_ref=necessity_decision_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            reason=reason,
            authority_identity=authority_identity,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json({
            "invalidation_id": self.invalidation_id,
            "schema_id": self.schema_id,
            "definition_ref": self.definition_ref,
            "necessity_decision_ref": self.necessity_decision_ref,
            "upstream_invalidation_ref": self.upstream_invalidation_ref,
            "reason": self.reason,
            "authority_identity": self.authority_identity,
        })


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
