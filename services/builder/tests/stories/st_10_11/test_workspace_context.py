import pytest

from cmf_builder.application.workspace_context import (
    InMemoryWorkspaceContextRepository,
    WorkspaceContext,
    WorkspaceContextError,
    apply_workspace_update,
)


def test_workspace_persists_reloads_and_isolates_operators_deterministically():
    repo = InMemoryWorkspaceContextRepository()
    context = WorkspaceContext("workspace:1", "operator:a", active_run="run:1", logical_views=("runs",), redaction_context=("field:secret:redacted",))
    saved = repo.save(context)
    reloaded = repo.load(operator_identity="operator:a", workspace_identity="workspace:1", known_references={"run:1"})

    assert saved.persistence_revision == 1
    assert reloaded.context_identity == saved.context_identity
    assert "workspace_context_is_not_authority_evidence" in reloaded.limitations

    other = repo.save(WorkspaceContext("workspace:1", "operator:b", active_run="run:2"))
    assert other.operator_identity == "operator:b"
    assert repo.raw_snapshot()["operator:a/workspace:1"]["active_run"] == "run:1"
    assert repo.raw_snapshot()["operator:b/workspace:1"]["active_run"] == "run:2"


def test_workspace_marks_stale_missing_references_without_silently_restoring_active():
    repo = InMemoryWorkspaceContextRepository()
    saved = repo.save(WorkspaceContext("workspace:2", "operator:a", active_run="run:missing"))

    loaded = repo.load(operator_identity="operator:a", workspace_identity="workspace:2", known_references=set())
    assert saved.invalidation_status == "ACTIVE"
    assert loaded.invalidation_status == "STALE"


def test_workspace_rejects_invalidated_saves_redaction_leaks_and_operator_overwrite():
    repo = InMemoryWorkspaceContextRepository()
    context = WorkspaceContext("workspace:3", "operator:a")

    with pytest.raises(WorkspaceContextError) as invalid:
        repo.save(WorkspaceContext("workspace:3", "operator:a", invalidation_status="INVALIDATED"))
    assert invalid.value.code == "INVALIDATED_CONTEXT_CANNOT_SAVE_ACTIVE"

    with pytest.raises(WorkspaceContextError) as redaction:
        WorkspaceContext("workspace:4", "operator:a", redaction_context=("UNREDACTED_SECRET",))
    assert redaction.value.code == "REDACTION_CONTEXT_UNSAFE"

    with pytest.raises(WorkspaceContextError) as isolation:
        apply_workspace_update(context, operator_identity="operator:b")
    assert isolation.value.code == "OPERATOR_CONTEXT_ISOLATION_VIOLATION"
