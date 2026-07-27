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
    ResponsibilityModuleRepository,
)
from cmf_builder.domain.capability_ownership import (
    EXPECTED_CAPABILITIES,
    CapabilityOwnerKind,
    CapabilityOwnershipGraph,
)
from cmf_builder.domain.harness_ir import HarnessIRAuthorityRejected
from cmf_builder.domain.responsibility_modules import (
    CAPABILITY_OWNERSHIP_CONTRACT,
    MODULE_COMPILATION_INPUT_PATH,
    MODULE_COMPILATION_INPUT_SCHEMA,
    MODULE_COMPILATION_INPUT_SHA256,
    RESPONSIBILITY_MODULE_SCHEMA_ID,
    RESPONSIBILITY_MODULE_SCHEMA_VERSION,
    RESPONSIBILITY_MODULE_SCOPE,
    ModuleBoundaryInvalid,
    ModuleCoverageInvalid,
    ModuleInputInvalid,
    ModulePublicContract,
    ModuleTestSeam,
    ResponsibilityModule,
    ResponsibilityModuleGraph,
    ResponsibilityModuleInvalidatedError,
    ResponsibilityModuleReceipt,
)
from cmf_builder.domain.run import LifecycleState, Run


class ModuleCommandRejected(Exception):
    code = "ModuleCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class CompileResponsibilityModulesCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    module_input_path: str = MODULE_COMPILATION_INPUT_PATH
    module_input_sha256: str = MODULE_COMPILATION_INPUT_SHA256


