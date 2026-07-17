from __future__ import annotations

from dataclasses import fields

import pytest

from cmf_builder.domain.conversational_feedback import (
    FEEDBACK_MATURITY,
    PROFILE_APPLICABILITY,
    ConversationalFeedbackInput,
    compile_structural_feedback_chain,
)


@pytest.mark.parametrize("profile_id", tuple(PROFILE_APPLICABILITY))
def test_all_four_profiles_compile_as_structural_external_feedback_contracts(
    feedback_source_factory, profile_id
) -> None:
    chain = compile_structural_feedback_chain(feedback_source_factory(profile_id))
    expected_reaction, expected_expression = PROFILE_APPLICABILITY[profile_id]
    assert chain.profile_id == profile_id
    assert chain.category_id == "conversational_activation_expression"
    assert chain.reaction_receipt.applicability == expected_reaction
    assert chain.expression_moment.applicability == expected_expression
    assert chain.reaction_receipt.issuance_owner == "EXTERNAL_HUMAN_CAPTURE_AUTHORITY"
    assert chain.expression_moment.issuance_owner == "EXTERNAL_HUMAN_CAPTURE_AUTHORITY"
    assert chain.maturity_status == FEEDBACK_MATURITY
    assert chain.production_ready is False
    assert chain.certified is False


def test_activative_call_preserves_desired_not_actual_human_semantics(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("reply_dm")
    chain = compile_structural_feedback_chain(source)
    call = chain.activative_call
    assert call.desired_human_role == source.desired_human_role
    assert call.desired_reaction == source.desired_reaction
    assert call.micro_commitment == source.micro_commitment
    assert call.execution_owner == "EXTERNAL_CONVERSATIONAL_HARNESS"
    assert not hasattr(call, "actual_reaction")
    assert not hasattr(call, "human_landing")


def test_human_response_request_is_attributable_and_payload_free(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("public_comment")
    chain = compile_structural_feedback_chain(source)
    request = chain.human_response_request
    assert request.source_human_authority_ref == source.source_human_authority_ref
    assert request.capture_authority_ref == source.capture_authority_ref
    assert request.consent_policy_ref == source.consent_policy_ref
    assert request.response_payload_permitted is False
    assert request.request_status == "STRUCTURAL_REQUEST_NOT_SENT"
    input_fields = {field.name for field in fields(ConversationalFeedbackInput)}
    assert "actual_human_response" not in input_fields
    assert "reaction_text" not in input_fields
    assert "expression_spans" not in input_fields


def test_wrong_reading_locks_and_complete_reference_lineage_are_preserved(
    feedback_source_factory,
) -> None:
    source = feedback_source_factory("reelcast_expression")
    chain = compile_structural_feedback_chain(source)
    assert chain.wrong_reading_locks == tuple(sorted(source.wrong_reading_locks))
    roles = {ref.lineage_role for ref in chain.semantic_lineage}
    assert roles == {
        "activative_intelligence_pack",
        "consent_policy",
        "source_human_authority",
        "capture_authority",
    }
    assert "HD-006:HUMAN_POLICY_PENDING" in chain.human_policy_gate


def test_identical_inputs_are_byte_identical(feedback_source_factory) -> None:
    source = feedback_source_factory("interview_expression")
    first = compile_structural_feedback_chain(source)
    second = compile_structural_feedback_chain(source)
    assert first.canonical_bytes == second.canonical_bytes
    assert first.chain_hash == second.chain_hash
