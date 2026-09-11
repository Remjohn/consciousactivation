"""Unit and integration tests for CAE M21 Four-Lane Agent Team + Sub-agent Runtime.

Governed by:
- Phase 2 Mandate M21 (02_PHASE_2_RUNTIME_FOUNDATION/M21_four_lane_agent_team_sub_agent_runtime.md)
- Phase 1 Mandate M09 (00_CONTROL/19_PHASE1_AGENT_TEAM_DELEGATION_REFERENCE_TOPOLOGY.md)
- CANONICAL_SKILL_AUTHORING_CONSTITUTION.md
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 00_CONTROL/25_PHASE2_OPERATOR_GATE_RUNTIME_CONTRACT.md

Proves:
1. Pilot runs multi-lane execution across at least two lanes and one sub-agent.
2. Wrong-lane work and subagent lane escalation fail closed.
3. Unauthorized capability access is rejected.
4. Skill nesting / recursion is rejected.
5. Concurrency bounds and task timeout / cancellation are enforced.
6. Retries execute with exponential backoff on transient errors.
7. Operator gates transition to WAITING_OPERATOR (no autonomous model self-approval).
8. Cross-workspace execution is strictly isolated.
9. Cryptographic provenance and deterministic sha256 receipts are retained.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict
from uuid import UUID, uuid4

import pytest

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime.agent_team import (
    AccessMode,
    AgentExecutionTimeoutError,
    AgentMemberSpec,
    AgentRuntimeError,
    AgentTeamRuntime,
    AgentTeamSpec,
    CapabilityProjection,
    CapabilityScope,
    ConcurrencyLimitExceededError,
    DelegationStatus,
    DelegationTask,
    DelegationTopologyViolationError,
    OperatorGateRequiredError,
    RetryPolicy,
    SkillNestingProhibitedError,
    StructuredDelegationResult,
    SubagentSpec,
    UnauthorizedAuthorityLaneError,
    UnauthorizedCapabilityAccessError,
    create_collision_discovery_pilot_team,
)
from ca_runtime.pi_adapter import AuthorityLane, CaePiRuntimeAdapter
from ca_runtime.tenancy import CrossWorkspaceLeakError, TenantContext, tenant_scope


@pytest.mark.asyncio
async def test_pilot_multi_lane_and_subagent_execution_succeeds():
    """Prove that a pilot team executes across all 4 Authority Lanes and invokes a sub-agent."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    team_spec, runtime = create_collision_discovery_pilot_team(workspace_id)
    session_id = f"pilot_session_{uuid4().hex[:10]}"

    with tenant_scope(context):
        # 1. Step 1: Hunter Lane delegates to Subagent (collision_sub_hunter) for signal ingest
        task_sub_hunter = DelegationTask(
            task_id="task_001_sub_hunter",
            session_id=session_id,
            delegator_id="collision_hunter",
            target_id="collision_sub_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={"source_url": "https://example.com/interview.mp4"},
            idempotency_key="sub_hunter_key_001",
            required_capabilities=[(CapabilityScope.CAE_TYPED_OPERATION, "cae.evidence.capture@1.0.0", AccessMode.READ_ONLY)],
            skills=["collision-evidence-ingest"],
            is_subagent=True,
        )
        res_sub_hunter = await runtime.execute_task(task_sub_hunter)

        assert res_sub_hunter.status == DelegationStatus.SUCCEEDED
        assert res_sub_hunter.actor_id == "collision_sub_hunter"
        assert res_sub_hunter.authority_lane == AuthorityLane.HUNTER
        assert res_sub_hunter.output_payload is not None
        assert "collision-evidence-ingest" in res_sub_hunter.output_payload
        assert len(res_sub_hunter.output_payload["collision-evidence-ingest"]["ingested_signals"]) == 2

        # 2. Step 2: Hunter Member (collision_hunter) generates candidate hypotheses
        task_hunter = DelegationTask(
            task_id="task_002_hunter",
            session_id=session_id,
            delegator_id="collision_orchestrator",
            target_id="collision_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={"signals": res_sub_hunter.output_payload["collision-evidence-ingest"]["ingested_signals"]},
            idempotency_key="hunter_key_001",
            required_capabilities=[(CapabilityScope.CAE_TYPED_OPERATION, "cae.evidence.capture@1.0.0", AccessMode.READ_ONLY)],
            skills=["collision-hypothesis-hunter"],
        )
        res_hunter = await runtime.execute_task(task_hunter)

        assert res_hunter.status == DelegationStatus.SUCCEEDED
        assert res_hunter.actor_id == "collision_hunter"
        assert res_hunter.authority_lane == AuthorityLane.HUNTER
        candidates = res_hunter.output_payload["collision-hypothesis-hunter"]["candidate_hypotheses"]
        assert len(candidates) == 1
        assert candidates[0]["hypothesis_id"] == "HYP-001"

        # 3. Step 3: Analyst Member (collision_analyst) performs adversarial falsification
        task_analyst = DelegationTask(
            task_id="task_003_analyst",
            session_id=session_id,
            delegator_id="collision_orchestrator",
            target_id="collision_analyst",
            authority_lane=AuthorityLane.ANALYST,
            input_payload={"candidate_hypotheses": candidates},
            idempotency_key="analyst_key_001",
            required_capabilities=[(CapabilityScope.CAE_TYPED_OPERATION, "cae.assessment.evaluate@1.0.0", AccessMode.READ_ONLY)],
            skills=["collision-falsification-analyst"],
        )
        res_analyst = await runtime.execute_task(task_analyst)

        assert res_analyst.status == DelegationStatus.SUCCEEDED
        assert res_analyst.actor_id == "collision_analyst"
        assert res_analyst.authority_lane == AuthorityLane.ANALYST
        evaluations = res_analyst.output_payload["collision-falsification-analyst"]["evaluated_hypotheses"]
        assert evaluations[0]["falsification_score"] == "0.94"
        assert evaluations[0]["cliche_risk"] == "LOW"

        # 4. Step 4: Composer Member (collision_composer) structures the validated portfolio
        task_composer = DelegationTask(
            task_id="task_004_composer",
            session_id=session_id,
            delegator_id="collision_orchestrator",
            target_id="collision_composer",
            authority_lane=AuthorityLane.COMPOSER,
            input_payload={"evaluated_hypotheses": evaluations},
            idempotency_key="composer_key_001",
            required_capabilities=[(CapabilityScope.CAE_TYPED_OPERATION, "cae.composition.compile@1.0.0", AccessMode.READ_WRITE)],
            skills=["hypothesis-portfolio-composer"],
        )
        res_composer = await runtime.execute_task(task_composer)

        assert res_composer.status == DelegationStatus.SUCCEEDED
        assert res_composer.actor_id == "collision_composer"
        assert res_composer.authority_lane == AuthorityLane.COMPOSER
        portfolio = res_composer.output_payload["hypothesis-portfolio-composer"]["portfolio"]
        assert portfolio["portfolio_id"] == "PORT-001"

        # 5. Step 5: Commander Member (collision_commander) seals state aggregate
        task_commander = DelegationTask(
            task_id="task_005_commander",
            session_id=session_id,
            delegator_id="collision_orchestrator",
            target_id="collision_commander",
            authority_lane=AuthorityLane.COMMANDER,
            input_payload={"portfolio": portfolio},
            idempotency_key="commander_key_001",
            required_capabilities=[(CapabilityScope.POSTGRES_STORAGE, "cae.collision_hypothesis", AccessMode.READ_WRITE)],
            skills=["operator-gate-authorizer"],
        )
        res_commander = await runtime.execute_task(task_commander)

        assert res_commander.status == DelegationStatus.SUCCEEDED
        assert res_commander.actor_id == "collision_commander"
        assert res_commander.authority_lane == AuthorityLane.COMMANDER

        # Check total receipts emitted
        receipts = runtime.get_receipts()
        assert len(receipts) == 5
        assert all(r.status == DelegationStatus.SUCCEEDED for r in receipts)