class ResponsibilityModuleCommandService:
    STORY_ID = "ST-04.02"
    CONTRACT_VERSION = (
        f"{RESPONSIBILITY_MODULE_SCHEMA_ID}@{RESPONSIBILITY_MODULE_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: ResponsibilityModuleRepository,
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
        self, command: CompileResponsibilityModulesCommand
    ) -> ResponsibilityModuleReceipt:
        run: Run | None = None
        capability_graph: CapabilityOwnershipGraph | None = None
        graph: ResponsibilityModuleGraph | None = None
        try:
            payload_hash = _command_hash(command)
            duplicate = self._duplicate(command.command_id, payload_hash)
            if duplicate is not None:
                self._emit_replay(command, duplicate)
                return duplicate
            self._validate_command(command)
            run = self._repository.load_run(command.run_id)
            if run.stream_version != command.expected_version:
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
                    "Only deterministic Builder code may compile responsibility modules.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            capability_graph = self._load_active_parent(run)
            modules = self._load_modules(command, capability_graph)
            graph = ResponsibilityModuleGraph.create(
                capability_graph=capability_graph,
                modules=modules,
                authority_identity=command.actor_id,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_responsibility_modules(
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                capability_graph_ref=capability_graph.graph_id,
                harness_ir_ref=capability_graph.ir_id,
                module_count=len(graph.modules),
                capability_count=len(graph.capability_ids),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = ResponsibilityModuleReceipt.create(
                command_id=command.command_id,
                graph=graph,
                capability_graph=capability_graph,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_responsibility_modules(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                graph=graph,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.02:ResponsibilityModulesCompiled",
                "ST-04.02:CapabilityPartitionValidated",
                "ST-04.02:ModuleContractsValidated",
                "ST-04.02:TestSeamsValidated",
                "ST-04.02:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    capability_graph=capability_graph,
                    graph=graph,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="ST-04.02:OutcomeRejected",
                outcome="FAIL",
                command=command,
                run=run,
                capability_graph=capability_graph,
                graph=graph,
                receipt=None,
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> ResponsibilityModuleGraph:
        run = self._repository.load_run(run_id)
        if (
            not run.responsibility_module_ref
            or run.responsibility_module_invalidation_ref is not None
            or self._repository.is_responsibility_module_invalidated(
                run.responsibility_module_ref
            )
        ):
            raise ResponsibilityModuleInvalidatedError(
                "No active responsibility module graph is available.", run_id=run_id
            )
        graph = self._repository.get_responsibility_module_graph(
            run.responsibility_module_ref
        )
        capability_graph = self._repository.get_capability_ownership_graph(
            graph.capability_graph_id if graph else ""
        )
        if (
            graph is None
            or capability_graph is None
            or graph.graph_hash != run.responsibility_module_hash
        ):
            raise ResponsibilityModuleInvalidatedError(
                "The active module graph is unavailable or hash-drifted."
            )
        graph.validate(capability_graph)
        return graph

    def get_historical(self, graph_id: str) -> ResponsibilityModuleGraph:
        graph = self._repository.get_responsibility_module_graph(graph_id)
        if graph is None:
            raise KeyError(graph_id)
        capability_graph = self._repository.get_capability_ownership_graph(
            graph.capability_graph_id
        )
        if capability_graph is None:
            raise KeyError(graph.capability_graph_id)
        graph.validate(capability_graph)
        return graph

    def _load_active_parent(self, run: Run) -> CapabilityOwnershipGraph:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.harness_ir_ref
            or not run.capability_ownership_ref
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_invalidation_ref is not None
            or run.artifact_set_invalidation_ref is not None
            or run.constitutional_validation_invalidation_ref is not None
            or run.capability_ownership_invalidation_ref is not None
            or run.responsibility_module_ref is not None
            or run.responsibility_module_invalidation_ref is not None
            or self._repository.is_capability_ownership_invalidated(
                run.capability_ownership_ref
            )
        ):
            raise ModuleCommandRejected(
                "Responsibility modules require the exact active ST-04.01 parent.",
                lifecycle_state=run.lifecycle_state.value,
            )
        graph = self._repository.get_capability_ownership_graph(
            run.capability_ownership_ref
        )
        receipts = self._repository.capability_ownership_receipts(run.run_id)
        if graph is None or len(receipts) != 1:
            raise ModuleCommandRejected(
                "Capability graph or its unique receipt is unavailable."
            )
        receipt = receipts[0]
        graph.validate()
        receipt.validate(graph)
        if (
            graph.run_id != run.run_id
            or graph.ir_id != run.harness_ir_ref
            or graph.graph_hash != run.capability_ownership_hash
            or receipt.graph_id != graph.graph_id
            or receipt.stream_version != run.stream_version
        ):
            raise ModuleCommandRejected(
                "The active capability lineage or receipt identity has drifted."
            )
        return graph

    def _load_modules(
        self,
        command: CompileResponsibilityModulesCommand,
        capability_graph: CapabilityOwnershipGraph,
    ) -> tuple[ResponsibilityModule, ...]:
        path = self._verified_file(command.module_input_path, command.module_input_sha256)
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ModuleInputInvalid(
                "Module input is not canonical UTF-8 JSON."
            ) from error
        root_keys = {
            "schema_version",
            "scope",
            "source_contract",
            "target_profile_ref",
            "implicit_modules_allowed",
            "modules",
            "production_eligible",
            "certified",
        }
        if (
            not isinstance(value, dict)
            or set(value) != root_keys
            or value["schema_version"] != MODULE_COMPILATION_INPUT_SCHEMA
            or value["scope"] != RESPONSIBILITY_MODULE_SCOPE
            or value["source_contract"] != CAPABILITY_OWNERSHIP_CONTRACT
            or value["target_profile_ref"] != capability_graph.target_profile_ref
            or value["implicit_modules_allowed"] is not False
            or value["production_eligible"] is not False
            or value["certified"] is not False
            or not isinstance(value["modules"], list)
        ):
            raise ModuleInputInvalid(
                "Module input root contract is incomplete or broadened."
            )
        module_keys = {
            "module_id",
            "responsibility",
            "owned_capabilities",
            "public_contract",
            "invariants",
            "exclusions",
            "dependencies",
            "failure_owner",
            "failure_modes",
            "boundary_rationale",
            "test_seam",
        }
        contract_keys = {"inputs", "outputs", "side_effects"}
        seam_keys = {
            "public_command",
            "expected_fixtures",
            "contract_tests",
            "failure_injections",
            "observable_outputs",
        }
        modules: list[ResponsibilityModule] = []
        for raw in value["modules"]:
            if not isinstance(raw, dict) or set(raw) != module_keys:
                raise ModuleInputInvalid("A module has unknown or missing fields.")
            contract = raw["public_contract"]
            seam = raw["test_seam"]
            sequence_fields = (
                raw["owned_capabilities"],
                raw["invariants"],
                raw["exclusions"],
                raw["dependencies"],
                raw["failure_modes"],
            )
            if (
                not isinstance(contract, dict)
                or set(contract) != contract_keys
                or not isinstance(seam, dict)
                or set(seam) != seam_keys
                or any(not isinstance(item, list) for item in sequence_fields)
                or any(not isinstance(contract[key], list) for key in contract_keys)
                or any(
                    not isinstance(seam[key], list)
                    for key in seam_keys - {"public_command"}
                )
            ):
                raise ModuleInputInvalid(
                    "Module contracts and test seams must use explicit ordered lists."
                )
            modules.append(
                ResponsibilityModule(
                    module_id=str(raw["module_id"]),
                    responsibility=str(raw["responsibility"]),
                    owned_capabilities=tuple(
                        str(item) for item in raw["owned_capabilities"]
                    ),
                    public_contract=ModulePublicContract(
                        inputs=tuple(str(item) for item in contract["inputs"]),
                        outputs=tuple(str(item) for item in contract["outputs"]),
                        side_effects=tuple(
                            str(item) for item in contract["side_effects"]
                        ),
                    ),
                    invariants=tuple(str(item) for item in raw["invariants"]),
                    exclusions=tuple(str(item) for item in raw["exclusions"]),
                    dependencies=tuple(str(item) for item in raw["dependencies"]),
                    failure_owner=str(raw["failure_owner"]),
                    failure_modes=tuple(str(item) for item in raw["failure_modes"]),
                    boundary_rationale=str(raw["boundary_rationale"]),
                    test_seam=ModuleTestSeam(
                        public_command=str(seam["public_command"]),
                        expected_fixtures=tuple(
                            str(item) for item in seam["expected_fixtures"]
                        ),
                        contract_tests=tuple(
                            str(item) for item in seam["contract_tests"]
                        ),
                        failure_injections=tuple(
                            str(item) for item in seam["failure_injections"]
                        ),
                        observable_outputs=tuple(
                            str(item) for item in seam["observable_outputs"]
                        ),
                    ),
                )
            )
        observed = tuple(
            capability for module in modules for capability in module.owned_capabilities
        )
        if (
            len(modules) != 2
            or tuple(sorted(observed)) != EXPECTED_CAPABILITIES
            or len(set(observed)) != len(observed)
        ):
            raise ModuleCoverageInvalid(
                "Every active capability must be assigned exactly once.",
                observed=tuple(sorted(observed)),
            )
        decisions = {item.capability_id: item for item in capability_graph.decisions}
        for module in modules:
            kinds = {decisions[item].owner_kind for item in module.owned_capabilities}
            if len(kinds) != 1 or next(iter(kinds)) is not CapabilityOwnerKind.CODE:
                raise ModuleBoundaryInvalid(
                    "The bounded synthetic module cannot change or mix owner authority.",
                    module_id=module.module_id,
                )
        return tuple(sorted(modules, key=lambda item: item.module_id))

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        if not relative_path.strip() or not expected_sha256.strip():
            raise ModuleInputInvalid("A governed file pin is incomplete.")
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise ModuleInputInvalid(
                "Governed input path escapes the repository root."
            ) from error
        try:
            observed = sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            raise ModuleInputInvalid(
                "Governed module input is unavailable.", path=relative_path
            ) from error
        if observed != expected_sha256:
            raise ModuleInputInvalid(
                "Governed module input hash does not match.",
                path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    @staticmethod
    def _validate_command(command: CompileResponsibilityModulesCommand) -> None:
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
            or command.module_input_path != MODULE_COMPILATION_INPUT_PATH
            or command.module_input_sha256 != MODULE_COMPILATION_INPUT_SHA256
        ):
            raise ModuleInputInvalid(
                "Module command identity or governed input pin is invalid."
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> ResponsibilityModuleReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, ResponsibilityModuleReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileResponsibilityModulesCommand,
        receipt: ResponsibilityModuleReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        graph = self._repository.get_responsibility_module_graph(receipt.graph_id)
        capability_graph = self._repository.get_capability_ownership_graph(
            graph.capability_graph_id if graph else ""
        )
        if graph is None or capability_graph is None:
            raise ModuleCommandRejected("Replay module lineage is unavailable.")
        self._emit(
            event_name="ST-04.02:CompilationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            capability_graph=capability_graph,
            graph=graph,
            receipt=receipt,
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileResponsibilityModulesCommand,
        run: Run | None,
        capability_graph: CapabilityOwnershipGraph | None,
        graph: ResponsibilityModuleGraph | None,
        receipt: ResponsibilityModuleReceipt | None,
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
                source_lock_id=(
                    capability_graph.source_lock_ref
                    if capability_graph
                    else "unassigned"
                ),
                boundary_id=(
                    capability_graph.boundary_ref
                    if capability_graph
                    else "unassigned"
                ),
                model_id=(
                    capability_graph.model_ref if capability_graph else "unassigned"
                ),
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(
                    receipt.receipt_hash if receipt else "unassigned"
                ),
                harness_ir_id=(
                    capability_graph.ir_id if capability_graph else "unassigned"
                ),
                harness_ir_hash=(
                    capability_graph.ir_hash if capability_graph else "unassigned"
                ),
                artifact_set_id=(
                    capability_graph.artifact_set_id
                    if capability_graph
                    else "unassigned"
                ),
                constitutional_report_id=(
                    capability_graph.constitutional_report_id
                    if capability_graph
                    else "unassigned"
                ),
                constitutional_report_hash=(
                    capability_graph.constitutional_report_hash
                    if capability_graph
                    else "unassigned"
                ),
                constitutional_receipt_id=(
                    capability_graph.constitutional_receipt_id
                    if capability_graph
                    else "unassigned"
                ),
                constitutional_receipt_hash=(
                    capability_graph.constitutional_receipt_hash
                    if capability_graph
                    else "unassigned"
                ),
                constitutional_precedence_disposition=(
                    "PASS_HIGHER_AUTHORITY_PRESERVED"
                    if capability_graph
                    else "unassigned"
                ),
                capability_graph_id=(
                    capability_graph.graph_id if capability_graph else "unassigned"
                ),
                capability_graph_hash=(
                    capability_graph.graph_hash if capability_graph else "unassigned"
                ),
                capability_count=(
                    len(capability_graph.decisions) if capability_graph else 0
                ),
                capability_owner_kind_counts=(
                    capability_graph.owner_kind_counts if capability_graph else ()
                ),
                capability_reliability_coverage_count=(
                    len(capability_graph.decisions) if capability_graph else 0
                ),
                capability_cost_coverage_count=(
                    len(capability_graph.decisions) if capability_graph else 0
                ),
                module_graph_id=(graph.graph_id if graph else "unassigned"),
                module_graph_hash=(graph.graph_hash if graph else "unassigned"),
                module_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                module_receipt_hash=(
                    receipt.receipt_hash if receipt else "unassigned"
                ),
                module_count=(len(graph.modules) if graph else 0),
                module_capability_coverage_count=(
                    len(graph.capability_ids) if graph else 0
                ),
                module_dependency_count=(graph.dependency_count if graph else 0),
                module_contract_coverage_count=(
                    len(graph.modules) if graph else 0
                ),
                module_test_seam_coverage_count=(
                    len(graph.modules) if graph else 0
                ),
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
