from __future__ import annotations

import pytest
from pydantic import ValidationError

from api.services.visual_chat import (
    VisualChatAction,
    VisualChatProposalStatus,
    VisualChatRequest,
    VisualChatValidationError,
    classify_visual_chat_request,
    compile_visual_chat,
)

ACTOR = {"actor_id": "operator:test", "actor_type": "human", "product_id": "cae", "workflow_role": "operator"}
TARGET = {"object_id": "layer:1", "version": "1", "sha256": "a" * 64}
CANONICAL = {"object_id": "revision:1", "version": "4", "sha256": "b" * 64}


def request(text: str, *, action: VisualChatAction | None = None, candidates: tuple[dict[str, str], ...] = ()) -> VisualChatRequest:
    return VisualChatRequest(
        natural_language_request=text,
        target_ref=TARGET,
        target_node_id="layer:1",
        operator_actor=ACTOR,
        expected_state_version=4,
        action=action,
        candidate_refs=candidates,
        canonical_revision_ref=CANONICAL,
    )


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("find alternatives for this source", VisualChatAction.FIND_ALTERNATIVES),
        ("replace source with another governed candidate", VisualChatAction.REPLACE_SOURCE),
        ("regenerate the BBOX prompt", VisualChatAction.REGENERATE_BBOX_PROMPT),
        ("make the composition alternatives", VisualChatAction.COMPOSITION_ALTERNATIVES),
        ("reduce visual intensity", VisualChatAction.REDUCE_INTENSITY),
        ("move emphasis to the subject", VisualChatAction.MOVE_EMPHASIS),
    ],
)
def test_classifier_is_closed_and_deterministic(text: str, expected: VisualChatAction) -> None:
    assert classify_visual_chat_request(text) == expected


def test_replace_source_without_governed_candidates_is_held() -> None:
    proposal = compile_visual_chat(request("replace source", action=VisualChatAction.REPLACE_SOURCE), canonical_revision_ref=CANONICAL, current_state_version=4)
    assert proposal.status == VisualChatProposalStatus.NEEDS_CANDIDATES
    assert proposal.candidate_refs == ()
    assert proposal.canonical_state_mutated is False
    assert proposal.requires_operator_authorization is True


def test_composition_alternatives_are_three_immutable_proposals_without_state_mutation() -> None:
    proposal = compile_visual_chat(request("show composition alternatives", action=VisualChatAction.COMPOSITION_ALTERNATIVES), canonical_revision_ref=CANONICAL, current_state_version=4)
    assert len(proposal.exact_operations) == 3
    assert proposal.proposal_id.startswith("visual-chat:")
    assert proposal.canonical_state_mutated is False


def test_preserve_evidence_is_a_contrastive_lock_against_source_swap() -> None:
    proposal = compile_visual_chat(request("keep the source evidence", action=VisualChatAction.PRESERVE_EVIDENCE), canonical_revision_ref=CANONICAL, current_state_version=4)
    assert proposal.evidence_preserved is True
    assert all("replace" not in operation.expected_effect.lower() for operation in proposal.exact_operations)


def test_auth_digest_and_replay_fail_closed() -> None:
    with pytest.raises(ValidationError):
        VisualChatRequest(
            natural_language_request="explain this",
            target_ref=TARGET,
            target_node_id="layer:1",
            operator_actor={"actor_type": "model"},
            expected_state_version=4,
        )
    first = compile_visual_chat(request("explain this"), canonical_revision_ref=CANONICAL, current_state_version=4)
    second = compile_visual_chat(request("explain this"), canonical_revision_ref=CANONICAL, current_state_version=4)
    assert first.model_dump(mode="json") == second.model_dump(mode="json")
    with pytest.raises(VisualChatValidationError, match="digest"):
        compile_visual_chat(request("explain this"), canonical_revision_ref={"object_id": "revision:2", "version": "4", "sha256": "c" * 64}, current_state_version=4)
    with pytest.raises(VisualChatValidationError, match="stale"):
        compile_visual_chat(request("explain this"), canonical_revision_ref=CANONICAL, current_state_version=5)
