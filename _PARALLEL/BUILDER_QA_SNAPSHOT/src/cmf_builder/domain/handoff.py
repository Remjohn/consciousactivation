from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.domain.phase_graph import PhaseGraph, PhaseNode


PHASE_HANDOFF_INPUT_PATH = "development-capsules/ST-04.04/PHASE_HANDOFF_INPUT.json"
PHASE_HANDOFF_INPUT_SHA256 = (
    "9901b5905d78212b5fed8bf63cc4fd9eda1b4f823d87bede38edf15b8c9c819f"
)
PHASE_HANDOFF_INPUT_SCHEMA = "cmf-builder-synthetic-phase-handoff-input/v1"
PHASE_HANDOFF_SCOPE = "ST-04.04_BUILDER_INTERNAL_HANDOFF_ONLY"
PHASE_GRAPH_CONTRACT = "cmf-builder-phase-graph/v1@1.0.0"
PHASE_CONTEXT_GRAPH_SCHEMA_ID = "cmf-builder-phase-context-graph/v1"
PHASE_HANDOFF_GRAPH_SCHEMA_ID = "cmf-builder-phase-handoff-graph/v1"
PHASE_HANDOFF_GRAPH_SCHEMA_VERSION = "1.0.0"
PHASE_HANDOFF_RECEIPT_SCHEMA_ID = "cmf-builder-phase-handoff-receipt/v1"
INTERNAL_HANDOFF_SCHEMA_ID = "cmf-builder-internal-handoff/v1"
INTERNAL_HANDOFF_DECISION_SCHEMA_ID = "cmf-builder-internal-handoff-decision/v1"
INTERNAL_HANDOFF_RECEIPT_SCHEMA_ID = "cmf-builder-internal-handoff-receipt/v1"


class HandoffError(Exception):
    code = "HandoffError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class HandoffInputInvalid(HandoffError):
    code = "HandoffInputInvalid"


class HandoffContractInvalid(HandoffError):
    code = "HandoffContractInvalid"


class HandoffAuthorityInvalid(HandoffError):
    code = "HandoffAuthorityInvalid"


class HandoffLineageInvalid(HandoffError):
    code = "HandoffLineageInvalid"


class HandoffStateInvalid(HandoffError):
    code = "HandoffStateInvalid"


class HandoffInvalidatedError(HandoffError):
    code = "HandoffInvalidated"


class InternalHandoffDecisionAction(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


def _unique_text(values: tuple[str, ...], label: str, *, allow_empty: bool = False) -> None:
    if (
        (not values and not allow_empty)
        or any(not value.strip() for value in values)
        or len(values) != len(set(values))
    ):
        raise HandoffContractInvalid(f"{label} must contain unique non-empty values.")


@dataclass(frozen=True, slots=True)
class ContextFieldDeclaration:
    field: str
    owner: str
    authority: str
    mutability: str

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.field, self.owner, self.authority)):
            raise HandoffContractInvalid("Context field identity and authority are required.")
        if self.mutability != "IMMUTABLE":
            raise HandoffContractInvalid("Builder-internal context fields must be immutable.")

    def canonical_dict(self) -> dict[str, str]:
        return {
            "field": self.field,
            "owner": self.owner,
            "authority": self.authority,
            "mutability": self.mutability,
        }


@dataclass(frozen=True, slots=True)
class PhaseContextContract:
    context_id: str
    phase_ref: str
    included_fields: tuple[ContextFieldDeclaration, ...]
    excluded_fields: tuple[str, ...]
    conditional_loads: tuple[str, ...]
    unload_behavior: str
    downstream_exposure: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.context_id, self.phase_ref, self.unload_behavior)):
            raise HandoffContractInvalid("Context identity, phase, and unload declaration are required.")
        names = tuple(item.field for item in self.included_fields)
        _unique_text(names, "Included context fields")
        _unique_text(self.excluded_fields, "Excluded context fields")
        _unique_text(self.conditional_loads, "Conditional context loads", allow_empty=True)
        _unique_text(self.downstream_exposure, "Downstream exposure")
        if set(names) & set(self.excluded_fields):
            raise HandoffContractInvalid("A context field cannot be both included and excluded.")
        owners = {item.field: item.owner for item in self.included_fields}
        if len(owners) != len(self.included_fields):
            raise HandoffContractInvalid("Every context field must have one primary owner.")
        if self.conditional_loads:
            raise HandoffContractInvalid(
                "The bounded internal-handoff proof cannot implement conditional loading."
            )
        if self.unload_behavior != "DROP_NON_OUTPUT_CONTEXT_AFTER_PHASE":
            raise HandoffContractInvalid("Context unload semantics are not governed.")

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(item.field for item in self.included_fields)

    def field(self, name: str) -> ContextFieldDeclaration:
        for item in self.included_fields:
            if item.field == name:
                return item
        raise KeyError(name)

    def canonical_dict(self) -> dict[str, object]:
        return {
            "context_id": self.context_id,
            "phase_ref": self.phase_ref,
            "included_fields": [item.canonical_dict() for item in self.included_fields],
            "excluded_fields": list(self.excluded_fields),
            "conditional_loads": list(self.conditional_loads),
            "unload_behavior": self.unload_behavior,
            "downstream_exposure": list(self.downstream_exposure),
        }


