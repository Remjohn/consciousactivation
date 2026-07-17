from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import DeterministicUuid7IdProvider, FixedClock
from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.genesis_decision_commands import (
    GenesisDecisionCommandService, RecordGenesisDecisionCommand, ReopenGenesisDecisionCommand,
)
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_03_01 import build_context as build_question_context, open_command


def build_context(*, seed="ST-03.02"):
    question_service, repository, observations, run_id = build_question_context(seed=f"{seed}-question")
    question_receipt = question_service.open(open_command(repository, run_id))
    actors = (
        Actor("architect-1", ActorKind.HUMAN), Actor("other-human", ActorKind.HUMAN),
        Actor("code-1", ActorKind.CODE), Actor("agent-1", ActorKind.AGENT),
        Actor("expired-human", ActorKind.HUMAN),
    )
    grants = (
        AuthorityGrant("architect-1", frozenset(Action), "*", NOW + timedelta(days=1)),
        AuthorityGrant("other-human", frozenset(Action), "another-run", NOW + timedelta(days=1)),
        AuthorityGrant("code-1", frozenset(Action), "*", NOW + timedelta(days=1)),
        AuthorityGrant("agent-1", frozenset(Action), "*", NOW + timedelta(days=1)),
        AuthorityGrant("expired-human", frozenset(Action), "*", NOW - timedelta(seconds=1)),
    )
    service = GenesisDecisionCommandService(
        repository=repository, authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(timestamp_ms=1_768_400_000_000, seed=seed),
        clock=FixedClock(NOW), observations=observations,
    )
    return service, repository, observations, run_id, question_receipt


def record_command(repository, run_id, package_id, **changes):
    run = repository.load_run(run_id)
    values = {
        "command_id": "genesis-decision-command-1", "run_id": run_id,
        "actor_id": "architect-1", "expected_version": run.stream_version,
        "correlation_id": "st-03-02-correlation-1", "causation_id": "ST-03.01:QuestionPackage",
        "package_id": package_id,
        "raw_answer": "Use the minimal linear phase sequence for this synthetic proof.",
        "selected_option": "minimal_linear_phases",
        "rationale": "It is the narrowest governed option and requires no external runtime.",
        "provisional_draft_ref": "advisory-draft:phase-hypotheses-v1",
    }
    values.update(changes)
    return RecordGenesisDecisionCommand(**values)


def reopen_command(repository, run_id, memory_id, **changes):
    run = repository.load_run(run_id)
    values = {
        "command_id": "genesis-decision-reopen-1", "run_id": run_id,
        "actor_id": "architect-1", "expected_version": run.stream_version,
        "correlation_id": "st-03-02-correlation-1", "causation_id": "governed-contradiction",
        "memory_id": memory_id,
        "reason": "New governed evidence contradicts the ratified phase decision.",
    }
    values.update(changes)
    return ReopenGenesisDecisionCommand(**values)
