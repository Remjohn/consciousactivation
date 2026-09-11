"""Cryptographic Evidence DAG (INV-DAG-001 / CA-M050).

Establishes the evidence topology as a durable, strictly acyclic,
multi-parent causal DAG whose nodes point backward to authoritative
evidence and whose rejected alternatives are explicitly pruned rather
than silently discarded.

Nodes link temporal evidence moments, transcripts, tension matrices,
and synthesized media blocks. Every parent edge carries a cryptographic
parent-hash that is verified on construction and on reopen. Topological
ordering alone is never treated as proof of provenance.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRUNED_REJECTION = "PRUNED_REJECTION"
"""Explicit marker recorded on edges/nodes that were rejected and pruned."""

EVIDENCE_DAG_VERSION = "1.0.0"
NODE_ID_PREFIX = "evidence-node"
EDGE_ID_PREFIX = "evidence-edge"


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class DAGValidationError(ValueError):
    """Base error for Evidence DAG invariant violations."""


class CycleDetectedError(DAGValidationError):
    """Raised when adding an edge or validating the graph would create a cycle."""


class MissingParentError(DAGValidationError):
    """Raised when a declared parent node identity does not exist in the DAG."""


class ParentHashMismatchError(DAGValidationError):
    """Raised when a recorded parent hash does not match the live parent content hash."""


class CrossTenantError(DAGValidationError):
    """Raised when a parent or child references a different workspace/tenant."""


class InferredParentError(DAGValidationError):
    """Raised when a parent reference was inferred rather than explicitly persisted."""


class NodeNotFoundError(DAGValidationError):
    """Raised when a requested node identity is absent from the DAG."""


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class EvidenceNodeKind(str, Enum):
    """Kinds of evidence that may appear as DAG nodes."""

    TEMPORAL_MOMENT = "TEMPORAL_MOMENT"
    TRANSCRIPT = "TRANSCRIPT"
    TENSION_MATRIX = "TENSION_MATRIX"
    SYNTHESIZED_MEDIA = "SYNTHESIZED_MEDIA"
    RECEIPT = "RECEIPT"
    COMPOSITE = "COMPOSITE"


class EvidenceNodeStatus(str, Enum):
    """Lifecycle status of an evidence node."""

    ACTIVE = "ACTIVE"
    PRUNED = "PRUNED"
    SUPERSEDED = "SUPERSEDED"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canonical_json_bytes(value: Any) -> bytes:
    """Deterministic JSON serialization for hashing (sort_keys, no whitespace)."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def content_hash(payload: Mapping[str, Any] | dict[str, Any]) -> str:
    """SHA-256 of canonical JSON payload. Returns lowercase hex digest."""
    return hashlib.sha256(_canonical_json_bytes(dict(payload))).hexdigest()


def make_node_id(kind: EvidenceNodeKind | str, content_digest: str) -> str:
    """Deterministic node identity from kind + content digest."""
    kind_value = kind.value if isinstance(kind, EvidenceNodeKind) else str(kind)
    material = f"{kind_value}:{content_digest}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"{NODE_ID_PREFIX}:{digest}"


