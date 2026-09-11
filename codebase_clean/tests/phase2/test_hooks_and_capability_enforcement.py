"""Comprehensive Unit & Fault-Injection Tests for CAE Hooks + Extensions + Capability Enforcement Runtime.

Governed by:
- Phase 2 Mandate M23 (M23_hooks_extensions_capability_enforcement_runtime.md)
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 00_CONTROL/23_PHASE2_EVENT_TRACE_CONTRACT.md
- 00_CONTROL/25_PHASE2_OPERATOR_GATE_RUNTIME_CONTRACT.md
- Phase 1 Mandate M06 (Hook / Extension Guarantee Matrix)
"""

from __future__ import annotations

import tempfile
from typing import Any, Dict, List
from uuid import UUID, uuid4
import pytest

from ca_runtime.context_capsule import AccessMode, CapabilityScope
from ca_runtime.hook_runtime import (
    CapabilityGrant,
    CapabilityPolicyEngine,
    CompletionGateVerificationError,
    HookDecisionRecord,
    HookExecutionDeniedError,
    HookExtensionManager,
    HookOutcome,
    HookPoint,
    OperatorGateReceipt,
    OperatorGateRecord,
    OperatorGateRuntimeEngine,
    OperatorGateStatus,
    OperatorGateRequiredError,
    SandboxSecurityViolationError,
    SelfApprovalProhibitedError,
    UnauthorizedCapabilityAccessError,
)
from ca_runtime.pi_adapter import AuthorityLane, AuthorityLaneMismatchError
from ca_runtime.program_state_runtime import (
    ProgramStateAggregate,
    ProgramStateLifecycle,
    UniversalProgramStateRuntime,
    get_canonical_collision_state_machine,
)
from ca_runtime.state_lifecycle import (
    CausalTraceEventType,
    CausalTraceLedger,
    StateEffectDeclaration,
    EffectKind,
    ReplaySafety,
)
from ca_runtime.tenancy import CrossWorkspaceLeakError, TenantContext


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def workspace_a() -> UUID:
    return uuid4()


@pytest.fixture
def workspace_b() -> UUID:
    return uuid4()


@pytest.fixture
def trace_ledger() -> CausalTraceLedger:
    return CausalTraceLedger()


@pytest.fixture
def policy_engine(workspace_a: UUID) -> CapabilityPolicyEngine:
    engine = CapabilityPolicyEngine()
    # Grant CAE typed operation
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.CAE_TYPED_OPERATION,
            access_mode=AccessMode.MUTATION_OPERATION,
            target="cae.evidence.capture@1.0.0",
            workspace_id=workspace_a,
            allowed_lanes=(AuthorityLane.HUNTER, AuthorityLane.COMMANDER),
        )
    )
    # Grant Filesystem inside sandbox
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.FILESYSTEM,
            access_mode=AccessMode.READ_WRITE,
            target="/workspace/data/*",
            workspace_id=workspace_a,
            sandbox_root="/workspace/data",
        )
    )
    # Grant CLI commands
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.PROCESS_CLI,
            access_mode=AccessMode.READ_ONLY,
            target="git status",
            workspace_id=workspace_a,
            cli_command_allowlist=("git", "python", "pytest"),
        )
    )
    # Grant CLI command requiring operator approval
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.PROCESS_CLI,
            access_mode=AccessMode.MUTATION_OPERATION,
            target="git push origin main",
            workspace_id=workspace_a,
            requires_operator_approval=True,
            cli_command_allowlist=("git",),
        )
    )
    # Grant Network
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.NETWORK,
            access_mode=AccessMode.READ_WRITE,
            target="*",
            workspace_id=workspace_a,
            network_allowlist=("api.consciousactivation.internal",),
        )
    )
    # Grant Secrets
    engine.add_grant(
        CapabilityGrant(
            scope=CapabilityScope.SECRETS,
            access_mode=AccessMode.READ_ONLY,
            target="ref:vault://credentials/transcription_api",
            workspace_id=workspace_a,
        )
    )
    return engine


