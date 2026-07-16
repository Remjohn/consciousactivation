from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    AtomicCommitFailed,
    AtomicContentHarnessValidationRepository,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdempotencyPayloadMismatch,
    IdProvider,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomic_harness_definition import (
    DEFINITION_INPUT_PATH,
    DEFINITION_INPUT_SHA256,
    PROFILE_ID,
    REQUIRED_SECTIONS,
    TARGET_KIND,
    AtomicHarnessDefinition,
)
from cmf_builder.domain.run import LifecycleState, Run
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    INTERNAL_COMPATIBILITY,
    REQUIRED_VALIDATION_DIMENSIONS,
    VALIDATION_OUTCOME,
    VALIDATION_POLICY_PATH,
    VALIDATION_POLICY_SHA256,
    VALIDATION_SCOPE,
    AtomicContentHarnessValidationReceipt,
    AtomicContentHarnessValidationReport,
    TargetValidationAuthorityInvalid,
    TargetValidationInputInvalid,
    TargetValidationInvalidatedError,
    TargetValidationLineageInvalid,
    TargetValidationScopeInvalid,
)


@dataclass(frozen=True, slots=True)
class ValidateAtomicContentHarnessCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    policy_path: str = VALIDATION_POLICY_PATH
    policy_sha256: str = VALIDATION_POLICY_SHA256
    requested_operation: str = "validate_atomic_content_harness"
    requested_target_kind: str = TARGET_KIND
    requested_profile_id: str = PROFILE_ID
    requested_dimensions: tuple[str, ...] = REQUIRED_VALIDATION_DIMENSIONS
    requested_internal_compatibility: str = INTERNAL_COMPATIBILITY
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY
    requested_production_eligible: bool = False
    requested_certified: bool = False
    requested_synthetic_not_certifiable: bool = True
    field_overrides: tuple[tuple[str, str], ...] = ()
    lineage_overrides: tuple[tuple[str, str], ...] = ()


