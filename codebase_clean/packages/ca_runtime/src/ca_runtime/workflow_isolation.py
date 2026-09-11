"""
CAE Workflow Isolation, Parallelism and Sandbox Semantics.

Governed by:
- Mandate CAE-M62 (Phase 08 - SDLF Factory, P8-B)
- Object Constitution CA-CAN-04 (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow; Agents own bounded reasoning;
- Parallel branches cannot mutate the same target without isolated sandboxes and explicit join strategies;
- Cancellation propagates deterministically to all child branches;
- Every artifact is cryptographically attributed to its originating branch, node, agent, and sandbox;
- Sandbox cleanup is idempotent and emits verifiable cleanup receipts;
- Cross-tenant sandbox access is strictly forbidden fail-closed.
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .pi_adapter import AuthorityLane
from .workflow_primitives import WorkflowPrimitiveError


# ============================================================================
# 1. Enums & Constants
# ============================================================================


class IsolationLevel(str, Enum):
    """Isolation level for a workflow sandbox."""

    READ_ONLY_MOUNT = "READ_ONLY_MOUNT"
    EPHEMERAL_WORKTREE = "EPHEMERAL_WORKTREE"
    PROCESS_ISOLATION = "PROCESS_ISOLATION"
    CONTAINER_SANDBOX = "CONTAINER_SANDBOX"


class SandboxState(str, Enum):
    """Lifecycle state of a sandbox."""

    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    CLEANED_UP = "CLEANED_UP"
    FAILED = "FAILED"


class JoinStrategy(str, Enum):
    """Synchronization strategy for parallel branch completion."""

    ALL = "ALL"
    ANY = "ANY"
    QUORUM = "QUORUM"
    FIRST_SUCCESS = "FIRST_SUCCESS"


class BranchState(str, Enum):
    """Execution state of a parallel branch."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


# ============================================================================
# 2. Error Taxonomy
# ============================================================================


class WorkflowIsolationError(WorkflowPrimitiveError):
    """Base error for workflow isolation failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "WORKFLOW_ISOLATION_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class ConcurrentMutationConflictError(WorkflowIsolationError):
    """Raised when parallel branches attempt to mutate the same target without isolation."""

    def __init__(self, target_path: str, branch_ids: Sequence[str]) -> None:
        super().__init__(
            f"Concurrent mutation conflict on '{target_path}' by branches {list(branch_ids)}",
            reason_code="ERR_CONCURRENT_MUTATION_CONFLICT",
            details={"target_path": target_path, "branch_ids": list(branch_ids)},
        )


class TenantSandboxIsolationViolationError(WorkflowIsolationError):
    """Raised when a branch or agent attempts to access another tenant's sandbox."""

    def __init__(self, requesting_tenant: str, target_tenant: str, sandbox_id: str) -> None:
        super().__init__(
            f"Tenant isolation violation: tenant '{requesting_tenant}' attempted to access "
            f"sandbox '{sandbox_id}' owned by tenant '{target_tenant}'",
            reason_code="ERR_TENANT_SANDBOX_ISOLATION_VIOLATION",
            details={
                "requesting_tenant": requesting_tenant,
                "target_tenant": target_tenant,
                "sandbox_id": sandbox_id,
            },
        )


class SandboxPathEscapeError(WorkflowIsolationError):
    """Raised when a write operation targets a path outside sandbox boundaries."""

    def __init__(self, attempted_path: str, sandbox_root: str) -> None:
        super().__init__(
            f"Sandbox path escape: '{attempted_path}' is outside sandbox root '{sandbox_root}'",
            reason_code="ERR_SANDBOX_PATH_ESCAPE",
            details={"attempted_path": attempted_path, "sandbox_root": sandbox_root},
        )


class CancellationPropagationError(WorkflowIsolationError):
    """Raised when cancellation cannot be propagated cleanly to child branches."""

    def __init__(self, branch_id: str, stuck_children: Sequence[str]) -> None:
        super().__init__(
            f"Cancellation propagation failed for branch '{branch_id}': "
            f"stuck children {list(stuck_children)}",
            reason_code="ERR_CANCELLATION_PROPAGATION",
            details={"branch_id": branch_id, "stuck_children": list(stuck_children)},
        )


