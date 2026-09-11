"""Typed Agent Result and Explicit Gate Engine for CAE.

Governed by:
- Phase 6 Mandate M54 (01_AGENT_EXECUTION/M54_typed_agent_result_explicit_gate_engine.md)
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/04_OBJECT_AUTHORITY_MAP.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Enforces:
1. Strict Typed Result Layer:
   Replaces raw model text with immutable, hash-addressed TypedAgentResult records.
2. Explicit, Granular Gate Evaluations:
   Evaluates individually visible checks: schema conformance, required fields, evidence verification,
   authority lane parity, and anti-narrative completion guards.
3. Non-Compensable Gate Gating:
   Failure of any non-compensable gate blocks phase completion and raises typed fail-closed errors.
4. Anti-Narrative Defense:
   Rejects responses that merely state "Done" or "Task finished" without structured contract compliance.
5. HandoffValidator Downstream Interoperability:
   Emits bilateral handoff payloads directly consumable by the Pipeline HandoffValidator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import logging
import re
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple
from uuid import UUID, uuid4

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.agent_invocation import AgentInvocation
from ca_runtime.agent_registry import AgentOutputContract
from ca_runtime.pi_adapter import AuthorityLane

logger = logging.getLogger("ca_runtime.agent_result_gates")


# ---------------------------------------------------------------------------
# Typed Error Taxonomy
# ---------------------------------------------------------------------------

class AgentResultGateError(RuntimeError):
    """Base error for agent result gate evaluation failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "AGENT_RESULT_GATE_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}


class SchemaValidationGateError(AgentResultGateError):
    """Raised when an Agent's output fails structural or type schema validation."""

    def __init__(self, contract_id: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"SCHEMA_VALIDATION_FAILED: Output failed schema contract '{contract_id}': {reason}",
            reason_code="SCHEMA_VALIDATION_FAILED",
            details={"contract_id": contract_id, "reason": reason, **(details or {})},
        )


class RequiredFieldGateError(AgentResultGateError):
    """Raised when mandatory contract fields are missing from the agent payload."""

    def __init__(self, contract_id: str, missing_fields: Sequence[str]):
        super().__init__(
            f"REQUIRED_FIELD_MISSING: Output contract '{contract_id}' is missing mandatory fields: {list(missing_fields)}",
            reason_code="REQUIRED_FIELD_MISSING",
            details={"contract_id": contract_id, "missing_fields": list(missing_fields)},
        )


class EvidenceRefGateError(AgentResultGateError):
    """Raised when cited evidence or artifact references are ungrounded or hallucinated."""

    def __init__(self, invalid_refs: Sequence[str], reason: str = "Evidence references not present in verified context"):
        super().__init__(
            f"UNVERIFIED_EVIDENCE_REF: Output cites ungrounded or invalid evidence/artifact refs: {list(invalid_refs)}. {reason}",
            reason_code="UNVERIFIED_EVIDENCE_REF",
            details={"invalid_refs": list(invalid_refs), "reason": reason},
        )


class AuthorityGateError(AgentResultGateError):
    """Raised when an agent output attempts operations or side effects outside its assigned Authority Lane."""

    def __init__(self, lane: str, attempted_operation: str, reason: str):
        super().__init__(
            f"AUTHORITY_LANE_VIOLATION: Agent in lane '{lane}' attempted unauthorized operation '{attempted_operation}': {reason}",
            reason_code="AUTHORITY_LANE_VIOLATION",
            details={"lane": lane, "attempted_operation": attempted_operation, "reason": reason},
        )


class AgentCompletionClaimRejectedError(AgentResultGateError):
    """Raised when an agent outputs narrative 'done' claims without structured contract satisfaction."""

    def __init__(self, message: str = "Agent output consists of narrative completion claim rather than required typed JSON"):
        super().__init__(
            f"COMPLETION_CLAIM_REJECTED: {message}",
            reason_code="COMPLETION_CLAIM_REJECTED",
            details={"message": message},
        )


