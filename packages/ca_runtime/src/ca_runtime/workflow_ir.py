"""
Executable Workflow Intermediate Representation (Workflow IR) & Canonical Compilation Engine.

Governed by:
- Mandate CAE-M58 (Phase 07 - Workflow Engineering)
- Workflow Primitive Constitution (docs/cae/constitutions/CA-CAN-04_WORKFLOW_PRIMITIVES.yaml)
- StateM Alignment Contract (docs/cae/CAE_Next_16_Mandate_Bundle/00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md)

Core Doctrine:
- Code owns deterministic control flow;
- Workflow IR makes workflow structure inspectable, diffable, compilable, and benchmarkable;
- Equivalent source graphs produce canonicalized, deterministic identity;
- Illegal cycles are rejected unless an explicit host-bounded LOOP/RETRY/REPAIR primitive declares termination;
- Runtime compiler remains the execution authority.
"""

from __future__ import annotations

import collections
import copy
import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ca_contracts import canonical_json_text

from .pi_adapter import AuthorityLane
from .workflow_primitives import (
    AgentMutatedLoopBoundError,
    ConditionBranchDefinition,
    HumanGateRequirement,
    JoinCondition,
    LoopBoundPolicy,
    ParallelBranchDefinition,
    ParallelSideEffectConflictError,
    RetryPolicyDefinition,
    SwitchCaseDefinition,
    UnboundedLoopError,
    UnevaluableConditionError,
    WorkflowPrimitiveDefinition,
    WorkflowPrimitiveError,
    WorkflowPrimitiveKind,
    WorkflowPrimitiveValidator,
    WorkflowStepContract,
    WorkflowTransitionSemantics,
    WorkUnitKind,
)


# ============================================================================
# 1. Error Taxonomy
# ============================================================================


class WorkflowIRError(WorkflowPrimitiveError):
    """Base error for all Workflow IR validation and compilation failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "WORKFLOW_IR_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class WorkflowIRValidationError(WorkflowIRError):
    """Raised when an IR structure fails semantic or structural validation."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, reason_code="ERR_WORKFLOW_IR_VALIDATION", details=details)


class WorkflowIRCyclicGraphError(WorkflowIRError):
    """Raised when an unhandled or unbounded cycle is detected in the workflow graph."""

    def __init__(self, cycle_path: Sequence[str]) -> None:
        path_str = " -> ".join(cycle_path)
        super().__init__(
            f"Illegal unbounded cycle detected in workflow graph: {path_str}. Cycles require an explicit LOOP/REPAIR primitive with host bounds.",
            reason_code="ERR_WORKFLOW_IR_ILLEGAL_CYCLE",
            details={"cycle_path": list(cycle_path)},
        )


class WorkflowIRNodeNotFoundError(WorkflowIRError):
    """Raised when an edge or branch references a non-existent node."""

    def __init__(self, node_id: str, referenced_by: str) -> None:
        super().__init__(
            f"Node '{node_id}' referenced by '{referenced_by}' not found in workflow graph",
            reason_code="ERR_WORKFLOW_IR_NODE_NOT_FOUND",
            details={"node_id": node_id, "referenced_by": referenced_by},
        )


class WorkflowIRBranchTargetMissingError(WorkflowIRError):
    """Raised when a condition or switch branch target is missing or unresolvable."""

    def __init__(self, source_node_id: str, branch_target: str, branch_type: str) -> None:
        super().__init__(
            f"Branch target '{branch_target}' ({branch_type}) on node '{source_node_id}' is missing from graph",
            reason_code="ERR_WORKFLOW_IR_BRANCH_TARGET_MISSING",
            details={"source_node_id": source_node_id, "branch_target": branch_target, "branch_type": branch_type},
        )


class WorkflowIRDuplicateNodeError(WorkflowIRError):
    """Raised when duplicate node IDs are declared in the workflow."""

    def __init__(self, duplicate_node_ids: Sequence[str]) -> None:
        super().__init__(
            f"Duplicate node IDs declared in workflow IR: {list(duplicate_node_ids)}",
            reason_code="ERR_WORKFLOW_IR_DUPLICATE_NODES",
            details={"duplicate_node_ids": list(duplicate_node_ids)},
        )


