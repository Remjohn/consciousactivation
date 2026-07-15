from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Mapping, Protocol

from cmf_builder.domain.run import Run, RunEvent
from cmf_builder.domain.target_profile import TargetProfile

if TYPE_CHECKING:
    from cmf_builder.application.checkpoints import Checkpoint
    from cmf_builder.domain.atomicity import (
        AtomicityDecision,
        AtomicityDecisionReceipt,
        AtomicityRatification,
        BoundaryInvalidation,
        DeclaredAtomicBoundary,
        DeclaredBoundaryInput,
        DraftHarnessModel,
    )
    from cmf_builder.domain.evidence_workspace import SourceLock, SourceProfile
    from cmf_builder.domain.harness_ir import (
        HarnessIR,
        HarnessIRCompilationReceipt,
        HarnessIRInvalidation,
    )
    from cmf_builder.domain.generated_artifacts import (
        ArtifactDriftReport,
        ArtifactManifest,
        ArtifactSetCompilationReceipt,
        ArtifactSetInvalidation,
        GeneratedArtifact,
    )
    from cmf_builder.domain.constitutional_validation import (
        ConstitutionalPrecedencePolicy,
        ConstitutionalValidationInvalidation,
        ConstitutionalValidationReceipt,
        ConstitutionalValidationReport,
    )
    from cmf_builder.domain.capability_ownership import (
        CapabilityOwnershipGraph,
        CapabilityOwnershipInvalidation,
        CapabilityOwnershipReceipt,
    )
    from cmf_builder.domain.responsibility_modules import (
        ResponsibilityModuleGraph,
        ResponsibilityModuleInvalidation,
        ResponsibilityModuleReceipt,
    )
    from cmf_builder.domain.phase_graph import (
        PhaseGraph,
        PhaseGraphInvalidation,
        PhaseGraphReceipt,
    )
    from cmf_builder.domain.handoff import (
        InternalHandoff,
        InternalHandoffDecision,
        InternalHandoffReceipt,
        PhaseHandoffGraph,
        PhaseHandoffInvalidation,
        PhaseHandoffReceipt,
    )
    from cmf_builder.domain.context_manifest import (
        ContextCompilationReceipt,
        ContextGraphInvalidation,
        MinimumCompleteContextGraph,
    )
    from cmf_builder.domain.skill_registry import (
        SkillNecessityDecision,
        SkillNecessityInvalidation,
        SkillNecessityReceipt,
        SkillRegistryConsumptionReceipt,
        SkillRegistrySnapshotInvalidation,
        SyntheticSkillRegistrySnapshot,
    )
    from cmf_builder.domain.atomic_harness_definition import (
        AtomicHarnessDefinition,
        AtomicHarnessDefinitionInvalidation,
        AtomicHarnessDefinitionReceipt,
    )


class PersistenceContractError(Exception):
    code = "PersistenceContractError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class ConcurrencyConflict(PersistenceContractError):
    code = "ConcurrencyConflict"


class IdempotencyPayloadMismatch(PersistenceContractError):
    code = "IdempotencyPayloadMismatch"


class AtomicCommitFailed(PersistenceContractError):
    code = "AtomicCommitFailed"


@dataclass(frozen=True, slots=True)
class CommandRecord:
    payload_hash: str
    result: object


