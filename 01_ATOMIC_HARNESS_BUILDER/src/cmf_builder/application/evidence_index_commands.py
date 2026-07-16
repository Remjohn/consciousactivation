from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    EvidenceIndexRepository,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.evidence_index import (
    ADAPTER_VERSION,
    INDEX_VERSION,
    EvidenceIndex,
    EvidenceIndexInvalidated,
    EvidenceIndexInvalidation,
    EvidenceIndexReceipt,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.run import LifecycleState, Run


class EvidenceIndexCommandRejected(Exception):
    code = "EvidenceIndexCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class IndexEvidenceCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    adapter_version: str = ADAPTER_VERSION
    index_version: str = INDEX_VERSION


@dataclass(frozen=True, slots=True)
class InvalidateEvidenceIndexCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    index_id: str
    reason: str


class EvidenceIndexCommandService:
    STORY_ID = "ST-01.03"
    CONTRACT_VERSION = INDEX_VERSION

    def __init__(
        self,
        *,
        repository: EvidenceIndexRepository,
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

    def index(self, command: IndexEvidenceCommand) -> EvidenceIndexReceipt:
        run: Run | None = None
        source_lock: SourceLock | None = None
        index: EvidenceIndex | None = None
        committed = False
        try:
            duplicate = self._duplicate_index(command)
            if duplicate is not None:
                self._deliver_pending(command.command_id)
                self._emit_replay(command, duplicate)
                return duplicate
            run = self._repository.load_run(command.run_id)
            self._validate_index_command(run, command)
            actor = self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.INDEX_EVIDENCE,
                resource_id=command.run_id,
                now=self._clock.now(),
            )
            if actor.kind is not ActorKind.CODE:
                raise EvidenceIndexCommandRejected(
                    "Evidence indexing may be committed only by deterministic Builder code.",
                    actor_id=command.actor_id,
                    actor_kind=actor.kind.value,
                )
            source_lock = self._repository.get_source_lock(run.source_lock_ref or "")
            self._validate_active_source_lock(run, source_lock)
            assert source_lock is not None
            index = EvidenceIndex.create(
                run_id=run.run_id,
                source_lock=source_lock,
                authority_identity=command.actor_id,
                adapter_version=command.adapter_version,
            )
            final_run, event = run.attach_evidence_index(
                index_ref=index.index_id,
                index_hash=index.index_hash,
                source_lock_ref=index.source_lock_ref,
                source_lock_hash=index.source_lock_hash,
                specimen_count=index.specimen_count,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = EvidenceIndexReceipt.create(
                command_id=command.command_id,
                index=index,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            observations = self._success_observations(
                command=command,
                run=final_run,
                source_lock=source_lock,
                index=index,
                receipt=receipt,
            )
            self._repository.commit_evidence_index(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(
                    payload_hash=_command_hash(command), result=receipt
                ),
                index=index,
                receipt=receipt,
                observations=observations,
            )
            committed = True
            self._deliver_pending(command.command_id)
            return receipt
        except Exception as error:
            if not committed:
                self._emit_rejection(command, run, source_lock, index, error)
            raise

    def invalidate(
        self, command: InvalidateEvidenceIndexCommand
    ) -> EvidenceIndexInvalidation:
        duplicate = self._duplicate_invalidation(command)
        if duplicate is not None:
            self._deliver_pending(command.command_id)
            return duplicate
        run = self._repository.load_run(command.run_id)
        if command.expected_version != run.stream_version:
            raise EvidenceIndexCommandRejected(
                "Expected stream version does not match active run state.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        actor = self._authority.authorize(
            actor_id=command.actor_id,
            action=Action.INDEX_EVIDENCE,
            resource_id=command.run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise EvidenceIndexCommandRejected(
                "Evidence-index invalidation requires deterministic Builder code."
            )
        if (
            run.evidence_index_ref != command.index_id
            or run.evidence_index_invalidation_ref is not None
        ):
            raise EvidenceIndexInvalidated(
                "Only the active evidence index may be invalidated.",
                index_id=command.index_id,
            )
        index = self._repository.get_evidence_index(command.index_id)
        if index is None or index.run_id != run.run_id:
            raise EvidenceIndexCommandRejected(
                "Active evidence index cannot be reconstructed."
            )
        event_id = self._ids.new_id("event")
        invalidation = EvidenceIndexInvalidation.create(
            command_id=command.command_id,
            index=index,
            authority_identity=command.actor_id,
            reason=command.reason,
            event_ids=(event_id,),
            stream_version=run.stream_version + 1,
        )
        final_run, event = run.invalidate_evidence_index(
            index_ref=index.index_id,
            index_hash=index.index_hash,
            source_lock_ref=index.source_lock_ref,
            invalidation_ref=invalidation.invalidation_id,
            reason=command.reason,
            event_id=event_id,
            command_id=command.command_id,
            actor_id=command.actor_id,
            timestamp=self._clock.now(),
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        if (
            invalidation.event_ids != (event.event_id,)
            or invalidation.stream_version != final_run.stream_version
        ):
            raise EvidenceIndexCommandRejected("Invalidation event and receipt differ.")
        observations = (
            self._observation(
                event_name="ST-01.03:EvidenceIndexInvalidated",
                outcome="PASS",
                command=command,
                run=final_run,
                artifact_identity=index.index_id,
                authority_identity=command.actor_id,
                provenance=index.source_lock_ref,
                failure_context={"reason": command.reason},
            ),
        )
        self._repository.commit_evidence_index_invalidation(
            run_id=run.run_id,
            expected_version=command.expected_version,
            events=(event,),
            command_id=command.command_id,
            command_record=CommandRecord(
                payload_hash=_command_hash(command), result=invalidation
            ),
            invalidation=invalidation,
            observations=observations,
        )
        self._deliver_pending(command.command_id)
        return invalidation

    def _duplicate_index(
        self, command: IndexEvidenceCommand
    ) -> EvidenceIndexReceipt | None:
        record = self._repository.get_command_record(command.command_id)
        if record is None:
            return None
        self._validate_duplicate_payload(command, record)
        if not isinstance(record.result, EvidenceIndexReceipt):
            raise IdempotencyPayloadMismatch(
                "Stored command result is not an evidence-index receipt.",
                command_id=command.command_id,
            )
        return record.result

    def _duplicate_invalidation(
        self, command: InvalidateEvidenceIndexCommand
    ) -> EvidenceIndexInvalidation | None:
        record = self._repository.get_command_record(command.command_id)
        if record is None:
            return None
        self._validate_duplicate_payload(command, record)
        if not isinstance(record.result, EvidenceIndexInvalidation):
            raise IdempotencyPayloadMismatch(
                "Stored command result is not an evidence-index invalidation.",
                command_id=command.command_id,
            )
        return record.result

    @staticmethod
    def _validate_duplicate_payload(command: object, record: CommandRecord) -> None:
        observed = _command_hash(command)
        if observed != record.payload_hash:
            raise IdempotencyPayloadMismatch(
                "A command identity was reused with a different payload.",
                original_payload_hash=record.payload_hash,
                observed_payload_hash=observed,
            )

    @staticmethod
    def _validate_index_command(run: Run, command: IndexEvidenceCommand) -> None:
        if (
            run.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or not run.source_lock_ref
            or run.evidence_index_ref is not None
            and run.evidence_index_invalidation_ref is None
        ):
            raise EvidenceIndexCommandRejected(
                "Indexing requires one active Source Lock and no active evidence index.",
                lifecycle_state=run.lifecycle_state.value,
                source_lock_ref=run.source_lock_ref,
                evidence_index_ref=run.evidence_index_ref,
            )
        if command.expected_version != run.stream_version:
            raise EvidenceIndexCommandRejected(
                "Expected stream version does not match active run state.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        if (
            command.adapter_version != ADAPTER_VERSION
            or command.index_version != INDEX_VERSION
        ):
            raise EvidenceIndexCommandRejected(
                "Evidence-index compiler versions differ from capsule authority."
            )

    @staticmethod
    def _validate_active_source_lock(
        run: Run, source_lock: SourceLock | None
    ) -> None:
        attachments = tuple(
            event
            for event in run.events
            if event.event_type == "SourceLockAttached"
            and event.value("source_lock_ref") == run.source_lock_ref
        )
        if (
            source_lock is None
            or source_lock.run_id != run.run_id
            or source_lock.lock_id != run.source_lock_ref
            or len(attachments) != 1
            or attachments[0].value("aggregate_hash") != source_lock.aggregate_hash
            or attachments[0].value("source_profile_ref")
            != source_lock.source_profile_ref
        ):
            raise EvidenceIndexCommandRejected(
                "The active Source Lock is missing, altered or unverifiable."
            )

    def _success_observations(
        self,
        *,
        command: IndexEvidenceCommand,
        run: Run,
        source_lock: SourceLock,
        index: EvidenceIndex,
        receipt: EvidenceIndexReceipt,
    ) -> tuple[Observation, ...]:
        common = {
            "command": command,
            "run": run,
            "artifact_identity": index.index_id,
            "authority_identity": index.authority_identity,
            "provenance": source_lock.lock_id,
        }
        return (
            self._observation(
                event_name="ST-01.03:EvidenceIndexStarted",
                outcome="PASS",
                failure_context={},
                **common,
            ),
            self._observation(
                event_name="ST-01.03:SpecimenInventoryCompleted",
                outcome="PASS",
                failure_context={
                    "descriptor_count": index.descriptor_count,
                    "specimen_count": index.specimen_count,
                },
                **common,
            ),
            self._observation(
                event_name="ST-01.03:EvidenceIndexCommitted",
                outcome="PASS",
                failure_context={
                    "index_hash": index.index_hash,
                    "receipt_id": receipt.receipt_id,
                    "source_lock_hash": source_lock.aggregate_hash,
                },
                **common,
            ),
            self._observation(
                event_name="ST-01.03:OutcomeVerified",
                outcome="PASS",
                failure_context={"receipt_hash": receipt.receipt_hash},
                **common,
            ),
        )

    def _emit_replay(
        self, command: IndexEvidenceCommand, receipt: EvidenceIndexReceipt
    ) -> None:
        run = self._repository.load_run(receipt.run_id)
        self._observations.emit(
            self._observation(
                event_name="ST-01.03:EvidenceIndexReplayReturned",
                outcome="PASS",
                command=command,
                run=run,
                artifact_identity=receipt.index_id,
                authority_identity=receipt.authority_identity,
                provenance=receipt.source_lock_ref,
                failure_context={"receipt_id": receipt.receipt_id},
            )
        )

    def _emit_rejection(
        self,
        command: IndexEvidenceCommand,
        run: Run | None,
        source_lock: SourceLock | None,
        index: EvidenceIndex | None,
        error: Exception,
    ) -> None:
        try:
            self._observations.emit(
                self._observation(
                    event_name="ST-01.03:OutcomeRejected",
                    outcome="FAIL",
                    command=command,
                    run=run,
                    artifact_identity=(
                        index.index_id if index else run.state_hash() if run else "unassigned"
                    ),
                    authority_identity=command.actor_id,
                    provenance=(source_lock.lock_id if source_lock else "unassigned"),
                    failure_context={
                        "error_type": type(error).__name__,
                        "error_code": getattr(error, "code", type(error).__name__),
                    },
                )
            )
        except Exception:
            return

    def _deliver_pending(self, command_id: str) -> bool:
        while True:
            observation = self._repository.claim_pending_observation(command_id)
            if observation is None:
                return not self._repository.pending_observations(command_id)
            try:
                self._observations.emit(observation)
            except Exception:
                self._repository.release_observation_delivery(command_id, observation)
                return False
            self._repository.complete_observation_delivery(command_id, observation)

    @staticmethod
    def _observation(
        *,
        event_name: str,
        outcome: str,
        command: IndexEvidenceCommand | InvalidateEvidenceIndexCommand,
        run: Run | None,
        artifact_identity: str,
        authority_identity: str,
        provenance: str,
        failure_context: dict[str, object],
    ) -> Observation:
        profile = run.target_profile if run is not None else None
        return Observation(
            event_name=event_name,
            run_id=command.run_id,
            story_id="ST-01.03",
            artifact_identity=artifact_identity,
            authority_identity=authority_identity,
            version=INDEX_VERSION,
            provenance=provenance,
            outcome=outcome,
            failure_context=failure_context,
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
            command_id=command.command_id,
            target_id=profile.target_id if profile else "unassigned",
            category_id=profile.category_id if profile else "unassigned",
            profile_id=profile.profile_id if profile else "unassigned",
            stream_version=run.stream_version if run else 0,
            source_lock_id=provenance,
        )


def _command_hash(command: object) -> str:
    return sha256(_canonical_json(asdict(command))).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
