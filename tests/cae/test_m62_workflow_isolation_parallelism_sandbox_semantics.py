"""
Unit and Integration Tests for CAE Mandate M62: Workflow Isolation, Parallelism + Sandbox Semantics.

Validates:
- All 5 Acceptance Gates
- All 4 False-proof/Reward-hacking Defense Vectors (§10)
- Sandbox lifecycle and path escape defense
- Idempotent cleanup and receipt generation
- First-success race termination and cancellation propagation
"""

from typing import List, Tuple
import pytest

from ca_runtime.workflow_isolation import (
    ArtifactAttributionMismatchError,
    ArtifactAttributionRecord,
    BranchState,
    CancellationPropagationError,
    CleanupReceipt,
    ConcurrentMutationConflictError,
    IsolationLevel,
    JoinStrategy,
    ParallelBranch,
    ParallelExecutionCoordinator,
    ParallelExecutionReport,
    SandboxIsolationPolicy,
    SandboxPathEscapeError,
    SandboxRecord,
    SandboxState,
    StaleSandboxAccessError,
    TenantSandboxIsolationViolationError,
    WorkflowIsolationError,
    WorkflowSandboxManager,
)


# ============================================================================
# Gate 1 & False-Proof 1: Concurrent Mutation Conflict Defense
# ============================================================================


def test_gate1_and_false_proof_1_concurrent_mutation_conflict_rejected() -> None:
    """Gate 1 & False-Proof 1: Two branches cannot target the same path in the same sandbox without isolation."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_001",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sandbox_1/",),
    )
    manager = WorkflowSandboxManager(policy)
    coordinator = ParallelExecutionCoordinator("exec_001", JoinStrategy.ALL, manager)

    sbx1 = manager.create_sandbox("branch_A", "node_1", "agent_hunter", "/workspace/sandbox_1/")

    # Register first branch
    coordinator.register_branch(
        branch_id="branch_A",
        node_id="node_1",
        agent_id="agent_hunter",
        sandbox_id=sbx1.sandbox_id,
        target_paths=("/workspace/sandbox_1/output.json",),
    )

    # Register conflicting second branch on same sandbox and path
    with pytest.raises(ConcurrentMutationConflictError) as exc_info:
        coordinator.register_branch(
            branch_id="branch_B",
            node_id="node_2",
            agent_id="agent_composer",
            sandbox_id=sbx1.sandbox_id,
            target_paths=("/workspace/sandbox_1/output.json",),
        )
    assert exc_info.value.reason_code == "ERR_CONCURRENT_MUTATION_CONFLICT"


# ============================================================================
# Gate 2 & False-Proof 2: Deterministic Cancellation Propagation
# ============================================================================


def test_gate2_and_false_proof_2_cancellation_propagation() -> None:
    """Gate 2 & False-Proof 2: Cancelling a parent branch cancels child branches and marks sandboxes CANCELLED."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_002",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sandbox_a/", "/workspace/sandbox_b/"),
    )
    manager = WorkflowSandboxManager(policy)
    coordinator = ParallelExecutionCoordinator("exec_002", JoinStrategy.ALL, manager)

    sbx_a = manager.create_sandbox("parent_branch", "node_parent", "agent_1", "/workspace/sandbox_a/")
    sbx_b = manager.create_sandbox("child_branch", "node_child", "agent_2", "/workspace/sandbox_b/")

    parent = coordinator.register_branch(
        branch_id="parent_branch",
        node_id="node_parent",
        agent_id="agent_1",
        sandbox_id=sbx_a.sandbox_id,
        target_paths=("/workspace/sandbox_a/parent.dat",),
    )

    child = coordinator.register_branch(
        branch_id="child_branch",
        node_id="node_child",
        agent_id="agent_2",
        sandbox_id=sbx_b.sandbox_id,
        target_paths=("/workspace/sandbox_b/child.dat",),
    )
    parent.children.append("child_branch")

    coordinator.start_branch("parent_branch")
    coordinator.start_branch("child_branch")

    # Cancel parent
    cancelled_ids = coordinator.cancel_branch("parent_branch")

    assert set(cancelled_ids) == {"parent_branch", "child_branch"}
    assert parent.state == BranchState.CANCELLED
    assert child.state == BranchState.CANCELLED
    assert sbx_a.state == SandboxState.CANCELLED
    assert sbx_b.state == SandboxState.CANCELLED


# ============================================================================
# Gate 3: Cryptographic Artifact Attribution
# ============================================================================