@dataclass(frozen=True, slots=True)
class Observation:
    event_name: str
    run_id: str
    story_id: str
    artifact_identity: str
    authority_identity: str
    version: str
    provenance: str
    outcome: str
    failure_context: Mapping[str, object]
    correlation_id: str
    causation_id: str
    command_id: str
    target_id: str
    category_id: str
    profile_id: str
    stream_version: int
    source_profile_id: str = "unassigned"
    source_profile_version: str = "unassigned"
    source_profile_hash: str = "unassigned"
    target_candidate: str = "unassigned"
    source_lock_id: str = "unassigned"
    declared_input_hash: str = "unassigned"
    boundary_id: str = "unassigned"
    boundary_version: str = "unassigned"
    boundary_status: str = "unassigned"
    selected_candidate: str = "unassigned"
    model_id: str = "unassigned"
    model_hash: str = "unassigned"
    model_status: str = "unassigned"
    decision_receipt_id: str = "unassigned"
    decision_receipt_hash: str = "unassigned"
    decision_action: str = "unassigned"
    hg_003: str = "unassigned"
    invalidated_artifact_ids: tuple[str, ...] = ()
    harness_ir_id: str = "unassigned"
    harness_ir_hash: str = "unassigned"
    harness_ir_schema_id: str = "unassigned"
    harness_ir_schema_version: str = "unassigned"
    harness_ir_revision: int = 0
    harness_ir_status: str = "unassigned"
    harness_ir_compatibility: str = "unassigned"
    activative_lineage_disposition: str = "unassigned"
    dependency_impact_refs: tuple[str, ...] = ()
    artifact_set_id: str = "unassigned"
    artifact_manifest_id: str = "unassigned"
    artifact_manifest_hash: str = "unassigned"
    artifact_compiler_id: str = "unassigned"
    artifact_compiler_version: str = "unassigned"
    artifact_config_hash: str = "unassigned"
    artifact_generation_timestamp: str = "unassigned"
    artifact_count: int = 0
    artifact_total_bytes: int = 0
    artifact_dependency_selectors: tuple[str, ...] = ()
    reproducibility_disposition: str = "unassigned"
    drift_disposition: str = "unassigned"
    quarantine_disposition: str = "unassigned"
    nondeterminism_disposition: str = "unassigned"
    constitutional_policy_path: str = "unassigned"
    constitutional_policy_hash: str = "unassigned"
    constitution_hash: str = "unassigned"
    builder_prd_amendment_hash: str = "unassigned"
    constitutional_report_id: str = "unassigned"
    constitutional_report_hash: str = "unassigned"
    constitutional_receipt_id: str = "unassigned"
    constitutional_receipt_hash: str = "unassigned"
    constitutional_finding_codes: tuple[str, ...] = ()
    constitutional_artifact_paths: tuple[str, ...] = ()
    constitutional_ir_node_paths: tuple[str, ...] = ()
    constitutional_coverage_count: int = 0
    constitutional_precedence_disposition: str = "unassigned"
    constitutional_invalidation_ref: str = "unassigned"
    capability_graph_id: str = "unassigned"
    capability_graph_hash: str = "unassigned"
    capability_receipt_id: str = "unassigned"
    capability_receipt_hash: str = "unassigned"
    capability_count: int = 0
    capability_owner_kind_counts: tuple[tuple[str, int], ...] = ()
    capability_reliability_coverage_count: int = 0
    capability_cost_coverage_count: int = 0
    capability_invalidation_ref: str = "unassigned"
    module_graph_id: str = "unassigned"
    module_graph_hash: str = "unassigned"
    module_receipt_id: str = "unassigned"
    module_receipt_hash: str = "unassigned"
    module_count: int = 0
    module_capability_coverage_count: int = 0
    module_dependency_count: int = 0
    module_contract_coverage_count: int = 0
    module_test_seam_coverage_count: int = 0
    module_invalidation_ref: str = "unassigned"
    phase_graph_id: str = "unassigned"
    phase_graph_hash: str = "unassigned"
    phase_receipt_id: str = "unassigned"
    phase_receipt_hash: str = "unassigned"
    phase_count: int = 0
    phase_module_coverage_count: int = 0
    phase_dependency_count: int = 0
    phase_gate_count: int = 0
    phase_initially_runnable_count: int = 0
    phase_blocked_count: int = 0
    phase_parallel_pair_count: int = 0
    phase_invalidation_ref: str = "unassigned"
    context_graph_id: str = "unassigned"
    context_graph_hash: str = "unassigned"
    handoff_graph_id: str = "unassigned"
    handoff_graph_hash: str = "unassigned"
    handoff_receipt_id: str = "unassigned"
    handoff_receipt_hash: str = "unassigned"
    handoff_context_count: int = 0
    handoff_contract_count: int = 0
    internal_handoff_id: str = "unassigned"
    internal_handoff_hash: str = "unassigned"
    handoff_sender_phase: str = "unassigned"
    handoff_sender_module: str = "unassigned"
    handoff_receiver_phase: str = "unassigned"
    handoff_receiver_module: str = "unassigned"
    handoff_status: str = "unassigned"
    handoff_decision_id: str = "unassigned"
    handoff_decision_hash: str = "unassigned"
    handoff_invalidation_ref: str = "unassigned"
    minimum_context_graph_id: str = "unassigned"
    minimum_context_graph_hash: str = "unassigned"
    context_compilation_receipt_id: str = "unassigned"
    context_compilation_receipt_hash: str = "unassigned"
    context_manifest_count: int = 0
    context_reference_count: int = 0
    context_required_count: int = 0
    context_conditional_count: int = 0
    context_optional_count: int = 0
    context_forbidden_count: int = 0
    context_unavailable_count: int = 0
    context_not_applicable_count: int = 0
    context_included_count: int = 0
    context_excluded_count: int = 0
    context_summarized_count: int = 0
    context_retrieved_count: int = 0
    context_compressed_count: int = 0
    context_overflow_count: int = 0
    context_invalidation_ref: str = "unassigned"
    context_manifest_ids: tuple[str, ...] = ()
    context_manifest_hashes: tuple[str, ...] = ()
    context_reference_ids: tuple[str, ...] = ()
    context_loading_modes: tuple[tuple[str, str], ...] = ()
    context_hard_token_budgets: tuple[tuple[str, int], ...] = ()
    context_soft_token_budgets: tuple[tuple[str, int], ...] = ()
    skill_snapshot_id: str = "unassigned"
    skill_snapshot_hash: str = "unassigned"
    skill_registry_id: str = "unassigned"
    skill_registry_version: str = "unassigned"
    skill_registry_hash: str = "unassigned"
    skill_policy_id: str = "unassigned"
    skill_policy_hash: str = "unassigned"
    skill_schema_hash: str = "unassigned"
    skill_validation_receipt_id: str = "unassigned"
    skill_validation_receipt_hash: str = "unassigned"
    skill_consumption_receipt_id: str = "unassigned"
    skill_consumption_receipt_hash: str = "unassigned"
    skill_capability_count: int = 0
    registered_skill_count: int = 0
    required_external_skill_count: int = 0
    skill_adaptation_count: int = 0
    experimental_capability_count: int = 0
    skill_invalidation_ref: str = "unassigned"
    skill_replay_status: str = "unassigned"
    skill_necessity_decision_id: str = "unassigned"
    skill_necessity_decision_hash: str = "unassigned"
    skill_necessity_receipt_id: str = "unassigned"
    skill_necessity_receipt_hash: str = "unassigned"
    skill_necessity_outcome: str = "unassigned"
    skill_necessity_capability_count: int = 0
    skill_target_failure_count: int = 0
    skill_alternative_assessment_count: int = 0
    skill_missing_required_count: int = 0
    skill_experiment_count: int = 0
    skill_jit_capsule_count: int = 0
    skill_design_brief_count: int = 0
    skill_design_brief_disposition: str = "unassigned"
    skill_necessity_invalidation_ref: str = "unassigned"
    atomic_harness_definition_id: str = "unassigned"
    atomic_harness_definition_hash: str = "unassigned"
    atomic_harness_definition_receipt_id: str = "unassigned"
    atomic_harness_definition_receipt_hash: str = "unassigned"
    atomic_harness_definition_section_count: int = 0
    atomic_harness_definition_external_skill_count: int = 0
    atomic_harness_definition_external_runtime_count: int = 0
    atomic_harness_definition_certification: str = "unassigned"
    atomic_harness_definition_milestone: str = "unassigned"
    atomic_harness_definition_invalidation_ref: str = "unassigned"


