import pytest

from cmf_builder.application.collection_budgets import CollectionBudget, CollectionBudgetError, bounded_graph_traversal, paginate_records


def test_pagination_is_stable_revision_bound_and_non_overlapping():
    budget = CollectionBudget(max_returned_records=5, page_size=2)
    records = [{"identity": f"r{i}", "sort_key": i} for i in range(5)]

    first = paginate_records(records, budget=budget, revision="rev:1")
    second = paginate_records(records, budget=budget, revision="rev:1", cursor=first["next_cursor"])

    assert [item["identity"] for item in first["records"]] == ["r0", "r1"]
    assert [item["identity"] for item in second["records"]] == ["r2", "r3"]
    assert set(item["identity"] for item in first["records"]).isdisjoint(item["identity"] for item in second["records"])
    assert first["partial"] is True
    assert first["production_ready"] is False


def test_budget_rejects_invalid_values_and_invalid_cursors():
    with pytest.raises(CollectionBudgetError) as invalid:
        CollectionBudget(max_returned_records=1, page_size=2)
    assert invalid.value.code == "PAGE_SIZE_EXCEEDS_MAX_RECORDS"

    budget = CollectionBudget(max_returned_records=5, page_size=2)
    page = paginate_records([{"identity": "a", "sort_key": 1}], budget=budget, revision="rev:1")
    assert page["next_cursor"] is None

    first = paginate_records([{"identity": f"r{i}", "sort_key": i} for i in range(3)], budget=budget, revision="rev:1")
    with pytest.raises(CollectionBudgetError) as mismatch:
        paginate_records([], budget=budget, revision="rev:2", cursor=first["next_cursor"])
    assert mismatch.value.code == "REVISION_BOUND_CURSOR_MISMATCH"


def test_graph_traversal_is_bounded_and_labels_partial_result():
    budget = CollectionBudget(graph_nodes=2, graph_edges=1)
    result = bounded_graph_traversal(["b", "a", "c"], [("a", "b"), ("b", "c"), ("a", "c")], budget=budget)

    assert result["nodes"] == ["a", "b"]
    assert result["edges"] == [("a", "b")]
    assert result["partial"] is True
    assert result["budget_exceeded"] is True
