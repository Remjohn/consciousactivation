"""
Workflow Control-Flow Compiler & Deterministic Scheduling Engine.

Governed by:
- Mandate CAE-M59 (Phase 07 - Workflow Engineering)
- Object Constitution CA-CAN-04 (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow;
- Routing, conditions, switch dispatch, loop bounds, retries, joins, timeouts, and human gates are 100% host-evaluated;
- Same workflow + same state snapshot => same routing decision (bit-for-bit identical SHA-256 digest);
- Host bounds strictly govern loops and retries;
- Human gates require explicit COMMANDER lane operator authorization.
"""

from __future__ import annotations

import collections
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .pi_adapter import AuthorityLane
from .workflow_ir import (
    ExecutableWorkflowIR,
    IREdgeType,
    WorkflowIREdge,
    WorkflowIRNode,
    WorkflowIRValidator,
)
from .workflow_primitives import (
    AgentMutatedLoopBoundError,
    ConditionBranchDefinition,
    HumanGateBypassError,
    HumanGateRequirement,
    JoinCondition,
    JoinPolicy,
    LoopBoundPolicy,
    LoopTerminationKind,
    ParallelSideEffectConflictError,
    RetryPolicyDefinition,
    SwitchCaseDefinition,
    UnboundedLoopError,
    UnevaluableConditionError,
    WorkflowPrimitiveDefinition,
    WorkflowPrimitiveError,
    WorkflowPrimitiveKind,
    WorkUnitKind,
)


# ============================================================================
# 1. Error Taxonomy
# ============================================================================


class WorkflowControlFlowError(WorkflowPrimitiveError):
    """Base error for workflow control-flow compiler and scheduling failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "WORKFLOW_CONTROL_FLOW_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class ControlFlowSchedulingError(WorkflowControlFlowError):
    """Raised when deterministic scheduling encounters an unresolvable state."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, reason_code="ERR_CONTROL_FLOW_SCHEDULING", details=details)


class LoopBoundExceededError(WorkflowControlFlowError):
    """Raised when a loop execution attempts to exceed its host-enforced max_iterations."""

    def __init__(self, node_id: str, current_iteration: int, max_iterations: int) -> None:
        super().__init__(
            f"Loop on node '{node_id}' exceeded host-enforced bound: iteration {current_iteration} > max {max_iterations}",
            reason_code="ERR_LOOP_BOUND_EXCEEDED",
            details={"node_id": node_id, "current_iteration": current_iteration, "max_iterations": max_iterations},
        )


class JoinSynchronizationError(WorkflowControlFlowError):
    """Raised when a JOIN node has missing, contradictory, or unreachable branches."""

    def __init__(self, join_node_id: str, missing_branches: Sequence[str]) -> None:
        super().__init__(
            f"JOIN node '{join_node_id}' cannot synchronize: missing or undeclared predecessor branches {list(missing_branches)}",
            reason_code="ERR_JOIN_SYNCHRONIZATION",
            details={"join_node_id": join_node_id, "missing_branches": list(missing_branches)},
        )


class TimeoutExceededError(WorkflowControlFlowError):
    """Raised when a step execution exceeds its host-enforced timeout."""

    def __init__(self, node_id: str, elapsed_seconds: float, timeout_seconds: float) -> None:
        super().__init__(
            f"Step '{node_id}' timed out: elapsed {elapsed_seconds}s exceeded timeout {timeout_seconds}s",
            reason_code="ERR_TIMEOUT_EXCEEDED",
            details={"node_id": node_id, "elapsed_seconds": elapsed_seconds, "timeout_seconds": timeout_seconds},
        )


class HumanGateSuspendedError(WorkflowControlFlowError):
    """Raised when attempting to execute past an unresolved HUMAN_GATE."""

    def __init__(self, gate_id: str) -> None:
        super().__init__(
            f"Execution suspended at HUMAN_GATE '{gate_id}'; awaiting COMMANDER operator grant",
            reason_code="ERR_HUMAN_GATE_SUSPENDED",
            details={"gate_id": gate_id},
        )