class Clock(Protocol):
    def now(self) -> datetime: ...


class IdProvider(Protocol):
    def new_id(self, kind: str) -> str: ...


class ObservationSink(Protocol):
    def emit(self, observation: Observation) -> None: ...


class TargetProfileRepository(Protocol):
    def recognized_target_ids(self) -> frozenset[str]: ...

    def resolve(
        self,
        target_ids: tuple[str, ...],
        category_id: str,
        profile_id: str,
    ) -> TargetProfile: ...


class EvidenceWorkspace(Protocol):
    def load_profile(
        self, relative_path: str, expected_sha256: str
    ) -> "SourceProfile": ...

    def create_lock(
        self,
        *,
        run_id: str,
        profile: "SourceProfile",
        created_at: datetime,
        created_by: str,
        invalidates_lock_ref: str | None = None,
    ) -> tuple["SourceLock", object]: ...


class DeclaredBoundaryInputRepository(Protocol):
    def load(
        self, relative_path: str, expected_sha256: str
    ) -> "DeclaredBoundaryInput": ...


class RunRepository(Protocol):
    def append(
        self,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
    ) -> None: ...

    def load_run(self, run_id: str) -> Run: ...

    def events(self, run_id: str) -> tuple[RunEvent, ...]: ...

    def event_count(self, run_id: str) -> int: ...

    def get_command_record(self, command_id: str) -> CommandRecord | None: ...

    def save_command_record(self, command_id: str, record: CommandRecord) -> None: ...

    def add_checkpoint(self, checkpoint: "Checkpoint") -> None: ...

    def list_checkpoints(self, run_id: str) -> tuple["Checkpoint", ...]: ...