@dataclass(frozen=True, slots=True)
class PhaseContextGraph:
    context_graph_id: str
    context_graph_hash: str
    schema_id: str
    run_id: str
    phase_graph_id: str
    phase_graph_hash: str
    contexts: tuple[PhaseContextContract, ...]

    @classmethod
    def create(
        cls, *, phase_graph: PhaseGraph, contexts: tuple[PhaseContextContract, ...]
    ) -> "PhaseContextGraph":
        candidate = cls(
            context_graph_id="pending",
            context_graph_hash="pending",
            schema_id=PHASE_CONTEXT_GRAPH_SCHEMA_ID,
            run_id=phase_graph.run_id,
            phase_graph_id=phase_graph.graph_id,
            phase_graph_hash=phase_graph.graph_hash,
            contexts=tuple(sorted(contexts, key=lambda item: item.phase_ref)),
        )
        candidate.validate(phase_graph, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(
            candidate,
            context_graph_id=f"phase-context-graph_{digest}",
            context_graph_hash=f"sha256:{digest}",
        )
        result.validate(phase_graph)
        return result

    def validate(self, phase_graph: PhaseGraph, *, verify_identity: bool = True) -> None:
        for context in self.contexts:
            context.__post_init__()
        phase_by_id = {phase.phase_id: phase for phase in phase_graph.phases}
        if (
            self.schema_id != PHASE_CONTEXT_GRAPH_SCHEMA_ID
            or self.run_id != phase_graph.run_id
            or self.phase_graph_id != phase_graph.graph_id
            or self.phase_graph_hash != phase_graph.graph_hash
            or tuple(item.phase_ref for item in self.contexts) != tuple(sorted(phase_by_id))
        ):
            raise HandoffContractInvalid("Context Graph coverage or Phase Graph lineage is invalid.")
        for context in self.contexts:
            phase = phase_by_id[context.phase_ref]
            if tuple(sorted(context.downstream_exposure)) != tuple(sorted(phase.exit_evidence)):
                raise HandoffContractInvalid(
                    "Context downstream exposure must preserve all governed phase outputs.",
                    phase_ref=context.phase_ref,
                )
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if (
                self.context_graph_id != f"phase-context-graph_{digest}"
                or self.context_graph_hash != f"sha256:{digest}"
            ):
                raise HandoffContractInvalid("Context Graph content identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "run_id": self.run_id,
            "phase_graph_id": self.phase_graph_id,
            "phase_graph_hash": self.phase_graph_hash,
            "contexts": [item.canonical_dict() for item in self.contexts],
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class HandoffFieldDeclaration:
    field: str
    owner: str

    def __post_init__(self) -> None:
        if not self.field.strip() or not self.owner.strip():
            raise HandoffContractInvalid("Handoff fields require identity and ownership.")

    def canonical_dict(self) -> dict[str, str]:
        return {"field": self.field, "owner": self.owner}


@dataclass(frozen=True, slots=True)
class PhaseHandoffContract:
    contract_id: str
    version: str
    producer_phase: str
    consumer_phases: tuple[str, ...]
    required_fields: tuple[HandoffFieldDeclaration, ...]
    optional_fields: tuple[HandoffFieldDeclaration, ...]
    provenance_required: bool
    authority: str
    validation: tuple[str, ...]
    compatibility: str
    mutability: str
    downstream_rewrite: str
    invalidation: str

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.contract_id,
                self.version,
                self.producer_phase,
                self.authority,
            )
        ):
            raise HandoffContractInvalid("Handoff identity, version, phases, and authority are required.")
        _unique_text(self.consumer_phases, "Handoff consumers")
        _unique_text(tuple(item.field for item in self.required_fields), "Required handoff fields")
        _unique_text(tuple(item.field for item in self.optional_fields), "Optional handoff fields", allow_empty=True)
        _unique_text(self.validation, "Handoff validation rules")
        all_fields = tuple(item.field for item in (*self.required_fields, *self.optional_fields))
        if len(all_fields) != len(set(all_fields)):
            raise HandoffContractInvalid("Required and optional handoff fields must not overlap.")
        if (
            not self.provenance_required
            or self.compatibility != "EXACT_MAJOR_BACKWARD_COMPATIBLE_MINOR"
            or self.mutability != "IMMUTABLE_NEW_VERSION_ONLY"
            or self.downstream_rewrite != "PROHIBITED"
            or self.invalidation != "AFFECTED_CONSUMER_DESCENDANTS_ONLY"
        ):
            raise HandoffContractInvalid("Handoff governance cannot be weakened.")

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(item.field for item in (*self.required_fields, *self.optional_fields))

    def canonical_dict(self) -> dict[str, object]:
        return {
            "contract_id": self.contract_id,
            "version": self.version,
            "producer_phase": self.producer_phase,
            "consumer_phases": list(self.consumer_phases),
            "required_fields": [item.canonical_dict() for item in self.required_fields],
            "optional_fields": [item.canonical_dict() for item in self.optional_fields],
            "provenance_required": self.provenance_required,
            "authority": self.authority,
            "validation": list(self.validation),
            "compatibility": self.compatibility,
            "mutability": self.mutability,
            "downstream_rewrite": self.downstream_rewrite,
            "invalidation": self.invalidation,
        }


