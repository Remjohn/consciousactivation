from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)

from cmf_builder.visual.atomicity_contracts import (
    AtomicityStatus,
    BoundaryCandidate,
    BoundaryOptionKind,
    ComparisonDimension,
    DimensionAssessment,
    EvidenceStatus,
    RecommendationDisposition,
    RiskDirection,
    RiskDomain,
    RiskSeverity,
    WrongBoundaryRisk,
)
from cmf_builder.visual.boundary_comparison import compare_candidate_boundaries
from cmf_builder.visual.induction import induce_provisional_grammar
from tests.stories.st_02_03.fixtures import (
    induction_policy,
    provisional_hypothesis,
    supported_graphs,
)


COMPARISON_AUTHORITY = "offline_atomicity_comparison_authority"
NOW = datetime(2026, 7, 17, 6, 0, tzinfo=timezone.utc)


def authority_service(
    resource_id: str,
    *,
    actor_id: str = COMPARISON_AUTHORITY,
    register_actor: bool = True,
    grant_resource_id: str | None = None,
    expires_at: datetime | None = None,
) -> AuthorityService:
    actors = (
        (Actor(actor_id=actor_id, kind=ActorKind.CODE),)
        if register_actor
        else ()
    )
    grants = (
        AuthorityGrant(
            actor_id=actor_id,
            actions=frozenset({Action.COMPARE_ATOMIC_BOUNDARIES}),
            resource_id=grant_resource_id or resource_id,
            expires_at=expires_at or NOW + timedelta(days=1),
        ),
    )
    return AuthorityService(actors=actors, grants=grants)


def grammar_result(*, statement: str | None = None):
    graphs = supported_graphs()
    hypothesis = provisional_hypothesis(
        graphs,
        **({} if statement is None else {"statement": statement}),
    )
    return induce_provisional_grammar(
        run_id="st_02_04_source_grammar",
        graphs=graphs,
        policy=induction_policy(),
        hypotheses=(hypothesis,),
    )


def candidate(
    grammar,
    option_kind: BoundaryOptionKind,
    *,
    status: AtomicityStatus | None = None,
    recommendation: RecommendationDisposition | None = None,
    unavailable_dimension: ComparisonDimension | None = None,
) -> BoundaryCandidate:
    graph_ids = tuple(item.graph_id for item in grammar.source_graphs)
    specimen_ids = tuple(sorted(item.specimen_id for item in grammar.source_graphs))
    motif_ids = (grammar.motifs[0].motif_id,)
    hypothesis_ids = (grammar.hypotheses[0].hypothesis_id,)
    dimensions = []
    for dimension in ComparisonDimension:
        if dimension is unavailable_dimension:
            dimensions.append(
                DimensionAssessment(
                    dimension=dimension,
                    finding=f"{dimension.value} needs additional governed evidence.",
                    evidence_status=EvidenceStatus.UNAVAILABLE,
                )
            )
        elif dimension is ComparisonDimension.COMPOSITION_GRAMMAR:
            dimensions.append(
                DimensionAssessment(
                    dimension=dimension,
                    finding="The repeated substrate-specific relation is deterministically observed.",
                    evidence_status=EvidenceStatus.DETERMINISTIC_SYNTAX,
                    source_graph_ids=graph_ids,
                    motif_ids=motif_ids,
                )
            )
        else:
            dimensions.append(
                DimensionAssessment(
                    dimension=dimension,
                    finding=(
                        f"The {dimension.value.lower()} consequence remains a visible "
                        "provisional interpretation."
                    ),
                    evidence_status=EvidenceStatus.PROVISIONAL_HYPOTHESIS,
                    source_graph_ids=graph_ids,
                    hypothesis_ids=hypothesis_ids,
                )
            )
    direction = (
        RiskDirection.OVER_MERGE
        if option_kind in (BoundaryOptionKind.MERGE, BoundaryOptionKind.FAMILY)
        else RiskDirection.OVER_SPLIT
    )
    risks = tuple(
        WrongBoundaryRisk(
            domain=domain,
            direction=direction,
            consequence=(
                f"The {option_kind.value.lower()} alternative may create a provisional "
                f"{domain.value.lower()} consequence if the boundary is wrong."
            ),
            severity=RiskSeverity.UNKNOWN,
            source_graph_ids=graph_ids,
            hypothesis_ids=hypothesis_ids,
        )
        for domain in RiskDomain
    )
    defaults = {
        BoundaryOptionKind.MERGE: (
            AtomicityStatus.NEEDS_PARTITION,
            RecommendationDisposition.REJECT,
        ),
        BoundaryOptionKind.SPLIT: (
            AtomicityStatus.ATOMIC_HARNESS_CANDIDATE,
            RecommendationDisposition.SUPPORT,
        ),
        BoundaryOptionKind.VARIANT: (
            AtomicityStatus.VARIANT_OF_EXISTING,
            RecommendationDisposition.SUPPORT,
        ),
        BoundaryOptionKind.FAMILY: (
            AtomicityStatus.DISH_FAMILY_CANDIDATE,
            RecommendationDisposition.SUPPORT,
        ),
    }
    default_status, default_recommendation = defaults[option_kind]
    if unavailable_dimension is not None:
        default_status = AtomicityStatus.INSUFFICIENT_EVIDENCE
        default_recommendation = RecommendationDisposition.MORE_EVIDENCE
    shared = tuple(
        dimension
        for dimension in ComparisonDimension
        if dimension
        in (
            ComparisonDimension.PRODUCTION_PROMISE,
            ComparisonDimension.INPUT_CONTRACT,
            ComparisonDimension.ASSET_PROGRAM,
        )
    )
    differing = tuple(
        dimension for dimension in ComparisonDimension if dimension not in shared
    )
    return BoundaryCandidate(
        candidate_id=f"candidate_{option_kind.value.lower()}",
        option_kind=option_kind,
        status=status or default_status,
        recommendation=recommendation or default_recommendation,
        consequence=(
            f"This {option_kind.value.lower()} alternative exposes configuration and "
            "capability-boundary consequences without selecting a boundary."
        ),
        affected_specimen_ids=specimen_ids,
        shared_dimensions=shared,
        differing_dimensions=differing,
        configuration_sufficient=option_kind is BoundaryOptionKind.VARIANT,
        breaking_dimensions=(
            ComparisonDimension.STATE_MACHINE,
            ComparisonDimension.RUNTIME_OWNERSHIP,
        ),
        evidence_gaps=(
            (f"Missing {unavailable_dimension.value} evidence",)
            if unavailable_dimension is not None
            else ()
        ),
        dimensions=tuple(dimensions),
        risks=risks,
    )


def all_candidates(grammar) -> tuple[BoundaryCandidate, ...]:
    return tuple(candidate(grammar, kind) for kind in BoundaryOptionKind)


def comparison_result(
    *,
    source=None,
    candidates=None,
    run_id="st_02_04_compare",
    authority_ref=COMPARISON_AUTHORITY,
):
    source = source or grammar_result()
    candidates = candidates or all_candidates(source.grammar)
    return compare_candidate_boundaries(
        run_id=run_id,
        grammar_result=source,
        candidates=candidates,
        comparison_authority_ref=authority_ref,
    )


def changed_comparison_result(source=None):
    source = source or grammar_result()
    candidates = list(all_candidates(source.grammar))
    candidates[0] = replace(
        candidates[0],
        consequence=candidates[0].consequence + " A new governed consequence is visible.",
    )
    return comparison_result(source=source, candidates=tuple(candidates))
