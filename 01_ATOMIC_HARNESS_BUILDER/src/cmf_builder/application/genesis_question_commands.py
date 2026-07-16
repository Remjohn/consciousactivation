from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    GenesisQuestionRepository,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.atomicity import DraftHarnessModel, ModelStatus
from cmf_builder.domain.evidence_saturation import SaturationEvaluation, SaturationOutcome
from cmf_builder.domain.genesis_questions import (
    GENESIS_QUESTION_VERSION,
    DecisionDefinition,
    DecisionGraph,
    EvidenceBackedRecommendation,
    GenesisQuestionInvalidation,
    GenesisQuestionPackage,
    GenesisQuestionReceipt,
    RecommendationAlternative,
)
from cmf_builder.domain.run import LifecycleState, Run


class GenesisQuestionCommandRejected(Exception):
    code = "GenesisQuestionCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class OpenGenesisQuestionCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    definitions: tuple[DecisionDefinition, ...]
    completed_decision_ids: tuple[str, ...]
    available_evidence_refs: tuple[str, ...]
    facts: tuple[str, ...]
    inferences: tuple[str, ...]
    alternatives: tuple[RecommendationAlternative, ...]
    contract_version: str = GENESIS_QUESTION_VERSION


@dataclass(frozen=True, slots=True)
class InvalidateGenesisQuestionCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    package_id: str
    reason: str


