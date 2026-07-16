from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
    SaturationRepository,
)
from cmf_builder.domain.evidence_index import EvidenceIndex
from cmf_builder.domain.evidence_saturation import (
    SATURATION_VERSION,
    SaturationConcern,
    SaturationContract,
    SaturationEvaluation,
    SaturationEvaluationInvalidated,
    SaturationInvalidation,
    SaturationReceipt,
)
from cmf_builder.domain.evidence_workspace import SourceLock
from cmf_builder.domain.run import LifecycleState, Run


class SaturationCommandRejected(Exception):
    code = "SaturationCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class EvaluateSaturationCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    contract: SaturationContract
    concerns: tuple[SaturationConcern, ...] = ()
    human_waiver_ref: str | None = None
    evaluator_version: str = SATURATION_VERSION


@dataclass(frozen=True, slots=True)
class InvalidateSaturationCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    evaluation_id: str
    reason: str


class SaturationCommandService:
    STORY_ID = "ST-01.04"

    def __init__(
        self,
        *,
        repository: SaturationRepository,
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

    def evaluate(self, command: EvaluateSaturationCommand) -> SaturationReceipt:
        run: Run | None = None
        source_lock: SourceLock | None = None
        index: EvidenceIndex | None = None
        evaluation: SaturationEvaluation | None = None
        committed = False
        try:
            duplicate = self._duplicate_evaluation(command)
            if duplicate is not None:
                self._deliver_pending(command.command_id)
                self._emit_replay(command, duplicate)
                return duplicate
            run = self._repository.load_run(command.run_id)
            self._validate_command(run, command)
            actor = self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.EVALUATE_SATURATION,
                resource_id=command.run_id,
                now=self._clock.now(),
            )
            if actor.kind is not ActorKind.CODE:
                raise SaturationCommandRejected(
                    "Saturation evaluation may be committed only by deterministic Builder code."
                )
            if command.human_waiver_ref is not None:
                raise SaturationCommandRejected(
                    "Code authority cannot issue or apply PASS_WITH_LIMITATIONS."
                )
            source_lock = self._repository.get_source_lock(run.source_lock_ref or "")
            index = self._repository.active_evidence_index(run.run_id)
            self._validate_active_inputs(run, source_lock, index)
            assert source_lock is not None and index is not None
            evaluation = SaturationEvaluation.evaluate(
                run_id=run.run_id,
                source_lock=source_lock,
                index=index,
                contract=command.contract,
                authority_identity=command.actor_id,
                concerns=command.concerns,
            )
            final_run, event = run.attach_saturation_evaluation(
                evaluation_ref=evaluation.evaluation_id,
                evaluation_hash=evaluation.evaluation_hash,
                contract_ref=evaluation.contract_id,
                contract_hash=evaluation.contract_hash,
                source_lock_ref=evaluation.source_lock_ref,
                evidence_index_ref=evaluation.evidence_index_ref,
                outcome=evaluation.outcome.value,
                downstream_consequence=evaluation.downstream_consequence.value,
                event_id=self._ids.new_id("event"),
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = SaturationReceipt.create(
                command_id=command.command_id,
                evaluation=evaluation,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            observations = self._success_observations(
                command=command,
                run=final_run,
                evaluation=evaluation,
                receipt=receipt,
            )
            self._repository.commit_saturation_evaluation(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(
                    payload_hash=_command_hash(command), result=receipt
                ),
                contract=command.contract,
                evaluation=evaluation,
                receipt=receipt,
                observations=observations,
            )
            committed = True
            self._deliver_pending(command.command_id)
            return receipt
        except Exception as error:
            if not committed:
                self._emit_rejection(command, run, source_lock, index, evaluation, error)
            raise

    def invalidate(self, command: InvalidateSaturationCommand) -> SaturationInvalidation:
        duplicate = self._duplicate_invalidation(command)
        if duplicate is not None:
            self._deliver_pending(command.command_id)
            return duplicate
        run = self._repository.load_run(command.run_id)
        if command.expected_version != run.stream_version:
            raise SaturationCommandRejected(
                "Expected stream version does not match active run state.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        actor = self._authority.authorize(
            actor_id=command.actor_id,
            action=Action.EVALUATE_SATURATION,
            resource_id=command.run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise SaturationCommandRejected("Saturation invalidation requires deterministic Builder code.")
        if (
            run.saturation_evaluation_ref != command.evaluation_id
            or run.saturation_evaluation_invalidation_ref is not None
        ):
            raise SaturationEvaluationInvalidated(
                "Only the active saturation evaluation may be invalidated.",
                evaluation_id=command.evaluation_id,
            )
        evaluation = self._repository.get_saturation_evaluation(command.evaluation_id)
        if evaluation is None or evaluation.run_id != run.run_id:
            raise SaturationCommandRejected("Active saturation evaluation cannot be reconstructed.")
        event_id = self._ids.new_id("event")
        invalidation = SaturationInvalidation.create(
            command_id=command.command_id,
            evaluation=evaluation,
            authority_identity=command.actor_id,
            reason=command.reason,
            event_ids=(event_id,),
            stream_version=run.stream_version + 1,
        )
        final_run, event = run.invalidate_saturation_evaluation(
            evaluation_ref=evaluation.evaluation_id,
            evaluation_hash=evaluation.evaluation_hash,
            invalidation_ref=invalidation.invalidation_id,
            reason=command.reason,
            event_id=event_id,
            command_id=command.command_id,
            actor_id=command.actor_id,
            timestamp=self._clock.now(),
            correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        observations = (
            self._observation(
                event_name="ST-01.04:SaturationInvalidated",
                outcome="PASS",
                command=command,
                run=final_run,
                artifact_identity=evaluation.evaluation_id,
                authority_identity=command.actor_id,
                provenance=evaluation.evidence_index_ref,
                failure_context={"reason": command.reason},
            ),
        )
        self._repository.commit_saturation_invalidation(
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

    def _duplicate_evaluation(
        self, command: EvaluateSaturationCommand
    ) -> SaturationReceipt | None:
        record = self._repository.get_command_record(command.command_id)
        if record is None:
            return None
        self._validate_duplicate_payload(command, record)
        if not isinstance(record.result, SaturationReceipt):
            raise IdempotencyPayloadMismatch(
                "Stored command result is not a saturation receipt.",
                command_id=command.command_id,
            )
        return record.result

    def _duplicate_invalidation(
        self, command: InvalidateSaturationCommand
    ) -> SaturationInvalidation | None:
        record = self._repository.get_command_record(command.command_id)
        if record is None:
            return None
        self._validate_duplicate_payload(command, record)
        if not isinstance(record.result, SaturationInvalidation):
            raise IdempotencyPayloadMismatch(
                "Stored command result is not a saturation invalidation.",
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
    def _validate_command(run: Run, command: EvaluateSaturationCommand) -> None:
        if (
            run.lifecycle_state is not LifecycleState.SOURCE_LOCKED
            or not run.source_lock_ref
            or not run.evidence_index_ref
            or run.evidence_index_invalidation_ref is not None
            or run.saturation_evaluation_ref is not None
            and run.saturation_evaluation_invalidation_ref is None
        ):
            raise SaturationCommandRejected(
                "Saturation requires an active Source Lock and Evidence Index with no active evaluation."
            )
        if command.expected_version != run.stream_version:
            raise SaturationCommandRejected(
                "Expected stream version does not match active run state.",
                expected_version=command.expected_version,
                current_version=run.stream_version,
            )
        if command.evaluator_version != SATURATION_VERSION:
            raise SaturationCommandRejected("Saturation evaluator version differs from capsule authority.")

    @staticmethod
    def _validate_active_inputs(
        run: Run, source_lock: SourceLock | None, index: EvidenceIndex | None
    ) -> None:
        if (
            source_lock is None
            or index is None
            or source_lock.run_id != run.run_id
            or source_lock.lock_id != run.source_lock_ref
            or index.run_id != run.run_id
            or index.index_id != run.evidence_index_ref
            or index.index_hash != run.evidence_index_hash
            or index.source_lock_ref != source_lock.lock_id
            or index.source_lock_hash != source_lock.aggregate_hash
        ):
            raise SaturationCommandRejected(
                "The active Source Lock or Evidence Index is missing, altered, stale or unverifiable."
            )

    def _success_observations(
        self,
        *,
        command: EvaluateSaturationCommand,
        run: Run,
        evaluation: SaturationEvaluation,
        receipt: SaturationReceipt,
    ) -> tuple[Observation, ...]:
        common = {
            "command": command,
            "run": run,
            "artifact_identity": evaluation.evaluation_id,
            "authority_identity": evaluation.authority_identity,
            "provenance": evaluation.evidence_index_ref,
        }
        return (
            self._observation(
                event_name="ST-01.04:SaturationEvaluated",
                outcome=evaluation.outcome.value,
                failure_context={
                    "contract_id": evaluation.contract_id,
                    "contract_hash": evaluation.contract_hash,
                    "gap_count": len(evaluation.gaps),
                    "authority_conflict_count": len(evaluation.authority_conflicts),
                    "downstream_consequence": evaluation.downstream_consequence.value,
                },
                **common,
            ),
            self._observation(
                event_name="ST-01.04:OutcomeVerified",
                outcome=evaluation.outcome.value,
                failure_context={
                    "receipt_id": receipt.receipt_id,
                    "receipt_hash": receipt.receipt_hash,
                    "source_lock_hash": evaluation.source_lock_hash,
                    "evidence_index_hash": evaluation.evidence_index_hash,
                },
                **common,
            ),
        )

    def _emit_replay(
        self, command: EvaluateSaturationCommand, receipt: SaturationReceipt
    ) -> None:
        run = self._repository.load_run(receipt.run_id)
        self._observations.emit(
            self._observation(
                event_name="ST-01.04:SaturationReplayReturned",
                outcome=receipt.outcome.value,
                command=command,
                run=run,
                artifact_identity=receipt.evaluation_id,
                authority_identity=receipt.authority_identity,
                provenance=run.evidence_index_ref or "unassigned",
                failure_context={"receipt_id": receipt.receipt_id},
            )
        )

    def _emit_rejection(
        self,
        command: EvaluateSaturationCommand,
        run: Run | None,
        source_lock: SourceLock | None,
        index: EvidenceIndex | None,
        evaluation: SaturationEvaluation | None,
        error: Exception,
    ) -> None:
        try:
            self._observations.emit(
                self._observation(
                    event_name="ST-01.04:OutcomeRejected",
                    outcome="FAIL",
                    command=command,
                    run=run,
                    artifact_identity=(
                        evaluation.evaluation_id
                        if evaluation
                        else run.state_hash() if run else "unassigned"
                    ),
                    authority_identity=command.actor_id,
                    provenance=(index.index_id if index else source_lock.lock_id if source_lock else "unassigned"),
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
        command: EvaluateSaturationCommand | InvalidateSaturationCommand,
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
            story_id="ST-01.04",
            artifact_identity=artifact_identity,
            authority_identity=authority_identity,
            version=SATURATION_VERSION,
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
            source_lock_id=run.source_lock_ref if run and run.source_lock_ref else "unassigned",
        )


def _command_hash(command: object) -> str:
    return sha256(_canonical_json(asdict(command))).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
