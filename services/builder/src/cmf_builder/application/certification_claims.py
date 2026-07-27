"""Bounded certification-claim governance for OD-AM-005 / ST-12.04."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Mapping


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class ClaimError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class ClaimClass(str, Enum):
    IMPLEMENTATION_COMPLETE = "IMPLEMENTATION_COMPLETE"
    DEVELOPMENT_VALIDATED = "DEVELOPMENT_VALIDATED"
    EMPIRICALLY_VALIDATED = "EMPIRICALLY_VALIDATED"
    EXTERNAL_INTEGRATION_VALIDATED = "EXTERNAL_INTEGRATION_VALIDATED"
    PRODUCTION_READY = "PRODUCTION_READY"
    CERTIFIED = "CERTIFIED"
    NOT_CERTIFIED = "NOT_CERTIFIED"
    LIMITED_SCOPE = "LIMITED_SCOPE"


MATURITY_ORDER = {
    "offline_implementation": 1,
    "development_validated": 2,
    "empirically_validated": 3,
    "external_integration_validated": 4,
    "production_ready": 5,
    "certified": 6,
}


@dataclass(frozen=True)
class CertificationClaim:
    claim_identity: str
    claim_class: ClaimClass
    subject_identity: str
    requested_scope: str
    supported_scope: str
    prohibited_scope: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    supplied_evidence: tuple[str, ...]
    missing_evidence: tuple[str, ...]
    authority_requirement: str
    maturity_requirement: str
    supplied_maturity: str
    production_requirement: bool
    certification_requirement: bool
    decision: str
    limitations: tuple[str, ...]
    expiration: str
    invalidation: str

    def __post_init__(self) -> None:
        if self.claim_class in {ClaimClass.PRODUCTION_READY, ClaimClass.CERTIFIED} and self.decision == "SUPPORTED":
            raise ClaimError("PRODUCTION_OR_CERTIFICATION_CLAIM_UNSUPPORTED", "production/certification claims are not supported by offline implementation")
        if self.missing_evidence and self.decision == "SUPPORTED":
            raise ClaimError("MISSING_EVIDENCE_CANNOT_SUPPORT_CLAIM", "missing evidence must remain explicit")
        if MATURITY_ORDER[self.supplied_maturity] < MATURITY_ORDER[self.maturity_requirement] and self.decision == "SUPPORTED":
            raise ClaimError("LOWER_MATURITY_CANNOT_SUPPORT_HIGHER_CLAIM", "lower maturity cannot support higher claim")
        if "agent_human_authority" in self.supplied_evidence:
            raise ClaimError("AGENT_PROPOSAL_NOT_HUMAN_AUTHORITY", "agent proposals cannot provide human authority")
        if self.invalidation == "INVALIDATED" and self.decision == "SUPPORTED":
            raise ClaimError("INVALIDATED_EVIDENCE_CANNOT_SUPPORT_CLAIM", "invalidated evidence cannot support a claim")

    @property
    def receipt_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "claim_identity": self.claim_identity,
            "claim_class": self.claim_class.value,
            "subject_identity": self.subject_identity,
            "requested_scope": self.requested_scope,
            "supported_scope": self.supported_scope,
            "prohibited_scope": list(self.prohibited_scope),
            "evidence_requirements": list(self.evidence_requirements),
            "supplied_evidence": list(self.supplied_evidence),
            "missing_evidence": list(self.missing_evidence),
            "authority_requirement": self.authority_requirement,
            "maturity_requirement": self.maturity_requirement,
            "supplied_maturity": self.supplied_maturity,
            "production_requirement": self.production_requirement,
            "certification_requirement": self.certification_requirement,
            "decision": self.decision,
            "limitations": list(self.limitations),
            "expiration": self.expiration,
            "invalidation": self.invalidation,
        }


def derive_offline_implementation_claim(receipts: Mapping[str, str], *, total_confirmed_stories: int, open_gates: tuple[str, ...]) -> CertificationClaim:
    implemented = sum(1 for verdict in receipts.values() if verdict == "IMPLEMENTED_DEVELOPMENT_PASS")
    missing = () if implemented == total_confirmed_stories else ("remaining_implementation_receipts",)
    return CertificationClaim(
        claim_identity=f"offline-implementation:{implemented}-of-{total_confirmed_stories}",
        claim_class=ClaimClass.IMPLEMENTATION_COMPLETE if not missing else ClaimClass.LIMITED_SCOPE,
        subject_identity="Atomic Harness Builder",
        requested_scope="offline_development_implementation",
        supported_scope=f"{implemented}/{total_confirmed_stories}",
        prohibited_scope=("production_ready", "certified", "external_integration_validated"),
        evidence_requirements=("implementation_receipts",),
        supplied_evidence=tuple(sorted(receipts)),
        missing_evidence=missing + open_gates,
        authority_requirement="OD-AM-005",
        maturity_requirement="offline_implementation",
        supplied_maturity="offline_implementation",
        production_requirement=False,
        certification_requirement=False,
        decision="LIMITED_SUPPORTED" if open_gates else ("SUPPORTED" if not missing else "UNSUPPORTED"),
        limitations=("full_evidence_closure_remains_evidence_driven", "production_ready_false", "certified_false"),
        expiration="superseded_by_new_receipt_index",
        invalidation="ACTIVE",
    )
