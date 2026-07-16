from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.harness_ir_migrations import HarnessIRVersionRegistry
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    HarnessIRRepository,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomicity import (
    AtomicityRatification,
    DeclaredAtomicBoundary,
    DraftHarnessModel,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.harness_ir import (
    ACTIVATIVE_LINEAGE_PATHS,
    HARNESS_IR_SCHEMA_ID,
    HARNESS_IR_SCHEMA_VERSION,
    HarnessIR,
    HarnessIRAuthorityRejected,
    HarnessIRCompilationReceipt,
    HarnessIRInvalidatedError,
    HarnessIRSchemaUnsupported,
)
from cmf_builder.domain.run import LifecycleState, Run


class HarnessIRCommandRejected(Exception):
    code = "HarnessIRCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class HarnessIRUpstreamInvalid(HarnessIRCommandRejected):
    code = "HarnessIRUpstreamInvalid"


@dataclass(frozen=True, slots=True)
class CompileHarnessIRCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    schema_version: str = HARNESS_IR_SCHEMA_VERSION


class HarnessIRCommandService:
    STORY_ID = "ST-03.03"
    CONTRACT_VERSION = HARNESS_IR_SCHEMA_ID

    def __init__(
        self,
        *,
        repository: HarnessIRRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations
        self._versions = HarnessIRVersionRegistry.initial()

    def compile(self, command: CompileHarnessIRCommand) -> HarnessIRCompilationReceipt:
        run: Run | None = None
        snapshot: HarnessIR | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            if not all(
                value.strip()
                for value in (
                    command.command_id,
                    command.run_id,
                    command.actor_id,
                    command.correlation_id,
                    command.causation_id,
                )
            ):
                raise HarnessIRCommandRejected("Compile command identity is incomplete.")
            run = self._repository.load_run(command.run_id)
            if command.expected_version != run.stream_version:
                raise ConcurrencyConflict(
                    "Expected stream version does not match authoritative state.",
                    expected_version=command.expected_version,
                    current_version=run.stream_version,
                )
            actor = self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.TRANSITION_RUN,
                resource_id=command.run_id,
                now=self._clock.now(),
            )
            if actor.kind is not ActorKind.CODE:
                raise HarnessIRAuthorityRejected(
                    "Only deterministic Builder code may compile canonical Harness IR.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            if command.schema_version != HARNESS_IR_SCHEMA_VERSION:
                raise HarnessIRSchemaUnsupported(
                    "Requested Harness IR schema version is unsupported.",
                    schema_version=command.schema_version,
                )
            self._versions.require_readable(command.schema_version)
            source_lock, boundary, ratification, model = self._load_upstream(run)
            snapshot = HarnessIR.compile(
                run=run,
                source_lock=source_lock,
                boundary=boundary,
                ratification=ratification,
                model=model,
                compiled_by=command.actor_id,
                schema_version=command.schema_version,
            )
            final_run, events = run.attach_harness_ir(
                harness_ir_ref=snapshot.ir_id,
                harness_ir_hash=snapshot.ir_hash,
                schema_version=snapshot.schema_version,
                revision=snapshot.revision,
                event_ids=(self._ids.new_id("event"), self._ids.new_id("event")),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = HarnessIRCompilationReceipt.create(
                receipt_id=self._ids.new_id("receipt"),
                command_id=command.command_id,
                run_id=run.run_id,
                ir=snapshot,
                authority_identity=command.actor_id,
                event_ids=tuple(event.event_id for event in events),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_harness_ir(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=events,
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                snapshot=snapshot,
                receipt=receipt,
            )
            for event_name in (
                "ST-03.03:HarnessIRCompiled",
                "ST-03.03:HarnessIRSnapshotCommitted",
                "ST-03.03:CompatibilityValidated",
                "ST-03.03:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    snapshot=snapshot,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._reject(command, run=run, snapshot=snapshot, error=error)
            raise

    def get_active(self, run_id: str) -> HarnessIR:
        run = self._repository.load_run(run_id)
        if (
            not run.harness_ir_ref
            or run.harness_ir_invalidation_ref is not None
            or self._repository.is_harness_ir_invalidated(run.harness_ir_ref)
        ):
            raise HarnessIRInvalidatedError(
                "No active canonical Harness IR is available.",
                run_id=run_id,
                harness_ir_ref=run.harness_ir_ref,
            )
        snapshot = self._repository.get_harness_ir(run.harness_ir_ref)
        if snapshot is None:
            raise HarnessIRUpstreamInvalid(
                "Run references an unavailable Harness IR snapshot.", run_id=run_id
            )
        snapshot.validate()
        return snapshot

    def _load_upstream(
        self, run: Run
    ) -> tuple[SourceLock, DeclaredAtomicBoundary, AtomicityRatification, DraftHarnessModel]:
        if (
            run.lifecycle_state is not LifecycleState.ATOMICITY_RATIFICATION
            or not run.source_lock_ref
            or not run.atomic_boundary_ref
            or not run.atomicity_ratification_ref
            or not run.draft_harness_model_ref
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_ref is not None
        ):
            raise HarnessIRUpstreamInvalid(
                "Run does not expose one active pre-ratified synthetic package.",
                lifecycle_state=run.lifecycle_state.value,
            )
        if (
            self._repository.is_boundary_invalidated(run.atomic_boundary_ref)
            or self._repository.is_model_invalidated(run.draft_harness_model_ref)
        ):
            raise HarnessIRUpstreamInvalid("Upstream boundary or model is invalidated.")
        source_lock = self._repository.get_source_lock(run.source_lock_ref)
        boundary = self._repository.get_atomic_boundary(run.atomic_boundary_ref)
        ratification = self._repository.get_atomicity_ratification(
            run.atomicity_ratification_ref
        )
        model = self._repository.get_draft_harness_model(run.draft_harness_model_ref)
        if any(value is None for value in (source_lock, boundary, ratification, model)):
            raise HarnessIRUpstreamInvalid(
                "A required immutable upstream artifact is unavailable.",
                source_lock_ref=run.source_lock_ref,
                boundary_ref=run.atomic_boundary_ref,
                ratification_ref=run.atomicity_ratification_ref,
                model_ref=run.draft_harness_model_ref,
            )
        return source_lock, boundary, ratification, model

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> HarnessIRCompilationReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, HarnessIRCompilationReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileHarnessIRCommand,
        receipt: HarnessIRCompilationReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        snapshot = self._repository.get_harness_ir(receipt.ir_id)
        if snapshot is None:
            raise HarnessIRUpstreamInvalid("Replay snapshot is unavailable.")
        self._emit(
            event_name="ST-03.03:CompilationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            snapshot=snapshot,
            receipt=receipt,
            failure_context={},
        )

    def _reject(
        self,
        command: CompileHarnessIRCommand,
        *,
        run: Run | None,
        snapshot: HarnessIR | None,
        error: Exception,
    ) -> None:
        context = dict(getattr(error, "context", {}))
        context.update({"code": getattr(error, "code", type(error).__name__), "message": str(error)})
        self._emit(
            event_name="ST-03.03:OutcomeRejected",
            outcome="FAIL",
            command=command,
            run=run,
            snapshot=snapshot,
            receipt=None,
            failure_context=context,
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileHarnessIRCommand,
        run: Run | None,
        snapshot: HarnessIR | None,
        receipt: HarnessIRCompilationReceipt | None,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run is not None else None
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(snapshot.ir_id if snapshot else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(";".join(snapshot.upstream_refs) if snapshot else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(profile.target_id if profile else "unassigned"),
                category_id=(profile.category_id if profile else "unassigned"),
                profile_id=(profile.profile_id if profile else "unassigned"),
                stream_version=(run.stream_version if run else command.expected_version),
                source_lock_id=(snapshot.source_lock_ref if snapshot else (run.source_lock_ref if run else "unassigned")) or "unassigned",
                boundary_id=(snapshot.boundary_ref if snapshot else (run.atomic_boundary_ref if run else "unassigned")) or "unassigned",
                model_id=(snapshot.model_ref if snapshot else (run.draft_harness_model_ref if run else "unassigned")) or "unassigned",
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                harness_ir_id=(snapshot.ir_id if snapshot else "unassigned"),
                harness_ir_hash=(snapshot.ir_hash if snapshot else "unassigned"),
                harness_ir_schema_id=(snapshot.schema_id if snapshot else HARNESS_IR_SCHEMA_ID),
                harness_ir_schema_version=(snapshot.schema_version if snapshot else command.schema_version),
                harness_ir_revision=(snapshot.revision if snapshot else 0),
                harness_ir_status=(snapshot.status.value if snapshot else "unassigned"),
                harness_ir_compatibility=(
                    "READ_WRITE_1.0.0_NO_PRIOR_MIGRATIONS"
                    if snapshot
                    else "unassigned"
                ),
                activative_lineage_disposition=(
                    "EXPLICIT_NOT_APPLICABLE_SEPARATE_KEYS"
                    if snapshot and all(snapshot.value(path).value is None for path in ACTIVATIVE_LINEAGE_PATHS)
                    else "unassigned"
                ),
                dependency_impact_refs=(
                    tuple(item.path for item in snapshot.material_values)
                    if snapshot
                    else ()
                ),
            )
        )


def _command_hash(command: object) -> str:
    return f"sha256:{sha256(_canonical_json(_canonical_value(asdict(command)))).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
