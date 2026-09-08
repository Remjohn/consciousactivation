"""
CA-M018 — Hierarchical Context Lineage.

Construct and validate hierarchical parent-child context trees with immutable
revision hashes and cycle detection. Prevent orphaned nodes and enforce
immutable provenance references across all sub-contexts.

Hierarchy (INV-CTX-001 / FR-CTX-001):
    Turn Context → Episode Narrative → Campaign Theme

An utterance or evidence fragment stripped of its episode or campaign parent
is semantically corrupted and must be rejected at the authoritative boundary.
Recovery never invents missing semantic parents.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


MANDATE_ID = "CA-M018"
REQUIREMENT_ID = "FR-CTX-001"
INVARIANT_ID = "INV-CTX-001"
LINEAGE_VERSION = "1.0.0"

LEVEL_ORDER: tuple[str, ...] = ("CAMPAIGN", "EPISODE", "TURN")
LEVEL_RANK = {level: idx for idx, level in enumerate(LEVEL_ORDER)}
CHILD_OF: dict[str, str | None] = {
    "CAMPAIGN": None,
    "EPISODE": "CAMPAIGN",
    "TURN": "EPISODE",
}
PARENT_OF: dict[str, str | None] = {
    "CAMPAIGN": "EPISODE",
    "EPISODE": "TURN",
    "TURN": None,
}

FAILURE_CLASS = {
    "MISSING_NODE": "LINEAGE_ERROR",
    "ORPHAN_NODE": "LINEAGE_ERROR",
    "CYCLE_DETECTED": "LINEAGE_ERROR",
    "LEVEL_VIOLATION": "LINEAGE_ERROR",
    "MISSING_PARENT_REF": "LINEAGE_ERROR",
    "PARENT_MISMATCH": "LINEAGE_ERROR",
    "HASH_MISMATCH": "PROVENANCE_ERROR",
    "IMMUTABLE_VIOLATION": "PROVENANCE_ERROR",
    "DUPLICATE_NODE": "SCHEMA_ERROR",
    "EMPTY_TREE": "SCHEMA_ERROR",
    "INVALID_LEVEL": "SCHEMA_ERROR",
    "FORGED_REVISION": "PROVENANCE_ERROR",
}


class ContextLineageValidationError(ValueError):
    """Raised when CA-M018 hierarchical lineage cannot be admitted."""

    def __init__(self, message: str, *, failure_class: str | None = None):
        if failure_class and not message.startswith(failure_class):
            message = f"{failure_class}: {message}"
        super().__init__(message)
        self.failure_class = failure_class


class ContextLevel(str, Enum):
    CAMPAIGN = "CAMPAIGN"
    EPISODE = "EPISODE"
    TURN = "TURN"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _canonical_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _require_sha256(value: str, field_name: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ContextLineageValidationError(
            f"{field_name} must be a 64-char lowercase SHA-256",
            failure_class=FAILURE_CLASS["FORGED_REVISION"],
        )
    if any(c not in "0123456789abcdef" for c in value):
        raise ContextLineageValidationError(
            f"{field_name} must be a 64-char lowercase SHA-256",
            failure_class=FAILURE_CLASS["FORGED_REVISION"],
        )
    return value


class ImmutableRef(BaseModel):
    """Exact, immutable identity of a context node revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    object_id: str = Field(min_length=1)
    revision_id: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)

    @model_validator(mode="after")
    def _validate_digest(self) -> "ImmutableRef":
        _require_sha256(self.sha256, "sha256")
        return self

    def as_dict(self) -> dict[str, str]:
        return {
            "object_id": self.object_id,
            "revision_id": self.revision_id,
            "sha256": self.sha256,
        }