class EvidenceWorkspaceRepository(RunRepository, Protocol):
    def commit_evidence_workspace(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        source_lock: "SourceLock",
        command_id: str,
        command_record: CommandRecord,
    ) -> None: ...

    def get_source_lock(self, lock_id: str) -> "SourceLock" | None: ...

    def source_locks(self, run_id: str) -> tuple["SourceLock", ...]: ...


class AtomicityRepository(EvidenceWorkspaceRepository, Protocol):
    def commit_atomicity(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        decision: "AtomicityDecision | None",
        receipt: "AtomicityDecisionReceipt",
        boundary: "DeclaredAtomicBoundary | None",
        ratification: "AtomicityRatification | None",
        model: "DraftHarnessModel | None",
        invalidation: "BoundaryInvalidation | None",
        harness_ir_invalidation: "HarnessIRInvalidation | None" = None,
        artifact_set_invalidation: "ArtifactSetInvalidation | None" = None,
        constitutional_validation_invalidation: "ConstitutionalValidationInvalidation | None" = None,
        capability_ownership_invalidation: "CapabilityOwnershipInvalidation | None" = None,
        responsibility_module_invalidation: "ResponsibilityModuleInvalidation | None" = None,
        phase_graph_invalidation: "PhaseGraphInvalidation | None" = None,
        phase_handoff_invalidation: "PhaseHandoffInvalidation | None" = None,
        context_graph_invalidation: "ContextGraphInvalidation | None" = None,
        skill_registry_snapshot_invalidation: "SkillRegistrySnapshotInvalidation | None" = None,
        skill_necessity_invalidation: "SkillNecessityInvalidation | None" = None,
        atomic_harness_definition_invalidation: "AtomicHarnessDefinitionInvalidation | None" = None,
    ) -> None: ...

    def get_atomic_boundary(
        self, boundary_id: str
    ) -> "DeclaredAtomicBoundary | None": ...

    def get_atomicity_ratification(
        self, ratification_id: str
    ) -> "AtomicityRatification | None": ...

    def get_draft_harness_model(
        self, model_id: str
    ) -> "DraftHarnessModel | None": ...

    def get_atomicity_receipt(
        self, receipt_id: str
    ) -> "AtomicityDecisionReceipt | None": ...

    def get_boundary_invalidation(
        self, invalidation_id: str
    ) -> "BoundaryInvalidation | None": ...

    def is_boundary_invalidated(self, boundary_id: str) -> bool: ...

    def is_model_invalidated(self, model_id: str) -> bool: ...


