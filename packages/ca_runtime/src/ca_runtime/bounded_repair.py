"""Bounded Repair and Same-Session Retry for CAE.

Governed by:
- Phase 6 Mandate M55 (01_AGENT_EXECUTION/M55_bounded_repair_same_session_retry.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Enforces:
1. In-Session Bounded Repair:
   Preserves live session context (session_id, run_id, state_id, agent_id, input_context_sha256)
   and routes structured failure codes, failed gate names, and corrective instructions back into the same bounded phase.
2. Failure Discrimination:
   Strictly separates Retryable Failures (schema, missing fields, ungrounded citations, narrative completion)
   from Non-Retryable Violations (Authority Lane violations, illegal mutations, tenancy leaks, package drift, security breaches).
3. Monotonic Attempt Bounding:
   Strictly enforces monotonic attempt counting (attempt_number <= max_retries), preventing infinite loops and attempt reset attacks.
4. Deterministic Exhaustion State:
   Transitions deterministically to FAILED_EXHAUSTED when attempt budget is exceeded, maintaining auditable repair lineage.
5. StateM Checked Transfer Semantics:
   Execution remains strictly in the source phase state during retries; failure leaves state in source/failure boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.agent_invocation import AgentInvocation
from ca_runtime.agent_result_gates import (
    AgentCompletionClaimRejectedError,
    AgentResultGateError,
    AgentResultGateEvaluation,
    AuthorityGateError,
    EvidenceRefGateError,
    GateEvaluationFailedError,
    RequiredFieldGateError,
    SchemaValidationGateError,
    TypedAgentResult,
)
from ca_runtime.pi_adapter import AuthorityLaneMismatchError
from ca_runtime.tenancy import TenancyViolationError

logger = logging.getLogger("ca_runtime.bounded_repair")


# ---------------------------------------------------------------------------
# Failure Classification Enum
# ---------------------------------------------------------------------------

class RepairFailureClassification(str, Enum):
    """Classification of failure reasons for bounded repair loops."""
    # Retryable failure modes
    RETRYABLE_SCHEMA_FAILURE = "RETRYABLE_SCHEMA_FAILURE"
    RETRYABLE_EVIDENCE_FAILURE = "RETRYABLE_EVIDENCE_FAILURE"
    RETRYABLE_NARRATIVE_FAILURE = "RETRYABLE_NARRATIVE_FAILURE"
    RETRYABLE_INFERENCE_TIMEOUT = "RETRYABLE_INFERENCE_TIMEOUT"

    # Non-retryable failure modes (fail immediately)
    NON_RETRYABLE_CONSTITUTIONAL_VIOLATION = "NON_RETRYABLE_CONSTITUTIONAL_VIOLATION"
    NON_RETRYABLE_SECURITY_VIOLATION = "NON_RETRYABLE_SECURITY_VIOLATION"
    NON_RETRYABLE_DRIFT_VIOLATION = "NON_RETRYABLE_DRIFT_VIOLATION"

    @property
    def is_retryable(self) -> bool:
        return self in (
            RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
            RepairFailureClassification.RETRYABLE_EVIDENCE_FAILURE,
            RepairFailureClassification.RETRYABLE_NARRATIVE_FAILURE,
            RepairFailureClassification.RETRYABLE_INFERENCE_TIMEOUT,
        )


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class BoundedRepairError(RuntimeError):
    """Base exception for bounded repair and retry operations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "BOUNDED_REPAIR_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class NonRetryableFailureError(BoundedRepairError):
    """Raised when a non-retryable failure (constitutional, security, drift) halts execution immediately."""

    def __init__(self, failure_classification: RepairFailureClassification, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"NON_RETRYABLE_VIOLATION: Execution halted immediately due to {failure_classification.value}: {reason}",
            reason_code="NON_RETRYABLE_VIOLATION",
            details={"classification": failure_classification.value, "reason": reason, **(details or {})},
        )


