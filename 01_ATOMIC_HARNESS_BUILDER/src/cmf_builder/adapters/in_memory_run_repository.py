from __future__ import annotations

from datetime import datetime
from functools import wraps
from hashlib import sha256
from threading import RLock
from uuid import UUID

from cmf_builder.application.checkpoints import Checkpoint
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    CommandRecord,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
    Observation,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.evidence_index import (
    EvidenceIndex,
    EvidenceIndexInvalidation,
    EvidenceIndexReceipt,
    Specimen,
)
from cmf_builder.domain.evidence_saturation import (
    SaturationContract,
    SaturationEvaluation,
    SaturationInvalidation,
    SaturationReceipt,
)
from cmf_builder.domain.genesis_questions import (
    DecisionGraph,
    GenesisQuestionInvalidation,
    GenesisQuestionPackage,
    GenesisQuestionReceipt,
)
from cmf_builder.domain.atomicity import (
    AtomicityDecision,
    AtomicityDecisionReceipt,
    AtomicityRatification,
    BoundaryInvalidation,
    DeclaredAtomicBoundary,
    DraftHarnessModel,
)
from cmf_builder.domain.run import Run, RunEvent
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
    ReproducibleBuildConfig,
)
from cmf_builder.domain.constitutional_validation import (
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
from cmf_builder.domain.target_package_validation import (
    AtomicContentHarnessValidationInvalidation,
    AtomicContentHarnessValidationReceipt,
    AtomicContentHarnessValidationReport,
)
from cmf_builder.domain.development_capsule import (
    DevelopmentCapsuleInvalidation,
    DevelopmentCapsuleReceipt,
    VersionedTraceableDevelopmentCapsule,
)

__all__ = [
    "AtomicCommitFailed",
    "ConcurrencyConflict",
    "DeterministicUuid7IdProvider",
    "FixedClock",
    "IdempotencyPayloadMismatch",
    "InMemoryRunRepository",
    "RecordingObservationSink",
]


def _synchronized(method):
    @wraps(method)
    def guarded(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    return guarded


class InMemoryRunRepository:
    """Deterministic test/development adapter; never a production persistence claim."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._streams: dict[str, tuple[RunEvent, ...]] = {}
        self._command_records: dict[str, CommandRecord] = {}
        self._checkpoints: dict[str, dict[str, Checkpoint]] = {}
        self._source_locks: dict[str, SourceLock] = {}
        self._run_source_locks: dict[str, tuple[str, ...]] = {}
        self._evidence_indexes: dict[str, EvidenceIndex] = {}
        self._run_evidence_indexes: dict[str, tuple[str, ...]] = {}
        self._evidence_index_receipts: dict[str, EvidenceIndexReceipt] = {}
        self._run_evidence_index_receipts: dict[str, tuple[str, ...]] = {}
        self._evidence_index_invalidations: dict[
            str, EvidenceIndexInvalidation
        ] = {}
        self._invalidated_evidence_indexes: dict[str, str] = {}
        self._saturation_contracts: dict[str, SaturationContract] = {}
        self._saturation_evaluations: dict[str, SaturationEvaluation] = {}
        self._run_saturation_evaluations: dict[str, tuple[str, ...]] = {}
        self._saturation_receipts: dict[str, SaturationReceipt] = {}
        self._run_saturation_receipts: dict[str, tuple[str, ...]] = {}
        self._saturation_invalidations: dict[str, SaturationInvalidation] = {}
        self._invalidated_saturation_evaluations: dict[str, str] = {}
        self._decision_graphs: dict[str, DecisionGraph] = {}
        self._genesis_question_packages: dict[str, GenesisQuestionPackage] = {}
        self._run_genesis_question_packages: dict[str, tuple[str, ...]] = {}
        self._genesis_question_receipts: dict[str, GenesisQuestionReceipt] = {}
        self._genesis_question_invalidations: dict[str, GenesisQuestionInvalidation] = {}
        self._invalidated_genesis_questions: dict[str, str] = {}
        self._atomic_boundaries: dict[str, DeclaredAtomicBoundary] = {}
        self._atomicity_ratifications: dict[str, AtomicityRatification] = {}
        self._draft_harness_models: dict[str, DraftHarnessModel] = {}
        self._atomicity_decisions: dict[str, tuple[AtomicityDecision, ...]] = {}
        self._atomicity_receipts: dict[str, AtomicityDecisionReceipt] = {}
        self._boundary_invalidations: dict[str, BoundaryInvalidation] = {}
        self._invalidated_boundaries: dict[str, str] = {}
        self._invalidated_models: dict[str, str] = {}
        self._harness_irs: dict[str, HarnessIR] = {}
        self._run_harness_irs: dict[str, tuple[str, ...]] = {}
        self._harness_ir_receipts: dict[str, HarnessIRCompilationReceipt] = {}
        self._harness_ir_invalidations: dict[str, HarnessIRInvalidation] = {}
        self._invalidated_harness_irs: dict[str, str] = {}
        self._artifact_manifests: dict[str, ArtifactManifest] = {}
        self._run_artifact_manifests: dict[str, tuple[str, ...]] = {}
        self._artifact_manifest_artifacts: dict[str, tuple[GeneratedArtifact, ...]] = {}
        self._artifact_receipts: dict[str, ArtifactSetCompilationReceipt] = {}
        self._artifact_set_invalidations: dict[str, ArtifactSetInvalidation] = {}
        self._invalidated_artifact_sets: dict[str, str] = {}
        self._artifact_drift_reports: dict[str, ArtifactDriftReport] = {}
        self._constitutional_validation_reports: dict[
            str, ConstitutionalValidationReport
        ] = {}
        self._run_constitutional_validation_reports: dict[str, tuple[str, ...]] = {}
        self._constitutional_validation_receipts: dict[
            str, ConstitutionalValidationReceipt
        ] = {}
        self._run_constitutional_validation_receipts: dict[
            str, tuple[str, ...]
        ] = {}
        self._constitutional_validation_invalidations: dict[
            str, ConstitutionalValidationInvalidation
        ] = {}
        self._invalidated_constitutional_validations: dict[str, str] = {}
        self._capability_ownership_graphs: dict[str, CapabilityOwnershipGraph] = {}
        self._run_capability_ownership_graphs: dict[str, tuple[str, ...]] = {}
        self._capability_ownership_receipts: dict[
            str, CapabilityOwnershipReceipt
        ] = {}
        self._run_capability_ownership_receipts: dict[str, tuple[str, ...]] = {}
        self._capability_ownership_invalidations: dict[
            str, CapabilityOwnershipInvalidation
        ] = {}
        self._invalidated_capability_ownership_graphs: dict[str, str] = {}
        self._responsibility_module_graphs: dict[str, ResponsibilityModuleGraph] = {}
        self._run_responsibility_module_graphs: dict[str, tuple[str, ...]] = {}
        self._responsibility_module_receipts: dict[
            str, ResponsibilityModuleReceipt
        ] = {}
        self._run_responsibility_module_receipts: dict[str, tuple[str, ...]] = {}
        self._responsibility_module_invalidations: dict[
            str, ResponsibilityModuleInvalidation
        ] = {}
        self._invalidated_responsibility_module_graphs: dict[str, str] = {}
        self._phase_graphs: dict[str, PhaseGraph] = {}
        self._run_phase_graphs: dict[str, tuple[str, ...]] = {}
        self._phase_graph_receipts: dict[str, PhaseGraphReceipt] = {}
        self._run_phase_graph_receipts: dict[str, tuple[str, ...]] = {}
        self._phase_graph_invalidations: dict[str, PhaseGraphInvalidation] = {}
        self._invalidated_phase_graphs: dict[str, str] = {}
        self._phase_handoff_graphs: dict[str, PhaseHandoffGraph] = {}
        self._run_phase_handoff_graphs: dict[str, tuple[str, ...]] = {}
        self._phase_handoff_receipts: dict[str, PhaseHandoffReceipt] = {}
        self._run_phase_handoff_receipts: dict[str, tuple[str, ...]] = {}
        self._internal_handoffs: dict[str, InternalHandoff] = {}
        self._run_internal_handoffs: dict[str, tuple[str, ...]] = {}
        self._internal_handoff_decisions: dict[str, InternalHandoffDecision] = {}
        self._internal_handoff_receipts: dict[str, InternalHandoffReceipt] = {}
        self._run_internal_handoff_receipts: dict[str, tuple[str, ...]] = {}
        self._phase_handoff_invalidations: dict[str, PhaseHandoffInvalidation] = {}
        self._invalidated_phase_handoff_graphs: dict[str, str] = {}
        self._minimum_context_graphs: dict[str, MinimumCompleteContextGraph] = {}
        self._run_minimum_context_graphs: dict[str, tuple[str, ...]] = {}
        self._context_compilation_receipts: dict[str, ContextCompilationReceipt] = {}
        self._run_context_compilation_receipts: dict[str, tuple[str, ...]] = {}
        self._context_graph_invalidations: dict[str, ContextGraphInvalidation] = {}
        self._invalidated_minimum_context_graphs: dict[str, str] = {}
        self._skill_registry_snapshots: dict[str, SyntheticSkillRegistrySnapshot] = {}
        self._run_skill_registry_snapshots: dict[str, tuple[str, ...]] = {}
        self._skill_registry_consumption_receipts: dict[
            str, SkillRegistryConsumptionReceipt
        ] = {}
        self._run_skill_registry_consumption_receipts: dict[str, tuple[str, ...]] = {}
        self._skill_registry_snapshot_invalidations: dict[
            str, SkillRegistrySnapshotInvalidation
        ] = {}
        self._invalidated_skill_registry_snapshots: dict[str, str] = {}
        self._skill_necessity_decisions: dict[str, SkillNecessityDecision] = {}
        self._run_skill_necessity_decisions: dict[str, tuple[str, ...]] = {}
        self._skill_necessity_receipts: dict[str, SkillNecessityReceipt] = {}
        self._run_skill_necessity_receipts: dict[str, tuple[str, ...]] = {}
        self._skill_necessity_invalidations: dict[str, SkillNecessityInvalidation] = {}
        self._invalidated_skill_necessity_decisions: dict[str, str] = {}
        self._atomic_harness_definitions: dict[str, AtomicHarnessDefinition] = {}
        self._run_atomic_harness_definitions: dict[str, tuple[str, ...]] = {}
        self._atomic_harness_definition_receipts: dict[
            str, AtomicHarnessDefinitionReceipt
        ] = {}
        self._run_atomic_harness_definition_receipts: dict[str, tuple[str, ...]] = {}
        self._atomic_harness_definition_invalidations: dict[
            str, AtomicHarnessDefinitionInvalidation
        ] = {}
        self._invalidated_atomic_harness_definitions: dict[str, str] = {}
        self._atomic_content_harness_validation_reports: dict[
            str, AtomicContentHarnessValidationReport
        ] = {}
        self._run_atomic_content_harness_validation_reports: dict[
            str, tuple[str, ...]
        ] = {}
        self._atomic_content_harness_validation_receipts: dict[
            str, AtomicContentHarnessValidationReceipt
        ] = {}
        self._run_atomic_content_harness_validation_receipts: dict[
            str, tuple[str, ...]
        ] = {}
        self._atomic_content_harness_validation_invalidations: dict[
            str, AtomicContentHarnessValidationInvalidation
        ] = {}
        self._invalidated_atomic_content_harness_validations: dict[str, str] = {}
        self._development_capsules: dict[
            str, VersionedTraceableDevelopmentCapsule
        ] = {}
        self._run_development_capsules: dict[str, tuple[str, ...]] = {}
        self._development_capsule_receipts: dict[
            str, DevelopmentCapsuleReceipt
        ] = {}
        self._run_development_capsule_receipts: dict[str, tuple[str, ...]] = {}
        self._development_capsule_invalidations: dict[
            str, DevelopmentCapsuleInvalidation
        ] = {}
        self._invalidated_development_capsules: dict[str, str] = {}
        self._fail_next_atomic_commit = False
        self._fail_next_run_command_boundary: str | None = None
        self._pending_observation_outbox: dict[str, tuple[Observation, ...]] = {}
        self._inflight_observation_outbox: dict[str, Observation] = {}
        self._delivered_observation_outbox: dict[str, tuple[Observation, ...]] = {}

    @property
    @_synchronized
    def stream_count(self) -> int:
        return len(self._streams)

    @_synchronized
    def append(
        self,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        self._streams[run_id] = (*current, *events)

    @_synchronized
    def commit_run_command(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        checkpoint: Checkpoint | None,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        result = command_record.result
        result_event_ids = tuple(getattr(result, "event_ids", ()))
        event_ids = tuple(event.event_id for event in events)
        if (
            not events
            or any(event.command_id != command_id for event in events)
            or getattr(result, "command_id", None) != command_id
            or getattr(result, "run_id", None) != run_id
            or result_event_ids != event_ids
        ):
            raise ConcurrencyConflict(
                "Run command receipt, events and command identity must agree.",
                run_id=run_id,
                command_id=command_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        checkpoint_store = self._checkpoints.get(run_id, {})
        if checkpoint is not None:
            if (
                checkpoint.run_id != run_id
                or getattr(result, "detail")("checkpoint_id")
                != checkpoint.checkpoint_id
            ):
                raise ConcurrencyConflict(
                    "Checkpoint and command receipt identities differ.",
                    run_id=run_id,
                    command_id=command_id,
                )
            existing_checkpoint = checkpoint_store.get(checkpoint.checkpoint_id)
            if existing_checkpoint is not None and existing_checkpoint != checkpoint:
                raise ConcurrencyConflict(
                    "A checkpoint identity cannot be overwritten.",
                    checkpoint_id=checkpoint.checkpoint_id,
                )
        for boundary in ("events", "checkpoint", "command_record"):
            if self._fail_next_run_command_boundary == boundary:
                self._fail_next_run_command_boundary = None
                raise AtomicCommitFailed(
                    "Injected run-command transaction failure.",
                    run_id=run_id,
                    command_id=command_id,
                    boundary=boundary,
                )
        self._streams[run_id] = (*current, *events)
        if checkpoint is not None:
            self._checkpoints.setdefault(run_id, {})[
                checkpoint.checkpoint_id
            ] = checkpoint
        self._command_records[command_id] = command_record

    @_synchronized
    def inject_next_run_command_commit_failure(self, boundary: str) -> None:
        if boundary not in {"events", "checkpoint", "command_record"}:
            raise ValueError(f"Unsupported run-command failure boundary: {boundary}")
        self._fail_next_run_command_boundary = boundary

    @_synchronized
    def commit_evidence_workspace(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        source_lock: SourceLock,
        command_id: str,
        command_record: CommandRecord,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        if source_lock.run_id != run_id:
            raise ConcurrencyConflict(
                "A Source Lock cannot be committed to a different run.",
                run_id=run_id,
                source_lock_run_id=source_lock.run_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        existing_lock = self._source_locks.get(source_lock.lock_id)
        if existing_lock is not None and existing_lock != source_lock:
            raise ConcurrencyConflict(
                "A Source Lock identity cannot be overwritten.",
                source_lock_id=source_lock.lock_id,
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the atomic commit.",
                run_id=run_id,
                source_lock_id=source_lock.lock_id,
            )

        self._streams[run_id] = (*current, *events)
        self._source_locks[source_lock.lock_id] = source_lock
        prior = self._run_source_locks.get(run_id, ())
        if source_lock.lock_id not in prior:
            self._run_source_locks[run_id] = (*prior, source_lock.lock_id)
        self._command_records[command_id] = command_record

    @_synchronized
    def inject_next_atomic_commit_failure(self) -> None:
        self._fail_next_atomic_commit = True

    @_synchronized
    def commit_evidence_index(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        index: EvidenceIndex,
        receipt: EvidenceIndexReceipt,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        source_lock = self._source_locks.get(index.source_lock_ref)
        if source_lock is None or source_lock.run_id != run_id:
            raise ConcurrencyConflict(
                "Evidence indexing requires the run's authoritative Source Lock.",
                run_id=run_id,
                source_lock_ref=index.source_lock_ref,
            )
        index.validate(source_lock)
        receipt.validate(index)
        if (
            index.run_id != run_id
            or command_record.result != receipt
            or receipt.command_id != command_id
            or len(events) != 1
            or events[0].event_type != "EvidenceIndexAttached"
            or events[0].command_id != command_id
            or events[0].actor_id != index.authority_identity
            or events[0].value("index_ref") != index.index_id
            or events[0].value("index_hash") != index.index_hash
            or events[0].value("source_lock_ref") != index.source_lock_ref
            or receipt.event_ids != (events[0].event_id,)
            or receipt.stream_version != events[0].stream_version
        ):
            raise ConcurrencyConflict(
                "Evidence index, event, receipt, authority and command must agree.",
                run_id=run_id,
                command_id=command_id,
            )
        self._assert_same_or_absent(
            self._evidence_indexes, index.index_id, index, "evidence index"
        )
        self._assert_same_or_absent(
            self._evidence_index_receipts,
            receipt.receipt_id,
            receipt,
            "evidence index receipt",
        )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected evidence-index transaction failure.",
                run_id=run_id,
                index_id=index.index_id,
            )
        self._streams[run_id] = (*current, *events)
        self._evidence_indexes[index.index_id] = index
        self._run_evidence_indexes[run_id] = (
            *self._run_evidence_indexes.get(run_id, ()),
            index.index_id,
        )
        self._evidence_index_receipts[receipt.receipt_id] = receipt
        self._run_evidence_index_receipts[run_id] = (
            *self._run_evidence_index_receipts.get(run_id, ()),
            receipt.receipt_id,
        )
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_evidence_index_invalidation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        invalidation: EvidenceIndexInvalidation,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        index = self._evidence_indexes.get(invalidation.index_id)
        if index is None or index.run_id != run_id:
            raise ConcurrencyConflict(
                "Evidence-index invalidation requires an immutable historical index."
            )
        invalidation.validate(index)
        if (
            command_record.result != invalidation
            or invalidation.command_id != command_id
            or invalidation.index_hash != index.index_hash
            or invalidation.source_lock_ref != index.source_lock_ref
            or len(events) != 1
            or events[0].event_type != "EvidenceIndexInvalidated"
            or events[0].command_id != command_id
            or events[0].actor_id != invalidation.authority_identity
            or events[0].value("index_ref") != index.index_id
            or events[0].value("invalidation_ref") != invalidation.invalidation_id
            or invalidation.event_ids != (events[0].event_id,)
            or invalidation.stream_version != events[0].stream_version
            or index.index_id in self._invalidated_evidence_indexes
        ):
            raise ConcurrencyConflict(
                "Evidence-index invalidation, event, authority and command must agree."
            )
        self._assert_same_or_absent(
            self._evidence_index_invalidations,
            invalidation.invalidation_id,
            invalidation,
            "evidence index invalidation",
        )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected evidence-index invalidation transaction failure.",
                run_id=run_id,
                index_id=index.index_id,
            )
        self._streams[run_id] = (*current, *events)
        self._evidence_index_invalidations[
            invalidation.invalidation_id
        ] = invalidation
        self._invalidated_evidence_indexes[
            index.index_id
        ] = invalidation.invalidation_id
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_saturation_evaluation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        contract: SaturationContract,
        evaluation: SaturationEvaluation,
        receipt: SaturationReceipt,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        source_lock = self._source_locks.get(evaluation.source_lock_ref)
        index = self._evidence_indexes.get(evaluation.evidence_index_ref)
        if (
            source_lock is None
            or index is None
            or source_lock.run_id != run_id
            or index.run_id != run_id
            or index.index_id in self._invalidated_evidence_indexes
        ):
            raise ConcurrencyConflict(
                "Saturation requires the active immutable Source Lock and Evidence Index."
            )
        evaluation.validate(source_lock=source_lock, index=index, contract=contract)
        receipt.validate(evaluation)
        if (
            evaluation.run_id != run_id
            or command_record.result != receipt
            or receipt.command_id != command_id
            or len(events) != 1
            or events[0].event_type != "SaturationEvaluationAttached"
            or events[0].command_id != command_id
            or events[0].actor_id != evaluation.authority_identity
            or events[0].value("evaluation_ref") != evaluation.evaluation_id
            or events[0].value("evaluation_hash") != evaluation.evaluation_hash
            or events[0].value("contract_ref") != contract.contract_id
            or events[0].value("contract_hash") != contract.contract_hash
            or events[0].value("source_lock_ref") != source_lock.lock_id
            or events[0].value("evidence_index_ref") != index.index_id
            or events[0].value("outcome") != evaluation.outcome.value
            or events[0].value("downstream_consequence")
            != evaluation.downstream_consequence.value
            or receipt.event_ids != (events[0].event_id,)
            or receipt.stream_version != events[0].stream_version
        ):
            raise ConcurrencyConflict(
                "Saturation contract, evaluation, event, receipt, authority and command must agree."
            )
        self._assert_same_or_absent(
            self._saturation_contracts, contract.contract_id, contract, "saturation contract"
        )
        self._assert_same_or_absent(
            self._saturation_evaluations,
            evaluation.evaluation_id,
            evaluation,
            "saturation evaluation",
        )
        self._assert_same_or_absent(
            self._saturation_receipts,
            receipt.receipt_id,
            receipt,
            "saturation receipt",
        )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected saturation-evaluation transaction failure.",
                run_id=run_id,
                evaluation_id=evaluation.evaluation_id,
            )
        self._streams[run_id] = (*current, *events)
        self._saturation_contracts[contract.contract_id] = contract
        self._saturation_evaluations[evaluation.evaluation_id] = evaluation
        self._run_saturation_evaluations[run_id] = (
            *self._run_saturation_evaluations.get(run_id, ()),
            evaluation.evaluation_id,
        )
        self._saturation_receipts[receipt.receipt_id] = receipt
        self._run_saturation_receipts[run_id] = (
            *self._run_saturation_receipts.get(run_id, ()),
            receipt.receipt_id,
        )
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_saturation_invalidation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        invalidation: SaturationInvalidation,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        evaluation = self._saturation_evaluations.get(invalidation.evaluation_id)
        if evaluation is None or evaluation.run_id != run_id:
            raise ConcurrencyConflict(
                "Saturation invalidation requires an immutable historical evaluation."
            )
        invalidation.validate(evaluation)
        if (
            command_record.result != invalidation
            or invalidation.command_id != command_id
            or len(events) != 1
            or events[0].event_type != "SaturationEvaluationInvalidated"
            or events[0].command_id != command_id
            or events[0].actor_id != invalidation.authority_identity
            or events[0].value("evaluation_ref") != evaluation.evaluation_id
            or events[0].value("invalidation_ref") != invalidation.invalidation_id
            or invalidation.event_ids != (events[0].event_id,)
            or invalidation.stream_version != events[0].stream_version
            or evaluation.evaluation_id in self._invalidated_saturation_evaluations
        ):
            raise ConcurrencyConflict(
                "Saturation invalidation, event, authority and command must agree."
            )
        self._assert_same_or_absent(
            self._saturation_invalidations,
            invalidation.invalidation_id,
            invalidation,
            "saturation invalidation",
        )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected saturation-invalidation transaction failure.",
                run_id=run_id,
                evaluation_id=evaluation.evaluation_id,
            )
        self._streams[run_id] = (*current, *events)
        self._saturation_invalidations[invalidation.invalidation_id] = invalidation
        self._invalidated_saturation_evaluations[
            evaluation.evaluation_id
        ] = invalidation.invalidation_id
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_genesis_question(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: DecisionGraph,
        package: GenesisQuestionPackage,
        receipt: GenesisQuestionReceipt,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        run = Run.replay(current)
        saturation = self._saturation_evaluations.get(graph.saturation_ref)
        model = self._draft_harness_models.get(graph.model_ref)
        if (
            saturation is None or model is None
            or saturation.evaluation_hash != graph.saturation_hash
            or model.model_hash != graph.model_hash
            or run.saturation_evaluation_ref != graph.saturation_ref
            or run.draft_harness_model_ref != graph.model_ref
            or run.atomic_boundary_ref != graph.boundary_ref
            or run.atomicity_ratification_ref != graph.ratification_ref
            or run.saturation_evaluation_invalidation_ref is not None
            or run.boundary_invalidation_ref is not None
            or graph.run_id != run_id or package.run_id != run_id
            or package.graph_ref != graph.graph_id or package.graph_hash != graph.graph_hash
            or package.selected_decision_id != graph.selected_decision_id
            or receipt.run_id != run_id or receipt.command_id != command_id
            or receipt.graph_id != graph.graph_id or receipt.graph_hash != graph.graph_hash
            or receipt.package_id != package.package_id or receipt.package_hash != package.package_hash
            or receipt.selected_decision_id != graph.selected_decision_id
            or receipt.authority_identity != package.authority_identity
            or command_record.result != receipt
            or len(events) != 1 or events[0].event_type != "GenesisQuestionPackageAttached"
            or events[0].command_id != command_id or events[0].actor_id != package.authority_identity
            or events[0].value("package_ref") != package.package_id
            or events[0].value("package_hash") != package.package_hash
            or events[0].value("graph_ref") != graph.graph_id
            or events[0].value("graph_hash") != graph.graph_hash
            or events[0].value("model_ref") != model.model_id
            or events[0].value("saturation_ref") != saturation.evaluation_id
            or receipt.event_ids != (events[0].event_id,)
            or receipt.stream_version != events[0].stream_version
        ):
            raise ConcurrencyConflict("Genesis graph, package, event, receipt and active authority must agree.")
        graph.selected_node()
        package.validate(graph)
        receipt.validate(graph, package)
        self._assert_same_or_absent(self._decision_graphs, graph.graph_id, graph, "decision graph")
        self._assert_same_or_absent(self._genesis_question_packages, package.package_id, package, "Genesis question package")
        self._assert_same_or_absent(self._genesis_question_receipts, receipt.receipt_id, receipt, "Genesis question receipt")
        existing = self._command_records.get(command_id)
        if existing is not None and existing != command_record:
            raise IdempotencyPayloadMismatch("A command record cannot be overwritten.", command_id=command_id)
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed("Injected Genesis-question transaction failure.", run_id=run_id)
        self._streams[run_id] = (*current, *events)
        self._decision_graphs[graph.graph_id] = graph
        self._genesis_question_packages[package.package_id] = package
        self._run_genesis_question_packages[run_id] = (*self._run_genesis_question_packages.get(run_id, ()), package.package_id)
        self._genesis_question_receipts[receipt.receipt_id] = receipt
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_genesis_question_invalidation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        invalidation: GenesisQuestionInvalidation,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        package = self._genesis_question_packages.get(invalidation.package_id)
        if (
            package is None or package.run_id != run_id
            or package.package_hash != invalidation.package_hash
            or package.package_id in self._invalidated_genesis_questions
            or command_record.result != invalidation
            or invalidation.command_id != command_id
            or len(events) != 1 or events[0].event_type != "GenesisQuestionPackageInvalidated"
            or events[0].actor_id != invalidation.authority_identity
            or events[0].value("package_ref") != package.package_id
            or events[0].value("package_hash") != package.package_hash
            or events[0].value("invalidation_ref") != invalidation.invalidation_id
            or invalidation.event_ids != (events[0].event_id,)
            or invalidation.stream_version != events[0].stream_version
        ):
            raise ConcurrencyConflict("Genesis-question invalidation must target exactly one active package.")
        self._assert_same_or_absent(self._genesis_question_invalidations, invalidation.invalidation_id, invalidation, "Genesis question invalidation")
        invalidation.validate(package)
        existing = self._command_records.get(command_id)
        if existing is not None and existing != command_record:
            raise IdempotencyPayloadMismatch("A command record cannot be overwritten.", command_id=command_id)
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed("Injected Genesis-question invalidation failure.", run_id=run_id)
        self._streams[run_id] = (*current, *events)
        self._genesis_question_invalidations[invalidation.invalidation_id] = invalidation
        self._invalidated_genesis_questions[package.package_id] = invalidation.invalidation_id
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def commit_atomicity(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        decision: AtomicityDecision | None,
        receipt: AtomicityDecisionReceipt,
        boundary: DeclaredAtomicBoundary | None,
        ratification: AtomicityRatification | None,
        model: DraftHarnessModel | None,
        invalidation: BoundaryInvalidation | None,
        harness_ir_invalidation: HarnessIRInvalidation | None = None,
        artifact_set_invalidation: ArtifactSetInvalidation | None = None,
        constitutional_validation_invalidation: ConstitutionalValidationInvalidation
        | None = None,
        capability_ownership_invalidation: CapabilityOwnershipInvalidation
        | None = None,
        responsibility_module_invalidation: ResponsibilityModuleInvalidation
        | None = None,
        phase_graph_invalidation: PhaseGraphInvalidation | None = None,
        phase_handoff_invalidation: PhaseHandoffInvalidation | None = None,
        context_graph_invalidation: ContextGraphInvalidation | None = None,
        skill_registry_snapshot_invalidation: SkillRegistrySnapshotInvalidation
        | None = None,
        skill_necessity_invalidation: SkillNecessityInvalidation | None = None,
        atomic_harness_definition_invalidation: AtomicHarnessDefinitionInvalidation
        | None = None,
        atomic_content_harness_validation_invalidation: AtomicContentHarnessValidationInvalidation
        | None = None,
        development_capsule_invalidation: DevelopmentCapsuleInvalidation
        | None = None,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        source_lock = self._source_locks.get(receipt.source_lock_ref)
        if source_lock is None or source_lock.run_id != run_id:
            raise ConcurrencyConflict(
                "Atomicity commit requires the run's authoritative Source Lock.",
                run_id=run_id,
                source_lock_ref=receipt.source_lock_ref,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        if receipt.run_id != run_id:
            raise ConcurrencyConflict(
                "Atomicity receipt belongs to a different run.",
                run_id=run_id,
                receipt_run_id=receipt.run_id,
            )
        self._assert_same_or_absent(
            self._atomicity_receipts, receipt.receipt_id, receipt, "receipt"
        )
        if boundary is not None:
            self._assert_same_or_absent(
                self._atomic_boundaries, boundary.boundary_id, boundary, "boundary"
            )
            if boundary.source_lock_ref != receipt.source_lock_ref:
                raise ConcurrencyConflict(
                    "Boundary and receipt Source Lock identities differ."
                )
        if ratification is not None:
            self._assert_same_or_absent(
                self._atomicity_ratifications,
                ratification.ratification_id,
                ratification,
                "ratification",
            )
        if model is not None:
            self._assert_same_or_absent(
                self._draft_harness_models, model.model_id, model, "model"
            )
        if invalidation is not None:
            self._assert_same_or_absent(
                self._boundary_invalidations,
                invalidation.invalidation_id,
                invalidation,
                "invalidation",
            )
            if (
                invalidation.boundary_ref not in self._atomic_boundaries
                or invalidation.model_ref not in self._draft_harness_models
                or invalidation.boundary_ref in self._invalidated_boundaries
                or invalidation.model_ref in self._invalidated_models
            ):
                raise ConcurrencyConflict(
                    "Invalidation requires one active stored boundary and model.",
                    boundary_ref=invalidation.boundary_ref,
                    model_ref=invalidation.model_ref,
                )
        if harness_ir_invalidation is not None:
            self._assert_same_or_absent(
                self._harness_ir_invalidations,
                harness_ir_invalidation.invalidation_id,
                harness_ir_invalidation,
                "Harness IR invalidation",
            )
            if (
                harness_ir_invalidation.ir_ref not in self._harness_irs
                or harness_ir_invalidation.ir_ref in self._invalidated_harness_irs
                or invalidation is None
                or harness_ir_invalidation.upstream_invalidation_ref
                != invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Harness IR invalidation requires one active snapshot and its upstream invalidation.",
                    ir_ref=harness_ir_invalidation.ir_ref,
                )
        if artifact_set_invalidation is not None:
            self._assert_same_or_absent(
                self._artifact_set_invalidations,
                artifact_set_invalidation.invalidation_id,
                artifact_set_invalidation,
                "artifact-set invalidation",
            )
            manifest = self._artifact_manifests.get(
                artifact_set_invalidation.manifest_ref
            )
            if (
                manifest is None
                or manifest.artifact_set_id
                != artifact_set_invalidation.artifact_set_ref
                or manifest.ir_id != artifact_set_invalidation.ir_ref
                or artifact_set_invalidation.artifact_set_ref
                in self._invalidated_artifact_sets
                or harness_ir_invalidation is None
                or artifact_set_invalidation.upstream_invalidation_ref
                != harness_ir_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Artifact-set invalidation requires one active manifest and its Harness IR invalidation.",
                    artifact_set_ref=artifact_set_invalidation.artifact_set_ref,
                )
        if constitutional_validation_invalidation is not None:
            self._assert_same_or_absent(
                self._constitutional_validation_invalidations,
                constitutional_validation_invalidation.invalidation_id,
                constitutional_validation_invalidation,
                "constitutional validation invalidation",
            )
            report = self._constitutional_validation_reports.get(
                constitutional_validation_invalidation.report_ref
            )
            if (
                report is None
                or report.artifact_set_id
                != constitutional_validation_invalidation.artifact_set_ref
                or report.report_id in self._invalidated_constitutional_validations
                or artifact_set_invalidation is None
                or constitutional_validation_invalidation.upstream_invalidation_ref
                != artifact_set_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Constitutional invalidation requires one active report and its artifact-set invalidation.",
                    report_ref=constitutional_validation_invalidation.report_ref,
                )
        if capability_ownership_invalidation is not None:
            self._assert_same_or_absent(
                self._capability_ownership_invalidations,
                capability_ownership_invalidation.invalidation_id,
                capability_ownership_invalidation,
                "capability ownership invalidation",
            )
            graph = self._capability_ownership_graphs.get(
                capability_ownership_invalidation.graph_ref
            )
            if (
                graph is None
                or graph.constitutional_report_id
                != capability_ownership_invalidation.constitutional_report_ref
                or graph.graph_id in self._invalidated_capability_ownership_graphs
                or constitutional_validation_invalidation is None
                or capability_ownership_invalidation.upstream_invalidation_ref
                != constitutional_validation_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Capability invalidation requires one active graph and its constitutional invalidation.",
                    graph_ref=capability_ownership_invalidation.graph_ref,
                )
        if responsibility_module_invalidation is not None:
            self._assert_same_or_absent(
                self._responsibility_module_invalidations,
                responsibility_module_invalidation.invalidation_id,
                responsibility_module_invalidation,
                "responsibility module invalidation",
            )
            graph = self._responsibility_module_graphs.get(
                responsibility_module_invalidation.module_graph_ref
            )
            if (
                graph is None
                or graph.capability_graph_id
                != responsibility_module_invalidation.capability_graph_ref
                or graph.graph_id in self._invalidated_responsibility_module_graphs
                or capability_ownership_invalidation is None
                or responsibility_module_invalidation.upstream_invalidation_ref
                != capability_ownership_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Module invalidation requires one active graph and its capability invalidation.",
                    graph_ref=responsibility_module_invalidation.module_graph_ref,
                )
        if phase_graph_invalidation is not None:
            self._assert_same_or_absent(
                self._phase_graph_invalidations,
                phase_graph_invalidation.invalidation_id,
                phase_graph_invalidation,
                "phase graph invalidation",
            )
            graph = self._phase_graphs.get(phase_graph_invalidation.phase_graph_ref)
            if (
                graph is None
                or graph.module_graph_id != phase_graph_invalidation.module_graph_ref
                or graph.graph_id in self._invalidated_phase_graphs
                or responsibility_module_invalidation is None
                or phase_graph_invalidation.upstream_invalidation_ref
                != responsibility_module_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Phase invalidation requires one active graph and its module invalidation.",
                    graph_ref=phase_graph_invalidation.phase_graph_ref,
                )
        if phase_handoff_invalidation is not None:
            self._assert_same_or_absent(
                self._phase_handoff_invalidations,
                phase_handoff_invalidation.invalidation_id,
                phase_handoff_invalidation,
                "phase handoff invalidation",
            )
            graph = self._phase_handoff_graphs.get(
                phase_handoff_invalidation.handoff_graph_ref
            )
            affected = tuple(sorted(self._run_internal_handoffs.get(run_id, ())))
            if (
                graph is None
                or graph.phase_graph_id != phase_handoff_invalidation.phase_graph_ref
                or graph.graph_id in self._invalidated_phase_handoff_graphs
                or phase_graph_invalidation is None
                or phase_handoff_invalidation.upstream_invalidation_ref
                != phase_graph_invalidation.invalidation_id
                or phase_handoff_invalidation.affected_handoff_ids != affected
            ):
                raise ConcurrencyConflict(
                    "Handoff invalidation requires the exact active graph, affected handoffs, and Phase Graph invalidation.",
                    graph_ref=phase_handoff_invalidation.handoff_graph_ref,
                )
        if context_graph_invalidation is not None:
            self._assert_same_or_absent(
                self._context_graph_invalidations,
                context_graph_invalidation.invalidation_id,
                context_graph_invalidation,
                "minimum context invalidation",
            )
            context_graph = self._minimum_context_graphs.get(
                context_graph_invalidation.context_graph_ref
            )
            if (
                context_graph is None
                or context_graph.handoff_graph_id
                != context_graph_invalidation.handoff_graph_ref
                or context_graph.graph_id in self._invalidated_minimum_context_graphs
                or phase_handoff_invalidation is None
                or context_graph_invalidation.upstream_invalidation_ref
                != phase_handoff_invalidation.invalidation_id
                or context_graph_invalidation.affected_manifest_ids
                != tuple(sorted(item.manifest_id for item in context_graph.manifests))
            ):
                raise ConcurrencyConflict(
                    "Minimum context invalidation requires the exact active graph, manifests, and handoff invalidation.",
                    graph_ref=context_graph_invalidation.context_graph_ref,
                )
        if skill_registry_snapshot_invalidation is not None:
            self._assert_same_or_absent(
                self._skill_registry_snapshot_invalidations,
                skill_registry_snapshot_invalidation.invalidation_id,
                skill_registry_snapshot_invalidation,
                "skill registry snapshot invalidation",
            )
            snapshot = self._skill_registry_snapshots.get(
                skill_registry_snapshot_invalidation.snapshot_ref
            )
            if (
                snapshot is None
                or snapshot.minimum_context_graph_id
                != skill_registry_snapshot_invalidation.minimum_context_ref
                or snapshot.snapshot_id in self._invalidated_skill_registry_snapshots
                or context_graph_invalidation is None
                or skill_registry_snapshot_invalidation.upstream_invalidation_ref
                != context_graph_invalidation.invalidation_id
                or skill_registry_snapshot_invalidation.affected_capability_ids
                != snapshot.capability_ids
            ):
                raise ConcurrencyConflict(
                    "Skill snapshot invalidation requires the exact active snapshot and context invalidation.",
                    snapshot_ref=skill_registry_snapshot_invalidation.snapshot_ref,
                )
        if skill_necessity_invalidation is not None:
            self._assert_same_or_absent(
                self._skill_necessity_invalidations,
                skill_necessity_invalidation.invalidation_id,
                skill_necessity_invalidation,
                "skill necessity invalidation",
            )
            decision = self._skill_necessity_decisions.get(
                skill_necessity_invalidation.decision_ref
            )
            if (
                decision is None
                or decision.snapshot_id != skill_necessity_invalidation.snapshot_ref
                or decision.decision_id in self._invalidated_skill_necessity_decisions
                or skill_registry_snapshot_invalidation is None
                or skill_necessity_invalidation.upstream_invalidation_ref
                != skill_registry_snapshot_invalidation.invalidation_id
                or skill_necessity_invalidation.affected_capability_ids
                != decision.capability_ids
            ):
                raise ConcurrencyConflict(
                    "Skill necessity invalidation requires the exact active decision and snapshot invalidation.",
                    decision_ref=skill_necessity_invalidation.decision_ref,
                )
        if atomic_harness_definition_invalidation is not None:
            self._assert_same_or_absent(
                self._atomic_harness_definition_invalidations,
                atomic_harness_definition_invalidation.invalidation_id,
                atomic_harness_definition_invalidation,
                "Atomic Harness Definition invalidation",
            )
            definition = self._atomic_harness_definitions.get(
                atomic_harness_definition_invalidation.definition_ref
            )
            if (
                definition is None
                or definition.skill_necessity_decision_id
                != atomic_harness_definition_invalidation.necessity_decision_ref
                or definition.definition_id
                in self._invalidated_atomic_harness_definitions
                or skill_necessity_invalidation is None
                or atomic_harness_definition_invalidation.upstream_invalidation_ref
                != skill_necessity_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Definition invalidation requires the exact active definition and necessity invalidation.",
                    definition_ref=atomic_harness_definition_invalidation.definition_ref,
                )
        if atomic_content_harness_validation_invalidation is not None:
            self._assert_same_or_absent(
                self._atomic_content_harness_validation_invalidations,
                atomic_content_harness_validation_invalidation.invalidation_id,
                atomic_content_harness_validation_invalidation,
                "Atomic Content Harness validation invalidation",
            )
            report = self._atomic_content_harness_validation_reports.get(
                atomic_content_harness_validation_invalidation.report_ref
            )
            if (
                report is None
                or report.definition_id
                != atomic_content_harness_validation_invalidation.definition_ref
                or report.report_id
                in self._invalidated_atomic_content_harness_validations
                or atomic_harness_definition_invalidation is None
                or atomic_content_harness_validation_invalidation.upstream_invalidation_ref
                != atomic_harness_definition_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Target-validation invalidation requires the active report and definition invalidation.",
                    report_ref=atomic_content_harness_validation_invalidation.report_ref,
                )
        if development_capsule_invalidation is not None:
            self._assert_same_or_absent(
                self._development_capsule_invalidations,
                development_capsule_invalidation.invalidation_id,
                development_capsule_invalidation,
                "Development Capsule invalidation",
            )
            capsule = self._development_capsules.get(
                development_capsule_invalidation.capsule_ref
            )
            if (
                capsule is None
                or capsule.validation_id
                != development_capsule_invalidation.validation_ref
                or capsule.capsule_id in self._invalidated_development_capsules
                or atomic_content_harness_validation_invalidation is None
                or development_capsule_invalidation.upstream_invalidation_ref
                != atomic_content_harness_validation_invalidation.invalidation_id
            ):
                raise ConcurrencyConflict(
                    "Development Capsule invalidation requires the active capsule and target-validation invalidation.",
                    capsule_ref=development_capsule_invalidation.capsule_ref,
                )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the atomic commit.",
                run_id=run_id,
                receipt_id=receipt.receipt_id,
            )

        self._streams[run_id] = (*current, *events)
        if decision is not None:
            self._atomicity_decisions[run_id] = (
                *self._atomicity_decisions.get(run_id, ()),
                decision,
            )
        if boundary is not None:
            self._atomic_boundaries[boundary.boundary_id] = boundary
        if ratification is not None:
            self._atomicity_ratifications[ratification.ratification_id] = ratification
        if model is not None:
            self._draft_harness_models[model.model_id] = model
        if invalidation is not None:
            self._boundary_invalidations[invalidation.invalidation_id] = invalidation
            self._invalidated_boundaries[invalidation.boundary_ref] = (
                invalidation.invalidation_id
            )
            self._invalidated_models[invalidation.model_ref] = invalidation.invalidation_id
        if harness_ir_invalidation is not None:
            self._harness_ir_invalidations[
                harness_ir_invalidation.invalidation_id
            ] = harness_ir_invalidation
            self._invalidated_harness_irs[harness_ir_invalidation.ir_ref] = (
                harness_ir_invalidation.invalidation_id
            )
        if artifact_set_invalidation is not None:
            self._artifact_set_invalidations[
                artifact_set_invalidation.invalidation_id
            ] = artifact_set_invalidation
            self._invalidated_artifact_sets[
                artifact_set_invalidation.artifact_set_ref
            ] = artifact_set_invalidation.invalidation_id
        if constitutional_validation_invalidation is not None:
            self._constitutional_validation_invalidations[
                constitutional_validation_invalidation.invalidation_id
            ] = constitutional_validation_invalidation
            self._invalidated_constitutional_validations[
                constitutional_validation_invalidation.report_ref
            ] = constitutional_validation_invalidation.invalidation_id
        if capability_ownership_invalidation is not None:
            self._capability_ownership_invalidations[
                capability_ownership_invalidation.invalidation_id
            ] = capability_ownership_invalidation
            self._invalidated_capability_ownership_graphs[
                capability_ownership_invalidation.graph_ref
            ] = capability_ownership_invalidation.invalidation_id
        if responsibility_module_invalidation is not None:
            self._responsibility_module_invalidations[
                responsibility_module_invalidation.invalidation_id
            ] = responsibility_module_invalidation
            self._invalidated_responsibility_module_graphs[
                responsibility_module_invalidation.module_graph_ref
            ] = responsibility_module_invalidation.invalidation_id
        if phase_graph_invalidation is not None:
            self._phase_graph_invalidations[
                phase_graph_invalidation.invalidation_id
            ] = phase_graph_invalidation
            self._invalidated_phase_graphs[phase_graph_invalidation.phase_graph_ref] = (
                phase_graph_invalidation.invalidation_id
            )
        if phase_handoff_invalidation is not None:
            self._phase_handoff_invalidations[
                phase_handoff_invalidation.invalidation_id
            ] = phase_handoff_invalidation
            self._invalidated_phase_handoff_graphs[
                phase_handoff_invalidation.handoff_graph_ref
            ] = phase_handoff_invalidation.invalidation_id
        if context_graph_invalidation is not None:
            self._context_graph_invalidations[
                context_graph_invalidation.invalidation_id
            ] = context_graph_invalidation
            self._invalidated_minimum_context_graphs[
                context_graph_invalidation.context_graph_ref
            ] = context_graph_invalidation.invalidation_id
        if skill_registry_snapshot_invalidation is not None:
            self._skill_registry_snapshot_invalidations[
                skill_registry_snapshot_invalidation.invalidation_id
            ] = skill_registry_snapshot_invalidation
            self._invalidated_skill_registry_snapshots[
                skill_registry_snapshot_invalidation.snapshot_ref
            ] = skill_registry_snapshot_invalidation.invalidation_id
        if skill_necessity_invalidation is not None:
            self._skill_necessity_invalidations[
                skill_necessity_invalidation.invalidation_id
            ] = skill_necessity_invalidation
            self._invalidated_skill_necessity_decisions[
                skill_necessity_invalidation.decision_ref
            ] = skill_necessity_invalidation.invalidation_id
        if atomic_harness_definition_invalidation is not None:
            self._atomic_harness_definition_invalidations[
                atomic_harness_definition_invalidation.invalidation_id
            ] = atomic_harness_definition_invalidation
            self._invalidated_atomic_harness_definitions[
                atomic_harness_definition_invalidation.definition_ref
            ] = atomic_harness_definition_invalidation.invalidation_id
        if atomic_content_harness_validation_invalidation is not None:
            self._atomic_content_harness_validation_invalidations[
                atomic_content_harness_validation_invalidation.invalidation_id
            ] = atomic_content_harness_validation_invalidation
            self._invalidated_atomic_content_harness_validations[
                atomic_content_harness_validation_invalidation.report_ref
            ] = atomic_content_harness_validation_invalidation.invalidation_id
        if development_capsule_invalidation is not None:
            self._development_capsule_invalidations[
                development_capsule_invalidation.invalidation_id
            ] = development_capsule_invalidation
            self._invalidated_development_capsules[
                development_capsule_invalidation.capsule_ref
            ] = development_capsule_invalidation.invalidation_id
        self._atomicity_receipts[receipt.receipt_id] = receipt
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_artifact_set(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        manifest: ArtifactManifest,
        artifacts: tuple[GeneratedArtifact, ...],
        receipt: ArtifactSetCompilationReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        snapshot = self._harness_irs.get(manifest.ir_id)
        if (
            snapshot is None
            or manifest.run_id != run_id
            or manifest.ir_id in self._invalidated_harness_irs
        ):
            raise ConcurrencyConflict(
                "Artifact commit requires the active immutable Harness IR.",
                run_id=run_id,
                ir_id=manifest.ir_id,
            )
        if artifacts != manifest.artifacts:
            raise ConcurrencyConflict("Artifact commit payload differs from its manifest.")
        receipt.validate(manifest)
        manifest.validate(
            snapshot,
            _manifest_config(manifest),
        )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._artifact_manifests, manifest.manifest_id, manifest, "artifact manifest"
        )
        self._assert_same_or_absent(
            self._artifact_receipts, receipt.receipt_id, receipt, "artifact receipt"
        )
        if self._run_artifact_manifests.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has an artifact-set manifest.", run_id=run_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the artifact-set commit.",
                run_id=run_id,
                manifest_id=manifest.manifest_id,
            )
        self._streams[run_id] = (*current, *events)
        self._artifact_manifests[manifest.manifest_id] = manifest
        self._run_artifact_manifests[run_id] = (manifest.manifest_id,)
        self._artifact_manifest_artifacts[manifest.manifest_id] = artifacts
        self._artifact_receipts[receipt.receipt_id] = receipt
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_harness_ir(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        snapshot: HarnessIR,
        receipt: HarnessIRCompilationReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        if snapshot.run_id != run_id or receipt.run_id != run_id:
            raise ConcurrencyConflict("Harness IR artifacts belong to a different run.")
        if (
            receipt.ir_id != snapshot.ir_id
            or receipt.ir_hash != snapshot.ir_hash
            or receipt.upstream_refs != snapshot.upstream_refs
        ):
            raise ConcurrencyConflict("Harness IR receipt and snapshot identities differ.")
        if (
            snapshot.source_lock_ref not in self._source_locks
            or snapshot.boundary_ref not in self._atomic_boundaries
            or snapshot.ratification_ref not in self._atomicity_ratifications
            or snapshot.model_ref not in self._draft_harness_models
            or snapshot.boundary_ref in self._invalidated_boundaries
            or snapshot.model_ref in self._invalidated_models
        ):
            raise ConcurrencyConflict("Harness IR commit requires active stored upstream artifacts.")
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(self._harness_irs, snapshot.ir_id, snapshot, "Harness IR")
        self._assert_same_or_absent(
            self._harness_ir_receipts, receipt.receipt_id, receipt, "Harness IR receipt"
        )
        if self._run_harness_irs.get(run_id):
            raise ConcurrencyConflict(
                "The initial Harness IR revision already exists.",
                run_id=run_id,
                existing_refs=self._run_harness_irs[run_id],
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the Harness IR commit.",
                run_id=run_id,
                ir_id=snapshot.ir_id,
            )
        self._streams[run_id] = (*current, *events)
        self._harness_irs[snapshot.ir_id] = snapshot
        self._run_harness_irs[run_id] = (snapshot.ir_id,)
        self._harness_ir_receipts[receipt.receipt_id] = receipt
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_constitutional_validation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        report: ConstitutionalValidationReport,
        receipt: ConstitutionalValidationReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        report.validate()
        receipt.validate(report)
        manifest = self._artifact_manifests.get(report.manifest_id)
        if (
            manifest is None
            or manifest.run_id != run_id
            or manifest.artifact_set_id != report.artifact_set_id
            or manifest.manifest_hash != report.manifest_hash
            or manifest.ir_id != report.ir_id
            or manifest.ir_hash != report.ir_hash
            or report.artifact_set_id in self._invalidated_artifact_sets
            or report.ir_id in self._invalidated_harness_irs
        ):
            raise ConcurrencyConflict(
                "Constitutional validation commit requires the active exact artifact set.",
                run_id=run_id,
                report_id=report.report_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._constitutional_validation_reports,
            report.report_id,
            report,
            "constitutional validation report",
        )
        self._assert_same_or_absent(
            self._constitutional_validation_receipts,
            receipt.receipt_id,
            receipt,
            "constitutional validation receipt",
        )
        if self._run_constitutional_validation_reports.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has a constitutional validation report.",
                run_id=run_id,
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the constitutional validation commit.",
                run_id=run_id,
                report_id=report.report_id,
            )
        self._streams[run_id] = (*current, *events)
        self._constitutional_validation_reports[report.report_id] = report
        self._run_constitutional_validation_reports[run_id] = (report.report_id,)
        self._constitutional_validation_receipts[receipt.receipt_id] = receipt
        self._run_constitutional_validation_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_capability_ownership(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: CapabilityOwnershipGraph,
        receipt: CapabilityOwnershipReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        graph.validate()
        receipt.validate(graph)
        ir = self._harness_irs.get(graph.ir_id)
        report = self._constitutional_validation_reports.get(
            graph.constitutional_report_id
        )
        constitutional_receipt = self._constitutional_validation_receipts.get(
            graph.constitutional_receipt_id
        )
        if (
            ir is None
            or report is None
            or constitutional_receipt is None
            or graph.run_id != run_id
            or graph.ir_hash != ir.ir_hash
            or graph.artifact_set_id != report.artifact_set_id
            or graph.constitutional_report_hash != report.report_hash
            or graph.constitutional_receipt_hash
            != constitutional_receipt.receipt_hash
            or graph.ir_id in self._invalidated_harness_irs
            or graph.artifact_set_id in self._invalidated_artifact_sets
            or graph.constitutional_report_id
            in self._invalidated_constitutional_validations
        ):
            raise ConcurrencyConflict(
                "Capability ownership commit requires the exact active constitutional parent.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._capability_ownership_graphs,
            graph.graph_id,
            graph,
            "capability ownership graph",
        )
        self._assert_same_or_absent(
            self._capability_ownership_receipts,
            receipt.receipt_id,
            receipt,
            "capability ownership receipt",
        )
        if self._run_capability_ownership_graphs.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has a capability ownership graph.",
                run_id=run_id,
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the capability ownership commit.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        self._streams[run_id] = (*current, *events)
        self._capability_ownership_graphs[graph.graph_id] = graph
        self._run_capability_ownership_graphs[run_id] = (graph.graph_id,)
        self._capability_ownership_receipts[receipt.receipt_id] = receipt
        self._run_capability_ownership_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_responsibility_modules(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: ResponsibilityModuleGraph,
        receipt: ResponsibilityModuleReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        capability_graph = self._capability_ownership_graphs.get(
            graph.capability_graph_id
        )
        capability_receipts = self.capability_ownership_receipts(run_id)
        if capability_graph is None or len(capability_receipts) != 1:
            raise ConcurrencyConflict(
                "Module commit requires one active capability graph and receipt.",
                run_id=run_id,
            )
        capability_receipt = capability_receipts[0]
        capability_receipt.validate(capability_graph)
        graph.validate(capability_graph)
        receipt.validate(graph, capability_graph)
        if (
            graph.run_id != run_id
            or graph.capability_graph_hash != capability_graph.graph_hash
            or graph.capability_graph_id in self._invalidated_capability_ownership_graphs
            or graph.ir_id in self._invalidated_harness_irs
            or graph.constitutional_report_id
            in self._invalidated_constitutional_validations
        ):
            raise ConcurrencyConflict(
                "Module commit requires the exact active capability parent.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._responsibility_module_graphs,
            graph.graph_id,
            graph,
            "responsibility module graph",
        )
        self._assert_same_or_absent(
            self._responsibility_module_receipts,
            receipt.receipt_id,
            receipt,
            "responsibility module receipt",
        )
        if self._run_responsibility_module_graphs.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has a responsibility module graph.",
                run_id=run_id,
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the module commit.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        self._streams[run_id] = (*current, *events)
        self._responsibility_module_graphs[graph.graph_id] = graph
        self._run_responsibility_module_graphs[run_id] = (graph.graph_id,)
        self._responsibility_module_receipts[receipt.receipt_id] = receipt
        self._run_responsibility_module_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_phase_graph(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: PhaseGraph,
        receipt: PhaseGraphReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        module_graph = self._responsibility_module_graphs.get(graph.module_graph_id)
        module_receipts = self.responsibility_module_receipts(run_id)
        capability_graph = self._capability_ownership_graphs.get(
            graph.capability_graph_id
        )
        if (
            module_graph is None
            or capability_graph is None
            or len(module_receipts) != 1
        ):
            raise ConcurrencyConflict(
                "Phase commit requires one active module graph and receipt.",
                run_id=run_id,
            )
        module_receipts[0].validate(module_graph, capability_graph)
        graph.validate(module_graph)
        receipt.validate(graph, module_graph)
        if (
            graph.run_id != run_id
            or graph.module_graph_hash != module_graph.graph_hash
            or graph.module_graph_id in self._invalidated_responsibility_module_graphs
            or graph.capability_graph_id in self._invalidated_capability_ownership_graphs
            or graph.ir_id in self._invalidated_harness_irs
        ):
            raise ConcurrencyConflict(
                "Phase commit requires the exact active module parent.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._phase_graphs, graph.graph_id, graph, "phase graph"
        )
        self._assert_same_or_absent(
            self._phase_graph_receipts,
            receipt.receipt_id,
            receipt,
            "phase graph receipt",
        )
        if self._run_phase_graphs.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has a Phase Graph.", run_id=run_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the Phase Graph commit.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        self._streams[run_id] = (*current, *events)
        self._phase_graphs[graph.graph_id] = graph
        self._run_phase_graphs[run_id] = (graph.graph_id,)
        self._phase_graph_receipts[receipt.receipt_id] = receipt
        self._run_phase_graph_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_phase_handoffs(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: PhaseHandoffGraph,
        receipt: PhaseHandoffReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        phase_graph = self._phase_graphs.get(graph.phase_graph_id)
        phase_receipts = self.phase_graph_receipts(run_id)
        if phase_graph is None or len(phase_receipts) != 1:
            raise ConcurrencyConflict(
                "Handoff commit requires one active Phase Graph and receipt.", run_id=run_id
            )
        module_graph = self._responsibility_module_graphs.get(phase_graph.module_graph_id)
        if module_graph is None:
            raise ConcurrencyConflict("Handoff commit Phase Graph lineage is unavailable.")
        phase_graph.validate(module_graph)
        phase_receipts[0].validate(phase_graph, module_graph)
        graph.validate(phase_graph)
        receipt.validate(graph, phase_graph)
        if (
            graph.run_id != run_id
            or graph.phase_graph_hash != phase_graph.graph_hash
            or graph.phase_graph_id in self._invalidated_phase_graphs
            or graph.module_graph_id in self._invalidated_responsibility_module_graphs
            or graph.ir_id in self._invalidated_harness_irs
        ):
            raise ConcurrencyConflict(
                "Handoff commit requires the exact active Phase Graph parent.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._phase_handoff_graphs, graph.graph_id, graph, "phase handoff graph"
        )
        self._assert_same_or_absent(
            self._phase_handoff_receipts,
            receipt.receipt_id,
            receipt,
            "phase handoff receipt",
        )
        if self._run_phase_handoff_graphs.get(run_id):
            raise ConcurrencyConflict(
                "The active run already has an internal handoff graph.", run_id=run_id
            )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the handoff graph commit.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        self._streams[run_id] = (*current, *events)
        self._phase_handoff_graphs[graph.graph_id] = graph
        self._run_phase_handoff_graphs[run_id] = (graph.graph_id,)
        self._phase_handoff_receipts[receipt.receipt_id] = receipt
        self._run_phase_handoff_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_internal_handoff(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        handoff: InternalHandoff,
        receipt: InternalHandoffReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        graph = self._phase_handoff_graphs.get(handoff.handoff_graph_id)
        phase_graph = self._phase_graphs.get(graph.phase_graph_id if graph else "")
        if graph is None or phase_graph is None:
            raise ConcurrencyConflict("Internal handoff graph lineage is unavailable.")
        handoff.validate(graph, phase_graph)
        receipt.validate(handoff, None)
        if (
            handoff.run_id != run_id
            or graph.graph_id in self._invalidated_phase_handoff_graphs
            or phase_graph.graph_id in self._invalidated_phase_graphs
            or self._run_internal_handoffs.get(run_id)
        ):
            raise ConcurrencyConflict("Only one active governed internal handoff may be issued.")
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._internal_handoffs, handoff.handoff_id, handoff, "internal handoff"
        )
        self._assert_same_or_absent(
            self._internal_handoff_receipts,
            receipt.receipt_id,
            receipt,
            "internal handoff receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected internal handoff issuance.",
                run_id=run_id,
            )
        self._streams[run_id] = (*current, *events)
        self._internal_handoffs[handoff.handoff_id] = handoff
        self._run_internal_handoffs[run_id] = (handoff.handoff_id,)
        self._internal_handoff_receipts[receipt.receipt_id] = receipt
        self._run_internal_handoff_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_internal_handoff_decision(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        handoff: InternalHandoff,
        decision: InternalHandoffDecision,
        receipt: InternalHandoffReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        stored = self._internal_handoffs.get(handoff.handoff_id)
        graph = self._phase_handoff_graphs.get(handoff.handoff_graph_id)
        phase_graph = self._phase_graphs.get(graph.phase_graph_id if graph else "")
        receiver = next(
            (
                item
                for item in (phase_graph.phases if phase_graph else ())
                if item.phase_id == handoff.receiver_phase
            ),
            None,
        )
        if stored != handoff or graph is None or phase_graph is None or receiver is None:
            raise ConcurrencyConflict("The internal handoff decision lineage is unavailable.")
        handoff.validate(graph, phase_graph)
        decision.validate(handoff, receiver.failure_owner)
        receipt.validate(handoff, decision)
        if (
            graph.graph_id in self._invalidated_phase_handoff_graphs
            or handoff.handoff_id in self._internal_handoff_decisions
        ):
            raise ConcurrencyConflict("The handoff is invalidated or already decided.")
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._internal_handoff_receipts,
            receipt.receipt_id,
            receipt,
            "internal handoff decision receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the handoff decision.",
                run_id=run_id,
            )
        self._streams[run_id] = (*current, *events)
        self._internal_handoff_decisions[handoff.handoff_id] = decision
        self._internal_handoff_receipts[receipt.receipt_id] = receipt
        self._run_internal_handoff_receipts[run_id] = (
            *self._run_internal_handoff_receipts.get(run_id, ()),
            receipt.receipt_id,
        )
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_minimum_context(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        graph: MinimumCompleteContextGraph,
        receipt: ContextCompilationReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        handoff_graph = self._phase_handoff_graphs.get(graph.handoff_graph_id)
        phase_graph = self._phase_graphs.get(graph.phase_graph_id)
        handoff = self._internal_handoffs.get(graph.accepted_handoff_id)
        decision = self._internal_handoff_decisions.get(graph.accepted_handoff_id)
        if handoff_graph is None or phase_graph is None or handoff is None or decision is None:
            raise ConcurrencyConflict(
                "Minimum context commit requires the active accepted internal handoff.",
                run_id=run_id,
            )
        graph.validate(handoff_graph, phase_graph, handoff, decision)
        receipt.validate(graph)
        if (
            graph.run_id != run_id
            or handoff_graph.graph_id in self._invalidated_phase_handoff_graphs
            or phase_graph.graph_id in self._invalidated_phase_graphs
            or self._run_minimum_context_graphs.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Minimum context commit requires one exact active handoff parent.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._minimum_context_graphs, graph.graph_id, graph, "minimum context graph"
        )
        self._assert_same_or_absent(
            self._context_compilation_receipts,
            receipt.receipt_id,
            receipt,
            "context compilation receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the minimum context commit.",
                run_id=run_id,
                graph_id=graph.graph_id,
            )
        self._streams[run_id] = (*current, *events)
        self._minimum_context_graphs[graph.graph_id] = graph
        self._run_minimum_context_graphs[run_id] = (graph.graph_id,)
        self._context_compilation_receipts[receipt.receipt_id] = receipt
        self._run_context_compilation_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_skill_registry_snapshot(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        snapshot: SyntheticSkillRegistrySnapshot,
        receipt: SkillRegistryConsumptionReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        context = self._minimum_context_graphs.get(
            snapshot.minimum_context_graph_id
        )
        if context is None:
            raise ConcurrencyConflict(
                "Skill snapshot commit requires the active Minimum Complete Context.",
                run_id=run_id,
            )
        snapshot.validate(context)
        receipt.validate(snapshot)
        if (
            snapshot.run_id != run_id
            or context.graph_id in self._invalidated_minimum_context_graphs
            or self._run_skill_registry_snapshots.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Skill snapshot commit requires one exact active context parent.",
                run_id=run_id,
                snapshot_id=snapshot.snapshot_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._skill_registry_snapshots,
            snapshot.snapshot_id,
            snapshot,
            "skill registry snapshot",
        )
        self._assert_same_or_absent(
            self._skill_registry_consumption_receipts,
            receipt.receipt_id,
            receipt,
            "skill registry consumption receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the skill snapshot commit.",
                run_id=run_id,
                snapshot_id=snapshot.snapshot_id,
            )
        self._streams[run_id] = (*current, *events)
        self._skill_registry_snapshots[snapshot.snapshot_id] = snapshot
        self._run_skill_registry_snapshots[run_id] = (snapshot.snapshot_id,)
        self._skill_registry_consumption_receipts[receipt.receipt_id] = receipt
        self._run_skill_registry_consumption_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_skill_necessity(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        decision: SkillNecessityDecision,
        receipt: SkillNecessityReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        snapshot = self._skill_registry_snapshots.get(decision.snapshot_id)
        context = self._minimum_context_graphs.get(decision.minimum_context_graph_id)
        if snapshot is None or context is None:
            raise ConcurrencyConflict(
                "Skill necessity commit requires the exact active snapshot and context.",
                run_id=run_id,
            )
        decision.validate(snapshot, context)
        receipt.validate(decision)
        if (
            decision.run_id != run_id
            or snapshot.snapshot_id in self._invalidated_skill_registry_snapshots
            or context.graph_id in self._invalidated_minimum_context_graphs
            or self._run_skill_necessity_decisions.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Skill necessity commit requires one active immutable parent chain.",
                run_id=run_id,
                decision_id=decision.decision_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._skill_necessity_decisions,
            decision.decision_id,
            decision,
            "skill necessity decision",
        )
        self._assert_same_or_absent(
            self._skill_necessity_receipts,
            receipt.receipt_id,
            receipt,
            "skill necessity receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the skill necessity commit.",
                run_id=run_id,
                decision_id=decision.decision_id,
            )
        self._streams[run_id] = (*current, *events)
        self._skill_necessity_decisions[decision.decision_id] = decision
        self._run_skill_necessity_decisions[run_id] = (decision.decision_id,)
        self._skill_necessity_receipts[receipt.receipt_id] = receipt
        self._run_skill_necessity_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_atomic_harness_definition(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        definition: AtomicHarnessDefinition,
        receipt: AtomicHarnessDefinitionReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        run = Run.replay(current)
        source_lock = self._source_locks.get(definition.source_lock_ref)
        boundary = self._atomic_boundaries.get(definition.boundary_ref)
        ratification = self._atomicity_ratifications.get(definition.ratification_ref)
        model = self._draft_harness_models.get(definition.model_ref)
        ir = self._harness_irs.get(definition.ir_id)
        manifest = self._artifact_manifests.get(definition.artifact_manifest_id)
        constitutional = self._constitutional_validation_reports.get(
            definition.constitutional_report_id
        )
        capability = self._capability_ownership_graphs.get(definition.capability_graph_id)
        modules = self._responsibility_module_graphs.get(definition.module_graph_id)
        phases = self._phase_graphs.get(definition.phase_graph_id)
        handoff_graph = self._phase_handoff_graphs.get(definition.handoff_graph_id)
        handoff = self._internal_handoffs.get(definition.accepted_handoff_id)
        context = self._minimum_context_graphs.get(definition.minimum_context_graph_id)
        snapshot = self._skill_registry_snapshots.get(definition.skill_snapshot_id)
        necessity = self._skill_necessity_decisions.get(
            definition.skill_necessity_decision_id
        )
        handoff_decision = (
            self._internal_handoff_decisions.get(context.accepted_handoff_id)
            if context is not None
            else None
        )
        required = (
            source_lock, boundary, ratification, model, ir, manifest,
            constitutional, capability, modules, phases, handoff_graph,
            handoff, handoff_decision, context, snapshot, necessity,
        )
        if any(item is None for item in required):
            raise ConcurrencyConflict(
                "Definition commit requires the complete active governed lineage.",
                run_id=run_id,
            )
        definition.validate(
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
            accepted_handoff=handoff,
            handoff_decision=handoff_decision,
            context=context,
            snapshot=snapshot,
            necessity=necessity,
        )
        receipt.validate(definition)
        invalidated = (
            definition.source_lock_ref != run.source_lock_ref
            or definition.boundary_ref in self._invalidated_boundaries
            or definition.model_ref in self._invalidated_models
            or definition.ir_id in self._invalidated_harness_irs
            or definition.artifact_set_id in self._invalidated_artifact_sets
            or definition.constitutional_report_id
            in self._invalidated_constitutional_validations
            or definition.capability_graph_id
            in self._invalidated_capability_ownership_graphs
            or definition.module_graph_id
            in self._invalidated_responsibility_module_graphs
            or definition.phase_graph_id in self._invalidated_phase_graphs
            or definition.handoff_graph_id in self._invalidated_phase_handoff_graphs
            or definition.minimum_context_graph_id
            in self._invalidated_minimum_context_graphs
            or definition.skill_snapshot_id in self._invalidated_skill_registry_snapshots
            or definition.skill_necessity_decision_id
            in self._invalidated_skill_necessity_decisions
        )
        if (
            definition.run_id != run_id
            or invalidated
            or self._run_atomic_harness_definitions.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Definition commit requires one active immutable parent chain.",
                run_id=run_id,
                definition_id=definition.definition_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._atomic_harness_definitions,
            definition.definition_id,
            definition,
            "Atomic Harness Definition",
        )
        self._assert_same_or_absent(
            self._atomic_harness_definition_receipts,
            receipt.receipt_id,
            receipt,
            "Atomic Harness Definition receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected the definition commit.",
                run_id=run_id,
                definition_id=definition.definition_id,
            )
        self._streams[run_id] = (*current, *events)
        self._atomic_harness_definitions[definition.definition_id] = definition
        self._run_atomic_harness_definitions[run_id] = (definition.definition_id,)
        self._atomic_harness_definition_receipts[receipt.receipt_id] = receipt
        self._run_atomic_harness_definition_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @_synchronized
    def commit_atomic_content_harness_validation(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        report: AtomicContentHarnessValidationReport,
        receipt: AtomicContentHarnessValidationReceipt,
        observations: tuple[Observation, ...],
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        run = Run.replay(current)
        definition = self._atomic_harness_definitions.get(report.definition_id)
        if definition is None:
            raise ConcurrencyConflict(
                "Target validation requires the exact stored Atomic Harness Definition.",
                run_id=run_id,
                definition_id=report.definition_id,
            )
        self._validate_definition_authority(run, definition)
        report.validate(definition)
        receipt.validate(report)
        if (
            len(observations) != 10
            or any(item.command_id != command_id for item in observations)
            or any(
                item.atomic_content_harness_validation_receipt_id
                != receipt.receipt_id
                for item in observations
            )
        ):
            raise ConcurrencyConflict(
                "Target-validation observation intents are incomplete or mismatched.",
                run_id=run_id,
                command_id=command_id,
            )
        if (
            report.run_id != run_id
            or run.atomic_harness_definition_ref != definition.definition_id
            or run.atomic_harness_definition_hash != definition.definition_hash
            or definition.definition_id in self._invalidated_atomic_harness_definitions
            or self._run_atomic_content_harness_validation_reports.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Target validation requires one active immutable definition parent.",
                run_id=run_id,
                report_id=report.report_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._atomic_content_harness_validation_reports,
            report.report_id,
            report,
            "Atomic Content Harness validation report",
        )
        self._assert_same_or_absent(
            self._atomic_content_harness_validation_receipts,
            receipt.receipt_id,
            receipt,
            "Atomic Content Harness validation receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected target validation.",
                run_id=run_id,
                report_id=report.report_id,
            )
        self._streams[run_id] = (*current, *events)
        self._atomic_content_harness_validation_reports[report.report_id] = report
        self._run_atomic_content_harness_validation_reports[run_id] = (
            report.report_id,
        )
        self._atomic_content_harness_validation_receipts[receipt.receipt_id] = receipt
        self._run_atomic_content_harness_validation_receipts[run_id] = (
            receipt.receipt_id,
        )
        self._command_records[command_id] = command_record
        self._pending_observation_outbox[command_id] = observations
        self._delivered_observation_outbox[command_id] = ()

    @_synchronized
    def claim_pending_observation(self, command_id: str) -> Observation | None:
        if command_id in self._inflight_observation_outbox:
            return None
        pending = self._pending_observation_outbox.get(command_id, ())
        if not pending:
            return None
        observation = pending[0]
        self._inflight_observation_outbox[command_id] = observation
        return observation

    @_synchronized
    def complete_observation_delivery(
        self, command_id: str, observation: Observation
    ) -> None:
        inflight = self._inflight_observation_outbox.get(command_id)
        pending = self._pending_observation_outbox.get(command_id, ())
        if inflight != observation or not pending or pending[0] != observation:
            raise ConcurrencyConflict(
                "Observation delivery acknowledgement does not match the claimed intent.",
                command_id=command_id,
            )
        delivered = self._delivered_observation_outbox.get(command_id, ())
        if observation in delivered:
            raise ConcurrencyConflict(
                "An observation intent cannot be acknowledged twice.",
                command_id=command_id,
            )
        self._pending_observation_outbox[command_id] = pending[1:]
        self._delivered_observation_outbox[command_id] = (*delivered, observation)
        del self._inflight_observation_outbox[command_id]

    @_synchronized
    def release_observation_delivery(
        self, command_id: str, observation: Observation
    ) -> None:
        if self._inflight_observation_outbox.get(command_id) != observation:
            raise ConcurrencyConflict(
                "Only the claimed observation intent may be released.",
                command_id=command_id,
            )
        del self._inflight_observation_outbox[command_id]

    @_synchronized
    def pending_observations(self, command_id: str) -> tuple[Observation, ...]:
        return self._pending_observation_outbox.get(command_id, ())

    @_synchronized
    def delivered_observations(self, command_id: str) -> tuple[Observation, ...]:
        return self._delivered_observation_outbox.get(command_id, ())

    @_synchronized
    def commit_development_capsule(
        self,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
        command_id: str,
        command_record: CommandRecord,
        capsule: VersionedTraceableDevelopmentCapsule,
        receipt: DevelopmentCapsuleReceipt,
    ) -> None:
        current = self._validated_append(run_id, expected_version, events)
        run = Run.replay(current)
        definition = self._atomic_harness_definitions.get(capsule.definition_id)
        validation = self._atomic_content_harness_validation_reports.get(
            capsule.validation_id
        )
        if definition is None or validation is None:
            raise ConcurrencyConflict(
                "Development Capsule requires the exact stored definition and validation.",
                run_id=run_id,
                capsule_id=capsule.capsule_id,
            )
        capsule.validate(definition, validation)
        receipt.validate(capsule)
        if (
            capsule.run_id != run_id
            or run.atomic_content_harness_validation_ref != validation.report_id
            or run.atomic_content_harness_validation_hash != validation.report_hash
            or definition.definition_id in self._invalidated_atomic_harness_definitions
            or validation.report_id
            in self._invalidated_atomic_content_harness_validations
            or self._run_development_capsules.get(run_id)
        ):
            raise ConcurrencyConflict(
                "Development Capsule requires one active immutable validated parent chain.",
                run_id=run_id,
                capsule_id=capsule.capsule_id,
            )
        existing_record = self._command_records.get(command_id)
        if existing_record is not None and existing_record != command_record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._assert_same_or_absent(
            self._development_capsules,
            capsule.capsule_id,
            capsule,
            "Development Capsule",
        )
        self._assert_same_or_absent(
            self._development_capsule_receipts,
            receipt.receipt_id,
            receipt,
            "Development Capsule receipt",
        )
        if self._fail_next_atomic_commit:
            self._fail_next_atomic_commit = False
            raise AtomicCommitFailed(
                "Injected development/test failure rejected Development Capsule generation.",
                run_id=run_id,
                capsule_id=capsule.capsule_id,
            )
        self._streams[run_id] = (*current, *events)
        self._development_capsules[capsule.capsule_id] = capsule
        self._run_development_capsules[run_id] = (capsule.capsule_id,)
        self._development_capsule_receipts[receipt.receipt_id] = receipt
        self._run_development_capsule_receipts[run_id] = (receipt.receipt_id,)
        self._command_records[command_id] = command_record

    @staticmethod
    def _assert_same_or_absent(
        values: dict[str, object], key: str, value: object, artifact: str
    ) -> None:
        existing = values.get(key)
        if existing is not None and existing != value:
            raise ConcurrencyConflict(
                f"An immutable {artifact} identity cannot be overwritten.",
                artifact=artifact,
                artifact_id=key,
            )

    def get_atomic_boundary(self, boundary_id: str) -> DeclaredAtomicBoundary | None:
        return self._atomic_boundaries.get(boundary_id)

    def get_atomicity_ratification(
        self, ratification_id: str
    ) -> AtomicityRatification | None:
        return self._atomicity_ratifications.get(ratification_id)

    def get_draft_harness_model(self, model_id: str) -> DraftHarnessModel | None:
        return self._draft_harness_models.get(model_id)

    def get_atomicity_receipt(
        self, receipt_id: str
    ) -> AtomicityDecisionReceipt | None:
        return self._atomicity_receipts.get(receipt_id)

    def get_boundary_invalidation(
        self, invalidation_id: str
    ) -> BoundaryInvalidation | None:
        return self._boundary_invalidations.get(invalidation_id)

    def atomicity_decisions(self, run_id: str) -> tuple[AtomicityDecision, ...]:
        return self._atomicity_decisions.get(run_id, ())

    def is_boundary_invalidated(self, boundary_id: str) -> bool:
        return boundary_id in self._invalidated_boundaries

    def is_model_invalidated(self, model_id: str) -> bool:
        return model_id in self._invalidated_models

    def get_harness_ir(self, ir_id: str) -> HarnessIR | None:
        return self._harness_irs.get(ir_id)

    def get_harness_ir_receipt(
        self, receipt_id: str
    ) -> HarnessIRCompilationReceipt | None:
        return self._harness_ir_receipts.get(receipt_id)

    def harness_irs(self, run_id: str) -> tuple[HarnessIR, ...]:
        return tuple(
            self._harness_irs[ir_id]
            for ir_id in self._run_harness_irs.get(run_id, ())
        )

    def get_harness_ir_invalidation(
        self, invalidation_id: str
    ) -> HarnessIRInvalidation | None:
        return self._harness_ir_invalidations.get(invalidation_id)

    def is_harness_ir_invalidated(self, ir_id: str) -> bool:
        return ir_id in self._invalidated_harness_irs

    def get_artifact_manifest(self, manifest_id: str) -> ArtifactManifest | None:
        return self._artifact_manifests.get(manifest_id)

    def artifacts_for_manifest(self, manifest_id: str) -> tuple[GeneratedArtifact, ...]:
        return self._artifact_manifest_artifacts.get(manifest_id, ())

    def artifact_manifests(self, run_id: str) -> tuple[ArtifactManifest, ...]:
        return tuple(
            self._artifact_manifests[manifest_id]
            for manifest_id in self._run_artifact_manifests.get(run_id, ())
        )

    def get_artifact_receipt(
        self, receipt_id: str
    ) -> ArtifactSetCompilationReceipt | None:
        return self._artifact_receipts.get(receipt_id)

    def get_artifact_set_invalidation(
        self, invalidation_id: str
    ) -> ArtifactSetInvalidation | None:
        return self._artifact_set_invalidations.get(invalidation_id)

    def is_artifact_set_invalidated(self, artifact_set_id: str) -> bool:
        return artifact_set_id in self._invalidated_artifact_sets

    def save_artifact_drift_report(self, report: ArtifactDriftReport) -> None:
        if report.manifest_id not in self._artifact_manifests:
            raise ConcurrencyConflict(
                "Drift evidence requires a stored artifact manifest.",
                manifest_id=report.manifest_id,
            )
        self._assert_same_or_absent(
            self._artifact_drift_reports, report.report_id, report, "artifact drift report"
        )
        self._artifact_drift_reports[report.report_id] = report

    def get_artifact_drift_report(
        self, report_id: str
    ) -> ArtifactDriftReport | None:
        return self._artifact_drift_reports.get(report_id)

    def get_constitutional_validation_report(
        self, report_id: str
    ) -> ConstitutionalValidationReport | None:
        return self._constitutional_validation_reports.get(report_id)

    def constitutional_validation_reports(
        self, run_id: str
    ) -> tuple[ConstitutionalValidationReport, ...]:
        return tuple(
            self._constitutional_validation_reports[report_id]
            for report_id in self._run_constitutional_validation_reports.get(run_id, ())
        )

    def get_constitutional_validation_receipt(
        self, receipt_id: str
    ) -> ConstitutionalValidationReceipt | None:
        return self._constitutional_validation_receipts.get(receipt_id)

    def constitutional_validation_receipts(
        self, run_id: str
    ) -> tuple[ConstitutionalValidationReceipt, ...]:
        return tuple(
            self._constitutional_validation_receipts[receipt_id]
            for receipt_id in self._run_constitutional_validation_receipts.get(
                run_id, ()
            )
        )

    def get_constitutional_validation_invalidation(
        self, invalidation_id: str
    ) -> ConstitutionalValidationInvalidation | None:
        return self._constitutional_validation_invalidations.get(invalidation_id)

    def is_constitutional_validation_invalidated(self, report_id: str) -> bool:
        return report_id in self._invalidated_constitutional_validations

    def get_capability_ownership_graph(
        self, graph_id: str
    ) -> CapabilityOwnershipGraph | None:
        return self._capability_ownership_graphs.get(graph_id)

    def capability_ownership_graphs(
        self, run_id: str
    ) -> tuple[CapabilityOwnershipGraph, ...]:
        return tuple(
            self._capability_ownership_graphs[graph_id]
            for graph_id in self._run_capability_ownership_graphs.get(run_id, ())
        )

    def get_capability_ownership_receipt(
        self, receipt_id: str
    ) -> CapabilityOwnershipReceipt | None:
        return self._capability_ownership_receipts.get(receipt_id)

    def capability_ownership_receipts(
        self, run_id: str
    ) -> tuple[CapabilityOwnershipReceipt, ...]:
        return tuple(
            self._capability_ownership_receipts[receipt_id]
            for receipt_id in self._run_capability_ownership_receipts.get(run_id, ())
        )

    def get_capability_ownership_invalidation(
        self, invalidation_id: str
    ) -> CapabilityOwnershipInvalidation | None:
        return self._capability_ownership_invalidations.get(invalidation_id)

    def is_capability_ownership_invalidated(self, graph_id: str) -> bool:
        return graph_id in self._invalidated_capability_ownership_graphs

    def get_responsibility_module_graph(
        self, graph_id: str
    ) -> ResponsibilityModuleGraph | None:
        return self._responsibility_module_graphs.get(graph_id)

    def responsibility_module_graphs(
        self, run_id: str
    ) -> tuple[ResponsibilityModuleGraph, ...]:
        return tuple(
            self._responsibility_module_graphs[graph_id]
            for graph_id in self._run_responsibility_module_graphs.get(run_id, ())
        )

    def get_responsibility_module_receipt(
        self, receipt_id: str
    ) -> ResponsibilityModuleReceipt | None:
        return self._responsibility_module_receipts.get(receipt_id)

    def responsibility_module_receipts(
        self, run_id: str
    ) -> tuple[ResponsibilityModuleReceipt, ...]:
        return tuple(
            self._responsibility_module_receipts[receipt_id]
            for receipt_id in self._run_responsibility_module_receipts.get(run_id, ())
        )

    def get_responsibility_module_invalidation(
        self, invalidation_id: str
    ) -> ResponsibilityModuleInvalidation | None:
        return self._responsibility_module_invalidations.get(invalidation_id)

    def is_responsibility_module_invalidated(self, graph_id: str) -> bool:
        return graph_id in self._invalidated_responsibility_module_graphs

    def get_phase_graph(self, graph_id: str) -> PhaseGraph | None:
        return self._phase_graphs.get(graph_id)

    def phase_graphs(self, run_id: str) -> tuple[PhaseGraph, ...]:
        return tuple(
            self._phase_graphs[graph_id]
            for graph_id in self._run_phase_graphs.get(run_id, ())
        )

    def get_phase_graph_receipt(self, receipt_id: str) -> PhaseGraphReceipt | None:
        return self._phase_graph_receipts.get(receipt_id)

    def phase_graph_receipts(self, run_id: str) -> tuple[PhaseGraphReceipt, ...]:
        return tuple(
            self._phase_graph_receipts[receipt_id]
            for receipt_id in self._run_phase_graph_receipts.get(run_id, ())
        )

    def get_phase_graph_invalidation(
        self, invalidation_id: str
    ) -> PhaseGraphInvalidation | None:
        return self._phase_graph_invalidations.get(invalidation_id)

    def is_phase_graph_invalidated(self, graph_id: str) -> bool:
        return graph_id in self._invalidated_phase_graphs

    def get_phase_handoff_graph(self, graph_id: str) -> PhaseHandoffGraph | None:
        return self._phase_handoff_graphs.get(graph_id)

    def phase_handoff_graphs(self, run_id: str) -> tuple[PhaseHandoffGraph, ...]:
        return tuple(
            self._phase_handoff_graphs[graph_id]
            for graph_id in self._run_phase_handoff_graphs.get(run_id, ())
        )

    def get_phase_handoff_receipt(
        self, receipt_id: str
    ) -> PhaseHandoffReceipt | None:
        return self._phase_handoff_receipts.get(receipt_id)

    def phase_handoff_receipts(self, run_id: str) -> tuple[PhaseHandoffReceipt, ...]:
        return tuple(
            self._phase_handoff_receipts[receipt_id]
            for receipt_id in self._run_phase_handoff_receipts.get(run_id, ())
        )

    def get_internal_handoff(self, handoff_id: str) -> InternalHandoff | None:
        return self._internal_handoffs.get(handoff_id)

    def internal_handoffs(self, run_id: str) -> tuple[InternalHandoff, ...]:
        return tuple(
            self._internal_handoffs[handoff_id]
            for handoff_id in self._run_internal_handoffs.get(run_id, ())
        )

    def get_internal_handoff_decision(
        self, handoff_id: str
    ) -> InternalHandoffDecision | None:
        return self._internal_handoff_decisions.get(handoff_id)

    def internal_handoff_receipts(
        self, run_id: str
    ) -> tuple[InternalHandoffReceipt, ...]:
        return tuple(
            self._internal_handoff_receipts[receipt_id]
            for receipt_id in self._run_internal_handoff_receipts.get(run_id, ())
        )

    def get_phase_handoff_invalidation(
        self, invalidation_id: str
    ) -> PhaseHandoffInvalidation | None:
        return self._phase_handoff_invalidations.get(invalidation_id)

    def is_phase_handoff_invalidated(self, graph_id: str) -> bool:
        return graph_id in self._invalidated_phase_handoff_graphs

    def is_internal_handoff_invalidated(self, handoff_id: str) -> bool:
        handoff = self._internal_handoffs.get(handoff_id)
        return handoff is not None and handoff.handoff_graph_id in self._invalidated_phase_handoff_graphs

    def get_minimum_context_graph(
        self, graph_id: str
    ) -> MinimumCompleteContextGraph | None:
        return self._minimum_context_graphs.get(graph_id)

    def minimum_context_graphs(
        self, run_id: str
    ) -> tuple[MinimumCompleteContextGraph, ...]:
        return tuple(
            self._minimum_context_graphs[graph_id]
            for graph_id in self._run_minimum_context_graphs.get(run_id, ())
        )

    def get_context_compilation_receipt(
        self, receipt_id: str
    ) -> ContextCompilationReceipt | None:
        return self._context_compilation_receipts.get(receipt_id)

    def context_compilation_receipts(
        self, run_id: str
    ) -> tuple[ContextCompilationReceipt, ...]:
        return tuple(
            self._context_compilation_receipts[receipt_id]
            for receipt_id in self._run_context_compilation_receipts.get(run_id, ())
        )

    def get_context_graph_invalidation(
        self, invalidation_id: str
    ) -> ContextGraphInvalidation | None:
        return self._context_graph_invalidations.get(invalidation_id)

    def is_minimum_context_invalidated(self, graph_id: str) -> bool:
        return graph_id in self._invalidated_minimum_context_graphs

    def get_skill_registry_snapshot(
        self, snapshot_id: str
    ) -> SyntheticSkillRegistrySnapshot | None:
        return self._skill_registry_snapshots.get(snapshot_id)

    def skill_registry_snapshots(
        self, run_id: str
    ) -> tuple[SyntheticSkillRegistrySnapshot, ...]:
        return tuple(
            self._skill_registry_snapshots[snapshot_id]
            for snapshot_id in self._run_skill_registry_snapshots.get(run_id, ())
        )

    def get_skill_registry_consumption_receipt(
        self, receipt_id: str
    ) -> SkillRegistryConsumptionReceipt | None:
        return self._skill_registry_consumption_receipts.get(receipt_id)

    def skill_registry_consumption_receipts(
        self, run_id: str
    ) -> tuple[SkillRegistryConsumptionReceipt, ...]:
        return tuple(
            self._skill_registry_consumption_receipts[receipt_id]
            for receipt_id in self._run_skill_registry_consumption_receipts.get(
                run_id, ()
            )
        )

    def get_skill_registry_snapshot_invalidation(
        self, invalidation_id: str
    ) -> SkillRegistrySnapshotInvalidation | None:
        return self._skill_registry_snapshot_invalidations.get(invalidation_id)

    def is_skill_registry_snapshot_invalidated(self, snapshot_id: str) -> bool:
        return snapshot_id in self._invalidated_skill_registry_snapshots

    def get_skill_necessity_decision(
        self, decision_id: str
    ) -> SkillNecessityDecision | None:
        return self._skill_necessity_decisions.get(decision_id)

    def skill_necessity_decisions(
        self, run_id: str
    ) -> tuple[SkillNecessityDecision, ...]:
        return tuple(
            self._skill_necessity_decisions[decision_id]
            for decision_id in self._run_skill_necessity_decisions.get(run_id, ())
        )

    def get_skill_necessity_receipt(
        self, receipt_id: str
    ) -> SkillNecessityReceipt | None:
        return self._skill_necessity_receipts.get(receipt_id)

    def skill_necessity_receipts(
        self, run_id: str
    ) -> tuple[SkillNecessityReceipt, ...]:
        return tuple(
            self._skill_necessity_receipts[receipt_id]
            for receipt_id in self._run_skill_necessity_receipts.get(run_id, ())
        )

    def get_skill_necessity_invalidation(
        self, invalidation_id: str
    ) -> SkillNecessityInvalidation | None:
        return self._skill_necessity_invalidations.get(invalidation_id)

    def is_skill_necessity_invalidated(self, decision_id: str) -> bool:
        return decision_id in self._invalidated_skill_necessity_decisions

    @_synchronized
    def get_atomic_harness_definition(
        self, definition_id: str
    ) -> AtomicHarnessDefinition | None:
        return self._atomic_harness_definitions.get(definition_id)

    def atomic_harness_definitions(
        self, run_id: str
    ) -> tuple[AtomicHarnessDefinition, ...]:
        return tuple(
            self._atomic_harness_definitions[definition_id]
            for definition_id in self._run_atomic_harness_definitions.get(run_id, ())
        )

    def get_atomic_harness_definition_receipt(
        self, receipt_id: str
    ) -> AtomicHarnessDefinitionReceipt | None:
        return self._atomic_harness_definition_receipts.get(receipt_id)

    @_synchronized
    def atomic_harness_definition_receipts(
        self, run_id: str
    ) -> tuple[AtomicHarnessDefinitionReceipt, ...]:
        return tuple(
            self._atomic_harness_definition_receipts[receipt_id]
            for receipt_id in self._run_atomic_harness_definition_receipts.get(
                run_id, ()
            )
        )

    def get_atomic_harness_definition_invalidation(
        self, invalidation_id: str
    ) -> AtomicHarnessDefinitionInvalidation | None:
        return self._atomic_harness_definition_invalidations.get(invalidation_id)

    def is_atomic_harness_definition_invalidated(self, definition_id: str) -> bool:
        return definition_id in self._invalidated_atomic_harness_definitions

    @_synchronized
    def get_atomic_content_harness_validation_report(
        self, report_id: str
    ) -> AtomicContentHarnessValidationReport | None:
        return self._atomic_content_harness_validation_reports.get(report_id)

    @_synchronized
    def atomic_content_harness_validation_reports(
        self, run_id: str
    ) -> tuple[AtomicContentHarnessValidationReport, ...]:
        return tuple(
            self._atomic_content_harness_validation_reports[report_id]
            for report_id in self._run_atomic_content_harness_validation_reports.get(
                run_id, ()
            )
        )

    @_synchronized
    def get_atomic_content_harness_validation_receipt(
        self, receipt_id: str
    ) -> AtomicContentHarnessValidationReceipt | None:
        return self._atomic_content_harness_validation_receipts.get(receipt_id)

    @_synchronized
    def atomic_content_harness_validation_receipts(
        self, run_id: str
    ) -> tuple[AtomicContentHarnessValidationReceipt, ...]:
        return tuple(
            self._atomic_content_harness_validation_receipts[receipt_id]
            for receipt_id in self._run_atomic_content_harness_validation_receipts.get(
                run_id, ()
            )
        )

    def get_atomic_content_harness_validation_invalidation(
        self, invalidation_id: str
    ) -> AtomicContentHarnessValidationInvalidation | None:
        return self._atomic_content_harness_validation_invalidations.get(
            invalidation_id
        )

    def is_atomic_content_harness_validation_invalidated(
        self, report_id: str
    ) -> bool:
        return report_id in self._invalidated_atomic_content_harness_validations

    def get_development_capsule(
        self, capsule_id: str
    ) -> VersionedTraceableDevelopmentCapsule | None:
        return self._development_capsules.get(capsule_id)

    def development_capsules(
        self, run_id: str
    ) -> tuple[VersionedTraceableDevelopmentCapsule, ...]:
        return tuple(
            self._development_capsules[capsule_id]
            for capsule_id in self._run_development_capsules.get(run_id, ())
        )

    def get_development_capsule_receipt(
        self, receipt_id: str
    ) -> DevelopmentCapsuleReceipt | None:
        return self._development_capsule_receipts.get(receipt_id)

    def development_capsule_receipts(
        self, run_id: str
    ) -> tuple[DevelopmentCapsuleReceipt, ...]:
        return tuple(
            self._development_capsule_receipts[receipt_id]
            for receipt_id in self._run_development_capsule_receipts.get(run_id, ())
        )

    def get_development_capsule_invalidation(
        self, invalidation_id: str
    ) -> DevelopmentCapsuleInvalidation | None:
        return self._development_capsule_invalidations.get(invalidation_id)

    def is_development_capsule_invalidated(self, capsule_id: str) -> bool:
        return capsule_id in self._invalidated_development_capsules

    @property
    def development_capsule_count(self) -> int:
        return len(self._development_capsules)

    @property
    def development_capsule_receipt_count(self) -> int:
        return len(self._development_capsule_receipts)

    @property
    def development_capsule_invalidation_count(self) -> int:
        return len(self._development_capsule_invalidations)

    @property
    def capability_ownership_graph_count(self) -> int:
        return len(self._capability_ownership_graphs)

    @property
    def capability_ownership_receipt_count(self) -> int:
        return len(self._capability_ownership_receipts)

    @property
    def capability_ownership_invalidation_count(self) -> int:
        return len(self._capability_ownership_invalidations)

    @property
    def responsibility_module_graph_count(self) -> int:
        return len(self._responsibility_module_graphs)

    @property
    def responsibility_module_receipt_count(self) -> int:
        return len(self._responsibility_module_receipts)

    @property
    def responsibility_module_invalidation_count(self) -> int:
        return len(self._responsibility_module_invalidations)

    @property
    def phase_graph_count(self) -> int:
        return len(self._phase_graphs)

    @property
    def phase_graph_receipt_count(self) -> int:
        return len(self._phase_graph_receipts)

    @property
    def phase_graph_invalidation_count(self) -> int:
        return len(self._phase_graph_invalidations)

    @property
    def phase_handoff_graph_count(self) -> int:
        return len(self._phase_handoff_graphs)

    @property
    def phase_handoff_receipt_count(self) -> int:
        return len(self._phase_handoff_receipts)

    @property
    def internal_handoff_count(self) -> int:
        return len(self._internal_handoffs)

    @property
    def internal_handoff_decision_count(self) -> int:
        return len(self._internal_handoff_decisions)

    @property
    def internal_handoff_receipt_count(self) -> int:
        return len(self._internal_handoff_receipts)

    @property
    def phase_handoff_invalidation_count(self) -> int:
        return len(self._phase_handoff_invalidations)

    @property
    def minimum_context_graph_count(self) -> int:
        return len(self._minimum_context_graphs)

    @property
    def context_compilation_receipt_count(self) -> int:
        return len(self._context_compilation_receipts)

    @property
    def context_graph_invalidation_count(self) -> int:
        return len(self._context_graph_invalidations)

    @property
    def skill_registry_snapshot_count(self) -> int:
        return len(self._skill_registry_snapshots)

    @property
    def skill_registry_consumption_receipt_count(self) -> int:
        return len(self._skill_registry_consumption_receipts)

    @property
    def skill_registry_snapshot_invalidation_count(self) -> int:
        return len(self._skill_registry_snapshot_invalidations)

    @property
    def skill_necessity_decision_count(self) -> int:
        return len(self._skill_necessity_decisions)

    @property
    def skill_necessity_receipt_count(self) -> int:
        return len(self._skill_necessity_receipts)

    @property
    def skill_necessity_invalidation_count(self) -> int:
        return len(self._skill_necessity_invalidations)

    @property
    def atomic_harness_definition_count(self) -> int:
        return len(self._atomic_harness_definitions)

    @property
    def atomic_harness_definition_receipt_count(self) -> int:
        return len(self._atomic_harness_definition_receipts)

    @property
    def atomic_harness_definition_invalidation_count(self) -> int:
        return len(self._atomic_harness_definition_invalidations)

    @property
    def atomic_content_harness_validation_report_count(self) -> int:
        return len(self._atomic_content_harness_validation_reports)

    @property
    def atomic_content_harness_validation_receipt_count(self) -> int:
        return len(self._atomic_content_harness_validation_receipts)

    @property
    def atomic_content_harness_validation_invalidation_count(self) -> int:
        return len(self._atomic_content_harness_validation_invalidations)

    @property
    def constitutional_validation_report_count(self) -> int:
        return len(self._constitutional_validation_reports)

    @property
    def constitutional_validation_receipt_count(self) -> int:
        return len(self._constitutional_validation_receipts)

    @property
    def constitutional_validation_invalidation_count(self) -> int:
        return len(self._constitutional_validation_invalidations)

    @property
    def artifact_manifest_count(self) -> int:
        return len(self._artifact_manifests)

    @property
    def generated_artifact_count(self) -> int:
        return sum(len(items) for items in self._artifact_manifest_artifacts.values())

    @property
    def artifact_receipt_count(self) -> int:
        return len(self._artifact_receipts)

    @property
    def artifact_invalidation_count(self) -> int:
        return len(self._artifact_set_invalidations)

    @property
    def artifact_drift_report_count(self) -> int:
        return len(self._artifact_drift_reports)

    @property
    def harness_ir_count(self) -> int:
        return len(self._harness_irs)

    @property
    def harness_ir_receipt_count(self) -> int:
        return len(self._harness_ir_receipts)

    @property
    def harness_ir_invalidation_count(self) -> int:
        return len(self._harness_ir_invalidations)

    @property
    def atomic_boundary_count(self) -> int:
        return len(self._atomic_boundaries)

    @property
    def draft_harness_model_count(self) -> int:
        return len(self._draft_harness_models)

    @property
    def atomicity_receipt_count(self) -> int:
        return len(self._atomicity_receipts)

    @property
    def boundary_invalidation_count(self) -> int:
        return len(self._boundary_invalidations)

    @_synchronized
    def get_evidence_index(self, index_id: str) -> EvidenceIndex | None:
        return self._evidence_indexes.get(index_id)

    @_synchronized
    def evidence_indexes(self, run_id: str) -> tuple[EvidenceIndex, ...]:
        return tuple(
            self._evidence_indexes[index_id]
            for index_id in self._run_evidence_indexes.get(run_id, ())
        )

    @_synchronized
    def get_evidence_index_receipt(
        self, receipt_id: str
    ) -> EvidenceIndexReceipt | None:
        return self._evidence_index_receipts.get(receipt_id)

    @_synchronized
    def evidence_index_receipts(
        self, run_id: str
    ) -> tuple[EvidenceIndexReceipt, ...]:
        return tuple(
            self._evidence_index_receipts[receipt_id]
            for receipt_id in self._run_evidence_index_receipts.get(run_id, ())
        )

    @_synchronized
    def get_evidence_index_invalidation(
        self, invalidation_id: str
    ) -> EvidenceIndexInvalidation | None:
        return self._evidence_index_invalidations.get(invalidation_id)

    @_synchronized
    def is_evidence_index_invalidated(self, index_id: str) -> bool:
        return index_id in self._invalidated_evidence_indexes

    @_synchronized
    def active_evidence_index(self, run_id: str) -> EvidenceIndex | None:
        run = self.load_run(run_id)
        if (
            not run.evidence_index_ref
            or run.evidence_index_invalidation_ref is not None
            or run.evidence_index_ref in self._invalidated_evidence_indexes
        ):
            return None
        return self._evidence_indexes.get(run.evidence_index_ref)

    @_synchronized
    def get_saturation_contract(self, contract_id: str) -> SaturationContract | None:
        return self._saturation_contracts.get(contract_id)

    @_synchronized
    def get_saturation_evaluation(
        self, evaluation_id: str
    ) -> SaturationEvaluation | None:
        return self._saturation_evaluations.get(evaluation_id)

    @_synchronized
    def saturation_evaluations(
        self, run_id: str
    ) -> tuple[SaturationEvaluation, ...]:
        return tuple(
            self._saturation_evaluations[evaluation_id]
            for evaluation_id in self._run_saturation_evaluations.get(run_id, ())
        )

    @_synchronized
    def get_saturation_receipt(self, receipt_id: str) -> SaturationReceipt | None:
        return self._saturation_receipts.get(receipt_id)

    @_synchronized
    def get_saturation_invalidation(
        self, invalidation_id: str
    ) -> SaturationInvalidation | None:
        return self._saturation_invalidations.get(invalidation_id)

    @_synchronized
    def is_saturation_evaluation_invalidated(self, evaluation_id: str) -> bool:
        return evaluation_id in self._invalidated_saturation_evaluations

    @_synchronized
    def active_saturation_evaluation(
        self, run_id: str
    ) -> SaturationEvaluation | None:
        run = self.load_run(run_id)
        if (
            not run.saturation_evaluation_ref
            or run.saturation_evaluation_invalidation_ref is not None
            or run.saturation_evaluation_ref
            in self._invalidated_saturation_evaluations
        ):
            return None
        return self._saturation_evaluations.get(run.saturation_evaluation_ref)

    @_synchronized
    def get_decision_graph(self, graph_id: str) -> DecisionGraph | None:
        return self._decision_graphs.get(graph_id)

    @_synchronized
    def get_genesis_question_package(self, package_id: str) -> GenesisQuestionPackage | None:
        return self._genesis_question_packages.get(package_id)

    @_synchronized
    def get_genesis_question_receipt(self, receipt_id: str) -> GenesisQuestionReceipt | None:
        return self._genesis_question_receipts.get(receipt_id)

    @_synchronized
    def get_genesis_question_invalidation(self, invalidation_id: str) -> GenesisQuestionInvalidation | None:
        return self._genesis_question_invalidations.get(invalidation_id)

    @_synchronized
    def active_genesis_question(self, run_id: str) -> GenesisQuestionPackage | None:
        run = self.load_run(run_id)
        if (
            not run.genesis_question_ref
            or run.genesis_question_invalidation_ref is not None
            or run.genesis_question_ref in self._invalidated_genesis_questions
        ):
            return None
        return self._genesis_question_packages.get(run.genesis_question_ref)

    @property
    @_synchronized
    def genesis_question_count(self) -> int:
        return len(self._genesis_question_packages)

    @property
    @_synchronized
    def genesis_question_receipt_count(self) -> int:
        return len(self._genesis_question_receipts)

    @property
    @_synchronized
    def saturation_evaluation_count(self) -> int:
        return len(self._saturation_evaluations)

    @property
    @_synchronized
    def saturation_receipt_count(self) -> int:
        return len(self._saturation_receipts)

    @_synchronized
    def query_evidence_index(
        self,
        index_id: str,
        *,
        specimen_id: str | None = None,
        source_id: str | None = None,
        role: str | None = None,
        governed_status: str | None = None,
        knowledge_status: str | None = None,
    ) -> tuple[Specimen, ...]:
        index = self._evidence_indexes.get(index_id)
        if index is None:
            raise KeyError(index_id)
        return index.query(
            specimen_id=specimen_id,
            source_id=source_id,
            role=role,
            governed_status=governed_status,
            knowledge_status=knowledge_status,
        )

    @property
    @_synchronized
    def evidence_index_count(self) -> int:
        return len(self._evidence_indexes)

    @property
    @_synchronized
    def evidence_index_receipt_count(self) -> int:
        return len(self._evidence_index_receipts)

    @_synchronized
    def get_source_lock(self, lock_id: str) -> SourceLock | None:
        return self._source_locks.get(lock_id)

    @_synchronized
    def source_locks(self, run_id: str) -> tuple[SourceLock, ...]:
        return tuple(
            self._source_locks[lock_id]
            for lock_id in self._run_source_locks.get(run_id, ())
        )

    @property
    def source_lock_count(self) -> int:
        return len(self._source_locks)

    @_synchronized
    def load_run(self, run_id: str) -> Run:
        if run_id not in self._streams:
            raise KeyError(run_id)
        return Run.replay(self._streams[run_id])

    @_synchronized
    def events(self, run_id: str) -> tuple[RunEvent, ...]:
        return self._streams.get(run_id, ())

    @_synchronized
    def event_count(self, run_id: str) -> int:
        return len(self._streams.get(run_id, ()))

    @_synchronized
    def get_command_record(self, command_id: str) -> CommandRecord | None:
        return self._command_records.get(command_id)

    @_synchronized
    def save_command_record(self, command_id: str, record: CommandRecord) -> None:
        existing = self._command_records.get(command_id)
        if existing is not None and existing != record:
            raise IdempotencyPayloadMismatch(
                "A command record cannot be overwritten.", command_id=command_id
            )
        self._command_records[command_id] = record

    @_synchronized
    def add_checkpoint(self, checkpoint: Checkpoint) -> None:
        self._checkpoints.setdefault(checkpoint.run_id, {})[
            checkpoint.checkpoint_id
        ] = checkpoint

    @_synchronized
    def list_checkpoints(self, run_id: str) -> tuple[Checkpoint, ...]:
        return tuple(self._checkpoints.get(run_id, {}).values())

    def _validated_append(
        self,
        run_id: str,
        expected_version: int,
        events: tuple[RunEvent, ...],
    ) -> tuple[RunEvent, ...]:
        current = self._streams.get(run_id, ())
        if len(current) != expected_version:
            raise ConcurrencyConflict(
                "Expected stream version does not match authoritative state.",
                run_id=run_id,
                expected_version=expected_version,
                current_version=len(current),
            )
        next_version = expected_version + 1
        for event in events:
            if event.run_id != run_id or event.stream_version != next_version:
                raise ConcurrencyConflict(
                    "Appended events are not contiguous for the target stream.",
                    run_id=run_id,
                    expected_event_version=next_version,
                    observed_event_version=event.stream_version,
                )
            next_version += 1
        return current

    def _validate_definition_authority(
        self, run: Run, definition: AtomicHarnessDefinition
    ) -> None:
        attachments = tuple(
            event
            for event in self._streams.get(run.run_id, ())
            if event.event_type == "AtomicHarnessDefinitionAttached"
            and event.value("definition_ref") == definition.definition_id
        )
        receipt_ids = self._run_atomic_harness_definition_receipts.get(
            run.run_id, ()
        )
        receipts = tuple(
            self._atomic_harness_definition_receipts[receipt_id]
            for receipt_id in receipt_ids
            if self._atomic_harness_definition_receipts[
                receipt_id
            ].definition_id
            == definition.definition_id
        )
        context = self._minimum_context_graphs.get(
            run.minimum_context_ref or ""
        )
        if len(attachments) != 1 or len(receipts) != 1 or context is None:
            raise ConcurrencyConflict(
                "Definition compiler authority evidence is missing or ambiguous.",
                run_id=run.run_id,
                definition_id=definition.definition_id,
            )
        attachment = attachments[0]
        definition_receipt = receipts[0]
        if (
            attachment.actor_id != definition.authority_identity
            or attachment.value("definition_hash") != definition.definition_hash
            or attachment.command_id != definition_receipt.command_id
            or definition_receipt.event_ids != (attachment.event_id,)
            or definition_receipt.stream_version != attachment.stream_version
            or definition_receipt.authority_identity != attachment.actor_id
        ):
            raise ConcurrencyConflict(
                "Definition attachment, receipt and compiler authority differ.",
                run_id=run.run_id,
                definition_id=definition.definition_id,
            )
        accepted_handoff = self._internal_handoffs.get(
            context.accepted_handoff_id
        )
        handoff_decision = self._internal_handoff_decisions.get(
            context.accepted_handoff_id
        )
        values = {
            "run": run,
            "source_lock": self._source_locks.get(run.source_lock_ref or ""),
            "boundary": self._atomic_boundaries.get(run.atomic_boundary_ref or ""),
            "ratification": self._atomicity_ratifications.get(
                run.atomicity_ratification_ref or ""
            ),
            "model": self._draft_harness_models.get(
                run.draft_harness_model_ref or ""
            ),
            "ir": self._harness_irs.get(run.harness_ir_ref or ""),
            "manifest": self._artifact_manifests.get(
                run.artifact_manifest_ref or ""
            ),
            "constitutional": self._constitutional_validation_reports.get(
                run.constitutional_validation_ref or ""
            ),
            "capability": self._capability_ownership_graphs.get(
                run.capability_ownership_ref or ""
            ),
            "modules": self._responsibility_module_graphs.get(
                run.responsibility_module_ref or ""
            ),
            "phases": self._phase_graphs.get(run.phase_graph_ref or ""),
            "handoff_graph": self._phase_handoff_graphs.get(
                run.phase_handoff_ref or ""
            ),
            "accepted_handoff": accepted_handoff,
            "handoff_decision": handoff_decision,
            "context": context,
            "snapshot": self._skill_registry_snapshots.get(
                run.skill_registry_snapshot_ref or ""
            ),
            "necessity": self._skill_necessity_decisions.get(
                run.skill_necessity_ref or ""
            ),
        }
        if any(value is None for value in values.values()):
            raise ConcurrencyConflict(
                "Definition upstream authority cannot be reconstructed.",
                run_id=run.run_id,
                definition_id=definition.definition_id,
            )
        try:
            definition_receipt.validate(definition)
            definition.validate(
                **values,
                expected_authority_identity=attachment.actor_id,
            )
        except Exception as error:
            raise ConcurrencyConflict(
                "Definition meaning does not match stored governed authority.",
                run_id=run.run_id,
                definition_id=definition.definition_id,
            ) from error


class FixedClock:
    def __init__(self, value: datetime) -> None:
        self._value = value

    def now(self) -> datetime:
        return self._value


class DeterministicUuid7IdProvider:
    """Generate reproducible prefix-plus-UUIDv7 identities for deterministic fixtures."""

    def __init__(self, *, timestamp_ms: int, seed: str) -> None:
        if timestamp_ms < 0 or timestamp_ms >= 1 << 48:
            raise ValueError("UUIDv7 timestamp must fit in 48 bits.")
        self._timestamp_ms = timestamp_ms
        self._seed = seed
        self._counter = 0

    def new_id(self, kind: str) -> str:
        if not kind or any(character.isspace() for character in kind):
            raise ValueError("Identity kind must be non-empty and contain no whitespace.")
        self._counter += 1
        entropy = int.from_bytes(
            sha256(f"{self._seed}|{kind}|{self._counter}".encode("utf-8")).digest(),
            "big",
        ) & ((1 << 74) - 1)
        rand_a = entropy >> 62
        rand_b = entropy & ((1 << 62) - 1)
        value = (
            (self._timestamp_ms << 80)
            | (0x7 << 76)
            | (rand_a << 64)
            | (0b10 << 62)
            | rand_b
        )
        identifier = UUID(int=value)
        if identifier.version != 7 or identifier.variant != "specified in RFC 4122":
            raise AssertionError("Generated identifier is not RFC-compatible UUIDv7.")
        return f"{kind}_{identifier}"


class RecordingObservationSink:
    def __init__(self) -> None:
        self._observations: list[Observation] = []

    @property
    def observations(self) -> tuple[Observation, ...]:
        return tuple(self._observations)

    def emit(self, observation: Observation) -> None:
        self._observations.append(observation)


def _manifest_config(manifest: ArtifactManifest) -> ReproducibleBuildConfig:
    return ReproducibleBuildConfig(
        compiler_id=manifest.compiler_id,
        compiler_version=manifest.compiler_version,
        config_version=manifest.config_version,
        generation_timestamp=manifest.generation_timestamp,
    )