@dataclass(frozen=True, slots=True)
class PhaseHandoffGraph:
    graph_id: str
    graph_hash: str
    schema_id: str
    schema_version: str
    scope: str
    run_id: str
    target_profile_ref: str
    phase_graph_id: str
    phase_graph_hash: str
    module_graph_id: str
    module_graph_hash: str
    capability_graph_id: str
    capability_graph_hash: str
    ir_id: str
    ir_hash: str
    source_lock_ref: str
    boundary_ref: str
    ratification_ref: str
    model_ref: str
    artifact_set_id: str
    constitutional_report_id: str
    constitutional_report_hash: str
    constitutional_receipt_id: str
    constitutional_receipt_hash: str
    authority_identity: str
    handoff_input_path: str
    handoff_input_hash: str
    context_graph: PhaseContextGraph
    contracts: tuple[PhaseHandoffContract, ...]
    external_product_handoffs: tuple[str, ...]
    production_eligible: bool
    certified: bool
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        phase_graph: PhaseGraph,
        contexts: tuple[PhaseContextContract, ...],
        contracts: tuple[PhaseHandoffContract, ...],
        authority_identity: str,
    ) -> "PhaseHandoffGraph":
        context_graph = PhaseContextGraph.create(phase_graph=phase_graph, contexts=contexts)
        candidate = cls(
            graph_id="pending",
            graph_hash="pending",
            schema_id=PHASE_HANDOFF_GRAPH_SCHEMA_ID,
            schema_version=PHASE_HANDOFF_GRAPH_SCHEMA_VERSION,
            scope=PHASE_HANDOFF_SCOPE,
            run_id=phase_graph.run_id,
            target_profile_ref=phase_graph.target_profile_ref,
            phase_graph_id=phase_graph.graph_id,
            phase_graph_hash=phase_graph.graph_hash,
            module_graph_id=phase_graph.module_graph_id,
            module_graph_hash=phase_graph.module_graph_hash,
            capability_graph_id=phase_graph.capability_graph_id,
            capability_graph_hash=phase_graph.capability_graph_hash,
            ir_id=phase_graph.ir_id,
            ir_hash=phase_graph.ir_hash,
            source_lock_ref=phase_graph.source_lock_ref,
            boundary_ref=phase_graph.boundary_ref,
            ratification_ref=phase_graph.ratification_ref,
            model_ref=phase_graph.model_ref,
            artifact_set_id=phase_graph.artifact_set_id,
            constitutional_report_id=phase_graph.constitutional_report_id,
            constitutional_report_hash=phase_graph.constitutional_report_hash,
            constitutional_receipt_id=phase_graph.constitutional_receipt_id,
            constitutional_receipt_hash=phase_graph.constitutional_receipt_hash,
            authority_identity=authority_identity,
            handoff_input_path=PHASE_HANDOFF_INPUT_PATH,
            handoff_input_hash=f"sha256:{PHASE_HANDOFF_INPUT_SHA256}",
            context_graph=context_graph,
            contracts=tuple(sorted(contracts, key=lambda item: item.contract_id)),
            external_product_handoffs=(),
            production_eligible=False,
            certified=False,
            outcome="PASS",
        )
        candidate.validate(phase_graph, verify_identity=False)
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        result = replace(candidate, graph_id=f"phase-handoff-graph_{digest}", graph_hash=f"sha256:{digest}")
        result.validate(phase_graph)
        return result

    @property
    def lineage_refs(self) -> tuple[str, ...]:
        return (
            self.source_lock_ref,
            self.boundary_ref,
            self.ratification_ref,
            self.model_ref,
            self.ir_id,
            self.artifact_set_id,
            self.constitutional_report_id,
            self.capability_graph_id,
            self.module_graph_id,
            self.phase_graph_id,
        )

    def contract(self, contract_id: str) -> PhaseHandoffContract:
        for item in self.contracts:
            if item.contract_id == contract_id:
                return item
        raise KeyError(contract_id)

    def validate(self, phase_graph: PhaseGraph, *, verify_identity: bool = True) -> None:
        self.context_graph.validate(phase_graph)
        phase_by_id = {phase.phase_id: phase for phase in phase_graph.phases}
        context_by_phase = {item.phase_ref: item for item in self.context_graph.contexts}
        if (
            self.schema_id != PHASE_HANDOFF_GRAPH_SCHEMA_ID
            or self.schema_version != PHASE_HANDOFF_GRAPH_SCHEMA_VERSION
            or self.scope != PHASE_HANDOFF_SCOPE
            or self.run_id != phase_graph.run_id
            or self.target_profile_ref != phase_graph.target_profile_ref
            or self.phase_graph_id != phase_graph.graph_id
            or self.phase_graph_hash != phase_graph.graph_hash
            or self.module_graph_id != phase_graph.module_graph_id
            or self.module_graph_hash != phase_graph.module_graph_hash
            or self.capability_graph_id != phase_graph.capability_graph_id
            or self.capability_graph_hash != phase_graph.capability_graph_hash
            or self.ir_id != phase_graph.ir_id
            or self.ir_hash != phase_graph.ir_hash
            or self.source_lock_ref != phase_graph.source_lock_ref
            or self.boundary_ref != phase_graph.boundary_ref
            or self.ratification_ref != phase_graph.ratification_ref
            or self.model_ref != phase_graph.model_ref
            or self.artifact_set_id != phase_graph.artifact_set_id
            or self.constitutional_report_id != phase_graph.constitutional_report_id
            or self.constitutional_report_hash != phase_graph.constitutional_report_hash
            or self.constitutional_receipt_id != phase_graph.constitutional_receipt_id
            or self.constitutional_receipt_hash != phase_graph.constitutional_receipt_hash
            or not self.authority_identity.strip()
            or self.handoff_input_path != PHASE_HANDOFF_INPUT_PATH
            or self.handoff_input_hash != f"sha256:{PHASE_HANDOFF_INPUT_SHA256}"
            or not self.contracts
            or tuple(item.contract_id for item in self.contracts) != tuple(sorted(item.contract_id for item in self.contracts))
            or len({item.contract_id for item in self.contracts}) != len(self.contracts)
            or self.external_product_handoffs
            or self.production_eligible
            or self.certified
            or self.outcome != "PASS"
        ):
            raise HandoffContractInvalid("Internal handoff graph identity, lineage, or scope is invalid.")
        dependency_edges = {
            (dependency, phase.phase_id)
            for phase in phase_graph.phases
            for dependency in phase.dependencies
        }
        contract_edges: set[tuple[str, str]] = set()
        for contract in self.contracts:
            contract.__post_init__()
            producer = phase_by_id.get(contract.producer_phase)
            if producer is None:
                raise HandoffContractInvalid("Handoff producer phase is undeclared.")
            producer_context = context_by_phase[producer.phase_id]
            if contract.authority != producer.failure_owner:
                raise HandoffAuthorityInvalid("Handoff authority must match producer failure ownership.")
            for consumer_id in contract.consumer_phases:
                consumer = phase_by_id.get(consumer_id)
                if consumer is None or (producer.phase_id, consumer_id) not in dependency_edges:
                    raise HandoffContractInvalid("Handoff consumer must be a governed direct descendant.")
                consumer_context = context_by_phase[consumer_id]
                required_names = tuple(item.field for item in contract.required_fields)
                if tuple(sorted(required_names)) != tuple(
                    sorted(set(producer_context.downstream_exposure) & set(consumer_context.field_names))
                ):
                    raise HandoffContractInvalid("Handoff fields do not exactly bridge producer outputs to consumer inputs.")
                for field in contract.required_fields:
                    if field.owner != producer.failure_owner or consumer_context.field(field.field).owner != field.owner:
                        raise HandoffAuthorityInvalid("Handoff field ownership conflicts across the phase boundary.")
                contract_edges.add((producer.phase_id, consumer_id))
        if contract_edges != dependency_edges:
            raise HandoffContractInvalid("Every governed phase dependency requires exactly one internal handoff.")
        if verify_identity:
            digest = sha256(self.canonical_bytes()).hexdigest()
            if self.graph_id != f"phase-handoff-graph_{digest}" or self.graph_hash != f"sha256:{digest}":
                raise HandoffContractInvalid("Internal handoff graph content identity is invalid.")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "run_id": self.run_id,
            "target_profile_ref": self.target_profile_ref,
            "phase_graph_id": self.phase_graph_id,
            "phase_graph_hash": self.phase_graph_hash,
            "module_graph_id": self.module_graph_id,
            "module_graph_hash": self.module_graph_hash,
            "capability_graph_id": self.capability_graph_id,
            "capability_graph_hash": self.capability_graph_hash,
            "ir_id": self.ir_id,
            "ir_hash": self.ir_hash,
            "source_lock_ref": self.source_lock_ref,
            "boundary_ref": self.boundary_ref,
            "ratification_ref": self.ratification_ref,
            "model_ref": self.model_ref,
            "artifact_set_id": self.artifact_set_id,
            "constitutional_report_id": self.constitutional_report_id,
            "constitutional_report_hash": self.constitutional_report_hash,
            "constitutional_receipt_id": self.constitutional_receipt_id,
            "constitutional_receipt_hash": self.constitutional_receipt_hash,
            "authority_identity": self.authority_identity,
            "handoff_input_path": self.handoff_input_path,
            "handoff_input_hash": self.handoff_input_hash,
            "context_graph": self.context_graph.canonical_dict(),
            "contracts": [item.canonical_dict() for item in self.contracts],
            "external_product_handoffs": list(self.external_product_handoffs),
            "production_eligible": self.production_eligible,
            "certified": self.certified,
            "outcome": self.outcome,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class GovernedHandoffArtifact:
    field: str
    artifact_id: str
    artifact_hash: str
    version: str
    lineage_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.field, self.artifact_id, self.version)):
            raise HandoffLineageInvalid("Handoff artifact identity and version are required.")
        if not self.artifact_hash.startswith("sha256:") or len(self.artifact_hash) != 71:
            raise HandoffLineageInvalid("Handoff artifacts require a lowercase SHA-256 identity.")
        _unique_text(self.lineage_refs, "Handoff artifact lineage")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "field": self.field,
            "artifact_id": self.artifact_id,
            "artifact_hash": self.artifact_hash,
            "version": self.version,
            "lineage_refs": list(self.lineage_refs),
        }


