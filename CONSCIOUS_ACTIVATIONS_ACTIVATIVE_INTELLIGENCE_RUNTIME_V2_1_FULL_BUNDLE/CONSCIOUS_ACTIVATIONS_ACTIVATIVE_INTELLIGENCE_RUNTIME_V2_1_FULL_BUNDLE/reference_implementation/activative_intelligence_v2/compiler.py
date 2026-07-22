from __future__ import annotations

from datetime import datetime, timezone

from .models import (
    ActivationEvaluationReceipt,
    ActivationHypothesisPortfolio,
    ActivationDomain,
    CanonicalInterviewSourcePackage,
    EpistemicState,
    ExpressionMoment,
    IdentityDNACandidateObservation,
    ImmutableRef,
    ObservedActivativeIntelligencePack,
    PlannedActivativeIntelligencePack,
    PlannedObservedDelta,
    ReactionReceipt,
)


def compile_planned_pack(
    *,
    pack_id: str,
    version: str,
    domain: ActivationDomain,
    source_premise_ref: ImmutableRef,
    coach_identity_dna_ref: ImmutableRef,
    audience_context_premise_ref: ImmutableRef,
    resonance_map_ref: ImmutableRef,
    matrix_of_edging_ref: ImmutableRef,
    portfolio: ActivationHypothesisPortfolio,
    selected_hypothesis_id: str,
    evaluation_contract_ref: ImmutableRef,
    registry_refs: tuple[ImmutableRef, ...],
    interviewer_resonance_ref: ImmutableRef | None = None,
    relationship_state_ref: ImmutableRef | None = None,
) -> PlannedActivativeIntelligencePack:
    return PlannedActivativeIntelligencePack(
        pack_id=pack_id,
        version=version,
        domain=domain,
        source_premise_ref=source_premise_ref,
        coach_identity_dna_ref=coach_identity_dna_ref,
        audience_context_premise_ref=audience_context_premise_ref,
        resonance_map_ref=resonance_map_ref,
        matrix_of_edging_ref=matrix_of_edging_ref,
        interviewer_resonance_ref=interviewer_resonance_ref,
        relationship_state_ref=relationship_state_ref,
        candidate_portfolio=portfolio,
        selected_hypothesis_id=selected_hypothesis_id,
        evaluation_contract_ref=evaluation_contract_ref,
        registry_refs=registry_refs,
    )


def compile_observed_pack(
    *,
    pack_id: str,
    version: str,
    planned_pack_ref: ImmutableRef,
    source_package: CanonicalInterviewSourcePackage,
    reaction_receipts: tuple[ReactionReceipt, ...],
    expression_moments: tuple[ExpressionMoment, ...],
    confirmed_roles: tuple[str, ...],
    confirmed_stances: tuple[str, ...],
    confirmed_stakes: tuple[str, ...],
    activated_hypothesis_ids: tuple[str, ...],
    unmet_hypothesis_ids: tuple[str, ...],
    unexpected_edges: tuple[str, ...] = (),
    rejected_assumptions: tuple[str, ...] = (),
    unresolved_inferences: tuple[str, ...] = (),
    identity_observations: tuple[IdentityDNACandidateObservation, ...] = (),
    transfer_requirements: tuple[str, ...] = (),
    campaign_opportunities: tuple[str, ...] = (),
    wrong_reading_updates: tuple[str, ...] = (),
) -> ObservedActivativeIntelligencePack:
    approved = tuple(
        moment for moment in expression_moments if moment.state.value == "approved"
    )
    return ObservedActivativeIntelligencePack(
        pack_id=pack_id,
        version=version,
        planned_pack_ref=planned_pack_ref,
        source_package_ref=ImmutableRef(
            object_id=source_package.source_package_id,
            version=source_package.version,
            sha256="0" * 64,
        ),
        epistemic_state=EpistemicState.OBSERVED,
        reaction_receipt_refs=tuple(
            ImmutableRef(object_id=r.receipt_id, version="1.0.0", sha256="0" * 64)
            for r in reaction_receipts
        ),
        expression_moment_refs=tuple(
            ImmutableRef(object_id=m.moment_id, version="1.0.0", sha256="0" * 64)
            for m in approved
        ),
        confirmed_roles=confirmed_roles,
        confirmed_stances=confirmed_stances,
        confirmed_stakes=confirmed_stakes,
        unresolved_inferences=unresolved_inferences,
        identity_dna_candidate_observations=identity_observations,
        planned_observed_delta=PlannedObservedDelta(
            activated_hypothesis_ids=activated_hypothesis_ids,
            unmet_hypothesis_ids=unmet_hypothesis_ids,
            unexpected_edges=unexpected_edges,
            rejected_assumptions=rejected_assumptions,
            unresolved_inferences=unresolved_inferences,
        ),
        transfer_requirements=transfer_requirements,
        campaign_opportunities=campaign_opportunities,
        wrong_reading_updates=wrong_reading_updates,
    )


def mechanical_evaluation_receipt(
    *,
    receipt_id: str,
    evaluated_ref: ImmutableRef,
    domain: ActivationDomain,
    gate_results: dict[str, bool],
    dimension_scores: dict[str, float],
    evidence_refs: tuple[ImmutableRef, ...],
) -> ActivationEvaluationReceipt:
    verdict = "pass" if all(gate_results.values()) else "fail"
    return ActivationEvaluationReceipt(
        receipt_id=receipt_id,
        evaluated_ref=evaluated_ref,
        domain=domain,
        gate_results=gate_results,
        dimension_scores=dimension_scores,
        verdict=verdict,
        evidence_refs=evidence_refs,
        created_at=datetime.now(timezone.utc),
    )
