from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
    PhaseHandoffRepository,
)
from cmf_builder.domain.handoff import (
    PHASE_GRAPH_CONTRACT,
    PHASE_HANDOFF_GRAPH_SCHEMA_ID,
    PHASE_HANDOFF_GRAPH_SCHEMA_VERSION,
    PHASE_HANDOFF_INPUT_PATH,
    PHASE_HANDOFF_INPUT_SCHEMA,
    PHASE_HANDOFF_INPUT_SHA256,
    PHASE_HANDOFF_SCOPE,
    ContextFieldDeclaration,
    GovernedHandoffArtifact,
    HandoffAuthorityInvalid,
    HandoffContractInvalid,
    HandoffFieldDeclaration,
    HandoffInputInvalid,
    HandoffInvalidatedError,
    HandoffLineageInvalid,
    HandoffStateInvalid,
    InternalHandoff,
    InternalHandoffDecision,
    InternalHandoffDecisionAction,
    InternalHandoffReceipt,
    PhaseContextContract,
    PhaseHandoffContract,
    PhaseHandoffGraph,
    PhaseHandoffReceipt,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.phase_graph import PhaseGraph
from cmf_builder.domain.run import LifecycleState, Run


class HandoffCommandRejected(Exception):
    code = "HandoffCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class CompilePhaseHandoffsCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    handoff_input_path: str = PHASE_HANDOFF_INPUT_PATH
    handoff_input_sha256: str = PHASE_HANDOFF_INPUT_SHA256


@dataclass(frozen=True, slots=True)
class IssueInternalHandoffCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    contract_id: str
    sender_phase: str
    receiver_phase: str
    artifacts: tuple[GovernedHandoffArtifact, ...]


@dataclass(frozen=True, slots=True)
class DecideInternalHandoffCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    handoff_id: str
    receiver_phase: str
    receiver_authority: str
    action: InternalHandoffDecisionAction
    reason_code: str
    reason: str


class PhaseHandoffCommandService:
    STORY_ID = "ST-04.04"
    CONTRACT_VERSION = (
        f"{PHASE_HANDOFF_GRAPH_SCHEMA_ID}@{PHASE_HANDOFF_GRAPH_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: PhaseHandoffRepository,
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

    def compile(self, command: CompilePhaseHandoffsCommand) -> PhaseHandoffReceipt:
        run: Run | None = None
        phase_graph: PhaseGraph | None = None
        graph: PhaseHandoffGraph | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash, PhaseHandoffReceipt)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_common(command)
            if (
                command.handoff_input_path != PHASE_HANDOFF_INPUT_PATH
                or command.handoff_input_sha256 != PHASE_HANDOFF_INPUT_SHA256
            ):
                raise HandoffInputInvalid("The governed handoff input pin is invalid.")
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            phase_graph = self._load_phase_parent(run)
            contexts, contracts = self._load_input(command, phase_graph)
            graph = PhaseHandoffGraph.create(
                phase_graph=phase_graph,
                contexts=contexts,
                contracts=contracts,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_phase_handoffs(
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                phase_graph_ref=phase_graph.graph_id,
                harness_ir_ref=phase_graph.ir_id,
                context_count=len(graph.context_graph.contexts),
                contract_count=len(graph.contracts),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = PhaseHandoffReceipt.create(
                command_id=command.command_id,
                graph=graph,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_phase_handoffs(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                graph=graph,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.04:ContextGraphCompiled",
                "ST-04.04:HandoffContractsCompiled",
                "ST-04.04:OwnershipAndMutationLimitsValidated",
                "ST-04.04:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    phase_graph=phase_graph,
                    graph=graph,
                    handoff=None,
                    receipt=receipt,
                    decision=None,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit_failure(command, error, run, phase_graph, graph)
            raise

    def issue(self, command: IssueInternalHandoffCommand) -> InternalHandoffReceipt:
        run: Run | None = None
        phase_graph: PhaseGraph | None = None
        graph: PhaseHandoffGraph | None = None
        handoff: InternalHandoff | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash, InternalHandoffReceipt)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_common(command)
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            graph, phase_graph = self._load_active_graph(run)
            try:
                contract = graph.contract(command.contract_id)
            except KeyError as error:
                raise HandoffContractInvalid("The requested handoff contract is undeclared.") from error
            if command.sender_phase != contract.producer_phase:
                raise HandoffContractInvalid("The command sender is not the governed producer phase.")
            self._verify_artifacts(graph, contract, command.artifacts)
            handoff = InternalHandoff.create(
                graph=graph,
                phase_graph=phase_graph,
                contract=contract,
                receiver_phase=command.receiver_phase,
                artifacts=command.artifacts,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.record_internal_handoff_event(
                event_type="InternalHandoffIssued",
                handoff_graph_ref=graph.graph_id,
                handoff_ref=handoff.handoff_id,
                handoff_hash=handoff.handoff_hash,
                sender_phase=handoff.sender_phase,
                receiver_phase=handoff.receiver_phase,
                status="ISSUED",
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = InternalHandoffReceipt.create(
                command_id=command.command_id,
                handoff=handoff,
                action="ISSUED",
                decision=None,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_internal_handoff(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                handoff=handoff,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.04:InternalHandoffIssued",
                "ST-04.04:ArtifactIdentityAndLineageValidated",
                "ST-04.04:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    phase_graph=phase_graph,
                    graph=graph,
                    handoff=handoff,
                    receipt=receipt,
                    decision=None,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit_failure(command, error, run, phase_graph, graph, handoff)
            raise

    def decide(self, command: DecideInternalHandoffCommand) -> InternalHandoffReceipt:
        run: Run | None = None
        phase_graph: PhaseGraph | None = None
        graph: PhaseHandoffGraph | None = None
        handoff: InternalHandoff | None = None
        decision: InternalHandoffDecision | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash, InternalHandoffReceipt)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_common(command)
            run = self._repository.load_run(command.run_id)
            self._require_version(command.expected_version, run)
            self._authorize_code(command.actor_id, command.run_id)
            graph, phase_graph = self._load_active_graph(run)
            handoff = self._repository.get_internal_handoff(command.handoff_id)
            if handoff is None or handoff.run_id != run.run_id or handoff.handoff_graph_id != graph.graph_id:
                raise HandoffStateInvalid("The governed internal handoff is unavailable.")
            if self._repository.get_internal_handoff_decision(handoff.handoff_id) is not None:
                raise HandoffStateInvalid("An immutable handoff already has a receiver decision.")
            contract = graph.contract(handoff.contract_id)
            receiver = next(
                (item for item in phase_graph.phases if item.phase_id == handoff.receiver_phase),
                None,
            )
            if (
                receiver is None
                or command.receiver_phase != handoff.receiver_phase
                or command.receiver_authority != receiver.failure_owner
            ):
                raise HandoffAuthorityInvalid("Only the exact governed receiver authority may decide the handoff.")
            self._verify_artifacts(graph, contract, handoff.artifacts)
            decision = InternalHandoffDecision.create(
                handoff=handoff,
                action=command.action,
                receiver_phase=command.receiver_phase,
                receiver_authority=command.receiver_authority,
                authority_identity=command.actor_id,
                reason_code=command.reason_code,
                reason=command.reason,
            )
            event_id = self._ids.new_id("event")
            event_type = (
                "InternalHandoffAccepted"
                if command.action is InternalHandoffDecisionAction.ACCEPTED
                else "InternalHandoffRejected"
            )
            final_run, event = run.record_internal_handoff_event(
                event_type=event_type,
                handoff_graph_ref=graph.graph_id,
                handoff_ref=handoff.handoff_id,
                handoff_hash=handoff.handoff_hash,
                sender_phase=handoff.sender_phase,
                receiver_phase=handoff.receiver_phase,
                status=command.action.value,
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = InternalHandoffReceipt.create(
                command_id=command.command_id,
                handoff=handoff,
                action=command.action.value,
                decision=decision,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_internal_handoff_decision(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                handoff=handoff,
                decision=decision,
                receipt=receipt,
            )
            for event_name in (
                f"ST-04.04:InternalHandoff{command.action.value.title()}",
                "ST-04.04:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    phase_graph=phase_graph,
                    graph=graph,
                    handoff=handoff,
                    receipt=receipt,
                    decision=decision,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit_failure(command, error, run, phase_graph, graph, handoff, decision)
            raise

    def get_active(self, run_id: str) -> PhaseHandoffGraph:
        run = self._repository.load_run(run_id)
        graph, _ = self._load_active_graph(run)
        return graph

    def get_historical(self, graph_id: str) -> PhaseHandoffGraph:
        graph = self._repository.get_phase_handoff_graph(graph_id)
        if graph is None:
            raise KeyError(graph_id)
        phase_graph = self._repository.get_phase_graph(graph.phase_graph_id)
        if phase_graph is None:
            raise KeyError(graph.phase_graph_id)
        graph.validate(phase_graph)
        return graph

    def _load_phase_parent(self, run: Run) -> PhaseGraph:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.phase_graph_ref
            or run.phase_handoff_ref is not None
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_invalidation_ref is not None
            or run.artifact_set_invalidation_ref is not None
            or run.constitutional_validation_invalidation_ref is not None
            or run.capability_ownership_invalidation_ref is not None
            or run.responsibility_module_invalidation_ref is not None
            or run.phase_graph_invalidation_ref is not None
            or run.phase_handoff_invalidation_ref is not None
            or self._repository.is_phase_graph_invalidated(run.phase_graph_ref)
        ):
            raise HandoffCommandRejected("Internal handoff compilation requires the exact active ST-04.03 parent.")
        phase_graph = self._repository.get_phase_graph(run.phase_graph_ref)
        phase_receipts = self._repository.phase_graph_receipts(run.run_id)
        if phase_graph is None or len(phase_receipts) != 1:
            raise HandoffCommandRejected("Phase Graph or its receipt is unavailable.")
        module_graph = self._repository.get_responsibility_module_graph(phase_graph.module_graph_id)
        if module_graph is None:
            raise HandoffCommandRejected("Phase Graph module lineage is unavailable.")
        phase_graph.validate(module_graph)
        phase_receipts[0].validate(phase_graph, module_graph)
        if (
            phase_graph.run_id != run.run_id
            or phase_graph.graph_hash != run.phase_graph_hash
            or phase_receipts[0].stream_version != run.stream_version
        ):
            raise HandoffCommandRejected("The active Phase Graph lineage or receipt has drifted.")
        return phase_graph

    def _load_active_graph(self, run: Run) -> tuple[PhaseHandoffGraph, PhaseGraph]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.phase_handoff_ref
            or not run.phase_graph_ref
            or run.boundary_invalidation_ref is not None
            or run.phase_graph_invalidation_ref is not None
            or run.phase_handoff_invalidation_ref is not None
            or self._repository.is_phase_handoff_invalidated(run.phase_handoff_ref)
        ):
            raise HandoffInvalidatedError("No active internal handoff graph is available.")
        graph = self._repository.get_phase_handoff_graph(run.phase_handoff_ref)
        phase_graph = self._repository.get_phase_graph(run.phase_graph_ref)
        if (
            graph is None
            or phase_graph is None
            or graph.graph_hash != run.phase_handoff_hash
            or graph.phase_graph_id != phase_graph.graph_id
            or self._repository.is_phase_graph_invalidated(phase_graph.graph_id)
        ):
            raise HandoffInvalidatedError("The internal handoff graph is unavailable or hash-drifted.")
        graph.validate(phase_graph)
        return graph, phase_graph

    def _verify_artifacts(
        self,
        graph: PhaseHandoffGraph,
        contract: PhaseHandoffContract,
        artifacts: tuple[GovernedHandoffArtifact, ...],
    ) -> None:
        if tuple(sorted(item.field for item in artifacts)) != tuple(
            sorted(item.field for item in contract.required_fields)
        ):
            raise HandoffContractInvalid("Required handoff artifacts are missing or undeclared.")
        by_field = {item.field: item for item in artifacts}
        if len(by_field) != len(artifacts):
            raise HandoffContractInvalid("Handoff artifact fields must be unique.")
        boundary = self._repository.get_atomic_boundary(graph.boundary_ref)
        boundary_artifact = by_field.get("frozen_atomic_boundary_ref")
        if (
            boundary is None
            or boundary_artifact is None
            or self._repository.is_boundary_invalidated(boundary.boundary_id)
            or boundary_artifact.artifact_id != boundary.boundary_id
            or boundary_artifact.artifact_hash != boundary.content_hash
            or boundary_artifact.version != boundary.version
        ):
            raise HandoffLineageInvalid("The frozen boundary artifact is missing, stale, or altered.")
        receipt_artifact = by_field.get("boundary_validation_receipt_ref")
        receipt = (
            self._repository.get_atomicity_receipt(receipt_artifact.artifact_id)
            if receipt_artifact is not None
            else None
        )
        if (
            receipt is None
            or receipt_artifact is None
            or receipt.receipt_hash != receipt_artifact.artifact_hash
            or receipt.decision_status != "APPROVED"
            or receipt.boundary_ref != graph.boundary_ref
            or receipt.ratification_ref != graph.ratification_ref
            or receipt_artifact.version != contract.version
        ):
            raise HandoffLineageInvalid("The boundary validation receipt is missing, stale, or altered.")
        for artifact in artifacts:
            artifact.__post_init__()
            if artifact.lineage_refs != graph.lineage_refs:
                raise HandoffLineageInvalid("Handoff artifact lineage does not match the active graph.")

    def _load_input(
        self,
        command: CompilePhaseHandoffsCommand,
        phase_graph: PhaseGraph,
    ) -> tuple[tuple[PhaseContextContract, ...], tuple[PhaseHandoffContract, ...]]:
        path = self._verified_file(command.handoff_input_path, command.handoff_input_sha256)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise HandoffInputInvalid("Handoff input is not canonical UTF-8 JSON.") from error
        root_keys = {
            "schema_version", "scope", "source_contract", "target_profile_ref",
            "implicit_context_fields_allowed", "downstream_rewrite_allowed",
            "contexts", "handoffs", "external_product_handoffs",
            "production_eligible", "certified",
        }
        if (
            not isinstance(value, dict)
            or set(value) != root_keys
            or value["schema_version"] != PHASE_HANDOFF_INPUT_SCHEMA
            or value["scope"] != PHASE_HANDOFF_SCOPE
            or value["source_contract"] != PHASE_GRAPH_CONTRACT
            or value["target_profile_ref"] != phase_graph.target_profile_ref
            or value["implicit_context_fields_allowed"] is not False
            or value["downstream_rewrite_allowed"] is not False
            or value["external_product_handoffs"] != []
            or value["production_eligible"] is not False
            or value["certified"] is not False
            or not isinstance(value["contexts"], list)
            or not isinstance(value["handoffs"], list)
        ):
            raise HandoffInputInvalid("Handoff input root contract is incomplete or broadened.")
        contexts = tuple(
            sorted((self._parse_context(item) for item in value["contexts"]), key=lambda item: item.phase_ref)
        )
        contracts = tuple(
            sorted((self._parse_contract(item) for item in value["handoffs"]), key=lambda item: item.contract_id)
        )
        return contexts, contracts

    @staticmethod
    def _parse_context(raw: object) -> PhaseContextContract:
        keys = {
            "context_id", "phase_ref", "included_fields", "excluded_fields",
            "conditional_loads", "unload_behavior", "downstream_exposure",
        }
        field_keys = {"field", "owner", "authority", "mutability"}
        if not isinstance(raw, dict) or set(raw) != keys:
            raise HandoffInputInvalid("A context declaration has unknown or missing fields.")
        for key in ("included_fields", "excluded_fields", "conditional_loads", "downstream_exposure"):
            if not isinstance(raw[key], list):
                raise HandoffInputInvalid("Context list fields must be explicit lists.")
        fields: list[ContextFieldDeclaration] = []
        for item in raw["included_fields"]:
            if not isinstance(item, dict) or set(item) != field_keys:
                raise HandoffInputInvalid("A context field declaration is incomplete.")
            fields.append(ContextFieldDeclaration(**{key: str(item[key]) for key in field_keys}))
        return PhaseContextContract(
            context_id=str(raw["context_id"]),
            phase_ref=str(raw["phase_ref"]),
            included_fields=tuple(sorted(fields, key=lambda item: item.field)),
            excluded_fields=tuple(str(item) for item in raw["excluded_fields"]),
            conditional_loads=tuple(str(item) for item in raw["conditional_loads"]),
            unload_behavior=str(raw["unload_behavior"]),
            downstream_exposure=tuple(str(item) for item in raw["downstream_exposure"]),
        )

    @staticmethod
    def _parse_contract(raw: object) -> PhaseHandoffContract:
        keys = {
            "contract_id", "version", "producer_phase", "consumer_phases",
            "required_fields", "optional_fields", "provenance_required",
            "authority", "validation", "compatibility", "mutability",
            "downstream_rewrite", "invalidation",
        }
        field_keys = {"field", "owner"}
        if not isinstance(raw, dict) or set(raw) != keys:
            raise HandoffInputInvalid("A handoff declaration has unknown or missing fields.")
        for key in ("consumer_phases", "required_fields", "optional_fields", "validation"):
            if not isinstance(raw[key], list):
                raise HandoffInputInvalid("Handoff list fields must be explicit lists.")
        def fields(name: str) -> tuple[HandoffFieldDeclaration, ...]:
            result: list[HandoffFieldDeclaration] = []
            for item in raw[name]:
                if not isinstance(item, dict) or set(item) != field_keys:
                    raise HandoffInputInvalid("A handoff field declaration is incomplete.")
                result.append(HandoffFieldDeclaration(field=str(item["field"]), owner=str(item["owner"])))
            return tuple(sorted(result, key=lambda item: item.field))
        return PhaseHandoffContract(
            contract_id=str(raw["contract_id"]),
            version=str(raw["version"]),
            producer_phase=str(raw["producer_phase"]),
            consumer_phases=tuple(str(item) for item in raw["consumer_phases"]),
            required_fields=fields("required_fields"),
            optional_fields=fields("optional_fields"),
            provenance_required=raw["provenance_required"] is True,
            authority=str(raw["authority"]),
            validation=tuple(str(item) for item in raw["validation"]),
            compatibility=str(raw["compatibility"]),
            mutability=str(raw["mutability"]),
            downstream_rewrite=str(raw["downstream_rewrite"]),
            invalidation=str(raw["invalidation"]),
        )

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
            observed = sha256(path.read_bytes()).hexdigest()
        except (ValueError, OSError) as error:
            raise HandoffInputInvalid("Governed handoff input is unavailable or escapes the repository.") from error
        if observed != expected_sha256:
            raise HandoffInputInvalid(
                "Governed handoff input hash does not match.",
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    def _authorize_code(self, actor_id: str, run_id: str) -> None:
        actor = self._authority.authorize(
            actor_id=actor_id,
            action=Action.TRANSITION_RUN,
            resource_id=run_id,
            now=self._clock.now(),
        )
        if actor.kind is not ActorKind.CODE:
            raise HarnessIRAuthorityRejected("Only deterministic Builder code may govern internal handoffs.")

    @staticmethod
    def _validate_common(command: object) -> None:
        values = (
            getattr(command, "command_id", ""), getattr(command, "run_id", ""),
            getattr(command, "actor_id", ""), getattr(command, "correlation_id", ""),
            getattr(command, "causation_id", ""),
        )
        if not all(str(value).strip() for value in values) or getattr(command, "expected_version", 0) < 1:
            raise HandoffInputInvalid("Handoff command identity is incomplete.")

    @staticmethod
    def _require_version(expected_version: int, run: Run) -> None:
        if expected_version != run.stream_version:
            raise ConcurrencyConflict(
                "Expected stream version does not match authoritative state.",
                expected_version=expected_version,
                current_version=run.stream_version,
            )

    def _duplicate(self, command_id: str, payload_hash: str, result_type: type):
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash or not isinstance(record.result, result_type):
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload or result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(self, command: object, receipt: object) -> None:
        run = self._repository.load_run(getattr(command, "run_id"))
        graph, phase_graph = self._load_active_graph(run)
        handoff_id = getattr(receipt, "handoff_id", "")
        handoff = self._repository.get_internal_handoff(handoff_id) if handoff_id else None
        decision = self._repository.get_internal_handoff_decision(handoff_id) if handoff_id else None
        self._emit(
            event_name="ST-04.04:CommandReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            phase_graph=phase_graph,
            graph=graph,
            handoff=handoff,
            receipt=receipt,
            decision=decision,
            failure_context={},
        )

    def _emit_failure(
        self,
        command: object,
        error: Exception,
        run: Run | None,
        phase_graph: PhaseGraph | None,
        graph: PhaseHandoffGraph | None,
        handoff: InternalHandoff | None = None,
        decision: InternalHandoffDecision | None = None,
    ) -> None:
        self._emit(
            event_name="ST-04.04:OutcomeRejected",
            outcome="FAIL",
            command=command,
            run=run,
            phase_graph=phase_graph,
            graph=graph,
            handoff=handoff,
            receipt=None,
            decision=decision,
            failure_context={
                "code": str(getattr(error, "code", type(error).__name__)),
                "message": str(error),
                **dict(getattr(error, "context", {})),
            },
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: object,
        run: Run | None,
        phase_graph: PhaseGraph | None,
        graph: PhaseHandoffGraph | None,
        handoff: InternalHandoff | None,
        receipt: object | None,
        decision: InternalHandoffDecision | None,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=getattr(command, "run_id", "unassigned"),
                story_id=self.STORY_ID,
                artifact_identity=(handoff.handoff_id if handoff else graph.graph_id if graph else "unassigned"),
                authority_identity=getattr(command, "actor_id", "unassigned"),
                version=self.CONTRACT_VERSION,
                provenance=(handoff.handoff_hash if handoff else graph.graph_hash if graph else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=getattr(command, "correlation_id", "unassigned"),
                causation_id=getattr(command, "causation_id", "unassigned"),
                command_id=getattr(command, "command_id", "unassigned"),
                target_id=(profile.target_id if profile else "unassigned"),
                category_id=(profile.category_id if profile else "unassigned"),
                profile_id=(profile.profile_id if profile else "unassigned"),
                stream_version=(run.stream_version if run else getattr(command, "expected_version", 0)),
                source_lock_id=(graph.source_lock_ref if graph else phase_graph.source_lock_ref if phase_graph else "unassigned"),
                boundary_id=(graph.boundary_ref if graph else phase_graph.boundary_ref if phase_graph else "unassigned"),
                model_id=(graph.model_ref if graph else phase_graph.model_ref if phase_graph else "unassigned"),
                decision_receipt_id=getattr(receipt, "receipt_id", "unassigned") if receipt else "unassigned",
                decision_receipt_hash=getattr(receipt, "receipt_hash", "unassigned") if receipt else "unassigned",
                harness_ir_id=(graph.ir_id if graph else phase_graph.ir_id if phase_graph else "unassigned"),
                harness_ir_hash=(graph.ir_hash if graph else phase_graph.ir_hash if phase_graph else "unassigned"),
                artifact_set_id=(graph.artifact_set_id if graph else phase_graph.artifact_set_id if phase_graph else "unassigned"),
                constitutional_report_id=(graph.constitutional_report_id if graph else phase_graph.constitutional_report_id if phase_graph else "unassigned"),
                constitutional_report_hash=(graph.constitutional_report_hash if graph else phase_graph.constitutional_report_hash if phase_graph else "unassigned"),
                capability_graph_id=(graph.capability_graph_id if graph else phase_graph.capability_graph_id if phase_graph else "unassigned"),
                capability_graph_hash=(graph.capability_graph_hash if graph else phase_graph.capability_graph_hash if phase_graph else "unassigned"),
                module_graph_id=(graph.module_graph_id if graph else phase_graph.module_graph_id if phase_graph else "unassigned"),
                module_graph_hash=(graph.module_graph_hash if graph else phase_graph.module_graph_hash if phase_graph else "unassigned"),
                phase_graph_id=(phase_graph.graph_id if phase_graph else "unassigned"),
                phase_graph_hash=(phase_graph.graph_hash if phase_graph else "unassigned"),
                phase_count=(len(phase_graph.phases) if phase_graph else 0),
                context_graph_id=(graph.context_graph.context_graph_id if graph else "unassigned"),
                context_graph_hash=(graph.context_graph.context_graph_hash if graph else "unassigned"),
                handoff_graph_id=(graph.graph_id if graph else "unassigned"),
                handoff_graph_hash=(graph.graph_hash if graph else "unassigned"),
                handoff_receipt_id=getattr(receipt, "receipt_id", "unassigned") if receipt else "unassigned",
                handoff_receipt_hash=getattr(receipt, "receipt_hash", "unassigned") if receipt else "unassigned",
                handoff_context_count=(len(graph.context_graph.contexts) if graph else 0),
                handoff_contract_count=(len(graph.contracts) if graph else 0),
                internal_handoff_id=(handoff.handoff_id if handoff else "unassigned"),
                internal_handoff_hash=(handoff.handoff_hash if handoff else "unassigned"),
                handoff_sender_phase=(handoff.sender_phase if handoff else "unassigned"),
                handoff_sender_module=(handoff.sender_module if handoff else "unassigned"),
                handoff_receiver_phase=(handoff.receiver_phase if handoff else "unassigned"),
                handoff_receiver_module=(handoff.receiver_module if handoff else "unassigned"),
                handoff_status=(decision.action.value if decision else handoff.status if handoff else "unassigned"),
                handoff_decision_id=(decision.decision_id if decision else "unassigned"),
                handoff_decision_hash=(decision.decision_hash if decision else "unassigned"),
            )
        )


def _command_hash(command: object) -> str:
    payload = _canonical_value(asdict(command))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{sha256(encoded).hexdigest()}"


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _canonical_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