@dataclass(frozen=True, slots=True)
class InternalHandoff:
    handoff_id: str
    handoff_hash: str
    schema_id: str
    run_id: str
    handoff_graph_id: str
    handoff_graph_hash: str
    contract_id: str
    contract_version: str
    sender_phase: str
    sender_module: str
    receiver_phase: str
    receiver_module: str
    artifacts: tuple[GovernedHandoffArtifact, ...]
    authority_identity: str
    provenance: tuple[str, ...]
    status: str

    @classmethod
    def create(
        cls,
        *,
        graph: PhaseHandoffGraph,
        phase_graph: PhaseGraph,
        contract: PhaseHandoffContract,
        receiver_phase: str,
        artifacts: tuple[GovernedHandoffArtifact, ...],
        authority_identity: str,
    ) -> "InternalHandoff":
        phase_by_id = {phase.phase_id: phase for phase in phase_graph.phases}
        producer = phase_by_id[contract.producer_phase]
        receiver = phase_by_id.get(receiver_phase)
        if receiver is None or receiver_phase not in contract.consumer_phases:
            raise HandoffContractInvalid("The receiver is not governed by this handoff contract.")
        if len(producer.module_refs) != 1 or len(receiver.module_refs) != 1:
            raise HandoffContractInvalid("The bounded handoff requires exact sender and receiver modules.")
        artifact_fields = tuple(item.field for item in artifacts)
        required_fields = tuple(item.field for item in contract.required_fields)
        if tuple(sorted(artifact_fields)) != tuple(sorted(required_fields)):
            raise HandoffContractInvalid("Issued artifacts do not exactly satisfy required handoff fields.")
        for artifact in artifacts:
            artifact.__post_init__()
            if artifact.version != contract.version or artifact.lineage_refs != graph.lineage_refs:
                raise HandoffLineageInvalid("A handed-off artifact has stale version or lineage.")
        candidate = cls(
            handoff_id="pending",
            handoff_hash="pending",
            schema_id=INTERNAL_HANDOFF_SCHEMA_ID,
            run_id=graph.run_id,
            handoff_graph_id=graph.graph_id,
            handoff_graph_hash=graph.graph_hash,
            contract_id=contract.contract_id,
            contract_version=contract.version,
            sender_phase=producer.phase_id,
            sender_module=producer.module_refs[0],
            receiver_phase=receiver.phase_id,
            receiver_module=receiver.module_refs[0],
            artifacts=tuple(sorted(artifacts, key=lambda item: item.field)),
            authority_identity=authority_identity,
            provenance=graph.lineage_refs,
            status="ISSUED",
        )
        if not authority_identity.strip():
            raise HandoffAuthorityInvalid("Issuance authority is required.")
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, handoff_id=f"internal-handoff_{digest}", handoff_hash=f"sha256:{digest}")

    def canonical_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "run_id": self.run_id,
            "handoff_graph_id": self.handoff_graph_id,
            "handoff_graph_hash": self.handoff_graph_hash,
            "contract_id": self.contract_id,
            "contract_version": self.contract_version,
            "sender_phase": self.sender_phase,
            "sender_module": self.sender_module,
            "receiver_phase": self.receiver_phase,
            "receiver_module": self.receiver_module,
            "artifacts": [item.canonical_dict() for item in self.artifacts],
            "authority_identity": self.authority_identity,
            "provenance": list(self.provenance),
            "status": self.status,
        }

    def validate(self, graph: PhaseHandoffGraph, phase_graph: PhaseGraph) -> None:
        graph.validate(phase_graph)
        contract = graph.contract(self.contract_id)
        phase_by_id = {phase.phase_id: phase for phase in phase_graph.phases}
        producer = phase_by_id.get(self.sender_phase)
        receiver = phase_by_id.get(self.receiver_phase)
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != INTERNAL_HANDOFF_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.handoff_graph_id != graph.graph_id
            or self.handoff_graph_hash != graph.graph_hash
            or self.contract_version != contract.version
            or producer is None
            or receiver is None
            or producer.phase_id != contract.producer_phase
            or receiver.phase_id not in contract.consumer_phases
            or self.sender_module not in producer.module_refs
            or self.receiver_module not in receiver.module_refs
            or tuple(item.field for item in self.artifacts)
            != tuple(sorted(item.field for item in contract.required_fields))
            or any(item.lineage_refs != graph.lineage_refs for item in self.artifacts)
            or self.provenance != graph.lineage_refs
            or not self.authority_identity.strip()
            or self.status != "ISSUED"
            or self.handoff_id != f"internal-handoff_{digest}"
            or self.handoff_hash != f"sha256:{digest}"
        ):
            raise HandoffStateInvalid("Internal handoff identity, contract, or lineage is invalid.")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(self.canonical_dict())