class GateEvaluationFailedError(AgentResultGateError):
    """Raised when one or more non-compensable gates fail evaluation."""

    def __init__(self, evaluation_id: str, failed_gates: Sequence[str], details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"GATE_EVALUATION_FAILED: AgentResultGateEvaluation '{evaluation_id}' failed non-compensable gates: {list(failed_gates)}",
            reason_code="GATE_EVALUATION_FAILED",
            details={"evaluation_id": evaluation_id, "failed_gates": list(failed_gates), **(details or {})},
        )


# ---------------------------------------------------------------------------
# Domain Models: IndividualGateCheck, AgentResultGateEvaluation, TypedAgentResult
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class IndividualGateCheck:
    """Individual visible gate evaluation check."""
    gate_name: str
    is_compensable: bool
    passed: bool
    score_bps: int
    failure_reason: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "gate_name": self.gate_name,
            "is_compensable": self.is_compensable,
            "passed": self.passed,
            "score_bps": int(self.score_bps),
            "failure_reason": self.failure_reason,
            "details": dict(sorted(self.details.items())),
        }


@dataclass(frozen=True, slots=True)
class AgentResultGateEvaluation:
    """Aggregated evaluation record detailing the pass/fail status of all gates."""
    evaluation_id: str
    invocation_id: str
    agent_id: str
    contract_id: str
    checks: Tuple[IndividualGateCheck, ...]
    all_required_passed: bool
    composite_score_bps: int
    evaluation_sha256: str
    evaluated_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "invocation_id": self.invocation_id,
            "agent_id": self.agent_id,
            "contract_id": self.contract_id,
            "checks": [c.canonical_dict() for c in sorted(self.checks, key=lambda c: c.gate_name)],
            "all_required_passed": self.all_required_passed,
            "composite_score_bps": int(self.composite_score_bps),
            "evaluated_at": self.evaluated_at,
        }

    def get_check(self, gate_name: str) -> Optional[IndividualGateCheck]:
        for c in self.checks:
            if c.gate_name == gate_name:
                return c
        return None


@dataclass(frozen=True, slots=True)
class TypedAgentResult:
    """The strongly typed, validated execution outcome produced by an AgentInvocation."""
    result_id: str
    invocation_id: str
    agent_id: str
    contract_id: str
    lane: AuthorityLane
    parsed_payload: Dict[str, Any]
    evidence_refs: Tuple[str, ...]
    artifact_refs: Tuple[str, ...]
    gate_evaluation: AgentResultGateEvaluation
    raw_response_sha256: str
    result_sha256: str
    created_at: str

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "invocation_id": self.invocation_id,
            "agent_id": self.agent_id,
            "contract_id": self.contract_id,
            "lane": self.lane.value,
            "parsed_payload": self.parsed_payload,
            "evidence_refs": list(sorted(self.evidence_refs)),
            "artifact_refs": list(sorted(self.artifact_refs)),
            "gate_evaluation": self.gate_evaluation.canonical_dict(),
            "raw_response_sha256": self.raw_response_sha256,
            "created_at": self.created_at,
        }

    def to_handoff_payload(
        self,
        *,
        consumer_node_id: str,
        producer_node_id: str,
        authority_refs: Optional[Sequence[str]] = None,
    ) -> Dict[str, Any]:
        """Produce a handoff envelope directly consumable by HandoffValidator."""
        return {
            "producer_node_id": producer_node_id,
            "consumer_node_id": consumer_node_id,
            "output_ref": {
                "object_id": self.result_id,
                "version": "1.0.0",
                "sha256": self.result_sha256,
            },
            "contract_id": self.contract_id,
            "validation_receipt_refs": [f"receipt:{self.gate_evaluation.evaluation_id}"],
            "authority_refs": list(authority_refs or [f"authority:lane:{self.lane.value}"]),
            "lifecycle_state": "ACCEPTED",
        }