def test_gate3_cryptographic_artifact_attribution() -> None:
    """Gate 3: Every artifact is cryptographically bound to branch, node, agent, and sandbox."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_003",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sbx_attr/",),
    )
    manager = WorkflowSandboxManager(policy)
    sbx = manager.create_sandbox("branch_attr", "node_attr", "agent_composer", "/workspace/sbx_attr/")

    manager.write_file(sbx.sandbox_id, "/workspace/sbx_attr/result.json", "tenant_alpha")

    attr = manager.register_artifact(
        sandbox_id=sbx.sandbox_id,
        artifact_id="art_001",
        branch_id="branch_attr",
        node_id="node_attr",
        agent_id="agent_composer",
        file_path="/workspace/sbx_attr/result.json",
        content_sha256="abcdef1234567890" * 4,
    )

    assert attr.artifact_id == "art_001"
    assert attr.sandbox_id == sbx.sandbox_id
    assert len(attr.attribution_sha256) == 64
    assert len(manager.attributions) == 1


# ============================================================================
# Gate 4: Idempotent Sandbox Cleanup & Receipts
# ============================================================================


def test_gate4_idempotent_sandbox_cleanup() -> None:
    """Gate 4: Sandbox cleanup is idempotent and produces verifiable cleanup receipts."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_004",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sbx_clean/",),
        cleanup_mode="IDEMPOTENT_DELETE",
    )
    manager = WorkflowSandboxManager(policy)
    sbx = manager.create_sandbox("branch_clean", "node_clean", "agent_hunter", "/workspace/sbx_clean/")

    manager.write_file(sbx.sandbox_id, "/workspace/sbx_clean/temp_file.txt", "tenant_alpha")

    # First cleanup
    receipt1 = manager.cleanup_sandbox(sbx.sandbox_id)
    assert receipt1.idempotent
    assert receipt1.sandbox_id == sbx.sandbox_id
    assert "/workspace/sbx_clean/temp_file.txt" in receipt1.cleaned_paths
    assert len(receipt1.receipt_sha256) == 64
    assert sbx.state == SandboxState.CLEANED_UP

    # Second cleanup (idempotent call)
    receipt2 = manager.cleanup_sandbox(sbx.sandbox_id)
    assert receipt2.receipt_sha256 == receipt1.receipt_sha256
    assert sbx.state == SandboxState.CLEANED_UP


# ============================================================================
# Gate 5 & False-Proof 3: First-Success Race Termination
# ============================================================================


def test_gate5_and_false_proof_3_first_success_race_termination() -> None:
    """Gate 5 & False-Proof 3: First completed branch wins; slower branches are cancelled and cleaned."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_005",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/fast/", "/workspace/slow/"),
    )
    manager = WorkflowSandboxManager(policy)
    coordinator = ParallelExecutionCoordinator("exec_race", JoinStrategy.FIRST_SUCCESS, manager)

    sbx_fast = manager.create_sandbox("branch_fast", "node_fast", "agent_1", "/workspace/fast/")
    sbx_slow = manager.create_sandbox("branch_slow", "node_slow", "agent_2", "/workspace/slow/")

    b_fast = coordinator.register_branch(
        "branch_fast", "node_fast", "agent_1", sbx_fast.sandbox_id, ("/workspace/fast/out.json",)
    )
    b_slow = coordinator.register_branch(
        "branch_slow", "node_slow", "agent_2", sbx_slow.sandbox_id, ("/workspace/slow/out.json",)
    )

    coordinator.start_branch("branch_fast")
    coordinator.start_branch("branch_slow")

    # Fast branch finishes first
    coordinator.complete_branch("branch_fast", {"winner": True})

    # Evaluate join
    report = coordinator.evaluate_join()

    assert report.winning_branch_id == "branch_fast"
    assert report.completed_branches == 1
    assert report.cancelled_branches == 1
    assert b_slow.state == BranchState.CANCELLED
    assert sbx_slow.state == SandboxState.CLEANED_UP
    assert len(report.cleanup_receipts) == 1
    assert report.cleanup_receipts[0].sandbox_id == sbx_slow.sandbox_id


# ============================================================================
# False-Proof 4: Tenant Sandbox Isolation Violation
# ============================================================================


def test_false_proof_4_tenant_sandbox_isolation_violation() -> None:
    """False-Proof 4: Attempting to write to another tenant's sandbox fails closed."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_006",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sbx_tenant/",),
    )
    manager = WorkflowSandboxManager(policy)
    sbx = manager.create_sandbox("branch_t", "node_t", "agent_1", "/workspace/sbx_tenant/")

    with pytest.raises(TenantSandboxIsolationViolationError) as exc_info:
        # Attacking tenant "tenant_beta" tries to write to "tenant_alpha" sandbox
        manager.write_file(sbx.sandbox_id, "/workspace/sbx_tenant/attack.txt", "tenant_beta")

    assert exc_info.value.reason_code == "ERR_TENANT_SANDBOX_ISOLATION_VIOLATION"


# ============================================================================
# Sandbox Path Escape & Stale Access Defenses
# ============================================================================


def test_sandbox_path_escape_and_stale_access_defenses() -> None:
    """Verify path escape and stale access rejections."""
    policy = SandboxIsolationPolicy(
        policy_id="pol_007",
        tenant_id="tenant_alpha",
        isolation_level=IsolationLevel.EPHEMERAL_WORKTREE,
        allowed_write_paths=("/workspace/sbx_esc/",),
    )
    manager = WorkflowSandboxManager(policy)
    sbx = manager.create_sandbox("branch_esc", "node_esc", "agent_1", "/workspace/sbx_esc/")

    # 1. Path escape outside sandbox root
    with pytest.raises(SandboxPathEscapeError):
        manager.write_file(sbx.sandbox_id, "/etc/passwd", "tenant_alpha")

    # 2. Stale access after cleanup
    manager.cleanup_sandbox(sbx.sandbox_id)
    with pytest.raises(StaleSandboxAccessError):
        manager.write_file(sbx.sandbox_id, "/workspace/sbx_esc/after_clean.txt", "tenant_alpha")
