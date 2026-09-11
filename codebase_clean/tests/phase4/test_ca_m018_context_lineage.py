"""
CA-M018 — Hierarchical Context Lineage tests.

Executable evidence for FR-CTX-001 / INV-CTX-001:
- Positive path: full Turn → Episode → Campaign tree admits and preserves hierarchy.
- Negative path: missing parent, orphan, cycle, hash forgery, level violation rejected.
- Immutable revision hashes and provenance enforcement.
"""

from __future__ import annotations

import copy
import hashlib

import pytest
from pydantic import ValidationError

from conscious_activations_interview_expression.context_lineage import (
    CHILD_OF,
    FAILURE_CLASS,
    LEVEL_ORDER,
    LINEAGE_VERSION,
    MANDATE_ID,
    REQUIREMENT_ID,
    ContextLevel,
    ContextLineageTree,
    ContextLineageValidationError,
    ContextNode,
    ImmutableRef,
    assert_immutable_provenance,
    build_context_lineage_tree,
    compute_revision_hash,
    detect_cycles,
    make_context_node,
    validate_hierarchy_refs,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _campaign(
    object_id: str = "CAMP-01",
    revision_id: str = "r1",
    label: str = "Campaign Theme Alpha",
) -> ContextNode:
    return make_context_node(
        object_id=object_id,
        level=ContextLevel.CAMPAIGN,
        revision_id=revision_id,
        content_payload={"theme": label, "kind": "campaign"},
        label=label,
        parent_ref=None,
    )


def _episode(
    parent: ContextNode,
    object_id: str = "EP-01",
    revision_id: str = "r1",
    label: str = "Episode Narrative One",
) -> ContextNode:
    parent_ref = ImmutableRef(
        object_id=parent.object_id,
        revision_id=parent.revision_id,
        sha256=parent.revision_hash,
    )
    return make_context_node(
        object_id=object_id,
        level=ContextLevel.EPISODE,
        revision_id=revision_id,
        content_payload={"narrative": label, "kind": "episode"},
        label=label,
        parent_ref=parent_ref,
    )


def _turn(
    parent: ContextNode,
    object_id: str = "TURN-01",
    revision_id: str = "r1",
    label: str = "Turn Context A",
) -> ContextNode:
    parent_ref = ImmutableRef(
        object_id=parent.object_id,
        revision_id=parent.revision_id,
        sha256=parent.revision_hash,
    )
    return make_context_node(
        object_id=object_id,
        level=ContextLevel.TURN,
        revision_id=revision_id,
        content_payload={"utterance": label, "kind": "turn"},
        label=label,
        parent_ref=parent_ref,
    )


def _full_tree() -> tuple[ContextNode, ContextNode, ContextNode, ContextLineageTree]:
    camp = _campaign()
    ep = _episode(camp)
    turn = _turn(ep)
    tree = build_context_lineage_tree(
        tree_id="TREE-01",
        nodes=[camp, ep, turn],
    )
    return camp, ep, turn, tree


# ---------------------------------------------------------------------------
# Constants / identity
# ---------------------------------------------------------------------------


def test_mandate_identity():
    assert MANDATE_ID == "CA-M018"
    assert REQUIREMENT_ID == "FR-CTX-001"
    assert LINEAGE_VERSION == "1.0.0"
    assert LEVEL_ORDER == ("CAMPAIGN", "EPISODE", "TURN")
    assert CHILD_OF["TURN"] == "EPISODE"
    assert CHILD_OF["EPISODE"] == "CAMPAIGN"
    assert CHILD_OF["CAMPAIGN"] is None


# ---------------------------------------------------------------------------
# Positive path — full hierarchy admitted
# ---------------------------------------------------------------------------


def test_build_valid_hierarchy_tree():
    camp, ep, turn, tree = _full_tree()

    assert tree.tree_id == "TREE-01"
    assert len(tree.nodes) == 3
    assert tree.root_ref.object_id == camp.object_id
    assert tree.root_ref.sha256 == camp.revision_hash
    assert tree.lineage_version == LINEAGE_VERSION

    by_level = tree.require_full_hierarchy(turn.object_id)
    assert by_level["CAMPAIGN"].object_id == camp.object_id
    assert by_level["EPISODE"].object_id == ep.object_id
    assert by_level["TURN"].object_id == turn.object_id


def test_lineage_path_order():
    camp, ep, turn, tree = _full_tree()
    path = tree.lineage_path(turn.object_id)
    assert [n.level for n in path] == [
        ContextLevel.CAMPAIGN,
        ContextLevel.EPISODE,
        ContextLevel.TURN,
    ]
    assert path[0].object_id == camp.object_id
    assert path[-1].object_id == turn.object_id


def test_ancestors_excludes_self():
    camp, ep, turn, tree = _full_tree()
    ancs = tree.ancestors(turn.object_id)
    assert len(ancs) == 2
    assert ancs[0].object_id == ep.object_id
    assert ancs[1].object_id == camp.object_id


def test_revision_hash_deterministic():
    camp = _campaign()
    h1 = compute_revision_hash(
        object_id=camp.object_id,
        level=camp.level,
        revision_id=camp.revision_id,
        parent_ref=None,
        content_digest=camp.content_digest,
    )
    assert h1 == camp.revision_hash
    h2 = compute_revision_hash(
        object_id=camp.object_id,
        level=camp.level,
        revision_id=camp.revision_id,
        parent_ref=None,
        content_digest=camp.content_digest,
    )
    assert h1 == h2


def test_multiple_turns_under_same_episode():
    camp = _campaign()
    ep = _episode(camp)
    t1 = _turn(ep, object_id="TURN-01")
    t2 = _turn(ep, object_id="TURN-02", label="Turn Context B")
    tree = build_context_lineage_tree(tree_id="TREE-MULTI", nodes=[camp, ep, t1, t2])
    assert len(tree.nodes) == 4
    tree.require_full_hierarchy("TURN-01")
    tree.require_full_hierarchy("TURN-02")


# ---------------------------------------------------------------------------
# Negative path — missing parents / orphans
# ---------------------------------------------------------------------------


def test_reject_turn_without_parent():
    with pytest.raises(ContextLineageValidationError) as exc:
        make_context_node(
            object_id="TURN-ORPHAN",
            level=ContextLevel.TURN,
            revision_id="r1",
            content_payload={"utterance": "orphan"},
            parent_ref=None,
        )
    assert FAILURE_CLASS["MISSING_PARENT_REF"] in str(exc.value)


def test_reject_episode_without_parent():
    with pytest.raises(ContextLineageValidationError) as exc:
        make_context_node(
            object_id="EP-ORPHAN",
            level=ContextLevel.EPISODE,
            revision_id="r1",
            content_payload={"narrative": "orphan"},
            parent_ref=None,
        )
    assert FAILURE_CLASS["MISSING_PARENT_REF"] in str(exc.value)


def test_reject_campaign_with_parent():
    fake_parent = ImmutableRef(
        object_id="FAKE",
        revision_id="r0",
        sha256=_sha("fake"),
    )
    with pytest.raises(ContextLineageValidationError) as exc:
        make_context_node(
            object_id="CAMP-BAD",
            level=ContextLevel.CAMPAIGN,
            revision_id="r1",
            content_payload={"theme": "bad"},
            parent_ref=fake_parent,
        )
    assert FAILURE_CLASS["LEVEL_VIOLATION"] in str(exc.value)


def test_reject_orphan_parent_ref_not_in_tree():
    camp = _campaign()
    # Episode points at a non-existent campaign revision
    bad_parent = ImmutableRef(
        object_id="CAMP-MISSING",
        revision_id="r9",
        sha256=_sha("missing"),
    )
    ep = make_context_node(
        object_id="EP-01",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        content_payload={"narrative": "x"},
        parent_ref=bad_parent,
    )
    with pytest.raises(ContextLineageValidationError) as exc:
        build_context_lineage_tree(tree_id="T", nodes=[camp, ep])
    msg = str(exc.value)
    assert (
        FAILURE_CLASS["ORPHAN_NODE"] in msg
        or FAILURE_CLASS["LEVEL_VIOLATION"] in msg
        or FAILURE_CLASS["MISSING_NODE"] in msg
    )


def test_validate_hierarchy_refs_requires_episode_and_campaign():
    turn_ref = ImmutableRef(
        object_id="TURN-01",
        revision_id="r1",
        sha256=_sha("turn"),
    )
    with pytest.raises(ContextLineageValidationError) as exc:
        validate_hierarchy_refs(
            turn_ref=turn_ref,
            episode_ref=None,
            campaign_ref=ImmutableRef(
                object_id="C", revision_id="r1", sha256=_sha("c")
            ),
        )
    assert FAILURE_CLASS["MISSING_PARENT_REF"] in str(exc.value)

    with pytest.raises(ContextLineageValidationError) as exc2:
        validate_hierarchy_refs(
            turn_ref=turn_ref,
            episode_ref=ImmutableRef(
                object_id="E", revision_id="r1", sha256=_sha("e")
            ),
            campaign_ref=None,
        )
    assert FAILURE_CLASS["MISSING_PARENT_REF"] in str(exc2.value)


def test_validate_hierarchy_refs_accepts_complete():
    validate_hierarchy_refs(
        turn_ref={"object_id": "T", "revision_id": "r1", "sha256": _sha("t")},
        episode_ref={"object_id": "E", "revision_id": "r1", "sha256": _sha("e")},
        campaign_ref={"object_id": "C", "revision_id": "r1", "sha256": _sha("c")},
    )


# ---------------------------------------------------------------------------
# Cycle detection
# ---------------------------------------------------------------------------


def test_detect_cycles_empty_on_valid_tree():
    _, _, _, tree = _full_tree()
    assert detect_cycles(tree.nodes) == []


def test_reject_cycle_via_forged_parent():
    """
    Construct three nodes where parent pointers form a cycle.
    We bypass make_context_node for the cyclic edges by directly building
    ContextNode after computing hashes against the intended (cyclic) parents.
    """
    # Campaign (will be made to point nowhere; cycle is among children via mutual refs)
    # Simpler: EP points to TURN and TURN points to EP (level violation also, but cycle first).
    # To hit pure cycle detection we need consistent levels or accept level+cycle.
    # Build: CAMP <- EP1 <- EP2 <- EP1  (level violation + cycle). Use same level via direct model.
    # Instead use build with nodes that have parent_ref pointing in a loop at TURN level
    # by forging after hash computation is impossible for valid ContextNode.
    # Practical approach: create two episodes both claiming each other as parent
    # using manually constructed ImmutableRefs and accept that level check or cycle fires.

    camp = _campaign()
    # Legitimate episode under camp
    ep_a = _episode(camp, object_id="EP-A")
    # Create ep_b that parents to ep_a (level violation: EP parent must be CAMPAIGN)
    # Then mutate conceptually by building a second tree attempt with swapped parents.

    # Direct cycle on identity keys using detect_cycles helper with synthetic nodes
    # that share level (helper does not re-validate levels).
    ref_a = ImmutableRef(object_id="X", revision_id="r1", sha256=_sha("a"))
    ref_b = ImmutableRef(object_id="Y", revision_id="r1", sha256=_sha("b"))

    # Manually craft minimal frozen-like objects is hard; use detect_cycles with
    # real ContextNodes where parent_ref points across same level after we
    # compute revision_hash against that parent.
    content = _sha("payload")
    # Node X parents to Y
    h_x = compute_revision_hash(
        object_id="X",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_b,
        content_digest=content,
    )
    # Node Y parents to X
    h_y = compute_revision_hash(
        object_id="Y",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_a,
        content_digest=content,
    )
    # Update refs to carry correct sha of the peer revision_hash
    ref_a2 = ImmutableRef(object_id="X", revision_id="r1", sha256=h_x)
    ref_b2 = ImmutableRef(object_id="Y", revision_id="r1", sha256=h_y)
    # Recompute with correct mutual parent shas
    h_x2 = compute_revision_hash(
        object_id="X",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_b2,
        content_digest=content,
    )
    h_y2 = compute_revision_hash(
        object_id="Y",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_a2,
        content_digest=content,
    )
    # One more iteration for fixed point of mutual hashes (sha depends on peer sha)
    ref_a3 = ImmutableRef(object_id="X", revision_id="r1", sha256=h_x2)
    ref_b3 = ImmutableRef(object_id="Y", revision_id="r1", sha256=h_y2)
    h_x3 = compute_revision_hash(
        object_id="X",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_b3,
        content_digest=content,
    )
    h_y3 = compute_revision_hash(
        object_id="Y",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        parent_ref=ref_a3,
        content_digest=content,
    )
    # Still not fixed-point; for cycle detection we only need parent pointers,
    # not full ContextNode validation of hash. Use detect_cycles with
    # nodes that have consistent internal revision_hash for their declared parent.
    node_x = ContextNode.model_construct(
        object_id="X",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        revision_hash=h_x3,
        parent_ref=ImmutableRef(object_id="Y", revision_id="r1", sha256=h_y3),
        content_digest=content,
        label="x",
    )
    node_y = ContextNode.model_construct(
        object_id="Y",
        level=ContextLevel.EPISODE,
        revision_id="r1",
        revision_hash=h_y3,
        parent_ref=ImmutableRef(object_id="X", revision_id="r1", sha256=h_x3),
        content_digest=content,
        label="y",
    )
    # Note: ContextNode validator recomputes expected hash; parent sha must match
    # the peer's revision_hash that was used in structural payload. We already
    # set parent_ref.sha256 = peer revision_hash, and revision_hash computed
    # against that. Should pass node construction.
    cycles = detect_cycles([node_x, node_y])
    assert len(cycles) >= 1

    # Full tree build must also reject (level or cycle or orphan relative to campaign).
    with pytest.raises(ContextLineageValidationError):
        build_context_lineage_tree(tree_id="CYC", nodes=[camp, node_x, node_y])


# ---------------------------------------------------------------------------
# Hash / immutability
# ---------------------------------------------------------------------------


def test_reject_forged_revision_hash():
    camp = _campaign()
    with pytest.raises((ContextLineageValidationError, ValidationError)) as exc:
        ContextNode(
            object_id=camp.object_id,
            level=camp.level,
            revision_id=camp.revision_id,
            revision_hash=_sha("forged"),
            parent_ref=None,
            content_digest=camp.content_digest,
            label=camp.label,
        )
    assert FAILURE_CLASS["HASH_MISMATCH"] in str(exc.value)


def test_assert_immutable_provenance():
    camp = _campaign()
    assert_immutable_provenance(camp, camp.revision_hash)
    with pytest.raises(ContextLineageValidationError) as exc:
        assert_immutable_provenance(camp, _sha("other"))
    assert FAILURE_CLASS["IMMUTABLE_VIOLATION"] in str(exc.value)


def test_tree_hash_covers_all_nodes():
    camp, ep, turn, tree = _full_tree()
    # Adding a node changes tree_hash
    t2 = _turn(ep, object_id="TURN-02")
    tree2 = build_context_lineage_tree(tree_id="TREE-01", nodes=[camp, ep, turn, t2])
    assert tree.tree_hash != tree2.tree_hash


def test_duplicate_node_identity_rejected():
    camp = _campaign()
    ep = _episode(camp)
    with pytest.raises(ContextLineageValidationError) as exc:
        build_context_lineage_tree(tree_id="DUP", nodes=[camp, ep, ep])
    assert FAILURE_CLASS["DUPLICATE_NODE"] in str(exc.value)


def test_empty_tree_rejected():
    with pytest.raises(ContextLineageValidationError) as exc:
        build_context_lineage_tree(tree_id="EMPTY", nodes=[])
    assert FAILURE_CLASS["EMPTY_TREE"] in str(exc.value)


def test_wrong_parent_level_rejected():
    camp = _campaign()
    # Turn whose parent_ref points directly at campaign (skipping episode)
    parent_ref = ImmutableRef(
        object_id=camp.object_id,
        revision_id=camp.revision_id,
        sha256=camp.revision_hash,
    )
    turn = make_context_node(
        object_id="TURN-SKIP",
        level=ContextLevel.TURN,
        revision_id="r1",
        content_payload={"utterance": "skip"},
        parent_ref=parent_ref,
    )
    with pytest.raises(ContextLineageValidationError) as exc:
        build_context_lineage_tree(tree_id="SKIP", nodes=[camp, turn])
    assert FAILURE_CLASS["LEVEL_VIOLATION"] in str(exc.value)


def test_require_full_hierarchy_on_non_turn_fails():
    camp, ep, _, tree = _full_tree()
    with pytest.raises(ContextLineageValidationError) as exc:
        tree.require_full_hierarchy(ep.object_id)
    assert FAILURE_CLASS["LEVEL_VIOLATION"] in str(exc.value)


def test_frozen_models_reject_mutation():
    camp, _, _, tree = _full_tree()
    with pytest.raises(ValidationError):
        camp.object_id = "mutated"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        tree.tree_id = "mutated"  # type: ignore[misc]


def test_immutable_ref_rejects_bad_sha():
    with pytest.raises((ContextLineageValidationError, ValidationError)):
        ImmutableRef(object_id="x", revision_id="r1", sha256="not-a-hash")
