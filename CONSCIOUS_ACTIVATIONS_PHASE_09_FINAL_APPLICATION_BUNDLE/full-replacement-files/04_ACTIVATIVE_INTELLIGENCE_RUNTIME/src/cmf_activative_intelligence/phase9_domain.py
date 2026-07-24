from __future__ import annotations
from typing import Any, Mapping

from .domain import _strict_fields


def _require_distinct_actors(payload: Mapping[str, Any], producer: str, evaluator: str, issues: list[str]) -> None:
    if payload.get(producer) == payload.get(evaluator):
        issues.append(f"{producer} and {evaluator} must differ")


def _validate_campaign_program(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['program_id','version','authority','lifecycle_state','epistemic_state','audience_context_ref','campaign_policy_ref','asset_plans','freshness_profile_ref','wrong_reading_lock_refs','evaluation_profile_ref','limitations'], issues=issues)
    plans = payload.get('asset_plans', [])
    if not isinstance(plans, list) or not plans:
        issues.append('asset_plans must be non-empty')
    else:
        indexes=[item.get('sequence_index') for item in plans if isinstance(item, Mapping)]
        if indexes != list(range(len(plans))): issues.append('asset_plans sequence_index must be contiguous and ordered')


def _validate_freshness(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['profile_id','version','authority','lifecycle_state','epistemic_state','audience_context_ref','platform_profile_id','window','exposure_refs','repetition_counts','hard_gates','freshness_findings','limitations'], issues=issues)
    counts=payload.get('repetition_counts')
    if not isinstance(counts, Mapping): issues.append('repetition_counts must be an object')
    elif any(not isinstance(v, int) or isinstance(v, bool) or v < 0 for v in counts.values()): issues.append('repetition counts must be non-negative integers')
    if not payload.get('hard_gates'): issues.append('hard_gates must be non-empty')
    if not payload.get('freshness_findings'): issues.append('freshness_findings must be non-empty')


def _validate_audience(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['receipt_id','version','authority','lifecycle_state','epistemic_state','campaign_program_ref','asset_ref','platform_profile_id','observation_window','observed_metrics','measurement_limits','inferred_role_signals','producer_actor_id','evaluator_actor_id','limitations'], issues=issues)
    _require_distinct_actors(payload, 'producer_actor_id', 'evaluator_actor_id', issues)
    if payload.get('epistemic_state') != 'observed': issues.append('audience reaction receipt must preserve observed state')
    if not payload.get('observed_metrics'): issues.append('observed_metrics must be non-empty')
    if not payload.get('measurement_limits'): issues.append('measurement_limits must be non-empty')

def _validate_revision(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['campaign_revision_request_id','version','campaign_program_ref','freshness_profile_ref','affected_entry_refs','reason_codes','responsible_owner','scope','historical_bytes_preserved','lifecycle_state','epistemic_state','authority'], issues=issues)
    if payload.get('scope') != 'AFFECTED_ENTRIES_ONLY': issues.append('campaign revision scope must be affected entries only')
    if payload.get('historical_bytes_preserved') is not True: issues.append('campaign revision must preserve historical bytes')


def _validate_pm_evidence(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['evidence_candidate_id','version','model_claim_ref','model_program_ref','semantic_scope_refs','human_resolution_refs','benchmark_ref','independent_evaluator_ref','producer_actor_id','evaluator_actor_id','promotion_ceiling','automatic_weight_update','automatic_doctrine_mutation','lifecycle_state','epistemic_state','authority'], issues=issues)
    _require_distinct_actors(payload, 'producer_actor_id', 'evaluator_actor_id', issues)
    if payload.get('automatic_weight_update') is not False: issues.append('automatic weight update forbidden')
    if payload.get('automatic_doctrine_mutation') is not False: issues.append('automatic doctrine mutation forbidden')


