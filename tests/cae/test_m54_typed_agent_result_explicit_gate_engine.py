"""Comprehensive Test Suite for CAE Mandate M54: Typed Agent Result + Explicit Gate Engine.

Governed by:
- 01_AGENT_EXECUTION/M54_typed_agent_result_explicit_gate_engine.md
- docs/cae/constitutions/CA-CAN-03_AGENT.yaml
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md

Verifies:
- Gate 1: Invalid schema cannot succeed (SchemaValidationGateError).
- Gate 2: Missing required artifact/evidence refs cannot succeed (EvidenceRefGateError).
- Gate 3: Gate results are individually visible in AgentResultGateEvaluation.
- Gate 4: Agent 'done' text never equals completion (AgentCompletionClaimRejectedError).
- Gate 5: Downstream HandoffValidator interoperability.
- False-Proof Defense 1: Arbitrary valid JSON with wrong schema fails schema gate.
- False-Proof Defense 2: Fake artifact refs in success envelope fail evidence gate.
- False-Proof Defense 3: Plausible narrative without required fields fails required fields gate.
- False-Proof Defense 4: Non-compensable gate failure fails evaluation.
- Concrete Execution Trace: Full end-to-end Invocation -> Inference -> GateEngine -> TypedAgentResult -> HandoffValidator.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List
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
    CapabilityProjection,
    CapabilityScope,
    EvidenceRefGateError,
    GateEvaluationFailedError,
    IndividualGateCheck,
    JITContextCapsule,
    JITContextCompiler,
    RequiredFieldGateError,
    SchemaValidationGateError,
    SkillMaturity,
    SkillPackageRef,
    TypedAgentResult,
)
from cmf_pipeline.workflow.application.handoff_validator import HandoffValidator


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
        run_id="run_m54_eval_001",
        state_id="STATE_RELATIONSHIP_CANONICALIZATION",
    )


@pytest.fixture
def verified_evidence_pool() -> List[str]:
    return ["ev_candidate_101", "ev_candidate_102", "ev_signal_201"]


@pytest.fixture
def verified_artifact_pool() -> List[str]:
    return ["art_knowledge_node_01", "art_knowledge_node_02"]


# ---------------------------------------------------------------------------
# Acceptance Gate Tests
# ---------------------------------------------------------------------------

def test_gate1_invalid_schema_cannot_succeed(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 1: Invalid schema or unparseable JSON fails closed with SchemaValidationGateError."""
    # Unparseable response
    with pytest.raises(SchemaValidationGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text="Error: Internal server error 500",
            parsed_json=None,
            output_contract={"contract_id": "contract:canonical-relationship:v1", "output_type": "JSON"},
            invocation=sample_invocation,
            verified_evidence_ids=verified_evidence_pool,
        )
    assert exc_info.value.reason_code == "SCHEMA_VALIDATION_FAILED"

    # Schema validator rejection
    def strict_schema_validator(payload: Dict[str, Any]) -> bool:
        return "relationship_type" in payload and isinstance(payload.get("confidence_bps"), int)

    with pytest.raises(SchemaValidationGateError) as exc_info2:
        AgentResultGateEngine.evaluate(
            raw_response_text='{"some_other_key": "val"}',
            parsed_json={"some_other_key": "val"},
            output_contract={"contract_id": "contract:canonical-relationship:v1", "output_type": "JSON"},
            invocation=sample_invocation,
            schema_validator=strict_schema_validator,
        )
    assert exc_info2.value.reason_code == "SCHEMA_VALIDATION_FAILED"


