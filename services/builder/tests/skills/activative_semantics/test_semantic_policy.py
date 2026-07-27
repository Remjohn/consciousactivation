from __future__ import annotations

from pathlib import Path

import yaml

from cmf_builder.skills.activative_contracts import (
    EXPECTED_DOWNSTREAM_OWNERS,
    SEMANTIC_FIELD_PATHS,
)


POLICY_PATH = Path(
    "governance/skills/activative_intelligence_pack_compiler/SEMANTIC_POLICY.yaml"
)


def test_semantic_policy_matches_frozen_interface_and_contract() -> None:
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))

    assert policy["skill"] == {
        "skill_id": "activative_intelligence_pack_compiler",
        "skill_version": "1.0.0",
        "authority_lane": "Analyst",
        "maturity_ceiling": "development_validated",
        "package_state": "development_uncertified",
        "production_eligible": False,
        "certified": False,
    }
    base_paths = tuple(
        path for path in SEMANTIC_FIELD_PATHS if not path.startswith("downstream_")
    )
    assert tuple(policy["required_semantic_fields"]) == base_paths
    assert tuple(policy["downstream_applicability"]["required_artifacts"]) == (
        "reaction_receipt",
        "expression_moment",
        "visual_semantic_pack",
        "visual_narrative_program",
        "feature_contracts",
        "tv_route",
        "composition_intent",
    )
    expected_owners = {
        artifact.value: owner
        for artifact, owner in EXPECTED_DOWNSTREAM_OWNERS.items()
    }
    assert policy["downstream_applicability"]["external_owners"] == (
        expected_owners
    )


def test_policy_preserves_human_truth_and_provider_boundaries() -> None:
    policy = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8"))
    prohibited = set(policy["authority"]["skill_must_not"])

    assert {
        "manufacture_human_original_truth",
        "manufacture_human_reaction",
        "issue_Reaction_Receipt",
        "issue_Expression_Moment",
        "approve_Identity_DNA_amendment",
        "execute_external_provider",
    } <= prohibited
    assert policy["lineage"]["mode"] == "per_field_non_flattened"
    assert policy["lineage"]["generic_notes_field_allowed"] is False
    assert policy["wrong_reading_locks"]["minimum_count"] == 1
    assert policy["boundaries"]["desired_reaction_status"] == (
        "intended_not_observed"
    )
    assert policy["boundaries"]["external_provider_execution"] == "forbidden"
    assert policy["boundaries"]["production_claim"] == "forbidden"
    assert policy["boundaries"]["certification_claim"] == "forbidden"