@dataclass(frozen=True, slots=True)
class InternalHandoffDecision:
    decision_id: str
    decision_hash: str
    schema_id: str
    handoff_id: str
    handoff_hash: str
    action: InternalHandoffDecisionAction
    receiver_phase: str
    receiver_authority: str
    authority_identity: str
    reason_code: str
    reason: str

    @classmethod
    def create(
        cls,
        *,
        handoff: InternalHandoff,
        action: InternalHandoffDecisionAction,
        receiver_phase: str,
        receiver_authority: str,
        authority_identity: str,
        reason_code: str,
        reason: str,
    ) -> "InternalHandoffDecision":
        if receiver_phase != handoff.receiver_phase:
            raise HandoffContractInvalid("Only the exact governed receiver may decide a handoff.")
        if not all(value.strip() for value in (receiver_authority, authority_identity, reason_code, reason)):
            raise HandoffAuthorityInvalid("A handoff decision requires receiver and actor authority plus typed rationale.")
        if action is InternalHandoffDecisionAction.ACCEPTED and reason_code != "CONTRACT_AND_ARTIFACTS_VALID":
            raise HandoffStateInvalid("Acceptance requires the governed validation disposition.")
        if action is InternalHandoffDecisionAction.REJECTED and reason_code == "CONTRACT_AND_ARTIFACTS_VALID":
            raise HandoffStateInvalid("Rejection requires a typed rejection reason.")
        candidate = cls(
            decision_id="pending",
            decision_hash="pending",
            schema_id=INTERNAL_HANDOFF_DECISION_SCHEMA_ID,
            handoff_id=handoff.handoff_id,
            handoff_hash=handoff.handoff_hash,
            action=action,
            receiver_phase=receiver_phase,
            receiver_authority=receiver_authority,
            authority_identity=authority_identity,
            reason_code=reason_code,
            reason=reason,
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, decision_id=f"internal-handoff-decision_{digest}", decision_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "handoff_id": self.handoff_id,
                "handoff_hash": self.handoff_hash,
                "action": self.action.value,
                "receiver_phase": self.receiver_phase,
                "receiver_authority": self.receiver_authority,
                "authority_identity": self.authority_identity,
                "reason_code": self.reason_code,
                "reason": self.reason,
            }
        )

    def validate(self, handoff: InternalHandoff, receiver_authority: str) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != INTERNAL_HANDOFF_DECISION_SCHEMA_ID
            or self.handoff_id != handoff.handoff_id
            or self.handoff_hash != handoff.handoff_hash
            or self.receiver_phase != handoff.receiver_phase
            or self.receiver_authority != receiver_authority
            or not self.authority_identity.strip()
            or not self.reason_code.strip()
            or not self.reason.strip()
            or self.decision_id != f"internal-handoff-decision_{digest}"
            or self.decision_hash != f"sha256:{digest}"
        ):
            raise HandoffStateInvalid("Internal handoff decision identity or authority is invalid.")


