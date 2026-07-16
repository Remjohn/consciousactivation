from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from hashlib import sha256
import json
from typing import Callable

from cmf_builder.application.authority import Action, AuthorityService
from cmf_builder.application.checkpoints import Checkpoint, CheckpointManager
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    IdempotencyPayloadMismatch,
    IdProvider,
    Observation,
    ObservationSink,
    RunRepository,
    TargetProfileRepository,
)
from cmf_builder.domain.run import LifecycleState, LifecycleWaiver, Run


@dataclass(frozen=True, slots=True)
class CreateRunCommand:
    command_id: str
    target_ids: tuple[str, ...]
    category_id: str
    profile_id: str
    compiler_version: str
    actor_id: str
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class TransitionRunCommand:
    command_id: str
    run_id: str
    to_state: LifecycleState
    prerequisites: frozenset[str]
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class GrantWaiverCommand:
    command_id: str
    run_id: str
    skipped_obligation: str
    rationale: str
    risk: str
    affected_gates: tuple[str, ...]
    scope: str
    expires_at: datetime
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class CreateCheckpointCommand:
    command_id: str
    run_id: str
    input_hash: str
    policy_hash: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class ResumeRunCommand:
    command_id: str
    run_id: str
    input_hash: str
    policy_hash: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class CommandReceipt:
    receipt_id: str
    command_id: str
    run_id: str
    event_ids: tuple[str, ...]
    outcome: str
    authority_identity: str
    artifact_identity: str
    provenance: str
    details: tuple[tuple[str, str], ...] = ()

    def detail(self, key: str) -> str:
        for candidate, value in self.details:
            if candidate == key:
                return value
        raise KeyError(key)


