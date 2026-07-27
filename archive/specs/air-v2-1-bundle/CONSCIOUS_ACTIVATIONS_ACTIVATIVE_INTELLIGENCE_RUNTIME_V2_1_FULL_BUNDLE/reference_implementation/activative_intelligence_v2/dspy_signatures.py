"""Declarative DSPy signature specifications.

DSPy is intentionally optional in this reference bundle. These dictionaries define
the expected typed program surfaces without importing the package.
"""

SIGNATURES = {
    "DissectLivePremise": {
        "inputs": ["live_premise", "source_context"],
        "outputs": ["surface_topic", "pressure_candidates", "assumptions", "research_gaps"],
    },
    "GenerateActivationHypothesisPortfolio": {
        "inputs": ["identity_context", "audience_context", "relationship_state", "domain", "freshness_profile"],
        "outputs": ["candidate_hypotheses", "diversity_axes", "mechanical_rejections"],
    },
    "CompileInterviewAssetContract": {
        "inputs": ["planned_pack", "target_state", "session_constraints"],
        "outputs": ["interview_asset_contract"],
    },
    "InterpretReactionObservation": {
        "inputs": ["source_signals", "active_contract", "live_state"],
        "outputs": ["observations", "inferred_interpretations", "uncertainty"],
    },
    "SelectNextActivativeAction": {
        "inputs": ["live_state", "active_contract", "recent_receipts"],
        "outputs": ["action_candidates", "selected_action", "stop_or_continue"],
    },
    "ResolveExpressionMomentCandidate": {
        "inputs": ["source_span", "context_window", "reaction_receipts", "route_goal"],
        "outputs": ["candidate", "verdict_dimensions", "wrong_readings"],
    },
    "CompileActivationTransferContract": {
        "inputs": ["observed_pack", "expression_moments", "target_format", "audience_segment"],
        "outputs": ["transfer_contract"],
    },
    "DiagnoseActivativeFailure": {
        "inputs": ["failed_object", "authoritative_inputs", "eval_receipt", "operator_feedback"],
        "outputs": ["failure_attribution", "repair_program"],
    },
    "CompileHumanResolutionEpisode": {
        "inputs": ["before_candidate", "operator_action", "replacement", "context"],
        "outputs": ["human_resolution_episode"],
    },
}