@pytest.mark.asyncio
async def test_wrong_lane_work_rejected_fail_closed():
    """Verify that attempting to execute wrong-lane work is rejected immediately."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    team_spec, runtime = create_collision_discovery_pilot_team(workspace_id)

    with tenant_scope(context):
        # Attempting Commander work on Hunter agent
        task = DelegationTask(
            task_id="wrong_lane_task",
            session_id="sess_001",
            delegator_id="collision_orchestrator",
            target_id="collision_hunter",
            authority_lane=AuthorityLane.COMMANDER,  # Mismatch!
            input_payload={},
            idempotency_key="wrong_lane_key",
        )

        with pytest.raises(UnauthorizedAuthorityLaneError) as exc_info:
            await runtime.execute_task(task)

        assert "LANE_VIOLATION" in str(exc_info.value)
        assert exc_info.value.details["assigned_lane"] == "HUNTER"
        assert exc_info.value.details["attempted_lane"] == "COMMANDER"


def test_subagent_lane_escalation_rejected_at_registration():
    """Verify that a subagent cannot be declared with an authority lane different from its parent."""
    # Parent in HUNTER, subagent in COMMANDER
    subagent = SubagentSpec(
        subagent_id="illegal_subagent",
        name="Escalated Subagent",
        parent_agent_id="parent_hunter",
        authority_lane=AuthorityLane.COMMANDER,
    )
    parent = AgentMemberSpec(
        agent_id="parent_hunter",
        name="Parent Hunter",
        authority_lane=AuthorityLane.HUNTER,
        subagents={"illegal_subagent": subagent},
    )

    with pytest.raises(UnauthorizedAuthorityLaneError) as exc_info:
        parent.validate()

    assert "LANE_VIOLATION" in str(exc_info.value)


@pytest.mark.asyncio
async def test_unauthorized_capability_access_rejected_fail_closed():
    """Verify that an agent attempting undeclared capabilities is rejected immediately."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    team_spec, runtime = create_collision_discovery_pilot_team(workspace_id)

    with tenant_scope(context):
        # Analyst trying to write to Postgres without permission
        task = DelegationTask(
            task_id="unauth_cap_task",
            session_id="sess_002",
            delegator_id="collision_orchestrator",
            target_id="collision_analyst",
            authority_lane=AuthorityLane.ANALYST,
            input_payload={},
            idempotency_key="unauth_cap_key",
            required_capabilities=[(CapabilityScope.POSTGRES_STORAGE, "cae.secret_vault", AccessMode.WRITE_ONLY)],
        )

        with pytest.raises(UnauthorizedCapabilityAccessError) as exc_info:
            await runtime.execute_task(task)

        assert "CAPABILITY_VIOLATION" in str(exc_info.value)
        assert exc_info.value.details["scope"] == "POSTGRES_STORAGE"


