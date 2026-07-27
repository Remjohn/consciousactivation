from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
from pathlib import Path

from cmf_builder.application.authority import Action, ActorKind, AuthorityService
from cmf_builder.application.ports import (
    CapabilityOwnershipRepository,
    Clock,
    CommandRecord,
    ConcurrencyConflict,
    IdProvider,
    IdempotencyPayloadMismatch,
    Observation,
    ObservationSink,
)
from cmf_builder.domain.capability_ownership import (
    CAPABILITY_OWNERSHIP_INPUT_PATH,
    CAPABILITY_OWNERSHIP_INPUT_SCHEMA,
    CAPABILITY_OWNERSHIP_INPUT_SHA256,
    CAPABILITY_OWNERSHIP_SCOPE,
    CAPABILITY_OWNERSHIP_SCHEMA_ID,
    CAPABILITY_OWNERSHIP_SCHEMA_VERSION,
    EMPTY_SKILL_REGISTRY_FIXTURE_PATH,
    EMPTY_SKILL_REGISTRY_FIXTURE_SHA256,
    EMPTY_SKILL_REGISTRY_POLICY_PATH,
    EMPTY_SKILL_REGISTRY_POLICY_SHA256,
    EMPTY_SKILL_REGISTRY_REF,
    EMPTY_SKILL_REGISTRY_VALIDATION_PATH,
    EMPTY_SKILL_REGISTRY_VALIDATION_SHA256,
    EXPECTED_CAPABILITIES,
    SOURCE_CAPABILITY_PATH,
    SYNTHETIC_TARGET_PROFILE_REF,
    CapabilityAuthorityInvalid,
    CapabilityCoverageInvalid,
    CapabilityOwnerKind,
    CapabilityOwnershipDecision,
    CapabilityOwnershipGraph,
    CapabilityOwnershipInputInvalid,
    CapabilityOwnershipInvalidatedError,
    CapabilityOwnershipReceipt,
)
from cmf_builder.domain.constitutional_validation import (
    ConstitutionalValidationReceipt,
    ConstitutionalValidationReport,
)
from cmf_builder.domain.harness_ir import HarnessIR, HarnessIRAuthorityRejected
from cmf_builder.domain.run import LifecycleState, Run


class CapabilityCommandRejected(Exception):
    code = "CapabilityCommandRejected"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class CompileCapabilityOwnershipCommand:
    command_id: str
    run_id: str
    actor_id: str
    expected_version: int
    correlation_id: str
    causation_id: str
    ownership_input_path: str = CAPABILITY_OWNERSHIP_INPUT_PATH
    ownership_input_sha256: str = CAPABILITY_OWNERSHIP_INPUT_SHA256