def _validate_iac(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['program_id','version','authority','lifecycle_state','epistemic_state','planned_pack_ref','source_context_ref','target_expression_state','first_line_anchor','depth_anchor','branch_program','pressure_envelope','landing_criteria','route_hypotheses','parent_lock_refs','evaluation_profile_ref','limitations'], issues=issues)
    branches = payload.get('branch_program', [])
    expected = {'ANCHOR_HIT','PARTIAL_HIT','DEFENSE','TOPIC_ESCAPE','CONTRADICTION','OVERLOAD','RELATIONAL_RESET'}
    observed = {str(item.get('condition')) for item in branches if isinstance(item, Mapping)}
    if observed != expected or len(branches) != 7: issues.append('branch_program must contain exactly the seven governed branches')
    ceiling = payload.get('pressure_envelope', {}).get('ceiling') if isinstance(payload.get('pressure_envelope'), Mapping) else None
    if not isinstance(ceiling, int) or ceiling < 0: issues.append('pressure ceiling must be a non-negative integer')


def _validate_iac_arm(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['receipt_id','version','authority','lifecycle_state','contract_ref','evaluation_result','compiler_actor_id','evaluator_actor_id','human_actor_id','session_context_ref','armed_hashes','production_authorized'], issues=issues)
    _require_distinct_actors(payload, 'compiler_actor_id', 'evaluator_actor_id', issues)
    if payload.get('production_authorized') is not False: issues.append('Phase 9 arm receipt cannot authorize production')
    if payload.get('evaluation_result') != 'PASS': issues.append('only a passing arm receipt may be stored as armed')


def _validate_live_policy(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['proposal_id','version','authority','lifecycle_state','epistemic_state','interview_asset_contract_ref','live_state_ref','state_watermark','counteractivation_profile','call_options','pressure_recommendation','transition_options','smallest_useful_call_proof','producer_actor_id','evaluator_actor_id','limitations'], issues=issues)
    _require_distinct_actors(payload, 'producer_actor_id', 'evaluator_actor_id', issues)
    rec = payload.get('pressure_recommendation', {})
    if isinstance(rec, Mapping):
        current, recommended, ceiling = rec.get('current_dose'), rec.get('recommended_dose'), rec.get('ceiling')
        if not all(isinstance(x, int) for x in (current, recommended, ceiling)): issues.append('pressure doses must be integers')
        elif not (0 <= recommended <= ceiling): issues.append('recommended pressure dose must stay within ceiling')
    calls = payload.get('call_options', [])
    if not any(isinstance(c, Mapping) and c.get('action_kind') == 'STOP' for c in calls): issues.append('STOP call must always remain available')


def _validate_observed_pack(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['pack_id','version','authority','lifecycle_state','epistemic_state','source_package_refs','reaction_receipt_refs','expression_moment_refs','input_manifest_ref','semantic_claims','primitive_evidence','planned_observed_delta','negative_and_unresolved_evidence','candidate_portfolio_ref','independent_evaluation_ref','human_resolution_ref','downstream_consumers','limitations'], issues=issues)
    if payload.get('epistemic_state') != 'observed': issues.append('Observed Activative Intelligence Pack must preserve observed state')
    if not payload.get('reaction_receipt_refs'): issues.append('reaction_receipt_refs must be non-empty')
    if not payload.get('expression_moment_refs'): issues.append('expression_moment_refs must be non-empty')


def _validate_relationship_state(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['state_id','version','authority','lifecycle_state','epistemic_state','subject_ref','stage','evidence_refs','pressure_ceiling','affinity_state','previous_state_ref','limitations'], issues=issues)
    if payload.get('stage') not in {'DISCOVERED','RECOGNIZED','ENGAGED','BRIEF_ACCEPTED','SESSION_SCHEDULED','SESSION_COMPLETE','PAUSED','CANCELLED'}: issues.append('unknown relationship stage')


def _validate_reelcast(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['program_id','version','authority','lifecycle_state','epistemic_state','relationship_state_ref','transition_policy_ref','ordered_steps','current_step_id','primitive_coalition_ref','pause_reset_cancel_policy_ref','evaluation_receipt_ref','limitations'], issues=issues)
    steps = payload.get('ordered_steps', [])
    ids = [item.get('step_id') for item in steps if isinstance(item, Mapping)]
    if len(ids) != len(set(ids)): issues.append('ordered_steps contains duplicate step IDs')
    if payload.get('current_step_id') not in ids: issues.append('current_step_id must reference an ordered step')


