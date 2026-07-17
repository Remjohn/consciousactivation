"""Governed large-collection budgets for OD-AM-005 / ST-10.14."""

from __future__ import annotations

from dataclasses import dataclass
import base64
import hashlib
import json
from typing import Any, Sequence


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class CollectionBudgetError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


@dataclass(frozen=True)
class CollectionBudget:
    max_returned_records: int = 100
    page_size: int = 25
    traversal_depth: int = 3
    graph_nodes: int = 100
    graph_edges: int = 250
    evidence_expansion_count: int = 50
    output_byte_size: int = 100_000
    processing_duration_ms: int = 1_000
    context_size: int = 20_000
    export_size: int = 250_000
    memory_use: int = 10_000_000

    def __post_init__(self) -> None:
        numeric = self.__dict__.values()
        if any(value <= 0 for value in numeric):
            raise CollectionBudgetError("INVALID_BUDGET", "budgets must be positive")
        if self.page_size > self.max_returned_records:
            raise CollectionBudgetError("PAGE_SIZE_EXCEEDS_MAX_RECORDS", "page size cannot exceed max returned records")

    @property
    def budget_identity(self) -> str:
        return sha256_of(self.__dict__)


def _encode_cursor(revision: str, offset: int, budget_identity: str) -> str:
    raw = json.dumps({"revision": revision, "offset": offset, "budget": budget_identity}, sort_keys=True, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode()


def _decode_cursor(cursor: str) -> dict[str, Any]:
    try:
        return json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())
    except Exception as exc:  # pragma: no cover - exact exception varies by Python/base64 failure mode
        raise CollectionBudgetError("INVALID_CURSOR", "cursor is not a governed continuation cursor") from exc


def paginate_records(records: Sequence[dict[str, Any]], *, budget: CollectionBudget, revision: str, cursor: str | None = None) -> dict[str, Any]:
    ordered = sorted(records, key=lambda item: (str(item.get("sort_key", "")), str(item.get("identity", ""))))
    offset = 0
    if cursor is not None:
        decoded = _decode_cursor(cursor)
        if decoded.get("revision") != revision or decoded.get("budget") != budget.budget_identity:
            raise CollectionBudgetError("REVISION_BOUND_CURSOR_MISMATCH", "cursor does not match revision and budget")
        offset = int(decoded["offset"])
    page_size = min(budget.page_size, budget.max_returned_records)
    page = ordered[offset : offset + page_size]
    next_offset = offset + len(page)
    return {
        "records": page,
        "partial": next_offset < len(ordered),
        "budget_exceeded": len(ordered) > budget.max_returned_records,
        "next_cursor": _encode_cursor(revision, next_offset, budget.budget_identity) if next_offset < len(ordered) else None,
        "revision": revision,
        "budget_identity": budget.budget_identity,
        "production_ready": False,
        "certified": False,
    }


def bounded_graph_traversal(nodes: Sequence[str], edges: Sequence[tuple[str, str]], *, budget: CollectionBudget) -> dict[str, Any]:
    ordered_nodes = sorted(nodes)[: budget.graph_nodes]
    node_set = set(ordered_nodes)
    ordered_edges = sorted(edge for edge in edges if edge[0] in node_set and edge[1] in node_set)[: budget.graph_edges]
    return {
        "nodes": ordered_nodes,
        "edges": ordered_edges,
        "partial": len(nodes) > len(ordered_nodes) or len(edges) > len(ordered_edges),
        "budget_exceeded": len(nodes) > budget.graph_nodes or len(edges) > budget.graph_edges,
        "budget_identity": budget.budget_identity,
    }