# ---------------------------------------------------------------------------
# Explicit Gate Engine
# ---------------------------------------------------------------------------

class AgentResultGateEngine:
    """Deterministic evaluation engine running explicit validation gates against model inferences."""

    NARRATIVE_COMPLETION_PATTERNS = [
        re.compile(r"^\s*(done|task completed|finished|i have completed|all tasks done|i have completed all tasks|task finished)[\.!]?\s*$", re.IGNORECASE),
        re.compile(r"^\s*here is the summary:?\s*$", re.IGNORECASE),
    ]

    @classmethod
    def evaluate(
        cls,
        *,
        raw_response_text: str,
        parsed_json: Optional[Dict[str, Any]],
        output_contract: AgentOutputContract | Dict[str, Any],
        invocation: AgentInvocation,
        verified_evidence_ids: Optional[Sequence[str]] = None,
        verified_artifact_ids: Optional[Sequence[str]] = None,
        schema_validator: Optional[Callable[[Dict[str, Any]], bool]] = None,
        required_fields: Optional[Sequence[str]] = None,
        strict: bool = True,
    ) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        """Evaluates all explicit gates against inference results.
        
        Evaluates 5 distinct gates:
        1. anti_narrative_completion (non-compensable)
        2. schema_conformance (non-compensable)
        3. required_fields (non-compensable)
        4. evidence_refs_verifiable (non-compensable)
        5. authority_lane_parity (non-compensable)
        """
        contract_id = (
            output_contract.contract_id
            if isinstance(output_contract, AgentOutputContract)
            else output_contract.get("contract_id", "contract:default")
        )
        checks: List[IndividualGateCheck] = []

        # -------------------------------------------------------------------
        # Gate 1: Anti-Narrative Completion Guard
        # -------------------------------------------------------------------
        is_narrative_done = False
        cleaned_text = raw_response_text.strip()
        for pat in cls.NARRATIVE_COMPLETION_PATTERNS:
            if pat.match(cleaned_text):
                is_narrative_done = True
                break

        if is_narrative_done and parsed_json is None:
            checks.append(
                IndividualGateCheck(
                    gate_name="anti_narrative_completion",
                    is_compensable=False,
                    passed=False,
                    score_bps=0,
                    failure_reason="Model returned narrative 'done' text without structured contract compliance",
                    details={"raw_text": cleaned_text[:100]},
                )
            )
        else:
            checks.append(
                IndividualGateCheck(
                    gate_name="anti_narrative_completion",
                    is_compensable=False,
                    passed=True,
                    score_bps=10000,
                    details={"checked_patterns": len(cls.NARRATIVE_COMPLETION_PATTERNS)},
                )
            )

        # -------------------------------------------------------------------
        # Gate 2: Schema Conformance Gate
        # -------------------------------------------------------------------
        schema_passed = True
        schema_failure_reason: Optional[str] = None
        schema_details: Dict[str, Any] = {}

        if parsed_json is None:
            schema_passed = False
            schema_failure_reason = "Model response could not be parsed as valid JSON"
        elif schema_validator is not None:
            try:
                if not schema_validator(parsed_json):
                    schema_passed = False
                    schema_failure_reason = "Schema validator function rejected payload"
            except Exception as e:
                schema_passed = False
                schema_failure_reason = f"Schema validator raised exception: {e}"
        elif isinstance(parsed_json, dict):
            # Baseline dictionary structure check
            if not parsed_json:
                schema_passed = False
                schema_failure_reason = "Parsed JSON payload is empty"
        else:
            schema_passed = False
            schema_failure_reason = "Parsed JSON is not a structured dictionary"

        checks.append(
            IndividualGateCheck(
                gate_name="schema_conformance",
                is_compensable=False,
                passed=schema_passed,
                score_bps=10000 if schema_passed else 0,
                failure_reason=schema_failure_reason,
                details=schema_details,
            )
        )

        # -------------------------------------------------------------------
        # Gate 3: Required Fields Gate
        # -------------------------------------------------------------------
        fields_passed = True
        missing_fields_list: List[str] = []

        # Derive required fields from contract or argument
        expected_fields: List[str] = list(required_fields or [])
        if not expected_fields and isinstance(output_contract, dict):
            expected_fields = output_contract.get("required_fields", [])

        if parsed_json and expected_fields:
            for req_field in expected_fields:
                if req_field not in parsed_json:
                    missing_fields_list.append(req_field)
            if missing_fields_list:
                fields_passed = False

        checks.append(
            IndividualGateCheck(
                gate_name="required_fields",
                is_compensable=False,
                passed=fields_passed,
                score_bps=10000 if fields_passed else 0,
                failure_reason=f"Missing mandatory fields: {missing_fields_list}" if missing_fields_list else None,
                details={"expected_fields": expected_fields, "missing_fields": missing_fields_list},
            )
        )

        # -------------------------------------------------------------------
        # Gate 4: Evidence & Artifact Verification Gate
        # -------------------------------------------------------------------
        evidence_passed = True
        invalid_evidence_refs: List[str] = []
        extracted_evidence: List[str] = []
        extracted_artifacts: List[str] = []

        if parsed_json:
            # Extract cited evidence and artifact IDs
            for key in ("evidence_refs", "evidence_ids", "source_evidence", "evidence"):
                if key in parsed_json and isinstance(parsed_json[key], list):
                    for item in parsed_json[key]:
                        if isinstance(item, str):
                            extracted_evidence.append(item)
                        elif isinstance(item, dict) and "id" in item:
                            extracted_evidence.append(item["id"])

            for key in ("artifact_refs", "artifacts", "artifact_ids"):
                if key in parsed_json and isinstance(parsed_json[key], list):
                    for item in parsed_json[key]:
                        if isinstance(item, str):
                            extracted_artifacts.append(item)
                        elif isinstance(item, dict) and "id" in item:
                            extracted_artifacts.append(item["id"])

            # Verify against ground truth pools if provided
            if verified_evidence_ids is not None:
                verified_set = set(verified_evidence_ids)
                for ref in extracted_evidence:
                    if ref not in verified_set:
                        invalid_evidence_refs.append(ref)
                if invalid_evidence_refs:
                    evidence_passed = False

            if verified_artifact_ids is not None:
                verified_art_set = set(verified_artifact_ids)
                for ref in extracted_artifacts:
                    if ref not in verified_art_set:
                        invalid_evidence_refs.append(ref)
                if invalid_evidence_refs:
                    evidence_passed = False

        checks.append(
            IndividualGateCheck(
                gate_name="evidence_refs_verifiable",
                is_compensable=False,
                passed=evidence_passed,
                score_bps=10000 if evidence_passed else 0,
                failure_reason=f"Ungrounded evidence/artifact references: {invalid_evidence_refs}" if invalid_evidence_refs else None,
                details={
                    "extracted_evidence_count": len(extracted_evidence),
                    "extracted_artifacts_count": len(extracted_artifacts),
                    "invalid_refs": invalid_evidence_refs,
                },
            )
        )

        # -------------------------------------------------------------------
        # Gate 5: Authority Lane & Mutation Gate
        # -------------------------------------------------------------------
        authority_passed = True
        authority_failure_reason: Optional[str] = None

        if parsed_json and invocation.lane in (AuthorityLane.HUNTER, AuthorityLane.ANALYST):
            # Check for illegal mutation proposals
            for forbidden_mutation_key in ("execute_sql", "mutate_database", "drop_table", "update_records"):
                if forbidden_mutation_key in parsed_json:
                    authority_passed = False
                    authority_failure_reason = f"Read-only lane '{invocation.lane.value}' attempted mutation key '{forbidden_mutation_key}'"
                    break

        checks.append(
            IndividualGateCheck(
                gate_name="authority_lane_parity",
                is_compensable=False,
                passed=authority_passed,
                score_bps=10000 if authority_passed else 0,
                failure_reason=authority_failure_reason,
                details={"lane": invocation.lane.value},
            )
        )

        # -------------------------------------------------------------------
        # Aggregate Results & Compute SHA-256
        # -------------------------------------------------------------------
        all_required_passed = all(c.passed for c in checks if not c.is_compensable)
        composite_score = sum(c.score_bps for c in checks) // len(checks)

        evaluated_at = utc_now_rfc3339()
        eval_id = f"eval_{hashlib.sha256(f'{invocation.invocation_id}:{evaluated_at}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"

        eval_partial = {
            "evaluation_id": eval_id,
            "invocation_id": invocation.invocation_id,
            "agent_id": invocation.agent_id,
            "contract_id": contract_id,
            "checks": [c.canonical_dict() for c in sorted(checks, key=lambda c: c.gate_name)],
            "all_required_passed": all_required_passed,
            "composite_score_bps": int(composite_score),
            "evaluated_at": evaluated_at,
        }
        eval_sha = canonical_sha256(eval_partial)

        gate_eval = AgentResultGateEvaluation(
            evaluation_id=eval_id,
            invocation_id=invocation.invocation_id,
            agent_id=invocation.agent_id,
            contract_id=contract_id,
            checks=tuple(checks),
            all_required_passed=all_required_passed,
            composite_score_bps=composite_score,
            evaluation_sha256=eval_sha,
            evaluated_at=evaluated_at,
        )

        # Fail closed on strict evaluation if required gates failed
        if strict and not all_required_passed:
            failed_names = [c.gate_name for c in checks if not c.passed]
            if not checks[0].passed:  # anti_narrative_completion
                raise AgentCompletionClaimRejectedError(checks[0].failure_reason or "Narrative completion rejected")
            if not checks[1].passed:  # schema_conformance
                raise SchemaValidationGateError(contract_id, checks[1].failure_reason or "Schema failed")
            if not checks[2].passed:  # required_fields
                raise RequiredFieldGateError(contract_id, missing_fields_list)
            if not checks[3].passed:  # evidence_refs_verifiable
                raise EvidenceRefGateError(invalid_evidence_refs)
            if not checks[4].passed:  # authority_lane_parity
                raise AuthorityGateError(invocation.lane.value, "MUTATION", checks[4].failure_reason or "Authority violated")
            raise GateEvaluationFailedError(eval_id, failed_names)

        # -------------------------------------------------------------------
        # Construct TypedAgentResult
        # -------------------------------------------------------------------
        raw_sha = hashlib.sha256(raw_response_text.encode("utf-8")).hexdigest()
        result_id = f"res_{hashlib.sha256(f'{eval_id}:{raw_sha}:{uuid4()}'.encode('utf-8')).hexdigest()[:20]}"
        created_at = utc_now_rfc3339()

        result_partial = {
            "result_id": result_id,
            "invocation_id": invocation.invocation_id,
            "agent_id": invocation.agent_id,
            "contract_id": contract_id,
            "lane": invocation.lane.value,
            "parsed_payload": parsed_json or {},
            "evidence_refs": list(sorted(set(extracted_evidence))),
            "artifact_refs": list(sorted(set(extracted_artifacts))),
            "gate_evaluation": gate_eval.canonical_dict(),
            "raw_response_sha256": raw_sha,
            "created_at": created_at,
        }
        result_sha = canonical_sha256(result_partial)

        typed_result = TypedAgentResult(
            result_id=result_id,
            invocation_id=invocation.invocation_id,
            agent_id=invocation.agent_id,
            contract_id=contract_id,
            lane=invocation.lane,
            parsed_payload=parsed_json or {},
            evidence_refs=tuple(sorted(set(extracted_evidence))),
            artifact_refs=tuple(sorted(set(extracted_artifacts))),
            gate_evaluation=gate_eval,
            raw_response_sha256=raw_sha,
            result_sha256=result_sha,
            created_at=created_at,
        )

        return typed_result, gate_eval
