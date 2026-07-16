from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.application.authority import (
    Action,
    ActorKind,
    AuthorityService,
)
from cmf_builder.application.ports import (
    AtomicHarnessDefinitionRepository,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
    IdProvider,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomic_harness_definition import (
    ACCEPTANCE_TEST_DECLARATIONS,
    CATEGORY_ADAPTER_REF,
    DEFINITION_COMPILER_VERSION,
    DEFINITION_INPUT_PATH,
    DEFINITION_INPUT_SHA256,
    DEFINITION_SCOPE,
    PROFILE_ID,
    REQUIRED_SECTIONS,
    TARGET_KIND,
    AtomicHarnessDefinition,
    AtomicHarnessDefinitionReceipt,
    DefinitionAuthorityInvalid,
    DefinitionInputInvalid,
    DefinitionInvalidatedError,
    DefinitionLineageInvalid,
    DefinitionScopeInvalid,
)
from cmf_builder.domain.atomicity import (
    AtomicityRatification,
    DeclaredAtomicBoundary,
    DraftHarnessModel,
)
from cmf_builder.domain.capability_ownership import CapabilityOwnershipGraph
from cmf_builder.domain.constitutional_validation import ConstitutionalValidationReport
from cmf_builder.domain.context_manifest import MinimumCompleteContextGraph
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.generated_artifacts import (
    ArtifactManifest,
    ReproducibleBuildConfig,
)
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


@dataclass(frozen=True, slots=True)
class CompileAtomicHarnessDefinitionCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    definition_input_path: str = DEFINITION_INPUT_PATH
    definition_input_sha256: str = DEFINITION_INPUT_SHA256
    requested_operation: str = "compile_atomic_harness_definition"
    requested_target_kind: str = TARGET_KIND
    requested_profile_id: str = PROFILE_ID
    requested_category_adapter_ref: str = CATEGORY_ADAPTER_REF
    requested_required_sections: tuple[str, ...] = REQUIRED_SECTIONS
    requested_external_runtime_ids: tuple[str, ...] = ()
    requested_external_skill_ids: tuple[str, ...] = ()
    requested_production_eligible: bool = False
    requested_certified: bool = False
    requested_synthetic_not_certifiable: bool = True
    lineage_overrides: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class _ActiveDefinitionInputs:
    run: Run
    source_lock: SourceLock
    boundary: DeclaredAtomicBoundary
    ratification: AtomicityRatification
    model: DraftHarnessModel
    ir: HarnessIR
    manifest: ArtifactManifest
    constitutional: ConstitutionalValidationReport
    capability: CapabilityOwnershipGraph
    modules: ResponsibilityModuleGraph
    phases: PhaseGraph
    handoff_graph: PhaseHandoffGraph
    accepted_handoff: InternalHandoff
    handoff_decision: InternalHandoffDecision
    context: MinimumCompleteContextGraph
    snapshot: SyntheticSkillRegistrySnapshot
    necessity: SkillNecessityDecision


class SyntheticAtomicHarnessDefinitionCommandService:
    STORY_ID = "ST-07.02"
    CONTRACT_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        root: Path,
        repository: AtomicHarnessDefinitionRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._root = root.resolve()
        self._repository = repository
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def compile(
        self, command: CompileAtomicHarnessDefinitionCommand
    ) -> AtomicHarnessDefinitionReceipt:
        inputs: _ActiveDefinitionInputs | None = None
        definition: AtomicHarnessDefinition | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            self._load_and_validate_input(command)
            inputs = self._load_active_inputs(run)
            definition = AtomicHarnessDefinition.create(
                run=inputs.run,
                source_lock=inputs.source_lock,
                boundary=inputs.boundary,
                ratification=inputs.ratification,
                model=inputs.model,
                ir=inputs.ir,
                manifest=inputs.manifest,
                constitutional=inputs.constitutional,
                capability=inputs.capability,
                modules=inputs.modules,
                phases=inputs.phases,
                handoff_graph=inputs.handoff_graph,
                accepted_handoff=inputs.accepted_handoff,
                handoff_decision=inputs.handoff_decision,
                context=inputs.context,
                snapshot=inputs.snapshot,
                necessity=inputs.necessity,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_atomic_harness_definition(
                definition_ref=definition.definition_id,
                definition_hash=definition.definition_hash,
                skill_necessity_ref=definition.skill_necessity_decision_id,
                skill_necessity_hash=definition.skill_necessity_decision_hash,
                section_count=len(definition.sections),
                external_skill_count=definition.external_skill_count,
                external_runtime_count=definition.external_runtime_count,
                synthetic_not_certifiable=definition.synthetic_not_certifiable,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = AtomicHarnessDefinitionReceipt.create(
                command_id=command.command_id,
                definition=definition,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_atomic_harness_definition(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                definition=definition,
                receipt=receipt,
            )
            for event_name in (
                "synthetic_atomic_harness_definition_started",
                "synthetic_atomic_harness_definition_validated",
                "synthetic_atomic_harness_definition_committed",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    inputs=inputs,
                    definition=definition,
                    receipt=receipt,
                    run=final_run,
                    replay_status="NEW_COMMIT",
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="synthetic_atomic_harness_definition_rejected",
                outcome="FAIL",
                command=command,
                inputs=inputs,
                definition=definition,
                receipt=None,
                run=(inputs.run if inputs else None),
                replay_status="NOT_COMMITTED",
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> AtomicHarnessDefinition:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.atomic_harness_definition_ref
            or run.atomic_harness_definition_invalidation_ref is not None
            or self._repository.is_atomic_harness_definition_invalidated(
                run.atomic_harness_definition_ref
            )
        ):
            raise DefinitionInvalidatedError(
                "No active synthetic Atomic Harness Definition is available."
            )
        definition = self._repository.get_atomic_harness_definition(
            run.atomic_harness_definition_ref
        )
        if (
            definition is None
            or definition.definition_hash != run.atomic_harness_definition_hash
        ):
            raise DefinitionInvalidatedError(
                "The active Atomic Harness Definition is missing or altered."
            )
        inputs = self._load_active_inputs(run, allow_existing_definition=True)
        self._validate_definition(definition, inputs)
        return definition

    def get_historical(self, definition_id: str) -> AtomicHarnessDefinition:
        definition = self._repository.get_atomic_harness_definition(definition_id)
        if definition is None:
            raise KeyError(definition_id)
        events = self._repository.events(definition.run_id)
        cutoff = next(
            (
                index
                for index, event in enumerate(events)
                if event.event_type == "AtomicHarnessDefinitionAttached"
                and event.value("definition_ref")
                == definition.definition_id
            ),
            None,
        )
        if cutoff is None:
            raise DefinitionLineageInvalid(
                "Historical definition attachment event is unavailable."
            )
        run = Run.replay(events[: cutoff + 1])
        inputs = self._load_historical_inputs(run, definition)
        self._validate_definition(definition, inputs)
        return definition

    def _load_active_inputs(
        self, run: Run, *, allow_existing_definition: bool = False
    ) -> _ActiveDefinitionInputs:
        refs = (
            run.source_lock_ref,
            run.atomic_boundary_ref,
            run.atomicity_ratification_ref,
            run.draft_harness_model_ref,
            run.harness_ir_ref,
            run.artifact_manifest_ref,
            run.constitutional_validation_ref,
            run.capability_ownership_ref,
            run.responsibility_module_ref,
            run.phase_graph_ref,
            run.phase_handoff_ref,
            run.minimum_context_ref,
            run.skill_registry_snapshot_ref,
            run.skill_necessity_ref,
        )
        invalidations = (
            run.boundary_invalidation_ref,
            run.harness_ir_invalidation_ref,
            run.artifact_set_invalidation_ref,
            run.constitutional_validation_invalidation_ref,
            run.capability_ownership_invalidation_ref,
            run.responsibility_module_invalidation_ref,
            run.phase_graph_invalidation_ref,
            run.phase_handoff_invalidation_ref,
            run.minimum_context_invalidation_ref,
            run.skill_registry_snapshot_invalidation_ref,
            run.skill_necessity_invalidation_ref,
        )
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not all(refs)
            or any(invalidations)
            or (run.atomic_harness_definition_ref is not None and not allow_existing_definition)
            or run.atomic_harness_definition_invalidation_ref is not None
        ):
            raise DefinitionInvalidatedError(
                "Definition compilation requires the complete exact active Builder Core lineage."
            )
        source_lock = self._repository.get_source_lock(run.source_lock_ref or "")
        boundary = self._repository.get_atomic_boundary(run.atomic_boundary_ref or "")
        ratification = self._repository.get_atomicity_ratification(
            run.atomicity_ratification_ref or ""
        )
        model = self._repository.get_draft_harness_model(
            run.draft_harness_model_ref or ""
        )
        ir = self._repository.get_harness_ir(run.harness_ir_ref or "")
        manifest = self._repository.get_artifact_manifest(
            run.artifact_manifest_ref or ""
        )
        constitutional = self._repository.get_constitutional_validation_report(
            run.constitutional_validation_ref or ""
        )
        capability = self._repository.get_capability_ownership_graph(
            run.capability_ownership_ref or ""
        )
        modules = self._repository.get_responsibility_module_graph(
            run.responsibility_module_ref or ""
        )
        phases = self._repository.get_phase_graph(run.phase_graph_ref or "")
        handoff_graph = self._repository.get_phase_handoff_graph(
            run.phase_handoff_ref or ""
        )
        context = self._repository.get_minimum_context_graph(
            run.minimum_context_ref or ""
        )
        snapshot = self._repository.get_skill_registry_snapshot(
            run.skill_registry_snapshot_ref or ""
        )
        necessity = self._repository.get_skill_necessity_decision(
            run.skill_necessity_ref or ""
        )
        accepted_handoff = (
            self._repository.get_internal_handoff(context.accepted_handoff_id)
            if context
            else None
        )
        handoff_decision = (
            self._repository.get_internal_handoff_decision(
                context.accepted_handoff_id
            )
            if context
            else None
        )
        values = (
            source_lock, boundary, ratification, model, ir, manifest,
            constitutional, capability, modules, phases, handoff_graph,
            accepted_handoff, handoff_decision, context, snapshot, necessity,
        )
        if any(value is None for value in values):
            raise DefinitionLineageInvalid(
                "One or more governed definition inputs cannot be reproduced."
            )
        inputs = _ActiveDefinitionInputs(
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
        self._validate_active_inputs(inputs)
        return inputs

    def _load_historical_inputs(
        self, run: Run, definition: AtomicHarnessDefinition
    ) -> _ActiveDefinitionInputs:
        source_lock = self._repository.get_source_lock(definition.source_lock_ref)
        boundary = self._repository.get_atomic_boundary(definition.boundary_ref)
        ratification = self._repository.get_atomicity_ratification(
            definition.ratification_ref
        )
        model = self._repository.get_draft_harness_model(definition.model_ref)
        ir = self._repository.get_harness_ir(definition.ir_id)
        manifest = self._repository.get_artifact_manifest(
            definition.artifact_manifest_id
        )
        constitutional = self._repository.get_constitutional_validation_report(
            definition.constitutional_report_id
        )
        capability = self._repository.get_capability_ownership_graph(
            definition.capability_graph_id
        )
        modules = self._repository.get_responsibility_module_graph(
            definition.module_graph_id
        )
        phases = self._repository.get_phase_graph(definition.phase_graph_id)
        handoff_graph = self._repository.get_phase_handoff_graph(
            definition.handoff_graph_id
        )
        accepted_handoff = self._repository.get_internal_handoff(
            definition.accepted_handoff_id
        )
        context = self._repository.get_minimum_context_graph(
            definition.minimum_context_graph_id
        )
        snapshot = self._repository.get_skill_registry_snapshot(
            definition.skill_snapshot_id
        )
        necessity = self._repository.get_skill_necessity_decision(
            definition.skill_necessity_decision_id
        )
        handoff_decision = (
            self._repository.get_internal_handoff_decision(
                context.accepted_handoff_id
            )
            if context
            else None
        )
        values = (
            source_lock, boundary, ratification, model, ir, manifest,
            constitutional, capability, modules, phases, handoff_graph,
            accepted_handoff, handoff_decision, context, snapshot, necessity,
        )
        if any(value is None for value in values):
            raise DefinitionLineageInvalid("Historical definition lineage is unavailable.")
        return _ActiveDefinitionInputs(
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

    def _validate_active_inputs(self, inputs: _ActiveDefinitionInputs) -> None:
        run = inputs.run
        invalid = (
            self._repository.is_boundary_invalidated(inputs.boundary.boundary_id)
            or self._repository.is_model_invalidated(inputs.model.model_id)
            or self._repository.is_harness_ir_invalidated(inputs.ir.ir_id)
            or self._repository.is_artifact_set_invalidated(inputs.manifest.artifact_set_id)
            or self._repository.is_constitutional_validation_invalidated(
                inputs.constitutional.report_id
            )
            or self._repository.is_capability_ownership_invalidated(
                inputs.capability.graph_id
            )
            or self._repository.is_responsibility_module_invalidated(
                inputs.modules.graph_id
            )
            or self._repository.is_phase_graph_invalidated(inputs.phases.graph_id)
            or self._repository.is_phase_handoff_invalidated(
                inputs.handoff_graph.graph_id
            )
            or self._repository.is_minimum_context_invalidated(inputs.context.graph_id)
            or self._repository.is_skill_registry_snapshot_invalidated(
                inputs.snapshot.snapshot_id
            )
            or self._repository.is_skill_necessity_invalidated(
                inputs.necessity.decision_id
            )
        )
        if invalid:
            raise DefinitionInvalidatedError("An upstream definition input is invalidated.")
        inputs.ir.validate()
        build = ReproducibleBuildConfig(
            compiler_id=inputs.manifest.compiler_id,
            compiler_version=inputs.manifest.compiler_version,
            config_version=inputs.manifest.config_version,
            generation_timestamp=inputs.manifest.generation_timestamp,
        )
        inputs.manifest.validate(inputs.ir, build)
        inputs.constitutional.validate()
        inputs.capability.validate()
        inputs.modules.validate(inputs.capability)
        inputs.phases.validate(inputs.modules)
        inputs.handoff_graph.validate(inputs.phases)
        inputs.accepted_handoff.validate(inputs.handoff_graph, inputs.phases)
        inputs.handoff_decision.validate(
            inputs.accepted_handoff,
            inputs.handoff_decision.receiver_authority,
        )
        inputs.context.validate(
            inputs.handoff_graph,
            inputs.phases,
            inputs.accepted_handoff,
            inputs.handoff_decision,
        )
        inputs.snapshot.validate(inputs.context)
        inputs.necessity.validate(inputs.snapshot, inputs.context)
        if (
            inputs.handoff_decision.action is not InternalHandoffDecisionAction.ACCEPTED
            or inputs.necessity.outcome != "NO_NEW_SKILL_REQUIRED"
            or inputs.necessity.external_skills_required_count
            or inputs.necessity.missing_required_skills_count
            or inputs.snapshot.registry_skill_count
            or inputs.snapshot.required_external_skill_count
            or run.target_profile.supplemental_proof is None
            or not run.target_profile.supplemental_proof.synthetic
            or not run.target_profile.supplemental_proof.repository_owned
            or not run.target_profile.supplemental_proof.non_production
            or not run.target_profile.supplemental_proof.non_certified
            or run.target_profile.profile_id != PROFILE_ID
            or inputs.ir.category_binding != "none_test_only"
            or inputs.ir.production_eligible
            or inputs.ir.certified
        ):
            raise DefinitionScopeInvalid(
                "Upstream evidence does not support the synthetic definition scope."
            )

    def _validate_definition(
        self,
        definition: AtomicHarnessDefinition,
        inputs: _ActiveDefinitionInputs,
    ) -> None:
        definition.validate(
            run=inputs.run,
            source_lock=inputs.source_lock,
            boundary=inputs.boundary,
            ratification=inputs.ratification,
            model=inputs.model,
            ir=inputs.ir,
            manifest=inputs.manifest,
            constitutional=inputs.constitutional,
            capability=inputs.capability,
            modules=inputs.modules,
            phases=inputs.phases,
            handoff_graph=inputs.handoff_graph,
            accepted_handoff=inputs.accepted_handoff,
            handoff_decision=inputs.handoff_decision,
            context=inputs.context,
            snapshot=inputs.snapshot,
            necessity=inputs.necessity,
        )

    def _load_and_validate_input(
        self, command: CompileAtomicHarnessDefinitionCommand
    ) -> dict[str, object]:
        path = self._verified_file(
            command.definition_input_path,
            command.definition_input_sha256,
        )
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise DefinitionInputInvalid(
                "The governed definition input is unreadable or invalid JSON."
            ) from error
        target = value.get("target", {})
        task = value.get("atomic_task", {})
        skills = value.get("skill_expectation", {})
        if (
            value.get("schema_version")
            != "cmf-builder-synthetic-atomic-harness-definition-input/v1"
            or value.get("scope") != DEFINITION_SCOPE
            or target.get("target_kind") != TARGET_KIND
            or target.get("profile_id") != PROFILE_ID
            or target.get("category_binding") != "none"
            or target.get("category_adapter_ref") != CATEGORY_ADAPTER_REF
            or not target.get("synthetic")
            or not target.get("synthetic_not_certifiable")
            or target.get("production_eligible")
            or target.get("certified")
            or task.get("task_id") != "synthetic_utf8_line_ending_normalization"
            or task.get("execution_owned_by_this_story")
            or set(value.get("required_definition_sections", ()))
            != set(REQUIRED_SECTIONS)
            or len(value.get("required_definition_sections", ()))
            != len(REQUIRED_SECTIONS)
            or set(value.get("acceptance_test_declarations", ()))
            != set(ACCEPTANCE_TEST_DECLARATIONS)
            or len(value.get("acceptance_test_declarations", ()))
            != len(ACCEPTANCE_TEST_DECLARATIONS)
            or any((
                skills.get("external_skills_required"),
                skills.get("missing_required_skills"),
                skills.get("adaptations_required"),
                skills.get("experiments_required"),
                skills.get("jit_capsules_required"),
                skills.get("skill_execution_required"),
            ))
            or value.get("expected_outcome")
            != "SYNTHETIC_ATOMIC_HARNESS_DEFINITION_COMPILED"
            or value.get("execution_performed")
            or value.get("development_capsule_generated")
        ):
            raise DefinitionInputInvalid(
                "The governed definition input is incomplete or semantically broadened."
            )
        return value

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        if (
            relative_path != DEFINITION_INPUT_PATH
            or expected_sha256 != DEFINITION_INPUT_SHA256
        ):
            raise DefinitionInputInvalid(
                "The definition input pin differs from capsule authority."
            )
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise DefinitionInputInvalid(
                "The definition input is missing or escapes the repository."
            ) from error
        if observed != expected_sha256:
            raise DefinitionInputInvalid(
                "The definition input hash does not match capsule authority.",
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    def _validate_command(self, command: CompileAtomicHarnessDefinitionCommand) -> None:
        if (
            not all(value.strip() for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
            ))
            or command.expected_version < 1
            or command.requested_operation != "compile_atomic_harness_definition"
            or command.requested_target_kind != TARGET_KIND
            or command.requested_profile_id != PROFILE_ID
            or command.requested_category_adapter_ref != CATEGORY_ADAPTER_REF
            or command.requested_required_sections != REQUIRED_SECTIONS
        ):
            raise DefinitionInputInvalid("Definition command identity or contract is invalid.")
        if command.requested_external_runtime_ids:
            raise DefinitionScopeInvalid("External runtime injection is prohibited.")
        if command.requested_external_skill_ids:
            raise DefinitionScopeInvalid("External skill injection is prohibited.")
        if command.requested_production_eligible or command.requested_certified:
            raise DefinitionAuthorityInvalid(
                "The synthetic definition cannot claim production eligibility or certification."
            )
        if not command.requested_synthetic_not_certifiable:
            raise DefinitionAuthorityInvalid(
                "The synthetic_not_certifiable marker cannot be removed."
            )
        if command.lineage_overrides:
            raise DefinitionLineageInvalid(
                "Command-supplied lineage overrides are not authoritative.",
                overrides=command.lineage_overrides,
            )

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise DefinitionAuthorityInvalid(
                "Only deterministic Builder code may compile the definition."
            )

    @staticmethod
    def _require_version(expected_version: int, run: Run) -> None:
        if expected_version != run.stream_version:
            raise ConcurrencyConflict(
                "Expected stream version does not match authoritative state.",
                expected_version=expected_version,
                current_version=run.stream_version,
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> AtomicHarnessDefinitionReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, AtomicHarnessDefinitionReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileAtomicHarnessDefinitionCommand,
        receipt: AtomicHarnessDefinitionReceipt,
    ) -> None:
        definition = self._repository.get_atomic_harness_definition(
            receipt.definition_id
        )
        run = self._repository.load_run(command.run_id)
        if definition is None:
            raise DefinitionLineageInvalid("Replayed definition is unavailable.")
        inputs = self._load_active_inputs(run, allow_existing_definition=True)
        self._emit(
            event_name="synthetic_atomic_harness_definition_replayed",
            outcome="PASS",
            command=command,
            inputs=inputs,
            definition=definition,
            receipt=receipt,
            run=run,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileAtomicHarnessDefinitionCommand,
        inputs: _ActiveDefinitionInputs | None,
        definition: AtomicHarnessDefinition | None,
        receipt: AtomicHarnessDefinitionReceipt | None,
        run: Run | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        context = inputs.context if inputs else None
        snapshot = inputs.snapshot if inputs else None
        necessity = inputs.necessity if inputs else None
        self._observations.emit(Observation(
            event_name=event_name,
            run_id=command.run_id,
            story_id=self.STORY_ID,
            artifact_identity=(definition.definition_id if definition else "unassigned"),
            authority_identity=command.actor_id,
            version=self.CONTRACT_VERSION,
            provenance=(definition.definition_hash if definition else "unassigned"),
            outcome=outcome,
            failure_context=failure_context,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=(profile.target_id if profile else command.requested_target_kind),
            category_id=(profile.category_id if profile else "none"),
            profile_id=(profile.profile_id if profile else command.requested_profile_id),
            stream_version=(run.stream_version if run else command.expected_version),
            source_profile_hash=(definition.profile_source_hash if definition else "unassigned"),
            source_lock_id=(definition.source_lock_ref if definition else "unassigned"),
            boundary_id=(definition.boundary_ref if definition else "unassigned"),
            model_id=(definition.model_ref if definition else "unassigned"),
            harness_ir_id=(definition.ir_id if definition else "unassigned"),
            harness_ir_hash=(definition.ir_hash if definition else "unassigned"),
            artifact_set_id=(definition.artifact_set_id if definition else "unassigned"),
            artifact_manifest_id=(definition.artifact_manifest_id if definition else "unassigned"),
            artifact_manifest_hash=(definition.artifact_manifest_hash if definition else "unassigned"),
            constitutional_report_id=(definition.constitutional_report_id if definition else "unassigned"),
            constitutional_report_hash=(definition.constitutional_report_hash if definition else "unassigned"),
            capability_graph_id=(definition.capability_graph_id if definition else "unassigned"),
            capability_graph_hash=(definition.capability_graph_hash if definition else "unassigned"),
            module_graph_id=(definition.module_graph_id if definition else "unassigned"),
            module_graph_hash=(definition.module_graph_hash if definition else "unassigned"),
            phase_graph_id=(definition.phase_graph_id if definition else "unassigned"),
            phase_graph_hash=(definition.phase_graph_hash if definition else "unassigned"),
            handoff_graph_id=(definition.handoff_graph_id if definition else "unassigned"),
            handoff_graph_hash=(definition.handoff_graph_hash if definition else "unassigned"),
            internal_handoff_id=(definition.accepted_handoff_id if definition else "unassigned"),
            internal_handoff_hash=(definition.accepted_handoff_hash if definition else "unassigned"),
            minimum_context_graph_id=(definition.minimum_context_graph_id if definition else "unassigned"),
            minimum_context_graph_hash=(definition.minimum_context_graph_hash if definition else "unassigned"),
            context_manifest_count=(len(context.manifests) if context else 0),
            skill_snapshot_id=(definition.skill_snapshot_id if definition else "unassigned"),
            skill_snapshot_hash=(definition.skill_snapshot_hash if definition else "unassigned"),
            skill_registry_id=(snapshot.registry_id if snapshot else "unassigned"),
            skill_registry_version=(snapshot.registry_version if snapshot else "unassigned"),
            skill_registry_hash=(snapshot.registry_hash if snapshot else "unassigned"),
            skill_necessity_decision_id=(definition.skill_necessity_decision_id if definition else "unassigned"),
            skill_necessity_decision_hash=(definition.skill_necessity_decision_hash if definition else "unassigned"),
            skill_necessity_outcome=(necessity.outcome if necessity else "unassigned"),
            skill_replay_status=replay_status,
            atomic_harness_definition_id=(definition.definition_id if definition else "unassigned"),
            atomic_harness_definition_hash=(definition.definition_hash if definition else "unassigned"),
            atomic_harness_definition_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
            atomic_harness_definition_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
            atomic_harness_definition_section_count=(len(definition.sections) if definition else 0),
            atomic_harness_definition_external_skill_count=(definition.external_skill_count if definition else 0),
            atomic_harness_definition_external_runtime_count=(definition.external_runtime_count if definition else 0),
            atomic_harness_definition_certification=("synthetic_not_certifiable" if definition else "unassigned"),
            atomic_harness_definition_milestone=(receipt.initial_atomic_harness_definition_milestone if receipt else "unassigned"),
        ))


def _command_hash(command: CompileAtomicHarnessDefinitionCommand) -> str:
    value = json.dumps(
        asdict(command),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{sha256(value).hexdigest()}"