@dataclass(frozen=True, slots=True)
class PhaseHandoffReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    graph_id: str
    graph_hash: str
    context_graph_id: str
    phase_graph_id: str
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    context_count: int
    contract_count: int
    field_count: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        graph: PhaseHandoffGraph,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "PhaseHandoffReceipt":
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=PHASE_HANDOFF_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=graph.run_id,
            graph_id=graph.graph_id,
            graph_hash=graph.graph_hash,
            context_graph_id=graph.context_graph.context_graph_id,
            phase_graph_id=graph.phase_graph_id,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            context_count=len(graph.context_graph.contexts),
            contract_count=len(graph.contracts),
            field_count=sum(len(item.required_fields) + len(item.optional_fields) for item in graph.contracts),
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, receipt_id=f"phase-handoff-receipt_{digest}", receipt_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "graph_id": self.graph_id,
                "graph_hash": self.graph_hash,
                "context_graph_id": self.context_graph_id,
                "phase_graph_id": self.phase_graph_id,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "context_count": self.context_count,
                "contract_count": self.contract_count,
                "field_count": self.field_count,
                "outcome": self.outcome,
            }
        )

    def validate(self, graph: PhaseHandoffGraph, phase_graph: PhaseGraph) -> None:
        graph.validate(phase_graph)
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != PHASE_HANDOFF_RECEIPT_SCHEMA_ID
            or self.run_id != graph.run_id
            or self.graph_id != graph.graph_id
            or self.graph_hash != graph.graph_hash
            or self.context_graph_id != graph.context_graph.context_graph_id
            or self.phase_graph_id != graph.phase_graph_id
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.context_count != len(graph.context_graph.contexts)
            or self.contract_count != len(graph.contracts)
            or self.field_count
            != sum(len(item.required_fields) + len(item.optional_fields) for item in graph.contracts)
            or self.outcome != "PASS"
            or self.receipt_id != f"phase-handoff-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise HandoffStateInvalid("Phase handoff receipt does not match its graph.")