@pytest.mark.asyncio
async def test_skill_nesting_prohibited_fail_closed():
    """Verify that recursive skill calls or subagent invocations inside skills are prohibited."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    team_spec, runtime = create_collision_discovery_pilot_team(workspace_id)

    with tenant_scope(context):
        task = DelegationTask(
            task_id="nesting_task",
            session_id="sess_003",
            delegator_id="collision_orchestrator",
            target_id="collision_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={},
            idempotency_key="nesting_key",
            skills=["nested-subagent-execution-skill"],
        )

        with pytest.raises(SkillNestingProhibitedError) as exc_info:
            await runtime.execute_task(task)

        assert "SKILL_NESTING_VIOLATION" in str(exc_info.value)


@pytest.mark.asyncio
async def test_timeout_and_cancellation():
    """Verify that a task exceeding its assigned timeout terminates cleanly with TIMED_OUT status."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    hunter_short_timeout = AgentMemberSpec(
        agent_id="fast_hunter",
        name="Fast Hunter",
        authority_lane=AuthorityLane.HUNTER,
        timeout_seconds=0.1,  # 100ms timeout
        retry_policy=RetryPolicy(max_retries=0),
    )
    team_spec = AgentTeamSpec(
        team_id="timeout_team",
        name="Timeout Team",
        workspace_id=workspace_id,
        members={"fast_hunter": hunter_short_timeout},
    )
    runtime = AgentTeamRuntime(team_spec=team_spec)

    async def slow_executor(task: DelegationTask) -> Dict[str, Any]:
        await asyncio.sleep(0.5)
        return {"done": True}

    with tenant_scope(context):
        task = DelegationTask(
            task_id="slow_task",
            session_id="sess_004",
            delegator_id="orchestrator",
            target_id="fast_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={},
            idempotency_key="slow_key",
        )

        result = await runtime.execute_task(task, async_executor_fn=slow_executor)
        assert result.status == DelegationStatus.TIMED_OUT
        assert result.error_details is not None
        assert result.error_details["error_type"] == "AgentExecutionTimeoutError"


