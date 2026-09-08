"""
Acceptance and integration tests for CA-M006 — Activative to Elicitation Linking.

The suite proves:
- one Activative can support many Elicitation Steps;
- one Elicitation Step can be supported by many Activatives;
- true many-to-many edges are queryable in both directions;
- trace hashes are deterministic and detect tampering;
- missing parents, duplicate edges, revision conflicts, and cross-workspace
  relationships fail closed;
- an unauthorized or untraced elicitation branch cannot become planning input;
- the relationship persists across a SQLite connection reload;
- the interview-planning projection consumes governed edges rather than labels.
"""

from __future__ import annotations

import sqlite3

import pytest

from ca_runtime.activative_elicitation_link import (
    ActivativeElicitationLink,
    ActivativeElicitationLinkRegistry,
    ActivativeTrigger,
    CrossWorkspaceLinkError,
    DuplicateLinkError,
    ElicitationStep,
    MissingParentError,
    RevisionConflictError,
    InvalidLinkError,
    TraceIntegrityError,
    UnauthorizedOriginError,
)


@pytest.fixture
def db() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def registry(db: sqlite3.Connection) -> ActivativeElicitationLinkRegistry:
    return ActivativeElicitationLinkRegistry(db)


def activative(
    ident: str,
    *,
    workspace: str = "ws-ca-m006",
    revision: int = 1,
    trigger: str | None = None,
    authorized: bool = True,
) -> ActivativeTrigger:
    return ActivativeTrigger.create(
        workspace_id=workspace,
        activative_id=ident,
        activative_revision=revision,
        trigger_id=trigger or f"{ident}-trigger",
        authority_ref=f"operator:{ident}",
        authorized=authorized,
    )


def step(
    ident: str,
    *,
    workspace: str = "ws-ca-m006",
    elicitation: str = "ELC-001",
    revision: int = 1,
    branch: str = "BRANCH-A",
    sequence: int = 0,
) -> ElicitationStep:
    return ElicitationStep.create(
        workspace_id=workspace,
        elicitation_id=elicitation,
        elicitation_revision=revision,
        step_id=ident,
        branch_id=branch,
        sequence=sequence,
        objective=f"Recover evidence for {ident}",
    )


def test_ca_m006_one_activative_to_many_steps(registry: ActivativeElicitationLinkRegistry) -> None:
    origin = activative("ACT-001")
    first = step("STEP-001", sequence=0)
    second = step("STEP-002", sequence=1)

    registry.register_activative(origin)
    registry.register_elicitation_step(first)
    registry.register_elicitation_step(second)
    registry.link(activative=origin, step=first)
    registry.link(activative=origin, step=second, role="FOLLOW_UP")

    linked = registry.resolve_activative(
        workspace_id=origin.workspace_id,
        activative_id=origin.activative_id,
        activative_revision=origin.activative_revision,
    )

    assert [item.step.step_id for item in linked] == ["STEP-001", "STEP-002"]
    assert [item.link.role for item in linked] == ["PRIMARY", "FOLLOW_UP"]


def test_ca_m006_many_activatives_to_one_step(registry: ActivativeElicitationLinkRegistry) -> None:
    first = activative("ACT-001")
    second = activative("ACT-002", trigger="ACT-002-trigger")
    target = step("STEP-SHARED")

    for origin in (first, second):
        registry.register_activative(origin)
    registry.register_elicitation_step(target)
    registry.link(activative=first, step=target)
    registry.link(activative=second, step=target, role="SUPPORTING")

    linked = registry.resolve_elicitation_branch(
        workspace_id=target.workspace_id,
        elicitation_id=target.elicitation_id,
        elicitation_revision=target.elicitation_revision,
        branch_id=target.branch_id,
    )

    assert [item.origin.activative_id for item in linked] == ["ACT-001", "ACT-002"]
    assert len({item.link.trace_hash for item in linked}) == 2