class ContextNode(BaseModel):
    """
    A single node in the hierarchical context tree.

    revision_hash is derived from (object_id, level, parent_ref, content_payload)
    and is immutable once admitted. parent_ref is required for EPISODE and TURN.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    object_id: str = Field(min_length=1)
    level: ContextLevel
    revision_id: str = Field(min_length=1)
    revision_hash: str = Field(min_length=64, max_length=64)
    parent_ref: ImmutableRef | None = None
    content_digest: str = Field(min_length=64, max_length=64)
    label: str = Field(default="", max_length=512)
    provenance_refs: tuple[ImmutableRef, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _validate_node_invariants(self) -> "ContextNode":
        _require_sha256(self.revision_hash, "revision_hash")
        _require_sha256(self.content_digest, "content_digest")

        expected_parent_level = CHILD_OF[self.level.value]
        if expected_parent_level is None:
            if self.parent_ref is not None:
                raise ContextLineageValidationError(
                    f"CAMPAIGN node '{self.object_id}' must not carry parent_ref",
                    failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
                )
        else:
            if self.parent_ref is None:
                raise ContextLineageValidationError(
                    f"{self.level.value} node '{self.object_id}' requires parent_ref "
                    f"to a {expected_parent_level}",
                    failure_class=FAILURE_CLASS["MISSING_PARENT_REF"],
                )

        # Self-consistency of revision_hash against structural identity.
        structural = {
            "object_id": self.object_id,
            "level": self.level.value,
            "revision_id": self.revision_id,
            "parent_ref": self.parent_ref.as_dict() if self.parent_ref else None,
            "content_digest": self.content_digest,
        }
        expected = _sha256_text(_canonical_json(structural))
        if expected != self.revision_hash:
            raise ContextLineageValidationError(
                f"revision_hash mismatch for node '{self.object_id}' "
                f"(expected {expected}, got {self.revision_hash})",
                failure_class=FAILURE_CLASS["HASH_MISMATCH"],
            )
        return self

    @property
    def identity_key(self) -> str:
        return f"{self.object_id}@{self.revision_id}"


def compute_revision_hash(
    *,
    object_id: str,
    level: str | ContextLevel,
    revision_id: str,
    parent_ref: ImmutableRef | Mapping[str, str] | None,
    content_digest: str,
) -> str:
    """Deterministic revision hash for a context node (immutable once admitted)."""
    level_value = level.value if isinstance(level, ContextLevel) else str(level)
    parent_payload: dict[str, str] | None
    if parent_ref is None:
        parent_payload = None
    elif isinstance(parent_ref, ImmutableRef):
        parent_payload = parent_ref.as_dict()
    else:
        parent_payload = {
            "object_id": str(parent_ref["object_id"]),
            "revision_id": str(parent_ref["revision_id"]),
            "sha256": str(parent_ref["sha256"]),
        }
    structural = {
        "object_id": object_id,
        "level": level_value,
        "revision_id": revision_id,
        "parent_ref": parent_payload,
        "content_digest": content_digest,
    }
    return _sha256_text(_canonical_json(structural))


def make_context_node(
    *,
    object_id: str,
    level: str | ContextLevel,
    revision_id: str,
    content_payload: Mapping[str, Any] | str,
    parent_ref: ImmutableRef | Mapping[str, str] | None = None,
    label: str = "",
    provenance_refs: Sequence[ImmutableRef | Mapping[str, str]] = (),
) -> ContextNode:
    """
    Factory that computes content_digest and revision_hash, then validates
    the resulting immutable ContextNode.
    """
    level_enum = ContextLevel(level) if not isinstance(level, ContextLevel) else level
    if isinstance(content_payload, str):
        content_digest = _sha256_text(content_payload)
    else:
        content_digest = _sha256_text(_canonical_json(dict(content_payload)))

    parent: ImmutableRef | None = None
    if parent_ref is not None:
        if isinstance(parent_ref, ImmutableRef):
            parent = parent_ref
        else:
            parent = ImmutableRef(
                object_id=str(parent_ref["object_id"]),
                revision_id=str(parent_ref["revision_id"]),
                sha256=str(parent_ref["sha256"]),
            )

    prov: list[ImmutableRef] = []
    for item in provenance_refs:
        if isinstance(item, ImmutableRef):
            prov.append(item)
        else:
            prov.append(
                ImmutableRef(
                    object_id=str(item["object_id"]),
                    revision_id=str(item["revision_id"]),
                    sha256=str(item["sha256"]),
                )
            )

    revision_hash = compute_revision_hash(
        object_id=object_id,
        level=level_enum,
        revision_id=revision_id,
        parent_ref=parent,
        content_digest=content_digest,
    )
    try:
        return ContextNode(
            object_id=object_id,
            level=level_enum,
            revision_id=revision_id,
            revision_hash=revision_hash,
            parent_ref=parent,
            content_digest=content_digest,
            label=label,
            provenance_refs=tuple(prov),
        )
    except ValidationError as err:
        raise ContextLineageValidationError(str(err)) from err


class ContextLineageTree(BaseModel):
    """
    Validated hierarchical parent-child context tree.

    Invariants enforced on construction:
    - Exactly one CAMPAIGN root (or forest of roots only if multi-campaign allowed;
      this implementation requires a single connected tree with one CAMPAIGN root).
    - Every EPISODE and TURN has a parent_ref that resolves inside the tree.
    - Parent level is exactly one rank higher (CAMPAIGN←EPISODE←TURN).
    - No cycles.
    - No orphan nodes.
    - All revision hashes are consistent and immutable.
    - Duplicate object_id@revision_id is rejected.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    tree_id: str = Field(min_length=1)
    nodes: tuple[ContextNode, ...] = Field(min_length=1)
    root_ref: ImmutableRef
    lineage_version: str = LINEAGE_VERSION
    tree_hash: str = Field(min_length=64, max_length=64)

    @model_validator(mode="after")
    def _validate_tree(self) -> "ContextLineageTree":
        _require_sha256(self.tree_hash, "tree_hash")
        if not self.nodes:
            raise ContextLineageValidationError(
                "tree must contain at least one node",
                failure_class=FAILURE_CLASS["EMPTY_TREE"],
            )

        by_key: dict[str, ContextNode] = {}
        by_object: dict[str, ContextNode] = {}
        for node in self.nodes:
            key = node.identity_key
            if key in by_key:
                raise ContextLineageValidationError(
                    f"duplicate node identity '{key}'",
                    failure_class=FAILURE_CLASS["DUPLICATE_NODE"],
                )
            by_key[key] = node
            # Latest revision wins for object_id lookup when walking parents;
            # identity still unique on (object_id, revision_id).
            by_object[node.object_id] = node

        # Locate and verify root.
        root_key = f"{self.root_ref.object_id}@{self.root_ref.revision_id}"
        if root_key not in by_key:
            raise ContextLineageValidationError(
                f"root_ref '{root_key}' not present in nodes",
                failure_class=FAILURE_CLASS["MISSING_NODE"],
            )
        root = by_key[root_key]
        if root.level != ContextLevel.CAMPAIGN:
            raise ContextLineageValidationError(
                f"root must be CAMPAIGN level, got {root.level.value}",
                failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
            )
        if root.revision_hash != self.root_ref.sha256:
            raise ContextLineageValidationError(
                "root_ref.sha256 does not match root node revision_hash",
                failure_class=FAILURE_CLASS["HASH_MISMATCH"],
            )

        # Parent resolution, level order, and orphan detection.
        for node in self.nodes:
            if node.level == ContextLevel.CAMPAIGN:
                if node.parent_ref is not None:
                    raise ContextLineageValidationError(
                        f"CAMPAIGN '{node.object_id}' must not have parent",
                        failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
                    )
                continue

            assert node.parent_ref is not None  # enforced by ContextNode
            parent_key = f"{node.parent_ref.object_id}@{node.parent_ref.revision_id}"
            if parent_key not in by_key:
                raise ContextLineageValidationError(
                    f"node '{node.identity_key}' parent_ref '{parent_key}' "
                    "does not resolve inside the tree (orphan)",
                    failure_class=FAILURE_CLASS["ORPHAN_NODE"],
                )
            parent = by_key[parent_key]
            if parent.revision_hash != node.parent_ref.sha256:
                raise ContextLineageValidationError(
                    f"parent_ref.sha256 mismatch for '{node.identity_key}'",
                    failure_class=FAILURE_CLASS["HASH_MISMATCH"],
                )
            expected_parent_level = CHILD_OF[node.level.value]
            if parent.level.value != expected_parent_level:
                raise ContextLineageValidationError(
                    f"node '{node.identity_key}' level {node.level.value} "
                    f"requires parent level {expected_parent_level}, "
                    f"got {parent.level.value}",
                    failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
                )

        # Cycle detection via ancestor walk from every node.
        for node in self.nodes:
            seen: set[str] = set()
            current: ContextNode | None = node
            while current is not None:
                key = current.identity_key
                if key in seen:
                    raise ContextLineageValidationError(
                        f"cycle detected involving '{key}'",
                        failure_class=FAILURE_CLASS["CYCLE_DETECTED"],
                    )
                seen.add(key)
                if current.parent_ref is None:
                    break
                parent_key = (
                    f"{current.parent_ref.object_id}@{current.parent_ref.revision_id}"
                )
                current = by_key.get(parent_key)

        # Reachability from root (no disconnected components / orphans by reachability).
        reachable: set[str] = set()
        stack = [root]
        while stack:
            n = stack.pop()
            key = n.identity_key
            if key in reachable:
                continue
            reachable.add(key)
            for candidate in self.nodes:
                if (
                    candidate.parent_ref is not None
                    and candidate.parent_ref.object_id == n.object_id
                    and candidate.parent_ref.revision_id == n.revision_id
                ):
                    stack.append(candidate)

        if len(reachable) != len(by_key):
            orphans = sorted(set(by_key) - reachable)
            raise ContextLineageValidationError(
                f"unreachable / orphaned nodes: {orphans}",
                failure_class=FAILURE_CLASS["ORPHAN_NODE"],
            )

        # tree_hash consistency.
        node_hashes = sorted(n.revision_hash for n in self.nodes)
        expected_tree = _sha256_text(
            _canonical_json(
                {
                    "tree_id": self.tree_id,
                    "root": self.root_ref.as_dict(),
                    "node_revision_hashes": node_hashes,
                    "lineage_version": self.lineage_version,
                }
            )
        )
        if expected_tree != self.tree_hash:
            raise ContextLineageValidationError(
                f"tree_hash mismatch (expected {expected_tree})",
                failure_class=FAILURE_CLASS["HASH_MISMATCH"],
            )
        return self

    def get_node(self, object_id: str, revision_id: str | None = None) -> ContextNode | None:
        if revision_id is not None:
            key = f"{object_id}@{revision_id}"
            for n in self.nodes:
                if n.identity_key == key:
                    return n
            return None
        for n in self.nodes:
            if n.object_id == object_id:
                return n
        return None

    def ancestors(self, object_id: str, revision_id: str | None = None) -> list[ContextNode]:
        """Return ordered ancestors from parent up to root (inclusive of root)."""
        node = self.get_node(object_id, revision_id)
        if node is None:
            raise ContextLineageValidationError(
                f"node '{object_id}' not found",
                failure_class=FAILURE_CLASS["MISSING_NODE"],
            )
        by_key = {n.identity_key: n for n in self.nodes}
        result: list[ContextNode] = []
        current = node
        seen: set[str] = set()
        while current.parent_ref is not None:
            key = f"{current.parent_ref.object_id}@{current.parent_ref.revision_id}"
            if key in seen:
                raise ContextLineageValidationError(
                    f"cycle while walking ancestors of '{object_id}'",
                    failure_class=FAILURE_CLASS["CYCLE_DETECTED"],
                )
            seen.add(key)
            parent = by_key.get(key)
            if parent is None:
                raise ContextLineageValidationError(
                    f"broken parent link at '{key}'",
                    failure_class=FAILURE_CLASS["ORPHAN_NODE"],
                )
            result.append(parent)
            current = parent
        return result

    def lineage_path(self, object_id: str, revision_id: str | None = None) -> list[ContextNode]:
        """Full path from CAMPAIGN root down to the target node."""
        node = self.get_node(object_id, revision_id)
        if node is None:
            raise ContextLineageValidationError(
                f"node '{object_id}' not found",
                failure_class=FAILURE_CLASS["MISSING_NODE"],
            )
        path = list(reversed(self.ancestors(object_id, revision_id)))
        path.append(node)
        return path

    def require_full_hierarchy(self, turn_object_id: str, turn_revision_id: str | None = None) -> dict[str, ContextNode]:
        """
        Enforce INV-CTX-001 for a TURN: must resolve Turn → Episode → Campaign.
        Returns mapping level -> node. Raises on any missing tier.
        """
        node = self.get_node(turn_object_id, turn_revision_id)
        if node is None:
            raise ContextLineageValidationError(
                f"turn '{turn_object_id}' not found",
                failure_class=FAILURE_CLASS["MISSING_NODE"],
            )
        if node.level != ContextLevel.TURN:
            raise ContextLineageValidationError(
                f"require_full_hierarchy expects TURN, got {node.level.value}",
                failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
            )
        path = self.lineage_path(turn_object_id, turn_revision_id)
        by_level = {n.level.value: n for n in path}
        for required in LEVEL_ORDER:
            if required not in by_level:
                raise ContextLineageValidationError(
                    f"incomplete hierarchy for turn '{turn_object_id}': missing {required}",
                    failure_class=FAILURE_CLASS["MISSING_PARENT_REF"],
                )
        return by_level