@dataclass(frozen=True, slots=True)
class InternalHandoffReceipt:
    receipt_id: str
    receipt_hash: str
    schema_id: str
    command_id: str
    run_id: str
    handoff_id: str
    handoff_hash: str
    action: str
    decision_id: str | None
    decision_hash: str | None
    authority_identity: str
    event_ids: tuple[str, ...]
    stream_version: int
    outcome: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        handoff: InternalHandoff,
        action: str,
        decision: InternalHandoffDecision | None,
        authority_identity: str,
        event_ids: tuple[str, ...],
        stream_version: int,
    ) -> "InternalHandoffReceipt":
        if action not in {"ISSUED", "ACCEPTED", "REJECTED"}:
            raise HandoffStateInvalid("Unknown internal handoff receipt action.")
        if (action == "ISSUED") != (decision is None):
            raise HandoffStateInvalid("Issue receipts omit decisions; decision receipts require one.")
        candidate = cls(
            receipt_id="pending",
            receipt_hash="pending",
            schema_id=INTERNAL_HANDOFF_RECEIPT_SCHEMA_ID,
            command_id=command_id,
            run_id=handoff.run_id,
            handoff_id=handoff.handoff_id,
            handoff_hash=handoff.handoff_hash,
            action=action,
            decision_id=decision.decision_id if decision else None,
            decision_hash=decision.decision_hash if decision else None,
            authority_identity=authority_identity,
            event_ids=event_ids,
            stream_version=stream_version,
            outcome="PASS",
        )
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, receipt_id=f"internal-handoff-receipt_{digest}", receipt_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "schema_id": self.schema_id,
                "command_id": self.command_id,
                "run_id": self.run_id,
                "handoff_id": self.handoff_id,
                "handoff_hash": self.handoff_hash,
                "action": self.action,
                "decision_id": self.decision_id,
                "decision_hash": self.decision_hash,
                "authority_identity": self.authority_identity,
                "event_ids": list(self.event_ids),
                "stream_version": self.stream_version,
                "outcome": self.outcome,
            }
        )

    def validate(
        self,
        handoff: InternalHandoff,
        decision: InternalHandoffDecision | None,
    ) -> None:
        digest = sha256(self.canonical_bytes()).hexdigest()
        if (
            self.schema_id != INTERNAL_HANDOFF_RECEIPT_SCHEMA_ID
            or self.run_id != handoff.run_id
            or self.handoff_id != handoff.handoff_id
            or self.handoff_hash != handoff.handoff_hash
            or self.action not in {"ISSUED", "ACCEPTED", "REJECTED"}
            or (self.action == "ISSUED") != (decision is None)
            or self.decision_id != (decision.decision_id if decision else None)
            or self.decision_hash != (decision.decision_hash if decision else None)
            or not self.authority_identity.strip()
            or len(self.event_ids) != 1
            or self.outcome != "PASS"
            or self.receipt_id != f"internal-handoff-receipt_{digest}"
            or self.receipt_hash != f"sha256:{digest}"
        ):
            raise HandoffStateInvalid("Internal handoff receipt does not match its governed state.")