@pytest.fixture
def hook_manager(policy_engine: CapabilityPolicyEngine, trace_ledger: CausalTraceLedger) -> HookExtensionManager:
    return HookExtensionManager(policy_engine=policy_engine, trace_ledger=trace_ledger)


# ============================================================================
# 1. Capability Security Policy Tests
# ============================================================================

def test_pre_tool_capability_allow_declared_grant(hook_manager: HookExtensionManager, workspace_a: UUID):
    decision = hook_manager.execute_pre_tool_hooks(
        scope=CapabilityScope.CAE_TYPED_OPERATION,
        target="cae.evidence.capture@1.0.0",
        mode=AccessMode.MUTATION_OPERATION,
        actor_id="agent_hunter_1",
        lane=AuthorityLane.HUNTER,
        workspace_id=workspace_a,
    )
    assert decision.outcome == HookOutcome.ALLOW
    assert decision.reason_code == "CAPABILITY_AUTHORIZED"
    assert len(decision.decision_sha256) == 64


def test_pre_tool_capability_deny_undeclared_grant(hook_manager: HookExtensionManager, workspace_a: UUID):
    with pytest.raises(UnauthorizedCapabilityAccessError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.CAE_TYPED_OPERATION,
            target="cae.unauthorized.operation@1.0.0",
            mode=AccessMode.MUTATION_OPERATION,
            actor_id="agent_hunter_1",
            lane=AuthorityLane.HUNTER,
            workspace_id=workspace_a,
        )
    assert "No matching explicit capability grant found" in str(exc_info.value)
    assert exc_info.value.reason_code == "UNAUTHORIZED_CAPABILITY_ACCESS"


def test_pre_tool_capability_deny_lane_mismatch(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Composer lane trying to execute Hunter operation
    with pytest.raises(UnauthorizedCapabilityAccessError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.CAE_TYPED_OPERATION,
            target="cae.evidence.capture@1.0.0",
            mode=AccessMode.MUTATION_OPERATION,
            actor_id="agent_composer_1",
            lane=AuthorityLane.COMPOSER,
            workspace_id=workspace_a,
        )
    assert "not authorized for grant" in str(exc_info.value)


# ============================================================================
# 2. Security Sandboxing Tests
# ============================================================================

def test_filesystem_sandbox_path_traversal_blocked(hook_manager: HookExtensionManager, workspace_a: UUID):
    with pytest.raises(SandboxSecurityViolationError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.FILESYSTEM,
            target="/workspace/data/../../etc/passwd",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_hunter_1",
            lane=AuthorityLane.HUNTER,
            workspace_id=workspace_a,
        )
    assert exc_info.value.violation_type == "PATH_TRAVERSAL_DETECTED"


def test_filesystem_sandbox_out_of_root_blocked(hook_manager: HookExtensionManager, workspace_a: UUID):
    with pytest.raises((SandboxSecurityViolationError, UnauthorizedCapabilityAccessError)):
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.FILESYSTEM,
            target="/var/log/system.log",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_hunter_1",
            lane=AuthorityLane.HUNTER,
            workspace_id=workspace_a,
        )


def test_process_cli_risky_command_blocked(hook_manager: HookExtensionManager, workspace_a: UUID):
    with pytest.raises(SandboxSecurityViolationError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.PROCESS_CLI,
            target="git status ; rm -rf /",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_analyst_1",
            lane=AuthorityLane.ANALYST,
            workspace_id=workspace_a,
        )
    assert exc_info.value.violation_type == "RISKY_CLI_COMMAND_DETECTED"


