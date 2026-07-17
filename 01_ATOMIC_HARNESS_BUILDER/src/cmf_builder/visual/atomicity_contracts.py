"""Typed, provisional atomic-boundary comparison contracts for ST-02.04.

The objects in this module make candidate consequences inspectable.  They do
not select, ratify, or freeze an atomic boundary and cannot authorize Genesis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
import unicodedata

from cmf_builder.visual.ontology import (
    SyntaxContractError,
    canonical_sha256,
    require_identifier,
)


STORY_ID = "ST-02.04"
DEVELOPMENT_MODE = "OD_AM_001_OFFLINE_DEVELOPMENT"


class AtomicityContractError(SyntaxContractError):
    code = "AtomicityContractError"


class BoundaryEvidenceInvalid(AtomicityContractError):
    code = "BoundaryEvidenceInvalid"


class AlternativesIncomplete(AtomicityContractError):
    code = "AlternativesIncomplete"


class AtomicityAuthorityRejected(AtomicityContractError):
    code = "AtomicityAuthorityRejected"


class AtomicityCommitRejected(AtomicityContractError):
    code = "AtomicityCommitRejected"


class UnsupportedCertaintyRejected(AtomicityContractError):
    code = "UnsupportedCertaintyRejected"


AUTHORITY_CLAIM_POLICY_ID = "ST-02.04:ReservedAuthorityVocabulary"
AUTHORITY_CLAIM_POLICY_VERSION = "1.0.0"
AUTHORITY_RESERVED_PREFIXES = (
    "approv",
    "authoriz",
    "certif",
    "genesis",
    "ratif",
)
AUTHORITY_RESERVED_PHRASES = (
    "cleared for deployment",
    "cleared for production",
    "cleared for release",
    "final decision",
    "go live",
    "green light",
    "has been released",
    "human sign off",
    "is released",
    "owner sign off",
    "production ready",
    "ready for deployment",
    "ready for production",
    "ready for release",
    "release authorized",
    "safe to proceed",
    "signed off",
)
AUTHORITY_CLAIM_POLICY_SHA256 = canonical_sha256(
    {
        "policy_id": AUTHORITY_CLAIM_POLICY_ID,
        "version": AUTHORITY_CLAIM_POLICY_VERSION,
        "reserved_prefixes": list(AUTHORITY_RESERVED_PREFIXES),
        "reserved_phrases": list(AUTHORITY_RESERVED_PHRASES),
        "behavior": "REJECT_CONSERVATIVELY_IN_PROVISIONAL_COMPARISON_TEXT",
    }
)


def validate_provisional_claim_text(value: str, field: str) -> None:
    """Reject blank or authority-reserved claims after canonical normalization."""

    text = value.strip()
    if not text:
        raise BoundaryEvidenceInvalid(f"{field} cannot be blank")
    normalized = unicodedata.normalize("NFKC", text).casefold()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    normalized = " ".join(normalized.split())
    tokens = tuple(normalized.split())
    if any(
        token.startswith(prefix)
        for token in tokens
        for prefix in AUTHORITY_RESERVED_PREFIXES
    ) or any(phrase in normalized for phrase in AUTHORITY_RESERVED_PHRASES):
        raise UnsupportedCertaintyRejected(
            f"{field} uses authority-reserved approval, release, or Genesis vocabulary"
        )


class BoundaryOptionKind(str, Enum):
    MERGE = "MERGE"
    SPLIT = "SPLIT"
    VARIANT = "VARIANT"
    FAMILY = "FAMILY"


class AtomicityStatus(str, Enum):
    ATOMIC_HARNESS_CANDIDATE = "atomic_harness_candidate"
    VARIANT_OF_EXISTING = "variant_of_existing"
    DISH_FAMILY_CANDIDATE = "dish_family_candidate"
    FORMAT_FAMILY_ONLY = "format_family_only"
    NEEDS_CLUSTERING = "needs_clustering"
    NEEDS_PARTITION = "needs_partition"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class EvidenceStatus(str, Enum):
    DETERMINISTIC_SYNTAX = "DETERMINISTIC_SYNTAX"
    PROVISIONAL_HYPOTHESIS = "PROVISIONAL_HYPOTHESIS"
    UNAVAILABLE = "UNAVAILABLE"


class RecommendationDisposition(str, Enum):
    SUPPORT = "SUPPORT"
    REJECT = "REJECT"
    MORE_EVIDENCE = "MORE_EVIDENCE"


class ComparisonDimension(str, Enum):
    PRODUCTION_PROMISE = "PRODUCTION_PROMISE"
    PERSISTENT_VISUAL_INSTRUMENT = "PERSISTENT_VISUAL_INSTRUMENT"
    COMPOSITION_GRAMMAR = "COMPOSITION_GRAMMAR"
    STATE_MACHINE = "STATE_MACHINE"
    SEMANTIC_WORKCELL = "SEMANTIC_WORKCELL"
    INPUT_CONTRACT = "INPUT_CONTRACT"
    ASSET_PROGRAM = "ASSET_PROGRAM"
    RUNTIME_OWNERSHIP = "RUNTIME_OWNERSHIP"
    EVALUATION_FAILURES = "EVALUATION_FAILURES"
    REPAIR_BEHAVIOR = "REPAIR_BEHAVIOR"


class RiskDirection(str, Enum):
    OVER_MERGE = "OVER_MERGE"
    OVER_SPLIT = "OVER_SPLIT"


class RiskDomain(str, Enum):
    IMPLEMENTATION = "IMPLEMENTATION"
    CREATIVE = "CREATIVE"
    EVALUATION = "EVALUATION"
    MIGRATION = "MIGRATION"
    MAINTENANCE = "MAINTENANCE"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class GrammarEvidenceReference:
    grammar_id: str
    grammar_version: str
    grammar_artifact_sha256: str
    induction_receipt_id: str
    induction_receipt_sha256: str
    source_graph_ids: tuple[str, ...]
    evidence_gate_status: str = "EVIDENCE_PENDING"
    maturity: str = "PROVISIONAL"

    def as_dict(self) -> dict[str, object]:
        return {
            "grammar_id": self.grammar_id,
            "grammar_version": self.grammar_version,
            "grammar_artifact_sha256": self.grammar_artifact_sha256,
            "induction_receipt_id": self.induction_receipt_id,
            "induction_receipt_sha256": self.induction_receipt_sha256,
            "source_graph_ids": list(self.source_graph_ids),
            "evidence_gate_status": self.evidence_gate_status,
            "maturity": self.maturity,
        }


@dataclass(frozen=True, slots=True)
class DimensionAssessment:
    dimension: ComparisonDimension
    finding: str
    evidence_status: EvidenceStatus
    source_graph_ids: tuple[str, ...] = ()
    motif_ids: tuple[str, ...] = ()
    hypothesis_ids: tuple[str, ...] = ()
    protected_boundary_claim: bool = False
    calibration_receipt_ref: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "dimension": self.dimension.value,
            "finding": self.finding,
            "evidence_status": self.evidence_status.value,
            "source_graph_ids": list(self.source_graph_ids),
            "motif_ids": list(self.motif_ids),
            "hypothesis_ids": list(self.hypothesis_ids),
            "protected_boundary_claim": self.protected_boundary_claim,
            "calibration_receipt_ref": self.calibration_receipt_ref,
        }


@dataclass(frozen=True, slots=True)
class WrongBoundaryRisk:
    domain: RiskDomain
    direction: RiskDirection
    consequence: str
    severity: RiskSeverity
    source_graph_ids: tuple[str, ...]
    hypothesis_ids: tuple[str, ...]
    provisional: bool = True

    def as_dict(self) -> dict[str, object]:
        return {
            "domain": self.domain.value,
            "direction": self.direction.value,
            "consequence": self.consequence,
            "severity": self.severity.value,
            "source_graph_ids": list(self.source_graph_ids),
            "hypothesis_ids": list(self.hypothesis_ids),
            "provisional": self.provisional,
        }


@dataclass(frozen=True, slots=True)
class BoundaryCandidate:
    candidate_id: str
    option_kind: BoundaryOptionKind
    status: AtomicityStatus
    recommendation: RecommendationDisposition
    consequence: str
    affected_specimen_ids: tuple[str, ...]
    shared_dimensions: tuple[ComparisonDimension, ...]
    differing_dimensions: tuple[ComparisonDimension, ...]
    configuration_sufficient: bool
    breaking_dimensions: tuple[ComparisonDimension, ...]
    evidence_gaps: tuple[str, ...]
    dimensions: tuple[DimensionAssessment, ...]
    risks: tuple[WrongBoundaryRisk, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "candidate_id": self.candidate_id,
            "option_kind": self.option_kind.value,
            "status": self.status.value,
            "recommendation": self.recommendation.value,
            "consequence": self.consequence,
            "affected_specimen_ids": list(self.affected_specimen_ids),
            "shared_dimensions": [item.value for item in self.shared_dimensions],
            "differing_dimensions": [item.value for item in self.differing_dimensions],
            "configuration_sufficient": self.configuration_sufficient,
            "breaking_dimensions": [item.value for item in self.breaking_dimensions],
            "evidence_gaps": list(self.evidence_gaps),
            "dimensions": [item.as_dict() for item in self.dimensions],
            "risks": [item.as_dict() for item in self.risks],
        }


@dataclass(frozen=True, slots=True)
class AtomicityComparisonPacket:
    packet_id: str
    series_id: str
    version: str
    category_id: str
    grammar_evidence: GrammarEvidenceReference
    candidates: tuple[BoundaryCandidate, ...]
    comparison_authority_ref: str
    artifact_sha256: str
    claim_policy_id: str = AUTHORITY_CLAIM_POLICY_ID
    claim_policy_version: str = AUTHORITY_CLAIM_POLICY_VERSION
    claim_policy_sha256: str = AUTHORITY_CLAIM_POLICY_SHA256
    knowledge_status: str = "PROVISIONAL_COMPARISON"
    decision_status: str = "UNRATIFIED"
    evidence_gate_status: str = "EVIDENCE_PENDING"
    human_decision_required: bool = True
    genesis_authorized: bool = False
    production_ready: bool = False
    certified: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "packet_id": self.packet_id,
            "series_id": self.series_id,
            "version": self.version,
            "category_id": self.category_id,
            "grammar_evidence": self.grammar_evidence.as_dict(),
            "candidates": [item.as_dict() for item in self.candidates],
            "comparison_authority_ref": self.comparison_authority_ref,
            "artifact_sha256": self.artifact_sha256,
            "claim_policy_id": self.claim_policy_id,
            "claim_policy_version": self.claim_policy_version,
            "claim_policy_sha256": self.claim_policy_sha256,
            "knowledge_status": self.knowledge_status,
            "decision_status": self.decision_status,
            "evidence_gate_status": self.evidence_gate_status,
            "human_decision_required": self.human_decision_required,
            "genesis_authorized": self.genesis_authorized,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class AtomicityComparisonReceipt:
    receipt_id: str
    run_id: str
    packet_id: str
    packet_version: str
    packet_artifact_sha256: str
    grammar_id: str
    grammar_artifact_sha256: str
    induction_receipt_sha256: str
    comparison_authority_ref: str
    candidate_count: int
    dimension_count_per_candidate: int
    outcome: str = "OUTCOME_VERIFIED_PROVISIONAL"
    failure_context: str = "NONE"
    event_name: str = "ST-02.04:ComparisonCompiled"
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
            "packet_id": self.packet_id,
            "packet_version": self.packet_version,
            "packet_artifact_sha256": self.packet_artifact_sha256,
            "grammar_id": self.grammar_id,
            "grammar_artifact_sha256": self.grammar_artifact_sha256,
            "induction_receipt_sha256": self.induction_receipt_sha256,
            "comparison_authority_ref": self.comparison_authority_ref,
            "candidate_count": self.candidate_count,
            "dimension_count_per_candidate": self.dimension_count_per_candidate,
            "outcome": self.outcome,
            "failure_context": self.failure_context,
        }


@dataclass(frozen=True, slots=True)
class AtomicityComparisonResult:
    packet: AtomicityComparisonPacket
    receipt: AtomicityComparisonReceipt

    def as_dict(self) -> dict[str, object]:
        return {"packet": self.packet.as_dict(), "receipt": self.receipt.as_dict()}


def validate_identifier_fields(candidate: BoundaryCandidate) -> None:
    """Validate identifiers close to the immutable contract boundary."""

    require_identifier(candidate.candidate_id, "atomicity_candidate_id")
    for specimen_id in candidate.affected_specimen_ids:
        require_identifier(specimen_id, "affected_specimen_id")
