from __future__ import annotations

import pytest

from cmf_activative_intelligence.application import AirApplication
from cmf_activative_intelligence.domain import AirValidationError, supported_object_types


def r(identifier: str, fill: str = "a") -> dict[str, str]:
    return {"object_id": identifier, "version": "1.0.0", "sha256": fill * 64}


def obj_ref(result: dict) -> dict[str, str]:
    obj = result["object"]
    return {"object_id": obj["object_id"], "version": obj["semantic_version"], "sha256": obj["canonical_sha256"]}


def test_phase9_air_types_registered():
    types = set(supported_object_types())
    required = {
        "interview_asset_contract", "interview_asset_contract_arm_receipt",
        "live_narrative_policy_proposal", "observed_activative_intelligence_pack",
        "campaign_activation_program", "activation_freshness_profile",
        "audience_reaction_receipt", "campaign_revision_request",
        "relationship_activation_state", "reelcast_progression_program",
        "visual_activation_handoff", "activation_evaluation_receipt",
        "programmed_model_evidence_candidate",
    }
    assert required.issubset(types)


def test_interview_contract_has_exact_seven_branches_and_arm_separation(tmp_path):
    app = AirApplication(tmp_path / "air.sqlite3"); app.initialize()
    result = app.phase9.compile_interview_asset_contract(
        program_id="iac:test", planned_pack_ref=r("planned"), source_context_ref=r("source"),
        evidence_refs=[r("e1"), r("e2")], parent_lock_refs=[r("lock")],
        evaluation_profile_ref=r("eval"), idempotency_key="iac",
    )
    branches = result["object"]["payload"]["branch_program"]
    assert len(branches) == 7
    assert {b["condition"] for b in branches} == {
        "ANCHOR_HIT", "PARTIAL_HIT", "DEFENSE", "TOPIC_ESCAPE",
        "CONTRADICTION", "OVERLOAD", "RELATIONAL_RESET",
    }
    with pytest.raises(AirValidationError):
        app.phase9.arm_contract(
            receipt_id="arm:bad", contract_ref=obj_ref(result), session_context_ref=r("session"),
            compiler_actor_id="same", evaluator_actor_id="same", human_actor_id="operator",
            idempotency_key="bad",
        )


def test_live_policy_observed_pack_relationship_and_visual_handoff(tmp_path):
    app = AirApplication(tmp_path / "air.sqlite3"); app.initialize()
    live = app.phase9.compile_live_policy(
        proposal_id="live:test", contract_ref=r("iac"), live_state_ref=r("live"),
        evidence_refs=[r("e")], current_dose=3, ceiling=3, overload=True,
        producer_actor_id="producer", evaluator_actor_id="evaluator", idempotency_key="live",
    )
    assert live["object"]["payload"]["pressure_recommendation"]["recommended_dose"] == 2
    assert live["object"]["payload"]["call_options"][0]["action_kind"] == "PAUSE"
    observed = app.phase9.compile_observed_pack(
        pack_id="observed:test", source_package_refs=[r("source")], reaction_refs=[r("reaction")],
        expression_refs=[r("expression")], input_manifest_ref=r("manifest"),
        candidate_portfolio_ref=r("portfolio"), independent_evaluation_ref=r("evaluation"),
        human_resolution_ref=r("human"), planned_pack_ref=r("planned"), idempotency_key="observed",
    )
    assert observed["object"]["payload"]["epistemic_state"] == "observed"
    state, program = app.phase9.compile_relationship_program(
        state_id="relationship:test", subject_ref=r("person"), evidence_refs=[r("evidence")],
        coalition_ref=r("coalition"), evaluation_ref=r("evaluation"), idempotency_key="relationship",
    )
    assert program["object"]["payload"]["current_step_id"] == "engage"
    handoff = app.phase9.compile_visual_handoff(
        handoff_id="visual:test", source_refs=[r("source")], semantic_package_ref=r("semantic"),
        final_script_ref=r("script"), transfer_ref=r("transfer"), wrong_reading_locks=[r("lock")],
        producer_actor_id="producer", evaluator_actor_id="evaluator", idempotency_key="visual",
    )
    assert handoff["object"]["payload"]["requirement_intents"][0]["authority_class"] == "NONAUTHORITATIVE_REQUIREMENT_INTENT"