class CapabilityCommandService:
    STORY_ID = "ST-04.01"
    CONTRACT_VERSION = (
        f"{CAPABILITY_OWNERSHIP_SCHEMA_ID}@{CAPABILITY_OWNERSHIP_SCHEMA_VERSION}"
    )

    def __init__(
        self,
        *,
        root: Path,
        repository: CapabilityOwnershipRepository,
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
        self, command: CompileCapabilityOwnershipCommand
    ) -> CapabilityOwnershipReceipt:
        run: Run | None = None
        ir: HarnessIR | None = None
        constitutional_report: ConstitutionalValidationReport | None = None
        constitutional_receipt: ConstitutionalValidationReceipt | None = None
        graph: CapabilityOwnershipGraph | None = None
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
                    "Only deterministic Builder code may compile capability ownership.",
                    actor_id=actor.actor_id,
                    actor_kind=actor.kind.value,
                )
            ir, constitutional_report, constitutional_receipt = (
                self._load_active_parent(run)
            )
            self._validate_empty_registry(ir)
            decisions = self._load_decisions(command, ir)
            graph = CapabilityOwnershipGraph.create(
                run_id=run.run_id,
                ir_id=ir.ir_id,
                ir_hash=ir.ir_hash,
                source_lock_ref=ir.source_lock_ref,
                boundary_ref=ir.boundary_ref,
                ratification_ref=ir.ratification_ref,
                model_ref=ir.model_ref,
                artifact_set_id=constitutional_report.artifact_set_id,
                constitutional_report_id=constitutional_report.report_id,
                constitutional_report_hash=constitutional_report.report_hash,
                constitutional_receipt_id=constitutional_receipt.receipt_id,
                constitutional_receipt_hash=constitutional_receipt.receipt_hash,
                authority_identity=command.actor_id,
                decisions=decisions,
            )
            event_id = self._ids.new_id("event")
            final_run, event = run.attach_capability_ownership(
                graph_ref=graph.graph_id,
                graph_hash=graph.graph_hash,
                harness_ir_ref=ir.ir_id,
                constitutional_report_ref=constitutional_report.report_id,
                capability_count=len(graph.decisions),
                event_id=event_id,
                command_id=command.command_id,
                actor_id=command.actor_id,
                timestamp=self._clock.now(),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
            )
            receipt = CapabilityOwnershipReceipt.create(
                command_id=command.command_id,
                graph=graph,
                authority_identity=command.actor_id,
                event_ids=(event.event_id,),
                stream_version=final_run.stream_version,
            )
            self._repository.commit_capability_ownership(
                run_id=run.run_id,
                expected_version=command.expected_version,
                events=(event,),
                command_id=command.command_id,
                command_record=CommandRecord(payload_hash=payload_hash, result=receipt),
                graph=graph,
                receipt=receipt,
            )
            for event_name in (
                "ST-04.01:CapabilityOwnershipCompiled",
                "ST-04.01:CapabilityCoverageValidated",
                "ST-04.01:OwnershipEvidenceValidated",
                "ST-04.01:OutcomeVerified",
            ):
                self._emit(
                    event_name=event_name,
                    outcome="PASS",
                    command=command,
                    run=final_run,
                    ir=ir,
                    constitutional_report=constitutional_report,
                    graph=graph,
                    receipt=receipt,
                    failure_context={},
                )
            return receipt
        except Exception as error:
            self._emit(
                event_name="ST-04.01:OutcomeRejected",
                outcome="FAIL",
                command=command,
                run=run,
                ir=ir,
                constitutional_report=constitutional_report,
                graph=graph,
                receipt=None,
                failure_context={
                    "code": str(getattr(error, "code", type(error).__name__)),
                    "message": str(error),
                    **dict(getattr(error, "context", {})),
                },
            )
            raise

    def get_active(self, run_id: str) -> CapabilityOwnershipGraph:
        run = self._repository.load_run(run_id)
        if (
            not run.capability_ownership_ref
            or run.capability_ownership_invalidation_ref is not None
            or self._repository.is_capability_ownership_invalidated(
                run.capability_ownership_ref
            )
        ):
            raise CapabilityOwnershipInvalidatedError(
                "No active capability ownership graph is available.", run_id=run_id
            )
        graph = self._repository.get_capability_ownership_graph(
            run.capability_ownership_ref
        )
        if graph is None or graph.graph_hash != run.capability_ownership_hash:
            raise CapabilityOwnershipInvalidatedError(
                "The active capability graph is unavailable or hash-drifted."
            )
        graph.validate()
        return graph

    def get_historical(self, graph_id: str) -> CapabilityOwnershipGraph:
        graph = self._repository.get_capability_ownership_graph(graph_id)
        if graph is None:
            raise KeyError(graph_id)
        graph.validate()
        return graph

    def _load_active_parent(
        self, run: Run
    ) -> tuple[
        HarnessIR,
        ConstitutionalValidationReport,
        ConstitutionalValidationReceipt,
    ]:
        if (
            run.lifecycle_state is not LifecycleState.GENESIS
            or not run.harness_ir_ref
            or not run.artifact_set_ref
            or not run.artifact_manifest_ref
            or not run.constitutional_validation_ref
            or run.boundary_invalidation_ref is not None
            or run.harness_ir_invalidation_ref is not None
            or run.artifact_set_invalidation_ref is not None
            or run.constitutional_validation_invalidation_ref is not None
            or run.capability_ownership_ref is not None
            or run.capability_ownership_invalidation_ref is not None
            or self._repository.is_harness_ir_invalidated(run.harness_ir_ref)
            or self._repository.is_artifact_set_invalidated(run.artifact_set_ref)
            or self._repository.is_constitutional_validation_invalidated(
                run.constitutional_validation_ref
            )
        ):
            raise CapabilityCommandRejected(
                "Capability ownership requires the exact active ST-03.05 parent.",
                lifecycle_state=run.lifecycle_state.value,
            )
        ir = self._repository.get_harness_ir(run.harness_ir_ref)
        report = self._repository.get_constitutional_validation_report(
            run.constitutional_validation_ref
        )
        receipts = self._repository.constitutional_validation_receipts(run.run_id)
        if ir is None or report is None or len(receipts) != 1:
            raise CapabilityCommandRejected(
                "Harness IR, constitutional report, or receipt is unavailable."
            )
        receipt = receipts[0]
        ir.validate()
        report.validate()
        receipt.validate(report)
        if (
            ir.run_id != run.run_id
            or ir.target_profile_ref != SYNTHETIC_TARGET_PROFILE_REF
            or report.run_id != run.run_id
            or report.ir_id != ir.ir_id
            or report.ir_hash != ir.ir_hash
            or report.artifact_set_id != run.artifact_set_ref
            or report.manifest_id != run.artifact_manifest_ref
            or report.manifest_hash != run.artifact_manifest_hash
            or report.report_hash != run.constitutional_validation_hash
            or receipt.stream_version != run.stream_version
        ):
            raise CapabilityCommandRejected(
                "The active parent lineage or receipt identity has drifted."
            )
        return ir, report, receipt

    def _load_decisions(
        self, command: CompileCapabilityOwnershipCommand, ir: HarnessIR
    ) -> tuple[CapabilityOwnershipDecision, ...]:
        path = self._verified_file(
            command.ownership_input_path, command.ownership_input_sha256
        )
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CapabilityOwnershipInputInvalid(
                "Capability ownership input is not canonical UTF-8 JSON."
            ) from error
        expected_root_keys = {
            "schema_version",
            "scope",
            "target_profile_ref",
            "source_harness_ir_path",
            "implicit_owner_defaults_allowed",
            "decisions",
            "external_skills_required",
            "dynamic_skill_discovery_allowed",
            "production_eligible",
            "certified",
        }
        if (
            not isinstance(value, dict)
            or set(value) != expected_root_keys
            or value["schema_version"] != CAPABILITY_OWNERSHIP_INPUT_SCHEMA
            or value["scope"] != CAPABILITY_OWNERSHIP_SCOPE
            or value["target_profile_ref"] != SYNTHETIC_TARGET_PROFILE_REF
            or value["source_harness_ir_path"] != SOURCE_CAPABILITY_PATH
            or value["implicit_owner_defaults_allowed"] is not False
            or value["external_skills_required"] is not False
            or value["dynamic_skill_discovery_allowed"] is not False
            or value["production_eligible"] is not False
            or value["certified"] is not False
            or not isinstance(value["decisions"], list)
        ):
            raise CapabilityOwnershipInputInvalid(
                "Capability ownership root contract is incomplete or broadened."
            )
        capabilities_value = ir.value(SOURCE_CAPABILITY_PATH).value
        if not isinstance(capabilities_value, (list, tuple)) or any(
            not isinstance(item, str) or not item.strip()
            for item in capabilities_value
        ):
            raise CapabilityCoverageInvalid(
                "Harness IR capabilities are not an explicit identifier list."
            )
        capabilities = tuple(str(item) for item in capabilities_value)
        if (
            len(set(capabilities)) != len(capabilities)
            or tuple(sorted(capabilities)) != EXPECTED_CAPABILITIES
        ):
            raise CapabilityCoverageInvalid(
                "Harness IR capability set is missing, extra, duplicated, renamed, or stale.",
                observed=tuple(sorted(capabilities)),
            )
        decision_keys = {
            "capability_id",
            "owner_kind",
            "owner_id",
            "reliability_evidence",
            "cost_evidence",
            "authority_boundary",
            "handoff_responsibility",
        }
        decisions: list[CapabilityOwnershipDecision] = []
        for raw in value["decisions"]:
            if not isinstance(raw, dict) or set(raw) != decision_keys:
                raise CapabilityOwnershipInputInvalid(
                    "A capability ownership decision has unknown or missing fields."
                )
            try:
                owner_kind = CapabilityOwnerKind(raw["owner_kind"])
            except (TypeError, ValueError) as error:
                raise CapabilityAuthorityInvalid(
                    "Capability owner kind is not in the governed vocabulary."
                ) from error
            if not isinstance(raw["reliability_evidence"], list) or not isinstance(
                raw["cost_evidence"], list
            ):
                raise CapabilityOwnershipInputInvalid(
                    "Capability evidence must be explicit ordered lists."
                )
            decision = CapabilityOwnershipDecision(
                capability_id=str(raw["capability_id"]),
                owner_kind=owner_kind,
                owner_id=str(raw["owner_id"]),
                reliability_evidence=tuple(
                    str(item) for item in raw["reliability_evidence"]
                ),
                cost_evidence=tuple(str(item) for item in raw["cost_evidence"]),
                authority_boundary=str(raw["authority_boundary"]),
                handoff_responsibility=raw["handoff_responsibility"],
            )
            decisions.append(decision)
        decision_ids = tuple(item.capability_id for item in decisions)
        if (
            len(set(decision_ids)) != len(decision_ids)
            or tuple(sorted(decision_ids)) != EXPECTED_CAPABILITIES
            or any(item.owner_kind is not CapabilityOwnerKind.CODE for item in decisions)
        ):
            raise CapabilityCoverageInvalid(
                "Every synthetic capability requires one explicit code owner.",
                observed=tuple(sorted(decision_ids)),
            )
        return tuple(sorted(decisions, key=lambda item: item.capability_id))

    def _validate_empty_registry(self, ir: HarnessIR) -> None:
        self._verified_file(
            EMPTY_SKILL_REGISTRY_POLICY_PATH, EMPTY_SKILL_REGISTRY_POLICY_SHA256
        )
        self._verified_file(
            EMPTY_SKILL_REGISTRY_FIXTURE_PATH, EMPTY_SKILL_REGISTRY_FIXTURE_SHA256
        )
        self._verified_file(
            EMPTY_SKILL_REGISTRY_VALIDATION_PATH,
            EMPTY_SKILL_REGISTRY_VALIDATION_SHA256,
        )
        if (
            ir.value("skills.skill_registry_ref").value != EMPTY_SKILL_REGISTRY_REF
            or ir.value("skills.external_skills_required").value is not False
            or not ir.synthetic
            or not ir.repository_owned
            or ir.production_eligible
            or ir.certified
        ):
            raise CapabilityAuthorityInvalid(
                "The governed empty registry applies only to the bounded synthetic proof."
            )

    def _verified_file(self, relative_path: str, expected_sha256: str) -> Path:
        if not relative_path.strip() or not expected_sha256.strip():
            raise CapabilityOwnershipInputInvalid("A governed file pin is incomplete.")
        path = (self._root / relative_path).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as error:
            raise CapabilityOwnershipInputInvalid(
                "Governed input path escapes the repository root."
            ) from error
        try:
            observed = sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            raise CapabilityOwnershipInputInvalid(
                "Governed capability input is unavailable.", path=relative_path
            ) from error
        if observed != expected_sha256:
            raise CapabilityOwnershipInputInvalid(
                "Governed capability input hash does not match.",
                path=relative_path,
                expected_sha256=expected_sha256,
                observed_sha256=observed,
            )
        return path

    def _validate_command(self, command: CompileCapabilityOwnershipCommand) -> None:
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
            or command.ownership_input_path != CAPABILITY_OWNERSHIP_INPUT_PATH
            or command.ownership_input_sha256 != CAPABILITY_OWNERSHIP_INPUT_SHA256
        ):
            raise CapabilityOwnershipInputInvalid(
                "Capability compilation command identity or governed input pin is invalid."
            )

    def _duplicate(
        self, command_id: str, payload_hash: str
    ) -> CapabilityOwnershipReceipt | None:
        record = self._repository.get_command_record(command_id)
        if record is None:
            return None
        if record.payload_hash != payload_hash:
            raise IdempotencyPayloadMismatch(
                "Command identity was reused with a different payload.",
                command_id=command_id,
            )
        if not isinstance(record.result, CapabilityOwnershipReceipt):
            raise IdempotencyPayloadMismatch(
                "Command identity belongs to a different result contract.",
                command_id=command_id,
            )
        return record.result

    def _emit_replay(
        self,
        command: CompileCapabilityOwnershipCommand,
        receipt: CapabilityOwnershipReceipt,
    ) -> None:
        run = self._repository.load_run(command.run_id)
        graph = self._repository.get_capability_ownership_graph(receipt.graph_id)
        if graph is None:
            raise CapabilityCommandRejected("Replay capability graph is unavailable.")
        ir = self._repository.get_harness_ir(graph.ir_id)
        report = self._repository.get_constitutional_validation_report(
            graph.constitutional_report_id
        )
        if ir is None or report is None:
            raise CapabilityCommandRejected("Replay capability lineage is unavailable.")
        self._emit(
            event_name="ST-04.01:CompilationReplayReturned",
            outcome="PASS",
            command=command,
            run=run,
            ir=ir,
            constitutional_report=report,
            graph=graph,
            receipt=receipt,
            failure_context={},
        )

    def _emit(
        self,
        *,
        event_name: str,
        outcome: str,
        command: CompileCapabilityOwnershipCommand,
        run: Run | None,
        ir: HarnessIR | None,
        constitutional_report: ConstitutionalValidationReport | None,
        graph: CapabilityOwnershipGraph | None,
        receipt: CapabilityOwnershipReceipt | None,
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
                source_lock_id=(ir.source_lock_ref if ir else "unassigned"),
                boundary_id=(ir.boundary_ref if ir else "unassigned"),
                model_id=(ir.model_ref if ir else "unassigned"),
                decision_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                decision_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                harness_ir_id=(ir.ir_id if ir else "unassigned"),
                harness_ir_hash=(ir.ir_hash if ir else "unassigned"),
                harness_ir_schema_id=(ir.schema_id if ir else "unassigned"),
                harness_ir_schema_version=(ir.schema_version if ir else "unassigned"),
                harness_ir_revision=(ir.revision if ir else 0),
                harness_ir_status=(ir.status.value if ir else "unassigned"),
                artifact_set_id=(
                    constitutional_report.artifact_set_id
                    if constitutional_report
                    else "unassigned"
                ),
                constitutional_report_id=(
                    constitutional_report.report_id
                    if constitutional_report
                    else "unassigned"
                ),
                constitutional_report_hash=(
                    constitutional_report.report_hash
                    if constitutional_report
                    else "unassigned"
                ),
                constitutional_precedence_disposition=(
                    "PASS_HIGHER_AUTHORITY_PRESERVED"
                    if constitutional_report
                    else "unassigned"
                ),
                capability_graph_id=(graph.graph_id if graph else "unassigned"),
                capability_graph_hash=(graph.graph_hash if graph else "unassigned"),
                capability_receipt_id=(receipt.receipt_id if receipt else "unassigned"),
                capability_receipt_hash=(receipt.receipt_hash if receipt else "unassigned"),
                capability_count=(len(graph.decisions) if graph else 0),
                capability_owner_kind_counts=(
                    graph.owner_kind_counts if graph else ()
                ),
                capability_reliability_coverage_count=(
                    sum(bool(item.reliability_evidence) for item in graph.decisions)
                    if graph
                    else 0
                ),
                capability_cost_coverage_count=(
                    sum(bool(item.cost_evidence) for item in graph.decisions)
                    if graph
                    else 0
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
