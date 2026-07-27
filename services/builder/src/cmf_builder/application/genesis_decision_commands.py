from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock, CommandRecord, GenesisDecisionRepository, IdProvider,
    IdempotencyPayloadMismatch, Observation, ObservationSink,
)
from cmf_builder.domain.genesis_decisions import (
    GENESIS_DECISION_VERSION, FinalDecision, GenesisDecisionInvalidation,
    GenesisDecisionMemory, GenesisDecisionReceipt, HarnessIRDecisionAmendment,
    HumanAnswer,
)
from cmf_builder.domain.run import Run


class GenesisDecisionCommandRejected(Exception):
    code = "GenesisDecisionCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class RecordGenesisDecisionCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    package_id: str
    raw_answer: str
    selected_option: str
    rationale: str
    provisional_draft_ref: str | None = None
    contract_version: str = GENESIS_DECISION_VERSION


@dataclass(frozen=True, slots=True)
class ReopenGenesisDecisionCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    memory_id: str
    reason: str


class GenesisDecisionCommandService:
    STORY_ID = "ST-03.02"

    def __init__(self, *, repository: GenesisDecisionRepository, authority: AuthorityService,
                 ids: IdProvider, clock: Clock, observations: ObservationSink) -> None:
        self._repository = repository
        self._authority = authority
        self._ids = ids
        self._clock = clock
        self._observations = observations

    def record(self, command: RecordGenesisDecisionCommand) -> GenesisDecisionReceipt:
        run: Run | None = None
        try:
            duplicate = self._duplicate(command, GenesisDecisionReceipt)
            if duplicate is not None:
                self._deliver_pending(command.command_id)
                self._emit("ST-03.02:DecisionReplayReturned", "PASS", command, self._repository.load_run(command.run_id), duplicate.memory_id, duplicate.authority_identity, {"receipt_id": duplicate.receipt_id})
                return duplicate
            run = self._repository.load_run(command.run_id)
            if (
                command.expected_version != run.stream_version
                or command.contract_version != GENESIS_DECISION_VERSION
                or run.genesis_question_ref != command.package_id
                or run.genesis_question_invalidation_ref is not None
                or run.genesis_decision_memory_ref is not None and run.genesis_decision_invalidation_ref is None
            ):
                raise GenesisDecisionCommandRejected("The active question, stream or decision state is not eligible for ratification.")
            actor = self._authority.authorize(
                actor_id=command.actor_id, action=Action.RATIFY_GENESIS_DECISION,
                resource_id=command.run_id, now=self._clock.now(),
            )
            if actor.kind is not ActorKind.HUMAN:
                raise GenesisDecisionCommandRejected("Only human authority may answer and ratify Genesis.")
            package = self._repository.get_genesis_question_package(command.package_id)
            if package is None or package.package_hash != run.genesis_question_hash:
                raise GenesisDecisionCommandRejected("Active question package is absent, altered or stale.")
            graph = self._repository.get_decision_graph(package.graph_ref)
            model = self._repository.get_draft_harness_model(run.draft_harness_model_ref or "")
            if graph is None or model is None or graph.graph_hash != package.graph_hash or graph.model_ref != model.model_id or graph.model_hash != model.model_hash:
                raise GenesisDecisionCommandRejected("Question graph or Draft Harness Model lineage is unverifiable.")
            answer = HumanAnswer.create(
                run_id=run.run_id, package_ref=package.package_id,
                package_hash=package.package_hash, decision_node_id=package.selected_decision_id,
                raw_answer=command.raw_answer, human_id=actor.actor_id,
                answered_at=self._clock.now(),
            )
            decision = FinalDecision.create(
                answer=answer, selected_option=command.selected_option,
                rationale=command.rationale, provisional_draft_ref=command.provisional_draft_ref,
            )
            amendment = HarnessIRDecisionAmendment.compile(
                model=model, graph=graph, package=package, answer=answer, decision=decision,
            )
            memory = GenesisDecisionMemory.compile(
                graph=graph, package=package, answer=answer, decision=decision,
                amendment=amendment, prior_memory=None,
            )
            event_id = self._ids.new_id("event")
            next_run, event = run.attach_genesis_decision_memory(
                memory_ref=memory.memory_id, memory_hash=memory.memory_hash,
                answer_ref=answer.answer_id, final_decision_ref=decision.final_decision_id,
                amendment_ref=amendment.amendment_id, graph_ref=graph.graph_id,
                package_ref=package.package_id, cascade_status=memory.cascade_status.value,
                event_id=event_id, command_id=command.command_id, actor_id=actor.actor_id,
                timestamp=self._clock.now(), correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = GenesisDecisionReceipt.create(
                receipt_id=self._ids.new_id("genesis-decision-receipt"),
                command_id=command.command_id, run_id=run.run_id,
                answer_id=answer.answer_id, answer_hash=answer.answer_hash,
                final_decision_id=decision.final_decision_id,
                final_decision_hash=decision.final_decision_hash,
                amendment_id=amendment.amendment_id, amendment_hash=amendment.amendment_hash,
                memory_id=memory.memory_id, memory_hash=memory.memory_hash,
                authority_identity=actor.actor_id, event_ids=(event.event_id,),
                stream_version=event.stream_version, outcome="PASS",
            )
            observations = (
                self._observation("ST-03.02:HumanDecisionRecorded", "PASS", command, next_run, memory.memory_id, actor.actor_id, {"answer_id": answer.answer_id, "final_decision_id": decision.final_decision_id, "amendment_id": amendment.amendment_id}),
                self._observation("ST-03.02:OutcomeVerified", "PASS", command, next_run, memory.memory_id, actor.actor_id, {"receipt_id": receipt.receipt_id, "cascade_status": memory.cascade_status.value}),
            )
            self._repository.commit_genesis_decision(
                run_id=run.run_id, expected_version=command.expected_version, events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=_command_hash(command), result=receipt),
                answer=answer, decision=decision, amendment=amendment, memory=memory,
                receipt=receipt, observations=observations,
            )
            self._deliver_pending(command.command_id)
            return receipt
        except Exception as error:
            self._emit("ST-03.02:OutcomeRejected", "FAIL", command, run, "unassigned", command.actor_id, {"error_type": type(error).__name__, "error_code": getattr(error, "code", type(error).__name__)})
            raise

    def resume(self, *, run_id: str, actor_id: str, correlation_id: str, causation_id: str) -> GenesisDecisionMemory:
        run = self._repository.load_run(run_id)
        self._authority.authorize(actor_id=actor_id, action=Action.RATIFY_GENESIS_DECISION, resource_id=run_id, now=self._clock.now())
        memory = self._repository.active_genesis_decision_memory(run_id)
        if memory is None:
            raise GenesisDecisionCommandRejected("No active Genesis decision memory can be resumed.")
        command = type("Resume", (), {"run_id": run_id, "command_id": "resume-query", "correlation_id": correlation_id, "causation_id": causation_id})()
        self._emit("ST-03.02:DecisionMemoryResumed", "PASS", command, run, memory.memory_id, actor_id, {"resolved_decision_ids": memory.resolved_decision_ids, "ready_decision_ids": memory.ready_decision_ids})
        return memory

    def reopen(self, command: ReopenGenesisDecisionCommand) -> GenesisDecisionInvalidation:
        duplicate = self._duplicate(command, GenesisDecisionInvalidation)
        if duplicate is not None:
            self._deliver_pending(command.command_id)
            return duplicate
        run = self._repository.load_run(command.run_id)
        if command.expected_version != run.stream_version or run.genesis_decision_memory_ref != command.memory_id or not command.reason.strip():
            raise GenesisDecisionCommandRejected("Reopen must target the exact active memory with a reason.")
        actor = self._authority.authorize(actor_id=command.actor_id, action=Action.REOPEN_GENESIS_DECISION, resource_id=command.run_id, now=self._clock.now())
        memory = self._repository.active_genesis_decision_memory(command.run_id)
        if actor.kind is not ActorKind.HUMAN or memory is None:
            raise GenesisDecisionCommandRejected("Only human authority may reopen active Genesis memory.")
        graph = self._repository.get_decision_graph(memory.graph_ref)
        if graph is None:
            raise GenesisDecisionCommandRejected("Decision graph history is unavailable.")
        affected = tuple(sorted({edge for node in graph.nodes if node.definition.decision_id in memory.resolved_decision_ids for edge in node.definition.invalidation_edges}))
        invalidation_id = self._ids.new_id("genesis-decision-invalidation")
        event_id = self._ids.new_id("event")
        next_run, event = run.invalidate_genesis_decision_memory(
            memory_ref=memory.memory_id, memory_hash=memory.memory_hash,
            invalidation_ref=invalidation_id, reason=command.reason,
            event_id=event_id, command_id=command.command_id, actor_id=actor.actor_id,
            timestamp=self._clock.now(), correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        invalidation = GenesisDecisionInvalidation.create(
            invalidation_id=invalidation_id, command_id=command.command_id,
            run_id=run.run_id, memory_id=memory.memory_id, memory_hash=memory.memory_hash,
            affected_amendment_ids=memory.amendment_refs,
            affected_descendant_decision_ids=affected, reason=command.reason,
            authority_identity=actor.actor_id, event_ids=(event.event_id,),
            stream_version=event.stream_version,
        )
        observations = (self._observation("ST-03.02:DecisionMemoryInvalidated", "INVALIDATED", command, next_run, memory.memory_id, actor.actor_id, {"invalidation_id": invalidation.invalidation_id, "affected_descendants": affected}),)
        self._repository.commit_genesis_decision_invalidation(
            run_id=run.run_id, expected_version=command.expected_version, events=(event,),
            command_id=command.command_id,
            command_record=CommandRecord(payload_hash=_command_hash(command), result=invalidation),
            invalidation=invalidation, observations=observations,
        )
        self._deliver_pending(command.command_id)
        return invalidation

    def _duplicate(self, command: object, expected: type):
        record = self._repository.get_command_record(getattr(command, "command_id"))
        if record is None: return None
        if record.payload_hash != _command_hash(command) or not isinstance(record.result, expected):
            raise IdempotencyPayloadMismatch("Genesis command identity was reused with a different payload or result type.")
        return record.result

    def _deliver_pending(self, command_id: str) -> None:
        while True:
            item = self._repository.claim_pending_observation(command_id)
            if item is None: return
            try: self._observations.emit(item)
            except Exception:
                self._repository.release_observation_delivery(command_id, item); return
            self._repository.complete_observation_delivery(command_id, item)

    def _emit(self, name, outcome, command, run, artifact, authority, context) -> None:
        try: self._observations.emit(self._observation(name, outcome, command, run, artifact, authority, context))
        except Exception: return

    @staticmethod
    def _observation(name, outcome, command, run, artifact, authority, context) -> Observation:
        profile = run.target_profile if run else None
        return Observation(
            event_name=name, run_id=command.run_id, story_id="ST-03.02",
            artifact_identity=artifact, authority_identity=authority,
            version=GENESIS_DECISION_VERSION,
            provenance=run.genesis_question_ref if run and run.genesis_question_ref else "unassigned",
            outcome=outcome, failure_context=context, correlation_id=command.correlation_id,
            causation_id=command.causation_id, command_id=command.command_id,
            target_id=profile.target_id if profile else "unassigned",
            category_id=profile.category_id if profile else "unassigned",
            profile_id=profile.profile_id if profile else "unassigned",
            stream_version=run.stream_version if run else 0,
            source_lock_id=run.source_lock_ref if run and run.source_lock_ref else "unassigned",
            boundary_id=run.atomic_boundary_ref if run and run.atomic_boundary_ref else "unassigned",
            model_id=run.draft_harness_model_ref if run and run.draft_harness_model_ref else "unassigned",
        )


def _command_hash(command: object) -> str:
    return sha256(json.dumps(asdict(command), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
