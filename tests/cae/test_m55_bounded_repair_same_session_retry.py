"""Comprehensive Test Suite for CAE Mandate M55: Bounded Repair + Same-Session Retry.

Governed by:
- 01_AGENT_EXECUTION/M55_bounded_repair_same_session_retry.md
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Verifies:
- Gate 1: Retry count is bounded (RepairBudgetExhaustedError).
- Gate 2: Same session/context identity is preserved where intended.
- Gate 3: Non-retryable failures fail immediately (NonRetryableFailureError).
- Gate 4: Every repair is observable (RepairAttemptRecord lineage).
- Gate 5: Exhaustion enters explicit failure state (FAILED_EXHAUSTED).
- False-Proof Defense 1: Feeding the same failed output forever exhausts budget.
- False-Proof Defense 2: Altering output contract between attempts raises RepairContractDriftError.
- False-Proof Defense 3: Retrying a constitutional violation fails immediately.
- False-Proof Defense 4: Resetting attempt count is prevented by monotonic counter.
- Concrete Execution Trace: Failure -> Diagnostic Repair -> Corrected Retry -> TypedAgentResult.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime import (
    AccessMode,
    AgentCapabilityGrant,
    AgentCompletionClaimRejectedError,
    AgentDefinition,
    AgentInvocation,
    AgentInvocationCompiler,
    AgentLifecycleState,
    AgentModelPolicy,
    AgentOutputContract,
    AgentPromptReference,
    AgentRegistry,
    AgentResultGateEngine,
    AgentResultGateError,
    AgentResultGateEvaluation,
    AuthorityGateError,
    AuthorityLane,
    BoundedRepairError,
    BoundedRepairRuntimeEngine,
    BoundedRepairSession,
    EvidenceRefGateError,
    IndividualGateCheck,
    JITContextCapsule,
    JITContextCompiler,
    NonRetryableFailureError,
    RepairAttemptRecord,
    RepairBudgetExhaustedError,
    RepairContractDriftError,
    RepairFailureClassification,
    RepairSessionCorruptedError,
    RequiredFieldGateError,
    SchemaValidationGateError,
    TypedAgentResult,
)


@pytest.fixture
def sample_workspace_id() -> UUID:
    return uuid4()


@pytest.fixture
def sample_analyst_agent() -> AgentDefinition:
    return AgentDefinition(
        agent_id="RelationshipCanonicalizationAnalystAgent",
        version="1.0.0",
        name="Relationship Canonicalization Analyst Agent",
        purpose="Classifies relationships and resolves contradictions across knowledge candidates.",
        authority_lane=AuthorityLane.ANALYST,
        lifecycle_state=AgentLifecycleState.APPROVED,
        model_policy=AgentModelPolicy(preferred_model="gemini-2.5-pro", temperature_bps=2000),
        prompt_reference=AgentPromptReference(instructions_ref="instructions.md", cae_md_ref="CAE.md"),
        tools=["semantic_similarity_analyzer"],
        output_contract=AgentOutputContract(
            contract_id="contract:canonical-relationship:v1",
            output_type="JSON",
            description="Classified relationship edges with confidence scoring",
        ),
    )


@pytest.fixture
def sample_context_capsule(sample_workspace_id: UUID) -> JITContextCapsule:
    return JITContextCompiler.assemble(
        workspace_id=sample_workspace_id,
        lane=AuthorityLane.ANALYST,
        actor_id="actor:operator-analyst",
        program_id="program:research_canonicalization",
        harness_id="harness:atomic_analyst",
        agent_id="RelationshipCanonicalizationAnalystAgent",
        model_id="gemini-2.5-pro",
        total_token_budget=64_000,
        constitutions=[
            ("CIVIL_CODE", "docs/CIVIL_CODE.md", "Civil Code: Verified citations only.")
        ],
        operator_grants=[
            ("GRANT_READ", "grants/op_read.json", "Operator grant: Read-only analyst.")
        ],
        program_harness_policies=[
            ("PROGRAM_POLICY", "policy/harness.yaml", "Program policy: Deterministic classification.")
        ],
        local_governance_cae_md=("CAE.md", "Local CAE rules."),
        agent_instructions=("instructions.md", "Classify relationships between candidates."),
        production_mode=True,
    )


@pytest.fixture
def sample_invocation(
    sample_analyst_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
) -> AgentInvocation:
    return AgentInvocationCompiler.compile(
        agent=sample_analyst_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_m55_repair_001",
        state_id="STATE_RELATIONSHIP_CANONICALIZATION",
    )


@pytest.fixture
def verified_evidence_pool() -> List[str]:
    return ["ev_candidate_101", "ev_candidate_102", "ev_signal_201"]


# ---------------------------------------------------------------------------
# Acceptance Gate Tests
# ---------------------------------------------------------------------------

def test_gate1_retry_count_is_bounded(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 1: Retry count is bounded and raises RepairBudgetExhaustedError when exceeded."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    # Simulated failing inference that always returns broken JSON
    def always_broken_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        return "Not valid json"

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=None,
            output_contract=inv.output_contract,
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    with pytest.raises(RepairBudgetExhaustedError) as exc_info:
        BoundedRepairRuntimeEngine.execute_with_repair(
            session=session,
            invocation=sample_invocation,
            inference_fn=always_broken_inference,
            gate_evaluator=gate_evaluator,
        )

    assert exc_info.value.reason_code == "REPAIR_BUDGET_EXHAUSTED"
    assert session.attempt_count == 3  # 1 initial + 2 retries = 3 attempts total
    assert session.terminal_state == "FAILED_EXHAUSTED"
    assert len(session.repair_history) == 3


def test_gate2_same_session_context_identity_preserved(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 2: Same session_id, run_id, state_id, agent_id, and input_context_sha256 are preserved across attempts."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    attempt_counter = 0

    def recovering_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter == 1:
            return "Done"  # Fails narrative completion gate
        # Attempt 2: valid payload
        return json.dumps({
            "relationship_type": "CORROBORATES",
            "confidence_bps": 9100,
            "evidence_refs": ["ev_candidate_101"],
        })

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        try:
            parsed = json.loads(raw_text)
        except Exception:
            parsed = None
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract=inv.output_contract,
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    typed_result, active_session = BoundedRepairRuntimeEngine.execute_with_repair(
        session=session,
        invocation=sample_invocation,
        inference_fn=recovering_inference,
        gate_evaluator=gate_evaluator,
    )

    assert active_session.session_id == session.session_id
    assert active_session.run_id == sample_invocation.run_id
    assert active_session.state_id == sample_invocation.state_id
    assert active_session.agent_id == sample_invocation.agent_id
    assert active_session.input_context_sha256 == sample_invocation.capsule_sha256
    assert active_session.terminal_state == "REPAIR_SUCCEEDED"
    assert len(active_session.repair_history) == 1

    # Verify repair record lineage
    record = active_session.repair_history[0]
    assert record.session_id == active_session.session_id
    assert record.attempt_number == 1
    assert record.failure_classification == RepairFailureClassification.RETRYABLE_NARRATIVE_FAILURE


def test_gate3_non_retryable_failures_fail_immediately(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 3: Constitutional / Authority Lane violations fail immediately with NonRetryableFailureError."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=3,
    )

    def illegal_mutation_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        return json.dumps({
            "relationship_type": "EQUIVALENT",
            "confidence_bps": 9900,
            "execute_sql": "DROP TABLE cae.candidates",  # Constitutional violation!
        })

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        parsed = json.loads(raw_text)
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract=inv.output_contract,
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    with pytest.raises(NonRetryableFailureError) as exc_info:
        BoundedRepairRuntimeEngine.execute_with_repair(
            session=session,
            invocation=sample_invocation,
            inference_fn=illegal_mutation_inference,
            gate_evaluator=gate_evaluator,
        )

    assert exc_info.value.reason_code == "NON_RETRYABLE_VIOLATION"
    assert session.attempt_count == 0  # Did not consume retry attempt
    assert session.terminal_state == "FAILED_FATAL"


def test_gate4_every_repair_is_observable(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 4: Every repair attempt generates an immutable RepairAttemptRecord with SHA-256 and diagnostics."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    attempt_counter = 0

    def multi_failure_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter == 1:
            # Failure 1: missing required field
            return json.dumps({"relationship_type": "SUPPORTS"})
        elif attempt_counter == 2:
            # Failure 2: ungrounded evidence
            return json.dumps({
                "relationship_type": "SUPPORTS",
                "confidence_bps": 8500,
                "evidence_refs": ["ev_ghost_999"],
            })
        # Attempt 3: valid
        return json.dumps({
            "relationship_type": "SUPPORTS",
            "confidence_bps": 8500,
            "evidence_refs": ["ev_candidate_101"],
        })

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        parsed = json.loads(raw_text)
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract={
                "contract_id": "contract:canonical-relationship:v1",
                "required_fields": ["relationship_type", "confidence_bps", "evidence_refs"],
            },
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    typed_result, active_session = BoundedRepairRuntimeEngine.execute_with_repair(
        session=session,
        invocation=sample_invocation,
        inference_fn=multi_failure_inference,
        gate_evaluator=gate_evaluator,
    )

    assert len(active_session.repair_history) == 2

    # Check Attempt 1 Record
    rec1 = active_session.repair_history[0]
    assert rec1.attempt_number == 1
    assert rec1.failure_classification == RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE
    assert "required_fields" in rec1.failed_gate_names
    assert len(rec1.attempt_sha256) == 64
    assert "confidence_bps" in rec1.corrective_instruction

    # Check Attempt 2 Record
    rec2 = active_session.repair_history[1]
    assert rec2.attempt_number == 2
    assert rec2.failure_classification == RepairFailureClassification.RETRYABLE_EVIDENCE_FAILURE
    assert "evidence_refs_verifiable" in rec2.failed_gate_names
    assert len(rec2.attempt_sha256) == 64
    assert "ev_ghost_999" in rec2.corrective_instruction


def test_gate5_exhaustion_enters_explicit_failure_state(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 5: Exhaustion transitions deterministically to FAILED_EXHAUSTED state."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=1,
    )

    def failing_inference(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        return json.dumps({"incomplete": "data"})

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        parsed = json.loads(raw_text)
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract={
                "contract_id": "contract:canonical-relationship:v1",
                "required_fields": ["relationship_type"],
            },
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    with pytest.raises(RepairBudgetExhaustedError):
        BoundedRepairRuntimeEngine.execute_with_repair(
            session=session,
            invocation=sample_invocation,
            inference_fn=failing_inference,
            gate_evaluator=gate_evaluator,
        )

    assert session.terminal_state == "FAILED_EXHAUSTED"
    assert session.attempt_count == 2  # 1 initial + 1 retry = 2 attempts


# ---------------------------------------------------------------------------
# False-Proof & Reward-Hacking Defenses
# ---------------------------------------------------------------------------

def test_false_proof_defense_feed_same_failed_output_forever(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """False-Proof Defense 1: Feeding the same failed output forever exhausts budget and terminates cleanly."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=3,
    )

    with pytest.raises(RepairBudgetExhaustedError):
        BoundedRepairRuntimeEngine.execute_with_repair(
            session=session,
            invocation=sample_invocation,
            inference_fn=lambda inv, prior: "INVALID PROSE ONLY",
            gate_evaluator=lambda raw, inv: AgentResultGateEngine.evaluate(
                raw_response_text=raw,
                parsed_json=None,
                output_contract=inv.output_contract,
                invocation=inv,
                verified_evidence_ids=verified_evidence_pool,
            ),
        )

    assert session.attempt_count == 4
    assert session.terminal_state == "FAILED_EXHAUSTED"