def test_network_allowlist_and_protocol_restriction(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Forbidden protocol (file://)
    with pytest.raises(SandboxSecurityViolationError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.NETWORK,
            target="file:///etc/shadow",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_analyst_1",
            lane=AuthorityLane.ANALYST,
            workspace_id=workspace_a,
        )
    assert exc_info.value.violation_type == "FORBIDDEN_NETWORK_PROTOCOL"

    # Non-whitelisted host
    with pytest.raises(SandboxSecurityViolationError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.NETWORK,
            target="https://unauthorized-evil-server.com/api",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_analyst_1",
            lane=AuthorityLane.ANALYST,
            workspace_id=workspace_a,
        )
    assert exc_info.value.violation_type == "UNAUTHORIZED_NETWORK_HOST"


def test_secrets_raw_access_blocked_named_ref_allowed(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Allowed named ref
    decision = hook_manager.execute_pre_tool_hooks(
        scope=CapabilityScope.SECRETS,
        target="ref:vault://credentials/transcription_api",
        mode=AccessMode.READ_ONLY,
        actor_id="agent_analyst_1",
        lane=AuthorityLane.ANALYST,
        workspace_id=workspace_a,
    )
    assert decision.outcome == HookOutcome.ALLOW

    # Prohibited raw secret attempt
    with pytest.raises(UnauthorizedCapabilityAccessError):
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.SECRETS,
            target="SECRET_API_KEY_VALUE_RAW",
            mode=AccessMode.READ_ONLY,
            actor_id="agent_analyst_1",
            lane=AuthorityLane.ANALYST,
            workspace_id=workspace_a,
        )


# ============================================================================
# 3. Durable Operator Gate Runtime Tests
# ============================================================================

def test_operator_gate_creation_and_pause(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Executing risky command triggers Operator Gate requirement
    with pytest.raises(OperatorGateRequiredError) as exc_info:
        hook_manager.execute_pre_tool_hooks(
            scope=CapabilityScope.PROCESS_CLI,
            target="git push origin main",
            mode=AccessMode.MUTATION_OPERATION,
            actor_id="agent_commander_1",
            lane=AuthorityLane.COMMANDER,
            workspace_id=workspace_a,
            state_aggregate_id="agg_test_001",
            command_payload={"branch": "main", "remote": "origin"},
        )

    gate_id = exc_info.value.gate_id
    assert gate_id.startswith("gate_")
    gate = hook_manager.operator_gate_runtime.get_gate(gate_id)
    assert gate is not None
    assert gate.status == OperatorGateStatus.PENDING
    assert gate.requester_id == "agent_commander_1"


def test_operator_gate_anti_self_approval_blocked(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Create gate
    gate = hook_manager.operator_gate_runtime.create_operator_gate(
        workspace_id=workspace_a,
        state_aggregate_id="agg_test_001",
        operation_id="git push origin main",
        decision_context={"target": "production"},
        requester_id="agent_model_requester",
    )

    # Requester attempting to approve own gate is strictly blocked
    requester_context = TenantContext(
        workspace_id=workspace_a,
        actor_id="agent_model_requester",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id="grant_op_requester",
    )

    with pytest.raises(SelfApprovalProhibitedError) as exc_info:
        hook_manager.operator_gate_runtime.submit_operator_decision(
            gate_id=gate.gate_id,
            decision="APPROVED",
            context=requester_context,
        )
    assert exc_info.value.gate_id == gate.gate_id
    assert exc_info.value.reason_code == "SELF_APPROVAL_PROHIBITED"


def test_operator_gate_authenticated_approval_resumes(hook_manager: HookExtensionManager, workspace_a: UUID):
    gate = hook_manager.operator_gate_runtime.create_operator_gate(
        workspace_id=workspace_a,
        state_aggregate_id="agg_test_001",
        operation_id="git push origin main",
        decision_context={"target": "production"},
        requester_id="agent_model_requester",
    )

    operator_context = TenantContext(
        workspace_id=workspace_a,
        actor_id="human_operator_john",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id="grant_op_123",
    )

    receipt = hook_manager.operator_gate_runtime.submit_operator_decision(
        gate_id=gate.gate_id,
        decision="APPROVED",
        context=operator_context,
        decision_notes="Approved release for production tag v1.0.0",
    )

    assert receipt.decision == "APPROVED"
    assert receipt.decided_by == "human_operator_john"
    assert len(receipt.receipt_sha256) == 64

    # Gate status is now APPROVED
    updated_gate = hook_manager.operator_gate_runtime.get_gate(gate.gate_id)
    assert updated_gate.status == OperatorGateStatus.APPROVED

    # Idempotent re-submission returns identical receipt
    receipt2 = hook_manager.operator_gate_runtime.submit_operator_decision(
        gate_id=gate.gate_id,
        decision="APPROVED",
        context=operator_context,
    )
    assert receipt2.receipt_id == receipt.receipt_id


def test_operator_gate_cross_workspace_approval_blocked(
    hook_manager: HookExtensionManager, workspace_a: UUID, workspace_b: UUID
):
    gate = hook_manager.operator_gate_runtime.create_operator_gate(
        workspace_id=workspace_a,
        state_aggregate_id="agg_test_001",
        operation_id="git push origin main",
        decision_context={"target": "production"},
        requester_id="agent_model_requester",
    )

    # Operator in different workspace
    other_ws_operator = TenantContext(
        workspace_id=workspace_b,
        actor_id="human_operator_other",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id="grant_op_other",
    )

    with pytest.raises(CrossWorkspaceLeakError):
        hook_manager.operator_gate_runtime.submit_operator_decision(
            gate_id=gate.gate_id,
            decision="APPROVED",
            context=other_ws_operator,
        )


# ============================================================================
# 4. Completion & Recovery Hook Tests
# ============================================================================

def test_completion_hook_blocks_missing_evidence(hook_manager: HookExtensionManager, workspace_a: UUID):
    agg = ProgramStateAggregate(
        aggregate_id="agg_test_complete",
        workspace_id=str(workspace_a),
        cae_run_id="run_complete_001",
        program_id="collision_discovery_program",
        program_version="1.0.0",
        current_state="ANALYSIS_COMPLETED",
        state_data={},
        version=5,
        state_hash="a" * 64,
        lifecycle=ProgramStateLifecycle.RUNNING,
        last_receipt_id="rcpt_prev_001",
        created_at="2026-08-31T00:00:00Z",
        updated_at="2026-08-31T00:00:00Z",
    )

    # Missing receipts and unapproved gate
    with pytest.raises(CompletionGateVerificationError) as exc_info:
        hook_manager.execute_completion_hooks(
            aggregate=agg,
            required_receipt_ids=[],
            required_gate_ids=["gate_unapproved_123"],
        )
    assert "REQUIRED_RECEIPTS_EMPTY" in exc_info.value.missing_criteria
    assert "UNAPPROVED_OPERATOR_GATE:gate_unapproved_123" in exc_info.value.missing_criteria


def test_completion_hook_allows_with_complete_proof(hook_manager: HookExtensionManager, workspace_a: UUID):
    # 1. Create and approve gate
    gate = hook_manager.operator_gate_runtime.create_operator_gate(
        workspace_id=workspace_a,
        state_aggregate_id="agg_test_complete",
        operation_id="cae.approval.confirm@1.0.0",
        decision_context={"review": "pass"},
        requester_id="agent_requester",
    )
    op_ctx = TenantContext(
        workspace_id=workspace_a,
        actor_id="human_op",
        role="OPERATOR",
        is_operator=True,
        operator_grant_id="grant_op_123",
    )
    hook_manager.operator_gate_runtime.submit_operator_decision(
        gate_id=gate.gate_id,
        decision="APPROVED",
        context=op_ctx,
    )

    agg = ProgramStateAggregate(
        aggregate_id="agg_test_complete",
        workspace_id=str(workspace_a),
        cae_run_id="run_complete_001",
        program_id="collision_discovery_program",
        program_version="1.0.0",
        current_state="ANALYSIS_COMPLETED",
        state_data={},
        version=5,
        state_hash="a" * 64,
        lifecycle=ProgramStateLifecycle.RUNNING,
        last_receipt_id="rcpt_prev_001",
        created_at="2026-08-31T00:00:00Z",
        updated_at="2026-08-31T00:00:00Z",
    )

    decision = hook_manager.execute_completion_hooks(
        aggregate=agg,
        required_receipt_ids=["rcpt_op_1", "rcpt_op_2"],
        required_gate_ids=[gate.gate_id],
        context=op_ctx,
    )

    assert decision.outcome == HookOutcome.ALLOW
    assert decision.reason_code == "COMPLETION_EVIDENCE_SATISFIED"


def test_recovery_hook_routes_on_failure(hook_manager: HookExtensionManager, workspace_a: UUID):
    runtime = UniversalProgramStateRuntime()
    sm = get_canonical_collision_state_machine()
    runtime.register_state_machine(sm)

    agg = runtime.initialize_program_state(
        program_id="collision_discovery_program",
        workspace_id=workspace_a,
        actor_id="test_actor",
    )

    error = RuntimeError("Database connection timeout during mutation")
    decision = hook_manager.execute_recovery_hooks(
        aggregate_id=agg.aggregate_id,
        workspace_id=workspace_a,
        actor_id="test_actor",
        error=error,
        state_runtime=runtime,
    )

    assert decision.outcome == HookOutcome.REPAIR_REQUIRED
    assert decision.reason_code == "REPAIR_ROUTING_ACTIVATED"

    # State aggregate transitioned to REPAIRING
    repaired_agg = runtime.get_aggregate(agg.aggregate_id)
    assert repaired_agg.lifecycle == ProgramStateLifecycle.REPAIRING


# ============================================================================
# 5. Custom Hook Extension & Trace Tests
# ============================================================================

def test_custom_hook_registration_and_priority_execution(hook_manager: HookExtensionManager, workspace_a: UUID):
    execution_order: List[str] = []

    def hook_first(**kwargs) -> HookDecisionRecord:
        execution_order.append("first")
        from ca_runtime.hook_runtime import _create_hook_decision_record
        return _create_hook_decision_record(
            hook_point=HookPoint.PRE_TOOL,
            hook_name="first_hook",
            outcome=HookOutcome.ALLOW,
            reason_code="FIRST_OK",
            target=kwargs.get("target", ""),
            actor_id=kwargs.get("actor_id", ""),
            lane=kwargs.get("lane", AuthorityLane.HUNTER).value,
            workspace_id=kwargs.get("workspace_id", workspace_a),
        )

    def hook_second(**kwargs) -> HookDecisionRecord:
        execution_order.append("second")
        from ca_runtime.hook_runtime import _create_hook_decision_record
        return _create_hook_decision_record(
            hook_point=HookPoint.PRE_TOOL,
            hook_name="second_hook",
            outcome=HookOutcome.ALLOW,
            reason_code="SECOND_OK",
            target=kwargs.get("target", ""),
            actor_id=kwargs.get("actor_id", ""),
            lane=kwargs.get("lane", AuthorityLane.HUNTER).value,
            workspace_id=kwargs.get("workspace_id", workspace_a),
        )

    hook_manager.register_hook(HookPoint.PRE_TOOL, "second_hook", hook_second, priority=20)
    hook_manager.register_hook(HookPoint.PRE_TOOL, "first_hook", hook_first, priority=10)

    decision = hook_manager.execute_pre_tool_hooks(
        scope=CapabilityScope.CAE_TYPED_OPERATION,
        target="cae.evidence.capture@1.0.0",
        mode=AccessMode.MUTATION_OPERATION,
        actor_id="agent_hunter_1",
        lane=AuthorityLane.HUNTER,
        workspace_id=workspace_a,
    )

    assert decision.outcome == HookOutcome.ALLOW
    assert execution_order == ["first", "second"]


def test_hook_decisions_recorded_in_causal_trace(hook_manager: HookExtensionManager, workspace_a: UUID):
    # Run pre-tool, post-mutation, and completion
    hook_manager.execute_pre_tool_hooks(
        scope=CapabilityScope.CAE_TYPED_OPERATION,
        target="cae.evidence.capture@1.0.0",
        mode=AccessMode.MUTATION_OPERATION,
        actor_id="agent_hunter_1",
        lane=AuthorityLane.HUNTER,
        workspace_id=workspace_a,
    )

    hook_manager.execute_post_mutation_hooks(
        target="cae.evidence.capture@1.0.0",
        actor_id="agent_hunter_1",
        lane=AuthorityLane.HUNTER,
        workspace_id=workspace_a,
        mutation_result={"status": "captured"},
    )

    history = hook_manager.get_decision_history()
    assert len(history) >= 2
    for record in history:
        assert record.decision_sha256 is not None
        assert len(record.decision_sha256) == 64