class HarnessIRRepository(AtomicityRepository, Protocol):
    def commit_harness_ir(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        snapshot: "HarnessIR",
        receipt: "HarnessIRCompilationReceipt",
    ) -> None: ...

    def get_harness_ir(self, ir_id: str) -> "HarnessIR | None": ...

    def get_harness_ir_receipt(
        self, receipt_id: str
    ) -> "HarnessIRCompilationReceipt | None": ...

    def harness_irs(self, run_id: str) -> tuple["HarnessIR", ...]: ...

    def get_harness_ir_invalidation(
        self, invalidation_id: str
    ) -> "HarnessIRInvalidation | None": ...

    def is_harness_ir_invalidated(self, ir_id: str) -> bool: ...


class ArtifactRepository(HarnessIRRepository, Protocol):
    def commit_artifact_set(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        manifest: "ArtifactManifest",
        artifacts: tuple["GeneratedArtifact", ...],
        receipt: "ArtifactSetCompilationReceipt",
    ) -> None: ...

    def get_artifact_manifest(self, manifest_id: str) -> "ArtifactManifest | None": ...

    def artifacts_for_manifest(self, manifest_id: str) -> tuple["GeneratedArtifact", ...]: ...

    def get_artifact_receipt(
        self, receipt_id: str
    ) -> "ArtifactSetCompilationReceipt | None": ...

    def get_artifact_set_invalidation(
        self, invalidation_id: str
    ) -> "ArtifactSetInvalidation | None": ...

    def is_artifact_set_invalidated(self, artifact_set_id: str) -> bool: ...

    def save_artifact_drift_report(self, report: "ArtifactDriftReport") -> None: ...

    def get_artifact_drift_report(
        self, report_id: str
    ) -> "ArtifactDriftReport | None": ...


class ConstitutionalPolicyRepository(Protocol):
    def load(
        self, relative_path: str, expected_sha256: str
    ) -> "ConstitutionalPrecedencePolicy": ...


class ConstitutionalValidationRepository(ArtifactRepository, Protocol):
    def commit_constitutional_validation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        report: "ConstitutionalValidationReport",
        receipt: "ConstitutionalValidationReceipt",
    ) -> None: ...

    def get_constitutional_validation_report(
        self, report_id: str
    ) -> "ConstitutionalValidationReport | None": ...

    def get_constitutional_validation_receipt(
        self, receipt_id: str
    ) -> "ConstitutionalValidationReceipt | None": ...

    def get_constitutional_validation_invalidation(
        self, invalidation_id: str
    ) -> "ConstitutionalValidationInvalidation | None": ...

    def is_constitutional_validation_invalidated(self, report_id: str) -> bool: ...

    def constitutional_validation_receipts(
        self, run_id: str
    ) -> tuple["ConstitutionalValidationReceipt", ...]: ...


class CapabilityOwnershipRepository(ConstitutionalValidationRepository, Protocol):
    def commit_capability_ownership(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: "CapabilityOwnershipGraph",
        receipt: "CapabilityOwnershipReceipt",
    ) -> None: ...

    def get_capability_ownership_graph(
        self, graph_id: str
    ) -> "CapabilityOwnershipGraph | None": ...

    def capability_ownership_graphs(
        self, run_id: str
    ) -> tuple["CapabilityOwnershipGraph", ...]: ...

    def get_capability_ownership_receipt(
        self, receipt_id: str
    ) -> "CapabilityOwnershipReceipt | None": ...

    def capability_ownership_receipts(
        self, run_id: str
    ) -> tuple["CapabilityOwnershipReceipt", ...]: ...

    def get_capability_ownership_invalidation(
        self, invalidation_id: str
    ) -> "CapabilityOwnershipInvalidation | None": ...

    def is_capability_ownership_invalidated(self, graph_id: str) -> bool: ...