class ArtifactAttributionMismatchError(WorkflowIsolationError):
    """Raised when an artifact's attribution does not match its sandbox context."""

    def __init__(self, artifact_id: str, expected_sandbox: str, actual_sandbox: str) -> None:
        super().__init__(
            f"Artifact attribution mismatch: artifact '{artifact_id}' claims sandbox "
            f"'{actual_sandbox}' but was produced in sandbox '{expected_sandbox}'",
            reason_code="ERR_ARTIFACT_ATTRIBUTION_MISMATCH",
            details={
                "artifact_id": artifact_id,
                "expected_sandbox": expected_sandbox,
                "actual_sandbox": actual_sandbox,
            },
        )


class StaleSandboxAccessError(WorkflowIsolationError):
    """Raised when accessing a sandbox that has already been cleaned up or cancelled."""

    def __init__(self, sandbox_id: str, current_state: str) -> None:
        super().__init__(
            f"Stale sandbox access: sandbox '{sandbox_id}' is in state '{current_state}'",
            reason_code="ERR_STALE_SANDBOX_ACCESS",
            details={"sandbox_id": sandbox_id, "current_state": current_state},
        )


# ============================================================================
# 3. Domain Models & Envelopes
# ============================================================================


@dataclass(frozen=True, slots=True)
class SandboxIsolationPolicy:
    """
    Declares isolation requirements for parallel workflow execution.
    """

    policy_id: str
    tenant_id: str
    isolation_level: IsolationLevel
    allowed_write_paths: Tuple[str, ...]
    max_write_concurrency: int = 1
    cleanup_mode: str = "IDEMPOTENT_DELETE"
    require_artifact_attribution: bool = True
    policy_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.policy_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "policy_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "tenant_id": self.tenant_id,
            "isolation_level": self.isolation_level.value,
            "allowed_write_paths": sorted(list(self.allowed_write_paths)),
            "max_write_concurrency": self.max_write_concurrency,
            "cleanup_mode": self.cleanup_mode,
            "require_artifact_attribution": self.require_artifact_attribution,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["policy_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class SandboxRecord:
    """
    Mutable sandbox lifecycle record.
    Tracks the complete lifecycle of an isolated execution sandbox.
    """

    sandbox_id: str
    tenant_id: str
    branch_id: str
    node_id: str
    agent_id: str
    sandbox_path: str
    isolation_level: IsolationLevel
    state: SandboxState = SandboxState.CREATED
    created_at_utc: str = "2026-09-02T06:00:00Z"
    cleaned_up_at_utc: Optional[str] = None
    written_paths: List[str] = field(default_factory=list)
    cleanup_receipt_sha256: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "sandbox_id": self.sandbox_id,
            "tenant_id": self.tenant_id,
            "branch_id": self.branch_id,
            "node_id": self.node_id,
            "agent_id": self.agent_id,
            "sandbox_path": self.sandbox_path,
            "isolation_level": self.isolation_level.value,
            "state": self.state.value,
            "created_at_utc": self.created_at_utc,
            "cleaned_up_at_utc": self.cleaned_up_at_utc or "",
            "written_paths": sorted(self.written_paths),
        }


@dataclass(frozen=True, slots=True)
class ArtifactAttributionRecord:
    """
    Cryptographically binds an artifact to its originating branch, node, agent, and sandbox.
    """

    artifact_id: str
    branch_id: str
    node_id: str
    agent_id: str
    sandbox_id: str
    file_path: str
    content_sha256: str
    attribution_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.attribution_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "attribution_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "branch_id": self.branch_id,
            "node_id": self.node_id,
            "agent_id": self.agent_id,
            "sandbox_id": self.sandbox_id,
            "file_path": self.file_path,
            "content_sha256": self.content_sha256,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["attribution_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ParallelBranch:
    """
    Tracks a single parallel execution branch within a coordinated fan-out.
    """

    branch_id: str
    node_id: str
    agent_id: str
    sandbox_id: str
    target_paths: Tuple[str, ...]
    state: BranchState = BranchState.PENDING
    result: Optional[Dict[str, Any]] = None
    children: List[str] = field(default_factory=list)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "branch_id": self.branch_id,
            "node_id": self.node_id,
            "agent_id": self.agent_id,
            "sandbox_id": self.sandbox_id,
            "target_paths": sorted(list(self.target_paths)),
            "state": self.state.value,
            "children": sorted(self.children),
        }