def test_ca_m006_true_many_to_many_is_queryable_both_directions(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    origins = [activative("ACT-A"), activative("ACT-B")]
    steps = [
        step("STEP-1", elicitation="ELC-001", branch="BRANCH-1", sequence=0),
        step("STEP-2", elicitation="ELC-001", branch="BRANCH-1", sequence=1),
    ]

    for origin in origins:
        registry.register_activative(origin)
    for target in steps:
        registry.register_elicitation_step(target)

    for origin in origins:
        for target in steps:
            registry.link(activative=origin, step=target)

    from_a = registry.resolve_activative(
        workspace_id="ws-ca-m006",
        activative_id="ACT-A",
        activative_revision=1,
    )
    branch = registry.resolve_elicitation_branch(
        workspace_id="ws-ca-m006",
        elicitation_id="ELC-001",
        elicitation_revision=1,
        branch_id="BRANCH-1",
    )

    assert [(x.step.step_id, x.link.role) for x in from_a] == [
        ("STEP-1", "PRIMARY"),
        ("STEP-2", "PRIMARY"),
    ]
    assert [(x.step.step_id, x.origin.activative_id) for x in branch] == [
        ("STEP-1", "ACT-A"),
        ("STEP-1", "ACT-B"),
        ("STEP-2", "ACT-A"),
        ("STEP-2", "ACT-B"),
    ]
    assert len(registry.list_links(workspace_id="ws-ca-m006")) == 4


def test_ca_m006_trace_hash_is_deterministic() -> None:
    origin = activative("ACT-001")
    target = step("STEP-001")

    first = ActivativeElicitationLink.create(activative=origin, step=target, role="PRIMARY")
    second = ActivativeElicitationLink.create(activative=origin, step=target, role="PRIMARY")

    assert first.trace_hash == second.trace_hash
    assert len(first.trace_hash) == 64


def test_ca_m006_revision_change_changes_trace_hash() -> None:
    origin_v1 = activative("ACT-001", revision=1)
    origin_v2 = activative("ACT-001", revision=2)
    target = step("STEP-001")

    first = ActivativeElicitationLink.create(activative=origin_v1, step=target)
    second = ActivativeElicitationLink.create(activative=origin_v2, step=target)

    assert origin_v1.canonical_sha256 != origin_v2.canonical_sha256
    assert first.trace_hash != second.trace_hash


def test_ca_m006_missing_parent_is_rejected(registry: ActivativeElicitationLinkRegistry) -> None:
    origin = activative("ACT-001")
    target = step("STEP-001")
    registry.register_activative(origin)

    with pytest.raises(MissingParentError):
        registry.link(activative=origin, step=target)


def test_ca_m006_duplicate_edge_is_rejected(registry: ActivativeElicitationLinkRegistry) -> None:
    origin = activative("ACT-001")
    target = step("STEP-001")
    registry.register_activative(origin)
    registry.register_elicitation_step(target)
    registry.link(activative=origin, step=target)

    with pytest.raises(DuplicateLinkError):
        registry.link(activative=origin, step=target)


def test_ca_m006_revision_reuse_with_different_bytes_is_rejected(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    origin_v1 = activative("ACT-001", revision=1)
    registry.register_activative(origin_v1)

    changed_same_revision = ActivativeTrigger.create(
        workspace_id=origin_v1.workspace_id,
        activative_id=origin_v1.activative_id,
        activative_revision=1,
        trigger_id=origin_v1.trigger_id,
        authority_ref="operator:changed",
    )

    with pytest.raises(RevisionConflictError):
        registry.register_activative(changed_same_revision)


def test_ca_m006_invalid_revision_is_rejected() -> None:
    with pytest.raises(InvalidLinkError):
        ActivativeTrigger.create(
            workspace_id="ws-ca-m006",
            activative_id="ACT-001",
            activative_revision=0,
            trigger_id="TRG-001",
            authority_ref="operator:test",
        )


def test_ca_m006_cross_workspace_link_is_rejected(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    origin = activative("ACT-001", workspace="ws-A")
    target = step("STEP-001", workspace="ws-B")

    registry.register_activative(origin)
    registry.register_elicitation_step(target)

    with pytest.raises(CrossWorkspaceLinkError):
        registry.link(activative=origin, step=target)


def test_ca_m006_unauthorized_activative_cannot_origin_link(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    origin = activative("ACT-001", authorized=False)
    target = step("STEP-001")
    registry.register_activative(origin)
    registry.register_elicitation_step(target)

    with pytest.raises(UnauthorizedOriginError):
        registry.link(activative=origin, step=target)


def test_ca_m006_untraced_branch_fails_closed(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    target = step("STEP-ORPHAN", branch="BRANCH-ORPHAN")
    registry.register_elicitation_step(target)

    with pytest.raises(UnauthorizedOriginError, match="cannot be traced"):
        registry.resolve_elicitation_branch(
            workspace_id=target.workspace_id,
            elicitation_id=target.elicitation_id,
            elicitation_revision=target.elicitation_revision,
            branch_id=target.branch_id,
        )


def test_ca_m006_tampered_trace_hash_fails_closed(
    registry: ActivativeElicitationLinkRegistry,
    db: sqlite3.Connection,
) -> None:
    origin = activative("ACT-001")
    target = step("STEP-001")
    registry.register_activative(origin)
    registry.register_elicitation_step(target)
    edge = registry.link(activative=origin, step=target)

    db.execute(
        """
        UPDATE ca_m006_links
        SET trace_hash = ?
        WHERE workspace_id = ?
          AND activative_id = ?
          AND activative_revision = ?
          AND trigger_id = ?
          AND elicitation_id = ?
          AND elicitation_revision = ?
          AND step_id = ?
        """,
        (
            "0" * 64,
            edge.workspace_id,
            edge.activative_id,
            edge.activative_revision,
            edge.trigger_id,
            edge.elicitation_id,
            edge.elicitation_revision,
            edge.step_id,
        ),
    )
    db.commit()

    with pytest.raises(TraceIntegrityError):
        registry.resolve_elicitation_branch(
            workspace_id=target.workspace_id,
            elicitation_id=target.elicitation_id,
            elicitation_revision=target.elicitation_revision,
            branch_id=target.branch_id,
        )


def test_ca_m006_branch_projection_is_structured_and_authoritative(
    registry: ActivativeElicitationLinkRegistry,
) -> None:
    origin = activative("ACT-001")
    target = step("STEP-001")
    registry.register_activative(origin)
    registry.register_elicitation_step(target)
    edge = registry.link(activative=origin, step=target)

    plan = registry.build_interview_planning_input(
        workspace_id=target.workspace_id,
        elicitation_id=target.elicitation_id,
        elicitation_revision=target.elicitation_revision,
        branch_id=target.branch_id,
    )

    assert plan == (
        {
            "workspace_id": target.workspace_id,
            "activative": {
                "id": origin.activative_id,
                "revision": origin.activative_revision,
                "trigger_id": origin.trigger_id,
                "authority_ref": origin.authority_ref,
                "canonical_sha256": origin.canonical_sha256,
            },
            "elicitation": {
                "id": target.elicitation_id,
                "revision": target.elicitation_revision,
                "step_id": target.step_id,
                "branch_id": target.branch_id,
                "sequence": target.sequence,
                "objective": target.objective,
                "canonical_sha256": target.canonical_sha256,
            },
            "relationship": {
                "role": edge.role,
                "trace_hash": edge.trace_hash,
            },
        },
    )


def test_ca_m006_persists_and_reloads_edges_from_sqlite(tmp_path) -> None:
    db_path = tmp_path / "ca-m006.sqlite"
    origin = activative("ACT-001")
    target = step("STEP-001")

    connection_one = sqlite3.connect(db_path)
    try:
        registry_one = ActivativeElicitationLinkRegistry(connection_one)
        registry_one.register_activative(origin)
        registry_one.register_elicitation_step(target)
        created = registry_one.link(activative=origin, step=target)
    finally:
        connection_one.close()

    connection_two = sqlite3.connect(db_path)
    try:
        registry_two = ActivativeElicitationLinkRegistry(connection_two)
        resolved = registry_two.resolve_elicitation_branch(
            workspace_id=target.workspace_id,
            elicitation_id=target.elicitation_id,
            elicitation_revision=target.elicitation_revision,
            branch_id=target.branch_id,
        )
    finally:
        connection_two.close()

    assert len(resolved) == 1
    assert resolved[0].link == created
    assert resolved[0].origin == origin
    assert resolved[0].step == target
