"""Typed, syntax-only contracts for the ST-02.01 offline development mode.

These contracts deliberately distinguish measured structure from hypotheses.  They
contain no provider client and grant no semantic or production authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any, Mapping


_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@-]*$")


class SyntaxContractError(ValueError):
    code = "SyntaxContractError"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


class SourceEvidenceInvalid(SyntaxContractError):
    code = "SourceEvidenceInvalid"


class ProvenanceInvalid(SyntaxContractError):
    code = "ProvenanceInvalid"


class UnsupportedParserOutput(SyntaxContractError):
    code = "UnsupportedParserOutput"


class ProviderOnlyClaimRejected(SyntaxContractError):
    code = "ProviderOnlyClaimRejected"


class ObservationContaminated(SyntaxContractError):
    code = "ObservationContaminated"


class ObservationStatus(str, Enum):
    MEASURED = "MEASURED"
    DETERMINISTICALLY_DERIVED = "DETERMINISTICALLY_DERIVED"


class GovernedStatus(str, Enum):
    GOVERNED = "GOVERNED"
    GOVERNED_SYNTHETIC = "GOVERNED_SYNTHETIC"
    UNVERIFIED = "UNVERIFIED"


class KnowledgeStatus(str, Enum):
    OBSERVATION = "OBSERVATION"
    DETERMINISTIC_DERIVATION = "DETERMINISTIC_DERIVATION"
    HYPOTHESIS = "HYPOTHESIS"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceOrigin(str, Enum):
    DETERMINISTIC_CODE = "DETERMINISTIC_CODE"
    GOVERNED_HUMAN_ANNOTATION = "GOVERNED_HUMAN_ANNOTATION"
    PROVIDER_ONLY = "PROVIDER_ONLY"


class UncertaintyKind(str, Enum):
    EXACT = "EXACT"
    BOUNDED_MEASUREMENT = "BOUNDED_MEASUREMENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ApplicabilityStatus(str, Enum):
    APPLICABLE = "APPLICABLE"
    CONDITIONALLY_APPLICABLE = "CONDITIONALLY_APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


ALLOWED_STRUCTURAL_FIELDS = frozenset(
    {
        "frame_index",
        "slide_index",
        "start_ms",
        "end_ms",
        "mask_sha256",
        "text_content_sha256",
    }
)

SEMANTIC_CONTAMINATION_FIELDS = frozenset(
    {
        "why",
        "meaning",
        "intent",
        "semantic_intent",
        "desired_reaction",
        "desired_human_role",
        "activative_call",
        "activative_hypothesis",
        "identity_dna",
        "reaction_receipt",
        "expression_moment",
        "production_ready",
        "certified",
    }
)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def require_identifier(value: str, field: str) -> str:
    if not value or not _IDENTIFIER.fullmatch(value):
        raise SyntaxContractError(
            f"{field} must be a non-empty governed identifier.",
            field=field,
        )
    return value


def require_sha256(value: str, field: str) -> str:
    if not _SHA256.fullmatch(value):
        raise SyntaxContractError(
            f"{field} must be a lowercase SHA-256 digest.",
            field=field,
        )
    return value


@dataclass(frozen=True, slots=True)
class SourceReference:
    source_id: str
    version: str
    content_sha256: str
    authority_ref: str
    repository_owned: bool

    def __post_init__(self) -> None:
        require_identifier(self.source_id, "source_id")
        require_identifier(self.version, "source_version")
        require_sha256(self.content_sha256, "source_content_sha256")
        require_identifier(self.authority_ref, "source_authority_ref")
        if not self.repository_owned:
            raise SourceEvidenceInvalid(
                "The offline mode accepts repository-owned source fixtures only.",
                source_id=self.source_id,
            )

    def as_dict(self) -> dict[str, object]:
        return {
            "source_id": self.source_id,
            "version": self.version,
            "content_sha256": self.content_sha256,
            "authority_ref": self.authority_ref,
            "repository_owned": self.repository_owned,
        }


@dataclass(frozen=True, slots=True)
class ProvenanceReference:
    artifact_id: str
    artifact_sha256: str
    relationship: str

    def __post_init__(self) -> None:
        require_identifier(self.artifact_id, "provenance_artifact_id")
        require_sha256(self.artifact_sha256, "provenance_artifact_sha256")
        require_identifier(self.relationship, "provenance_relationship")

    def as_dict(self) -> dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_sha256": self.artifact_sha256,
            "relationship": self.relationship,
        }


@dataclass(frozen=True, slots=True)
class Uncertainty:
    kind: UncertaintyKind
    confidence_ppm: int
    rationale: str

    def __post_init__(self) -> None:
        if not 0 <= self.confidence_ppm <= 1_000_000:
            raise SyntaxContractError(
                "uncertainty confidence must be within zero and one million ppm"
            )
        if self.kind is UncertaintyKind.EXACT and self.confidence_ppm != 1_000_000:
            raise SyntaxContractError("exact observations require full confidence")
        if self.kind is UncertaintyKind.BOUNDED_MEASUREMENT and not (
            0 < self.confidence_ppm < 1_000_000
        ):
            raise SyntaxContractError(
                "bounded measurements require non-zero, non-exact confidence"
            )
        if self.kind is UncertaintyKind.NOT_APPLICABLE and self.confidence_ppm != 0:
            raise SyntaxContractError("not-applicable uncertainty must have zero confidence")
        if not self.rationale.strip():
            raise SyntaxContractError("uncertainty rationale is required")

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind.value,
            "confidence_ppm": self.confidence_ppm,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class Applicability:
    status: ApplicabilityStatus
    rationale: str

    def __post_init__(self) -> None:
        if not self.rationale.strip():
            raise SyntaxContractError("applicability rationale is required")

    def as_dict(self) -> dict[str, str]:
        return {"status": self.status.value, "rationale": self.rationale}


@dataclass(frozen=True, slots=True)
class OntologyTerm:
    term_id: str
    allowed_categories: tuple[str, ...]

    def __post_init__(self) -> None:
        require_identifier(self.term_id, "ontology_term_id")
        if not self.allowed_categories or len(set(self.allowed_categories)) != len(
            self.allowed_categories
        ):
            raise SyntaxContractError(
                "ontology terms require a non-empty, duplicate-free category set"
            )
        for category in self.allowed_categories:
            require_identifier(category, "ontology_allowed_category")

    def as_dict(self) -> dict[str, object]:
        return {
            "term_id": self.term_id,
            "allowed_categories": list(sorted(self.allowed_categories)),
        }


@dataclass(frozen=True, slots=True)
class SyntaxOntology:
    ontology_id: str
    version: str
    terms: tuple[OntologyTerm, ...]

    def __post_init__(self) -> None:
        require_identifier(self.ontology_id, "ontology_id")
        require_identifier(self.version, "ontology_version")
        if not self.terms:
            raise SyntaxContractError("syntax ontology requires at least one term")
        term_ids = tuple(term.term_id for term in self.terms)
        if len(term_ids) != len(set(term_ids)):
            raise SyntaxContractError("syntax ontology term identities must be unique")

    @property
    def ontology_sha256(self) -> str:
        return canonical_sha256(self.as_dict())

    def require_term(self, term_id: str, category_id: str) -> OntologyTerm:
        for term in self.terms:
            if term.term_id == term_id:
                if category_id not in term.allowed_categories:
                    raise UnsupportedParserOutput(
                        "ontology term is not legal for the specimen category",
                        term_id=term_id,
                        category_id=category_id,
                    )
                return term
        raise UnsupportedParserOutput(
            "parser output references an unknown ontology term",
            term_id=term_id,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "ontology_id": self.ontology_id,
            "version": self.version,
            "terms": [term.as_dict() for term in sorted(self.terms, key=lambda item: item.term_id)],
        }


def validate_structural_fields(
    fields: Mapping[str, str | int | bool],
) -> tuple[tuple[str, str | int | bool], ...]:
    normalized: list[tuple[str, str | int | bool]] = []
    for name, value in fields.items():
        canonical_name = name.strip().lower()
        if canonical_name in SEMANTIC_CONTAMINATION_FIELDS:
            raise ObservationContaminated(
                "syntax observation contains a semantic or authority claim",
                field=canonical_name,
            )
        if canonical_name not in ALLOWED_STRUCTURAL_FIELDS:
            raise UnsupportedParserOutput(
                "parser output contains an unsupported structural field",
                field=canonical_name,
            )
        if isinstance(value, str) and not value.strip():
            raise UnsupportedParserOutput(
                "parser structural fields cannot contain blank strings",
                field=canonical_name,
            )
        if not isinstance(value, (str, int, bool)):
            raise UnsupportedParserOutput(
                "parser structural field value has an unsupported type",
                field=canonical_name,
            )
        normalized.append((canonical_name, value))
    return tuple(sorted(normalized, key=lambda item: item[0]))
