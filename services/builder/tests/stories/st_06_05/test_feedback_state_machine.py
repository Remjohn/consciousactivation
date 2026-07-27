from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.domain.conversational_feedback import (
    ConversationalFeedbackError,
    FeedbackTransition,
    compile_structural_feedback_chain,
    transition_feedback_chain,
)


def test_request_external_response_is_authority_bound(feedback_source_factory) -> None:
    source = feedback_source_factory("reply_dm")
    chain = compile_structural_feedback_chain(source)
    requested = transition_feedback_chain(
        chain,
        FeedbackTransition(
            event="REQUEST_HUMAN_RESPONSE",
            new_version="1.1.0",
            authority_ref=source.capture_authority_ref,
        ),
    )
    assert requested.state == "AWAITING_EXTERNAL_HUMAN_RESPONSE"
    assert requested.human_response_request.request_status == "EXTERNAL_REQUEST_PENDING"
    assert requested.human_response_request.response_payload_permitted is False


@pytest.mark.parametrize("profile_id", ("reply_dm", "reelcast_expression", "interview_expression"))
def test_external_references_enable_reference_only_recompile_path(
    feedback_source_factory, ref_factory, profile_id
) -> None:
    source = feedback_source_factory(profile_id)
    chain = compile_structural_feedback_chain(source)
    reaction = ref_factory("reaction_receipt")
    expression = (
        ref_factory("expression_moment")
        if profile_id in {"reelcast_expression", "interview_expression"}
        else None
    )
    with_refs = transition_feedback_chain(
        chain,
        FeedbackTransition(
            event="REGISTER_EXTERNAL_REFERENCES",
            new_version="1.1.0",
            authority_ref=source.capture_authority_ref,
            reaction_receipt_ref=reaction,
            expression_moment_ref=expression,
        ),
    )
    eligible = transition_feedback_chain(
        with_refs,
        FeedbackTransition(
            event="MARK_RECOMPILE_ELIGIBLE",
            new_version="1.2.0",
            authority_ref=source.capture_authority_ref,
        ),
    )
    assert eligible.state == "RECOMPILE_ELIGIBLE_REFERENCE_ONLY"
    assert eligible.reaction_receipt.external_ref == reaction
    assert eligible.expression_moment.external_ref == expression


def test_expression_reference_requires_reaction_receipt_provenance(
    feedback_source_factory, ref_factory
) -> None:
    source = feedback_source_factory("reelcast_expression")
    chain = compile_structural_feedback_chain(source)
    with pytest.raises(ConversationalFeedbackError, match="ReactionReceipt"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="REGISTER_EXTERNAL_REFERENCES",
                new_version="1.1.0",
                authority_ref=source.capture_authority_ref,
                expression_moment_ref=ref_factory("expression_moment"),
            ),
        )


def test_withdrawal_revokes_reference_use_and_preserves_history(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    chain = compile_structural_feedback_chain(source)
    withdrawn = transition_feedback_chain(
        chain,
        FeedbackTransition(
            event="WITHDRAW_CONSENT",
            new_version="2.0.0",
            authority_ref=source.source_human_authority_ref,
        ),
    )
    assert withdrawn.state == "WITHDRAWN"
    assert withdrawn.consent_status == "WITHDRAWN"
    assert withdrawn.reference_use_allowed is False
    assert chain.state == "STRUCTURAL_COMPILED"
    with pytest.raises(ConversationalFeedbackError, match="terminal"):
        transition_feedback_chain(
            withdrawn,
            FeedbackTransition(
                event="REQUEST_HUMAN_RESPONSE",
                new_version="2.1.0",
                authority_ref=source.capture_authority_ref,
            ),
        )


@pytest.mark.parametrize(
    ("event", "expected_state"),
    [
        ("INVALIDATE_UPSTREAM", "INVALIDATED"),
        ("CLOSE_WITHOUT_RESPONSE", "CLOSED_NO_RESPONSE"),
    ],
)
def test_invalidation_and_no_response_close_are_terminal(
    feedback_source_factory, event, expected_state
) -> None:
    source = feedback_source_factory("public_comment")
    chain = compile_structural_feedback_chain(source)
    authority = source.capture_authority_ref
    terminal = transition_feedback_chain(
        chain,
        FeedbackTransition(event=event, new_version="2.0.0", authority_ref=authority),
    )
    assert terminal.state == expected_state
    assert terminal.reference_use_allowed is False


def test_invalidation_rejects_role_only_authority_impersonation(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    chain = compile_structural_feedback_chain(source)
    role_only_impostor = replace(
        source.capture_authority_ref,
        object_id="capture-authority-impostor",
        sha256="f" * 64,
    )

    with pytest.raises(ConversationalFeedbackError, match="exact governed chain authority"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="INVALIDATE_UPSTREAM",
                new_version="2.0.0",
                authority_ref=role_only_impostor,
            ),
        )


def test_stale_version_wrong_authority_and_missing_required_refs_fail(
    feedback_source_factory, ref_factory
) -> None:
    source = feedback_source_factory("interview_expression")
    chain = compile_structural_feedback_chain(source)
    with pytest.raises(ConversationalFeedbackError, match="new immutable version"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="REQUEST_HUMAN_RESPONSE",
                new_version=chain.chain_version,
                authority_ref=source.capture_authority_ref,
            ),
        )
    with pytest.raises(ConversationalFeedbackError, match="not attributable"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="REQUEST_HUMAN_RESPONSE",
                new_version="1.1.0",
                authority_ref=source.source_human_authority_ref,
            ),
        )
    with pytest.raises(ConversationalFeedbackError, match="ExpressionMoment"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="REGISTER_EXTERNAL_REFERENCES",
                new_version="1.1.0",
                authority_ref=source.capture_authority_ref,
                reaction_receipt_ref=ref_factory("reaction_receipt"),
            ),
        )


@pytest.mark.parametrize("invalid_version", ("", "  ", "version-one", "01.0.0", "1.0"))
def test_blank_or_invalid_transition_version_identity_fails_closed(
    feedback_source_factory, invalid_version
) -> None:
    source = feedback_source_factory("public_comment")
    chain = compile_structural_feedback_chain(source)
    with pytest.raises(ConversationalFeedbackError, match="immutable semantic version"):
        transition_feedback_chain(
            chain,
            FeedbackTransition(
                event="REQUEST_HUMAN_RESPONSE",
                new_version=invalid_version,
                authority_ref=source.capture_authority_ref,
            ),
        )