def test_gate2_missing_required_artifact_evidence_refs_cannot_succeed(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 2: Missing or ungrounded evidence/artifact references fail closed with EvidenceRefGateError."""
    # Payload citing hallucinated evidence ID
    hallucinated_payload = {
        "relationship_type": "SUPPORTS",
        "confidence_bps": 9000,
        "evidence_refs": ["ev_candidate_101", "ev_hallucinated_ghost_999"],  # Ghost ref!
    }

    with pytest.raises(EvidenceRefGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text=json.dumps(hallucinated_payload),
            parsed_json=hallucinated_payload,
            output_contract={"contract_id": "contract:canonical-relationship:v1", "output_type": "JSON"},
            invocation=sample_invocation,
            verified_evidence_ids=verified_evidence_pool,
        )

    assert exc_info.value.reason_code == "UNVERIFIED_EVIDENCE_REF"
    assert "ev_hallucinated_ghost_999" in exc_info.value.details["invalid_refs"]


def test_gate3_gate_results_are_individually_visible(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 3: Gate results are individually visible in AgentResultGateEvaluation with granular scores."""
    valid_payload = {
        "relationship_type": "CONTRADICTION",
        "confidence_bps": 9500,
        "evidence_refs": ["ev_candidate_101", "ev_candidate_102"],
        "summary": "Direct contradiction identified between statements.",
    }

    typed_result, gate_eval = AgentResultGateEngine.evaluate(
        raw_response_text=json.dumps(valid_payload),
        parsed_json=valid_payload,
        output_contract={
            "contract_id": "contract:canonical-relationship:v1",
            "required_fields": ["relationship_type", "confidence_bps", "evidence_refs"],
        },
        invocation=sample_invocation,
        verified_evidence_ids=verified_evidence_pool,
    )

    assert isinstance(gate_eval, AgentResultGateEvaluation)
    assert len(gate_eval.checks) == 5
    assert gate_eval.all_required_passed is True
    assert gate_eval.composite_score_bps == 10000

    # Verify individual checks are accessible
    anti_narrative_check = gate_eval.get_check("anti_narrative_completion")
    assert anti_narrative_check is not None
    assert anti_narrative_check.passed is True

    schema_check = gate_eval.get_check("schema_conformance")
    assert schema_check is not None
    assert schema_check.passed is True

    required_fields_check = gate_eval.get_check("required_fields")
    assert required_fields_check is not None
    assert required_fields_check.passed is True

    evidence_check = gate_eval.get_check("evidence_refs_verifiable")
    assert evidence_check is not None
    assert evidence_check.passed is True

    authority_check = gate_eval.get_check("authority_lane_parity")
    assert authority_check is not None
    assert authority_check.passed is True


def test_gate4_agent_done_text_never_equals_completion(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 4: Agent output consisting solely of narrative 'done' text is rejected."""
    done_texts = [
        "Done.",
        "Task completed",
        "Finished!",
        "I have completed all tasks.",
        "All tasks done",
    ]

    for done_text in done_texts:
        with pytest.raises(AgentCompletionClaimRejectedError) as exc_info:
            AgentResultGateEngine.evaluate(
                raw_response_text=done_text,
                parsed_json=None,
                output_contract={"contract_id": "contract:canonical-relationship:v1", "output_type": "JSON"},
                invocation=sample_invocation,
                verified_evidence_ids=verified_evidence_pool,
            )
        assert exc_info.value.reason_code == "COMPLETION_CLAIM_REJECTED"


def test_gate5_handoff_validator_downstream_interoperability(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """Gate 5: TypedAgentResult produces a valid handoff payload consumable by HandoffValidator."""
    valid_payload = {
        "relationship_type": "CORROBORATES",
        "confidence_bps": 9200,
        "evidence_refs": ["ev_candidate_101"],
    }

    typed_result, _ = AgentResultGateEngine.evaluate(
        raw_response_text=json.dumps(valid_payload),
        parsed_json=valid_payload,
        output_contract={"contract_id": "contract:canonical-relationship:v1"},
        invocation=sample_invocation,
        verified_evidence_ids=verified_evidence_pool,
    )

    # Convert to bilateral handoff payload
    handoff_payload = typed_result.to_handoff_payload(
        producer_node_id="node_relationship_canonicalization",
        consumer_node_id="node_okf_projection",
    )

    # Validate against Pipeline HandoffValidator
    producer_node = {
        "node_id": "node_relationship_canonicalization",
        "output_contracts": ["contract:canonical-relationship:v1"],
    }
    consumer_node = {
        "node_id": "node_okf_projection",
        "input_contracts": ["contract:canonical-relationship:v1"],
    }

    handoff_val = HandoffValidator()
    validated_handoff = handoff_val.validate(
        handoff_payload,
        producer_node=producer_node,
        consumer_node=consumer_node,
    )

    assert validated_handoff["handoff_id"].startswith("handoff:")
    assert validated_handoff["lifecycle_state"] == "ACCEPTED"
    assert len(validated_handoff["handoff_sha256"]) == 64


# ---------------------------------------------------------------------------
# False-Proof & Reward-Hacking Defenses
# ---------------------------------------------------------------------------

def test_false_proof_defense_arbitrary_json_wrong_schema(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """False-Proof Defense 1: Arbitrary valid JSON with wrong schema fails closed."""
    arbitrary_json = {"unrelated_field": "some_value", "random_num": 42}

    def strict_validator(p: Dict[str, Any]) -> bool:
        return "relationship_type" in p

    with pytest.raises(SchemaValidationGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text=json.dumps(arbitrary_json),
            parsed_json=arbitrary_json,
            output_contract={"contract_id": "contract:canonical-relationship:v1"},
            invocation=sample_invocation,
            schema_validator=strict_validator,
        )

    assert exc_info.value.reason_code == "SCHEMA_VALIDATION_FAILED"


def test_false_proof_defense_fake_artifact_refs_in_success_envelope(
    sample_invocation: AgentInvocation,
    verified_artifact_pool: List[str],
):
    """False-Proof Defense 2: Fake artifact references in success envelope fail closed."""
    fake_artifact_payload = {
        "status": "SUCCESS",
        "relationship_type": "SYNONYMOUS",
        "artifact_refs": ["art_knowledge_node_01", "art_fake_ghost_artifact_99"],  # Fake!
    }

    with pytest.raises(EvidenceRefGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text=json.dumps(fake_artifact_payload),
            parsed_json=fake_artifact_payload,
            output_contract={"contract_id": "contract:canonical-relationship:v1"},
            invocation=sample_invocation,
            verified_artifact_ids=verified_artifact_pool,
        )

    assert exc_info.value.reason_code == "UNVERIFIED_EVIDENCE_REF"


def test_false_proof_defense_plausible_narrative_missing_required_fields(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """False-Proof Defense 3: Plausible narrative missing required fields fails closed."""
    narrative_payload = {
        "commentary": "I analyzed the candidate assertions and found strong thematic alignment across signals.",
        # Missing required 'relationship_type', 'confidence_bps', 'evidence_refs'
    }

    with pytest.raises(RequiredFieldGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text=json.dumps(narrative_payload),
            parsed_json=narrative_payload,
            output_contract={
                "contract_id": "contract:canonical-relationship:v1",
                "required_fields": ["relationship_type", "confidence_bps", "evidence_refs"],
            },
            invocation=sample_invocation,
            verified_evidence_ids=verified_evidence_pool,
        )

    assert exc_info.value.reason_code == "REQUIRED_FIELD_MISSING"


def test_false_proof_defense_authority_lane_mutation_attempt(
    sample_invocation: AgentInvocation,
    verified_evidence_pool: List[str],
):
    """False-Proof Defense 4: Read-only lane agent proposing SQL database mutations fails closed."""
    illegal_mutation_payload = {
        "relationship_type": "EQUIVALENT",
        "confidence_bps": 9900,
        "evidence_refs": ["ev_candidate_101"],
        "execute_sql": "DELETE FROM cae.knowledge_nodes WHERE id = 'node_01'",  # Illegal mutation!
    }

    with pytest.raises(AuthorityGateError) as exc_info:
        AgentResultGateEngine.evaluate(
            raw_response_text=json.dumps(illegal_mutation_payload),
            parsed_json=illegal_mutation_payload,
            output_contract={"contract_id": "contract:canonical-relationship:v1"},
            invocation=sample_invocation,
            verified_evidence_ids=verified_evidence_pool,
        )

    assert exc_info.value.reason_code == "AUTHORITY_LANE_VIOLATION"


# ---------------------------------------------------------------------------
# Concrete Execution Trace Demonstration
# ---------------------------------------------------------------------------

def test_concrete_agent_result_and_gate_evaluation_trace(
    sample_analyst_agent: AgentDefinition,
    sample_context_capsule: JITContextCapsule,
    sample_workspace_id: UUID,
    verified_evidence_pool: List[str],
):
    """Demonstrates complete Agent -> Invocation -> Inference -> GateEngine -> TypedAgentResult -> Handoff."""
    # 1. Compile AgentInvocation
    invocation = AgentInvocationCompiler.compile(
        agent=sample_analyst_agent,
        capsule=sample_context_capsule,
        workspace_id=sample_workspace_id,
        run_id="run_e2e_m54_trace",
        state_id="PHASE_RELATIONSHIP_CANONICALIZATION",
    )
    assert invocation.invocation_sha256 != ""

    # 2. Simulated genuine model inference output conforming to contract
    model_response_payload = {
        "relationship_id": "rel_edge_001",
        "relationship_type": "ELABORATES",
        "source_candidate_id": "cand_101",
        "target_candidate_id": "cand_102",
        "confidence_bps": 9400,
        "evidence_refs": ["ev_candidate_101", "ev_candidate_102"],
        "reasoning": "Candidate 102 provides empirical elaboration of the thesis in Candidate 101.",
    }
    raw_response = json.dumps(model_response_payload)

    # 3. Explicit Gate Engine Evaluation
    typed_result, gate_eval = AgentResultGateEngine.evaluate(
        raw_response_text=raw_response,
        parsed_json=model_response_payload,
        output_contract={
            "contract_id": "contract:canonical-relationship:v1",
            "required_fields": ["relationship_type", "confidence_bps", "evidence_refs"],
        },
        invocation=invocation,
        verified_evidence_ids=verified_evidence_pool,
    )

    # 4. Verify TypedAgentResult
    assert isinstance(typed_result, TypedAgentResult)
    assert typed_result.agent_id == sample_analyst_agent.agent_id
    assert typed_result.lane == AuthorityLane.ANALYST
    assert typed_result.contract_id == "contract:canonical-relationship:v1"
    assert typed_result.evidence_refs == ("ev_candidate_101", "ev_candidate_102")
    assert len(typed_result.result_sha256) == 64

    # 5. Verify Gate Evaluation Evidence
    assert gate_eval.all_required_passed is True
    assert gate_eval.composite_score_bps == 10000
    assert len(gate_eval.evaluation_sha256) == 64

    # 6. Verify Handoff Consumption
    handoff_envelope = typed_result.to_handoff_payload(
        producer_node_id="node_relationship_canonicalization",
        consumer_node_id="node_okf_projection",
    )
    assert handoff_envelope["lifecycle_state"] == "ACCEPTED"
    assert handoff_envelope["contract_id"] == "contract:canonical-relationship:v1"