@dataclass(frozen=True, slots=True)
class PhaseHandoffInvalidation:
    invalidation_id: str
    invalidation_hash: str
    handoff_graph_ref: str
    phase_graph_ref: str
    upstream_invalidation_ref: str
    affected_handoff_ids: tuple[str, ...]
    reason: str
    authority_identity: str

    @classmethod
    def create(
        cls,
        *,
        invalidation_id: str,
        handoff_graph_ref: str,
        phase_graph_ref: str,
        upstream_invalidation_ref: str,
        affected_handoff_ids: tuple[str, ...],
        reason: str,
        authority_identity: str,
    ) -> "PhaseHandoffInvalidation":
        _unique_text(affected_handoff_ids, "Affected internal handoffs", allow_empty=True)
        candidate = cls(
            invalidation_id=invalidation_id,
            invalidation_hash="pending",
            handoff_graph_ref=handoff_graph_ref,
            phase_graph_ref=phase_graph_ref,
            upstream_invalidation_ref=upstream_invalidation_ref,
            affected_handoff_ids=tuple(sorted(affected_handoff_ids)),
            reason=reason,
            authority_identity=authority_identity,
        )
        if not all(
            value.strip()
            for value in (
                invalidation_id,
                handoff_graph_ref,
                phase_graph_ref,
                upstream_invalidation_ref,
                reason,
                authority_identity,
            )
        ):
            raise HandoffError("Internal handoff invalidation identity is incomplete.")
        digest = sha256(candidate.canonical_bytes()).hexdigest()
        return replace(candidate, invalidation_hash=f"sha256:{digest}")

    def canonical_bytes(self) -> bytes:
        return _canonical_json(
            {
                "invalidation_id": self.invalidation_id,
                "handoff_graph_ref": self.handoff_graph_ref,
                "phase_graph_ref": self.phase_graph_ref,
                "upstream_invalidation_ref": self.upstream_invalidation_ref,
                "affected_handoff_ids": list(self.affected_handoff_ids),
                "reason": self.reason,
                "authority_identity": self.authority_identity,
            }
        )


def phase_failure_owner(phase: PhaseNode) -> str:
    return phase.failure_owner


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