def _validate_visual_handoff(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['handoff_id','version','authority','lifecycle_state','epistemic_state','source_package_refs','semantic_production_package_ref','approved_final_script_ref','activation_transfer_contract_ref','visual_semantic_pack','visual_narrative_program','composition_intents','feature_contracts','requirement_intents','category_id','profile_id','wrong_reading_lock_refs','producer_actor_id','evaluator_actor_id','limitations'], issues=issues)
    _require_distinct_actors(payload, 'producer_actor_id', 'evaluator_actor_id', issues)
    for item in payload.get('requirement_intents', []):
        if isinstance(item, Mapping) and item.get('authority_class') != 'NONAUTHORITATIVE_REQUIREMENT_INTENT': issues.append('VAE requirement intents must remain nonauthoritative')


def _validate_activation_evaluation(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['receipt_id','version','authority','lifecycle_state','target_ref','evaluation_profile_ref','deterministic_checks','judgment_dimensions','failure_attribution','producer_actor_id','evaluator_actor_id','verdict','limitations'], issues=issues)
    _require_distinct_actors(payload, 'producer_actor_id', 'evaluator_actor_id', issues)
    hard_fail = any(isinstance(c, Mapping) and c.get('hard_gate') and c.get('result') != 'PASS' for c in payload.get('deterministic_checks', []))
    if hard_fail and payload.get('verdict') == 'PASS': issues.append('hard-gate failure cannot receive PASS')


def _validate_programmed_model_evidence(payload: Mapping[str, Any], issues: list[str]) -> None:
    _strict_fields(payload, required=['evidence_id','version','authority','lifecycle_state','model_claim_ref','task_family','dataset_lineage_refs','evaluation_receipt_refs','shadow_result_ref','baseline_comparison_ref','fallback_ref','applicability_envelope','promotion_state','limitations'], issues=issues)
    if payload.get('promotion_state') not in {'SHADOW_READY','VALIDATED_DEVELOPMENT','REJECTED'}:
        issues.append('programmed model evidence promotion_state is outside the development envelope')
    limitations=payload.get('limitations', [])
    if 'no live weight update' not in limitations: issues.append('programmed model evidence must prohibit live weight update')
    if 'no production promotion' not in limitations: issues.append('programmed model evidence must prohibit production promotion')


PHASE9_VALIDATORS = {
    'campaign_activation_program': _validate_campaign_program,
    'activation_freshness_profile': _validate_freshness,
    'audience_reaction_receipt': _validate_audience,
    'campaign_revision_request': _validate_revision,
    'programmed_model_evidence_candidate': _validate_pm_evidence,
    'programmed_model_evidence': _validate_programmed_model_evidence,
    'interview_asset_contract': _validate_iac,
    'interview_asset_contract_arm_receipt': _validate_iac_arm,
    'live_narrative_policy_proposal': _validate_live_policy,
    'observed_activative_intelligence_pack': _validate_observed_pack,
    'relationship_activation_state': _validate_relationship_state,
    'reelcast_progression_program': _validate_reelcast,
    'visual_activation_handoff': _validate_visual_handoff,
    'activation_evaluation_receipt': _validate_activation_evaluation,
}

PHASE9_ID_FIELDS = {
    'campaign_activation_program': 'program_id',
    'activation_freshness_profile': 'profile_id',
    'audience_reaction_receipt': 'receipt_id',
    'campaign_revision_request': 'campaign_revision_request_id',
    'programmed_model_evidence_candidate': 'evidence_candidate_id',
    'programmed_model_evidence': 'evidence_id',
    'interview_asset_contract': 'program_id',
    'interview_asset_contract_arm_receipt': 'receipt_id',
    'live_narrative_policy_proposal': 'proposal_id',
    'observed_activative_intelligence_pack': 'pack_id',
    'relationship_activation_state': 'state_id',
    'reelcast_progression_program': 'program_id',
    'visual_activation_handoff': 'handoff_id',
    'activation_evaluation_receipt': 'receipt_id',
}
