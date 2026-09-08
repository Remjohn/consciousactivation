"""
CA-M022 — Adaptive Elicitation & Missing-Unit Resilience
Requirement: FR-022 / FR-ELIC-002

Interview completion is evaluated on holistic narrative yield sufficiency,
not 100% linear script execution (Canon Q22).

Design invariants enforced by this module
==========================================
1. A session MAY succeed when one or more planned elicitation units are omitted,
   PROVIDED overall yield criteria are satisfied.
2. Omitted units must NEVER disappear from the completion record; omission is
   always visible.
3. When overall yield criteria are NOT met, the evaluation FAILS CLOSED even
   when every executed unit returned a non-null response.
4. Remediation follow-up prompts are injected without breaking conversational
   coherence or constitution boundaries. They are suggestions only — the
   canonical authority surface (Operator / live session) decides whether to
   dispatch them.
5. This module does NOT implement full portfolio yield gating (Q23) or
   authorization policy (Q24); those are separate mandates.

Authoritative surface
=====================
``AdaptiveElicitationEvaluator.evaluate`` is the single runtime boundary for
holistic yield-sufficiency checking.  Callers must not inspect completion
records directly to decide whether a session succeeded.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from math import isfinite
from typing import Any, Mapping, Sequence

MANDATE_ID = "CA-M022"
INVARIANT_ID = "FR-ELIC-002"
POLICY_VERSION = "CA-M022-ADAPTIVE-ELICITATION-V1"

# ---------------------------------------------------------------------------
# Statistical significance thresholds — these are explicit, hard policy inputs.
# They are intentionally NOT combined into a weighted score.  Each gate is an
# independent hard gate, consistent with the pattern established by CA-M017.
# ---------------------------------------------------------------------------

#: Minimum holistic yield ratio (admitted evidence / total planned evidence).
DEFAULT_MIN_HOLISTIC_YIELD_RATIO: float = 0.70

#: Minimum mean tension score across executed units.
DEFAULT_MIN_TENSION_SCORE: float = 0.40

#: Minimum evidence count across the entire session for significance.
DEFAULT_MIN_EVIDENCE_COUNT: int = 1

#: Maximum fraction of planned units that may be omitted and still allow
#: the session to pass yield evaluation.
DEFAULT_MAX_OMISSION_RATE: float = 0.50


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class UnitStatus(str, Enum):
    """Execution status of a single planned elicitation unit."""

    EXECUTED = "EXECUTED"
    OMITTED = "OMITTED"
    PARTIAL = "PARTIAL"


class YieldEvaluationOutcome(str, Enum):
    """Holistic yield evaluation outcome at the authoritative boundary."""

    PASSED = "PASSED"
    FAILED_INSUFFICIENT_YIELD = "FAILED_INSUFFICIENT_YIELD"
    FAILED_BELOW_TENSION_THRESHOLD = "FAILED_BELOW_TENSION_THRESHOLD"
    FAILED_BELOW_EVIDENCE_MINIMUM = "FAILED_BELOW_EVIDENCE_MINIMUM"
    FAILED_OMISSION_RATE_EXCEEDED = "FAILED_OMISSION_RATE_EXCEEDED"


class RemediationKind(str, Enum):
    """Category of injected remediation prompt."""

    DEEPEN = "DEEPEN"        # Escalate specificity on a low-tension unit
    REACTIVATE = "REACTIVATE"  # Revisit an omitted unit conversationally
    CLARIFY = "CLARIFY"      # Request clarification on ambiguous evidence
    BRIDGE = "BRIDGE"        # Conversational bridge to restore coherence


# ---------------------------------------------------------------------------
# Error hierarchy
# ---------------------------------------------------------------------------


class AdaptiveRemediationError(RuntimeError):
    """Base class for CA-M022 boundary errors."""

    code = "CA_M022_ERROR"

    def __init__(self, message: str, *, context: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.context: dict[str, Any] = dict(context or {})


class InvalidUnitRecordError(AdaptiveRemediationError):
    """Raised when a unit record fails input validation."""

    code = "CA_M022_INVALID_UNIT_RECORD"


class YieldEvaluationBlockedError(AdaptiveRemediationError):
    """Raised when holistic yield evaluation cannot be completed."""

    code = "CA_M022_YIELD_EVALUATION_BLOCKED"


class YieldCriteriaNotMetError(AdaptiveRemediationError):
    """Raised (fail-closed) when session yield criteria are not satisfied."""

    code = "CA_M022_YIELD_CRITERIA_NOT_MET"


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ElicitationUnitRecord:
    """Record of a single planned elicitation unit's execution outcome.

    Parameters
    ----------
    unit_id:
        Non-empty string uniquely identifying the planned unit.
    status:
        Execution status — EXECUTED, OMITTED, or PARTIAL.
    tension_score:
        Observed tension score for this unit (0.0–1.0). Must be 0.0 when
        the unit is OMITTED. Reflects the degree of productive disagreement
        or evidence pressure elicited by the unit.
    evidence_count:
        Number of admitted evidence items yielded by this unit. Must be 0
        when the unit is OMITTED.
    omission_reason:
        Non-empty reason string when status is OMITTED; empty string
        otherwise. Omitted units MUST carry a reason so omission remains
        visible in the completion record.
    """

    unit_id: str
    status: UnitStatus
    tension_score: float
    evidence_count: int
    omission_reason: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.unit_id, str) or not self.unit_id.strip():
            raise InvalidUnitRecordError("unit_id must be a non-empty string")

        if not isinstance(self.status, UnitStatus):
            try:
                object.__setattr__(self, "status", UnitStatus(self.status))
            except (TypeError, ValueError) as exc:
                raise InvalidUnitRecordError(
                    f"status must be one of {[s.value for s in UnitStatus]}"
                ) from exc

        if not _is_score(self.tension_score):
            raise InvalidUnitRecordError(
                "tension_score must be a finite number between 0.0 and 1.0"
            )

        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise InvalidUnitRecordError("evidence_count must be an integer")
        if self.evidence_count < 0:
            raise InvalidUnitRecordError("evidence_count must be >= 0")

        if self.status is UnitStatus.OMITTED:
            if self.tension_score != 0.0:
                raise InvalidUnitRecordError(
                    "OMITTED unit must carry tension_score of 0.0"
                )
            if self.evidence_count != 0:
                raise InvalidUnitRecordError(
                    "OMITTED unit must carry evidence_count of 0"
                )
            if not isinstance(self.omission_reason, str) or not self.omission_reason.strip():
                raise InvalidUnitRecordError(
                    "OMITTED unit must carry a non-empty omission_reason"
                )
        else:
            if not isinstance(self.omission_reason, str):
                raise InvalidUnitRecordError(
                    "omission_reason must be a string (empty for non-OMITTED units)"
                )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ElicitationUnitRecord":
        """Construct from a serialised mapping, rejecting missing required fields."""
        if not isinstance(value, Mapping):
            raise InvalidUnitRecordError("unit record must be a mapping")
        required = {"unit_id", "status", "tension_score", "evidence_count"}
        missing = sorted(required.difference(value))
        if missing:
            raise InvalidUnitRecordError(
                "missing required unit record fields",
                context={"missing_fields": missing},
            )
        return cls(
            unit_id=value["unit_id"],
            status=value["status"],
            tension_score=value["tension_score"],
            evidence_count=value["evidence_count"],
            omission_reason=value.get("omission_reason", ""),
        )


@dataclass(frozen=True, slots=True)
class YieldSufficiencyPolicy:
    """Immutable hard-threshold policy for holistic yield evaluation.

    All thresholds are independent gates.  Exceeding one threshold cannot
    compensate for failing another.
    """

    min_holistic_yield_ratio: float = DEFAULT_MIN_HOLISTIC_YIELD_RATIO
    min_tension_score: float = DEFAULT_MIN_TENSION_SCORE
    min_evidence_count: int = DEFAULT_MIN_EVIDENCE_COUNT
    max_omission_rate: float = DEFAULT_MAX_OMISSION_RATE

    def __post_init__(self) -> None:
        for name, value in (
            ("min_holistic_yield_ratio", self.min_holistic_yield_ratio),
            ("min_tension_score", self.min_tension_score),
            ("max_omission_rate", self.max_omission_rate),
        ):
            if not _is_score(value):
                raise ValueError(f"{name} must be a finite number between 0.0 and 1.0")

        if (
            isinstance(self.min_evidence_count, bool)
            or not isinstance(self.min_evidence_count, int)
        ):
            raise ValueError("min_evidence_count must be an integer")
        if self.min_evidence_count < 0:
            raise ValueError("min_evidence_count must be >= 0")


@dataclass(frozen=True, slots=True)
class UnitGateResult:
    """Auditable outcome for a single unit-level metric gate."""

    passed: bool
    observed: Any
    required: Any
    reason_code: str | None


@dataclass(frozen=True, slots=True)
class OmittedUnitRecord:
    """Immutable record of a single omitted unit, preserved in completion evidence."""

    unit_id: str
    omission_reason: str


@dataclass(frozen=True, slots=True)
class RemediationPrompt:
    """A targeted follow-up prompt injected by the remediation engine.

    This is a *suggestion* — authority remains with the Operator/session.
    The prompt is constitutionally bounded: it cannot instruct fabrication
    or violate the subject's voice constitution.
    """

    prompt_id: str
    kind: RemediationKind
    target_unit_id: str
    suggested_expression: str
    constitutional_check_passed: bool
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "prompt_id": self.prompt_id,
            "kind": self.kind.value,
            "target_unit_id": self.target_unit_id,
            "suggested_expression": self.suggested_expression,
            "constitutional_check_passed": self.constitutional_check_passed,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class YieldEvaluationReceipt:
    """Immutable, hash-addressable yield evaluation receipt.

    This is the authoritative completion record for FR-ELIC-002.  It is the
    ONLY object callers should inspect to determine session success.
    """

    mandate_id: str
    invariant_id: str
    policy_version: str
    session_id: str
    outcome: YieldEvaluationOutcome
    passed: bool
    total_planned_units: int
    executed_unit_count: int
    omitted_unit_count: int
    partial_unit_count: int
    holistic_yield_ratio: float
    mean_tension_score: float
    total_evidence_count: int
    omission_rate: float
    omitted_units: tuple[OmittedUnitRecord, ...]
    gates: Mapping[str, UnitGateResult]
    policy: YieldSufficiencyPolicy
    remediation_prompts: tuple[RemediationPrompt, ...]
    limitations: tuple[str, ...]
    receipt_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "mandate_id": self.mandate_id,
            "invariant_id": self.invariant_id,
            "policy_version": self.policy_version,
            "session_id": self.session_id,
            "outcome": self.outcome.value,
            "passed": self.passed,
            "total_planned_units": self.total_planned_units,
            "executed_unit_count": self.executed_unit_count,
            "omitted_unit_count": self.omitted_unit_count,
            "partial_unit_count": self.partial_unit_count,
            "holistic_yield_ratio": self.holistic_yield_ratio,
            "mean_tension_score": self.mean_tension_score,
            "total_evidence_count": self.total_evidence_count,
            "omission_rate": self.omission_rate,
            "omitted_units": [
                {"unit_id": ou.unit_id, "omission_reason": ou.omission_reason}
                for ou in self.omitted_units
            ],
            "gates": {
                name: {
                    "passed": g.passed,
                    "observed": g.observed,
                    "required": g.required,
                    "reason_code": g.reason_code,
                }
                for name, g in self.gates.items()
            },
            "policy": {
                "min_holistic_yield_ratio": self.policy.min_holistic_yield_ratio,
                "min_tension_score": self.policy.min_tension_score,
                "min_evidence_count": self.policy.min_evidence_count,
                "max_omission_rate": self.policy.max_omission_rate,
            },
            "remediation_prompts": [p.to_dict() for p in self.remediation_prompts],
            "limitations": list(self.limitations),
            "receipt_sha256": self.receipt_sha256,
        }


# ---------------------------------------------------------------------------
# Remediation prompt generator
# ---------------------------------------------------------------------------


class RemediationPromptGenerator:
    """Generates constitutionally-bounded follow-up prompts for failing units.

    Constitution boundaries enforced:
    - Prompts must not assert facts not in the session record.
    - Prompts must not violate conversational coherence (must be contextually
      plausible follow-ups, not abrupt subject changes).
    - Prompts must not attempt to elicit content outside the declared scope.
    - All generated prompts are flagged with ``constitutional_check_passed``
      so callers can verify the boundary was applied.
    """

    # Prompt templates indexed by RemediationKind.
    # Templates use {unit_id} as the only interpolation placeholder so that
    # no user data is structurally embedded in a way that could fabricate facts.
    _TEMPLATES: dict[RemediationKind, str] = {
        RemediationKind.DEEPEN: (
            "I want to make sure I fully understand your perspective on {unit_id}. "
            "Could you tell me a bit more about what that was like for you?"
        ),
        RemediationKind.REACTIVATE: (
            "We touched on a number of areas today. I'd like to come back to {unit_id} "
            "for a moment — is there anything there you haven't had a chance to share?"
        ),
        RemediationKind.CLARIFY: (
            "Just to make sure I'm understanding correctly — when you mentioned {unit_id}, "
            "could you say more about what you mean by that?"
        ),
        RemediationKind.BRIDGE: (
            "Before we continue, I want to circle back briefly to {unit_id} "
            "so we don't lose the thread of what you were saying."
        ),
    }

    def generate(
        self,
        unit: ElicitationUnitRecord,
        *,
        kind: RemediationKind,
    ) -> RemediationPrompt:
        """Generate a single constitutionally-bounded remediation prompt.

        Parameters
        ----------
        unit:
            The unit whose yield or tension is below threshold.
        kind:
            The category of remediation to apply.

        Returns
        -------
        RemediationPrompt
            A bounded, reviewable follow-up suggestion.
        """
        template = self._TEMPLATES[kind]
        expression = template.format(unit_id=unit.unit_id)

        # Constitutional check: verify the generated expression does not
        # contain fabricated fact markers. This is a structural check —
        # the expression is generated from templates that do not embed
        # factual claims, so the check is definitionally satisfied for all
        # template-derived prompts.  Future extensions that introduce
        # data interpolation must re-evaluate this predicate.
        constitutional_ok = self._constitutional_check(expression)

        prompt_id = _short_sha256(
            {"unit_id": unit.unit_id, "kind": kind.value, "expression": expression}
        )

        return RemediationPrompt(
            prompt_id=f"rem:{prompt_id}",
            kind=kind,
            target_unit_id=unit.unit_id,
            suggested_expression=expression,
            constitutional_check_passed=constitutional_ok,
            rationale=(
                f"Unit '{unit.unit_id}' {unit.status.value.lower()} with "
                f"tension_score={unit.tension_score:.2f} and "
                f"evidence_count={unit.evidence_count}. "
                f"Remediation kind: {kind.value}."
            ),
        )

    @staticmethod
    def _constitutional_check(expression: str) -> bool:
        """Return True when the expression satisfies constitution boundaries.

        Current rules:
        - Expression must be a non-empty string.
        - Expression must not embed fabrication markers (hard-coded sentinel set).
        - Expression must not exceed a reasonable length (prevent runaway prompts).
        """
        if not isinstance(expression, str) or not expression.strip():
            return False
        _FABRICATION_MARKERS = frozenset(
            {"[FABRICATED]", "[INVENTED]", "[HALLUCINATION]", "ASSERT_FALSE"}
        )
        if any(marker in expression for marker in _FABRICATION_MARKERS):
            return False
        # Coherence bound: prompt must be conversationally reasonable length
        if len(expression) > 500:
            return False
        return True


# ---------------------------------------------------------------------------
# Authoritative evaluator (runtime boundary)
# ---------------------------------------------------------------------------


class AdaptiveElicitationEvaluator:
    """Authoritative CA-M022 holistic yield-sufficiency evaluator.

    This is the single runtime boundary for FR-ELIC-002.  Callers must use
    ``evaluate`` rather than inspecting unit records directly.

    Evaluation rules
    ----------------
    1. Compute holistic yield ratio = (executed + partial) / total planned.
    2. Compute mean tension score across executed + partial units.
    3. Count total evidence across all units.
    4. Compute omission rate = omitted / total planned.
    5. Apply each gate independently.  A session passes ONLY when all four
       gates pass.
    6. When any gate fails, inject targeted remediation prompts for the
       failing units and return the receipt with ``passed=False``.
    7. The omitted_units list is ALWAYS populated, even on a passing session,
       so omissions remain visible.
    """

    def __init__(
        self,
        policy: YieldSufficiencyPolicy | None = None,
        prompt_generator: RemediationPromptGenerator | None = None,
    ) -> None:
        self.policy = policy or YieldSufficiencyPolicy()
        self._prompt_generator = prompt_generator or RemediationPromptGenerator()

    def evaluate(
        self,
        session_id: str,
        units: Sequence[ElicitationUnitRecord | Mapping[str, Any]],
        *,
        limitations: Sequence[str] = (),
    ) -> YieldEvaluationReceipt:
        """Evaluate holistic yield sufficiency for a session.

        Parameters
        ----------
        session_id:
            Non-empty string identifying the interview session.
        units:
            Sequence of unit records (dataclass or mapping) for all planned
            elicitation units.  An empty sequence fails the evidence-minimum
            gate unless min_evidence_count is 0.
        limitations:
            Optional list of pre-recorded limitation strings.

        Returns
        -------
        YieldEvaluationReceipt
            Immutable, hash-addressable receipt.  ``passed`` is True only
            when all gates pass.

        Raises
        ------
        YieldEvaluationBlockedError
            When the evaluation cannot be performed (e.g. invalid session_id).
        InvalidUnitRecordError
            When any unit record fails validation.
        """
        if not isinstance(session_id, str) or not session_id.strip():
            raise YieldEvaluationBlockedError(
                "session_id must be a non-empty string",
                context={"reason_code": "INVALID_SESSION_ID"},
            )

        # Normalise unit records — raises InvalidUnitRecordError on bad input
        normalised: list[ElicitationUnitRecord] = [
            u if isinstance(u, ElicitationUnitRecord) else ElicitationUnitRecord.from_mapping(u)
            for u in units
        ]

        total_planned = len(normalised)
        executed = [u for u in normalised if u.status is UnitStatus.EXECUTED]
        omitted = [u for u in normalised if u.status is UnitStatus.OMITTED]
        partial = [u for u in normalised if u.status is UnitStatus.PARTIAL]

        executed_count = len(executed)
        omitted_count = len(omitted)
        partial_count = len(partial)

        # Compute holistic yield ratio
        active_count = executed_count + partial_count
        holistic_yield_ratio = (active_count / total_planned) if total_planned > 0 else 0.0

        # Compute mean tension score across executed + partial units
        active_units = executed + partial
        mean_tension = (
            sum(u.tension_score for u in active_units) / active_count
            if active_count > 0
            else 0.0
        )

        # Compute total evidence count across all units
        total_evidence = sum(u.evidence_count for u in normalised)

        # Compute omission rate
        omission_rate = (omitted_count / total_planned) if total_planned > 0 else 0.0

        # Evaluate gates
        gates = self._evaluate_gates(
            holistic_yield_ratio=holistic_yield_ratio,
            mean_tension=mean_tension,
            total_evidence=total_evidence,
            omission_rate=omission_rate,
        )

        failures = [
            gate.reason_code for gate in gates.values()
            if not gate.passed and gate.reason_code
        ]

        passed = not failures
        outcome = self._derive_outcome(failures)

        # Build omitted-unit visibility records (always, even on pass)
        omitted_records = tuple(
            OmittedUnitRecord(unit_id=u.unit_id, omission_reason=u.omission_reason)
            for u in omitted
        )

        # Inject remediation prompts when session has not fully passed
        prompts: tuple[RemediationPrompt, ...] = ()
        if not passed:
            prompts = self._generate_remediation_prompts(normalised, failures)

        effective_limitations = [str(lim) for lim in limitations]

        receipt_payload: dict[str, Any] = {
            "mandate_id": MANDATE_ID,
            "invariant_id": INVARIANT_ID,
            "policy_version": POLICY_VERSION,
            "session_id": session_id,
            "outcome": outcome.value,
            "passed": passed,
            "total_planned_units": total_planned,
            "executed_unit_count": executed_count,
            "omitted_unit_count": omitted_count,
            "partial_unit_count": partial_count,
            "holistic_yield_ratio": holistic_yield_ratio,
            "mean_tension_score": mean_tension,
            "total_evidence_count": total_evidence,
            "omission_rate": omission_rate,
            "omitted_units": [
                {"unit_id": ou.unit_id, "omission_reason": ou.omission_reason}
                for ou in omitted_records
            ],
            "gates": {
                name: {
                    "passed": g.passed,
                    "observed": g.observed,
                    "required": g.required,
                    "reason_code": g.reason_code,
                }
                for name, g in gates.items()
            },
            "policy": {
                "min_holistic_yield_ratio": self.policy.min_holistic_yield_ratio,
                "min_tension_score": self.policy.min_tension_score,
                "min_evidence_count": self.policy.min_evidence_count,
                "max_omission_rate": self.policy.max_omission_rate,
            },
            "limitations": effective_limitations,
        }
        receipt_sha256 = _canonical_sha256(receipt_payload)

        return YieldEvaluationReceipt(
            mandate_id=MANDATE_ID,
            invariant_id=INVARIANT_ID,
            policy_version=POLICY_VERSION,
            session_id=session_id,
            outcome=outcome,
            passed=passed,
            total_planned_units=total_planned,
            executed_unit_count=executed_count,
            omitted_unit_count=omitted_count,
            partial_unit_count=partial_count,
            holistic_yield_ratio=holistic_yield_ratio,
            mean_tension_score=mean_tension,
            total_evidence_count=total_evidence,
            omission_rate=omission_rate,
            omitted_units=omitted_records,
            gates=gates,
            policy=self.policy,
            remediation_prompts=prompts,
            limitations=tuple(effective_limitations),
            receipt_sha256=receipt_sha256,
        )

    def require_session_passed(self, receipt: YieldEvaluationReceipt) -> None:
        """Enforce fail-closed: raise if the session did not satisfy yield criteria.

        This is the downstream gate guard.  Callers that must not proceed on
        a failed session call this method instead of reading ``receipt.passed``
        directly.

        Raises
        ------
        YieldCriteriaNotMetError
            When the session did not pass holistic yield evaluation.
        """
        if not isinstance(receipt, YieldEvaluationReceipt):
            raise YieldCriteriaNotMetError(
                "require_session_passed requires an authoritative YieldEvaluationReceipt",
                context={"reason_code": "MISSING_AUTHORITATIVE_RECEIPT"},
            )
        if (
            receipt.mandate_id != MANDATE_ID
            or receipt.invariant_id != INVARIANT_ID
            or receipt.policy_version != POLICY_VERSION
        ):
            raise YieldCriteriaNotMetError(
                "receipt is not an authoritative CA-M022 yield evaluation receipt",
                context={"reason_code": "INVALID_YIELD_RECEIPT"},
            )
        if not receipt.passed:
            raise YieldCriteriaNotMetError(
                "session did not satisfy holistic yield criteria — downstream blocked",
                context={
                    "reason_code": "YIELD_CRITERIA_NOT_MET",
                    "session_id": receipt.session_id,
                    "outcome": receipt.outcome.value,
                    "holistic_yield_ratio": receipt.holistic_yield_ratio,
                    "mean_tension_score": receipt.mean_tension_score,
                    "omission_rate": receipt.omission_rate,
                    "omitted_unit_ids": [ou.unit_id for ou in receipt.omitted_units],
                },
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _evaluate_gates(
        self,
        *,
        holistic_yield_ratio: float,
        mean_tension: float,
        total_evidence: int,
        omission_rate: float,
    ) -> dict[str, UnitGateResult]:
        return {
            "holistic_yield_ratio": _threshold_gate(
                holistic_yield_ratio,
                self.policy.min_holistic_yield_ratio,
                "BELOW_MIN_HOLISTIC_YIELD_RATIO",
            ),
            "mean_tension_score": _threshold_gate(
                mean_tension,
                self.policy.min_tension_score,
                "BELOW_MIN_TENSION_SCORE",
            ),
            "evidence_count": _count_gate(
                total_evidence,
                self.policy.min_evidence_count,
                "BELOW_MIN_EVIDENCE_COUNT",
            ),
            "omission_rate": _ceiling_gate(
                omission_rate,
                self.policy.max_omission_rate,
                "OMISSION_RATE_EXCEEDED",
            ),
        }

    @staticmethod
    def _derive_outcome(failures: list[str]) -> YieldEvaluationOutcome:
        if not failures:
            return YieldEvaluationOutcome.PASSED
        # Return the most specific failure (first failure wins for diagnosis)
        _reason_to_outcome: dict[str, YieldEvaluationOutcome] = {
            "BELOW_MIN_HOLISTIC_YIELD_RATIO": YieldEvaluationOutcome.FAILED_INSUFFICIENT_YIELD,
            "BELOW_MIN_TENSION_SCORE": YieldEvaluationOutcome.FAILED_BELOW_TENSION_THRESHOLD,
            "BELOW_MIN_EVIDENCE_COUNT": YieldEvaluationOutcome.FAILED_BELOW_EVIDENCE_MINIMUM,
            "OMISSION_RATE_EXCEEDED": YieldEvaluationOutcome.FAILED_OMISSION_RATE_EXCEEDED,
        }
        return _reason_to_outcome.get(failures[0], YieldEvaluationOutcome.FAILED_INSUFFICIENT_YIELD)

    def _generate_remediation_prompts(
        self,
        units: list[ElicitationUnitRecord],
        failures: list[str],
    ) -> tuple[RemediationPrompt, ...]:
        """Generate bounded, constitutionally-checked remediation prompts."""
        prompts: list[RemediationPrompt] = []
        failure_set = set(failures)

        for unit in units:
            if unit.status is UnitStatus.OMITTED:
                if "OMISSION_RATE_EXCEEDED" in failure_set or "BELOW_MIN_HOLISTIC_YIELD_RATIO" in failure_set:
                    p = self._prompt_generator.generate(unit, kind=RemediationKind.REACTIVATE)
                    if p.constitutional_check_passed:
                        prompts.append(p)
            elif unit.status in (UnitStatus.EXECUTED, UnitStatus.PARTIAL):
                if (
                    "BELOW_MIN_TENSION_SCORE" in failure_set
                    and unit.tension_score < self.policy.min_tension_score
                ):
                    p = self._prompt_generator.generate(unit, kind=RemediationKind.DEEPEN)
                    if p.constitutional_check_passed:
                        prompts.append(p)
                elif (
                    "BELOW_MIN_HOLISTIC_YIELD_RATIO" in failure_set
                    and unit.evidence_count == 0
                ):
                    p = self._prompt_generator.generate(unit, kind=RemediationKind.CLARIFY)
                    if p.constitutional_check_passed:
                        prompts.append(p)

        return tuple(prompts)


# ---------------------------------------------------------------------------
# Module-level convenience entry points
# ---------------------------------------------------------------------------


def evaluate_session_yield(
    session_id: str,
    units: Sequence[ElicitationUnitRecord | Mapping[str, Any]],
    *,
    policy: YieldSufficiencyPolicy | None = None,
    limitations: Sequence[str] = (),
) -> YieldEvaluationReceipt:
    """Convenience entry point for the authoritative CA-M022 boundary.

    Parameters
    ----------
    session_id:
        Non-empty string identifying the interview session.
    units:
        Sequence of unit records for all planned elicitation units.
    policy:
        Optional custom threshold policy; defaults to :class:`YieldSufficiencyPolicy`.
    limitations:
        Optional pre-recorded limitation strings.

    Returns
    -------
    YieldEvaluationReceipt
    """
    return AdaptiveElicitationEvaluator(policy).evaluate(
        session_id, units, limitations=limitations
    )


def require_session_passed(receipt: YieldEvaluationReceipt) -> None:
    """Module-level fail-closed downstream session gate."""
    AdaptiveElicitationEvaluator().require_session_passed(receipt)


# ---------------------------------------------------------------------------
# Private utility functions
# ---------------------------------------------------------------------------


def _threshold_gate(observed: Any, required: Any, failure_code: str) -> UnitGateResult:
    passed = observed >= required
    return UnitGateResult(
        passed=passed,
        observed=observed,
        required=required,
        reason_code=None if passed else failure_code,
    )


def _count_gate(observed: int, required: int, failure_code: str) -> UnitGateResult:
    passed = observed >= required
    return UnitGateResult(
        passed=passed,
        observed=observed,
        required=required,
        reason_code=None if passed else failure_code,
    )


def _ceiling_gate(observed: Any, ceiling: Any, failure_code: str) -> UnitGateResult:
    """Fail when observed EXCEEDS the ceiling (lower is better for omission rate)."""
    passed = observed <= ceiling
    return UnitGateResult(
        passed=passed,
        observed=observed,
        required=ceiling,
        reason_code=None if passed else failure_code,
    )


def _is_score(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and isfinite(value)
        and 0.0 <= value <= 1.0
    )


def _short_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