def test_false_proof_defense_alter_output_contract_between_attempts(
    sample_invocation: AgentInvocation,
    sample_analyst_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
):
    """False-Proof Defense 2: Altering the output contract between attempts raises RepairContractDriftError."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    # Create mutated invocation with altered contract
    mutated_agent = AgentDefinition(
        agent_id=sample_analyst_agent.agent_id,
        version=sample_analyst_agent.version,
        name=sample_analyst_agent.name,
        purpose=sample_analyst_agent.purpose,
        authority_lane=sample_analyst_agent.authority_lane,
        lifecycle_state=sample_analyst_agent.lifecycle_state,
        model_policy=sample_analyst_agent.model_policy,
        prompt_reference=sample_analyst_agent.prompt_reference,
        output_contract=AgentOutputContract(
            contract_id="contract:MUTATED_DRIFT_CONTRACT:v9",
            output_type="JSON",
            description="Mutated contract",
        ),
    )
    mutated_invocation = AgentInvocationCompiler.compile(
        agent=mutated_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_m55_repair_001",
        state_id="STATE_RELATIONSHIP_CANONICALIZATION",
    )

    with pytest.raises(RepairContractDriftError) as exc_info:
        session.verify_session_integrity(mutated_invocation)

    assert exc_info.value.reason_code == "CONTRACT_DRIFT_DETECTED"


def test_false_proof_defense_retry_constitutional_violation(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """False-Proof Defense 3: Constitutional violations cannot be retried in-session."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=5,
    )

    with pytest.raises(NonRetryableFailureError) as exc_info:
        session.record_failure(
            failure_classification=RepairFailureClassification.NON_RETRYABLE_CONSTITUTIONAL_VIOLATION,
            failed_gates=["authority_lane_parity"],
            failure_reason="Read-only lane attempted SQL write",
            corrective_instruction="N/A",
            input_context_sha256=sample_invocation.invocation_sha256,
        )

    assert exc_info.value.reason_code == "NON_RETRYABLE_VIOLATION"
    assert session.attempt_count == 0


