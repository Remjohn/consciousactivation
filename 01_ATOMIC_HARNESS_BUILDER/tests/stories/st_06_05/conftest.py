from __future__ import annotations

from hashlib import sha256

import pytest

from cmf_builder.domain.category_runtime_rules import (
    CategoryPolicyInput,
    compile_category_operating_rules,
)
from cmf_builder.domain.category_syntax import (
    CATEGORY_CONSTITUTION_VERSION,
    GRAMMAR_FAMILIES,
    CategorySyntaxInput,
    GovernedRef,
    compile_category_native_syntax,
)
from cmf_builder.domain.conversational_feedback import ConversationalFeedbackInput


def make_ref(
    role: str,
    *,
    suffix: str = "v1",
    status: str = "ACTIVE",
    authority: str = "governed-test-authority",
) -> GovernedRef:
    return GovernedRef(
        object_id=f"{role}-{suffix}",
        version="1.0.0",
        sha256=sha256(f"{role}:{suffix}".encode()).hexdigest(),
        authority=authority,
        lineage_role=role,
        status=status,
    )


def make_policy(profile_id: str = "public_comment"):
    rich_roles = (
        "source_premise",
        "identity_dna",
        "context_premise",
        "resonance_map",
        "matrix_of_edging",
        "activative_intelligence_pack",
        "evaluation_contract",
    )
    syntax_input = CategorySyntaxInput(
        harness_id=f"harness-{profile_id}",
        harness_version="1.0.0",
        mode="activative",
        category_id="conversational_activation_expression",
        profile_id=profile_id,
        category_constitution_version=CATEGORY_CONSTITUTION_VERSION,
        requested_grammar_family=GRAMMAR_FAMILIES[
            "conversational_activation_expression"
        ],
        category_binding_ref=make_ref("category_binding"),
        structural_profile_ref=make_ref("structural_profile"),
        shared_activative_core_ref=make_ref("shared_activative_core"),
        evidence_refs=(make_ref("syntax_evidence"),),
        rich_source_object_refs=tuple(make_ref(role) for role in rich_roles),
        authority_refs=(make_ref("constitutional_authority"),),
        wrong_reading_locks=("never invent human truth", "preserve source authority"),
        activation_direction="invite owned response",
        participant_role="source human",
        states=("CALL_READY", "HUMAN_RESPONSE_EXTERNAL"),
        transitions=("CALL_READY->HUMAN_RESPONSE_EXTERNAL",),
        pacing="adaptive external conversation",
        sonic_or_silence_function="NOT_APPLICABLE_CONVERSATIONAL",
        payoff="human-owned next step",
        intended_reaction="desired recognition only not actual reaction",
        micro_commitment="name one owned next step",
    )
    syntax, sequence = compile_category_native_syntax(syntax_input)
    return compile_category_operating_rules(
        CategoryPolicyInput(
            ruleset_name=f"rules-{profile_id}",
            ruleset_version="1.0.0",
            syntax=syntax,
            sequence=sequence,
            evaluator_owner_ref=make_ref("evaluation_owner"),
            repair_owner_ref=make_ref("repair_owner"),
            migration_authority_ref=make_ref("migration_authority"),
            compatibility_authority_ref=make_ref("compatibility_authority"),
        )
    )


def make_feedback_source(profile_id: str = "public_comment") -> ConversationalFeedbackInput:
    return ConversationalFeedbackInput(
        chain_id=f"feedback-{profile_id}",
        chain_version="1.0.0",
        category_policy=make_policy(profile_id),
        activative_pack_ref=make_ref("activative_intelligence_pack"),
        consent_policy_ref=make_ref("consent_policy"),
        source_human_authority_ref=make_ref(
            "source_human_authority", authority="feedback-human"
        ),
        capture_authority_ref=make_ref("capture_authority", authority="feedback-code"),
        call_constraints=(
            "do not supply the human answer",
            "stop before external runtime execution",
        ),
        desired_human_role="source human with authority over original truth",
        desired_reaction="desired recognition without asserted actual reaction",
        micro_commitment="offer one self-owned next step",
        wrong_reading_locks=(
            "do not invent a human reaction",
            "do not issue evidence locally",
        ),
    )


@pytest.fixture
def feedback_source_factory():
    return make_feedback_source


@pytest.fixture
def ref_factory():
    return make_ref