class ResponsibilityModuleRepository(CapabilityOwnershipRepository, Protocol):
    def commit_responsibility_modules(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: "ResponsibilityModuleGraph",
        receipt: "ResponsibilityModuleReceipt",
    ) -> None: ...

    def get_responsibility_module_graph(
        self, graph_id: str
    ) -> "ResponsibilityModuleGraph | None": ...

    def responsibility_module_graphs(
        self, run_id: str
    ) -> tuple["ResponsibilityModuleGraph", ...]: ...

    def get_responsibility_module_receipt(
        self, receipt_id: str
    ) -> "ResponsibilityModuleReceipt | None": ...

    def responsibility_module_receipts(
        self, run_id: str
    ) -> tuple["ResponsibilityModuleReceipt", ...]: ...

    def get_responsibility_module_invalidation(
        self, invalidation_id: str
    ) -> "ResponsibilityModuleInvalidation | None": ...

    def is_responsibility_module_invalidated(self, graph_id: str) -> bool: ...


class PhaseGraphRepository(ResponsibilityModuleRepository, Protocol):
    def commit_phase_graph(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: "PhaseGraph",
        receipt: "PhaseGraphReceipt",
    ) -> None: ...

    def get_phase_graph(self, graph_id: str) -> "PhaseGraph | None": ...

    def phase_graphs(self, run_id: str) -> tuple["PhaseGraph", ...]: ...

    def get_phase_graph_receipt(
        self, receipt_id: str
    ) -> "PhaseGraphReceipt | None": ...

    def phase_graph_receipts(
        self, run_id: str
    ) -> tuple["PhaseGraphReceipt", ...]: ...

    def get_phase_graph_invalidation(
        self, invalidation_id: str
    ) -> "PhaseGraphInvalidation | None": ...

    def is_phase_graph_invalidated(self, graph_id: str) -> bool: ...


class PhaseHandoffRepository(PhaseGraphRepository, Protocol):
    def commit_phase_handoffs(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: "PhaseHandoffGraph",
        receipt: "PhaseHandoffReceipt",
    ) -> None: ...

    def commit_internal_handoff(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        handoff: "InternalHandoff",
        receipt: "InternalHandoffReceipt",
    ) -> None: ...

    def commit_internal_handoff_decision(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        handoff: "InternalHandoff",
        decision: "InternalHandoffDecision",
        receipt: "InternalHandoffReceipt",
    ) -> None: ...

    def get_phase_handoff_graph(
        self, graph_id: str
    ) -> "PhaseHandoffGraph | None": ...

    def phase_handoff_graphs(
        self, run_id: str
    ) -> tuple["PhaseHandoffGraph", ...]: ...

    def phase_handoff_receipts(
        self, run_id: str
    ) -> tuple["PhaseHandoffReceipt", ...]: ...

    def get_internal_handoff(
        self, handoff_id: str
    ) -> "InternalHandoff | None": ...

    def internal_handoffs(self, run_id: str) -> tuple["InternalHandoff", ...]: ...

    def get_internal_handoff_decision(
        self, handoff_id: str
    ) -> "InternalHandoffDecision | None": ...

    def get_phase_handoff_invalidation(
        self, invalidation_id: str
    ) -> "PhaseHandoffInvalidation | None": ...

    def is_phase_handoff_invalidated(self, graph_id: str) -> bool: ...


