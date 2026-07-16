from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityService
from cmf_builder.application.ports import (
    AtomicityRepository,
    Clock,
    CommandRecord,
    DeclaredBoundaryInputRepository,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomicity import (
    AtomicityDecision,
    AtomicityDecisionAction,
    AtomicityDecisionReceipt,
    AtomicityReadinessEvaluation,
    AtomicityRatification,
    AuthorityStatus,
    BoundaryInputMismatch,
    BoundaryInvalidation,
    CriticalBoundaryContradiction,
    DeclaredAtomicBoundary,
    DeclaredBoundaryInput,
    DecisionPackageIncomplete,
    DraftHarnessModel,
    FieldAuthorityRejected,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.run import LifecycleState, Run
from cmf_builder.domain.harness_ir import HarnessIRInvalidation
from cmf_builder.domain.generated_artifacts import ArtifactSetInvalidation
from cmf_builder.domain.constitutional_validation import (
    ConstitutionalValidationInvalidation,
)
from cmf_builder.domain.capability_ownership import (
    CapabilityOwnershipInvalidation,
)
from cmf_builder.domain.responsibility_modules import (
    ResponsibilityModuleInvalidation,
)
from cmf_builder.domain.phase_graph import PhaseGraphInvalidation
from cmf_builder.domain.handoff import PhaseHandoffInvalidation
from cmf_builder.domain.context_manifest import ContextGraphInvalidation
from cmf_builder.domain.skill_registry import (
    SkillNecessityInvalidation,
    SkillRegistrySnapshotInvalidation,
)
from cmf_builder.domain.atomic_harness_definition import (
    AtomicHarnessDefinitionInvalidation,
)
from cmf_builder.domain.target_package_validation import (
    AtomicContentHarnessValidationInvalidation,
)
from cmf_builder.domain.development_capsule import DevelopmentCapsuleInvalidation


DECLARED_INPUT_PATH = "development-capsules/ST-02.05/DECLARED_BOUNDARY_INPUT.json"
DECLARED_INPUT_SHA256 = (
    "5c36325c876201e5c96a0171b05b4d4fdb9421c72d0bc42c9365e189896e5ead"
)
SYNTHETIC_PROFILE_ID = "synthetic_text_normalization_v1"
SYNTHETIC_PROFILE_VERSION = "1.0.0"
SYNTHETIC_CATEGORY_ID = "none_test_only"


class AtomicityCommandRejected(Exception):
    code = "AtomicityCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class DecideAtomicBoundaryCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    decision: AtomicityDecision
    declared_input_path: str = DECLARED_INPUT_PATH
    declared_input_sha256: str = DECLARED_INPUT_SHA256


@dataclass(frozen=True, slots=True)
class ReopenAtomicBoundaryCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    reason: str


class AtomicityCommandService:
    STORY_ID = "ST-02.05"
    CONTRACT_VERSION = "cmf-builder-atomicity/v1"

    def __init__(
        self,
        *,
        repository: AtomicityRepository,
        declared_inputs: DeclaredBoundaryInputRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._declared_inputs = declared_inputs
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def decide(self, command: DecideAtomicBoundaryCommand) -> AtomicityDecisionReceipt:
        run: Run | None = None
        declared: DeclaredBoundaryInput | None = None
        source_lock: SourceLock | None = None
        try:
            duplicate = self._duplicate(command.command_id, _command_hash(command))
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._validate_decision_command(run, command)
            action = {
                AtomicityDecisionAction.APPROVE: Action.RATIFY_ATOMIC_BOUNDARY,
                AtomicityDecisionAction.REVISE: Action.REVISE_ATOMIC_BOUNDARY,
                AtomicityDecisionAction.REJECT: Action.REJECT_ATOMIC_BOUNDARY,
            }[command.decision.action]
            self._authority.authorize(
                actor_id=command.actor_id,
                action=action,
                resource_id=command.run_id,
                now=now,
            )
            if command.decision.decided_at != now:
                raise DecisionPackageIncomplete(
                    "Decision time must equal the governed command time.",
                    decision_time=command.decision.decided_at.isoformat(),
                    command_time=now.isoformat(),
                )
            source_lock = self._required_source_lock(run)
            declared = self._load_declared(command)
            self._validate_declared_against_run(declared, run, source_lock)
            command.decision.validate(declared, actor_id=command.actor_id)

            if command.decision.action is AtomicityDecisionAction.APPROVE:
                return self._approve(command, run, source_lock, declared)
            return self._record_nonapproval(command, run, source_lock, declared)
        except Exception as error:
            self._reject(
                command_id=command.command_id,
                run_id=command.run_id,
                actor_id=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                run=run,
                declared=declared,
                source_lock=source_lock,
                error=error,
            )
            raise

    def reopen(self, command: ReopenAtomicBoundaryCommand) -> AtomicityDecisionReceipt:
        run: Run | None = None
        declared: DeclaredBoundaryInput | None = None
        source_lock: SourceLock | None = None
        try:
            duplicate = self._duplicate(command.command_id, _command_hash(command))
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            if (
                run.lifecycle_state not in {
                    LifecycleState.ATOMICITY_RATIFICATION,
                    LifecycleState.GENESIS,
                }
                or command.expected_version != run.stream_version
                or not run.atomic_boundary_ref
                or not run.draft_harness_model_ref
                or run.boundary_invalidation_ref is not None
            ):
                raise AtomicityCommandRejected(
                    "Only one active frozen boundary may be reopened.",
                    lifecycle_state=run.lifecycle_state.value,
                    expected_version=command.expected_version,
                    current_version=run.stream_version,
                )
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.REOPEN_ATOMIC_BOUNDARY,
                resource_id=command.run_id,
                now=now,
            )
            source_lock = self._required_source_lock(run)
            declared = self._declared_inputs.load(
                DECLARED_INPUT_PATH, DECLARED_INPUT_SHA256
            )
            invalidation = BoundaryInvalidation.create(
                invalidation_id=self._ids.new_id("invalidation"),
                boundary_ref=run.atomic_boundary_ref,
                model_ref=run.draft_harness_model_ref,
                reason=command.reason,
                human_id=command.actor_id,
                reopened_at=now,
            )
            evaluation = AtomicityReadinessEvaluation(
                gate_id="HG-003",
                result="FAIL",
                reason="The prior boundary was reopened and invalidated.",
                evidence_refs=(invalidation.invalidation_hash,),
            )
            harness_ir_invalidation = (
                HarnessIRInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    ir_ref=run.harness_ir_ref,
                    upstream_invalidation_ref=invalidation.invalidation_id,
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.harness_ir_ref
                else None
            )
            artifact_set_invalidation = (
                ArtifactSetInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    artifact_set_ref=run.artifact_set_ref,
                    manifest_ref=run.artifact_manifest_ref,
                    ir_ref=run.harness_ir_ref,
                    upstream_invalidation_ref=invalidation.invalidation_id,
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.artifact_set_ref
                and run.artifact_manifest_ref
                and run.harness_ir_ref
                else None
            )
            constitutional_validation_invalidation = (
                ConstitutionalValidationInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    report_ref=run.constitutional_validation_ref,
                    artifact_set_ref=run.artifact_set_ref,
                    upstream_invalidation_ref=invalidation.invalidation_id,
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.constitutional_validation_ref and run.artifact_set_ref
                else None
            )
            capability_ownership_invalidation = (
                CapabilityOwnershipInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    graph_ref=run.capability_ownership_ref,
                    constitutional_report_ref=run.constitutional_validation_ref,
                    upstream_invalidation_ref=(
                        constitutional_validation_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.capability_ownership_ref
                and run.constitutional_validation_ref
                and constitutional_validation_invalidation is not None
                else None
            )
            responsibility_module_invalidation = (
                ResponsibilityModuleInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    module_graph_ref=run.responsibility_module_ref,
                    capability_graph_ref=run.capability_ownership_ref,
                    upstream_invalidation_ref=(
                        capability_ownership_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.responsibility_module_ref
                and run.capability_ownership_ref
                and capability_ownership_invalidation is not None
                else None
            )
            phase_graph_invalidation = (
                PhaseGraphInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    phase_graph_ref=run.phase_graph_ref,
                    module_graph_ref=run.responsibility_module_ref,
                    upstream_invalidation_ref=(
                        responsibility_module_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.phase_graph_ref
                and run.responsibility_module_ref
                and responsibility_module_invalidation is not None
                else None
            )
            phase_handoff_invalidation = (
                PhaseHandoffInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    handoff_graph_ref=run.phase_handoff_ref,
                    phase_graph_ref=run.phase_graph_ref,
                    upstream_invalidation_ref=phase_graph_invalidation.invalidation_id,
                    affected_handoff_ids=tuple(
                        item.handoff_id
                        for item in self._repository.internal_handoffs(run.run_id)
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.phase_handoff_ref
                and run.phase_graph_ref
                and phase_graph_invalidation is not None
                else None
            )
            active_context_graph = (
                self._repository.get_minimum_context_graph(run.minimum_context_ref)
                if run.minimum_context_ref
                else None
            )
            context_graph_invalidation = (
                ContextGraphInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    context_graph_ref=run.minimum_context_ref,
                    handoff_graph_ref=run.phase_handoff_ref,
                    upstream_invalidation_ref=phase_handoff_invalidation.invalidation_id,
                    affected_manifest_ids=tuple(
                        item.manifest_id for item in active_context_graph.manifests
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.minimum_context_ref
                and run.phase_handoff_ref
                and phase_handoff_invalidation is not None
                and active_context_graph is not None
                else None
            )
            active_skill_snapshot = (
                self._repository.get_skill_registry_snapshot(
                    run.skill_registry_snapshot_ref
                )
                if run.skill_registry_snapshot_ref
                else None
            )
            skill_registry_snapshot_invalidation = (
                SkillRegistrySnapshotInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    snapshot_ref=run.skill_registry_snapshot_ref,
                    minimum_context_ref=run.minimum_context_ref,
                    upstream_invalidation_ref=context_graph_invalidation.invalidation_id,
                    affected_capability_ids=active_skill_snapshot.capability_ids,
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.skill_registry_snapshot_ref
                and run.minimum_context_ref
                and context_graph_invalidation is not None
                and active_skill_snapshot is not None
                else None
            )
            active_skill_necessity = (
                self._repository.get_skill_necessity_decision(
                    run.skill_necessity_ref
                )
                if run.skill_necessity_ref
                else None
            )
            skill_necessity_invalidation = (
                SkillNecessityInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    decision_ref=run.skill_necessity_ref,
                    snapshot_ref=run.skill_registry_snapshot_ref,
                    upstream_invalidation_ref=(
                        skill_registry_snapshot_invalidation.invalidation_id
                    ),
                    affected_capability_ids=active_skill_necessity.capability_ids,
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.skill_necessity_ref
                and run.skill_registry_snapshot_ref
                and skill_registry_snapshot_invalidation is not None
                and active_skill_necessity is not None
                else None
            )
            active_atomic_harness_definition = (
                self._repository.get_atomic_harness_definition(
                    run.atomic_harness_definition_ref
                )
                if run.atomic_harness_definition_ref
                else None
            )
            atomic_harness_definition_invalidation = (
                AtomicHarnessDefinitionInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    definition_ref=run.atomic_harness_definition_ref,
                    necessity_decision_ref=run.skill_necessity_ref,
                    upstream_invalidation_ref=(
                        skill_necessity_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.atomic_harness_definition_ref
                and run.skill_necessity_ref
                and skill_necessity_invalidation is not None
                and active_atomic_harness_definition is not None
                else None
            )
            active_target_validation = (
                self._repository.get_atomic_content_harness_validation_report(
                    run.atomic_content_harness_validation_ref
                )
                if run.atomic_content_harness_validation_ref
                else None
            )
            atomic_content_harness_validation_invalidation = (
                AtomicContentHarnessValidationInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    report_ref=run.atomic_content_harness_validation_ref,
                    definition_ref=run.atomic_harness_definition_ref,
                    upstream_invalidation_ref=(
                        atomic_harness_definition_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.atomic_content_harness_validation_ref
                and run.atomic_harness_definition_ref
                and atomic_harness_definition_invalidation is not None
                and active_target_validation is not None
                else None
            )
            active_development_capsule = (
                self._repository.get_development_capsule(
                    run.development_capsule_ref
                )
                if run.development_capsule_ref
                else None
            )
            development_capsule_invalidation = (
                DevelopmentCapsuleInvalidation.create(
                    invalidation_id=invalidation.invalidation_id,
                    capsule_ref=run.development_capsule_ref,
                    validation_ref=run.atomic_content_harness_validation_ref,
                    upstream_invalidation_ref=(
                        atomic_content_harness_validation_invalidation.invalidation_id
                    ),
                    reason=command.reason,
                    authority_identity=command.actor_id,
                )
                if run.development_capsule_ref
                and run.atomic_content_harness_validation_ref
                and atomic_content_harness_validation_invalidation is not None
                and active_development_capsule is not None
                else None
            )
            final_run, events = run.reopen_atomic_boundary(
                invalidation_ref=invalidation.invalidation_id,
                reason=command.reason,
                event_ids=tuple(
                    self._ids.new_id("event")
                    for _ in range(
                        15
                        if run.development_capsule_ref
                        else (
                            14
                            if run.atomic_content_harness_validation_ref
                            else (
                                13
                                if run.atomic_harness_definition_ref
                                else (
                                    12
                                    if run.skill_necessity_ref
                                    else (
                                        11
                                        if run.skill_registry_snapshot_ref
                                        else (
                                            10
                                            if run.minimum_context_ref
                                            else (
                                                9
                                                if run.phase_handoff_ref
                                                else (
                                                    8
                                                    if run.phase_graph_ref
                                                    else (
                                                        7
                                                        if run.responsibility_module_ref
                                                        else (
                                                            6
                                                            if run.capability_ownership_ref
                                                            else (
                                                                5
                                                                if run.constitutional_validation_ref
                                                                else 4
                                                                if run.artifact_set_ref
                                                                else (3 if run.harness_ir_ref else 2)
                                                            )
                                                        )
                                                    )
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = AtomicityDecisionReceipt.create(
                receipt_id=self._ids.new_id("receipt"),
                command_id=command.command_id,
                run_id=run.run_id,
                decision_status="REOPENED",
                authority_identity=command.actor_id,
                declared_input_hash=declared.input_hash,
                source_lock_ref=source_lock.lock_id,
                boundary_ref=run.atomic_boundary_ref,
                model_ref=run.draft_harness_model_ref,
                ratification_ref=None,
                invalidation_ref=invalidation.invalidation_id,
                event_ids=tuple(item.event_id for item in events),
                hg_003_result=evaluation.result,
            )
            self._repository.commit_atomicity(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=events,
                command_id=command.command_id,
                command_record=CommandRecord(
                    payload_hash=_command_hash(command), result=receipt
                ),
                decision=None,
                receipt=receipt,
                boundary=None,
                ratification=None,
                model=None,
                invalidation=invalidation,
                harness_ir_invalidation=harness_ir_invalidation,
                artifact_set_invalidation=artifact_set_invalidation,
                constitutional_validation_invalidation=constitutional_validation_invalidation,
                capability_ownership_invalidation=capability_ownership_invalidation,
                responsibility_module_invalidation=responsibility_module_invalidation,
                phase_graph_invalidation=phase_graph_invalidation,
                phase_handoff_invalidation=phase_handoff_invalidation,
                context_graph_invalidation=context_graph_invalidation,
                skill_registry_snapshot_invalidation=skill_registry_snapshot_invalidation,
                skill_necessity_invalidation=skill_necessity_invalidation,
                atomic_harness_definition_invalidation=atomic_harness_definition_invalidation,
                atomic_content_harness_validation_invalidation=atomic_content_harness_validation_invalidation,
                development_capsule_invalidation=development_capsule_invalidation,
            )
            invalidated_artifacts = (
                invalidation.boundary_ref,
                invalidation.model_ref,
                *((run.harness_ir_ref,) if run.harness_ir_ref else ()),
                *((run.artifact_set_ref,) if run.artifact_set_ref else ()),
                *((run.artifact_manifest_ref,) if run.artifact_manifest_ref else ()),
                *((run.constitutional_validation_ref,) if run.constitutional_validation_ref else ()),
                *((run.capability_ownership_ref,) if run.capability_ownership_ref else ()),
                *((run.responsibility_module_ref,) if run.responsibility_module_ref else ()),
                *((run.phase_graph_ref,) if run.phase_graph_ref else ()),
                *((run.phase_handoff_ref,) if run.phase_handoff_ref else ()),
                *((run.minimum_context_ref,) if run.minimum_context_ref else ()),
                *((run.skill_registry_snapshot_ref,) if run.skill_registry_snapshot_ref else ()),
                *((run.skill_necessity_ref,) if run.skill_necessity_ref else ()),
                *((run.atomic_harness_definition_ref,) if run.atomic_harness_definition_ref else ()),
                *((run.atomic_content_harness_validation_ref,) if run.atomic_content_harness_validation_ref else ()),
                *((run.development_capsule_ref,) if run.development_capsule_ref else ()),
                *(
                    tuple(item.manifest_id for item in active_context_graph.manifests)
                    if active_context_graph is not None
                    else ()
                ),
                *(
                    tuple(
                        item.handoff_id
                        for item in self._repository.internal_handoffs(run.run_id)
                    )
                    if run.phase_handoff_ref
                    else ()
                ),
            )
            for event_name in (
                "ST-02.05:BoundaryReopened",
                "ST-02.05:DraftModelInvalidated",
                "ST-02.05:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command_id=command.command_id,
                    actor_id=command.actor_id,
                    correlation_id=command.correlation_id,
                    causation_id=command.causation_id,
                    run=final_run,
                    declared=declared,
                    source_lock=source_lock,
                    receipt=receipt,
                    failure_context={},
                    invalidated_artifacts=invalidated_artifacts,
                )
            if harness_ir_invalidation is not None:
                snapshot = self._repository.get_harness_ir(
                    harness_ir_invalidation.ir_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-03.03:HarnessIRInvalidated",
                        run_id=run.run_id,
                        story_id="ST-03.03",
                        artifact_identity=harness_ir_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-harness-ir/v1",
                        provenance=harness_ir_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=source_lock.lock_id,
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=harness_ir_invalidation.ir_ref,
                        harness_ir_hash=(
                            snapshot.ir_hash if snapshot else "unassigned"
                        ),
                        harness_ir_schema_id=(
                            snapshot.schema_id if snapshot else "unassigned"
                        ),
                        harness_ir_schema_version=(
                            snapshot.schema_version if snapshot else "unassigned"
                        ),
                        harness_ir_revision=(snapshot.revision if snapshot else 0),
                        harness_ir_status="INVALIDATED",
                        harness_ir_compatibility=(
                            "READ_WRITE_1.0.0_NO_PRIOR_MIGRATIONS"
                        ),
                        activative_lineage_disposition=(
                            "EXPLICIT_NOT_APPLICABLE_SEPARATE_KEYS"
                        ),
                        dependency_impact_refs=(
                            invalidation.boundary_ref,
                            invalidation.model_ref,
                            harness_ir_invalidation.ir_ref,
                        ),
                    )
                )
            if artifact_set_invalidation is not None:
                self._observations.emit(
                    Observation(
                        event_name="ST-03.04:ArtifactSetInvalidated",
                        run_id=run.run_id,
                        story_id="ST-03.04",
                        artifact_identity=artifact_set_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-artifact-manifest/v1",
                        provenance=artifact_set_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=source_lock.lock_id,
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=artifact_set_invalidation.ir_ref,
                        harness_ir_status="INVALIDATED",
                        artifact_set_id=artifact_set_invalidation.artifact_set_ref,
                        artifact_manifest_id=artifact_set_invalidation.manifest_ref,
                        drift_disposition="INVALIDATED_BY_AUTHORITATIVE_UPSTREAM_REOPEN",
                        quarantine_disposition="ACTIVE_CONSUMPTION_BLOCKED_HISTORY_PRESERVED",
                        dependency_impact_refs=invalidated_artifacts,
                    )
                )
            if constitutional_validation_invalidation is not None:
                report = self._repository.get_constitutional_validation_report(
                    constitutional_validation_invalidation.report_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-03.05:ConstitutionalValidationInvalidated",
                        run_id=run.run_id,
                        story_id="ST-03.05",
                        artifact_identity=constitutional_validation_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-constitutional-validation/v1",
                        provenance=constitutional_validation_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=source_lock.lock_id,
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(report.ir_id if report else "unassigned"),
                        harness_ir_hash=(report.ir_hash if report else "unassigned"),
                        artifact_set_id=constitutional_validation_invalidation.artifact_set_ref,
                        artifact_manifest_id=(report.manifest_id if report else "unassigned"),
                        artifact_manifest_hash=(report.manifest_hash if report else "unassigned"),
                        constitutional_policy_path=(report.policy_path if report else "unassigned"),
                        constitutional_policy_hash=(report.policy_hash if report else "unassigned"),
                        constitution_hash=(report.constitution_hash if report else "unassigned"),
                        builder_prd_amendment_hash=(report.builder_prd_amendment_hash if report else "unassigned"),
                        constitutional_report_id=constitutional_validation_invalidation.report_ref,
                        constitutional_report_hash=(report.report_hash if report else "unassigned"),
                        constitutional_coverage_count=(len(report.coverage) if report else 0),
                        constitutional_precedence_disposition="INVALIDATED_BY_AUTHORITATIVE_UPSTREAM_REOPEN",
                        constitutional_invalidation_ref=constitutional_validation_invalidation.invalidation_id,
                    )
                )
            if capability_ownership_invalidation is not None:
                graph = self._repository.get_capability_ownership_graph(
                    capability_ownership_invalidation.graph_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-04.01:CapabilityOwnershipInvalidated",
                        run_id=run.run_id,
                        story_id="ST-04.01",
                        artifact_identity=capability_ownership_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-capability-ownership/v1@1.0.0",
                        provenance=capability_ownership_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(graph.source_lock_ref if graph else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(graph.ir_id if graph else "unassigned"),
                        harness_ir_hash=(graph.ir_hash if graph else "unassigned"),
                        artifact_set_id=(graph.artifact_set_id if graph else "unassigned"),
                        constitutional_report_id=capability_ownership_invalidation.constitutional_report_ref,
                        constitutional_report_hash=(
                            graph.constitutional_report_hash if graph else "unassigned"
                        ),
                        constitutional_precedence_disposition="INVALIDATED_BY_AUTHORITATIVE_UPSTREAM_REOPEN",
                        capability_graph_id=capability_ownership_invalidation.graph_ref,
                        capability_graph_hash=(graph.graph_hash if graph else "unassigned"),
                        capability_count=(len(graph.decisions) if graph else 0),
                        capability_owner_kind_counts=(
                            graph.owner_kind_counts if graph else ()
                        ),
                        capability_reliability_coverage_count=(
                            len(graph.decisions) if graph else 0
                        ),
                        capability_cost_coverage_count=(
                            len(graph.decisions) if graph else 0
                        ),
                        capability_invalidation_ref=capability_ownership_invalidation.invalidation_id,
                    )
                )
            if responsibility_module_invalidation is not None:
                graph = self._repository.get_responsibility_module_graph(
                    responsibility_module_invalidation.module_graph_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-04.02:ResponsibilityModulesInvalidated",
                        run_id=run.run_id,
                        story_id="ST-04.02",
                        artifact_identity=responsibility_module_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-responsibility-module-graph/v1@1.0.0",
                        provenance=responsibility_module_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(graph.source_lock_ref if graph else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(graph.ir_id if graph else "unassigned"),
                        harness_ir_hash=(graph.ir_hash if graph else "unassigned"),
                        artifact_set_id=(graph.artifact_set_id if graph else "unassigned"),
                        constitutional_report_id=(
                            graph.constitutional_report_id if graph else "unassigned"
                        ),
                        constitutional_report_hash=(
                            graph.constitutional_report_hash if graph else "unassigned"
                        ),
                        capability_graph_id=responsibility_module_invalidation.capability_graph_ref,
                        capability_graph_hash=(
                            graph.capability_graph_hash if graph else "unassigned"
                        ),
                        capability_count=(
                            len(graph.capability_ownerships) if graph else 0
                        ),
                        module_graph_id=responsibility_module_invalidation.module_graph_ref,
                        module_graph_hash=(graph.graph_hash if graph else "unassigned"),
                        module_count=(len(graph.modules) if graph else 0),
                        module_capability_coverage_count=(
                            len(graph.capability_ids) if graph else 0
                        ),
                        module_dependency_count=(graph.dependency_count if graph else 0),
                        module_contract_coverage_count=(
                            len(graph.modules) if graph else 0
                        ),
                        module_test_seam_coverage_count=(
                            len(graph.modules) if graph else 0
                        ),
                        module_invalidation_ref=responsibility_module_invalidation.invalidation_id,
                    )
                )
            if phase_graph_invalidation is not None:
                graph = self._repository.get_phase_graph(
                    phase_graph_invalidation.phase_graph_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-04.03:PhaseGraphInvalidated",
                        run_id=run.run_id,
                        story_id="ST-04.03",
                        artifact_identity=phase_graph_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-phase-graph/v1@1.0.0",
                        provenance=phase_graph_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(graph.source_lock_ref if graph else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(graph.ir_id if graph else "unassigned"),
                        harness_ir_hash=(graph.ir_hash if graph else "unassigned"),
                        artifact_set_id=(graph.artifact_set_id if graph else "unassigned"),
                        constitutional_report_id=(graph.constitutional_report_id if graph else "unassigned"),
                        constitutional_report_hash=(graph.constitutional_report_hash if graph else "unassigned"),
                        capability_graph_id=(graph.capability_graph_id if graph else "unassigned"),
                        capability_graph_hash=(graph.capability_graph_hash if graph else "unassigned"),
                        module_graph_id=phase_graph_invalidation.module_graph_ref,
                        module_graph_hash=(graph.module_graph_hash if graph else "unassigned"),
                        module_count=(len(graph.modules) if graph else 0),
                        phase_graph_id=phase_graph_invalidation.phase_graph_ref,
                        phase_graph_hash=(graph.graph_hash if graph else "unassigned"),
                        phase_count=(len(graph.phases) if graph else 0),
                        phase_module_coverage_count=(len(graph.module_refs) if graph else 0),
                        phase_dependency_count=(graph.dependency_count if graph else 0),
                        phase_gate_count=(graph.gate_count if graph else 0),
                        phase_initially_runnable_count=(len(graph.execution_plan.initially_runnable) if graph else 0),
                        phase_blocked_count=(len(graph.execution_plan.blocked_by) if graph else 0),
                        phase_parallel_pair_count=(len(graph.execution_plan.parallel_pairs) if graph else 0),
                        phase_invalidation_ref=phase_graph_invalidation.invalidation_id,
                    )
                )
            if phase_handoff_invalidation is not None:
                graph = self._repository.get_phase_handoff_graph(
                    phase_handoff_invalidation.handoff_graph_ref
                )
                self._observations.emit(
                    Observation(
                        event_name="ST-04.04:PhaseHandoffsInvalidated",
                        run_id=run.run_id,
                        story_id="ST-04.04",
                        artifact_identity=phase_handoff_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-phase-handoff-graph/v1@1.0.0",
                        provenance=phase_handoff_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(graph.source_lock_ref if graph else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(graph.ir_id if graph else "unassigned"),
                        harness_ir_hash=(graph.ir_hash if graph else "unassigned"),
                        artifact_set_id=(graph.artifact_set_id if graph else "unassigned"),
                        constitutional_report_id=(graph.constitutional_report_id if graph else "unassigned"),
                        constitutional_report_hash=(graph.constitutional_report_hash if graph else "unassigned"),
                        capability_graph_id=(graph.capability_graph_id if graph else "unassigned"),
                        capability_graph_hash=(graph.capability_graph_hash if graph else "unassigned"),
                        module_graph_id=(graph.module_graph_id if graph else "unassigned"),
                        module_graph_hash=(graph.module_graph_hash if graph else "unassigned"),
                        phase_graph_id=phase_handoff_invalidation.phase_graph_ref,
                        phase_graph_hash=(graph.phase_graph_hash if graph else "unassigned"),
                        context_graph_id=(graph.context_graph.context_graph_id if graph else "unassigned"),
                        context_graph_hash=(graph.context_graph.context_graph_hash if graph else "unassigned"),
                        handoff_graph_id=phase_handoff_invalidation.handoff_graph_ref,
                        handoff_graph_hash=(graph.graph_hash if graph else "unassigned"),
                        handoff_context_count=(len(graph.context_graph.contexts) if graph else 0),
                        handoff_contract_count=(len(graph.contracts) if graph else 0),
                        handoff_invalidation_ref=phase_handoff_invalidation.invalidation_id,
                    )
                )
            if context_graph_invalidation is not None:
                graph = active_context_graph
                self._observations.emit(
                    Observation(
                        event_name="ST-04.05:MinimumCompleteContextInvalidated",
                        run_id=run.run_id,
                        story_id="ST-04.05",
                        artifact_identity=context_graph_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-minimum-complete-context-graph/v1@1.0.0",
                        provenance=context_graph_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(graph.source_lock_ref if graph else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(graph.ir_id if graph else "unassigned"),
                        harness_ir_hash=(graph.ir_hash if graph else "unassigned"),
                        artifact_set_id=(graph.artifact_set_id if graph else "unassigned"),
                        constitutional_report_id=(graph.constitutional_report_id if graph else "unassigned"),
                        constitutional_report_hash=(graph.constitutional_report_hash if graph else "unassigned"),
                        capability_graph_id=(graph.capability_graph_id if graph else "unassigned"),
                        capability_graph_hash=(graph.capability_graph_hash if graph else "unassigned"),
                        module_graph_id=(graph.module_graph_id if graph else "unassigned"),
                        module_graph_hash=(graph.module_graph_hash if graph else "unassigned"),
                        phase_graph_id=(graph.phase_graph_id if graph else "unassigned"),
                        phase_graph_hash=(graph.phase_graph_hash if graph else "unassigned"),
                        handoff_graph_id=(graph.handoff_graph_id if graph else "unassigned"),
                        handoff_graph_hash=(graph.handoff_graph_hash if graph else "unassigned"),
                        minimum_context_graph_id=(graph.graph_id if graph else "unassigned"),
                        minimum_context_graph_hash=(graph.graph_hash if graph else "unassigned"),
                        context_manifest_count=(len(graph.manifests) if graph else 0),
                        context_reference_count=(len(graph.references) if graph else 0),
                        context_included_count=(graph.included_count if graph else 0),
                        context_excluded_count=(graph.excluded_count if graph else 0),
                        context_invalidation_ref=context_graph_invalidation.invalidation_id,
                    )
                )
            if skill_registry_snapshot_invalidation is not None:
                snapshot = active_skill_snapshot
                self._observations.emit(
                    Observation(
                        event_name="synthetic_skill_registry_invalidated",
                        run_id=run.run_id,
                        story_id="ST-05.01",
                        artifact_identity=skill_registry_snapshot_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-synthetic-skill-registry-snapshot/v1@1.0.0",
                        provenance=skill_registry_snapshot_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(snapshot.source_lock_ref if snapshot else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        minimum_context_graph_id=(
                            snapshot.minimum_context_graph_id if snapshot else "unassigned"
                        ),
                        minimum_context_graph_hash=(
                            snapshot.minimum_context_graph_hash if snapshot else "unassigned"
                        ),
                        skill_snapshot_id=(snapshot.snapshot_id if snapshot else "unassigned"),
                        skill_snapshot_hash=(snapshot.snapshot_hash if snapshot else "unassigned"),
                        skill_registry_id=(snapshot.registry_id if snapshot else "unassigned"),
                        skill_registry_version=(snapshot.registry_version if snapshot else "unassigned"),
                        skill_registry_hash=(snapshot.registry_hash if snapshot else "unassigned"),
                        skill_policy_id=(snapshot.policy_id if snapshot else "unassigned"),
                        skill_policy_hash=(snapshot.policy_hash if snapshot else "unassigned"),
                        skill_schema_hash=(snapshot.schema_hash if snapshot else "unassigned"),
                        skill_validation_receipt_id=(
                            snapshot.validation_receipt_id if snapshot else "unassigned"
                        ),
                        skill_validation_receipt_hash=(
                            snapshot.validation_receipt_hash if snapshot else "unassigned"
                        ),
                        skill_capability_count=(
                            len(snapshot.capability_classifications) if snapshot else 0
                        ),
                        registered_skill_count=(snapshot.registry_skill_count if snapshot else 0),
                        required_external_skill_count=(
                            snapshot.required_external_skill_count if snapshot else 0
                        ),
                        skill_invalidation_ref=(
                            skill_registry_snapshot_invalidation.invalidation_id
                        ),
                        skill_replay_status="HISTORICAL_REPRODUCTION_PRESERVED",
                    )
                )
            if skill_necessity_invalidation is not None:
                decision = active_skill_necessity
                self._observations.emit(
                    Observation(
                        event_name="synthetic_skill_necessity_invalidated",
                        run_id=run.run_id,
                        story_id="ST-05.02",
                        artifact_identity=skill_necessity_invalidation.invalidation_hash,
                        authority_identity=command.actor_id,
                        version="cmf-builder-skill-necessity-decision/v1@1.0.0",
                        provenance=skill_necessity_invalidation.upstream_invalidation_ref,
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(decision.source_lock_ref if decision else "unassigned"),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        minimum_context_graph_id=(
                            decision.minimum_context_graph_id if decision else "unassigned"
                        ),
                        minimum_context_graph_hash=(
                            decision.minimum_context_graph_hash if decision else "unassigned"
                        ),
                        skill_snapshot_id=(decision.snapshot_id if decision else "unassigned"),
                        skill_snapshot_hash=(decision.snapshot_hash if decision else "unassigned"),
                        skill_registry_id=(active_skill_snapshot.registry_id if active_skill_snapshot else "unassigned"),
                        skill_registry_version=(active_skill_snapshot.registry_version if active_skill_snapshot else "unassigned"),
                        skill_registry_hash=(decision.registry_hash if decision else "unassigned"),
                        skill_policy_id=(decision.policy_id if decision else "unassigned"),
                        skill_policy_hash=(decision.policy_hash if decision else "unassigned"),
                        skill_necessity_decision_id=(
                            decision.decision_id if decision else "unassigned"
                        ),
                        skill_necessity_decision_hash=(
                            decision.decision_hash if decision else "unassigned"
                        ),
                        skill_necessity_outcome=(
                            decision.outcome if decision else "unassigned"
                        ),
                        skill_necessity_capability_count=(
                            len(decision.capability_evidence) if decision else 0
                        ),
                        skill_target_failure_count=(
                            decision.target_failure_count if decision else 0
                        ),
                        skill_alternative_assessment_count=(
                            decision.alternative_assessment_count if decision else 0
                        ),
                        skill_missing_required_count=(
                            decision.missing_required_skills_count if decision else 0
                        ),
                        skill_adaptation_count=(
                            decision.adaptations_required_count if decision else 0
                        ),
                        skill_experiment_count=(
                            decision.experiments_required_count if decision else 0
                        ),
                        skill_jit_capsule_count=(
                            decision.jit_capsules_required_count if decision else 0
                        ),
                        skill_design_brief_count=(
                            decision.skill_design_brief_count if decision else 0
                        ),
                        skill_design_brief_disposition=(
                            decision.brief_disposition.value if decision else "unassigned"
                        ),
                        skill_necessity_invalidation_ref=(
                            skill_necessity_invalidation.invalidation_id
                        ),
                        skill_replay_status="HISTORICAL_REPRODUCTION_PRESERVED",
                    )
                )
            if atomic_harness_definition_invalidation is not None:
                definition = active_atomic_harness_definition
                self._observations.emit(
                    Observation(
                        event_name="synthetic_atomic_harness_definition_invalidated",
                        run_id=run.run_id,
                        story_id="ST-07.02",
                        artifact_identity=(
                            atomic_harness_definition_invalidation.invalidation_hash
                        ),
                        authority_identity=command.actor_id,
                        version="cmf-builder-atomic-harness-definition/v1@1.0.0",
                        provenance=(
                            atomic_harness_definition_invalidation.upstream_invalidation_ref
                        ),
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        source_lock_id=(
                            definition.source_lock_ref if definition else "unassigned"
                        ),
                        boundary_id=invalidation.boundary_ref,
                        model_id=invalidation.model_ref,
                        invalidated_artifact_ids=invalidated_artifacts,
                        harness_ir_id=(definition.ir_id if definition else "unassigned"),
                        harness_ir_hash=(definition.ir_hash if definition else "unassigned"),
                        skill_necessity_decision_id=(
                            definition.skill_necessity_decision_id
                            if definition else "unassigned"
                        ),
                        skill_necessity_decision_hash=(
                            definition.skill_necessity_decision_hash
                            if definition else "unassigned"
                        ),
                        atomic_harness_definition_id=(
                            definition.definition_id if definition else "unassigned"
                        ),
                        atomic_harness_definition_hash=(
                            definition.definition_hash if definition else "unassigned"
                        ),
                        atomic_harness_definition_section_count=(
                            len(definition.sections) if definition else 0
                        ),
                        atomic_harness_definition_external_skill_count=(
                            definition.external_skill_count if definition else 0
                        ),
                        atomic_harness_definition_external_runtime_count=(
                            definition.external_runtime_count if definition else 0
                        ),
                        atomic_harness_definition_certification=(
                            "synthetic_not_certifiable" if definition else "unassigned"
                        ),
                        atomic_harness_definition_invalidation_ref=(
                            atomic_harness_definition_invalidation.invalidation_id
                        ),
                        skill_replay_status="HISTORICAL_REPRODUCTION_PRESERVED",
                    )
                )
            if atomic_content_harness_validation_invalidation is not None:
                report = active_target_validation
                self._observations.emit(
                    Observation(
                        event_name="atomic_content_harness_validation_invalidated",
                        run_id=run.run_id,
                        story_id="ST-07.04",
                        artifact_identity=(
                            atomic_content_harness_validation_invalidation.invalidation_hash
                        ),
                        authority_identity=command.actor_id,
                        version="cmf-builder-atomic-content-harness-validation/v1@1.0.0",
                        provenance=(
                            atomic_content_harness_validation_invalidation.upstream_invalidation_ref
                        ),
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        invalidated_artifact_ids=invalidated_artifacts,
                        atomic_harness_definition_id=(
                            report.definition_id if report else "unassigned"
                        ),
                        atomic_harness_definition_hash=(
                            report.definition_hash if report else "unassigned"
                        ),
                        atomic_content_harness_validation_id=(
                            report.report_id if report else "unassigned"
                        ),
                        atomic_content_harness_validation_hash=(
                            report.report_hash if report else "unassigned"
                        ),
                        atomic_content_harness_validation_dimension_count=(
                            len(report.dimensions) if report else 0
                        ),
                        atomic_content_harness_internal_compatibility=(
                            report.internal_compatibility if report else "unassigned"
                        ),
                        atomic_content_harness_external_compatibility=(
                            report.external_target_compatibility
                            if report else "unassigned"
                        ),
                        atomic_content_harness_certification=(
                            "synthetic_not_certifiable" if report else "unassigned"
                        ),
                        atomic_content_harness_invalidation_ref=(
                            atomic_content_harness_validation_invalidation.invalidation_id
                        ),
                        atomic_content_harness_replay_status=(
                            "HISTORICAL_REPRODUCTION_PRESERVED"
                        ),
                    )
                )
            if development_capsule_invalidation is not None:
                capsule = active_development_capsule
                self._observations.emit(
                    Observation(
                        event_name="development_capsule_invalidated",
                        run_id=run.run_id,
                        story_id="ST-11.01",
                        artifact_identity=(
                            development_capsule_invalidation.invalidation_hash
                        ),
                        authority_identity=command.actor_id,
                        version="cmf-builder-versioned-traceable-development-capsule/v1@1.0.0",
                        provenance=(
                            development_capsule_invalidation.upstream_invalidation_ref
                        ),
                        outcome="PASS",
                        failure_context={},
                        correlation_id=command.correlation_id,
                        causation_id=command.causation_id,
                        command_id=command.command_id,
                        target_id=run.target_profile.target_id,
                        category_id=run.target_profile.category_id,
                        profile_id=run.target_profile.profile_id,
                        stream_version=final_run.stream_version,
                        invalidated_artifact_ids=invalidated_artifacts,
                        atomic_harness_definition_id=(
                            capsule.definition_id if capsule else "unassigned"
                        ),
                        atomic_harness_definition_hash=(
                            capsule.definition_hash if capsule else "unassigned"
                        ),
                        atomic_content_harness_validation_id=(
                            capsule.validation_id if capsule else "unassigned"
                        ),
                        atomic_content_harness_validation_hash=(
                            capsule.validation_hash if capsule else "unassigned"
                        ),
                        development_capsule_id=(
                            capsule.capsule_id if capsule else "unassigned"
                        ),
                        development_capsule_hash=(
                            capsule.capsule_hash if capsule else "unassigned"
                        ),
                        development_capsule_section_count=(
                            len(capsule.sections) if capsule else 0
                        ),
                        development_capsule_reference_count=(
                            len(capsule.references) if capsule else 0
                        ),
                        development_capsule_obligation_count=(
                            len(capsule.obligation_ids) if capsule else 0
                        ),
                        development_capsule_compatibility=(
                            capsule.internal_compatibility
                            if capsule
                            else "unassigned"
                        ),
                        development_capsule_certification=(
                            capsule.certification_state
                            if capsule
                            else "unassigned"
                        ),
                        development_capsule_invalidation_ref=(
                            development_capsule_invalidation.invalidation_id
                        ),
                        development_capsule_replay_status=(
                            "HISTORICAL_REPRODUCTION_PRESERVED"
                        ),
                    )
                )
            return receipt
        except Exception as error:
            self._reject(
                command_id=command.command_id,
                run_id=command.run_id,
                actor_id=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                run=run,
                declared=declared,
                source_lock=source_lock,
                error=error,
            )
            raise

    def consume_field(
        self,
        *,
        run_id: str,
        field_name: str,
        required_authority: AuthorityStatus,
    ) -> object:
        run = self._repository.load_run(run_id)
        if (
            not run.draft_harness_model_ref
            or run.boundary_invalidation_ref is not None
            or self._repository.is_model_invalidated(run.draft_harness_model_ref)
        ):
            raise FieldAuthorityRejected(
                "No active Draft Harness Model is available.",
                run_id=run_id,
                model_ref=run.draft_harness_model_ref,
            )
        model = self._repository.get_draft_harness_model(
            run.draft_harness_model_ref
        )
        if model is None:
            raise FieldAuthorityRejected(
                "Draft Harness Model identity is unavailable.", run_id=run_id
            )
        return model.consume(field_name, required_authority=required_authority)

    def _approve(
        self,
        command: DecideAtomicBoundaryCommand,
        run: Run,
        source_lock: SourceLock,
        declared: DeclaredBoundaryInput,
    ) -> AtomicityDecisionReceipt:
        if declared.critical_contradictions:
            raise CriticalBoundaryContradiction(
                "A critical contradiction prevents boundary freeze.",
                contradictions=declared.critical_contradictions,
            )
        boundary = DeclaredAtomicBoundary.freeze(
            declared, source_lock_ref=source_lock.lock_id
        )
        ratification = AtomicityRatification.create(
            ratification_id=self._ids.new_id("ratification"),
            boundary=boundary,
            decision=command.decision,
        )
        evaluation = AtomicityReadinessEvaluation(
            gate_id="HG-003",
            result="PASS",
            reason="The declared boundary has authorized evidence and no critical contradiction.",
            evidence_refs=(
                source_lock.aggregate_hash,
                ratification.ratification_hash,
                boundary.content_hash,
            ),
        )
        model = DraftHarnessModel.compile(
            model_id=self._ids.new_id("draft-model"),
            declared=declared,
            boundary=boundary,
            ratification=ratification,
        )
        final_run, events = run.freeze_atomic_boundary(
            boundary_ref=boundary.boundary_id,
            model_ref=model.model_id,
            ratification_ref=ratification.ratification_id,
            decision_hash=command.decision.decision_hash,
            event_ids=tuple(self._ids.new_id("event") for _ in range(4)),
            command_id=command.command_id,
            actor_id=command.actor_id,
            timestamp=self._clock.now(),
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        receipt = AtomicityDecisionReceipt.create(
            receipt_id=self._ids.new_id("receipt"),
            command_id=command.command_id,
            run_id=run.run_id,
            decision_status="APPROVED",
            authority_identity=command.actor_id,
            declared_input_hash=declared.input_hash,
            source_lock_ref=source_lock.lock_id,
            boundary_ref=boundary.boundary_id,
            model_ref=model.model_id,
            ratification_ref=ratification.ratification_id,
            invalidation_ref=None,
            event_ids=tuple(item.event_id for item in events),
            hg_003_result=evaluation.result,
        )
        self._repository.commit_atomicity(
            run_id=run.run_id,
            expected_version=command.expected_version,
            events=events,
            command_id=command.command_id,
            command_record=CommandRecord(
                payload_hash=_command_hash(command), result=receipt
            ),
            decision=command.decision,
            receipt=receipt,
            boundary=boundary,
            ratification=ratification,
            model=model,
            invalidation=None,
        )
        for event_name in (
            "ST-02.05:BoundaryRatified",
            "ST-02.05:DraftModelCompiled",
            "ST-02.05:BoundaryFrozen",
            "ST-02.05:OutcomeVerified",
        ):
            self._emit(
                event_name=event_name,
                outcome="PASS",
                command_id=command.command_id,
                actor_id=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                run=final_run,
                declared=declared,
                source_lock=source_lock,
                receipt=receipt,
                failure_context={},
            )
        return receipt

    def _record_nonapproval(
        self,
        command: DecideAtomicBoundaryCommand,
        run: Run,
        source_lock: SourceLock,
        declared: DeclaredBoundaryInput,
    ) -> AtomicityDecisionReceipt:
        status = (
            "REVISION_REQUIRED"
            if command.decision.action is AtomicityDecisionAction.REVISE
            else "REJECTED"
        )
        evaluation = AtomicityReadinessEvaluation(
            gate_id="HG-003",
            result="FAIL",
            reason=(
                "Boundary revision is required before freeze."
                if status == "REVISION_REQUIRED"
                else "The declared boundary was rejected by human authority."
            ),
            evidence_refs=command.decision.evidence_refs,
        )
        final_run, event = run.record_atomicity_decision(
            action=command.decision.action.value,
            decision_status=status,
            decision_hash=command.decision.decision_hash,
            event_id=self._ids.new_id("event"),
            command_id=command.command_id,
            actor_id=command.actor_id,
            timestamp=self._clock.now(),
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        receipt = AtomicityDecisionReceipt.create(
            receipt_id=self._ids.new_id("receipt"),
            command_id=command.command_id,
            run_id=run.run_id,
            decision_status=status,
            authority_identity=command.actor_id,
            declared_input_hash=declared.input_hash,
            source_lock_ref=source_lock.lock_id,
            boundary_ref=None,
            model_ref=None,
            ratification_ref=None,
            invalidation_ref=None,
            event_ids=(event.event_id,),
            hg_003_result=evaluation.result,
        )
        self._repository.commit_atomicity(
            run_id=run.run_id,
            expected_version=command.expected_version,
            events=(event,),
            command_id=command.command_id,
            command_record=CommandRecord(
                payload_hash=_command_hash(command), result=receipt
            ),
            decision=command.decision,
            receipt=receipt,
            boundary=None,
            ratification=None,
            model=None,
            invalidation=None,
        )
        event_name = (
            "ST-02.05:BoundaryRevisionRequested"
            if status == "REVISION_REQUIRED"
            else "ST-02.05:BoundaryRejected"
        )
        for name in (event_name, "ST-02.05:OutcomeVerified"):
            self._emit(
                event_name=name,
                outcome="PASS",
                command_id=command.command_id,
                actor_id=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                run=final_run,
                declared=declared,
                source_lock=source_lock,
                receipt=receipt,
                failure_context={},
            )
        return receipt

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> AtomicityDecisionReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "A command identity was reused with a different payload.",
                command_id=command_id,
                original_payload_hash=record.payload_hash,
                observed_payload_hash=payload_hash,
            )
        if not isinstance(record.result, AtomicityDecisionReceipt):
            raise IdempotencyPayloadMismatch(
                "Stored command result has an incompatible type.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: DecideAtomicBoundaryCommand | ReopenAtomicBoundaryCommand,
        receipt: AtomicityDecisionReceipt,
    ) -> None:
        run = self._repository.load_run(receipt.run_id)
        source_lock = self._repository.get_source_lock(receipt.source_lock_ref)
        self._emit(
            event_name="ST-02.05:DecisionReplayReturned",
            outcome="PASS",
            command_id=command.command_id,
            actor_id=command.actor_id,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            run=run,
            declared=None,
            source_lock=source_lock,
            receipt=receipt,
            failure_context={},
        )

    @staticmethod
    def _validate_decision_command(
        run: Run, command: DecideAtomicBoundaryCommand
    ) -> None:
        profile = run.target_profile
        if (
            run.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or run.source_lock_ref is None
            or run.atomic_boundary_ref is not None
            or profile.profile_id != SYNTHETIC_PROFILE_ID
            or profile.version != SYNTHETIC_PROFILE_VERSION
            or profile.category_id != SYNTHETIC_CATEGORY_ID
            or profile.supplemental_proof is None
            or not profile.supplemental_proof.synthetic
            or not profile.supplemental_proof.repository_owned
            or not profile.supplemental_proof.builder_core_validation_only
        ):
            raise AtomicityCommandRejected(
                "Only one SOURCE_LOCKED synthetic Builder Core run may enter declared-boundary ratification.",
                lifecycle_state=run.lifecycle_state.value,
                profile_ref=profile.profile_ref,
            )
        if command.expected_version != run.stream_version:
            raise AtomicityCommandRejected(
                "Expected stream version does not match the loaded run.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        if (
            command.declared_input_path != DECLARED_INPUT_PATH
            or command.declared_input_sha256 != DECLARED_INPUT_SHA256
        ):
            raise AtomicityCommandRejected(
                "The command attempts to substitute an ungoverned boundary input.",
                declared_input_path=command.declared_input_path,
                declared_input_sha256=command.declared_input_sha256,
            )

    def _required_source_lock(self, run: Run) -> SourceLock:
        source_lock = (
            self._repository.get_source_lock(run.source_lock_ref)
            if run.source_lock_ref
            else None
        )
        if source_lock is None or source_lock.run_id != run.run_id:
            raise BoundaryInputMismatch(
                "The run does not carry its authoritative Source Lock.",
                run_id=run.run_id,
                source_lock_ref=run.source_lock_ref,
            )
        return source_lock

    def _load_declared(
        self, command: DecideAtomicBoundaryCommand
    ) -> DeclaredBoundaryInput:
        return self._declared_inputs.load(
            command.declared_input_path, command.declared_input_sha256
        )

    @staticmethod
    def _validate_declared_against_run(
        declared: DeclaredBoundaryInput, run: Run, source_lock: SourceLock
    ) -> None:
        descriptor_hashes = {item.sha256 for item in source_lock.ordered_descriptors}
        expected_profile_ref = f"{run.target_profile.profile_id}@{run.target_profile.version}"
        if (
            source_lock.source_profile_ref != declared.source_profile_ref
            or source_lock.source_profile_hash != declared.source_profile_hash
            or source_lock.target_profile_ref != declared.target_profile_ref
            or source_lock.target_candidate_ref != declared.target_candidate_ref
            or declared.target_candidate_hash not in descriptor_hashes
            or declared.target_profile_ref != expected_profile_ref
            or declared.category_binding != "none"
            or not declared.synthetic
            or not declared.repository_owned
            or declared.production_eligible
            or declared.certified
        ):
            raise BoundaryInputMismatch(
                "Declared boundary does not match the immutable Source Lock and synthetic profile.",
                source_lock_ref=source_lock.lock_id,
                source_profile_ref=source_lock.source_profile_ref,
                target_profile_ref=source_lock.target_profile_ref,
            )

    def _reject(
        self,
        *,
        command_id: str,
        run_id: str,
        actor_id: str,
        correlation_id: str,
        causation_id: str,
        run: Run | None,
        declared: DeclaredBoundaryInput | None,
        source_lock: SourceLock | None,
        error: Exception,
    ) -> None:
        if not hasattr(error, "code"):
            return
        context = {
            "code": str(getattr(error, "code")),
            **getattr(error, "context", {}),
        }
        for event_name in (
            "ST-02.05:BoundaryDecisionRejected",
            "ST-02.05:OutcomeRejected",
        ):
            self._emit(
                event_name=event_name,
                outcome="FAIL",
                command_id=command_id,
                actor_id=actor_id,
                correlation_id=correlation_id,
                causation_id=causation_id,
                run=run,
                declared=declared,
                source_lock=source_lock,
                receipt=None,
                failure_context=context,
            )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command_id: str,
        actor_id: str,
        correlation_id: str,
        causation_id: str,
        run: Run | None,
        declared: DeclaredBoundaryInput | None,
        source_lock: SourceLock | None,
        receipt: AtomicityDecisionReceipt | None,
        failure_context: dict[str, object],
        invalidated_artifacts: tuple[str, ...] = (),
    ) -> None:
        boundary = (
            self._repository.get_atomic_boundary(receipt.boundary_ref)
            if receipt and receipt.boundary_ref
            else None
        )
        model = (
            self._repository.get_draft_harness_model(receipt.model_ref)
            if receipt and receipt.model_ref
            else None
        )
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=run.run_id if run else "unassigned",
                story_id=self.STORY_ID,
                artifact_identity=(
                    model.model_hash
                    if model
                    else (boundary.content_hash if boundary else (run.state_hash() if run else "Atomicity"))
                ),
                authority_identity=actor_id,
                version=self.CONTRACT_VERSION,
                provenance=self.STORY_ID,
                outcome=outcome,
                failure_context=dict(failure_context),
                correlation_id=correlation_id,
                causation_id=causation_id,
                command_id=command_id,
                target_id=run.target_profile.target_id if run else "atomic_content_harness",
                category_id=run.target_profile.category_id if run else SYNTHETIC_CATEGORY_ID,
                profile_id=run.target_profile.profile_id if run else SYNTHETIC_PROFILE_ID,
                stream_version=run.stream_version if run else 0,
                source_profile_id=(
                    source_lock.source_profile_ref.split("@", 1)[0]
                    if source_lock
                    else "unassigned"
                ),
                source_profile_version=(
                    source_lock.source_profile_ref.split("@", 1)[1]
                    if source_lock and "@" in source_lock.source_profile_ref
                    else "unassigned"
                ),
                source_profile_hash=(
                    source_lock.source_profile_hash if source_lock else "unassigned"
                ),
                target_candidate=(
                    source_lock.target_candidate_ref if source_lock else "unassigned"
                ),
                source_lock_id=source_lock.lock_id if source_lock else "unassigned",
                declared_input_hash=(
                    receipt.declared_input_hash
                    if receipt
                    else (declared.input_hash if declared else "unassigned")
                ),
                boundary_id=receipt.boundary_ref if receipt and receipt.boundary_ref else "unassigned",
                boundary_version=boundary.version if boundary else "unassigned",
                boundary_status=(
                    "INVALIDATED"
                    if receipt and receipt.invalidation_ref
                    else (boundary.status.value if boundary else "unassigned")
                ),
                selected_candidate=boundary.candidate_id if boundary else "unassigned",
                model_id=receipt.model_ref if receipt and receipt.model_ref else "unassigned",
                model_hash=model.model_hash if model else "unassigned",
                model_status=model.status.value if model else "unassigned",
                decision_receipt_id=receipt.receipt_id if receipt else "unassigned",
                decision_receipt_hash=receipt.receipt_hash if receipt else "unassigned",
                decision_action=receipt.decision_status if receipt else "unassigned",
                hg_003=receipt.hg_003_result if receipt else "FAIL",
                invalidated_artifact_ids=invalidated_artifacts,
            )
        )


def _command_hash(
    command: DecideAtomicBoundaryCommand | ReopenAtomicBoundaryCommand,
) -> str:
    payload = _canonical_value(asdict(command))
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (set, frozenset)):
        return sorted(_canonical_value(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
