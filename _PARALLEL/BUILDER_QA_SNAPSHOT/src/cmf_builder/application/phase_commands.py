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
    PhaseGraphRepository,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.phase_graph import (
    PHASE_GRAPH_INPUT_PATH,
    PHASE_GRAPH_INPUT_SCHEMA,
    PHASE_GRAPH_INPUT_SHA256,
    PHASE_GRAPH_SCHEMA_ID,
    PHASE_GRAPH_SCHEMA_VERSION,
    PHASE_GRAPH_SCOPE,
    RESPONSIBILITY_MODULE_CONTRACT,
    PhaseGraph,
    PhaseGraphInputInvalid,
    PhaseGraphInvalidatedError,
    PhaseGraphReceipt,
    PhaseNode,
)
from cmf_builder.domain.responsibility_modules import ResponsibilityModuleGraph
from cmf_builder.domain.run import LifecycleState, Run


class PhaseCommandRejected(Exception):
    code = "PhaseCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class CompilePhaseGraphCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    phase_input_path: str = PHASE_GRAPH_INPUT_PATH
    phase_input_sha256: str = PHASE_GRAPH_INPUT_SHA256


class PhaseGraphCommandService:
    STORY_ID = "ST-04.03"
    CONTRACT_VERSION = f"{PHASE_GRAPH_SCHEMA_ID}@{PHASE_GRAPH_SCHEMA_VERSION}"

    def __init__(
        self,
        *,
        root: Path,
        repository: PhaseGraphRepository,
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

    def compile(self, command: CompilePhaseGraphCommand) -> PhaseGraphReceipt:
        run: Run | None = None
        module_graph: ResponsibilityModuleGraph | None = None
        graph: PhaseGraph | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
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
                    "Only deterministic Builder code may compile the Phase Graph.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            module_graph = self._load_active_parent(run)
            phases = self._load_phases(command, module_graph)
            graph = PhaseGraph.create(
                module_graph=module_graph,
                phases=phases,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_phase_graph(
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                module_graph_ref=module_graph.graph_id,
                harness_ir_ref=module_graph.ir_id,
                phase_count=len(graph.phases),
                module_count=len(graph.module_refs),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = PhaseGraphReceipt.create(
                command_id=command.command_id,
                graph=graph,
                module_graph=module_graph,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_phase_graph(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                graph=graph,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.03:PhaseGraphCompiled",
                "ST-04.03:TopologyValidated",
                "ST-04.03:RunnableStateDerived",
                "ST-04.03:ParallelismValidated",
                "ST-04.03:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    module_graph=module_graph,
                    graph=graph,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="ST-04.03:OutcomeRejected",
                outcome="FAIL",
                command=command,
                run=run,
                module_graph=module_graph,
                graph=graph,
                receipt=None,
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> PhaseGraph:
        run = self._repository.load_run(run_id)
        if (
            not run.phase_graph_ref
            or run.phase_graph_invalidation_ref is not None
            or self._repository.is_phase_graph_invalidated(run.phase_graph_ref)
        ):
            raise PhaseGraphInvalidatedError(
                "No active Phase Graph is available.", run_id=run_id
            )
        graph = self._repository.get_phase_graph(run.phase_graph_ref)
        module_graph = self._repository.get_responsibility_module_graph(
            graph.module_graph_id if graph else ""
        )
        if (
            graph is None
            or module_graph is None
            or graph.graph_hash != run.phase_graph_hash
        ):
            raise PhaseGraphInvalidatedError(
                "The active Phase Graph is unavailable or hash-drifted."
            )
        graph.validate(module_graph)
        return graph

    def get_historical(self, graph_id: str) -> PhaseGraph:
        graph = self._repository.get_phase_graph(graph_id)
        if graph is None:
            raise KeyError(graph_id)
        module_graph = self._repository.get_responsibility_module_graph(
            graph.module_graph_id
        )
        if module_graph is None:
            raise KeyError(graph.module_graph_id)
        graph.validate(module_graph)
        return graph

    def _load_active_parent(self, run: Run) -> ResponsibilityModuleGraph:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.harness_ir_ref
            or not run.responsibility_module_ref
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_invalidation_ref is not None
            or run.artifact_set_invalidation_ref is not None
            or run.constitutional_validation_invalidation_ref is not None
            or run.capability_ownership_invalidation_ref is not None
            or run.responsibility_module_invalidation_ref is not None
            or run.phase_graph_ref is not None
            or run.phase_graph_invalidation_ref is not None
            or self._repository.is_responsibility_module_invalidated(
                run.responsibility_module_ref
            )
        ):
            raise PhaseCommandRejected(
                "Phase compilation requires the exact active ST-04.02 parent.",
                lifecycle_state=run.lifecycle_state.value,
            )
        graph = self._repository.get_responsibility_module_graph(
            run.responsibility_module_ref
        )
        receipts = self._repository.responsibility_module_receipts(run.run_id)
        if graph is None or len(receipts) != 1:
            raise PhaseCommandRejected("Module graph or its receipt is unavailable.")
        capability_graph = self._repository.get_capability_ownership_graph(
            graph.capability_graph_id
        )
        if capability_graph is None:
            raise PhaseCommandRejected("Capability lineage is unavailable.")
        receipt = receipts[0]
        graph.validate(capability_graph)
        receipt.validate(graph, capability_graph)
        if (
            graph.run_id != run.run_id
            or graph.ir_id != run.harness_ir_ref
            or graph.graph_hash != run.responsibility_module_hash
            or receipt.graph_id != graph.graph_id
            or receipt.stream_version != run.stream_version
        ):
            raise PhaseCommandRejected(
                "The active module lineage or receipt identity has drifted."
            )
        return graph

    def _load_phases(
        self,
        command: CompilePhaseGraphCommand,
        module_graph: ResponsibilityModuleGraph,
    ) -> tuple[PhaseNode, ...]:
        path = self._verified_file(command.phase_input_path, command.phase_input_sha256)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PhaseGraphInputInvalid(
                "Phase input is not canonical UTF-8 JSON."
            ) from error
        root_keys = {
            "schema_version",
            "scope",
            "source_contract",
            "target_profile_ref",
            "implicit_phases_allowed",
            "default_parallelism_allowed",
            "phases",
            "production_eligible",
            "certified",
        }
        if (
            not isinstance(value, dict)
            or set(value) != root_keys
            or value["schema_version"] != PHASE_GRAPH_INPUT_SCHEMA
            or value["scope"] != PHASE_GRAPH_SCOPE
            or value["source_contract"] != RESPONSIBILITY_MODULE_CONTRACT
            or value["target_profile_ref"] != module_graph.target_profile_ref
            or value["implicit_phases_allowed"] is not False
            or value["default_parallelism_allowed"] is not False
            or value["production_eligible"] is not False
            or value["certified"] is not False
            or not isinstance(value["phases"], list)
        ):
            raise PhaseGraphInputInvalid(
                "Phase input root contract is incomplete or broadened."
            )
        phase_keys = {
            "phase_id",
            "responsibility",
            "module_refs",
            "dependencies",
            "parallel_with",
            "entry_conditions",
            "exit_evidence",
            "failure_owner",
            "required_gates",
            "execution_kind",
        }
        list_keys = {
            "module_refs",
            "dependencies",
            "parallel_with",
            "entry_conditions",
            "exit_evidence",
            "required_gates",
        }
        phases: list[PhaseNode] = []
        for raw in value["phases"]:
            if (
                not isinstance(raw, dict)
                or set(raw) != phase_keys
                or any(not isinstance(raw[key], list) for key in list_keys)
            ):
                raise PhaseGraphInputInvalid(
                    "A phase has unknown, missing, or non-list fields."
                )
            phases.append(
                PhaseNode(
                    phase_id=str(raw["phase_id"]),
                    responsibility=str(raw["responsibility"]),
                    module_refs=tuple(str(item) for item in raw["module_refs"]),
                    dependencies=tuple(str(item) for item in raw["dependencies"]),
                    parallel_with=tuple(str(item) for item in raw["parallel_with"]),
                    entry_conditions=tuple(
                        str(item) for item in raw["entry_conditions"]
                    ),
                    exit_evidence=tuple(str(item) for item in raw["exit_evidence"]),
                    failure_owner=str(raw["failure_owner"]),
                    required_gates=tuple(str(item) for item in raw["required_gates"]),
                    execution_kind=str(raw["execution_kind"]),
                )
            )
        return tuple(sorted(phases, key=lambda phase: phase.phase_id))

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        if not relative_path.strip() or not expected_sha256.strip():
            raise PhaseGraphInputInvalid("A governed file pin is incomplete.")
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise PhaseGraphInputInvalid(
                "Governed input path escapes the repository root."
            ) from error
        try:
            observed = sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            raise PhaseGraphInputInvalid(
                "Governed phase input is unavailable.", path=relative_path
            ) from error
        if observed != expected_sha256:
            raise PhaseGraphInputInvalid(
                "Governed phase input hash does not match.",
                path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    @staticmethod
    def _validate_command(command: CompilePhaseGraphCommand) -> None:
        if (
            not all(
                value.strip()
                for value in (
                    command.command_id,
                    command.run_id,
                    command.actor_id,
                    command.correlation_id,
                    command.causation_id,
                )
            )
            or command.expected_version < 1
            or command.phase_input_path != PHASE_GRAPH_INPUT_PATH
            or command.phase_input_sha256 != PHASE_GRAPH_INPUT_SHA256
        ):
            raise PhaseGraphInputInvalid(
                "Phase command identity or governed input pin is invalid."
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> PhaseGraphReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, PhaseGraphReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self, command: CompilePhaseGraphCommand, receipt: PhaseGraphReceipt
    ) -> None:
        run = self._repository.load_run(command.run_id)
        graph = self._repository.get_phase_graph(receipt.graph_id)
        module_graph = self._repository.get_responsibility_module_graph(
            graph.module_graph_id if graph else ""
        )
        if graph is None or module_graph is None:
            raise PhaseCommandRejected("Replay phase lineage is unavailable.")
        self._emit(
            event_name="ST-04.03:CompilationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            module_graph=module_graph,
            graph=graph,
            receipt=receipt,
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompilePhaseGraphCommand,
        run: Run | None,
        module_graph: ResponsibilityModuleGraph | None,
        graph: PhaseGraph | None,
        receipt: PhaseGraphReceipt | None,
        failure_context: dict[str, object],
    ) -> None:
        profile = run.target_profile if run else None
        self._observations.emit(
            Observation(
                event_name=event_name,
                run_id=command.run_id,
                story_id=self.STORY_ID,
                artifact_identity=(graph.graph_id if graph else "unassigned"),
                authority_identity=command.actor_id,
                version=self.CONTRACT_VERSION,
                provenance=(graph.graph_hash if graph else "unassigned"),
                outcome=outcome,
                failure_context=failure_context,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                command_id=command.command_id,
                target_id=(profile.target_id if profile else "unassigned"),
                category_id=(profile.category_id if profile else "unassigned"),
                profile_id=(profile.profile_id if profile else "unassigned"),
                stream_version=(run.stream_version if run else command.expected_version),
                source_lock_id=(module_graph.source_lock_ref if module_graph else "unassigned"),
                boundary_id=(module_graph.boundary_ref if module_graph else "unassigned"),
                model_id=(module_graph.model_ref if module_graph else "unassigned"),
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                harness_ir_id=(module_graph.ir_id if module_graph else "unassigned"),
                harness_ir_hash=(module_graph.ir_hash if module_graph else "unassigned"),
                artifact_set_id=(module_graph.artifact_set_id if module_graph else "unassigned"),
                constitutional_report_id=(module_graph.constitutional_report_id if module_graph else "unassigned"),
                constitutional_report_hash=(module_graph.constitutional_report_hash if module_graph else "unassigned"),
                constitutional_receipt_id=(module_graph.constitutional_receipt_id if module_graph else "unassigned"),
                constitutional_receipt_hash=(module_graph.constitutional_receipt_hash if module_graph else "unassigned"),
                constitutional_precedence_disposition=("PASS_HIGHER_AUTHORITY_PRESERVED" if module_graph else "unassigned"),
                capability_graph_id=(module_graph.capability_graph_id if module_graph else "unassigned"),
                capability_graph_hash=(module_graph.capability_graph_hash if module_graph else "unassigned"),
                capability_count=(len(module_graph.capability_ownerships) if module_graph else 0),
                module_graph_id=(module_graph.graph_id if module_graph else "unassigned"),
                module_graph_hash=(module_graph.graph_hash if module_graph else "unassigned"),
                module_count=(len(module_graph.modules) if module_graph else 0),
                module_capability_coverage_count=(len(module_graph.capability_ids) if module_graph else 0),
                module_dependency_count=(module_graph.dependency_count if module_graph else 0),
                phase_graph_id=(graph.graph_id if graph else "unassigned"),
                phase_graph_hash=(graph.graph_hash if graph else "unassigned"),
                phase_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                phase_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                phase_count=(len(graph.phases) if graph else 0),
                phase_module_coverage_count=(len(graph.module_refs) if graph else 0),
                phase_dependency_count=(graph.dependency_count if graph else 0),
                phase_gate_count=(graph.gate_count if graph else 0),
                phase_initially_runnable_count=(len(graph.execution_plan.initially_runnable) if graph else 0),
                phase_blocked_count=(len(graph.execution_plan.blocked_by) if graph else 0),
                phase_parallel_pair_count=(len(graph.execution_plan.parallel_pairs) if graph else 0),
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
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_canonical_value(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value