class MinimumContextRepository(PhaseHandoffRepository, Protocol):
    def commit_minimum_context(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: "MinimumCompleteContextGraph",
        receipt: "ContextCompilationReceipt",
    ) -> None: ...

    def get_minimum_context_graph(
        self, graph_id: str
    ) -> "MinimumCompleteContextGraph | None": ...

    def minimum_context_graphs(
        self, run_id: str
    ) -> tuple["MinimumCompleteContextGraph", ...]: ...

    def get_context_compilation_receipt(
        self, receipt_id: str
    ) -> "ContextCompilationReceipt | None": ...

    def context_compilation_receipts(
        self, run_id: str
    ) -> tuple["ContextCompilationReceipt", ...]: ...

    def get_context_graph_invalidation(
        self, invalidation_id: str
    ) -> "ContextGraphInvalidation | None": ...

    def is_minimum_context_invalidated(self, graph_id: str) -> bool: ...


class SkillRegistryRepository(MinimumContextRepository, Protocol):
    def commit_skill_registry_snapshot(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        snapshot: "SyntheticSkillRegistrySnapshot",
        receipt: "SkillRegistryConsumptionReceipt",
    ) -> None: ...

    def get_skill_registry_snapshot(
        self, snapshot_id: str
    ) -> "SyntheticSkillRegistrySnapshot | None": ...

    def skill_registry_snapshots(
        self, run_id: str
    ) -> tuple["SyntheticSkillRegistrySnapshot", ...]: ...

    def get_skill_registry_consumption_receipt(
        self, receipt_id: str
    ) -> "SkillRegistryConsumptionReceipt | None": ...

    def skill_registry_consumption_receipts(
        self, run_id: str
    ) -> tuple["SkillRegistryConsumptionReceipt", ...]: ...

    def get_skill_registry_snapshot_invalidation(
        self, invalidation_id: str
    ) -> "SkillRegistrySnapshotInvalidation | None": ...

    def is_skill_registry_snapshot_invalidated(self, snapshot_id: str) -> bool: ...


class SkillNecessityRepository(SkillRegistryRepository, Protocol):
    def commit_skill_necessity(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        decision: "SkillNecessityDecision",
        receipt: "SkillNecessityReceipt",
    ) -> None: ...

    def get_skill_necessity_decision(
        self, decision_id: str
    ) -> "SkillNecessityDecision | None": ...

    def skill_necessity_decisions(
        self, run_id: str
    ) -> tuple["SkillNecessityDecision", ...]: ...

    def get_skill_necessity_receipt(
        self, receipt_id: str
    ) -> "SkillNecessityReceipt | None": ...

    def skill_necessity_receipts(
        self, run_id: str
    ) -> tuple["SkillNecessityReceipt", ...]: ...

    def get_skill_necessity_invalidation(
        self, invalidation_id: str
    ) -> "SkillNecessityInvalidation | None": ...

    def is_skill_necessity_invalidated(self, decision_id: str) -> bool: ...


class AtomicHarnessDefinitionRepository(SkillNecessityRepository, Protocol):
    def commit_atomic_harness_definition(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        definition: "AtomicHarnessDefinition",
        receipt: "AtomicHarnessDefinitionReceipt",
    ) -> None: ...

    def get_atomic_harness_definition(
        self, definition_id: str
    ) -> "AtomicHarnessDefinition | None": ...

    def atomic_harness_definitions(
        self, run_id: str
    ) -> tuple["AtomicHarnessDefinition", ...]: ...

    def get_atomic_harness_definition_receipt(
        self, receipt_id: str
    ) -> "AtomicHarnessDefinitionReceipt | None": ...

    def atomic_harness_definition_receipts(
        self, run_id: str
    ) -> tuple["AtomicHarnessDefinitionReceipt", ...]: ...

    def get_atomic_harness_definition_invalidation(
        self, invalidation_id: str
    ) -> "AtomicHarnessDefinitionInvalidation | None": ...

    def is_atomic_harness_definition_invalidated(
        self, definition_id: str
    ) -> bool: ...
