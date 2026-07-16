from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.evidence_index_commands import EvidenceIndexCommandService
from cmf_builder.application.evidence_saturation_commands import SaturationCommandService
from cmf_builder.application.genesis_question_commands import (
    GenesisQuestionCommandService,
    InvalidateGenesisQuestionCommand,
    OpenGenesisQuestionCommand,
)
from cmf_builder.domain.evidence_saturation import SaturationContract
from cmf_builder.domain.genesis_questions import (
    DecisionDefinition,
    RecommendationAlternative,
)
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_01_03 import index_command
from tests.stories.st_01_04 import evaluation_command
from tests.stories.st_02_05 import build_context as build_atomicity_context, decide_command


def build_context(*, seed: str = "ST-03.01", genesis_observations=None):
    atomicity, repository, observations, run_id, source_receipt = build_atomicity_context()
    code = Actor("code-1", ActorKind.CODE)
    actors = (code, Actor("architect-1", ActorKind.HUMAN), Actor("agent-1", ActorKind.AGENT))
    grants = tuple(
        AuthorityGrant(actor.actor_id, frozenset(Action), "*", NOW + timedelta(days=1))
        for actor in actors
    )
    authority = AuthorityService(actors=actors, grants=grants)
    indexer = EvidenceIndexCommandService(
        repository=repository, authority=authority,
        ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_100_000_000, seed=f"{seed}-index"),
        clock=FixedClock(NOW), observations=observations,
    )
    indexer.index(index_command(run_id))
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    contract = SaturationContract.create(
        contract_id="synthetic_category_neutral_saturation_v1",
        source_profile_ref=lock.source_profile_ref,
        required_roles=("governed_task_definition",),
    )
    saturation = SaturationCommandService(
        repository=repository, authority=authority,
        ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_200_000_000, seed=f"{seed}-saturation"),
        clock=FixedClock(NOW), observations=observations,
    )
    saturation.evaluate(evaluation_command(run_id, contract))
    atomicity.decide(decide_command(run_id, expected_version=7))
    service = GenesisQuestionCommandService(
        repository=repository, authority=authority,
        ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_300_000_000, seed=seed),
        clock=FixedClock(NOW), observations=genesis_observations or observations,
    )
    return service, repository, observations, run_id


def definitions(repository, run_id: str) -> tuple[DecisionDefinition, ...]:
    run = repository.load_run(run_id)
    evidence = (run.source_lock_ref or "", run.saturation_evaluation_ref or "", run.draft_harness_model_ref or "")
    return (
        DecisionDefinition.create(
            decision_id="phase_hypotheses", target_profile_applicability=(run.target_profile.profile_id,), priority=10,
            question="Which governed phase hypothesis should the synthetic Builder use?",
            rationale="The Draft Harness Model marks phase hypotheses as a human decision.",
            required_evidence=evidence, dependencies=(), options=("minimal_linear_phases", "defer_phase_design"),
            recommended_option="minimal_linear_phases", recommendation_policy="prefer_smallest_governed_atomic_sequence",
            authority_owner="HUMAN", affected_ir_paths=("fields.phase_hypotheses",),
            invalidation_edges=("runtime_hypotheses", "evaluation_hypotheses"),
            completion_rule="human_selects_one_option_with_attributable_ratification",
        ),
        DecisionDefinition.create(
            decision_id="runtime_hypotheses", target_profile_applicability=(run.target_profile.profile_id,), priority=20,
            question="Which runtime hypothesis follows the ratified phase decision?",
            rationale="Runtime meaning depends on the phase hypothesis.",
            required_evidence=evidence, dependencies=("phase_hypotheses",), options=("deterministic_local", "defer_runtime"),
            recommended_option="deterministic_local", recommendation_policy="prefer_no_external_runtime_for_synthetic_proof",
            authority_owner="HUMAN", affected_ir_paths=("fields.runtime_hypotheses",),
            invalidation_edges=("evaluation_hypotheses",),
            completion_rule="human_selects_one_option_after_phase_ratification",
        ),
    )


def open_command(repository, run_id: str, **changes: object) -> OpenGenesisQuestionCommand:
    run = repository.load_run(run_id)
    defs = definitions(repository, run_id)
    options = defs[0].options
    values: dict[str, object] = {
        "command_id": "genesis-question-command-1", "run_id": run_id,
        "actor_id": "code-1", "expected_version": run.stream_version,
        "correlation_id": "st-03-01-correlation-1", "causation_id": "ST-01.04-and-ST-02.05",
        "definitions": defs, "completed_decision_ids": (),
        "available_evidence_refs": (run.source_lock_ref, run.saturation_evaluation_ref, run.draft_harness_model_ref),
        "facts": ("The active Draft Harness Model marks phase_hypotheses DECISION_REQUIRED.", "Saturation permits provisional downstream work."),
        "inferences": ("A minimal linear phase choice is the narrowest synthetic-proof option.",),
        "alternatives": tuple(
            RecommendationAlternative(
                option_id=option,
                tradeoffs=(f"tradeoff:{option}",),
                downstream_consequences=(f"consequence:{option}",),
                risks=(f"risk:{option}",),
            )
            for option in options
        ),
    }
    values.update(changes)
    return OpenGenesisQuestionCommand(**values)


def invalidation_command(repository, run_id: str, package_id: str, **changes: object) -> InvalidateGenesisQuestionCommand:
    run = repository.load_run(run_id)
    values: dict[str, object] = {
        "command_id": "genesis-question-invalidation-1", "run_id": run_id,
        "actor_id": "code-1", "expected_version": run.stream_version,
        "correlation_id": "st-03-01-correlation-1", "causation_id": "governed-upstream-change",
        "package_id": package_id, "reason": "Active evidence changed; a new immutable question package is required.",
    }
    values.update(changes)
    return InvalidateGenesisQuestionCommand(**values)