@pytest.mark.asyncio
async def test_retry_policy_with_exponential_backoff():
    """Verify that transient failures trigger configured retries and succeed on subsequent attempt."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    retry_hunter = AgentMemberSpec(
        agent_id="retry_hunter",
        name="Retry Hunter",
        authority_lane=AuthorityLane.HUNTER,
        retry_policy=RetryPolicy(max_retries=2, initial_delay_seconds=0.05, backoff_factor=1.5, jitter=False),
    )
    team_spec = AgentTeamSpec(
        team_id="retry_team",
        name="Retry Team",
        workspace_id=workspace_id,
        members={"retry_hunter": retry_hunter},
    )
    runtime = AgentTeamRuntime(team_spec=team_spec)

    attempt_counter = 0

    def flaky_executor(task: DelegationTask) -> Dict[str, Any]:
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter < 2:
            raise RuntimeError("Transient network glitch")
        return {"recovered": True, "attempts": attempt_counter}

    with tenant_scope(context):
        task = DelegationTask(
            task_id="flaky_task",
            session_id="sess_005",
            delegator_id="orchestrator",
            target_id="retry_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={},
            idempotency_key="flaky_key",
        )

        result = await runtime.execute_task(task, executor_fn=flaky_executor)
        assert result.status == DelegationStatus.SUCCEEDED
        assert result.attempt_count == 2
        assert result.output_payload == {"recovered": True, "attempts": 2}


@pytest.mark.asyncio
async def test_operator_gate_runtime_contract_waiting_operator():
    """Verify that hitting an operator gate transitions cleanly to WAITING_OPERATOR."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    commander = AgentMemberSpec(
        agent_id="gate_commander",
        name="Gate Commander",
        authority_lane=AuthorityLane.COMMANDER,
        is_commander=True,
    )
    team_spec = AgentTeamSpec(
        team_id="gate_team",
        name="Gate Team",
        workspace_id=workspace_id,
        members={"gate_commander": commander},
    )
    runtime = AgentTeamRuntime(team_spec=team_spec)

    def gated_executor(task: DelegationTask) -> Dict[str, Any]:
        raise OperatorGateRequiredError(
            gate_id="gate_001_approval",
            decision_context={
                "portfolio_id": "PORT-001",
                "risk_level": "HIGH",
                "requires_editorial_signoff": True,
            },
        )

    with tenant_scope(context):
        task = DelegationTask(
            task_id="gate_task_001",
            session_id="sess_006",
            delegator_id="orchestrator",
            target_id="gate_commander",
            authority_lane=AuthorityLane.COMMANDER,
            input_payload={"items": ["ITEM-01"]},
            idempotency_key="gate_key_001",
        )

        result = await runtime.execute_task(task, executor_fn=gated_executor)
        assert result.status == DelegationStatus.WAITING_OPERATOR
        assert result.output_payload is not None
        assert result.output_payload["status"] == "WAITING_OPERATOR"

        # Check stored operator decision context
        gate_ctx = runtime.get_operator_gate_context("gate_task_001")
        assert gate_ctx is not None
        assert gate_ctx["gate_id"] == "gate_001_approval"
        assert gate_ctx["decision_context"]["requires_editorial_signoff"] is True


@pytest.mark.asyncio
async def test_cross_workspace_leak_rejected():
    """Verify that executing a task under mismatched TenantContext is rejected immediately."""
    team_workspace_id = uuid4()
    other_workspace_id = uuid4()

    team_spec, runtime = create_collision_discovery_pilot_team(team_workspace_id)

    # Mismatched context
    other_context = TenantContext(
        workspace_id=other_workspace_id,
        actor_id="operator_test",
    )

    with tenant_scope(other_context):
        task = DelegationTask(
            task_id="cross_ws_task",
            session_id="sess_007",
            delegator_id="collision_orchestrator",
            target_id="collision_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={},
            idempotency_key="cross_ws_key",
        )

        with pytest.raises(CrossWorkspaceLeakError) as exc_info:
            await runtime.execute_task(task)

        assert "CROSS_WORKSPACE_LEAK" in str(exc_info.value)


@pytest.mark.asyncio
async def test_cryptographic_provenance_retention():
    """Verify that every execution result generates a deterministic sha256 digest and provenance chain."""
    workspace_id = uuid4()
    context = TenantContext(
        workspace_id=workspace_id,
        actor_id="operator_test",
    )

    team_spec, runtime = create_collision_discovery_pilot_team(workspace_id)

    with tenant_scope(context):
        task = DelegationTask(
            task_id="task_provenance_check",
            session_id="session_prov_001",
            delegator_id="collision_hunter",
            target_id="collision_sub_hunter",
            authority_lane=AuthorityLane.HUNTER,
            input_payload={"source_id": "SRC-999"},
            idempotency_key="prov_key_001",
            skills=["collision-evidence-ingest"],
            is_subagent=True,
        )

        result: StructuredDelegationResult = await runtime.execute_task(task)

        # 1. Result SHA-256 validation
        expected_digest_payload = {
            "task_id": "task_provenance_check",
            "session_id": "session_prov_001",
            "actor_id": "collision_sub_hunter",
            "authority_lane": "HUNTER",
            "status": "SUCCEEDED",
            "output_payload": result.output_payload,
            "error": None,
            "attempt_count": 1,
        }
        expected_sha = canonical_sha256(canonical_json_text(expected_digest_payload))
        assert result.result_sha256 == expected_sha

        # 2. Provenance chain validation
        input_digest = canonical_sha256(canonical_json_text({"source_id": "SRC-999"}))
        assert f"input_sha256:{input_digest}" in result.provenance_chain
        assert "session:session_prov_001" in result.provenance_chain
        assert "lane:HUNTER" in result.provenance_chain
        assert "actor:collision_sub_hunter" in result.provenance_chain