class HumanGateLaneViolationError(WorkflowControlFlowError):
    """Raised when an operator grant is signed by an unauthorized authority lane."""

    def __init__(self, gate_id: str, attempted_lane: str) -> None:
        super().__init__(
            f"Operator grant for HUMAN_GATE '{gate_id}' came from unauthorized lane '{attempted_lane}'; COMMANDER required",
            reason_code="ERR_HUMAN_GATE_LANE_VIOLATION",
            details={"gate_id": gate_id, "attempted_lane": attempted_lane},
        )


class ConditionEvaluationError(WorkflowControlFlowError):
    """Raised when a condition expression fails host evaluation."""

    def __init__(self, node_id: str, expression: str, reason: str) -> None:
        super().__init__(
            f"Condition evaluation failed on node '{node_id}' for expression '{expression}': {reason}",
            reason_code="ERR_CONDITION_EVALUATION",
            details={"node_id": node_id, "expression": expression, "reason": reason},
        )


# ============================================================================
# 2. Domain Models & State Snapshots
# ============================================================================


@dataclass(frozen=True, slots=True)
class OperatorGrantRecord:
    """Cryptographically signed approval record for a HUMAN_GATE primitive."""

    grant_id: str
    gate_id: str
    approver_id: str
    approver_role: str
    authority_lane: AuthorityLane
    decision: str  # "APPROVED", "REJECTED", "REVISE"
    rationale: str
    granted_at_utc: str
    signature_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.signature_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "signature_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "grant_id": self.grant_id,
            "gate_id": self.gate_id,
            "approver_id": self.approver_id,
            "approver_role": self.approver_role,
            "authority_lane": self.authority_lane.value,
            "decision": self.decision,
            "rationale": self.rationale,
            "granted_at_utc": self.granted_at_utc,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["signature_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class ControlFlowExecutionSnapshot:
    """
    Immutable snapshot of a running workflow at a specific scheduling tick.
    """

    run_id: str
    workflow_id: str
    node_states: Mapping[str, str]  # node_id -> "BLOCKED", "READY", "RUNNING", "SUCCEEDED", "FAILED", "SKIPPED", "TIMED_OUT", "WAITING_OPERATOR"
    node_outputs: Mapping[str, Any] = field(default_factory=dict)
    loop_counters: Mapping[str, int] = field(default_factory=dict)  # node_id -> iteration count
    retry_attempts: Mapping[str, int] = field(default_factory=dict)  # node_id -> attempt count
    operator_grants: Mapping[str, OperatorGrantRecord] = field(default_factory=dict)  # gate_id -> OperatorGrantRecord
    node_elapsed_seconds: Mapping[str, float] = field(default_factory=dict)  # node_id -> elapsed seconds

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "workflow_id": self.workflow_id,
            "node_states": {k: self.node_states[k] for k in sorted(self.node_states)},
            "node_outputs": {k: self.node_outputs[k] for k in sorted(self.node_outputs)},
            "loop_counters": {k: self.loop_counters[k] for k in sorted(self.loop_counters)},
            "retry_attempts": {k: self.retry_attempts[k] for k in sorted(self.retry_attempts)},
            "operator_grants": {k: self.operator_grants[k].canonical_dict() for k in sorted(self.operator_grants)},
            "node_elapsed_seconds": {k: self.node_elapsed_seconds[k] for k in sorted(self.node_elapsed_seconds)},
        }

    def compute_sha256(self) -> str:
        raw = canonical_json_text(self.canonical_dict())
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    """
    Deterministic routing output for a single scheduling evaluation step.
    """

    workflow_id: str
    ready_nodes: Tuple[str, ...]
    skipped_nodes: Tuple[str, ...]
    waiting_human_gates: Tuple[str, ...]
    timed_out_nodes: Tuple[str, ...]
    loop_actions: Mapping[str, str]  # node_id -> "CONTINUE_LOOP" | "TERMINATE_LOOP"
    join_statuses: Mapping[str, str]  # node_id -> "WAITING_PREDECESSORS" | "SATISFIED"
    active_parallel_batches: Tuple[Tuple[str, ...], ...] = ()
    routing_digest_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.routing_digest_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "routing_digest_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "ready_nodes": sorted(list(self.ready_nodes)),
            "skipped_nodes": sorted(list(self.skipped_nodes)),
            "waiting_human_gates": sorted(list(self.waiting_human_gates)),
            "timed_out_nodes": sorted(list(self.timed_out_nodes)),
            "loop_actions": {k: self.loop_actions[k] for k in sorted(self.loop_actions)},
            "join_statuses": {k: self.join_statuses[k] for k in sorted(self.join_statuses)},
            "active_parallel_batches": [list(b) for b in self.active_parallel_batches],
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["routing_digest_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ============================================================================
# 3. Deterministic Control-Flow Scheduler
# ============================================================================


class DeterministicControlFlowScheduler:
    """
    Extends and unifies deterministic workflow scheduling with executable semantics
    for all 14 ratified control flow primitives.
    """

    @classmethod
    def compute_routing(
        cls,
        ir: ExecutableWorkflowIR,
        snapshot: ControlFlowExecutionSnapshot,
    ) -> RoutingDecision:
        """
        Compute deterministic routing decisions given a workflow IR and state snapshot.
        Guarantees: Same (ir, snapshot) => Bit-for-bit identical RoutingDecision.
        """
        node_map = {n.node_id: n for n in ir.nodes}
        incoming_edges: Dict[str, List[WorkflowIREdge]] = collections.defaultdict(list)
        outgoing_edges: Dict[str, List[WorkflowIREdge]] = collections.defaultdict(list)

        for edge in ir.edges:
            incoming_edges[edge.target_node_id].append(edge)
            outgoing_edges[edge.source_node_id].append(edge)

        ready_nodes: List[str] = []
        skipped_nodes: Set[str] = set()
        waiting_human_gates: List[str] = []
        timed_out_nodes: List[str] = []
        loop_actions: Dict[str, str] = {}
        join_statuses: Dict[str, str] = {}

        # First, propagate SKIPPED states from branch decisions
        for node in ir.nodes:
            state = snapshot.node_states.get(node.node_id, "BLOCKED")
            if state == "SKIPPED":
                skipped_nodes.add(node.node_id)
                continue

            # Check if this node is a CONDITION node that evaluated to skip a branch
            if node.primitive_kind == WorkflowPrimitiveKind.CONDITION and state == "SUCCEEDED":
                taken_branch, untaken_branch = cls._evaluate_condition_branches(node, snapshot)
                if untaken_branch:
                    cls._propagate_skip(untaken_branch, outgoing_edges, snapshot, skipped_nodes)

            # Check if this node is a SWITCH node that evaluated to skip cases
            elif node.primitive_kind == WorkflowPrimitiveKind.SWITCH and state == "SUCCEEDED":
                taken_step, untaken_steps = cls._evaluate_switch_branches(node, snapshot)
                for u_step in untaken_steps:
                    cls._propagate_skip(u_step, outgoing_edges, snapshot, skipped_nodes)

        # Now evaluate ready candidates across all topological steps
        for node_id in ir.topological_order:
            node = node_map[node_id]
            current_state = snapshot.node_states.get(node_id, "BLOCKED")

            if node_id in skipped_nodes or current_state == "SKIPPED":
                continue

            # Check for Timeout on RUNNING nodes
            if current_state == "RUNNING":
                elapsed = snapshot.node_elapsed_seconds.get(node_id, 0.0)
                timeout_limit = None
                if node.primitive_definition and node.primitive_definition.timeout_seconds:
                    timeout_limit = node.primitive_definition.timeout_seconds

                if timeout_limit is not None and elapsed > timeout_limit:
                    timed_out_nodes.append(node_id)
                    continue

            # Only nodes in BLOCKED or READY state are scheduling candidates
            if current_state not in {"BLOCKED", "READY"}:
                continue

            in_edges = incoming_edges.get(node_id, [])
            if not in_edges:
                # Root node with no predecessors
                cls._process_ready_candidate(node, snapshot, ready_nodes, waiting_human_gates, loop_actions)
                continue

            # Evaluate incoming edges based on primitive kind
            if node.primitive_kind == WorkflowPrimitiveKind.JOIN:
                join_ready, missing = cls._evaluate_join_synchronization(node, in_edges, snapshot, skipped_nodes)
                if join_ready:
                    join_statuses[node_id] = "SATISFIED"
                    cls._process_ready_candidate(node, snapshot, ready_nodes, waiting_human_gates, loop_actions)
                else:
                    join_statuses[node_id] = "WAITING_PREDECESSORS"

            elif node.primitive_kind == WorkflowPrimitiveKind.LOOP:
                loop_ready, action = cls._evaluate_loop_readiness(node, in_edges, snapshot)
                loop_actions[node_id] = action
                if loop_ready:
                    cls._process_ready_candidate(node, snapshot, ready_nodes, waiting_human_gates, loop_actions)

            else:
                # Standard SEQUENCE / general dependency
                # All active non-skipped predecessors must be SUCCEEDED
                active_predecessors = [e.source_node_id for e in in_edges if e.edge_type != IREdgeType.LOOP_BACK]
                all_parents_succeeded = True
                for p_id in active_predecessors:
                    p_state = snapshot.node_states.get(p_id, "BLOCKED")
                    if p_id in skipped_nodes or p_state == "SKIPPED":
                        continue
                    if p_state != "SUCCEEDED":
                        all_parents_succeeded = False
                        break

                if all_parents_succeeded and active_predecessors:
                    cls._process_ready_candidate(node, snapshot, ready_nodes, waiting_human_gates, loop_actions)

        # Compute safe parallel batches
        parallel_batches = cls._compute_safe_parallel_batches(ready_nodes, node_map)

        return RoutingDecision(
            workflow_id=ir.workflow_ir_id,
            ready_nodes=tuple(ready_nodes),
            skipped_nodes=tuple(sorted(skipped_nodes)),
            waiting_human_gates=tuple(waiting_human_gates),
            timed_out_nodes=tuple(timed_out_nodes),
            loop_actions=loop_actions,
            join_statuses=join_statuses,
            active_parallel_batches=parallel_batches,
        )

    @classmethod
    def _process_ready_candidate(
        cls,
        node: WorkflowIRNode,
        snapshot: ControlFlowExecutionSnapshot,
        ready_nodes: List[str],
        waiting_human_gates: List[str],
        loop_actions: Dict[str, str],
    ) -> None:
        """Process candidate node for readiness or human gate suspension."""
        if node.primitive_kind == WorkflowPrimitiveKind.HUMAN_GATE:
            gate_id = node.node_id
            grant = snapshot.operator_grants.get(gate_id)

            if not grant:
                waiting_human_gates.append(gate_id)
                return

            if grant.authority_lane != AuthorityLane.COMMANDER:
                raise HumanGateLaneViolationError(gate_id, grant.authority_lane.value)

            if grant.decision == "APPROVED":
                ready_nodes.append(node.node_id)
            else:
                waiting_human_gates.append(gate_id)
        else:
            ready_nodes.append(node.node_id)

    @classmethod
    def _evaluate_condition_branches(
        cls,
        node: WorkflowIRNode,
        snapshot: ControlFlowExecutionSnapshot,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Evaluate CONDITION node predicate against snapshot outputs.
        Returns (taken_step_id, untaken_step_id).
        """
        if not node.primitive_definition or not node.primitive_definition.condition_config:
            return None, None

        cfg = node.primitive_definition.condition_config
        expr = cfg.condition_expression
        context = snapshot.node_outputs.get(node.node_id, {})

        # Evaluate host condition safely
        result = cls.evaluate_host_condition(expr, context)
        if result:
            return cfg.then_step_id, cfg.else_step_id
        else:
            return cfg.else_step_id, cfg.then_step_id

    @classmethod
    def evaluate_host_condition(cls, expression: str, context: Mapping[str, Any]) -> bool:
        """
        Safely evaluate deterministic condition expression against dictionary context.
        Prohibits arbitrary code execution; supports comparisons and key lookups.
        """
        if not expression or not expression.strip():
            raise UnevaluableConditionError("EMPTY_EXPRESSION", "Expression cannot be empty")

        expr = expression.strip()
        # Handle simple operators: >, >=, <, <=, ==, !=
        for op in [">=", "<=", "!=", "==", ">", "<"]:
            if op in expr:
                left_var, right_val = expr.split(op, 1)
                left_var = left_var.strip()
                right_val = right_val.strip()

                if left_var not in context:
                    # Missing context variable evaluates to False or raises
                    return False

                val = context[left_var]
                # Try int/float parsing
                try:
                    r_num = float(right_val)
                    l_num = float(val)
                    if op == ">=":
                        return l_num >= r_num
                    if op == "<=":
                        return l_num <= r_num
                    if op == ">":
                        return l_num > r_num
                    if op == "<":
                        return l_num < r_num
                    if op == "==":
                        return l_num == r_num
                    if op == "!=":
                        return l_num != r_num
                except (ValueError, TypeError):
                    # String comparison
                    clean_r = right_val.strip("'\"")
                    if op == "==":
                        return str(val) == clean_r
                    if op == "!=":
                        return str(val) != clean_r

        # Boolean key lookup
        if expr in context:
            return bool(context[expr])

        return False

    @classmethod
    def _evaluate_switch_branches(
        cls,
        node: WorkflowIRNode,
        snapshot: ControlFlowExecutionSnapshot,
    ) -> Tuple[Optional[str], List[str]]:
        """
        Evaluate SWITCH selector against snapshot outputs.
        Returns (taken_step_id, list_of_untaken_step_ids).
        """
        if not node.primitive_definition or not node.primitive_definition.switch_cases:
            return None, []

        p_def = node.primitive_definition
        context = snapshot.node_outputs.get(node.node_id, {})
        selector_val = str(context.get("selector", context.get("value", "")))

        taken_step: Optional[str] = None
        untaken_steps: List[str] = []

        matched = False
        for sc in p_def.switch_cases:
            if sc.match_value == selector_val and not matched:
                taken_step = sc.target_step_id
                matched = True
            else:
                untaken_steps.append(sc.target_step_id)

        if not matched and p_def.default_switch_step:
            taken_step = p_def.default_switch_step
        elif p_def.default_switch_step and matched:
            untaken_steps.append(p_def.default_switch_step)

        return taken_step, untaken_steps

    @classmethod
    def _propagate_skip(
        cls,
        start_node_id: str,
        outgoing_edges: Mapping[str, Sequence[WorkflowIREdge]],
        snapshot: ControlFlowExecutionSnapshot,
        skipped_nodes: Set[str],
    ) -> None:
        """Recursively mark unselected branch nodes as SKIPPED unless reached by an active path."""
        queue = [start_node_id]
        while queue:
            curr = queue.pop(0)
            if curr in skipped_nodes:
                continue
            # Only skip if not already succeeded or running
            st = snapshot.node_states.get(curr, "BLOCKED")
            if st not in {"SUCCEEDED", "RUNNING"}:
                skipped_nodes.add(curr)
                for edge in outgoing_edges.get(curr, []):
                    queue.append(edge.target_node_id)

    @classmethod
    def _evaluate_join_synchronization(
        cls,
        node: WorkflowIRNode,
        incoming_edges: Sequence[WorkflowIREdge],
        snapshot: ControlFlowExecutionSnapshot,
        skipped_nodes: Set[str],
    ) -> Tuple[bool, List[str]]:
        """
        Evaluate JOIN synchronization policy across declared incoming edges.
        Returns (is_ready, missing_branches).
        """
        join_policy = JoinPolicy.ALL
        quorum_count = len(incoming_edges)
        if node.primitive_definition and node.primitive_definition.join_condition:
            join_policy = node.primitive_definition.join_condition.policy
            if node.primitive_definition.join_condition.quorum_count:
                quorum_count = node.primitive_definition.join_condition.quorum_count

        succeeded_count = 0
        missing: List[str] = []

        active_edges = [e for e in incoming_edges if e.source_node_id not in skipped_nodes]
        if not active_edges:
            return False, ["NO_ACTIVE_INCOMING_EDGES"]

        for edge in active_edges:
            src_state = snapshot.node_states.get(edge.source_node_id, "BLOCKED")
            if src_state == "SUCCEEDED":
                succeeded_count += 1
            else:
                missing.append(edge.source_node_id)

        if join_policy == JoinPolicy.ALL:
            return succeeded_count == len(active_edges), missing
        elif join_policy == JoinPolicy.ANY:
            return succeeded_count >= 1, missing
        elif join_policy == JoinPolicy.QUORUM:
            return succeeded_count >= quorum_count, missing

        return False, missing

    @classmethod
    def _evaluate_loop_readiness(
        cls,
        node: WorkflowIRNode,
        incoming_edges: Sequence[WorkflowIREdge],
        snapshot: ControlFlowExecutionSnapshot,
    ) -> Tuple[bool, str]:
        """
        Evaluate LOOP readiness and bound enforcement.
        Returns (is_ready, action).
        """
        max_iter = 1
        if node.primitive_definition and node.primitive_definition.loop_policy:
            max_iter = node.primitive_definition.loop_policy.max_iterations

        current_iter = snapshot.loop_counters.get(node.node_id, 0)

        # Check if incoming forward edges are satisfied
        forward_edges = [e for e in incoming_edges if e.edge_type != IREdgeType.LOOP_BACK]
        forward_ok = True
        for e in forward_edges:
            if snapshot.node_states.get(e.source_node_id) != "SUCCEEDED":
                forward_ok = False
                break

        if not forward_ok and current_iter == 0:
            return False, "WAITING_FORWARD_PREDECESSORS"

        if current_iter >= max_iter:
            return False, "TERMINATE_LOOP"

        return True, "CONTINUE_LOOP"

    @classmethod
    def _compute_safe_parallel_batches(
        cls,
        ready_node_ids: Sequence[str],
        node_map: Mapping[str, WorkflowIRNode],
    ) -> Tuple[Tuple[str, ...], ...]:
        """
        Partition ready nodes into safe execution batches guaranteeing side-effect isolation.
        Two mutating nodes with non-READ_ONLY side effects are placed in separate batches.
        """
        batches: List[List[str]] = []
        occupied_effects: List[Set[str]] = []

        for nid in ready_node_ids:
            node = node_map[nid]
            effect = node.side_effect_class

            placed = False
            for idx, batch_effects in enumerate(occupied_effects):
                if effect in {"NONE", "READ_ONLY"} or effect not in batch_effects:
                    batches[idx].append(nid)
                    if effect not in {"NONE", "READ_ONLY"}:
                        batch_effects.add(effect)
                    placed = True
                    break

            if not placed:
                batches.append([nid])
                new_effects: Set[str] = set()
                if effect not in {"NONE", "READ_ONLY"}:
                    new_effects.add(effect)
                occupied_effects.append(new_effects)

        return tuple(tuple(b) for b in batches)


# ============================================================================
# 4. Workflow Control-Flow Compiler
# ============================================================================


@dataclass(frozen=True, slots=True)
class CompiledWorkflowExecutionGraph:
    """Compiled, verified graph ready for runtime execution and deterministic scheduling."""

    ir: ExecutableWorkflowIR
    compiled_at_utc: str
    control_flow_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.control_flow_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "control_flow_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "ir": self.ir.canonical_dict(),
            "compiled_at_utc": self.compiled_at_utc,
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["control_flow_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class WorkflowControlFlowCompiler:
    """Compiles ExecutableWorkflowIR into a verified executable control-flow graph."""

    @classmethod
    def compile_execution_graph(
        cls,
        ir: ExecutableWorkflowIR,
        *,
        compiled_at_utc: str = "2026-09-02T05:20:00Z",
    ) -> CompiledWorkflowExecutionGraph:
        """Validate and compile ExecutableWorkflowIR into CompiledWorkflowExecutionGraph."""
        WorkflowIRValidator.validate_ir(ir)
        return CompiledWorkflowExecutionGraph(
            ir=ir,
            compiled_at_utc=compiled_at_utc,
        )