def build_context_lineage_tree(
    *,
    tree_id: str,
    nodes: Sequence[ContextNode],
    root: ContextNode | None = None,
) -> ContextLineageTree:
    """
    Construct and fully validate a ContextLineageTree.

    If root is omitted, the single CAMPAIGN node is selected; multiple CAMPAIGN
    roots are rejected.
    """
    node_list = list(nodes)
    if not node_list:
        raise ContextLineageValidationError(
            "cannot build empty lineage tree",
            failure_class=FAILURE_CLASS["EMPTY_TREE"],
        )

    campaigns = [n for n in node_list if n.level == ContextLevel.CAMPAIGN]
    if root is None:
        if len(campaigns) != 1:
            raise ContextLineageValidationError(
                f"exactly one CAMPAIGN root required, found {len(campaigns)}",
                failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
            )
        root = campaigns[0]
    else:
        if root.level != ContextLevel.CAMPAIGN:
            raise ContextLineageValidationError(
                "explicit root must be CAMPAIGN",
                failure_class=FAILURE_CLASS["LEVEL_VIOLATION"],
            )

    root_ref = ImmutableRef(
        object_id=root.object_id,
        revision_id=root.revision_id,
        sha256=root.revision_hash,
    )
    node_hashes = sorted(n.revision_hash for n in node_list)
    tree_hash = _sha256_text(
        _canonical_json(
            {
                "tree_id": tree_id,
                "root": root_ref.as_dict(),
                "node_revision_hashes": node_hashes,
                "lineage_version": LINEAGE_VERSION,
            }
        )
    )
    try:
        return ContextLineageTree(
            tree_id=tree_id,
            nodes=tuple(node_list),
            root_ref=root_ref,
            lineage_version=LINEAGE_VERSION,
            tree_hash=tree_hash,
        )
    except ValidationError as err:
        raise ContextLineageValidationError(str(err)) from err