def test_campaign_freshness_audience_revision_and_programmed_model_evidence(tmp_path):
    app = AirApplication(tmp_path / "air.sqlite3"); app.initialize()
    campaign = app.campaigns.store_program({
        "campaign_program_id": "campaign:test", "version": "1.0.0",
        "audience_context_ref": r("audience"), "source_package_refs": [r("source")],
        "entry_program_refs": [r("derivative")], "freshness_policy_ref": r("freshness-policy"),
        "activation_axes": [{
            "entry_program_ref": r("derivative"), "psychological_role": "self-recognizing witness",
            "tension": "control protects agency while isolating the person", "edge_product_ref": r("edge"),
            "primitive_coalition_ref": r("coalition"), "archetype_coalition_ref": r("archetype"),
            "relief_state": "PARTIAL",
        }],
        "sequence_constraints": ["preserve source-first order"],
        "relief_requirements": ["provide a truthful release after pressure"],
        "lifecycle_state": "VALIDATED",
        "authority": {"authority_id": "ca-program-control-v2.1-candidate", "authority_version": "2.1.0-candidate", "authority_sha256": "b" * 64, "authority_state": "candidate_not_current"},
    }, idempotency_key="campaign")
    fresh = app.campaigns.compile_freshness_profile(
        campaign_program_ref=obj_ref(campaign), audience_context_ref=r("audience"),
        platform_id="development-export", window_id="window:1",
        exposures=[{
            "asset_ref": r("asset"), "pattern_ids": ["pattern:role"], "impressions": 100,
            "engagements": 10, "shares": 3, "cohort_id": "cohort:reference",
            "paid_or_organic": "organic", "metric_definition_ref": r("metric"),
        }],
        policy={"repeated_pattern_threshold": 3, "minimum_share_rate_micros": 1000},
        idempotency_key="freshness",
    )
    assert fresh["object"]["payload"]["causal_claim_authorized"] is False
    audience = app.campaigns.record_audience_reaction(
        campaign_program_ref=obj_ref(campaign), asset_ref=r("asset"), audience_context_ref=r("audience"),
        observations=[{
            "observation_id": "obs:1", "metric_name": "operator_acceptance", "value": 1,
            "denominator": 1, "epistemic_state": "observed", "limitations": ["development operator"],
            "metric_definition_ref": r("metric"),
        }],
        evaluator_id="audience-evaluator", producer_id="publisher", idempotency_key="audience",
    )
    assert audience["object"]["payload"]["source_reaction_receipt_overwritten"] is False
    revision = app.campaigns.propose_revision(
        campaign_program_ref=obj_ref(campaign), freshness_profile_ref=obj_ref(fresh),
        affected_entry_refs=[r("derivative")], reason_codes=["FORMULA_VISIBILITY"],
        owner_product="activative-intelligence-runtime", idempotency_key="revision",
    )
    assert revision["object"]["payload"]["scope"] == "AFFECTED_ENTRIES_ONLY"
    evidence = app.programmed_model_evidence.register_claim_candidate(
        model_claim_ref=r("claim"), model_program_ref=r("program"), semantic_scope_refs=[r("scope")],
        human_resolution_refs=[r("human")], benchmark_ref=r("benchmark"),
        independent_evaluator_ref=r("independent-evaluator"), producer_actor_id="producer",
        evaluator_actor_id="evaluator", idempotency_key="pm-evidence",
    )
    assert evidence["object"]["payload"]["automatic_weight_update"] is False
