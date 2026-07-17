"""Trustworthy graph projections for OD-AM-003 / ST-10.02."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class GraphExplorationError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class GraphFamily(str, Enum):
    PHASE_GRAPH = "PHASE_GRAPH"
    CONTEXT_GRAPH = "CONTEXT_GRAPH"
    DEPENDENCY_GRAPH = "DEPENDENCY_GRAPH"


class ValidityState(str, Enum):
    ACTIVE = "ACTIVE"
    INVALIDATED = "INVALIDATED"
    STALE = "STALE"
    REDACTED = "REDACTED"
    PARTIAL = "PARTIAL"


class SemanticNodeType(str, Enum):
    PHASE = "PHASE"
    CONTEXT_UNIT = "CONTEXT_UNIT"
    STORY_DEPENDENCY = "STORY_DEPENDENCY"
    OBLIGATION_DEPENDENCY = "OBLIGATION_DEPENDENCY"
    RECEIPT_DEPENDENCY = "RECEIPT_DEPENDENCY"
    IMPLEMENTATION_DEPENDENCY = "IMPLEMENTATION_DEPENDENCY"
    EVIDENCE_DEPENDENCY = "EVIDENCE_DEPENDENCY"
    EXTERNAL_DEPENDENCY = "EXTERNAL_DEPENDENCY"


class EdgeType(str, Enum):
    PRECEDES = "PRECEDES"
    DEPENDS_ON = "DEPENDS_ON"
    CONSUMES_CONTEXT = "CONSUMES_CONTEXT"
    PRODUCES_CONTEXT = "PRODUCES_CONTEXT"
    BLOCKED_BY = "BLOCKED_BY"
    SUPERSEDES = "SUPERSEDES"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise GraphExplorationError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class GraphNode:
    local_id: str
    graph_family: GraphFamily
    semantic_type: SemanticNodeType
    source_record: str
    evidence_ref: str
    validity_state: ValidityState
    source_revision: str
    redacted: bool = False
    partial_evidence: bool = False
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for value, name in (
            (self.local_id, "local_id"),
            (self.source_record, "source_record"),
            (self.evidence_ref, "evidence_ref"),
            (self.source_revision, "source_revision"),
        ):
            _text(value, name)
        if self.validity_state is ValidityState.ACTIVE and self.attributes.get("invalidated") is True:
            raise GraphExplorationError("INVALIDATED_NODE_REPRESENTED_ACTIVE", "invalidated evidence cannot be active")

    @property
    def node_identity(self) -> str:
        return sha256_of(self.as_dict(include_identity=False))

    def as_dict(self, *, include_identity: bool = True) -> dict[str, Any]:
        payload = {
            "local_id": self.local_id,
            "graph_family": self.graph_family.value,
            "semantic_type": self.semantic_type.value,
            "source_record": self.source_record,
            "evidence_ref": self.evidence_ref,
            "validity_state": self.validity_state.value,
            "source_revision": self.source_revision,
            "redacted": self.redacted,
            "partial_evidence": self.partial_evidence,
            "attributes": self.attributes,
        }
        if include_identity:
            payload["node_identity"] = sha256_of(payload)
        return payload


@dataclass(frozen=True)
class GraphEdge:
    source_id: str
    target_id: str
    graph_family: GraphFamily
    edge_type: EdgeType
    source_record: str
    evidence_ref: str
    validity_state: ValidityState
    source_revision: str
    external_dependency_builder_owned: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.source_id, "source_id"),
            (self.target_id, "target_id"),
            (self.source_record, "source_record"),
            (self.evidence_ref, "evidence_ref"),
            (self.source_revision, "source_revision"),
        ):
            _text(value, name)
        if self.external_dependency_builder_owned:
            raise GraphExplorationError("EXTERNAL_DEPENDENCY_CLAIMED_BUILDER_OWNED", "external dependencies must remain externally owned")

    @property
    def edge_identity(self) -> str:
        return sha256_of(self.as_dict(include_identity=False))

    def as_dict(self, *, include_identity: bool = True) -> dict[str, Any]:
        payload = {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "graph_family": self.graph_family.value,
            "edge_type": self.edge_type.value,
            "source_record": self.source_record,
            "evidence_ref": self.evidence_ref,
            "validity_state": self.validity_state.value,
            "source_revision": self.source_revision,
            "external_dependency_builder_owned": False,
        }
        if include_identity:
            payload["edge_identity"] = sha256_of(payload)
        return payload


@dataclass(frozen=True)
class GraphProjection:
    graph_family: GraphFamily
    projection_revision: str
    projection_timestamp: str
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]
    acyclic_required: bool = True
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _text(self.projection_revision, "projection_revision")
        _text(self.projection_timestamp, "projection_timestamp")
        if not self.nodes:
            raise GraphExplorationError("EMPTY_GRAPH", "graph projection requires nodes")
        ids = [node.local_id for node in self.nodes]
        if len(ids) != len(set(ids)):
            raise GraphExplorationError("DUPLICATE_GRAPH_NODE", "node ids must be unique")
        if any(node.graph_family is not self.graph_family for node in self.nodes):
            raise GraphExplorationError("GRAPH_FAMILY_FLATTENING_REJECTED", "node graph families must match projection")
        if any(edge.graph_family is not self.graph_family for edge in self.edges):
            raise GraphExplorationError("GRAPH_FAMILY_FLATTENING_REJECTED", "edge graph families must match projection")
        known = set(ids)
        dangling = [edge.as_dict() for edge in self.edges if edge.source_id not in known or edge.target_id not in known]
        if dangling:
            raise GraphExplorationError("DANGLING_EDGE_REJECTED", "edges must reference known nodes", dangling=dangling)
        if self.acyclic_required and detect_cycles(self.nodes, self.edges):
            raise GraphExplorationError("CYCLE_REJECTED", "governed graph is acyclic")
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "graph_family": self.graph_family.value,
            "projection_revision": self.projection_revision,
            "projection_timestamp": self.projection_timestamp,
            "nodes": [node.as_dict() for node in sorted(self.nodes, key=lambda item: item.local_id)],
            "edges": [edge.as_dict() for edge in sorted(self.edges, key=lambda item: (item.source_id, item.target_id, item.edge_type.value))],
            "acyclic_required": self.acyclic_required,
        }

    @property
    def projection_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise GraphExplorationError("MUTATED_GOVERNED_OBJECT", "graph projection changed")
        payload["projection_identity"] = sha256_of(payload)
        return payload


def detect_cycles(nodes: tuple[GraphNode, ...], edges: tuple[GraphEdge, ...]) -> bool:
    adjacency: dict[str, list[str]] = {node.local_id: [] for node in nodes}
    for edge in edges:
        adjacency.setdefault(edge.source_id, []).append(edge.target_id)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node_id: str) -> bool:
        if node_id in visiting:
            return True
        if node_id in visited:
            return False
        visiting.add(node_id)
        for child in adjacency.get(node_id, []):
            if visit(child):
                return True
        visiting.remove(node_id)
        visited.add(node_id)
        return False

    return any(visit(node.local_id) for node in nodes)


def direct_neighbors(projection: GraphProjection, node_id: str) -> tuple[GraphNode, ...]:
    known = {node.local_id: node for node in projection.nodes}
    if node_id not in known:
        return ()
    targets = {edge.target_id for edge in projection.edges if edge.source_id == node_id}
    sources = {edge.source_id for edge in projection.edges if edge.target_id == node_id}
    return tuple(known[item] for item in sorted(targets | sources))


def traverse_successors(projection: GraphProjection, node_id: str, *, depth: int = 1) -> tuple[GraphNode, ...]:
    return _traverse(projection, node_id, depth=depth, reverse=False)


def traverse_predecessors(projection: GraphProjection, node_id: str, *, depth: int = 1) -> tuple[GraphNode, ...]:
    return _traverse(projection, node_id, depth=depth, reverse=True)


def _traverse(projection: GraphProjection, node_id: str, *, depth: int, reverse: bool) -> tuple[GraphNode, ...]:
    if depth < 0:
        raise GraphExplorationError("INVALID_TRAVERSAL_DEPTH", "depth cannot be negative")
    known = {node.local_id: node for node in projection.nodes}
    frontier = {node_id}
    seen: set[str] = set()
    for _ in range(depth):
        next_frontier: set[str] = set()
        for current in frontier:
            for edge in projection.edges:
                if reverse and edge.target_id == current:
                    next_frontier.add(edge.source_id)
                elif not reverse and edge.source_id == current:
                    next_frontier.add(edge.target_id)
        seen |= next_frontier
        frontier = next_frontier
    seen.discard(node_id)
    return tuple(known[item] for item in sorted(seen) if item in known)


def explain_dependency_path(projection: GraphProjection, source_id: str, target_id: str) -> tuple[GraphEdge, ...]:
    if projection.graph_family is not GraphFamily.DEPENDENCY_GRAPH:
        raise GraphExplorationError("DEPENDENCY_PATH_REQUIRES_DEPENDENCY_GRAPH", "path explanation is dependency-graph only")
    queue: list[tuple[str, tuple[GraphEdge, ...]]] = [(source_id, ())]
    visited: set[str] = set()
    while queue:
        current, path = queue.pop(0)
        if current == target_id:
            return path
        if current in visited:
            continue
        visited.add(current)
        for edge in sorted((edge for edge in projection.edges if edge.source_id == current), key=lambda item: item.target_id):
            queue.append((edge.target_id, path + (edge,)))
    return ()


def filter_graph(projection: GraphProjection, *, validity_state: ValidityState | None = None, semantic_type: SemanticNodeType | None = None) -> GraphProjection:
    nodes = tuple(
        node
        for node in projection.nodes
        if (validity_state is None or node.validity_state is validity_state)
        and (semantic_type is None or node.semantic_type is semantic_type)
    )
    node_ids = {node.local_id for node in nodes}
    edges = tuple(edge for edge in projection.edges if edge.source_id in node_ids and edge.target_id in node_ids)
    return GraphProjection(projection.graph_family, projection.projection_revision, projection.projection_timestamp, nodes, edges, projection.acyclic_required)


def stale_projection(projection: GraphProjection, active_revision: str) -> bool:
    _text(active_revision, "active_revision")
    return projection.projection_revision != active_revision