def validate_hierarchy_refs(
    *,
    turn_ref: ImmutableRef | Mapping[str, str],
    episode_ref: ImmutableRef | Mapping[str, str] | None,
    campaign_ref: ImmutableRef | Mapping[str, str] | None,
) -> None:
    """
    Lightweight structural check for evidence fragments that only carry refs
    (no full tree materialised). Fail-closed: missing episode or campaign is
    rejected. Does not invent parents.
    """

    def _as_ref(value: ImmutableRef | Mapping[str, str], name: str) -> ImmutableRef:
        if isinstance(value, ImmutableRef):
            return value
        try:
            return ImmutableRef(
                object_id=str(value["object_id"]),
                revision_id=str(value["revision_id"]),
                sha256=str(value["sha256"]),
            )
        except Exception as exc:
            raise ContextLineageValidationError(
                f"invalid {name}: {exc}",
                failure_class=FAILURE_CLASS["FORGED_REVISION"],
            ) from exc

    _as_ref(turn_ref, "turn_ref")
    if episode_ref is None:
        raise ContextLineageValidationError(
            "episode_ref is required (INV-CTX-001)",
            failure_class=FAILURE_CLASS["MISSING_PARENT_REF"],
        )
    if campaign_ref is None:
        raise ContextLineageValidationError(
            "campaign_ref is required (INV-CTX-001)",
            failure_class=FAILURE_CLASS["MISSING_PARENT_REF"],
        )
    _as_ref(episode_ref, "episode_ref")
    _as_ref(campaign_ref, "campaign_ref")


