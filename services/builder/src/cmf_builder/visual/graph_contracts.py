"""Typed substrate-graph contracts for the ST-02.02 offline branch.

Graph artifacts retain the ST-02.01 observation objects that authorize every node
and edge.  The contracts do not infer meaning, execute providers, or promote
development evidence into production authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from cmf_builder.visual.normalization import SyntaxObservation
from cmf_builder.visual.ontology import (
    Applicability,
    EvidenceOrigin,
    KnowledgeStatus,
    ObservationContaminated,
    ObservationStatus,
    ProvenanceReference,
    ProviderOnlyClaimRejected,
    SourceReference,
    SyntaxContractError,
    Uncertainty,
    canonical_sha256,
    require_identifier,
)


STORY_ID = "ST-02.02"
DEVELOPMENT_MODE = "OD_AM_001_OFFLINE_DEVELOPMENT"


class GraphContractError(SyntaxContractError):
    code = "GraphContractError"


class GraphPlanInvalid(GraphContractError):
    code = "GraphPlanInvalid"


class UnsupportedSubstrateRelation(GraphContractError):
    code = "UnsupportedSubstrateRelation"


class UntraceableGraphEdge(GraphContractError):
    code = "UntraceableGraphEdge"


class GraphCycleDetected(GraphContractError):
    code = "GraphCycleDetected"


class RelationshipContradiction(GraphContractError):
    code = "RelationshipContradiction"


class TemporalStateMissing(GraphContractError):
    code = "TemporalStateMissing"


class SubstrateKind(str, Enum):
    STATIC_VISUAL = "STATIC_VISUAL"
    TIME_BASED_VISUAL = "TIME_BASED_VISUAL"
    STRUCTURAL_CONVERSATIONAL = "STRUCTURAL_CONVERSATIONAL"


class GraphKind(str, Enum):
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"
    READING_ORDER = "READING_ORDER"
    STRUCTURAL_CONVERSATIONAL = "STRUCTURAL_CONVERSATIONAL"


class CompositionVariableClass(str, Enum):
    NORMALIZED_GEOMETRY = "NORMALIZED_GEOMETRY"
    STRUCTURAL_SEQUENCE = "STRUCTURAL_SEQUENCE"
    TEMPORAL_POSITION = "TEMPORAL_POSITION"
    CONTENT_REFERENCE = "CONTENT_REFERENCE"


@dataclass(frozen=True, slots=True)
class CompositionVariable:
    variable_id: str
    variable_class: CompositionVariableClass
    name: str
    value: str | int | bool
    observation_id: str
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty

    def as_dict(self) -> dict[str, object]:
        return {
            "variable_id": self.variable_id,
            "variable_class": self.variable_class.value,
            "name": self.name,
            "value": self.value,
            "observation_id": self.observation_id,
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class RelationEvidence:
    relation: str
    from_observation_id: str
    to_observation_id: str
    evidence_observation_ids: tuple[str, ...]
    observation_status: ObservationStatus
    knowledge_status: KnowledgeStatus
    origin: EvidenceOrigin
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    applicability: Applicability

    @classmethod
    def create(
        cls,
        *,
        relation: str,
        from_observation_id: str,
        to_observation_id: str,
        evidence_observation_ids: Sequence[str],
        observation_status: ObservationStatus,
        knowledge_status: KnowledgeStatus,
        origin: EvidenceOrigin,
        provenance: Sequence[ProvenanceReference],
        uncertainty: Uncertainty,
        applicability: Applicability,
    ) -> "RelationEvidence":
        normalized_relation = relation.strip().upper()
        if not normalized_relation:
            raise GraphPlanInvalid("relation cannot be blank")
        for value, field in (
            (from_observation_id, "from_observation_id"),
            (to_observation_id, "to_observation_id"),
        ):
            if not value:
                raise GraphPlanInvalid(f"{field} cannot be blank")
        if from_observation_id == to_observation_id:
            raise GraphPlanInvalid("self-referential graph edges are prohibited")
        evidence_ids = tuple(sorted(set(evidence_observation_ids)))
        if not evidence_ids:
            raise UntraceableGraphEdge(
                "every relation requires at least one source observation"
            )
        if origin is EvidenceOrigin.PROVIDER_ONLY:
            raise ProviderOnlyClaimRejected(
                "provider-only relation output cannot enter a governed graph"
            )
        if knowledge_status is KnowledgeStatus.HYPOTHESIS:
            raise ObservationContaminated(
                "a relationship hypothesis cannot be promoted into a syntax graph"
            )
        expected = {
            ObservationStatus.MEASURED: KnowledgeStatus.OBSERVATION,
            ObservationStatus.DETERMINISTICALLY_DERIVED: KnowledgeStatus.DETERMINISTIC_DERIVATION,
        }[observation_status]
        if knowledge_status is not expected:
            raise ObservationContaminated(
                "relation observation and knowledge statuses disagree"
            )
        ordered_provenance = tuple(
            sorted(
                set(provenance),
                key=lambda item: (
                    item.artifact_id,
                    item.relationship,
                    item.artifact_sha256,
                ),
            )
        )
        if not ordered_provenance:
            raise UntraceableGraphEdge("relation provenance cannot be empty")
        return cls(
            relation=normalized_relation,
            from_observation_id=from_observation_id,
            to_observation_id=to_observation_id,
            evidence_observation_ids=evidence_ids,
            observation_status=observation_status,
            knowledge_status=knowledge_status,
            origin=origin,
            provenance=ordered_provenance,
            uncertainty=uncertainty,
            applicability=applicability,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "relation": self.relation,
            "from_observation_id": self.from_observation_id,
            "to_observation_id": self.to_observation_id,
            "evidence_observation_ids": list(self.evidence_observation_ids),
            "observation_status": self.observation_status.value,
            "knowledge_status": self.knowledge_status.value,
            "origin": self.origin.value,
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "applicability": self.applicability.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class SubstrateGraphPlan:
    plan_id: str
    version: str
    substrate: SubstrateKind
    authority_ref: str
    relations: tuple[RelationEvidence, ...]

    def __post_init__(self) -> None:
        require_identifier(self.plan_id, "graph_plan_id")
        require_identifier(self.version, "graph_plan_version")
        require_identifier(self.authority_ref, "graph_plan_authority_ref")

    @property
    def plan_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "version": self.version,
            "substrate": self.substrate.value,
            "authority_ref": self.authority_ref,
            "relations": [
                item.as_dict()
                for item in sorted(
                    self.relations,
                    key=lambda relation: (
                        relation.relation,
                        relation.from_observation_id,
                        relation.to_observation_id,
                    ),
                )
            ],
        }


@dataclass(frozen=True, slots=True)
class GraphNode:
    node_id: str
    observation: SyntaxObservation
    composition_variables: tuple[CompositionVariable, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "observation": self.observation.as_dict(),
            "composition_variables": [
                item.as_dict() for item in self.composition_variables
            ],
        }


@dataclass(frozen=True, slots=True)
class GraphEdge:
    edge_id: str
    graph_kind: GraphKind
    relation: str
    from_node_id: str
    to_node_id: str
    evidence_observation_ids: tuple[str, ...]
    source: SourceReference
    observation_status: ObservationStatus
    knowledge_status: KnowledgeStatus
    origin: EvidenceOrigin
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    applicability: Applicability

    def as_dict(self) -> dict[str, object]:
        return {
            "edge_id": self.edge_id,
            "graph_kind": self.graph_kind.value,
            "relation": self.relation,
            "from_node_id": self.from_node_id,
            "to_node_id": self.to_node_id,
            "evidence_observation_ids": list(self.evidence_observation_ids),
            "source": self.source.as_dict(),
            "observation_status": self.observation_status.value,
            "knowledge_status": self.knowledge_status.value,
            "origin": self.origin.value,
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "applicability": self.applicability.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class SubstrateGraph:
    graph_id: str
    graph_kind: GraphKind
    substrate: SubstrateKind
    specimen_id: str
    specimen_artifact_sha256: str
    plan_sha256: str
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    artifact_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "graph_id": self.graph_id,
            "graph_kind": self.graph_kind.value,
            "substrate": self.substrate.value,
            "specimen_id": self.specimen_id,
            "specimen_artifact_sha256": self.specimen_artifact_sha256,
            "plan_sha256": self.plan_sha256,
            "nodes": [item.as_dict() for item in self.nodes],
            "edges": [item.as_dict() for item in self.edges],
            "artifact_sha256": self.artifact_sha256,
        }


@dataclass(frozen=True, slots=True)
class GraphCompilationReceipt:
    receipt_id: str
    run_id: str
    result_sha256: str
    specimen_artifact_sha256: str
    plan_sha256: str
    authority_identity: str
    graph_count: int
    node_count: int
    edge_count: int
    provenance: tuple[ProvenanceReference, ...]
    outcome: str = "OUTCOME_VERIFIED"
    failure_context: str = "NONE"
    event_name: str = "ST-02.02:OutcomeVerified"
    story_id: str = STORY_ID
    development_mode: str = DEVELOPMENT_MODE
    evidence_gate_status: str = "EVIDENCE_PENDING"
    production_ready: bool = False
    certified: bool = False

    @property
    def receipt_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "run_id": self.run_id,
            "story_id": self.story_id,
            "development_mode": self.development_mode,
            "event_name": self.event_name,
            "result_sha256": self.result_sha256,
            "specimen_artifact_sha256": self.specimen_artifact_sha256,
            "plan_sha256": self.plan_sha256,
            "authority_identity": self.authority_identity,
            "graph_count": self.graph_count,
            "node_count": self.node_count,
            "edge_count": self.edge_count,
            "provenance": [item.as_dict() for item in self.provenance],
            "outcome": self.outcome,
            "failure_context": self.failure_context,
            "evidence_gate_status": self.evidence_gate_status,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class GraphCompilationResult:
    result_sha256: str
    graphs: tuple[SubstrateGraph, ...]
    receipt: GraphCompilationReceipt

    def as_dict(self) -> dict[str, object]:
        return {
            "result_sha256": self.result_sha256,
            "graphs": [item.as_dict() for item in self.graphs],
            "receipt": self.receipt.as_dict(),
        }