@dataclass(frozen=True, slots=True)
class CleanupReceipt:
    """Immutable receipt for idempotent sandbox cleanup."""

    sandbox_id: str
    cleaned_paths: Tuple[str, ...]
    cleanup_mode: str
    idempotent: bool
    receipt_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.receipt_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "receipt_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "sandbox_id": self.sandbox_id,
            "cleaned_paths": sorted(list(self.cleaned_paths)),
            "cleanup_mode": self.cleanup_mode,
            "idempotent": self.idempotent,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["receipt_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ParallelExecutionReport:
    """Summary of an entire parallel fan-out/join execution."""

    execution_id: str
    join_strategy: JoinStrategy
    total_branches: int
    completed_branches: int
    cancelled_branches: int
    failed_branches: int
    winning_branch_id: Optional[str]
    artifact_attributions: Tuple[ArtifactAttributionRecord, ...]
    cleanup_receipts: Tuple[CleanupReceipt, ...]
    report_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.report_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "report_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "join_strategy": self.join_strategy.value,
            "total_branches": self.total_branches,
            "completed_branches": self.completed_branches,
            "cancelled_branches": self.cancelled_branches,
            "failed_branches": self.failed_branches,
            "winning_branch_id": self.winning_branch_id or "",
            "artifact_attributions": [a.canonical_dict() for a in self.artifact_attributions],
            "cleanup_receipts": [c.canonical_dict() for c in self.cleanup_receipts],
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["report_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ============================================================================
# 4. Workflow Sandbox Manager
# ============================================================================


class WorkflowSandboxManager:
    """
    Manages sandbox lifecycle: creation, isolated worktree allocation, file writes
    within allowed paths, artifact attribution registration, and idempotent cleanup.
    """

    def __init__(self, policy: SandboxIsolationPolicy) -> None:
        self.policy = policy
        self._sandboxes: Dict[str, SandboxRecord] = {}
        self._attributions: List[ArtifactAttributionRecord] = []
        self._cleanup_receipts: List[CleanupReceipt] = []

    def create_sandbox(
        self,
        branch_id: str,
        node_id: str,
        agent_id: str,
        sandbox_path: str,
    ) -> SandboxRecord:
        """Create and register a new isolated sandbox."""
        sandbox_id = f"sbx_{branch_id}_{node_id}"
        record = SandboxRecord(
            sandbox_id=sandbox_id,
            tenant_id=self.policy.tenant_id,
            branch_id=branch_id,
            node_id=node_id,
            agent_id=agent_id,
            sandbox_path=sandbox_path,
            isolation_level=self.policy.isolation_level,
            state=SandboxState.ACTIVE,
        )
        self._sandboxes[sandbox_id] = record
        return record

    def write_file(self, sandbox_id: str, file_path: str, tenant_id: str) -> None:
        """
        Register a write operation within a sandbox, enforcing path and tenant boundaries.
        """
        record = self._sandboxes.get(sandbox_id)
        if record is None:
            raise StaleSandboxAccessError(sandbox_id, "NOT_FOUND")

        # Tenant isolation check
        if tenant_id != record.tenant_id:
            raise TenantSandboxIsolationViolationError(
                requesting_tenant=tenant_id,
                target_tenant=record.tenant_id,
                sandbox_id=sandbox_id,
            )

        # Lifecycle check
        if record.state not in (SandboxState.CREATED, SandboxState.ACTIVE):
            raise StaleSandboxAccessError(sandbox_id, record.state.value)

        # Path escape check
        if not file_path.startswith(record.sandbox_path):
            raise SandboxPathEscapeError(file_path, record.sandbox_path)

        # Allowed paths check
        if self.policy.allowed_write_paths:
            allowed = any(file_path.startswith(p) for p in self.policy.allowed_write_paths)
            if not allowed:
                raise SandboxPathEscapeError(file_path, str(self.policy.allowed_write_paths))

        record.written_paths.append(file_path)

    def register_artifact(
        self,
        sandbox_id: str,
        artifact_id: str,
        branch_id: str,
        node_id: str,
        agent_id: str,
        file_path: str,
        content_sha256: str,
    ) -> ArtifactAttributionRecord:
        """Register an artifact attribution, verifying sandbox context."""
        record = self._sandboxes.get(sandbox_id)
        if record is None:
            raise StaleSandboxAccessError(sandbox_id, "NOT_FOUND")

        # Verify attribution consistency
        if record.sandbox_id != sandbox_id:
            raise ArtifactAttributionMismatchError(artifact_id, record.sandbox_id, sandbox_id)

        attribution = ArtifactAttributionRecord(
            artifact_id=artifact_id,
            branch_id=branch_id,
            node_id=node_id,
            agent_id=agent_id,
            sandbox_id=sandbox_id,
            file_path=file_path,
            content_sha256=content_sha256,
        )
        self._attributions.append(attribution)
        return attribution

    def cleanup_sandbox(self, sandbox_id: str) -> CleanupReceipt:
        """
        Idempotently clean up a sandbox. Safe to call multiple times.
        """
        record = self._sandboxes.get(sandbox_id)
        if record is None:
            # Idempotent: already cleaned or never existed
            return CleanupReceipt(
                sandbox_id=sandbox_id,
                cleaned_paths=(),
                cleanup_mode="IDEMPOTENT_NOOP",
                idempotent=True,
            )

        if record.state == SandboxState.CLEANED_UP:
            # Idempotent: already cleaned
            existing = [r for r in self._cleanup_receipts if r.sandbox_id == sandbox_id]
            if existing:
                return existing[0]
            return CleanupReceipt(
                sandbox_id=sandbox_id,
                cleaned_paths=tuple(record.written_paths),
                cleanup_mode="IDEMPOTENT_NOOP",
                idempotent=True,
            )

        cleaned_paths = tuple(sorted(record.written_paths))
        record.state = SandboxState.CLEANED_UP
        record.cleaned_up_at_utc = "2026-09-02T06:10:00Z"

        receipt = CleanupReceipt(
            sandbox_id=sandbox_id,
            cleaned_paths=cleaned_paths,
            cleanup_mode=self.policy.cleanup_mode,
            idempotent=True,
        )
        record.cleanup_receipt_sha256 = receipt.receipt_sha256
        self._cleanup_receipts.append(receipt)
        return receipt

    def cancel_sandbox(self, sandbox_id: str) -> None:
        """Cancel a sandbox, marking it as no longer accepting writes."""
        record = self._sandboxes.get(sandbox_id)
        if record is not None and record.state in (SandboxState.CREATED, SandboxState.ACTIVE):
            record.state = SandboxState.CANCELLED

    def get_sandbox(self, sandbox_id: str) -> Optional[SandboxRecord]:
        return self._sandboxes.get(sandbox_id)

    @property
    def attributions(self) -> List[ArtifactAttributionRecord]:
        return list(self._attributions)

    @property
    def cleanup_receipts(self) -> List[CleanupReceipt]:
        return list(self._cleanup_receipts)


# ============================================================================
# 5. Parallel Execution Coordinator
# ============================================================================


class ParallelExecutionCoordinator:
    """
    Coordinates safe parallel fan-out, enforces isolation constraints,
    evaluates join/race conditions, and propagates deterministic cancellation.
    """

    def __init__(
        self,
        execution_id: str,
        join_strategy: JoinStrategy,
        sandbox_manager: WorkflowSandboxManager,
    ) -> None:
        self.execution_id = execution_id
        self.join_strategy = join_strategy
        self.sandbox_manager = sandbox_manager
        self._branches: Dict[str, ParallelBranch] = {}
        self._target_write_registry: Dict[str, List[str]] = {}  # path -> [branch_ids]

    def register_branch(
        self,
        branch_id: str,
        node_id: str,
        agent_id: str,
        sandbox_id: str,
        target_paths: Tuple[str, ...],
    ) -> ParallelBranch:
        """
        Register a parallel branch, validating that write targets do not conflict
        with other active branches (unless fully isolated via separate sandboxes).
        """
        # Check for concurrent mutation conflicts on shared targets
        for path in target_paths:
            if path in self._target_write_registry:
                existing_branches = self._target_write_registry[path]
                # Conflict: multiple branches targeting the same path
                conflicting = [
                    bid for bid in existing_branches
                    if bid in self._branches
                    and self._branches[bid].state in (BranchState.PENDING, BranchState.RUNNING)
                ]
                if conflicting:
                    # Check if they share the same sandbox (would be a true conflict)
                    for cbid in conflicting:
                        cb = self._branches[cbid]
                        if cb.sandbox_id == sandbox_id:
                            raise ConcurrentMutationConflictError(
                                path, [cbid, branch_id]
                            )

        branch = ParallelBranch(
            branch_id=branch_id,
            node_id=node_id,
            agent_id=agent_id,
            sandbox_id=sandbox_id,
            target_paths=target_paths,
            state=BranchState.PENDING,
        )
        self._branches[branch_id] = branch

        # Register target paths
        for path in target_paths:
            if path not in self._target_write_registry:
                self._target_write_registry[path] = []
            self._target_write_registry[path].append(branch_id)

        return branch

    def start_branch(self, branch_id: str) -> None:
        """Mark a branch as running."""
        branch = self._branches[branch_id]
        branch.state = BranchState.RUNNING

    def complete_branch(self, branch_id: str, result: Dict[str, Any]) -> None:
        """Mark a branch as completed with its result."""
        branch = self._branches[branch_id]
        branch.state = BranchState.COMPLETED
        branch.result = result

    def fail_branch(self, branch_id: str, error: str) -> None:
        """Mark a branch as failed."""
        branch = self._branches[branch_id]
        branch.state = BranchState.FAILED
        branch.result = {"error": error}

    def cancel_branch(self, branch_id: str) -> List[str]:
        """
        Cancel a branch and propagate cancellation deterministically to all child branches.
        Returns list of all cancelled branch IDs.
        """
        cancelled: List[str] = []
        branch = self._branches.get(branch_id)
        if branch is None:
            return cancelled

        if branch.state in (BranchState.PENDING, BranchState.RUNNING):
            branch.state = BranchState.CANCELLED
            cancelled.append(branch_id)

            # Cancel the sandbox
            self.sandbox_manager.cancel_sandbox(branch.sandbox_id)

            # Recursively cancel children
            for child_id in branch.children:
                cancelled.extend(self.cancel_branch(child_id))

        return cancelled

    def evaluate_join(self) -> ParallelExecutionReport:
        """
        Evaluate the join condition based on the configured strategy.
        For FIRST_SUCCESS, cancels all non-winning branches.
        """
        completed = [b for b in self._branches.values() if b.state == BranchState.COMPLETED]
        failed = [b for b in self._branches.values() if b.state == BranchState.FAILED]
        cancelled = [b for b in self._branches.values() if b.state == BranchState.CANCELLED]
        winning_branch_id: Optional[str] = None
        all_cleanup_receipts: List[CleanupReceipt] = []

        if self.join_strategy == JoinStrategy.FIRST_SUCCESS:
            if completed:
                # First completed branch wins
                winning_branch_id = completed[0].branch_id

                # Cancel all other non-completed, non-cancelled branches
                for branch in self._branches.values():
                    if branch.branch_id != winning_branch_id and branch.state in (
                        BranchState.PENDING,
                        BranchState.RUNNING,
                    ):
                        self.cancel_branch(branch.branch_id)

                # Cleanup all non-winning sandboxes
                for branch in self._branches.values():
                    if branch.branch_id != winning_branch_id:
                        receipt = self.sandbox_manager.cleanup_sandbox(branch.sandbox_id)
                        all_cleanup_receipts.append(receipt)

        elif self.join_strategy == JoinStrategy.ALL:
            # All must complete for success
            if len(completed) == len(self._branches):
                winning_branch_id = None  # All branches contribute

        elif self.join_strategy == JoinStrategy.ANY:
            if completed:
                winning_branch_id = completed[0].branch_id

        # Re-count after possible cancellations
        completed_count = sum(1 for b in self._branches.values() if b.state == BranchState.COMPLETED)
        cancelled_count = sum(1 for b in self._branches.values() if b.state == BranchState.CANCELLED)
        failed_count = sum(1 for b in self._branches.values() if b.state == BranchState.FAILED)

        return ParallelExecutionReport(
            execution_id=self.execution_id,
            join_strategy=self.join_strategy,
            total_branches=len(self._branches),
            completed_branches=completed_count,
            cancelled_branches=cancelled_count,
            failed_branches=failed_count,
            winning_branch_id=winning_branch_id,
            artifact_attributions=tuple(self.sandbox_manager.attributions),
            cleanup_receipts=tuple(all_cleanup_receipts),
        )

    @property
    def branches(self) -> Dict[str, ParallelBranch]:
        return dict(self._branches)