def assert_immutable_provenance(
    node: ContextNode,
    expected_revision_hash: str,
) -> None:
    """Reject any attempt to mutate or forge a previously admitted revision."""
    if node.revision_hash != expected_revision_hash:
        raise ContextLineageValidationError(
            f"immutable provenance violation on '{node.object_id}': "
            f"revision_hash changed from {expected_revision_hash} to {node.revision_hash}",
            failure_class=FAILURE_CLASS["IMMUTABLE_VIOLATION"],
        )


def detect_cycles(nodes: Sequence[ContextNode]) -> list[str]:
    """
    Stand-alone cycle detector. Returns list of identity keys participating
    in cycles (empty list means acyclic). Useful for pre-admission diagnostics.
    """
    by_key = {n.identity_key: n for n in nodes}
    cycles: list[str] = []
    for start in nodes:
        seen: list[str] = []
        current: ContextNode | None = start
        visited_in_path: set[str] = set()
        while current is not None:
            key = current.identity_key
            if key in visited_in_path:
                cycles.append(key)
                break
            visited_in_path.add(key)
            seen.append(key)
            if current.parent_ref is None:
                break
            parent_key = (
                f"{current.parent_ref.object_id}@{current.parent_ref.revision_id}"
            )
            current = by_key.get(parent_key)
            if current is None:
                break
    return sorted(set(cycles))
