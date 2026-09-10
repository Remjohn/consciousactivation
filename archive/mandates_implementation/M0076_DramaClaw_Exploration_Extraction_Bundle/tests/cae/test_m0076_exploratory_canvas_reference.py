from pathlib import Path
import importlib.util
import sys
import pytest

MODULE_PATH = Path(__file__).resolve().parents[2] / "docs/cae/CAE_Visual_Production_Exploration_M0076_v1/exploratory_canvas_reference.py"
spec = importlib.util.spec_from_file_location("m0076_exploratory_canvas_reference", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = module
spec.loader.exec_module(module)

AuthorizationError = module.AuthorizationError
ExplorationCanvas = module.ExploratoryCanvas
AgentCanvasCommand = module.AgentCanvasCommand
InvalidPromotionError = module.InvalidPromotionError
LockedNodeError = module.LockedNodeError
StaleRevisionError = module.StaleRevisionError


def cmd(canvas, command_id, operation, payload, approved=True):
    return canvas.apply(AgentCanvasCommand(command_id, "operator-1", operation, payload, canvas.revision, approved))


def test_success_history_group_lock_branch_and_replay():
    canvas = ExplorationCanvas("cx-1", "project-1")
    cmd(canvas, "c1", "create_node", {"node_id": "n1", "kind": "image", "source_refs": ["evidence://seg-1"]})
    receipt = cmd(canvas, "c2", "update_node", {"node_id": "n1", "data": {"caption": "candidate"}})
    assert canvas.nodes["n1"].history[-1].operation == "update_node"
    cmd(canvas, "c3", "group", {"group_id": "g1", "node_ids": ["n1"]})
    cmd(canvas, "c4", "lock", {"node_ids": ["n1"]})
    branch = canvas.branch("b1")
    assert branch.parent_revision == canvas.revision
    assert branch.parent_canvas_id == "cx-1"
    assert receipt.revision_after == 2
    # Deterministic replay returns the original receipt and does not increment revision.
    before = canvas.revision
    replay = canvas.apply(AgentCanvasCommand("c4", "operator-1", "lock", {"node_ids": ["n1"]}, before, True))
    assert replay == canvas.receipts()[3]
    assert canvas.revision == before


def test_good_looking_but_wrong_locked_edit_is_rejected():
    canvas = ExplorationCanvas("cx-2", "project-1")
    cmd(canvas, "c1", "create_node", {"node_id": "n1", "kind": "image", "source_refs": ["evidence://seg-1"]})
    cmd(canvas, "c2", "lock", {"node_ids": ["n1"]})
    before = canvas.revision
    with pytest.raises(LockedNodeError):
        cmd(canvas, "c3", "update_node", {"node_id": "n1", "data": {"caption": "looks better"}})
    assert canvas.revision == before


def test_agent_requires_explicit_operator_approval():
    canvas = ExplorationCanvas("cx-3", "project-1")
    with pytest.raises(AuthorizationError):
        cmd(canvas, "c1", "create_node", {"node_id": "n1", "kind": "text"}, approved=False)
    assert canvas.revision == 0


def test_stale_command_does_not_mutate_exploration():
    canvas = ExplorationCanvas("cx-4", "project-1")
    cmd(canvas, "c1", "create_node", {"node_id": "n1", "kind": "text"})
    before = canvas.revision
    with pytest.raises(StaleRevisionError):
        canvas.apply(AgentCanvasCommand("c2", "operator-1", "create_node", {"node_id": "n2", "kind": "text"}, 0, True))
    assert canvas.revision == before
    assert "n2" not in canvas.nodes


def test_promotion_is_request_only_and_requires_provenance_and_operator_receipt():
    canvas = ExplorationCanvas("cx-5", "project-1")
    cmd(canvas, "c1", "create_node", {"node_id": "n1", "kind": "image", "source_refs": ["evidence://seg-9"]})
    request = canvas.promote_request(
        workspace_id="w1",
        canonical_storyboard_id="story-1",
        candidate_id="cand-1",
        source_node_ids=("n1",),
        operator_receipt_id="receipt-1",
        operator_approved=True,
    )
    assert request.canonical_storyboard_id == "story-1"
    assert request.source_canvas_revision == canvas.revision
    assert request.source_provenance == ("evidence://seg-9",)
    # No canonical CAE object is imported or mutated by the reference component.

    with pytest.raises(InvalidPromotionError):
        canvas.promote_request(
            workspace_id="w1",
            canonical_storyboard_id="story-1",
            candidate_id="cand-1",
            source_node_ids=("n1",),
            operator_receipt_id="",
            operator_approved=True,
        )
