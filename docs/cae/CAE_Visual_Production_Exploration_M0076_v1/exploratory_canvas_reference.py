"""M0076 isolated behavioral reference for DramaClaw-style canvas exploration.

This module is deliberately not wired to CAE runtime state. It models only the
minimum reversible interaction grammar needed for later integration: node
history, approved agent commands, grouping/locking, branches, and a promotion
request that references (but never mutates) canonical CAE storyboard state.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from hashlib import sha256
import json
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple


class ExplorationError(ValueError):
    """Base error for invalid exploration operations."""


class AuthorizationError(ExplorationError):
    """Agent command lacks explicit approval."""


class StaleRevisionError(ExplorationError):
    """Command was compiled against a non-current canvas revision."""


class LockedNodeError(ExplorationError):
    """Mutation attempted against a locked node."""


class InvalidPromotionError(ExplorationError):
    """Promotion request lacks required canonical linkage or approval."""


@dataclass(frozen=True)
class NodeHistoryEntry:
    history_id: str
    node_id: str
    operation: str
    actor: str
    payload_sha256: str
    revision: int


@dataclass(frozen=True)
class ExplorationNode:
    node_id: str
    kind: str
    position: Tuple[float, float] = (0.0, 0.0)
    data: Mapping[str, Any] = field(default_factory=dict)
    source_refs: Tuple[str, ...] = ()
    group_id: Optional[str] = None
    locked: bool = False
    history: Tuple[NodeHistoryEntry, ...] = ()


@dataclass(frozen=True)
class CanvasReceipt:
    command_id: str
    actor: str
    operation: str
    preconditions: Tuple[str, ...]
    validators: Tuple[str, ...]
    postconditions: Tuple[str, ...]
    revision_before: int
    revision_after: int
    recovery_path: str
    error_route: str
    result_sha256: str


@dataclass(frozen=True)
class AgentCanvasCommand:
    command_id: str
    actor: str
    operation: str
    payload: Mapping[str, Any]
    expected_revision: int
    approved_by_operator: bool = False


@dataclass(frozen=True)
class PromotionRequest:
    workspace_id: str
    canonical_storyboard_id: str
    candidate_id: str
    source_node_ids: Tuple[str, ...]
    source_canvas_revision: int
    source_provenance: Tuple[str, ...]
    operator_receipt_id: str
    operator_approved: bool
    request_sha256: str


@dataclass(frozen=True)
class ExplorationBranch:
    branch_id: str
    parent_canvas_id: str
    parent_revision: int
    node_ids: Tuple[str, ...]
    edge_pairs: Tuple[Tuple[str, str], ...]


class ExploratoryCanvas:
    """Pure in-memory exploration state; no canonical CAE mutation occurs here."""

    def __init__(self, canvas_id: str, project_id: str) -> None:
        self.canvas_id = canvas_id
        self.project_id = project_id
        self.revision = 0
        self.nodes: Dict[str, ExplorationNode] = {}
        self.edges: set[Tuple[str, str]] = set()
        self.groups: Dict[str, Tuple[str, ...]] = {}
        self._receipts: Dict[str, CanvasReceipt] = {}
        self._command_fingerprints: Dict[str, str] = {}

    @staticmethod
    def _digest(value: Any) -> str:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
        return sha256(encoded).hexdigest()

    def _assert_revision(self, command: AgentCanvasCommand) -> None:
        if command.expected_revision != self.revision:
            raise StaleRevisionError(
                f"expected revision {command.expected_revision}, current revision {self.revision}"
            )

    def _assert_unlocked(self, node: ExplorationNode) -> None:
        if node.locked:
            raise LockedNodeError(f"node {node.node_id} is locked")

    def _history_entry(self, node: ExplorationNode, operation: str, actor: str, payload: Any) -> NodeHistoryEntry:
        index = len(node.history) + 1
        history_id = f"{node.node_id}:h{index:04d}"
        return NodeHistoryEntry(
            history_id=history_id,
            node_id=node.node_id,
            operation=operation,
            actor=actor,
            payload_sha256=self._digest(payload),
            revision=self.revision + 1,
        )

    def _receipt(self, command: AgentCanvasCommand, before: int, result: Any, post: Iterable[str]) -> CanvasReceipt:
        after = self.revision
        receipt = CanvasReceipt(
            command_id=command.command_id,
            actor=command.actor,
            operation=command.operation,
            preconditions=(f"canvas_revision={before}", "command_operator_approved=true"),
            validators=("revision_match", "operation_schema", "lock_guard", "exploration_only"),
            postconditions=tuple(post) + (f"canvas_revision={after}",),
            revision_before=before,
            revision_after=after,
            recovery_path="restore_prior_revision_or_discard_branch",
            error_route="return_validation_error_without_mutating_canonical_state",
            result_sha256=self._digest(result),
        )
        self._receipts[command.command_id] = receipt
        self._command_fingerprints[command.command_id] = self._digest(command.payload)
        return receipt

    def apply(self, command: AgentCanvasCommand) -> CanvasReceipt:
        """Apply one bounded command, requiring explicit operator approval."""
        if not command.approved_by_operator:
            raise AuthorizationError("agent-to-canvas commands require explicit operator approval")

        existing = self._receipts.get(command.command_id)
        if existing is not None:
            if self._command_fingerprints[command.command_id] != self._digest(command.payload):
                raise ExplorationError("command_id replay payload mismatch")
            return existing

        self._assert_revision(command)

        before = self.revision
        payload = dict(command.payload)
        op = command.operation

        if op == "create_node":
            node_id = str(payload["node_id"])
            if node_id in self.nodes:
                raise ExplorationError(f"node {node_id} already exists")
            node = ExplorationNode(
                node_id=node_id,
                kind=str(payload["kind"]),
                position=(float(payload.get("x", 0.0)), float(payload.get("y", 0.0))),
                data=dict(payload.get("data", {})),
                source_refs=tuple(payload.get("source_refs", ())),
            )
            node = replace(node, history=(self._history_entry(node, op, command.actor, payload),))
            self.nodes[node_id] = node
            self.revision += 1
            return self._receipt(command, before, {"node_id": node_id}, (f"node={node_id}_created",))

        if op == "update_node":
            node_id = str(payload["node_id"])
            node = self.nodes[node_id]
            self._assert_unlocked(node)
            updated = replace(
                node,
                data={**node.data, **dict(payload.get("data", {}))},
                position=(float(payload["x"]) if "x" in payload else node.position[0],
                          float(payload["y"]) if "y" in payload else node.position[1]),
                source_refs=tuple(payload.get("source_refs", node.source_refs)),
            )
            updated = replace(updated, history=node.history + (self._history_entry(node, op, command.actor, payload),))
            self.nodes[node_id] = updated
            self.revision += 1
            return self._receipt(command, before, {"node_id": node_id}, (f"node={node_id}_updated",))

        if op == "connect":
            source, target = str(payload["source"]), str(payload["target"])
            if source not in self.nodes or target not in self.nodes:
                raise ExplorationError("connect requires existing nodes")
            self.edges.add((source, target))
            self.revision += 1
            return self._receipt(command, before, {"edge": [source, target]}, ("edge_created",))

        if op == "group":
            group_id = str(payload["group_id"])
            node_ids = tuple(str(item) for item in payload["node_ids"])
            if not node_ids or any(item not in self.nodes for item in node_ids):
                raise ExplorationError("group requires one or more existing nodes")
            self.groups[group_id] = node_ids
            for node_id in node_ids:
                self.nodes[node_id] = replace(self.nodes[node_id], group_id=group_id)
            self.revision += 1
            return self._receipt(command, before, {"group_id": group_id}, (f"group={group_id}_created",))

        if op == "lock":
            node_ids = tuple(str(item) for item in payload["node_ids"])
            locked = bool(payload.get("locked", True))
            for node_id in node_ids:
                if node_id not in self.nodes:
                    raise ExplorationError(f"unknown node {node_id}")
                self.nodes[node_id] = replace(self.nodes[node_id], locked=locked)
            self.revision += 1
            return self._receipt(command, before, {"node_ids": node_ids, "locked": locked}, ("lock_state_changed",))

        if op == "restore_node_history":
            node_id = str(payload["node_id"])
            node = self.nodes[node_id]
            self._assert_unlocked(node)
            target = str(payload["history_id"])
            if not any(item.history_id == target for item in node.history):
                raise ExplorationError(f"history entry {target} not found")
            updated = replace(node, data={**node.data, "restored_from_history": target}, history=node.history + (self._history_entry(node, op, command.actor, payload),))
            self.nodes[node_id] = updated
            self.revision += 1
            return self._receipt(command, before, {"node_id": node_id, "restored_from": target}, (f"node={node_id}_restored",))

        if op == "run_node":
            node_id = str(payload["node_id"])
            node = self.nodes[node_id]
            self._assert_unlocked(node)
            proposal = {"node_id": node_id, "execution": "proposal_only", "inputs": dict(payload.get("inputs", {}))}
            updated = replace(node, data={**node.data, "last_run_proposal": proposal}, history=node.history + (self._history_entry(node, op, command.actor, payload),))
            self.nodes[node_id] = updated
            self.revision += 1
            return self._receipt(command, before, proposal, ("run_recorded_as_exploration_only",))

        raise ExplorationError(f"unsupported exploration operation: {op}")

    def branch(self, branch_id: str) -> ExplorationBranch:
        """Create a reversible branch descriptor; canonical state is untouched."""
        return ExplorationBranch(
            branch_id=branch_id,
            parent_canvas_id=self.canvas_id,
            parent_revision=self.revision,
            node_ids=tuple(sorted(self.nodes)),
            edge_pairs=tuple(sorted(self.edges)),
        )

    def promote_request(
        self,
        *,
        workspace_id: str,
        canonical_storyboard_id: str,
        candidate_id: str,
        source_node_ids: Tuple[str, ...],
        operator_receipt_id: str,
        operator_approved: bool,
    ) -> PromotionRequest:
        """Create a governed handoff request without mutating canonical CAE state."""
        if not operator_approved:
            raise InvalidPromotionError("operator approval is required for promotion")
        if not canonical_storyboard_id or not candidate_id or not operator_receipt_id:
            raise InvalidPromotionError("canonical storyboard, candidate and operator receipt are required")
        if not source_node_ids or any(node_id not in self.nodes for node_id in source_node_ids):
            raise InvalidPromotionError("promotion requires existing source nodes")
        provenance = tuple(sorted({ref for node_id in source_node_ids for ref in self.nodes[node_id].source_refs}))
        if not provenance:
            raise InvalidPromotionError("promotion requires source provenance")
        payload = {
            "workspace_id": workspace_id,
            "canonical_storyboard_id": canonical_storyboard_id,
            "candidate_id": candidate_id,
            "source_node_ids": source_node_ids,
            "source_canvas_revision": self.revision,
            "source_provenance": provenance,
            "operator_receipt_id": operator_receipt_id,
            "operator_approved": operator_approved,
        }
        return PromotionRequest(**payload, request_sha256=self._digest(payload))

    def receipts(self) -> Tuple[CanvasReceipt, ...]:
        return tuple(self._receipts[key] for key in sorted(self._receipts))
