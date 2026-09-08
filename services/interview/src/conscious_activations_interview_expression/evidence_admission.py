"""Fail-closed multi-dimensional evidence admission for CA-M017.

The admission boundary deliberately keeps quantitative thresholds separate from the
constitutional boolean dimensions defined by FR-EVID-001. A candidate is admitted
only when every declared gate passes. A high scalar confidence value can never
compensate for a failed corroboration, fidelity, epistemic, identity, or domain gate.

The module is intentionally self-contained so it can be adopted without changing
existing persistence or composition surfaces. Downstream callers must consume the
returned :class:`EvidenceAdmissionReceipt` through ``require_generation_admission``
(or an equivalent policy-aware guard) rather than inspecting the candidate directly.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any, Mapping

MANDATE_ID = "CA-M017"
INVARIANT_ID = "FR-EV-001"
POLICY_VERSION = "CA-M017-EVIDENCE-ADMISSION-V1"

# Thresholds are explicit, deterministic policy inputs. They are intentionally not
# combined into a weighted score: every threshold is an independent hard gate.
DEFAULT_MIN_ADMISSION_CONFIDENCE = 0.80
DEFAULT_MIN_CORROBORATION_COUNT = 2
DEFAULT_MIN_VERBATIM_FIDELITY = 0.95


class EvidenceType(str, Enum):
    MEDIA = "media"
    QUOTE = "quote"
    CLAIM = "claim"


class AdmissionState(str, Enum):
    ADMITTED = "ADMITTED"
    QUARANTINED = "QUARANTINED"


class EvidenceAdmissionError(RuntimeError):
    """Base error for the CA-M017 admission boundary."""

    code = "CA_M017_EVIDENCE_ADMISSION_ERROR"

    def __init__(self, message: str, *, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.context = dict(context or {})


class InvalidEvidenceCandidateError(EvidenceAdmissionError):
    """Raised when the admission boundary cannot establish required inputs."""

    code = "CA_M017_INVALID_CANDIDATE"


class EvidenceGenerationBlockedError(EvidenceAdmissionError):
    """Raised when quarantined or otherwise inadmissible evidence reaches generation."""

    code = "CA_M017_GENERATION_BLOCKED"


@dataclass(frozen=True, slots=True)
class EvidenceAdmissionPolicy:
    """Immutable hard-threshold policy for all CA-M017 evidence types."""

    min_admission_confidence: float = DEFAULT_MIN_ADMISSION_CONFIDENCE
    min_corroboration_count: int = DEFAULT_MIN_CORROBORATION_COUNT
    min_verbatim_fidelity: float = DEFAULT_MIN_VERBATIM_FIDELITY

    def __post_init__(self) -> None:
        if not _is_probability(self.min_admission_confidence):
            raise ValueError("min_admission_confidence must be a finite number between 0 and 1")
        if isinstance(self.min_corroboration_count, bool) or not isinstance(
            self.min_corroboration_count, int
        ):
            raise ValueError("min_corroboration_count must be an integer")
        if self.min_corroboration_count < 0:
            raise ValueError("min_corroboration_count must be >= 0")
        if not _is_probability(self.min_verbatim_fidelity):
            raise ValueError("min_verbatim_fidelity must be a finite number between 0 and 1")


@dataclass(frozen=True, slots=True)
class EvidenceCandidate:
    """Evidence proposed for admission at the authoritative boundary.

    The quantitative gates implement the user-facing CA-M017 acceptance contract:
    confidence, corroboration count, and verbatim fidelity. The three constitutional
    boolean dimensions remain explicit because FR-EVID-001 requires unanimous pass
    across fidelity, epistemic legality, identity fit, and domain fit.
    """

    evidence_id: str
    evidence_type: EvidenceType
    admission_confidence: float
    corroboration_count: int
    verbatim_fidelity: float
    fidelity_pass: bool
    epistemic_legality: bool
    identity_fit: bool
    domain_fit: bool
    source_ref: str
    downstream_generation_requested: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_id, str) or not self.evidence_id.strip():
            raise InvalidEvidenceCandidateError("evidence_id must be a non-empty string")
        if not isinstance(self.evidence_type, EvidenceType):
            try:
                object.__setattr__(self, "evidence_type", EvidenceType(self.evidence_type))
            except (TypeError, ValueError) as exc:
                raise InvalidEvidenceCandidateError(
                    "evidence_type must be one of media, quote, or claim"
                ) from exc
        if not _is_probability(self.admission_confidence):
            raise InvalidEvidenceCandidateError(
                "admission_confidence must be a finite number between 0 and 1"
            )
        if isinstance(self.corroboration_count, bool) or not isinstance(
            self.corroboration_count, int
        ):
            raise InvalidEvidenceCandidateError("corroboration_count must be an integer")
        if self.corroboration_count < 0:
            raise InvalidEvidenceCandidateError("corroboration_count must be >= 0")
        if not _is_probability(self.verbatim_fidelity):
            raise InvalidEvidenceCandidateError(
                "verbatim_fidelity must be a finite number between 0 and 1"
            )
        if not isinstance(self.fidelity_pass, bool):
            raise InvalidEvidenceCandidateError("fidelity_pass must be boolean")
        for name, value in (
            ("epistemic_legality", self.epistemic_legality),
            ("identity_fit", self.identity_fit),
            ("domain_fit", self.domain_fit),
        ):
            if not isinstance(value, bool):
                raise InvalidEvidenceCandidateError(f"{name} must be boolean")
        if not isinstance(self.source_ref, str) or not self.source_ref.strip():
            raise InvalidEvidenceCandidateError("source_ref must be a non-empty string")
        if not isinstance(self.downstream_generation_requested, bool):
            raise InvalidEvidenceCandidateError("downstream_generation_requested must be boolean")
        if not isinstance(self.metadata, Mapping):
            raise InvalidEvidenceCandidateError("metadata must be a mapping")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "EvidenceCandidate":
        """Build a candidate from a serialized boundary payload without defaults.

        Missing required gate inputs are rejected instead of silently defaulting to
        true or to a permissive score. This preserves the fail-closed invariant.
        """

        if not isinstance(value, Mapping):
            raise InvalidEvidenceCandidateError("evidence candidate must be a mapping")
        required = {
            "evidence_id",
            "evidence_type",
            "admission_confidence",
            "corroboration_count",
            "verbatim_fidelity",
            "fidelity_pass",
            "epistemic_legality",
            "identity_fit",
            "domain_fit",
            "source_ref",
        }
        missing = sorted(required.difference(value))
        if missing:
            raise InvalidEvidenceCandidateError(
                "missing required admission inputs",
                context={"missing_fields": missing},
            )
        return cls(
            evidence_id=value["evidence_id"],
            evidence_type=value["evidence_type"],
            admission_confidence=value["admission_confidence"],
            corroboration_count=value["corroboration_count"],
            verbatim_fidelity=value["verbatim_fidelity"],
            fidelity_pass=value["fidelity_pass"],
            epistemic_legality=value["epistemic_legality"],
            identity_fit=value["identity_fit"],
            domain_fit=value["domain_fit"],
            source_ref=value["source_ref"],
            downstream_generation_requested=value.get("downstream_generation_requested", False),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True, slots=True)
class EvidenceGateResult:
    """Auditable outcome of one hard admission gate."""

    passed: bool
    observed: Any
    required: Any
    reason_code: str | None


@dataclass(frozen=True, slots=True)
class EvidenceAdmissionReceipt:
    """Immutable, hash-addressable admission/quarantine receipt."""

    mandate_id: str
    invariant_id: str
    policy_version: str
    evidence_id: str
    evidence_type: EvidenceType
    state: AdmissionState
    admitted: bool
    downstream_generation_allowed: bool
    quarantine_reason_codes: tuple[str, ...]
    gates: Mapping[str, EvidenceGateResult]
    threshold_policy: EvidenceAdmissionPolicy
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "policy_version": self.policy_version,
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "state": self.state.value,
            "admitted": self.admitted,
            "downstream_generation_allowed": self.downstream_generation_allowed,
            "quarantine_reason_codes": list(self.quarantine_reason_codes),
            "gates": {
                name: {
                    "passed": gate.passed,
                    "observed": gate.observed,
                    "required": gate.required,
                    "reason_code": gate.reason_code,
                }
                for name, gate in self.gates.items()
            },
            "threshold_policy": {
                "min_admission_confidence": self.threshold_policy.min_admission_confidence,
                "min_corroboration_count": self.threshold_policy.min_corroboration_count,
                "min_verbatim_fidelity": self.threshold_policy.min_verbatim_fidelity,
            },
            "receipt_sha256": self.receipt_sha256,
        }


class EvidenceAdmissionBoundary:
    """Authoritative CA-M017 evidence admission/verifier boundary."""

    def __init__(self, policy: EvidenceAdmissionPolicy | None = None):
        self.policy = policy or EvidenceAdmissionPolicy()

    def admit(self, candidate: EvidenceCandidate | Mapping[str, Any]) -> EvidenceAdmissionReceipt:
        """Evaluate a candidate with unanimous hard gates and fail closed.

        This method is the intended runtime admission entry point. It never returns
        an admitted receipt when any declared gate fails. Rejected evidence is
        explicitly quarantined and marked ineligible for downstream generation.
        """

        normalized = (
            candidate
            if isinstance(candidate, EvidenceCandidate)
            else EvidenceCandidate.from_mapping(candidate)
        )

        gates = self._evaluate_gates(normalized)
        failures = tuple(
            gate.reason_code for gate in gates.values() if not gate.passed and gate.reason_code
        )
        admitted = not failures
        state = AdmissionState.ADMITTED if admitted else AdmissionState.QUARANTINED
        downstream_allowed = admitted and normalized.downstream_generation_requested

        if admitted:
            # Generation may be requested only after a successful admission receipt.
            downstream_allowed = normalized.downstream_generation_requested

        receipt_payload = {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "policy_version": POLICY_VERSION,
            "evidence_id": normalized.evidence_id,
            "evidence_type": normalized.evidence_type.value,
            "state": state.value,
            "admitted": admitted,
            "downstream_generation_allowed": downstream_allowed,
            "quarantine_reason_codes": list(failures),
            "gates": {
                name: {
                    "passed": gate.passed,
                    "observed": gate.observed,
                    "required": gate.required,
                    "reason_code": gate.reason_code,
                }
                for name, gate in gates.items()
            },
            "threshold_policy": {
                "min_admission_confidence": self.policy.min_admission_confidence,
                "min_corroboration_count": self.policy.min_corroboration_count,
                "min_verbatim_fidelity": self.policy.min_verbatim_fidelity,
            },
        }
        receipt_sha256 = _canonical_sha256(receipt_payload)
        return EvidenceAdmissionReceipt(
            mandate_id=MANDATE_ID,
            invariant_id=INVARIANT_ID,
            policy_version=POLICY_VERSION,
            evidence_id=normalized.evidence_id,
            evidence_type=normalized.evidence_type,
            state=state,
            admitted=admitted,
            downstream_generation_allowed=downstream_allowed,
            quarantine_reason_codes=failures,
            gates=gates,
            threshold_policy=self.policy,
            receipt_sha256=receipt_sha256,
        )

    def require_generation_admission(
        self, receipt: EvidenceAdmissionReceipt | Mapping[str, Any]
    ) -> None:
        """Refuse downstream generation unless admission is explicit and unanimous."""

        if not isinstance(receipt, EvidenceAdmissionReceipt):
            raise EvidenceGenerationBlockedError(
                "downstream generation requires an authoritative EvidenceAdmissionReceipt",
                context={"reason_code": "MISSING_AUTHORITATIVE_RECEIPT"},
            )
        if (
            receipt.mandate_id != MANDATE_ID
            or receipt.invariant_id != INVARIANT_ID
            or receipt.policy_version != POLICY_VERSION
        ):
            raise EvidenceGenerationBlockedError(
                "receipt is not an authoritative CA-M017 admission receipt",
                context={"reason_code": "INVALID_ADMISSION_RECEIPT"},
            )
        if not receipt.admitted or receipt.state is not AdmissionState.ADMITTED:
            raise EvidenceGenerationBlockedError(
                "evidence is quarantined and barred from downstream generation",
                context={
                    "reason_code": "QUARANTINED_EVIDENCE",
                    "evidence_id": receipt.evidence_id,
                    "quarantine_reason_codes": list(receipt.quarantine_reason_codes),
                },
            )

    def admit_for_generation(
        self, candidate: EvidenceCandidate | Mapping[str, Any]
    ) -> EvidenceAdmissionReceipt:
        """Admit and immediately enforce the downstream-generation barrier."""

        receipt = self.admit(candidate)
        self.require_generation_admission(receipt)
        return receipt

    def _evaluate_gates(self, candidate: EvidenceCandidate) -> dict[str, EvidenceGateResult]:
        return {
            "confidence": _threshold_gate(
                candidate.admission_confidence,
                self.policy.min_admission_confidence,
                "BELOW_MINIMUM_ADMISSION_CONFIDENCE",
            ),
            "corroboration": _threshold_gate(
                candidate.corroboration_count,
                self.policy.min_corroboration_count,
                "INSUFFICIENT_CORROBORATION",
            ),
            "verbatim_fidelity": _threshold_gate(
                candidate.verbatim_fidelity,
                self.policy.min_verbatim_fidelity,
                "BELOW_MINIMUM_VERBATIM_FIDELITY",
            ),
            "fidelity": _boolean_gate(
                candidate.fidelity_pass,
                "FIDELITY_GATE_FAILED",
            ),
            "epistemic_legality": _boolean_gate(
                candidate.epistemic_legality,
                "EPISTEMIC_LEGALITY_GATE_FAILED",
            ),
            "identity_fit": _boolean_gate(
                candidate.identity_fit,
                "IDENTITY_FIT_GATE_FAILED",
            ),
            "domain_fit": _boolean_gate(
                candidate.domain_fit,
                "DOMAIN_FIT_GATE_FAILED",
            ),
        }


def admit_evidence(
    candidate: EvidenceCandidate | Mapping[str, Any],
    *,
    policy: EvidenceAdmissionPolicy | None = None,
) -> EvidenceAdmissionReceipt:
    """Convenience entry point for the authoritative CA-M017 boundary."""

    return EvidenceAdmissionBoundary(policy).admit(candidate)


def require_generation_admission(receipt: EvidenceAdmissionReceipt) -> None:
    """Module-level downstream generation barrier."""

    EvidenceAdmissionBoundary().require_generation_admission(receipt)


def _threshold_gate(observed: Any, required: Any, failure_code: str) -> EvidenceGateResult:
    passed = observed >= required
    return EvidenceGateResult(
        passed=passed,
        observed=observed,
        required=required,
        reason_code=None if passed else failure_code,
    )


def _boolean_gate(observed: bool, failure_code: str) -> EvidenceGateResult:
    return EvidenceGateResult(
        passed=observed,
        observed=observed,
        required=True,
        reason_code=None if observed else failure_code,
    )


def _is_probability(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value) and 0.0 <= value <= 1.0


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