class GenesisQuestionCommandService:
    STORY_ID = "ST-03.01"

    def __init__(
        self,
        *,
        repository: GenesisQuestionRepository,
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

    def open(self, command: OpenGenesisQuestionCommand) -> GenesisQuestionReceipt:
        run: Run | None = None
        graph: DecisionGraph | None = None
        package: GenesisQuestionPackage | None = None
        try:
            duplicate = self._duplicate(command, GenesisQuestionReceipt)
            if duplicate is not None:
                self._deliver_pending(command.command_id)
                self._emit_replay(command, duplicate)
                return duplicate
            run = self._repository.load_run(command.run_id)
            self._validate_open_command(run, command)
            actor = self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.OPEN_GENESIS_QUESTION,
                resource_id=command.run_id,
                now=self._clock.now(),
            )
            if actor.kind is not ActorKind.CODE:
                raise GenesisQuestionCommandRejected("Only deterministic Builder code may select the active question.")
            model, saturation = self._active_inputs(run)
            graph = DecisionGraph.compile(
                run_id=run.run_id,
                target_profile_id=run.target_profile.profile_id,
                source_lock_ref=run.source_lock_ref or "",
                boundary_ref=run.atomic_boundary_ref or "",
                ratification_ref=run.atomicity_ratification_ref or "",
                model=model,
                saturation=saturation,
                definitions=command.definitions,
                completed_decision_ids=command.completed_decision_ids,
                available_evidence_refs=command.available_evidence_refs,
            )
            selected = graph.selected_node().definition
            recommendation = EvidenceBackedRecommendation.create(
                definition=selected,
                facts=command.facts,
                inferences=command.inferences,
                evidence_refs=command.available_evidence_refs,
                alternatives=command.alternatives,
            )
            package = GenesisQuestionPackage.compile(
                graph=graph,
                recommendation=recommendation,
                authority_identity=actor.actor_id,
            )
            event_id = self._ids.new_id("event")
            next_run, event = run.attach_genesis_question(
                package_ref=package.package_id,
                package_hash=package.package_hash,
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                model_ref=model.model_id,
                saturation_ref=saturation.evaluation_id,
                selected_decision_id=graph.selected_decision_id,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=actor.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = GenesisQuestionReceipt.create(
                receipt_id=self._ids.new_id("genesis-question-receipt"),
                command_id=command.command_id,
                run_id=run.run_id,
                graph_id=graph.graph_id,
                graph_hash=graph.graph_hash,
                package_id=package.package_id,
                package_hash=package.package_hash,
                selected_decision_id=graph.selected_decision_id,
                authority_identity=actor.actor_id,
                event_ids=(event.event_id,),
                stream_version=event.stream_version,
                outcome="PASS",
            )
            observations = self._success_observations(command, next_run, graph, package, receipt)
            self._repository.commit_genesis_question(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=_command_hash(command), result=receipt),
                graph=graph,
                package=package,
                receipt=receipt,
                observations=observations,
            )
            self._deliver_pending(command.command_id)
            return receipt
        except Exception as error:
            self._emit_rejection(command, run, graph, package, error)
            raise

    def invalidate(self, command: InvalidateGenesisQuestionCommand) -> GenesisQuestionInvalidation:
        duplicate = self._duplicate(command, GenesisQuestionInvalidation)
        if duplicate is not None:
            self._deliver_pending(command.command_id)
            return duplicate
        run = self._repository.load_run(command.run_id)
        if command.expected_version != run.stream_version or run.genesis_question_ref != command.package_id:
            raise GenesisQuestionCommandRejected("Invalidation must target the exact active package and stream.")
        actor = self._authority.authorize(
            actor_id=command.actor_id, action=Action.OPEN_GENESIS_QUESTION,
            resource_id=command.run_id, now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE or not command.reason.strip():
            raise GenesisQuestionCommandRejected("Code authority and a governed reason are required.")
        package = self._repository.get_genesis_question_package(command.package_id)
        if package is None or package.package_hash != run.genesis_question_hash:
            raise GenesisQuestionCommandRejected("Active package bytes are unavailable or altered.")
        invalidation_id = self._ids.new_id("genesis-question-invalidation")
        event_id = self._ids.new_id("event")
        next_run, event = run.invalidate_genesis_question(
            package_ref=package.package_id, package_hash=package.package_hash,
            invalidation_ref=invalidation_id, reason=command.reason,
            event_id=event_id, command_id=command.command_id, actor_id=actor.actor_id,
            timestamp=self._clock.now(), correlation_id=command.correlation_id,
            causation_id=command.causation_id,
        )
        invalidation = GenesisQuestionInvalidation.create(
            invalidation_id=invalidation_id, command_id=command.command_id,
            run_id=run.run_id, package_id=package.package_id,
            package_hash=package.package_hash, reason=command.reason,
            authority_identity=actor.actor_id, event_ids=(event.event_id,),
            stream_version=event.stream_version,
        )
        observations = (
            self._observation(
                event_name="ST-03.01:QuestionPackageInvalidated", outcome="INVALIDATED",
                command=command, run=next_run, artifact_identity=package.package_id,
                authority_identity=actor.actor_id, provenance=package.graph_ref,
                failure_context={"invalidation_id": invalidation.invalidation_id, "reason": command.reason},
            ),
        )
        self._repository.commit_genesis_question_invalidation(
            run_id=run.run_id, expected_version=command.expected_version,
            events=(event,), command_id=command.command_id,
            command_record=CommandRecord(payload_hash=_command_hash(command), result=invalidation),
            invalidation=invalidation, observations=observations,
        )
        self._deliver_pending(command.command_id)
        return invalidation

    @staticmethod
    def _validate_open_command(run: Run, command: OpenGenesisQuestionCommand) -> None:
        if (
            run.lifecycle_state is not LifecycleState.ATOMICITY_RATIFICATION
            or command.expected_version != run.stream_version
            or command.contract_version != GENESIS_QUESTION_VERSION
            or not run.source_lock_ref or not run.atomic_boundary_ref
            or not run.atomicity_ratification_ref or not run.draft_harness_model_ref
            or not run.saturation_evaluation_ref
            or run.boundary_invalidation_ref is not None
            or run.saturation_evaluation_invalidation_ref is not None
            or run.genesis_question_ref is not None and run.genesis_question_invalidation_ref is None
        ):
            raise GenesisQuestionCommandRejected("Genesis entry gates or expected stream version are not satisfied.")

    def _active_inputs(self, run: Run) -> tuple[DraftHarnessModel, SaturationEvaluation]:
        model = self._repository.get_draft_harness_model(run.draft_harness_model_ref or "")
        saturation = self._repository.get_saturation_evaluation(run.saturation_evaluation_ref or "")
        if (
            model is None or saturation is None
            or model.status is not ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS
            or model.boundary_ref != run.atomic_boundary_ref
            or model.source_lock_ref != run.source_lock_ref
            or saturation.evaluation_hash != run.saturation_evaluation_hash
            or saturation.source_lock_ref != run.source_lock_ref
            or saturation.outcome not in {SaturationOutcome.PASS, SaturationOutcome.PASS_WITH_LIMITATIONS}
        ):
            raise GenesisQuestionCommandRejected("Active model or saturation evidence is absent, stale or inconsistent.")
        return model, saturation

    def _duplicate(self, command: object, expected: type):
        record = self._repository.get_command_record(getattr(command, "command_id"))
        if record is None:
            return None
        if record.payload_hash != _command_hash(command):
            raise IdempotencyPayloadMismatch("A command identity was reused with a different payload.")
        if not isinstance(record.result, expected):
            raise IdempotencyPayloadMismatch("Stored result type does not match this Genesis command.")
        return record.result

    def _success_observations(self, command, run, graph, package, receipt) -> tuple[Observation, ...]:
        common = dict(command=command, run=run, artifact_identity=package.package_id,
                      authority_identity=package.authority_identity, provenance=graph.graph_id)
        return (
            self._observation(event_name="ST-03.01:QuestionPackageCompiled", outcome="PASS", failure_context={"node_count": len(graph.nodes), "selected_decision_id": graph.selected_decision_id}, **common),
            self._observation(event_name="ST-03.01:OutcomeVerified", outcome="PASS", failure_context={"receipt_id": receipt.receipt_id, "recommendation_id": package.recommendation.recommendation_id}, **common),
        )

    def _emit_replay(self, command, receipt) -> None:
        run = self._repository.load_run(receipt.run_id)
        self._observations.emit(self._observation(
            event_name="ST-03.01:QuestionPackageReplayReturned", outcome="PASS",
            command=command, run=run, artifact_identity=receipt.package_id,
            authority_identity=receipt.authority_identity, provenance=receipt.graph_id,
            failure_context={"receipt_id": receipt.receipt_id},
        ))

    def _emit_rejection(self, command, run, graph, package, error) -> None:
        try:
            self._observations.emit(self._observation(
                event_name="ST-03.01:QuestionPackageRejected", outcome="FAIL",
                command=command, run=run,
                artifact_identity=package.package_id if package else graph.graph_id if graph else "unassigned",
                authority_identity=command.actor_id,
                provenance=run.draft_harness_model_ref if run and run.draft_harness_model_ref else "unassigned",
                failure_context={"error_type": type(error).__name__, "error_code": getattr(error, "code", type(error).__name__)},
            ))
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
    def _observation(*, event_name, outcome, command, run, artifact_identity, authority_identity, provenance, failure_context) -> Observation:
        profile = run.target_profile if run else None
        return Observation(
            event_name=event_name, run_id=command.run_id, story_id="ST-03.01",
            artifact_identity=artifact_identity, authority_identity=authority_identity,
            version=GENESIS_QUESTION_VERSION, provenance=provenance, outcome=outcome,
            failure_context=failure_context, correlation_id=command.correlation_id,
            causation_id=command.causation_id, command_id=command.command_id,
            target_id=profile.target_id if profile else "unassigned",
            category_id=profile.category_id if profile else "unassigned",
            profile_id=profile.profile_id if profile else "unassigned",
            stream_version=run.stream_version if run else 0,
            source_lock_id=run.source_lock_ref if run and run.source_lock_ref else "unassigned",
            boundary_id=run.atomic_boundary_ref if run and run.atomic_boundary_ref else "unassigned",
            model_id=run.draft_harness_model_ref if run and run.draft_harness_model_ref else "unassigned",
            model_status=ModelStatus.UNRATIFIED_CONSTITUTIONAL_FIELDS.value if run and run.draft_harness_model_ref else "unassigned",
        )


def _command_hash(command: object) -> str:
    return sha256(json.dumps(asdict(command), sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=lambda item: item.value).encode("utf-8")).hexdigest()