def make_edge_id(child_id: str, parent_id: str, relation: str) -> str:
    """Deterministic edge identity from child, parent, and relation type."""
    material = f"{child_id}|{parent_id}|{relation}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"{EDGE_ID_PREFIX}:{digest}"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EvidenceEdge:
    """Directed edge from child → parent (backward provenance).

    The edge records the cryptographic hash of the parent at the moment
    the link was established so that later mutation of the parent is
    detectable.
    """

    edge_id: str
    child_id: str
    parent_id: str
    parent_content_hash: str
    relation: str
    workspace_id: str
    status: str = "ACTIVE"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "child_id": self.child_id,
            "parent_id": self.parent_id,
            "parent_content_hash": self.parent_content_hash,
            "relation": self.relation,
            "workspace_id": self.workspace_id,
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvidenceEdge":
        return cls(
            edge_id=str(data["edge_id"]),
            child_id=str(data["child_id"]),
            parent_id=str(data["parent_id"]),
            parent_content_hash=str(data["parent_content_hash"]),
            relation=str(data["relation"]),
            workspace_id=str(data["workspace_id"]),
            status=str(data.get("status", "ACTIVE")),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(frozen=True)
class EvidenceNode:
    """A single evidence node in the causal DAG.

    Nodes are content-addressed. The ``content_hash`` is computed from
    the semantic payload excluding identity and status fields so that
    status transitions (e.g. ACTIVE → PRUNED) do not change the hash
    that children verified against.
    """

    node_id: str
    kind: EvidenceNodeKind
    workspace_id: str
    content_hash: str
    payload: Mapping[str, Any]
    status: EvidenceNodeStatus = EvidenceNodeStatus.ACTIVE
    created_at: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "kind": self.kind.value,
            "workspace_id": self.workspace_id,
            "content_hash": self.content_hash,
            "payload": dict(self.payload),
            "status": self.status.value,
            "created_at": self.created_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvidenceNode":
        return cls(
            node_id=str(data["node_id"]),
            kind=EvidenceNodeKind(str(data["kind"])),
            workspace_id=str(data["workspace_id"]),
            content_hash=str(data["content_hash"]),
            payload=dict(data.get("payload") or {}),
            status=EvidenceNodeStatus(str(data.get("status", "ACTIVE"))),
            created_at=data.get("created_at"),
            metadata=dict(data.get("metadata") or {}),
        )


# ---------------------------------------------------------------------------
# EvidenceDAG
# ---------------------------------------------------------------------------


class EvidenceDAG:
    """Strictly acyclic, multi-parent cryptographic evidence DAG.

    Design rules (INV-DAG-001):
    - Nodes point *backward* to authoritative parents (child → parent edges).
    - Parent existence and parent content-hash are verified on every link.
    - Workspace (tenant) binding is enforced; cross-tenant links are rejected.
    - Cycles are rejected at construction time.
    - Rejected alternatives receive an explicit PRUNED_REJECTION marker;
      they are never silently dropped.
    - Topological sort success alone is *not* treated as provenance proof.
    - Parent references must be explicitly persisted; inferred parents are
      rejected (InferredParentError).
    """

    def __init__(self, workspace_id: str | None = None) -> None:
        self._workspace_id: str | None = workspace_id
        self._nodes: dict[str, EvidenceNode] = {}
        self._edges: dict[str, EvidenceEdge] = {}
        # adjacency: child_id → set of parent_ids (active edges only)
        self._parents: dict[str, set[str]] = defaultdict(set)
        # reverse adjacency: parent_id → set of child_ids
        self._children: dict[str, set[str]] = defaultdict(set)

    # -- construction -------------------------------------------------------

    @property
    def workspace_id(self) -> str | None:
        return self._workspace_id

    def node_count(self) -> int:
        return len(self._nodes)

    def edge_count(self, *, include_pruned: bool = False) -> int:
        if include_pruned:
            return len(self._edges)
        return sum(1 for e in self._edges.values() if e.status == "ACTIVE")

    def add_node(
        self,
        *,
        kind: EvidenceNodeKind | str,
        payload: Mapping[str, Any],
        workspace_id: str,
        node_id: str | None = None,
        created_at: str | None = None,
        metadata: Mapping[str, Any] | None = None,
        status: EvidenceNodeStatus | str = EvidenceNodeStatus.ACTIVE,
    ) -> EvidenceNode:
        """Add an evidence node. Content-hash is derived from payload only."""
        if not workspace_id:
            raise DAGValidationError("workspace_id is required")

        if self._workspace_id is None:
            self._workspace_id = workspace_id
        elif workspace_id != self._workspace_id:
            raise CrossTenantError(
                f"node workspace_id={workspace_id!r} does not match "
                f"DAG workspace_id={self._workspace_id!r}"
            )

        kind_enum = kind if isinstance(kind, EvidenceNodeKind) else EvidenceNodeKind(str(kind))
        status_enum = (
            status if isinstance(status, EvidenceNodeStatus) else EvidenceNodeStatus(str(status))
        )
        digest = content_hash(payload)
        resolved_id = node_id or make_node_id(kind_enum, digest)

        if resolved_id in self._nodes:
            existing = self._nodes[resolved_id]
            if existing.content_hash != digest:
                raise DAGValidationError(
                    f"node_id {resolved_id!r} already exists with different content_hash"
                )
            return existing

        node = EvidenceNode(
            node_id=resolved_id,
            kind=kind_enum,
            workspace_id=workspace_id,
            content_hash=digest,
            payload=dict(payload),
            status=status_enum,
            created_at=created_at,
            metadata=dict(metadata or {}),
        )
        self._nodes[resolved_id] = node
        return node

    def link_parent(
        self,
        *,
        child_id: str,
        parent_id: str,
        relation: str = "DERIVES_FROM",
        metadata: Mapping[str, Any] | None = None,
        allow_inferred: bool = False,
    ) -> EvidenceEdge:
        """Create a verified parent edge (child → parent).

        Verifies:
        - both nodes exist
        - same workspace
        - parent content hash is recorded and matches live parent
        - adding the edge does not create a cycle
        - parent was not inferred unless allow_inferred=True
        """
        if not allow_inferred and metadata and metadata.get("inferred") is True:
            raise InferredParentError(
                f"parent {parent_id!r} was marked inferred; explicit persistence required"
            )

        child = self._require_node(child_id)
        parent = self._require_node(parent_id)

        if child.workspace_id != parent.workspace_id:
            raise CrossTenantError(
                f"cross-tenant link refused: child workspace={child.workspace_id!r} "
                f"parent workspace={parent.workspace_id!r}"
            )
        if self._workspace_id and child.workspace_id != self._workspace_id:
            raise CrossTenantError(
                f"child workspace={child.workspace_id!r} does not match "
                f"DAG workspace={self._workspace_id!r}"
            )

        # Cycle check: would parent be reachable *from* child already
        # (i.e. is parent already a descendant of child)?
        if self._would_create_cycle(child_id, parent_id):
            raise CycleDetectedError(
                f"linking {child_id!r} → {parent_id!r} would create a cycle"
            )

        edge_id = make_edge_id(child_id, parent_id, relation)
        if edge_id in self._edges:
            existing = self._edges[edge_id]
            if existing.status == "ACTIVE":
                # Re-verify parent hash
                if existing.parent_content_hash != parent.content_hash:
                    raise ParentHashMismatchError(
                        f"edge {edge_id!r}: recorded parent_content_hash "
                        f"{existing.parent_content_hash!r} != live {parent.content_hash!r}"
                    )
                return existing

        edge = EvidenceEdge(
            edge_id=edge_id,
            child_id=child_id,
            parent_id=parent_id,
            parent_content_hash=parent.content_hash,
            relation=relation,
            workspace_id=child.workspace_id,
            status="ACTIVE",
            metadata=dict(metadata or {}),
        )
        self._edges[edge_id] = edge
        self._parents[child_id].add(parent_id)
        self._children[parent_id].add(child_id)
        return edge

    def prune(
        self,
        node_id: str,
        *,
        reason: str = PRUNED_REJECTION,
        metadata: Mapping[str, Any] | None = None,
    ) -> EvidenceNode:
        """Explicitly prune a node. Records PRUNED_REJECTION; does not delete.

        Pruned nodes remain addressable so that rejected alternatives are
        auditable rather than silently discarded.
        """
        node = self._require_node(node_id)
        if node.status == EvidenceNodeStatus.PRUNED:
            return node

        meta = dict(node.metadata)
        meta["prune_reason"] = reason
        if metadata:
            meta.update(metadata)

        pruned = EvidenceNode(
            node_id=node.node_id,
            kind=node.kind,
            workspace_id=node.workspace_id,
            content_hash=node.content_hash,
            payload=node.payload,
            status=EvidenceNodeStatus.PRUNED,
            created_at=node.created_at,
            metadata=meta,
        )
        self._nodes[node_id] = pruned

        # Mark incident edges as pruned
        for edge_id, edge in list(self._edges.items()):
            if edge.child_id == node_id or edge.parent_id == node_id:
                if edge.status == "ACTIVE":
                    self._edges[edge_id] = EvidenceEdge(
                        edge_id=edge.edge_id,
                        child_id=edge.child_id,
                        parent_id=edge.parent_id,
                        parent_content_hash=edge.parent_content_hash,
                        relation=edge.relation,
                        workspace_id=edge.workspace_id,
                        status=PRUNED_REJECTION,
                        metadata={**dict(edge.metadata), "prune_reason": reason},
                    )
                    self._parents[edge.child_id].discard(edge.parent_id)
                    self._children[edge.parent_id].discard(edge.child_id)
        return pruned

    # -- queries ------------------------------------------------------------

    def get_node(self, node_id: str) -> EvidenceNode:
        return self._require_node(node_id)

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def parents_of(self, node_id: str, *, include_pruned: bool = False) -> list[str]:
        self._require_node(node_id)
        if include_pruned:
            return sorted(
                e.parent_id
                for e in self._edges.values()
                if e.child_id == node_id
            )
        return sorted(self._parents.get(node_id, set()))

    def children_of(self, node_id: str, *, include_pruned: bool = False) -> list[str]:
        self._require_node(node_id)
        if include_pruned:
            return sorted(
                e.child_id
                for e in self._edges.values()
                if e.parent_id == node_id
            )
        return sorted(self._children.get(node_id, set()))

    def edges_of(self, node_id: str, *, include_pruned: bool = False) -> list[EvidenceEdge]:
        self._require_node(node_id)
        result = []
        for edge in self._edges.values():
            if edge.child_id == node_id or edge.parent_id == node_id:
                if include_pruned or edge.status == "ACTIVE":
                    result.append(edge)
        return sorted(result, key=lambda e: e.edge_id)

    # -- verification & traversal -------------------------------------------

    def verify_parent_hashes(self) -> list[str]:
        """Re-verify every active edge's recorded parent content hash.

        Returns a list of edge_ids that failed verification (empty = ok).
        Raises ParentHashMismatchError if any mismatch is found when
        ``strict`` is desired by the caller — this method returns the list
        so callers can decide.
        """
        failures: list[str] = []
        for edge in self._edges.values():
            if edge.status != "ACTIVE":
                continue
            parent = self._nodes.get(edge.parent_id)
            if parent is None:
                failures.append(edge.edge_id)
                continue
            if parent.content_hash != edge.parent_content_hash:
                failures.append(edge.edge_id)
        return failures

    def verify_all(self, *, strict: bool = True) -> dict[str, Any]:
        """Full invariant check.

        Checks:
        - all parent references resolve
        - parent content hashes match
        - no cycles
        - workspace consistency
        - no inferred parents on active edges
        """
        report: dict[str, Any] = {
            "node_count": self.node_count(),
            "active_edge_count": self.edge_count(include_pruned=False),
            "pruned_edge_count": self.edge_count(include_pruned=True) - self.edge_count(include_pruned=False),
            "acyclic": True,
            "parent_hash_ok": True,
            "workspace_ok": True,
            "no_inferred_parents": True,
            "failures": [],
        }

        # Missing parents / hash mismatches
        for edge in self._edges.values():
            if edge.status != "ACTIVE":
                continue
            parent = self._nodes.get(edge.parent_id)
            if parent is None:
                report["failures"].append(
                    {"type": "missing_parent", "edge_id": edge.edge_id, "parent_id": edge.parent_id}
                )
                report["parent_hash_ok"] = False
                continue
            if parent.content_hash != edge.parent_content_hash:
                report["failures"].append(
                    {
                        "type": "parent_hash_mismatch",
                        "edge_id": edge.edge_id,
                        "recorded": edge.parent_content_hash,
                        "live": parent.content_hash,
                    }
                )
                report["parent_hash_ok"] = False
            if edge.metadata.get("inferred") is True:
                report["failures"].append(
                    {"type": "inferred_parent", "edge_id": edge.edge_id, "parent_id": edge.parent_id}
                )
                report["no_inferred_parents"] = False
            if self._workspace_id and edge.workspace_id != self._workspace_id:
                report["failures"].append(
                    {
                        "type": "cross_tenant",
                        "edge_id": edge.edge_id,
                        "edge_workspace": edge.workspace_id,
                        "dag_workspace": self._workspace_id,
                    }
                )
                report["workspace_ok"] = False

        # Cycle detection via topological sort attempt
        try:
            self.topological_order()
        except CycleDetectedError as exc:
            report["acyclic"] = False
            report["failures"].append({"type": "cycle", "detail": str(exc)})

        # Workspace consistency of nodes
        for node in self._nodes.values():
            if self._workspace_id and node.workspace_id != self._workspace_id:
                report["workspace_ok"] = False
                report["failures"].append(
                    {
                        "type": "cross_tenant_node",
                        "node_id": node.node_id,
                        "node_workspace": node.workspace_id,
                        "dag_workspace": self._workspace_id,
                    }
                )

        ok = (
            report["acyclic"]
            and report["parent_hash_ok"]
            and report["workspace_ok"]
            and report["no_inferred_parents"]
            and not report["failures"]
        )
        report["ok"] = ok

        if strict and not ok:
            # Raise the most specific error available
            for f in report["failures"]:
                t = f.get("type")
                if t == "cycle":
                    raise CycleDetectedError(f.get("detail", "cycle detected"))
                if t == "missing_parent":
                    raise MissingParentError(f"parent {f.get('parent_id')!r} missing")
                if t == "parent_hash_mismatch":
                    raise ParentHashMismatchError(
                        f"edge {f.get('edge_id')}: recorded {f.get('recorded')} != live {f.get('live')}"
                    )
                if t == "inferred_parent":
                    raise InferredParentError(
                        f"edge {f.get('edge_id')} references inferred parent {f.get('parent_id')}"
                    )
                if t in ("cross_tenant", "cross_tenant_node"):
                    raise CrossTenantError(str(f))
            raise DAGValidationError(f"DAG verification failed: {report['failures']}")

        return report

    def topological_order(self, *, include_pruned: bool = False) -> list[str]:
        """Deterministic topological order (parents before children).

        Uses Kahn's algorithm with sorted queues for determinism.
        Raises CycleDetectedError if a cycle exists among the selected nodes.
        """
        # Build indegree over active (or all) edges
        nodes = [
            n.node_id
            for n in self._nodes.values()
            if include_pruned or n.status != EvidenceNodeStatus.PRUNED
        ]
        node_set = set(nodes)
        indegree: dict[str, int] = {nid: 0 for nid in nodes}
        adjacency: dict[str, list[str]] = defaultdict(list)

        for edge in self._edges.values():
            if not include_pruned and edge.status != "ACTIVE":
                continue
            if edge.parent_id not in node_set or edge.child_id not in node_set:
                continue
            # edge is child → parent; for topo we want parent before child,
            # so adjacency[parent] → child and indegree[child]++
            adjacency[edge.parent_id].append(edge.child_id)
            indegree[edge.child_id] = indegree.get(edge.child_id, 0) + 1

        # Sort adjacency lists for determinism
        for k in adjacency:
            adjacency[k] = sorted(set(adjacency[k]))

        queue = deque(sorted(nid for nid, deg in indegree.items() if deg == 0))
        order: list[str] = []

        while queue:
            nid = queue.popleft()
            order.append(nid)
            for child in adjacency.get(nid, []):
                indegree[child] -= 1
                if indegree[child] == 0:
                    # maintain sorted insertion
                    # deque doesn't support sorted insert cheaply; rebuild when needed
                    queue.append(child)
            # re-sort queue for determinism after batch
            if queue:
                items = sorted(queue)
                queue = deque(items)

        if len(order) != len(nodes):
            remaining = sorted(set(nodes) - set(order))
            raise CycleDetectedError(
                f"cycle detected; nodes not ordered: {remaining}"
            )
        return order

    def ancestors(self, node_id: str, *, include_pruned: bool = False) -> list[str]:
        """All transitive parents (ancestors) of node_id, deterministic order."""
        self._require_node(node_id)
        visited: set[str] = set()
        stack = list(self.parents_of(node_id, include_pruned=include_pruned))
        while stack:
            pid = stack.pop()
            if pid in visited:
                continue
            visited.add(pid)
            stack.extend(self.parents_of(pid, include_pruned=include_pruned))
        return sorted(visited)

    def descendants(self, node_id: str, *, include_pruned: bool = False) -> list[str]:
        """All transitive children (descendants) of node_id, deterministic order."""
        self._require_node(node_id)
        visited: set[str] = set()
        stack = list(self.children_of(node_id, include_pruned=include_pruned))
        while stack:
            cid = stack.pop()
            if cid in visited:
                continue
            visited.add(cid)
            stack.extend(self.children_of(cid, include_pruned=include_pruned))
        return sorted(visited)

    # -- serialization ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Serialize the full DAG (nodes + edges) for persistence/reopen."""
        return {
            "evidence_dag_version": EVIDENCE_DAG_VERSION,
            "workspace_id": self._workspace_id,
            "nodes": {nid: node.to_dict() for nid, node in sorted(self._nodes.items())},
            "edges": {eid: edge.to_dict() for eid, edge in sorted(self._edges.items())},
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvidenceDAG":
        """Reopen a DAG from serialized form and re-verify parent hashes."""
        workspace_id = data.get("workspace_id")
        dag = cls(workspace_id=str(workspace_id) if workspace_id else None)

        for nid, ndata in (data.get("nodes") or {}).items():
            node = EvidenceNode.from_dict(ndata)
            if dag._workspace_id is None:
                dag._workspace_id = node.workspace_id
            elif node.workspace_id != dag._workspace_id:
                raise CrossTenantError(
                    f"node {nid} workspace {node.workspace_id!r} != DAG {dag._workspace_id!r}"
                )
            dag._nodes[node.node_id] = node

        for eid, edata in (data.get("edges") or {}).items():
            edge = EvidenceEdge.from_dict(edata)
            # Verify parent exists and hash matches for active edges
            if edge.status == "ACTIVE":
                parent = dag._nodes.get(edge.parent_id)
                if parent is None:
                    raise MissingParentError(
                        f"edge {edge.edge_id}: parent {edge.parent_id!r} not found on reopen"
                    )
                if parent.content_hash != edge.parent_content_hash:
                    raise ParentHashMismatchError(
                        f"edge {edge.edge_id}: parent hash mismatch on reopen "
                        f"(recorded={edge.parent_content_hash!r}, live={parent.content_hash!r})"
                    )
                if edge.metadata.get("inferred") is True:
                    raise InferredParentError(
                        f"edge {edge.edge_id}: inferred parent refused on reopen"
                    )
                dag._parents[edge.child_id].add(edge.parent_id)
                dag._children[edge.parent_id].add(edge.child_id)
            dag._edges[edge.edge_id] = edge

        # Final acyclicity check
        dag.topological_order(include_pruned=True)
        return dag

    def evidence_refs(self) -> list[dict[str, Any]]:
        """Export evidence_refs serialization (node identities + content hashes)."""
        refs = []
        for node in sorted(self._nodes.values(), key=lambda n: n.node_id):
            refs.append(
                {
                    "node_id": node.node_id,
                    "kind": node.kind.value,
                    "content_hash": node.content_hash,
                    "workspace_id": node.workspace_id,
                    "status": node.status.value,
                }
            )
        return refs

    # -- internal -----------------------------------------------------------

    def _require_node(self, node_id: str) -> EvidenceNode:
        node = self._nodes.get(node_id)
        if node is None:
            raise NodeNotFoundError(f"node {node_id!r} not found in DAG")
        return node

    def _would_create_cycle(self, child_id: str, parent_id: str) -> bool:
        """Return True if adding child→parent would introduce a cycle.

        A cycle exists if parent is already reachable as a descendant of child
        (i.e. there is already a path child ↝ … ↝ parent).
        """
        if child_id == parent_id:
            return True
        # BFS from child following children edges; if we reach parent, cycle
        visited: set[str] = set()
        queue = deque([child_id])
        while queue:
            current = queue.popleft()
            if current == parent_id:
                return True
            if current in visited:
                continue
            visited.add(current)
            for desc in self._children.get(current, set()):
                if desc not in visited:
                    queue.append(desc)
        return False


__all__ = [
    "EvidenceDAG",
    "EvidenceNode",
    "EvidenceNodeKind",
    "EvidenceNodeStatus",
    "EvidenceEdge",
    "DAGValidationError",
    "CycleDetectedError",
    "MissingParentError",
    "ParentHashMismatchError",
    "CrossTenantError",
    "InferredParentError",
    "NodeNotFoundError",
    "PRUNED_REJECTION",
    "content_hash",
    "make_node_id",
    "make_edge_id",
    "EVIDENCE_DAG_VERSION",
]
