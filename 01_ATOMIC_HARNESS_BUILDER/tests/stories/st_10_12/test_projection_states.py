import pytest

from cmf_builder.application.projection_states import ProjectionState, ProjectionStateClass, ProjectionStateError, summarize_projection_states


def test_projection_states_are_distinct_and_deterministic():
    ready = ProjectionState("run:1", ProjectionStateClass.READY, "index", "rev:1", "rev:1", "CURRENT", "ready", False, False, ("not production",), "receipt:1")
    empty = ProjectionState("run:none", ProjectionStateClass.EMPTY, "index", "rev:1", "rev:1", "NO_RECORDS", "no records", False, False, ("empty is not failure",))
    summary = summarize_projection_states((empty, ready))

    assert summary["states"][0]["subject_identity"] == "run:1"
    assert summary["states"][1]["state_class"] == "EMPTY"
    assert summary["production_ready"] is False
    assert summary["certified"] is False
    assert ready.state_identity == ProjectionState("run:1", ProjectionStateClass.READY, "index", "rev:1", "rev:1", "CURRENT", "ready", False, False, ("not production",), "receipt:1").state_identity


def test_state_semantics_reject_flattening_and_fabrication():
    with pytest.raises(ProjectionStateError) as empty:
        ProjectionState("subject", ProjectionStateClass.EMPTY, "source", "rev:1", "rev:1", "FAILURE", "failed", False, False, ())
    assert empty.value.code == "EMPTY_STATE_MISREPRESENTED_AS_FAILURE"

    with pytest.raises(ProjectionStateError) as stale:
        ProjectionState("subject", ProjectionStateClass.STALE, "source", "rev:1", "rev:1", "REVISION_DRIFT", "stale", True, True, ())
    assert stale.value.code == "STALE_REQUIRES_REVISION_DRIFT"

    with pytest.raises(ProjectionStateError) as loading:
        ProjectionState("subject", ProjectionStateClass.LOADING, "source", "NONE", "rev:1", "FETCHING", "loading", True, False, (), last_known_payload_identity="payload")
    assert loading.value.code == "LOADING_FABRICATED_PARTIAL_RESULT"

    with pytest.raises(ProjectionStateError) as unavailable:
        ProjectionState("subject", ProjectionStateClass.UNAVAILABLE, "source", "NONE", "rev:1", "NO_AUTHORITY", "unavailable", False, False, ("cached_authority",))
    assert unavailable.value.code == "UNAVAILABLE_FABRICATED_CACHED_AUTHORITY"