class WorkflowIRCompilationError(WorkflowIRError):
    """Raised when compiling IR to runtime projection fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, reason_code="ERR_WORKFLOW_IR_COMPILATION", details=details)


# ============================================================================
# 2. Enums
# ============================================================================


class IREdgeType(str, Enum):
    """Semantic classification of edges in Workflow IR."""

    NORMAL = "NORMAL"
    THEN_BRANCH = "THEN_BRANCH"
    ELSE_BRANCH = "ELSE_BRANCH"
    SWITCH_CASE = "SWITCH_CASE"
    LOOP_BACK = "LOOP_BACK"
    RETRY_EDGE = "RETRY_EDGE"
    REPAIR_EDGE = "REPAIR_EDGE"
    TIMEOUT_EDGE = "TIMEOUT_EDGE"
    FAIL_EDGE = "FAIL_EDGE"


# ============================================================================
# 3. Domain Dataclasses
# ============================================================================


@dataclass(frozen=True, slots=True)
class WorkflowIRNode:
    """Canonical representation of an individual node in the Workflow IR."""

    node_id: str
    capability_id: str
    phase_order: int
    purpose: str
    actor_kind: str  # DETERMINISTIC_MODULE, AGENT_PROGRAM, PROGRAMMED_MODEL, HUMAN_GATE, EXTERNAL_PRODUCT, CONTROL
    role: str  # HUNTER, ANALYST, COMPOSER, COMMANDER, NOT_APPLICABLE_BY_RULE
    product_boundary: str  # AIR, AHP, INTERVIEW, STUDIO, VAE, DELEGATION, BUILDER
    side_effect_class: str  # NONE, READ_ONLY, MUTATION_OPERATION
    primitive_kind: WorkflowPrimitiveKind = WorkflowPrimitiveKind.SEQUENCE
    work_unit_kind: WorkUnitKind = WorkUnitKind.NOT_APPLICABLE
    input_contracts: Tuple[str, ...] = ()
    output_contracts: Tuple[str, ...] = ()
    implementation: Optional[Dict[str, Any]] = None
    primitive_definition: Optional[WorkflowPrimitiveDefinition] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "capability_id": self.capability_id,
            "phase_order": self.phase_order,
            "purpose": self.purpose,
            "actor_kind": self.actor_kind,
            "role": self.role,
            "product_boundary": self.product_boundary,
            "side_effect_class": self.side_effect_class,
            "primitive_kind": self.primitive_kind.value,
            "work_unit_kind": self.work_unit_kind.value,
            "input_contracts": sorted(list(self.input_contracts)),
            "output_contracts": sorted(list(self.output_contracts)),
            "implementation": self.implementation,
            "primitive_definition": self.primitive_definition.canonical_dict() if self.primitive_definition else None,
        }


@dataclass(frozen=True, slots=True)
class WorkflowIREdge:
    """Canonical representation of a directed control/data edge in Workflow IR."""

    source_node_id: str
    target_node_id: str
    contract_id: str
    edge_type: IREdgeType = IREdgeType.NORMAL
    guard_expression: Optional[str] = None
    case_value: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "contract_id": self.contract_id,
            "edge_type": self.edge_type.value,
            "guard_expression": self.guard_expression,
            "case_value": self.case_value,
        }


@dataclass(frozen=True, slots=True)
class ExecutableWorkflowIR:
    """
    The canonical, inspectable, diffable, compilable, and benchmarkable Workflow IR.
    """

    workflow_ir_id: str
    name: str
    version: str
    category_id: str
    profile_id: str
    purpose: str
    authority_lane: AuthorityLane
    nodes: Tuple[WorkflowIRNode, ...]
    edges: Tuple[WorkflowIREdge, ...]
    topological_order: Tuple[str, ...] = ()
    wrong_reading_locks: Tuple[str, ...] = ()
    evaluation_requirements: Tuple[str, ...] = ()
    repair_laws: Tuple[str, ...] = ()
    semantic_dependency_refs: Tuple[str, ...] = ()
    ir_digest_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.ir_digest_sha256:
            digest = self._compute_sha256()
            object.__setattr__(self, "ir_digest_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        # Canonicalize nodes and edges order for deterministic hashing
        canonical_nodes = sorted(
            [n.canonical_dict() for n in self.nodes],
            key=lambda item: (item["phase_order"], item["node_id"]),
        )
        canonical_edges = sorted(
            [e.canonical_dict() for e in self.edges],
            key=lambda item: (item["source_node_id"], item["target_node_id"], item["contract_id"]),
        )
        return {
            "workflow_ir_id": self.workflow_ir_id,
            "name": self.name,
            "version": self.version,
            "category_id": self.category_id,
            "profile_id": self.profile_id,
            "purpose": self.purpose,
            "authority_lane": self.authority_lane.value,
            "nodes": canonical_nodes,
            "edges": canonical_edges,
            "topological_order": list(self.topological_order),
            "wrong_reading_locks": sorted(list(self.wrong_reading_locks)),
            "evaluation_requirements": sorted(list(self.evaluation_requirements)),
            "repair_laws": sorted(list(self.repair_laws)),
            "semantic_dependency_refs": sorted(list(self.semantic_dependency_refs)),
        }

    def _compute_sha256(self) -> str:
        data = self.canonical_dict()
        data["ir_digest_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def verify_integrity(self) -> bool:
        return self._compute_sha256() == self.ir_digest_sha256


@dataclass(frozen=True, slots=True)
class WorkflowIRDiffResult:
    """Structured delta between two ExecutableWorkflowIR definitions."""

    identical: bool
    left_id: str
    right_id: str
    added_nodes: Tuple[str, ...] = ()
    removed_nodes: Tuple[str, ...] = ()
    modified_nodes: Tuple[str, ...] = ()
    added_edges: Tuple[Tuple[str, str, str], ...] = ()
    removed_edges: Tuple[Tuple[str, str, str], ...] = ()
    policy_changes: Tuple[str, ...] = ()
    diff_digest_sha256: str = field(default="")

    def __post_init__(self) -> None:
        if not self.diff_digest_sha256:
            digest = self._compute_digest()
            object.__setattr__(self, "diff_digest_sha256", digest)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "identical": self.identical,
            "left_id": self.left_id,
            "right_id": self.right_id,
            "added_nodes": sorted(list(self.added_nodes)),
            "removed_nodes": sorted(list(self.removed_nodes)),
            "modified_nodes": sorted(list(self.modified_nodes)),
            "added_edges": [list(e) for e in sorted(self.added_edges)],
            "removed_edges": [list(e) for e in sorted(self.removed_edges)],
            "policy_changes": sorted(list(self.policy_changes)),
        }

    def _compute_digest(self) -> str:
        data = self.canonical_dict()
        data["diff_digest_sha256"] = ""
        raw = canonical_json_text(data)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


# ============================================================================
# 4. Workflow IR Validator & Cycle Engine
# ============================================================================


class WorkflowIRValidator:
    """Validates structural and semantic invariants of ExecutableWorkflowIR."""

    @classmethod
    def validate_ir(cls, ir: ExecutableWorkflowIR) -> None:
        """Complete validation of an ExecutableWorkflowIR instance."""
        # 1. Verify node unique IDs
        node_ids = [n.node_id for n in ir.nodes]
        if len(node_ids) != len(set(node_ids)):
            duplicates = [item for item, count in collections.Counter(node_ids).items() if count > 1]
            raise WorkflowIRDuplicateNodeError(duplicates)

        node_map = {n.node_id: n for n in ir.nodes}

        # 2. Verify all edge endpoints exist
        for edge in ir.edges:
            if edge.source_node_id not in node_map:
                raise WorkflowIRNodeNotFoundError(edge.source_node_id, f"edge from '{edge.source_node_id}' to '{edge.target_node_id}'")
            if edge.target_node_id not in node_map:
                raise WorkflowIRNodeNotFoundError(edge.target_node_id, f"edge from '{edge.source_node_id}' to '{edge.target_node_id}'")

        # 3. Verify branch conditions and targets
        for node in ir.nodes:
            if node.primitive_definition:
                WorkflowPrimitiveValidator.validate_primitive(node.primitive_definition)

                # If node is CONDITION, verify branch targets exist
                if node.primitive_definition.condition_config:
                    cond = node.primitive_definition.condition_config
                    if cond.then_step_id and cond.then_step_id not in node_map:
                        raise WorkflowIRBranchTargetMissingError(node.node_id, cond.then_step_id, "then_step_id")
                    if cond.else_step_id and cond.else_step_id not in node_map:
                        raise WorkflowIRBranchTargetMissingError(node.node_id, cond.else_step_id, "else_step_id")

                # If node is SWITCH, verify case targets exist
                if node.primitive_definition.switch_cases:
                    for sc in node.primitive_definition.switch_cases:
                        if sc.target_step_id not in node_map:
                            raise WorkflowIRBranchTargetMissingError(node.node_id, sc.target_step_id, f"switch_case({sc.match_value})")
                    if node.primitive_definition.default_switch_step and node.primitive_definition.default_switch_step not in node_map:
                        raise WorkflowIRBranchTargetMissingError(node.node_id, node.primitive_definition.default_switch_step, "default_switch_step")

        # 4. Verify parallel side-effect conflicts
        cls.validate_parallel_side_effects(ir.nodes, ir.edges)

        # 5. Cycle Detection with controlled loop allowance
        cls.detect_illegal_cycles(ir.nodes, ir.edges)

        # 6. Verify topological order validity if present
        if ir.topological_order:
            if set(ir.topological_order) != set(node_ids) or len(ir.topological_order) != len(node_ids):
                raise WorkflowIRValidationError("topological_order must include every node exactly once")
            # Verify DAG edge ordering for non-back-edges
            pos = {node_id: idx for idx, node_id in enumerate(ir.topological_order)}
            for edge in ir.edges:
                if edge.edge_type not in {IREdgeType.LOOP_BACK, IREdgeType.RETRY_EDGE, IREdgeType.REPAIR_EDGE}:
                    if pos[edge.source_node_id] >= pos[edge.target_node_id]:
                        raise WorkflowIRValidationError(
                            f"topological order violates forward edge from '{edge.source_node_id}' to '{edge.target_node_id}'"
                        )

    @classmethod
    def validate_parallel_side_effects(
        cls,
        nodes: Sequence[WorkflowIRNode],
        edges: Sequence[WorkflowIREdge],
    ) -> None:
        """Ensure concurrent nodes do not have conflicting non-read-only side effects."""
        node_map = {n.node_id: n for n in nodes}
        # Group siblings by common predecessor
        predecessors: Dict[str, Set[str]] = collections.defaultdict(set)
        successors: Dict[str, Set[str]] = collections.defaultdict(set)
        for edge in edges:
            predecessors[edge.target_node_id].add(edge.source_node_id)
            successors[edge.source_node_id].add(edge.target_node_id)

        # Find parallel siblings
        for parent_id, children in successors.items():
            if len(children) > 1:
                mutating: List[str] = []
                for child_id in children:
                    child_node = node_map.get(child_id)
                    if child_node and child_node.side_effect_class not in {"NONE", "READ_ONLY"}:
                        mutating.append(child_id)
                if len(mutating) > 1:
                    raise ParallelSideEffectConflictError(
                        conflicting_branches=mutating,
                        side_effects=[node_map[m].side_effect_class for m in mutating],
                    )

    @classmethod
    def detect_illegal_cycles(
        cls,
        nodes: Sequence[WorkflowIRNode],
        edges: Sequence[WorkflowIREdge],
    ) -> None:
        """
        Detect cycles in the workflow graph.
        Cycles are permitted IF AND ONLY IF the back-edge is explicitly declared on
        a node governed by a finite-bound LOOP, RETRY, or REPAIR primitive.
        Any undeclared or unbounded cycle raises WorkflowIRCyclicGraphError.
        """
        node_map = {n.node_id: n for n in nodes}
        adj: Dict[str, List[WorkflowIREdge]] = collections.defaultdict(list)
        for edge in edges:
            adj[edge.source_node_id].append(edge)

        visited: Dict[str, int] = {}  # 0=unvisited, 1=visiting (on stack), 2=visited
        path_stack: List[str] = []

        def dfs(u: str) -> None:
            visited[u] = 1
            path_stack.append(u)

            for edge in adj[u]:
                v = edge.target_node_id
                if visited.get(v, 0) == 1:
                    # Found a cycle from u -> v
                    cycle_start_idx = path_stack.index(v)
                    cycle_nodes = path_stack[cycle_start_idx:] + [v]

                    # Check if this cycle is an authorized, host-bounded loop/repair
                    is_authorized_loop = False
                    if edge.edge_type in {IREdgeType.LOOP_BACK, IREdgeType.RETRY_EDGE, IREdgeType.REPAIR_EDGE}:
                        # Source or target must be bounded
                        target_node = node_map.get(v)
                        source_node = node_map.get(u)
                        for candidate in (target_node, source_node):
                            if candidate and candidate.primitive_definition:
                                p_def = candidate.primitive_definition
                                if p_def.primitive_kind in {WorkflowPrimitiveKind.LOOP, WorkflowPrimitiveKind.RETRY, WorkflowPrimitiveKind.REPAIR}:
                                    if p_def.loop_policy and p_def.loop_policy.max_iterations > 0:
                                        is_authorized_loop = True
                                        break
                                    if p_def.retry_policy and p_def.retry_policy.max_attempts > 0:
                                        is_authorized_loop = True
                                        break

                    if not is_authorized_loop:
                        raise WorkflowIRCyclicGraphError(cycle_nodes)

                elif visited.get(v, 0) == 0:
                    dfs(v)

            path_stack.pop()
            visited[u] = 2

        for node in nodes:
            if visited.get(node.node_id, 0) == 0:
                dfs(node.node_id)

    @classmethod
    def compute_canonical_topological_order(
        cls,
        nodes: Sequence[WorkflowIRNode],
        edges: Sequence[WorkflowIREdge],
    ) -> Tuple[str, ...]:
        """
        Compute deterministic topological sort of DAG nodes (ignoring authorized back-edges).
        Uses Kahn's algorithm with lexical tie-breaking: (phase_order, node_id).
        """
        node_map = {n.node_id: n for n in nodes}
        in_degree: Dict[str, int] = {n.node_id: 0 for n in nodes}
        forward_edges: List[WorkflowIREdge] = []

        for edge in edges:
            if edge.edge_type not in {IREdgeType.LOOP_BACK, IREdgeType.RETRY_EDGE, IREdgeType.REPAIR_EDGE}:
                in_degree[edge.target_node_id] = in_degree.get(edge.target_node_id, 0) + 1
                forward_edges.append(edge)

        # Priority queue / sorted list of zero in-degree nodes
        zero_in = [n.node_id for n in nodes if in_degree[n.node_id] == 0]
        zero_in.sort(key=lambda nid: (node_map[nid].phase_order, nid))

        result: List[str] = []
        adj: Dict[str, List[str]] = collections.defaultdict(list)
        for e in forward_edges:
            adj[e.source_node_id].append(e.target_node_id)

        while zero_in:
            curr = zero_in.pop(0)
            result.append(curr)

            for nxt in adj[curr]:
                in_degree[nxt] -= 1
                if in_degree[nxt] == 0:
                    zero_in.append(nxt)
                    zero_in.sort(key=lambda nid: (node_map[nid].phase_order, nid))

        if len(result) != len(nodes):
            missing = set(node_map) - set(result)
            raise WorkflowIRValidationError(f"Could not topologically order all nodes; cycle exists among: {missing}")

        return tuple(result)


# ============================================================================
# 5. Workflow IR Diff Engine
# ============================================================================


class WorkflowIRDiff:
    """Computes structured cryptographic deltas between two ExecutableWorkflowIR definitions."""

    @classmethod
    def diff(cls, left: ExecutableWorkflowIR, right: ExecutableWorkflowIR) -> WorkflowIRDiffResult:
        """Produce a granular diff between two IR instances."""
        left_nodes = {n.node_id: n for n in left.nodes}
        right_nodes = {n.node_id: n for n in right.nodes}

        added_nodes = tuple(sorted(set(right_nodes) - set(left_nodes)))
        removed_nodes = tuple(sorted(set(left_nodes) - set(right_nodes)))

        modified_nodes: List[str] = []
        for nid in set(left_nodes) & set(right_nodes):
            ln = left_nodes[nid].canonical_dict()
            rn = right_nodes[nid].canonical_dict()
            if ln != rn:
                modified_nodes.append(nid)

        left_edges = {(e.source_node_id, e.target_node_id, e.contract_id): e for e in left.edges}
        right_edges = {(e.source_node_id, e.target_node_id, e.contract_id): e for e in right.edges}

        added_edges = tuple(sorted(set(right_edges) - set(left_edges)))
        removed_edges = tuple(sorted(set(left_edges) - set(right_edges)))

        policy_changes: List[str] = []
        if left.wrong_reading_locks != right.wrong_reading_locks:
            policy_changes.append("wrong_reading_locks")
        if left.evaluation_requirements != right.evaluation_requirements:
            policy_changes.append("evaluation_requirements")
        if left.repair_laws != right.repair_laws:
            policy_changes.append("repair_laws")
        if left.authority_lane != right.authority_lane:
            policy_changes.append("authority_lane")

        identical = (
            not added_nodes
            and not removed_nodes
            and not modified_nodes
            and not added_edges
            and not removed_edges
            and not policy_changes
        )

        return WorkflowIRDiffResult(
            identical=identical,
            left_id=left.workflow_ir_id,
            right_id=right.workflow_ir_id,
            added_nodes=added_nodes,
            removed_nodes=removed_nodes,
            modified_nodes=tuple(sorted(modified_nodes)),
            added_edges=added_edges,
            removed_edges=removed_edges,
            policy_changes=tuple(sorted(policy_changes)),
        )


# ============================================================================
# 6. Workflow IR Compiler & Runtime Adapter
# ============================================================================


PRODUCT_BOUNDARY_NORM = {
    "AHP": "ATOMIC_HARNESS_PIPELINE",
    "AIR": "ACTIVATIVE_INTELLIGENCE_RUNTIME",
    "STUDIO": "CONSCIOUS_ACTIVATIONS_STUDIO",
    "INTERVIEW": "INTERVIEW_EXPRESSION",
    "VAE": "VISUAL_ASSET_EDITOR",
    "DELEGATION": "DELEGATION_PROTOCOL",
    "BUILDER": "ATOMIC_HARNESS_BUILDER",
    "ATOMIC_HARNESS_PIPELINE": "ATOMIC_HARNESS_PIPELINE",
    "ACTIVATIVE_INTELLIGENCE_RUNTIME": "ACTIVATIVE_INTELLIGENCE_RUNTIME",
    "CONSCIOUS_ACTIVATIONS_STUDIO": "CONSCIOUS_ACTIVATIONS_STUDIO",
    "INTERVIEW_EXPRESSION": "INTERVIEW_EXPRESSION",
    "VISUAL_ASSET_EDITOR": "VISUAL_ASSET_EDITOR",
    "DELEGATION_PROTOCOL": "DELEGATION_PROTOCOL",
    "ATOMIC_HARNESS_BUILDER": "ATOMIC_HARNESS_BUILDER",
}


class WorkflowIRCompiler:
    """Compiles source representations into canonical Workflow IR and runtime projections."""

    @classmethod
    def compile_from_source(
        cls,
        *,
        workflow_ir_id: str,
        name: str,
        version: str = "1.0.0",
        category_id: str,
        profile_id: str,
        purpose: str,
        authority_lane: AuthorityLane,
        nodes: Sequence[Mapping[str, Any]],
        edges: Sequence[Mapping[str, Any]],
        wrong_reading_locks: Sequence[str] = (),
        evaluation_requirements: Sequence[str] = ("PASS_QA_GATE",),
        repair_laws: Sequence[str] = ("BOUNDED_SAME_SESSION_REPAIR",),
        semantic_dependency_refs: Sequence[str] = (),
    ) -> ExecutableWorkflowIR:
        """Compile raw node/edge mappings into a canonical ExecutableWorkflowIR."""
        ir_nodes: List[WorkflowIRNode] = []
        for n in nodes:
            prim_kind_str = n.get("primitive_kind", WorkflowPrimitiveKind.SEQUENCE.value)
            try:
                prim_kind = WorkflowPrimitiveKind(prim_kind_str)
            except Exception as exc:
                raise WorkflowIRValidationError(f"Invalid primitive kind '{prim_kind_str}' in node '{n.get('node_id')}'") from exc

            wu_kind_str = n.get("work_unit_kind", WorkUnitKind.NOT_APPLICABLE.value)
            try:
                wu_kind = WorkUnitKind(wu_kind_str)
            except Exception as exc:
                raise WorkflowIRValidationError(f"Invalid work unit kind '{wu_kind_str}' in node '{n.get('node_id')}'") from exc

            # Parse optional primitive definition
            prim_def = n.get("primitive_definition")
            if prim_def is not None and isinstance(prim_def, WorkflowPrimitiveDefinition):
                parsed_prim = prim_def
            else:
                parsed_prim = None

            raw_boundary = n.get("product_boundary", "ATOMIC_HARNESS_PIPELINE")
            normalized_boundary = PRODUCT_BOUNDARY_NORM.get(raw_boundary, raw_boundary)

            ir_node = WorkflowIRNode(
                node_id=n["node_id"],
                capability_id=n["capability_id"],
                phase_order=int(n["phase_order"]),
                purpose=n.get("purpose", f"Step {n['node_id']}"),
                actor_kind=n.get("actor_kind", "DETERMINISTIC_MODULE"),
                role=n.get("role", "ANALYST"),
                product_boundary=normalized_boundary,
                side_effect_class=n.get("side_effect_class", "READ_ONLY"),
                primitive_kind=prim_kind,
                work_unit_kind=wu_kind,
                input_contracts=tuple(n.get("input_contracts", ())),
                output_contracts=tuple(n.get("output_contracts", ())),
                implementation=n.get("implementation"),
                primitive_definition=parsed_prim,
            )
            ir_nodes.append(ir_node)

        ir_edges: List[WorkflowIREdge] = []
        for e in edges:
            edge_type_str = e.get("edge_type", IREdgeType.NORMAL.value)
            try:
                edge_type = IREdgeType(edge_type_str)
            except Exception as exc:
                raise WorkflowIRValidationError(f"Invalid edge type '{edge_type_str}'") from exc

            ir_edge = WorkflowIREdge(
                source_node_id=e["source_node_id"],
                target_node_id=e["target_node_id"],
                contract_id=e.get("contract_id", "STC-DEFAULT-001"),
                edge_type=edge_type,
                guard_expression=e.get("guard_expression"),
                case_value=e.get("case_value"),
            )
            ir_edges.append(ir_edge)

        # 1. Cycle detection first to reject illegal cycles with WorkflowIRCyclicGraphError
        WorkflowIRValidator.detect_illegal_cycles(ir_nodes, ir_edges)

        # 2. Compute deterministic topological order
        topo_order = WorkflowIRValidator.compute_canonical_topological_order(ir_nodes, ir_edges)

        ir = ExecutableWorkflowIR(
            workflow_ir_id=workflow_ir_id,
            name=name,
            version=version,
            category_id=category_id,
            profile_id=profile_id,
            purpose=purpose,
            authority_lane=authority_lane,
            nodes=tuple(ir_nodes),
            edges=tuple(ir_edges),
            topological_order=topo_order,
            wrong_reading_locks=tuple(wrong_reading_locks),
            evaluation_requirements=tuple(evaluation_requirements),
            repair_laws=tuple(repair_laws),
            semantic_dependency_refs=tuple(semantic_dependency_refs),
        )

        # 3. Full validation
        WorkflowIRValidator.validate_ir(ir)
        return ir

    @classmethod
    def compile_to_runtime_projection(
        cls,
        ir: ExecutableWorkflowIR,
        binding_manifest: Mapping[str, Any],
    ) -> Dict[str, Any]:
        """
        Compile ExecutableWorkflowIR and a binding manifest into a runtime projection
        dictionary accepted by validate_runtime_workflow() and RuntimeWorkflowCompiler.
        """
        WorkflowIRValidator.validate_ir(ir)

        bindings = {b["capability_id"]: b for b in binding_manifest.get("bindings", [])}

        runtime_nodes: List[Dict[str, Any]] = []
        for node in sorted(ir.nodes, key=lambda item: (item.phase_order, item.node_id)):
            binding = bindings.get(node.capability_id)
            if not binding and not node.implementation:
                raise WorkflowIRCompilationError(
                    f"No implementation binding found for node '{node.node_id}' with capability '{node.capability_id}'"
                )

            impl = node.implementation or {
                "implementation_id": binding["implementation_id"],
                "implementation_version": binding["implementation_version"],
                "implementation_sha256": binding["implementation_sha256"],
                "owner_product": binding.get("owner_product", node.product_boundary),
                "implementation_kind": binding.get("implementation_kind", "DETERMINISTIC_MODULE"),
                "side_effect_class": binding.get("side_effect_class", node.side_effect_class),
                "authority_boundary": binding.get("authority_boundary", node.role),
            }

            runtime_nodes.append({
                "node_id": node.node_id,
                "capability_id": node.capability_id,
                "phase_order": node.phase_order,
                "purpose": node.purpose,
                "actor_kind": node.actor_kind,
                "role": node.role,
                "product_boundary": node.product_boundary,
                "input_contracts": list(node.input_contracts),
                "output_contracts": list(node.output_contracts),
                "side_effect_class": node.side_effect_class,
                "implementation": impl,
            })

        runtime_edges = [
            {
                "source_node_id": e.source_node_id,
                "target_node_id": e.target_node_id,
                "contract_id": e.contract_id,
            }
            for e in sorted(ir.edges, key=lambda item: (item.source_node_id, item.target_node_id, item.contract_id))
        ]

        projection_payload = {
            "source_projection_id": f"proj_{ir.workflow_ir_id}",
            "binding_manifest_id": binding_manifest.get("manifest_id", f"bm_{ir.workflow_ir_id}"),
            "category_id": ir.category_id,
            "profile_id": ir.profile_id,
            "purpose": ir.purpose,
            "semantic_dependency_refs": list(ir.semantic_dependency_refs),
            "nodes": runtime_nodes,
            "edges": runtime_edges,
            "topological_order": list(ir.topological_order),
            "runtime_projection_digest": ir.ir_digest_sha256,
            "semantic_parity_digest": hashlib.sha256(ir.ir_digest_sha256.encode("utf-8")).hexdigest(),
            "wrong_reading_locks": list(ir.wrong_reading_locks),
            "evaluation_requirements": list(ir.evaluation_requirements) or ["DEFAULT_EVALUATION"],
            "repair_laws": list(ir.repair_laws) or ["DEFAULT_REPAIR_LAW"],
        }
        return projection_payload