class RepairBudgetExhaustedError(BoundedRepairError):
    """Raised when a bounded repair loop exhausts its maximum retry budget."""

    def __init__(self, session_id: str, attempt_count: int, max_retries: int, last_reason: str):
        super().__init__(
            f"REPAIR_BUDGET_EXHAUSTED: Session '{session_id}' exhausted retry budget ({attempt_count}/{max_retries} attempts). Last failure: {last_reason}",
            reason_code="REPAIR_BUDGET_EXHAUSTED",
            details={
                "session_id": session_id,
                "attempt_count": attempt_count,
                "max_retries": max_retries,
                "last_reason": last_reason,
            },
        )


class RepairContractDriftError(BoundedRepairError):
    """Raised when an attempt is made to alter the output contract or agent identity during a retry loop."""

    def __init__(self, expected: str, actual: str, field_name: str):
        super().__init__(
            f"CONTRACT_DRIFT_DETECTED: Immutable {field_name} drift during repair retry. Expected '{expected}', got '{actual}'",
            reason_code="CONTRACT_DRIFT_DETECTED",
            details={"field_name": field_name, "expected": expected, "actual": actual},
        )


class RepairSessionCorruptedError(BoundedRepairError):
    """Raised when session tracking invariants (e.g. monotonic counter) are corrupted or tampered."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"SESSION_CORRUPTED: {message}",
            reason_code="SESSION_CORRUPTED",
            details=details or {},
        )


# ---------------------------------------------------------------------------
# Domain Models: RepairAttemptRecord & BoundedRepairSession
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class RepairAttemptRecord:
    """Immutable audit record of a single repair iteration in a live Agent Session."""
    repair_id: str
    session_id: str
    run_id: str
    state_id: str
    agent_id: str
    contract_id: str
    attempt_number: int
    max_retries: int
    failure_classification: RepairFailureClassification
    failed_gate_names: Tuple[str, ...]
    failure_reason: str
    corrective_instruction: str
    input_context_sha256: str
    prior_output_sha256: Optional[str]
    attempt_sha256: str
    recorded_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "repair_id": self.repair_id,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "state_id": self.state_id,
            "agent_id": self.agent_id,
            "contract_id": self.contract_id,
            "attempt_number": int(self.attempt_number),
            "max_retries": int(self.max_retries),
            "failure_classification": self.failure_classification.value,
            "failed_gate_names": list(sorted(self.failed_gate_names)),
            "failure_reason": self.failure_reason,
            "corrective_instruction": self.corrective_instruction,
            "input_context_sha256": self.input_context_sha256,
            "prior_output_sha256": self.prior_output_sha256,
            "recorded_at": self.recorded_at,
        }


@dataclass
class BoundedRepairSession:
    """Tracks state, attempt budgets, and lineage for bounded in-session repairs."""
    session_id: str
    run_id: str
    state_id: str
    agent_id: str
    contract_id: str
    input_context_sha256: str
    max_retries: int = 2
    attempt_count: int = 0
    repair_history: List[RepairAttemptRecord] = field(default_factory=list)
    terminal_state: str = "ACTIVE"

    def record_failure(
        self,
        *,
        failure_classification: RepairFailureClassification,
        failed_gates: Sequence[str],
        failure_reason: str,
        corrective_instruction: str,
        input_context_sha256: str,
        prior_output_sha256: Optional[str] = None,
    ) -> RepairAttemptRecord:
        """Records a failure attempt, updates attempt budget, and enforces non-retryable and exhaustion boundaries."""
        # Non-retryable violations halt immediately without consuming retry attempts
        if not failure_classification.is_retryable:
            self.terminal_state = "FAILED_FATAL"
            raise NonRetryableFailureError(
                failure_classification,
                failure_reason,
                {"session_id": self.session_id, "failed_gates": list(failed_gates)},
            )

        # Increment monotonic attempt count
        self.attempt_count += 1
        attempt_number = self.attempt_count

        recorded_at = utc_now_rfc3339()
        repair_id = f"repair_{hashlib.sha256(f'{self.session_id}:{attempt_number}:{recorded_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        attempt_partial = {
            "repair_id": repair_id,
            "session_id": self.session_id,
            "run_id": self.run_id,
            "state_id": self.state_id,
            "agent_id": self.agent_id,
            "contract_id": self.contract_id,
            "attempt_number": int(attempt_number),
            "max_retries": int(self.max_retries),
            "failure_classification": failure_classification.value,
            "failed_gate_names": list(sorted(failed_gates)),
            "failure_reason": failure_reason,
            "corrective_instruction": corrective_instruction,
            "input_context_sha256": input_context_sha256,
            "prior_output_sha256": prior_output_sha256,
            "recorded_at": recorded_at,
        }
        attempt_sha = canonical_sha256(attempt_partial)

        record = RepairAttemptRecord(
            repair_id=repair_id,
            session_id=self.session_id,
            run_id=self.run_id,
            state_id=self.state_id,
            agent_id=self.agent_id,
            contract_id=self.contract_id,
            attempt_number=attempt_number,
            max_retries=self.max_retries,
            failure_classification=failure_classification,
            failed_gate_names=tuple(sorted(failed_gates)),
            failure_reason=failure_reason,
            corrective_instruction=corrective_instruction,
            input_context_sha256=input_context_sha256,
            prior_output_sha256=prior_output_sha256,
            attempt_sha256=attempt_sha,
            recorded_at=recorded_at,
        )

        self.repair_history.append(record)

        # Check for budget exhaustion
        if self.attempt_count > self.max_retries:
            self.terminal_state = "FAILED_EXHAUSTED"
            raise RepairBudgetExhaustedError(
                self.session_id,
                self.attempt_count,
                self.max_retries,
                failure_reason,
            )

        self.terminal_state = "REPAIR_RETRYING"
        return record

    def record_success(self, result: TypedAgentResult) -> None:
        """Marks the bounded repair session as successfully completed."""
        self.terminal_state = "REPAIR_SUCCEEDED"

    def verify_session_integrity(self, invocation: AgentInvocation) -> None:
        """Verifies session invariance across attempts to prevent contract drift and session tampering."""
        if invocation.agent_id != self.agent_id:
            raise RepairContractDriftError(self.agent_id, invocation.agent_id, "agent_id")
        contract_id = (
            invocation.output_contract.contract_id
            if hasattr(invocation.output_contract, "contract_id")
            else str(invocation.output_contract)
        )
        if contract_id != self.contract_id:
            raise RepairContractDriftError(self.contract_id, contract_id, "contract_id")


# ---------------------------------------------------------------------------
# Bounded Repair Runtime Engine
# ---------------------------------------------------------------------------

class BoundedRepairRuntimeEngine:
    """Drives governed same-session repair retry loops with deterministic failure diagnosis."""

    @classmethod
    def create_session(
        cls,
        *,
        invocation: AgentInvocation,
        max_retries: int = 2,
    ) -> BoundedRepairSession:
        """Initialize a new BoundedRepairSession for an AgentInvocation."""
        contract_id = (
            invocation.output_contract.contract_id
            if hasattr(invocation.output_contract, "contract_id")
            else str(invocation.output_contract)
        )
        input_context_sha = (
            invocation.capsule_sha256
            if hasattr(invocation, "capsule_sha256") and invocation.capsule_sha256
            else invocation.invocation_sha256
        )
        return BoundedRepairSession(
            session_id=f"sess_{uuid4().hex[:16]}",
            run_id=invocation.run_id,
            state_id=invocation.state_id,
            agent_id=invocation.agent_id,
            contract_id=contract_id,
            input_context_sha256=input_context_sha,
            max_retries=max_retries,
        )

    @classmethod
    def diagnose_failure(
        cls,
        error: Exception,
        raw_response_text: str = "",
    ) -> Tuple[RepairFailureClassification, List[str], str, str]:
        """Diagnose an execution/gate error into failure classification, failed gates, reason, and corrective instruction."""
        if isinstance(error, (AuthorityGateError, AuthorityLaneMismatchError)):
            return (
                RepairFailureClassification.NON_RETRYABLE_CONSTITUTIONAL_VIOLATION,
                ["authority_lane_parity"],
                str(error),
                "Constitutional Authority Lane violation cannot be repaired in session.",
            )

        if isinstance(error, TenancyViolationError):
            return (
                RepairFailureClassification.NON_RETRYABLE_SECURITY_VIOLATION,
                ["tenancy_isolation"],
                str(error),
                "Security Tenancy violation cannot be repaired in session.",
            )

        if isinstance(error, AgentCompletionClaimRejectedError):
            return (
                RepairFailureClassification.RETRYABLE_NARRATIVE_FAILURE,
                ["anti_narrative_completion"],
                str(error),
                "Your previous output was rejected because it contained plain narrative 'done' text. "
                "You MUST output valid, structured JSON adhering strictly to the declared output contract.",
            )

        if isinstance(error, SchemaValidationGateError):
            return (
                RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
                ["schema_conformance"],
                str(error),
                f"Your previous output failed schema validation: {error.details.get('reason', str(error))}. "
                "Ensure output is valid JSON matching all property types.",
            )

        if isinstance(error, RequiredFieldGateError):
            missing = error.details.get("missing_fields", [])
            return (
                RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
                ["required_fields"],
                str(error),
                f"Your previous output was missing mandatory contract fields: {missing}. "
                "Include all required fields in your JSON response.",
            )

        if isinstance(error, EvidenceRefGateError):
            invalid_refs = error.details.get("invalid_refs", [])
            return (
                RepairFailureClassification.RETRYABLE_EVIDENCE_FAILURE,
                ["evidence_refs_verifiable"],
                str(error),
                f"Your previous output cited ungrounded/invalid evidence or artifact IDs: {invalid_refs}. "
                "Only cite verified evidence references provided in your context.",
            )

        if isinstance(error, TimeoutError):
            return (
                RepairFailureClassification.RETRYABLE_INFERENCE_TIMEOUT,
                ["execution_timeout"],
                str(error),
                "Previous inference attempt timed out. Re-evaluating with focused context.",
            )

        # Default fallback
        return (
            RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
            ["gate_evaluation"],
            str(error),
            f"Previous attempt encountered error: {str(error)}. Correct output to comply with contract.",
        )

    @classmethod
    def execute_with_repair(
        cls,
        *,
        session: BoundedRepairSession,
        invocation: AgentInvocation,
        inference_fn: Callable[[AgentInvocation, Optional[RepairAttemptRecord]], str],
        gate_evaluator: Callable[[str, AgentInvocation], Tuple[TypedAgentResult, AgentResultGateEvaluation]],
    ) -> Tuple[TypedAgentResult, BoundedRepairSession]:
        """Drives the bounded repair loop until success or budget exhaustion."""
        while True:
            session.verify_session_integrity(invocation)
            prior_record = session.repair_history[-1] if session.repair_history else None

            raw_response = inference_fn(invocation, prior_record)

            try:
                typed_result, gate_eval = gate_evaluator(raw_response, invocation)
                session.record_success(typed_result)
                return typed_result, session
            except Exception as exc:
                failure_class, failed_gates, reason, corrective = cls.diagnose_failure(exc, raw_response)
                session.record_failure(
                    failure_classification=failure_class,
                    failed_gates=failed_gates,
                    failure_reason=reason,
                    corrective_instruction=corrective,
                    input_context_sha256=session.input_context_sha256,
                    prior_output_sha256=hashlib.sha256(raw_response.encode("utf-8")).hexdigest(),
                )
