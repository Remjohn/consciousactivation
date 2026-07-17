import pytest

from cmf_builder.application.genesis_review import (
    DecisionClass,
    DecisionStatus,
    GenesisDecision,
    GenesisReviewError,
    OwnerType,
    ReviewDisposition,
    filter_decisions,
    review_genesis_decision,
)


def decision(**overrides):
    values = {
        "decision_identity": "decision:bd004-admission",
        "decision_class": DecisionClass.EVIDENCE_ADMISSION,
        "subject_identity": "archive:bd004",
        "originating_context": "OD-AM evidence branch",
        "decision_owner": "emilio-conscious-elite-internal-dev",
        "owner_type": OwnerType.GOVERNED_OPERATOR,
        "authority_basis": "bounded internal development authority",
        "effective_date": "2026-07-17",
        "status": DecisionStatus.ACTIVE,
        "decision_statement": "admit bounded development evidence",
        "supporting_evidence": ("receipt:bd004",),
        "conflicting_evidence": (),
        "limitations": ("development only",),
        "scope": ("development",),
        "excluded_scope": ("production", "certification"),
        "predecessor_decisions": (),
        "superseding_decisions": (),
        "dependent_objects": ("ST-06.03",),
        "invalidation_conditions": ("operator withdraws authority",),
        "review_state": "reviewed",
    }
    values.update(overrides)
    return GenesisDecision(**values)


def test_valid_limited_and_active_review_dispositions_are_distinct():
    active = review_genesis_decision(decision(), requested_scope="development")
    limited = review_genesis_decision(decision(), requested_scope="production")

    assert active.disposition is ReviewDisposition.VALID_ACTIVE
    assert limited.disposition is ReviewDisposition.VALID_LIMITED_SCOPE
    assert active.review_identity


def test_superseded_invalidated_proposal_and_expired_reviews_are_explicit():
    assert review_genesis_decision(decision(status=DecisionStatus.SUPERSEDED, superseding_decisions=("decision:new",))).disposition is ReviewDisposition.SUPERSEDED
    assert review_genesis_decision(decision(status=DecisionStatus.INVALIDATED)).disposition is ReviewDisposition.INVALIDATED
    assert review_genesis_decision(decision(status=DecisionStatus.PROPOSED, owner_type=OwnerType.AGENT_PROPOSAL)).disposition is ReviewDisposition.PROPOSAL_ONLY
    assert review_genesis_decision(decision(status=DecisionStatus.EXPIRED)).disposition is ReviewDisposition.MISSING_AUTHORITY


def test_missing_evidence_and_conflicting_authority_are_not_hidden():
    assert review_genesis_decision(decision(supporting_evidence=())).disposition is ReviewDisposition.MISSING_EVIDENCE
    assert review_genesis_decision(decision(conflicting_evidence=("conflict:1",))).disposition is ReviewDisposition.CONFLICTING_AUTHORITY


def test_agent_proposals_and_deterministic_code_cannot_impersonate_human_authority():
    with pytest.raises(GenesisReviewError) as proposal:
        decision(owner_type=OwnerType.AGENT_PROPOSAL, status=DecisionStatus.ACTIVE)
    assert proposal.value.code == "AGENT_PROPOSAL_NOT_APPROVAL"

    with pytest.raises(GenesisReviewError) as code:
        decision(decision_class=DecisionClass.HUMAN_AUTHORITY, owner_type=OwnerType.DETERMINISTIC_CODE)
    assert code.value.code == "DETERMINISTIC_CODE_NOT_POLICY_AUTHORITY"


def test_development_only_authority_cannot_be_displayed_as_production_or_certification():
    with pytest.raises(GenesisReviewError) as production:
        decision(production_authority=True)
    assert production.value.code == "PRODUCTION_SCOPE_NOT_GOVERNED"

    with pytest.raises(GenesisReviewError) as cert:
        decision(decision_class=DecisionClass.MATURITY, certified_authority=True)
    assert cert.value.code == "CERTIFICATION_CLASS_REQUIRED"


def test_redaction_filtering_and_no_mutation_review_result():
    redacted = decision(redacted_fields=("display_name",))
    result = review_genesis_decision(redacted)
    assert result.redacted_fields == ("display_name",)

    decisions = (
        redacted,
        decision(decision_identity="decision:workflow", decision_class=DecisionClass.WORKFLOW_POLICY, subject_identity="workflow:1"),
    )
    assert [item.decision_identity for item in filter_decisions(decisions, decision_class=DecisionClass.WORKFLOW_POLICY)] == ["decision:workflow"]

    with pytest.raises(GenesisReviewError) as mutation:
        result.__class__(result.decision_identity, result.disposition, result.reason, result.dependent_objects, result.redacted_fields, underlying_decision_mutated=True)
    assert mutation.value.code == "REVIEW_CANNOT_AMEND_DECISION"
