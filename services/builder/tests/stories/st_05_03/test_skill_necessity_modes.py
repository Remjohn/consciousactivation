from __future__ import annotations

import dataclasses

import pytest

from cmf_builder.skills.necessity import (
    ACTIVATIVE_COMPILER_SKILL_ID,
    HarnessSkillMode,
    SkillRequirementDecision,
    SkillRequirementError,
    determine_skill_requirement,
)


def test_generic_fixture_preserves_governed_zero_skill_result() -> None:
    decision = determine_skill_requirement(HarnessSkillMode.GENERIC_DETERMINISTIC)
    assert decision.real_skill_required is False
    assert decision.required_skill_id is None
    assert decision.decision_status == "development_validated"
    assert decision.canonical_dict()["decision_hash"] == decision.decision_hash


def test_activative_fixture_proves_exact_portable_skill_is_required() -> None:
    decision = determine_skill_requirement(HarnessSkillMode.ACTIVATIVE)
    assert decision.real_skill_required is True
    assert decision.required_skill_id == ACTIVATIVE_COMPILER_SKILL_ID
    assert decision.required_skill_version == "1.0.0"
    assert any(item.alternative == "deterministic_builder_code" and not item.adequate for item in decision.alternatives)
    assert any(item.alternative == "canonical_portable_skill" and item.adequate for item in decision.alternatives)
    assert decision.production_eligible is False
    assert decision.certified is False


def test_skill_necessity_is_deterministic_and_detects_drift() -> None:
    first = determine_skill_requirement(HarnessSkillMode.ACTIVATIVE)
    second = determine_skill_requirement(HarnessSkillMode.ACTIVATIVE)
    assert first == second
    altered = dataclasses.replace(first, required_capability="changed")
    with pytest.raises(SkillRequirementError, match="drifted"):
        altered.canonical_dict()


def test_no_skill_claim_cannot_hide_a_skill_pin() -> None:
    source = determine_skill_requirement(HarnessSkillMode.GENERIC_DETERMINISTIC)
    with pytest.raises(SkillRequirementError, match="hidden skill"):
        SkillRequirementDecision.create(
            mode=HarnessSkillMode.GENERIC_DETERMINISTIC,
            required_capability=source.required_capability,
            real_skill_required=False,
            required_skill_id=ACTIVATIVE_COMPILER_SKILL_ID,
            required_skill_version="1.0.0",
            governing_policy_refs=source.governing_policy_refs,
            authority_refs=source.authority_refs,
            alternatives=source.alternatives,
        )
