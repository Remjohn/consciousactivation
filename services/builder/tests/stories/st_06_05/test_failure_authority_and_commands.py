from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.conversational_commands import (
    CompileConversationalFeedbackCommand,
    ConversationalCommandRejected,
    ConversationalFeedbackService,
    InMemoryConversationalFeedbackRepository,
    InMemoryConversationalObservationSink,
    TransitionConversationalFeedbackCommand,
)
from cmf_builder.domain.conversational_feedback import (
    ConversationalFeedbackError,
    compile_structural_feedback_chain,
)


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def _service():
    authority = AuthorityService(
        actors=(
            Actor("feedback-code", ActorKind.CODE),
            Actor("feedback-human", ActorKind.HUMAN),
            Actor("other-code", ActorKind.CODE),
            Actor("external", ActorKind.EXTERNAL),
        ),
        grants=(
            AuthorityGrant(
                "feedback-code",
                frozenset({Action.COMPILE_CONVERSATIONAL_FEEDBACK}),
                "*",
                NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                "feedback-human",
                frozenset({Action.WITHDRAW_CONVERSATIONAL_FEEDBACK_CONSENT}),
                "*",
                NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                "other-code",
                frozenset({Action.COMPILE_CONVERSATIONAL_FEEDBACK}),
                "*",
                NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                "external",
                frozenset({Action.COMPILE_CONVERSATIONAL_FEEDBACK}),
                "*",
                NOW + timedelta(days=1),
            ),
        ),
    )
    repository = InMemoryConversationalFeedbackRepository()
    observations = InMemoryConversationalObservationSink()
    return ConversationalFeedbackService(authority, repository, observations), repository, observations


def _compile_command(source, command_id="feedback-1", actor_id="feedback-code"):
    return CompileConversationalFeedbackCommand(
        command_id=command_id,
        source=source,
        actor_id=actor_id,
        now=NOW,
        correlation_id="corr-st0605",
        causation_id="ST-06.04",
    )


