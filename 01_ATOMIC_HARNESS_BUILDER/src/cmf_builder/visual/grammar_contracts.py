"""Immutable provisional-grammar contracts for ST-02.03.

Syntax motifs are deterministic derivations from ST-02.02 graphs.  Meaning and
Activative interpretations remain explicit hypotheses and cannot be promoted by
this offline development branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence

from cmf_builder.visual.graph_contracts import (
    GraphKind,
    SubstrateGraph,
    SubstrateKind,
)
from cmf_builder.visual.ontology import (
    Applicability,
    KnowledgeStatus,
    ProvenanceReference,
    SourceReference,
    SyntaxContractError,
    Uncertainty,
    canonical_sha256,
    require_identifier,
)


STORY_ID = "ST-02.03"
DEVELOPMENT_MODE = "OD_AM_001_OFFLINE_DEVELOPMENT"


class GrammarContractError(SyntaxContractError):
    code = "GrammarContractError"


class GraphEvidenceInvalid(GrammarContractError):
    code = "GraphEvidenceInvalid"


class InsufficientGraphSupport(GrammarContractError):
    code = "InsufficientGraphSupport"


class GenericFlatteningRejected(GrammarContractError):
    code = "GenericFlatteningRejected"


class KnowledgePromotionRejected(GrammarContractError):
    code = "KnowledgePromotionRejected"


class GrammarAuthorityRejected(GrammarContractError):
    code = "GrammarAuthorityRejected"


class AtomicGrammarCommitRejected(GrammarContractError):
    code = "AtomicGrammarCommitRejected"


class GrammarMaturity(str, Enum):
    PROVISIONAL = "PROVISIONAL"


class ProjectionMode(str, Enum):
    SUBSTRATE_SPECIFIC = "SUBSTRATE_SPECIFIC"
    GENERIC_FLATTENED = "GENERIC_FLATTENED"


class HypothesisScope(str, Enum):
    FUNCTION = "FUNCTION"
    SEQUENCE_EFFECT = "SEQUENCE_EFFECT"
    ACTIVATIVE_ROLE = "ACTIVATIVE_ROLE"


@dataclass(frozen=True, slots=True)
class GrammarInductionPolicy:
    policy_id: str
    version: str
    category_id: str
    minimum_distinct_specimen_support: int
    induction_authority_ref: str
    allowed_hypothesis_proposers: tuple[str, ...]
    projection_mode: ProjectionMode = ProjectionMode.SUBSTRATE_SPECIFIC

    def __post_init__(self) -> None:
        require_identifier(self.policy_id, "grammar_policy_id")
        require_identifier(self.version, "grammar_policy_version")
        require_identifier(self.category_id, "grammar_category_id")
        require_identifier(self.induction_authority_ref, "induction_authority_ref")
        if self.minimum_distinct_specimen_support < 2:
            raise InsufficientGraphSupport(
                "cross-specimen grammar induction requires at least two specimens"
            )
        if self.projection_mode is ProjectionMode.GENERIC_FLATTENED:
            raise GenericFlatteningRejected(
                "grammar induction must preserve substrate and graph-kind identity"
            )
        if not self.allowed_hypothesis_proposers or len(
            set(self.allowed_hypothesis_proposers)
        ) != len(self.allowed_hypothesis_proposers):
            raise GrammarAuthorityRejected(
                "hypothesis proposer authorities must be non-empty and unique"
            )
        for proposer in self.allowed_hypothesis_proposers:
            require_identifier(proposer, "hypothesis_proposer_authority")

    @property
    def policy_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "category_id": self.category_id,
            "minimum_distinct_specimen_support": self.minimum_distinct_specimen_support,
            "induction_authority_ref": self.induction_authority_ref,
            "allowed_hypothesis_proposers": list(
                sorted(self.allowed_hypothesis_proposers)
            ),
            "projection_mode": self.projection_mode.value,
        }


@dataclass(frozen=True, slots=True)
class RichObservationReference:
    observation_id: str
    component_id: str
    ontology_term_id: str
    category_id: str
    source: SourceReference
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    applicability: Applicability
    observation_status: str
    knowledge_status: str
    geometry_sha256: str

    def as_dict(self) -> dict[str, object]:
        return {
            "observation_id": self.observation_id,
            "component_id": self.component_id,
            "ontology_term_id": self.ontology_term_id,
            "category_id": self.category_id,
            "source": self.source.as_dict(),
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "applicability": self.applicability.as_dict(),
            "observation_status": self.observation_status,
            "knowledge_status": self.knowledge_status,
            "geometry_sha256": self.geometry_sha256,
        }


@dataclass(frozen=True, slots=True)
class SourceGraphReference:
    graph_id: str
    artifact_sha256: str
    graph_kind: GraphKind
    substrate: SubstrateKind
    specimen_id: str
    specimen_artifact_sha256: str
    source_content_sha256: str
    plan_sha256: str
    observations: tuple[RichObservationReference, ...]
    edge_ids: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "graph_id": self.graph_id,
            "artifact_sha256": self.artifact_sha256,
            "graph_kind": self.graph_kind.value,
            "substrate": self.substrate.value,
            "specimen_id": self.specimen_id,
            "specimen_artifact_sha256": self.specimen_artifact_sha256,
            "source_content_sha256": self.source_content_sha256,
            "plan_sha256": self.plan_sha256,
            "observations": [item.as_dict() for item in self.observations],
            "edge_ids": list(self.edge_ids),
        }


@dataclass(frozen=True, slots=True)
class GrammarMotif:
    motif_id: str
    substrate: SubstrateKind
    graph_kind: GraphKind
    relation: str
    from_ontology_term_id: str
    to_ontology_term_id: str
    distinct_specimen_support: int
    source_graph_ids: tuple[str, ...]
    source_edge_ids: tuple[str, ...]
    source_observation_ids: tuple[str, ...]
    provenance: tuple[ProvenanceReference, ...]
    knowledge_status: KnowledgeStatus = KnowledgeStatus.DETERMINISTIC_DERIVATION

    def as_dict(self) -> dict[str, object]:
        return {
            "motif_id": self.motif_id,
            "substrate": self.substrate.value,
            "graph_kind": self.graph_kind.value,
            "relation": self.relation,
            "from_ontology_term_id": self.from_ontology_term_id,
            "to_ontology_term_id": self.to_ontology_term_id,
            "distinct_specimen_support": self.distinct_specimen_support,
            "source_graph_ids": list(self.source_graph_ids),
            "source_edge_ids": list(self.source_edge_ids),
            "source_observation_ids": list(self.source_observation_ids),
            "provenance": [item.as_dict() for item in self.provenance],
            "knowledge_status": self.knowledge_status.value,
        }


@dataclass(frozen=True, slots=True)
class ProvisionalMeaningHypothesis:
    hypothesis_id: str
    scope: HypothesisScope
    statement: str
    proposer_authority_ref: str
    source_graph_ids: tuple[str, ...]
    source_edge_ids: tuple[str, ...]
    source_observation_ids: tuple[str, ...]
    alternatives: tuple[str, ...]
    provenance: tuple[ProvenanceReference, ...]
    uncertainty: Uncertainty
    knowledge_status: KnowledgeStatus = KnowledgeStatus.HYPOTHESIS
    maturity: GrammarMaturity = GrammarMaturity.PROVISIONAL

    @staticmethod
    def contains_unauthorized_claim(statement: str) -> bool:
        forbidden_claims = (
            "production ready",
            "certified",
            "ratified truth",
            "reaction receipt issued",
            "expression moment issued",
            "human reaction is",
        )
        return any(claim in statement.lower() for claim in forbidden_claims)

    @classmethod
    def create(
        cls,
        *,
        scope: HypothesisScope,
        statement: str,
        proposer_authority_ref: str,
        source_graph_ids: Sequence[str],
        source_edge_ids: Sequence[str],
        source_observation_ids: Sequence[str],
        alternatives: Sequence[str],
        provenance: Sequence[ProvenanceReference],
        uncertainty: Uncertainty,
    ) -> "ProvisionalMeaningHypothesis":
        require_identifier(proposer_authority_ref, "hypothesis_proposer_authority")
        text = statement.strip()
        if not text:
            raise KnowledgePromotionRejected("hypothesis statement cannot be blank")
        if cls.contains_unauthorized_claim(text):
            raise KnowledgePromotionRejected(
                "provisional hypothesis contains an unauthorized authority claim"
            )
        graph_ids = tuple(sorted(set(source_graph_ids)))
        edge_ids = tuple(sorted(set(source_edge_ids)))
        observation_ids = tuple(sorted(set(source_observation_ids)))
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
        if not graph_ids or not edge_ids or not observation_ids or not ordered_provenance:
            raise KnowledgePromotionRejected(
                "hypotheses require graph, edge, observation and provenance evidence"
            )
        normalized_alternatives = tuple(
            sorted({item.strip() for item in alternatives if item.strip()})
        )
        payload = {
            "scope": scope.value,
            "statement": text,
            "proposer_authority_ref": proposer_authority_ref,
            "source_graph_ids": list(graph_ids),
            "source_edge_ids": list(edge_ids),
            "source_observation_ids": list(observation_ids),
            "alternatives": list(normalized_alternatives),
            "provenance": [item.as_dict() for item in ordered_provenance],
            "uncertainty": uncertainty.as_dict(),
            "knowledge_status": KnowledgeStatus.HYPOTHESIS.value,
            "maturity": GrammarMaturity.PROVISIONAL.value,
        }
        return cls(
            hypothesis_id=canonical_sha256(payload),
            scope=scope,
            statement=text,
            proposer_authority_ref=proposer_authority_ref,
            source_graph_ids=graph_ids,
            source_edge_ids=edge_ids,
            source_observation_ids=observation_ids,
            alternatives=normalized_alternatives,
            provenance=ordered_provenance,
            uncertainty=uncertainty,
        )

    def identity_payload(self) -> dict[str, object]:
        return {
            "scope": self.scope.value,
            "statement": self.statement,
            "proposer_authority_ref": self.proposer_authority_ref,
            "source_graph_ids": list(self.source_graph_ids),
            "source_edge_ids": list(self.source_edge_ids),
            "source_observation_ids": list(self.source_observation_ids),
            "alternatives": list(self.alternatives),
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "knowledge_status": self.knowledge_status.value,
            "maturity": self.maturity.value,
        }

    def as_dict(self) -> dict[str, object]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "scope": self.scope.value,
            "statement": self.statement,
            "proposer_authority_ref": self.proposer_authority_ref,
            "source_graph_ids": list(self.source_graph_ids),
            "source_edge_ids": list(self.source_edge_ids),
            "source_observation_ids": list(self.source_observation_ids),
            "alternatives": list(self.alternatives),
            "provenance": [item.as_dict() for item in self.provenance],
            "uncertainty": self.uncertainty.as_dict(),
            "knowledge_status": self.knowledge_status.value,
            "maturity": self.maturity.value,
        }


@dataclass(frozen=True, slots=True)
class ProvisionalGrammar:
    grammar_id: str
    series_id: str
    version: str
    category_id: str
    policy_sha256: str
    source_graphs: tuple[SourceGraphReference, ...]
    motifs: tuple[GrammarMotif, ...]
    hypotheses: tuple[ProvisionalMeaningHypothesis, ...]
    induction_authority_ref: str
    artifact_sha256: str
    maturity: GrammarMaturity = GrammarMaturity.PROVISIONAL
    projection_mode: ProjectionMode = ProjectionMode.SUBSTRATE_SPECIFIC
    evidence_gate_status: str = "EVIDENCE_PENDING"
    production_ready: bool = False
    certified: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "grammar_id": self.grammar_id,
            "series_id": self.series_id,
            "version": self.version,
            "category_id": self.category_id,
            "policy_sha256": self.policy_sha256,
            "source_graphs": [item.as_dict() for item in self.source_graphs],
            "motifs": [item.as_dict() for item in self.motifs],
            "hypotheses": [item.as_dict() for item in self.hypotheses],
            "induction_authority_ref": self.induction_authority_ref,
            "artifact_sha256": self.artifact_sha256,
            "maturity": self.maturity.value,
            "projection_mode": self.projection_mode.value,
            "evidence_gate_status": self.evidence_gate_status,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class GrammarInductionReceipt:
    receipt_id: str
    run_id: str
    grammar_id: str
    grammar_version: str
    grammar_artifact_sha256: str
    policy_sha256: str
    authority_identity: str
    source_graph_count: int
    motif_count: int
    hypothesis_count: int
    provenance: tuple[ProvenanceReference, ...]
    outcome: str = "OUTCOME_VERIFIED"
    failure_context: str = "NONE"
    event_name: str = "ST-02.03:OutcomeVerified"
    story_id: str = STORY_ID
    development_mode: str = DEVELOPMENT_MODE

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
            "grammar_id": self.grammar_id,
            "grammar_version": self.grammar_version,
            "grammar_artifact_sha256": self.grammar_artifact_sha256,
            "policy_sha256": self.policy_sha256,
            "authority_identity": self.authority_identity,
            "source_graph_count": self.source_graph_count,
            "motif_count": self.motif_count,
            "hypothesis_count": self.hypothesis_count,
            "provenance": [item.as_dict() for item in self.provenance],
            "outcome": self.outcome,
            "failure_context": self.failure_context,
        }


@dataclass(frozen=True, slots=True)
class GrammarInductionResult:
    grammar: ProvisionalGrammar
    receipt: GrammarInductionReceipt

    def as_dict(self) -> dict[str, object]:
        return {"grammar": self.grammar.as_dict(), "receipt": self.receipt.as_dict()}