def test_false_proof_defense_reset_attempt_count_prevented(
    sample_invocation: AgentInvocation,
):
    """False-Proof Defense 4: Attempt count increments strictly monotonically across retries."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    rec1 = session.record_failure(
        failure_classification=RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
        failed_gates=["schema_conformance"],
        failure_reason="Schema fail 1",
        corrective_instruction="Fix schema",
        input_context_sha256=sample_invocation.invocation_sha256,
    )
    assert rec1.attempt_number == 1
    assert session.attempt_count == 1

    rec2 = session.record_failure(
        failure_classification=RepairFailureClassification.RETRYABLE_SCHEMA_FAILURE,
        failed_gates=["schema_conformance"],
        failure_reason="Schema fail 2",
        corrective_instruction="Fix schema again",
        input_context_sha256=sample_invocation.invocation_sha256,
    )
    assert rec2.attempt_number == 2
    assert session.attempt_count == 2


# ---------------------------------------------------------------------------
# Concrete Execution Trace Demonstration
# ---------------------------------------------------------------------------

def test_concrete_failure_repair_and_retry_lifecycle_trace(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Demonstrates complete lifecycle: initial failure -> corrective feedback -> successful retry."""
    session = BoundedRepairRuntimeEngine.create_session(
        invocation=sample_invocation,
        max_retries=2,
    )

    attempt_step = 0
    feedback_received_by_agent: List[str] = []

    def mock_model_with_self_repair(inv: AgentInvocation, prior: Optional[RepairAttemptRecord]) -> str:
        nonlocal attempt_step
        attempt_step += 1
        if prior is not None:
            feedback_received_by_agent.append(prior.corrective_instruction)

        if attempt_step == 1:
            # Attempt 1: Model outputs ungrounded citation
            return json.dumps({
                "relationship_type": "SUPPORTS",
                "confidence_bps": 9000,
                "evidence_refs": ["ev_unverified_signal_999"],  # Invalid
            })
        else:
            # Attempt 2: Model self-corrects using feedback
            return json.dumps({
                "relationship_type": "SUPPORTS",
                "confidence_bps": 9500,
                "evidence_refs": ["ev_candidate_101", "ev_candidate_102"],  # Valid
            })

    def gate_evaluator(raw_text: str, inv: AgentInvocation) -> Tuple[TypedAgentResult, AgentResultGateEvaluation]:
        parsed = json.loads(raw_text)
        return AgentResultGateEngine.evaluate(
            raw_response_text=raw_text,
            parsed_json=parsed,
            output_contract={
                "contract_id": "contract:canonical-relationship:v1",
                "required_fields": ["relationship_type", "confidence_bps", "evidence_refs"],
            },
            invocation=inv,
            verified_evidence_ids=verified_evidence_pool,
        )

    typed_result, completed_session = BoundedRepairRuntimeEngine.execute_with_repair(
        session=session,
        invocation=sample_invocation,
        inference_fn=mock_model_with_self_repair,
        gate_evaluator=gate_evaluator,
    )

    # Assertions
    assert isinstance(typed_result, TypedAgentResult)
    assert typed_result.evidence_refs == ("ev_candidate_101", "ev_candidate_102")
    assert completed_session.terminal_state == "REPAIR_SUCCEEDED"
    assert len(completed_session.repair_history) == 1
    assert len(feedback_received_by_agent) == 1
    assert "ev_unverified_signal_999" in feedback_received_by_agent[0]