class AtomicContentHarnessValidationCommandService:
    STORY_ID = "ST-07.04"
    CONTRACT_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        root: Path,
        repository: AtomicContentHarnessValidationRepository,
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

    def validate(
        self, command: ValidateAtomicContentHarnessCommand
    ) -> AtomicContentHarnessValidationReceipt:
        run: Run | None = None
        definition: AtomicHarnessDefinition | None = None
        report: AtomicContentHarnessValidationReport | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._deliver_pending(command.command_id)
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            self._load_policy(command)
            definition = self._load_active_definition(run)
            report = AtomicContentHarnessValidationReport.create(
                definition=definition,
                authority_identity=command.actor_id,
                definition_authority_identity=definition.authority_identity,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_atomic_content_harness_validation(
                validation_ref=report.report_id,
                validation_hash=report.report_hash,
                definition_ref=report.definition_id,
                definition_hash=report.definition_hash,
                dimension_count=len(report.dimensions),
                section_count=len(report.section_ids),
                internal_compatibility=report.internal_compatibility,
                external_target_compatibility=report.external_target_compatibility,
                synthetic_not_certifiable=report.synthetic_not_certifiable,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = AtomicContentHarnessValidationReceipt.create(
                command_id=command.command_id,
                report=report,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            observation_intents = (
                self._observation(
                    event_name="atomic_content_harness_validation_started",
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    definition=definition,
                    report=report,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={},
                ),
                *(
                    self._observation(
                        event_name=(
                            "atomic_content_harness_dimension_"
                            f"{dimension.dimension_id}"
                        ),
                        outcome="PASS",
                        command=command,
                        run=final_run,
                        definition=definition,
                        report=report,
                        receipt=receipt,
                        replay_status="NEW_COMMIT",
                        failure_context={"dimension": dimension.dimension_id},
                    )
                    for dimension in report.dimensions
                ),
                self._observation(
                    event_name="atomic_content_harness_validation_committed",
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    definition=definition,
                    report=report,
                    receipt=receipt,
                    replay_status="NEW_COMMIT",
                    failure_context={},
                ),
            )
            self._repository.commit_atomic_content_harness_validation(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                report=report,
                receipt=receipt,
                observations=observation_intents,
            )
            self._deliver_pending(command.command_id)
            return receipt
        except Exception as error:
            if not isinstance(error, AtomicCommitFailed):
                self._emit_best_effort(
                    event_name="atomic_content_harness_validation_rejected",
                    outcome="FAIL",
                    command=command,
                    run=run,
                    definition=definition,
                    report=report,
                    receipt=None,
                    replay_status="NOT_COMMITTED",
                    failure_context={
                        "code": str(getattr(error, "code", type(error).__name__)),
                        "message": str(error),
                        **dict(getattr(error, "context", {})),
                    },
                )
            raise

    def get_active(self, run_id: str) -> AtomicContentHarnessValidationReport:
        run = self._repository.load_run(run_id)
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.atomic_content_harness_validation_ref
            or run.atomic_content_harness_validation_invalidation_ref is not None
            or self._repository.is_atomic_content_harness_validation_invalidated(
                run.atomic_content_harness_validation_ref
            )
        ):
            raise TargetValidationInvalidatedError(
                "No active Atomic Content Harness validation is available."
            )
        report = self._repository.get_atomic_content_harness_validation_report(
            run.atomic_content_harness_validation_ref
        )
        definition = self._load_active_definition(run, allow_existing_validation=True)
        if report is None or report.report_hash != run.atomic_content_harness_validation_hash:
            raise TargetValidationInvalidatedError(
                "The active target-validation report is missing or altered."
            )
        report.validate(definition)
        return report

    def get_historical(
        self, report_id: str
    ) -> AtomicContentHarnessValidationReport:
        report = self._repository.get_atomic_content_harness_validation_report(report_id)
        if report is None:
            raise KeyError(report_id)
        definition = self._repository.get_atomic_harness_definition(report.definition_id)
        if definition is None:
            raise TargetValidationLineageInvalid(
                "Historical validation definition is unavailable."
            )
        report.validate(definition)
        return report

    def _load_active_definition(
        self, run: Run, *, allow_existing_validation: bool = False
    ) -> AtomicHarnessDefinition:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.atomic_harness_definition_ref
            or not run.atomic_harness_definition_hash
            or run.atomic_harness_definition_invalidation_ref is not None
            or (
                run.atomic_content_harness_validation_ref is not None
                and not allow_existing_validation
            )
            or run.atomic_content_harness_validation_invalidation_ref is not None
            or self._repository.is_atomic_harness_definition_invalidated(
                run.atomic_harness_definition_ref
            )
        ):
            raise TargetValidationInvalidatedError(
                "Validation requires one exact active Atomic Harness Definition."
            )
        definition = self._repository.get_atomic_harness_definition(
            run.atomic_harness_definition_ref
        )
        if definition is None:
            raise TargetValidationLineageInvalid(
                "The active Atomic Harness Definition is unavailable."
            )
        digest = sha256(definition.canonical_bytes()).hexdigest()
        run_refs = (
            (run.source_lock_ref, definition.source_lock_ref),
            (run.atomic_boundary_ref, definition.boundary_ref),
            (run.atomicity_ratification_ref, definition.ratification_ref),
            (run.draft_harness_model_ref, definition.model_ref),
            (run.harness_ir_ref, definition.ir_id),
            (run.artifact_set_ref, definition.artifact_set_id),
            (run.artifact_manifest_ref, definition.artifact_manifest_id),
            (run.constitutional_validation_ref, definition.constitutional_report_id),
            (run.capability_ownership_ref, definition.capability_graph_id),
            (run.responsibility_module_ref, definition.module_graph_id),
            (run.phase_graph_ref, definition.phase_graph_id),
            (run.phase_handoff_ref, definition.handoff_graph_id),
            (run.minimum_context_ref, definition.minimum_context_graph_id),
            (run.skill_registry_snapshot_ref, definition.skill_snapshot_id),
            (run.skill_necessity_ref, definition.skill_necessity_decision_id),
        )
        invalidated = (
            self._repository.is_boundary_invalidated(definition.boundary_ref)
            or self._repository.is_model_invalidated(definition.model_ref)
            or self._repository.is_harness_ir_invalidated(definition.ir_id)
            or self._repository.is_artifact_set_invalidated(definition.artifact_set_id)
            or self._repository.is_constitutional_validation_invalidated(
                definition.constitutional_report_id
            )
            or self._repository.is_capability_ownership_invalidated(
                definition.capability_graph_id
            )
            or self._repository.is_responsibility_module_invalidated(
                definition.module_graph_id
            )
            or self._repository.is_phase_graph_invalidated(definition.phase_graph_id)
            or self._repository.is_phase_handoff_invalidated(
                definition.handoff_graph_id
            )
            or self._repository.is_minimum_context_invalidated(
                definition.minimum_context_graph_id
            )
            or self._repository.is_skill_registry_snapshot_invalidated(
                definition.skill_snapshot_id
            )
            or self._repository.is_skill_necessity_invalidated(
                definition.skill_necessity_decision_id
            )
        )
        if (
            definition.definition_id != f"atomic-harness-definition_{digest}"
            or definition.definition_hash != f"sha256:{digest}"
            or definition.definition_hash != run.atomic_harness_definition_hash
            or any(left != right for left, right in run_refs)
            or invalidated
        ):
            raise TargetValidationLineageInvalid(
                "The active definition or its complete governed lineage is altered."
            )
        self._validate_definition_authority(run, definition)
        return definition

    def _validate_definition_authority(
        self, run: Run, definition: AtomicHarnessDefinition
    ) -> None:
        self._verify_definition_input_pin()
        attachments = tuple(
            event
            for event in self._repository.events(run.run_id)
            if event.event_type == "AtomicHarnessDefinitionAttached"
            and event.value("definition_ref") == definition.definition_id
        )
        receipts = tuple(
            receipt
            for receipt in self._repository.atomic_harness_definition_receipts(
                run.run_id
            )
            if receipt.definition_id == definition.definition_id
        )
        if len(attachments) != 1 or len(receipts) != 1:
            raise TargetValidationLineageInvalid(
                "Definition compiler attachment and receipt evidence must be unique."
            )
        attachment = attachments[0]
        definition_receipt = receipts[0]
        if (
            attachment.value("definition_hash") != definition.definition_hash
            or attachment.actor_id != definition.authority_identity
            or attachment.command_id != definition_receipt.command_id
            or definition_receipt.event_ids != (attachment.event_id,)
            or definition_receipt.stream_version != attachment.stream_version
            or definition_receipt.definition_hash != definition.definition_hash
            or definition_receipt.authority_identity != attachment.actor_id
        ):
            raise TargetValidationLineageInvalid(
                "Definition, attachment, receipt and compiler authority do not agree."
            )
        try:
            definition_receipt.validate(definition)
        except Exception as error:
            raise TargetValidationLineageInvalid(
                "Definition receipt cannot reproduce compiler authority."
            ) from error
        try:
            compiler = self._authority.authorize(
                actor_id=attachment.actor_id,
                action=Action.TRANSITION_RUN,
                resource_id=run.run_id,
                now=self._clock.now(),
            )
        except Exception as error:
            raise TargetValidationAuthorityInvalid(
                "Definition compiler authority is unknown, stale, or unauthorized."
            ) from error
        if compiler.kind is not ActorKind.CODE:
            raise TargetValidationAuthorityInvalid(
                "Definition compiler authority must be deterministic Builder code."
            )
        context = self._repository.get_minimum_context_graph(
            run.minimum_context_ref or ""
        )
        values = {
            "run": run,
            "source_lock": self._repository.get_source_lock(
                run.source_lock_ref or ""
            ),
            "boundary": self._repository.get_atomic_boundary(
                run.atomic_boundary_ref or ""
            ),
            "ratification": self._repository.get_atomicity_ratification(
                run.atomicity_ratification_ref or ""
            ),
            "model": self._repository.get_draft_harness_model(
                run.draft_harness_model_ref or ""
            ),
            "ir": self._repository.get_harness_ir(run.harness_ir_ref or ""),
            "manifest": self._repository.get_artifact_manifest(
                run.artifact_manifest_ref or ""
            ),
            "constitutional": self._repository.get_constitutional_validation_report(
                run.constitutional_validation_ref or ""
            ),
            "capability": self._repository.get_capability_ownership_graph(
                run.capability_ownership_ref or ""
            ),
            "modules": self._repository.get_responsibility_module_graph(
                run.responsibility_module_ref or ""
            ),
            "phases": self._repository.get_phase_graph(run.phase_graph_ref or ""),
            "handoff_graph": self._repository.get_phase_handoff_graph(
                run.phase_handoff_ref or ""
            ),
            "accepted_handoff": (
                self._repository.get_internal_handoff(context.accepted_handoff_id)
                if context is not None
                else None
            ),
            "handoff_decision": (
                self._repository.get_internal_handoff_decision(
                    context.accepted_handoff_id
                )
                if context is not None
                else None
            ),
            "context": context,
            "snapshot": self._repository.get_skill_registry_snapshot(
                run.skill_registry_snapshot_ref or ""
            ),
            "necessity": self._repository.get_skill_necessity_decision(
                run.skill_necessity_ref or ""
            ),
        }
        if any(value is None for value in values.values()):
            raise TargetValidationLineageInvalid(
                "Definition authority cannot be reconstructed from active upstream evidence."
            )
        try:
            definition.validate(
                **values,
                expected_authority_identity=attachment.actor_id,
            )
        except Exception as error:
            raise TargetValidationLineageInvalid(
                "Definition meaning differs from governed upstream authority."
            ) from error

    def _verify_definition_input_pin(self) -> None:
        path = (self._root / DEFINITION_INPUT_PATH).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise TargetValidationInputInvalid(
                "Definition authority input is missing or outside the repository."
            ) from error
        if observed != DEFINITION_INPUT_SHA256:
            raise TargetValidationInputInvalid(
                "Definition authority input hash differs from the governed pin."
            )

    def _load_policy(self, command: ValidateAtomicContentHarnessCommand) -> None:
        if (
            command.policy_path != VALIDATION_POLICY_PATH
            or command.policy_sha256 != VALIDATION_POLICY_SHA256
        ):
            raise TargetValidationInputInvalid(
                "Target-validation policy pin differs from capsule authority."
            )
        path = (self._root / command.policy_path).resolve()
        try:
            path.relative_to(self._root)
            raw = path.read_bytes()
            observed = sha256(raw).hexdigest()
            value = json.loads(raw.decode("utf-8"))
        except (ValueError, OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise TargetValidationInputInvalid(
                "Target-validation policy is missing, unreadable, or outside the repository."
            ) from error
        target = value.get("target", {})
        compatibility = value.get("compatibility_scope", {})
        if (
            observed != VALIDATION_POLICY_SHA256
            or value.get("scope") != VALIDATION_SCOPE
            or tuple(value.get("required_validation_dimensions", ()))
            != REQUIRED_VALIDATION_DIMENSIONS
            or tuple(value.get("required_definition_sections", ()))
            != REQUIRED_SECTIONS
            or target.get("target_kind") != TARGET_KIND
            or target.get("profile_id") != PROFILE_ID
            or target.get("category_binding") != "none"
            or target.get("production_eligible")
            or target.get("certified")
            or not target.get("synthetic_not_certifiable")
            or compatibility.get("atomic_content_harness_internal")
            != "PASS_REQUIRED"
            or compatibility.get("visual_asset_editor")
            != EXTERNAL_TARGET_COMPATIBILITY
            or compatibility.get("delegation_contract")
            != EXTERNAL_TARGET_COMPATIBILITY
            or compatibility.get("external_target_packages_compiled")
            or compatibility.get("BD_014_applies")
            or value.get("expected_outcome") != VALIDATION_OUTCOME
        ):
            raise TargetValidationInputInvalid(
                "Target-validation policy content is incomplete or broadened."
            )

    def _validate_command(self, command: ValidateAtomicContentHarnessCommand) -> None:
        if (
            not all(value.strip() for value in (
                command.command_id,
                command.run_id,
                command.actor_id,
                command.correlation_id,
                command.causation_id,
            ))
            or command.expected_version < 1
            or command.requested_operation != "validate_atomic_content_harness"
            or command.requested_target_kind != TARGET_KIND
            or command.requested_profile_id != PROFILE_ID
            or command.requested_dimensions != REQUIRED_VALIDATION_DIMENSIONS
            or command.requested_internal_compatibility != INTERNAL_COMPATIBILITY
        ):
            raise TargetValidationInputInvalid(
                "Target-validation command identity or contract is invalid."
            )
        if command.requested_external_target_compatibility != EXTERNAL_TARGET_COMPATIBILITY:
            raise TargetValidationScopeInvalid(
                "External-target compatibility cannot be promoted in this mode."
            )
        if command.requested_production_eligible or command.requested_certified:
            raise TargetValidationAuthorityInvalid(
                "The synthetic Harness cannot claim production or certification."
            )
        if not command.requested_synthetic_not_certifiable:
            raise TargetValidationAuthorityInvalid(
                "The synthetic_not_certifiable marker cannot be removed."
            )
        if command.field_overrides or command.lineage_overrides:
            raise TargetValidationLineageInvalid(
                "Command-supplied field or lineage overrides are not authoritative."
            )

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise TargetValidationAuthorityInvalid(
                "Only deterministic Builder code may issue target validation."
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
    ) -> AtomicContentHarnessValidationReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if (
            record.payload_hash != payload_hash
            or not isinstance(record.result, AtomicContentHarnessValidationReceipt)
        ):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: ValidateAtomicContentHarnessCommand,
        receipt: AtomicContentHarnessValidationReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        report = self._repository.get_atomic_content_harness_validation_report(
            receipt.report_id
        )
        definition = self._repository.get_atomic_harness_definition(
            receipt.definition_id
        )
        if report is None or definition is None:
            raise TargetValidationLineageInvalid(
                "Replayed validation evidence is unavailable."
            )
        self._emit_best_effort(
            event_name="atomic_content_harness_validation_replayed",
            outcome="PASS",
            command=command,
            run=run,
            definition=definition,
            report=report,
            receipt=receipt,
            replay_status="ORIGINAL_RECEIPT_RETURNED",
            failure_context={},
        )

    def _observation(
        self,
        *,
        event_name: str,
        outcome: str,
        command: ValidateAtomicContentHarnessCommand,
        run: Run | None,
        definition: AtomicHarnessDefinition | None,
        report: AtomicContentHarnessValidationReport | None,
        receipt: AtomicContentHarnessValidationReceipt | None,
        replay_status: str,
        failure_context: dict[str, object],
    ) -> Observation:
        return Observation(
            event_name=event_name,
            run_id=command.run_id,
            story_id=self.STORY_ID,
            artifact_identity=(report.report_id if report else "unassigned"),
            authority_identity=command.actor_id,
            version=self.CONTRACT_VERSION,
            provenance=(report.report_hash if report else "unassigned"),
            outcome=outcome,
            failure_context=failure_context,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=(run.target_profile.target_id if run else command.requested_target_kind),
            category_id=(run.target_profile.category_id if run else "none"),
            profile_id=(run.target_profile.profile_id if run else command.requested_profile_id),
            stream_version=(run.stream_version if run else command.expected_version),
            atomic_harness_definition_id=(definition.definition_id if definition else "unassigned"),
            atomic_harness_definition_hash=(definition.definition_hash if definition else "unassigned"),
            atomic_harness_definition_section_count=(len(definition.sections) if definition else 0),
            atomic_harness_definition_external_skill_count=(definition.external_skill_count if definition else 0),
            atomic_harness_definition_external_runtime_count=(definition.external_runtime_count if definition else 0),
            atomic_harness_definition_certification=("synthetic_not_certifiable" if definition else "unassigned"),
            atomic_content_harness_validation_id=(report.report_id if report else "unassigned"),
            atomic_content_harness_validation_hash=(report.report_hash if report else "unassigned"),
            atomic_content_harness_validation_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
            atomic_content_harness_validation_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
            atomic_content_harness_validation_dimension_count=(len(report.dimensions) if report else 0),
            atomic_content_harness_internal_compatibility=(report.internal_compatibility if report else "unassigned"),
            atomic_content_harness_external_compatibility=(report.external_target_compatibility if report else "unassigned"),
            atomic_content_harness_certification=("synthetic_not_certifiable" if report else "unassigned"),
            atomic_content_harness_replay_status=replay_status,
        )

    def _emit_best_effort(self, **values: object) -> None:
        try:
            self._observations.emit(self._observation(**values))
        except Exception:
            # Telemetry is delivery evidence, never a second command outcome.
            return

    def _deliver_pending(self, command_id: str) -> None:
        while True:
            observation = self._repository.claim_pending_observation(command_id)
            if observation is None:
                return
            try:
                self._observations.emit(observation)
            except Exception:
                self._repository.release_observation_delivery(
                    command_id, observation
                )
                return
            self._repository.complete_observation_delivery(
                command_id, observation
            )


def _command_hash(command: ValidateAtomicContentHarnessCommand) -> str:
    value = json.dumps(
        asdict(command),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return f"sha256:{sha256(value).hexdigest()}"