class RunCommandService:
    STORY_ID = "ST-01.01"
    CONTRACT_VERSION = "cmf-builder-run-lifecycle/v1"

    def __init__(
        self,
        *,
        repository: RunRepository,
        profiles: TargetProfileRepository,
        authority: AuthorityService,
        ids: IdProvider,
        clock: Clock,
        observations: ObservationSink,
    ) -> None:
        self._repository = repository
        self._profiles = profiles
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations
        self._checkpoints = CheckpointManager()

    def create_run(self, command: CreateRunCommand) -> CommandReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.CREATE_RUN,
                resource_id="run:create",
                now=now,
            )
            profile = self._profiles.resolve(
                command.target_ids, command.category_id, command.profile_id
            )
            run_id = self._ids.new_id("run")
            run, events = Run.create(
                run_id=run_id,
                profile=profile,
                compiler_version=command.compiler_version,
                actor_id=command.actor_id,
                command_id=command.command_id,
                event_ids=(self._ids.new_id("event"), self._ids.new_id("event")),
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = self._receipt(command, run, events)
            self._commit(
                command,
                run_id=run_id,
                expected_version=0,
                events=events,
                receipt=receipt,
            )
            self._emit(command, run, "ST-01.01:OutcomeVerified", "PASS", {})
            return receipt
        except Exception as error:
            self._reject(command, run, error)
            raise

    def transition_run(self, command: TransitionRunCommand) -> CommandReceipt:
        return self._run_mutation(
            command,
            action=Action.TRANSITION_RUN,
            mutate=lambda run, now: run.transition(
                to_state=command.to_state,
                prerequisites=command.prerequisites,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            ),
            success_event="LifecycleTransitioned",
        )

    def grant_waiver(self, command: GrantWaiverCommand) -> CommandReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.GRANT_WAIVER,
                resource_id=command.run_id,
                now=now,
            )
            human_receipt_id = self._ids.new_id("human-receipt")
            waiver = LifecycleWaiver(
                skipped_obligation=command.skipped_obligation,
                rationale=command.rationale,
                risk=command.risk,
                affected_gates=command.affected_gates,
                scope=command.scope,
                expires_at=command.expires_at,
                signed_by=command.actor_id,
                human_receipt_id=human_receipt_id,
            )
            updated, event = run.grant_waiver(
                waiver,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = self._receipt(
                command,
                updated,
                (event,),
                details={"human_receipt_id": human_receipt_id},
            )
            self._commit(
                command,
                run_id=command.run_id,
                expected_version=command.expected_version,
                events=(event,),
                receipt=receipt,
            )
            self._emit(command, updated, "LifecycleWaiverGranted", "PASS", {})
            return receipt
        except Exception as error:
            self._reject(command, run, error)
            raise

    def create_checkpoint(self, command: CreateCheckpointCommand) -> CommandReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.CREATE_CHECKPOINT,
                resource_id=command.run_id,
                now=now,
            )
            checkpoint_id = self._ids.new_id("checkpoint")
            updated, event = run.record_checkpoint(
                checkpoint_id=checkpoint_id,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            checkpoint = Checkpoint.from_run(
                updated,
                checkpoint_id=checkpoint_id,
                input_hash=command.input_hash,
                policy_hash=command.policy_hash,
                created_at=now,
            )
            receipt = self._receipt(
                command,
                updated,
                (event,),
                details={"checkpoint_id": checkpoint_id},
            )
            self._commit(
                command,
                run_id=command.run_id,
                expected_version=command.expected_version,
                events=(event,),
                receipt=receipt,
                checkpoint=checkpoint,
            )
            self._emit(command, updated, "CheckpointCreated", "PASS", {})
            return receipt
        except Exception as error:
            self._reject(command, run, error)
            raise

    def resume_run(self, command: ResumeRunCommand) -> CommandReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.RESUME_RUN,
                resource_id=command.run_id,
                now=now,
            )
            checkpoint, invalid_ids = self._checkpoints.select_latest_valid(
                run,
                self._repository.list_checkpoints(command.run_id),
                input_hash=command.input_hash,
                policy_hash=command.policy_hash,
            )
            for checkpoint_id in invalid_ids:
                self._emit(
                    command,
                    run,
                    "CheckpointInvalid",
                    "FAIL",
                    {"code": "CheckpointInvalid", "checkpoint_id": checkpoint_id},
                )
            checkpoint_id = checkpoint.checkpoint_id if checkpoint else None
            updated, event = run.resume(
                checkpoint_id=checkpoint_id,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=now,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = self._receipt(
                command,
                updated,
                (event,),
                details={
                    "checkpoint_id": checkpoint_id or "event-stream-replay",
                    "replayed_human_decision_count": "0",
                    "referenced_human_decision_count": str(
                        len(updated.human_decision_receipt_ids)
                    ),
                },
            )
            self._commit(
                command,
                run_id=command.run_id,
                expected_version=command.expected_version,
                events=(event,),
                receipt=receipt,
            )
            self._emit(command, updated, "RunResumed", "PASS", {})
            self._emit(command, updated, "ST-01.01:OutcomeVerified", "PASS", {})
            return receipt
        except Exception as error:
            self._reject(command, run, error)
            raise

    def _run_mutation(
        self,
        command: TransitionRunCommand,
        *,
        action: Action,
        mutate: Callable[[Run, datetime], tuple[Run, object]],
        success_event: str,
    ) -> CommandReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command)
            if duplicate is not None:
                return duplicate
            now = self._clock.now()
            run = self._repository.load_run(command.run_id)
            self._authority.authorize(
                actor_id=command.actor_id,
                action=action,
                resource_id=command.run_id,
                now=now,
            )
            updated, event = mutate(run, now)
            receipt = self._receipt(command, updated, (event,))
            self._commit(
                command,
                run_id=command.run_id,
                expected_version=command.expected_version,
                events=(event,),
                receipt=receipt,
            )
            self._emit(command, updated, success_event, "PASS", {})
            return receipt
        except Exception as error:
            self._reject(command, run, error)
            raise

    def _duplicate(self, command: object) -> CommandReceipt | None:
        command_id = str(getattr(command, "command_id"))
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        payload_hash = _command_hash(command)
        if payload_hash != record.payload_hash:
            raise IdempotencyPayloadMismatch(
                "A command identity was reused with a different payload.",
                command_id=command_id,
                original_payload_hash=record.payload_hash,
                observed_payload_hash=payload_hash,
            )
        receipt = record.result
        if not isinstance(receipt, CommandReceipt):
            raise IdempotencyPayloadMismatch(
                "Stored command result has an incompatible type.", command_id=command_id
            )
        run: Run | None = None
        try:
            run = self._repository.load_run(receipt.run_id)
        except KeyError:
            pass
        self._emit(command, run, "DuplicateCommandObserved", "PASS", {})
        return receipt

    def _commit(
        self,
        command: object,
        *,
        run_id: str,
        expected_version: int,
        events: tuple[object, ...],
        receipt: CommandReceipt,
        checkpoint: Checkpoint | None = None,
    ) -> None:
        self._repository.commit_run_command(
            run_id=run_id,
            expected_version=expected_version,
            events=events,
            command_id=str(getattr(command, "command_id")),
            command_record=CommandRecord(
                payload_hash=_command_hash(command), result=receipt
            ),
            checkpoint=checkpoint,
        )

    def _receipt(
        self,
        command: object,
        run: Run,
        events: tuple[object, ...],
        *,
        details: dict[str, str] | None = None,
    ) -> CommandReceipt:
        return CommandReceipt(
            receipt_id=self._ids.new_id("receipt"),
            command_id=str(getattr(command, "command_id")),
            run_id=run.run_id,
            event_ids=tuple(str(getattr(event, "event_id")) for event in events),
            outcome="PASS",
            authority_identity=str(getattr(command, "actor_id")),
            artifact_identity=run.state_hash(),
            provenance=self.STORY_ID,
            details=tuple(sorted((details or {}).items())),
        )

    def _reject(self, command: object, run: Run | None, error: Exception) -> None:
        if not hasattr(error, "code"):
            return
        context = {"code": str(getattr(error, "code")), **getattr(error, "context", {})}
        self._emit(command, run, "ST-01.01:OutcomeRejected", "FAIL", context)

    def _emit(
        self,
        command: object,
        run: Run | None,
        event_name: str,
        outcome: str,
        failure_context: dict[str, object],
    ) -> None:
        target_ids = tuple(getattr(command, "target_ids", ()))
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=run.run_id if run else str(getattr(command, "run_id", "unassigned")),
                story_id=self.STORY_ID,
                artifact_identity=run.state_hash() if run else "RunLifecycle",
                authority_identity=str(getattr(command, "actor_id", "unassigned")),
                version=self.CONTRACT_VERSION,
                provenance=self.STORY_ID,
                outcome=outcome,
                failure_context=dict(failure_context),
                correlation_id=str(getattr(command, "correlation_id", "unassigned")),
                causation_id=str(getattr(command, "causation_id", "unassigned")),
                command_id=str(getattr(command, "command_id", "unassigned")),
                target_id=(
                    run.target_profile.target_id
                    if run
                    else (target_ids[0] if len(target_ids) == 1 else "unassigned")
                ),
                category_id=(
                    run.target_profile.category_id
                    if run
                    else str(getattr(command, "category_id", "unassigned"))
                ),
                profile_id=(
                    run.target_profile.profile_id
                    if run
                    else str(getattr(command, "profile_id", "unassigned"))
                ),
                stream_version=run.stream_version if run else 0,
            )
        )


def _command_hash(command: object) -> str:
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
    if isinstance(value, datetime):
        return value.isoformat()
    return value