def test_missing_policy_authority_scripted_landing_and_identity_approval_fail(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    with pytest.raises(ConversationalFeedbackError, match="consent_policy"):
        compile_structural_feedback_chain(
            replace(source, consent_policy_ref=replace(source.consent_policy_ref, lineage_role="other"))
        )
    with pytest.raises(ConversationalFeedbackError, match="scripted"):
        compile_structural_feedback_chain(
            replace(source, scripted_human_landing="the guest realizes the answer")
        )
    with pytest.raises(ConversationalFeedbackError, match="Identity DNA"):
        compile_structural_feedback_chain(
            replace(source, identity_dna_approval_requested=True)
        )


def test_missing_locks_and_readiness_claims_fail_closed(feedback_source_factory) -> None:
    source = feedback_source_factory("reply_dm")
    with pytest.raises(ConversationalFeedbackError, match="wrong_reading_locks"):
        compile_structural_feedback_chain(replace(source, wrong_reading_locks=()))
    with pytest.raises(ConversationalFeedbackError, match="production or certification"):
        compile_structural_feedback_chain(replace(source, certified=True))


@pytest.mark.parametrize("invalid_version", ("", "  ", "version-one", "01.0.0", "1.0"))
def test_blank_or_invalid_initial_version_identity_fails_closed(
    feedback_source_factory, invalid_version
) -> None:
    source = replace(
        feedback_source_factory("public_comment"), chain_version=invalid_version
    )
    with pytest.raises(ConversationalFeedbackError, match="immutable semantic version"):
        compile_structural_feedback_chain(source)


def test_compile_replay_resume_transition_and_historical_reproduction(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    service, repository, observations = _service()
    command = _compile_command(source)
    first = service.compile(command)
    second = service.compile(command)
    assert first == second
    original = service.resume(source.chain_id)
    transition = TransitionConversationalFeedbackCommand(
        command_id="feedback-transition-1",
        chain_id=source.chain_id,
        expected_parent_hash=original.chain_hash,
        event="REQUEST_HUMAN_RESPONSE",
        new_version="1.1.0",
        authority_ref=source.capture_authority_ref,
        actor_id="feedback-code",
        now=NOW,
        correlation_id="corr-st0605",
        causation_id=first.receipt_id,
    )
    transition_first = service.transition(transition)
    transition_second = service.transition(transition)
    assert transition_first == transition_second
    assert service.resume(source.chain_id).state == "AWAITING_EXTERNAL_HUMAN_RESPONSE"
    assert repository.historical_chain(source.chain_id, "1.0.0") == original
    assert repository.chain_version_count == 2
    assert [item.event_name for item in observations.items] == [
        "ST-06.05:FeedbackChainCompiled",
        "ST-06.05:FeedbackChainReplayReturned",
        "ST-06.05:FeedbackTransitionCommitted",
        "ST-06.05:FeedbackTransitionReplayReturned",
    ]


def test_command_conflict_unauthorized_actor_stale_parent_and_atomic_failure(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("reply_dm")
    service, repository, observations = _service()
    service.compile(_compile_command(source))
    with pytest.raises(ConversationalCommandRejected, match="different payload"):
        service.compile(_compile_command(replace(source, chain_version="2.0.0")))
    with pytest.raises(ConversationalCommandRejected, match="actor"):
        service.compile(_compile_command(source, "feedback-2", "external"))
    with pytest.raises(ConversationalCommandRejected, match="stale"):
        service.transition(
            TransitionConversationalFeedbackCommand(
                command_id="stale-transition",
                chain_id=source.chain_id,
                expected_parent_hash="sha256:" + "0" * 64,
                event="REQUEST_HUMAN_RESPONSE",
                new_version="1.1.0",
                authority_ref=source.capture_authority_ref,
                actor_id="feedback-code",
                now=NOW,
                correlation_id="corr",
                causation_id="cause",
            )
        )
    assert observations.items[-1].event_name == "ST-06.05:FeedbackTransitionRejected"
    assert observations.items[-1].outcome == "FAIL"
    assert "stale" in (observations.items[-1].failure_context or "")

    fresh, fresh_repository, fresh_observations = _service()
    fresh_repository.inject_failure_before_commit()
    with pytest.raises(ConversationalCommandRejected, match="Injected"):
        fresh.compile(_compile_command(source))
    assert fresh_repository.chain_version_count == 0
    assert fresh_repository.receipt_count == 0
    assert fresh_repository.command_count == 0
    assert fresh_observations.items[-1].outcome == "FAIL"


def test_transition_replay_conflict_emits_typed_rejection_observation(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    service, _, observations = _service()
    service.compile(_compile_command(source))
    active = service.resume(source.chain_id)
    command = TransitionConversationalFeedbackCommand(
        command_id="transition-replay-conflict",
        chain_id=source.chain_id,
        expected_parent_hash=active.chain_hash,
        event="REQUEST_HUMAN_RESPONSE",
        new_version="1.1.0",
        authority_ref=source.capture_authority_ref,
        actor_id="feedback-code",
        now=NOW,
        correlation_id="corr",
        causation_id="cause",
    )
    service.transition(command)

    with pytest.raises(ConversationalCommandRejected, match="different payload"):
        service.transition(replace(command, reason="conflicting governed reason"))

    rejected = observations.items[-1]
    assert rejected.event_name == "ST-06.05:FeedbackTransitionRejected"
    assert rejected.outcome == "FAIL"
    assert "different payload" in (rejected.failure_context or "")


def test_transition_actor_must_match_exact_authority_evidence(
    feedback_source_factory,
) -> None:
    source = replace(
        feedback_source_factory("public_comment"),
        capture_authority_ref=replace(
            feedback_source_factory("public_comment").capture_authority_ref,
            authority="other-code",
        ),
    )
    service, _, observations = _service()
    service.compile(_compile_command(source))
    active = service.resume(source.chain_id)

    with pytest.raises(ConversationalCommandRejected, match="acting actor"):
        service.transition(
            TransitionConversationalFeedbackCommand(
                command_id="actor-authority-mismatch",
                chain_id=source.chain_id,
                expected_parent_hash=active.chain_hash,
                event="REQUEST_HUMAN_RESPONSE",
                new_version="1.1.0",
                authority_ref=source.capture_authority_ref,
                actor_id="feedback-code",
                now=NOW,
                correlation_id="corr",
                causation_id="cause",
            )
        )
    assert observations.items[-1].event_name == "ST-06.05:FeedbackTransitionRejected"

    invalid_authority_ref = replace(
        source.capture_authority_ref, authority="feedback-code", sha256="not-a-sha256"
    )
    with pytest.raises(ConversationalCommandRejected, match="evidence is invalid"):
        service.transition(
            TransitionConversationalFeedbackCommand(
                command_id="invalid-transition-authority-evidence",
                chain_id=source.chain_id,
                expected_parent_hash=active.chain_hash,
                event="REQUEST_HUMAN_RESPONSE",
                new_version="1.1.0",
                authority_ref=invalid_authority_ref,
                actor_id="feedback-code",
                now=NOW,
                correlation_id="corr",
                causation_id="cause",
            )
        )
    assert observations.items[-1].event_name == "ST-06.05:FeedbackTransitionRejected"


def test_withdrawal_requires_exact_human_actor_and_human_only_action(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    service, _, observations = _service()
    service.compile(_compile_command(source))
    active = service.resume(source.chain_id)
    command = TransitionConversationalFeedbackCommand(
        command_id="withdraw-human-only",
        chain_id=source.chain_id,
        expected_parent_hash=active.chain_hash,
        event="WITHDRAW_CONSENT",
        new_version="2.0.0",
        authority_ref=source.source_human_authority_ref,
        actor_id="feedback-code",
        now=NOW,
        correlation_id="corr",
        causation_id="cause",
    )

    with pytest.raises(ConversationalCommandRejected, match="human"):
        service.transition(command)
    assert observations.items[-1].event_name == "ST-06.05:FeedbackTransitionRejected"

    receipt = service.transition(
        replace(command, command_id="withdraw-human-authorized", actor_id="feedback-human")
    )
    assert receipt.state == "WITHDRAWN"
