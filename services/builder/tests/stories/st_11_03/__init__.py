from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import FixedClock
from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.implementation_feedback_commands import (
    GovernImplementationFeedbackCommand,
    ImplementationFeedbackCommandService,
)
from cmf_builder.domain.implementation_feedback import (
    DIRECT_DEPENDENCIES,
    FEEDBACK_INPUT_PATH,
    FEEDBACK_INPUT_SHA256,
    FEEDBACK_MODE,
    FEEDBACK_PROFILE_ID,
    OWNED_OBLIGATIONS,
    PROPOSAL_STATUS,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_11_02 import build_context as build_plan_context
from tests.stories.st_11_02 import plan_command


def build_context(*, seed: str = "ST-11.03", root=ROOT):
    service, _, atomicity, repository, observations, run_id, _, _ = build_plan_context(seed=f"{seed}-plan", root=root)
    plan_receipt = service.compile(plan_command(run_id))
    actors = tuple(Actor(actor_id, kind) for actor_id, kind in (
        ("architect-1", ActorKind.HUMAN), ("code-1", ActorKind.CODE),
        ("agent-1", ActorKind.AGENT), ("external-1", ActorKind.EXTERNAL),
    ))
    grants = tuple(AuthorityGrant(actor_id=actor.actor_id, actions=frozenset(Action), resource_id="*", expires_at=NOW + timedelta(days=1)) for actor in actors)
    feedback_service = ImplementationFeedbackCommandService(
        root=root, repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        clock=FixedClock(NOW), observations=observations,
    )
    return feedback_service, service, atomicity, repository, observations, run_id, plan_receipt, service.get_active(run_id)


def feedback_command(
    run_id: str, *, command_id: str = "synthetic-feedback-proposal-1",
    actor_id: str = "code-1", expected_version: int = 25,
    feedback_input_path: str = FEEDBACK_INPUT_PATH,
    feedback_input_sha256: str = FEEDBACK_INPUT_SHA256,
    requested_operation: str = "govern_implementation_feedback_as_proposal",
    requested_mode: str = FEEDBACK_MODE,
    requested_profile_id: str = FEEDBACK_PROFILE_ID,
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS,
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES,
    requested_proposal_status: str = PROPOSAL_STATUS,
    requested_apply_proposal: bool = False, requested_ratified: bool = False,
    requested_authority_mutation: bool = False,
    requested_production_eligible: bool = False, requested_certified: bool = False,
    feedback_overrides: tuple[tuple[str, str], ...] = (),
) -> GovernImplementationFeedbackCommand:
    return GovernImplementationFeedbackCommand(
        command_id=command_id, run_id=run_id, actor_id=actor_id,
        expected_version=expected_version, correlation_id="st-11-03-correlation-1",
        causation_id="ST-11.02:StoryCompletionReceipt",
        feedback_input_path=feedback_input_path,
        feedback_input_sha256=feedback_input_sha256,
        requested_operation=requested_operation, requested_mode=requested_mode,
        requested_profile_id=requested_profile_id,
        requested_obligations=requested_obligations,
        requested_dependencies=requested_dependencies,
        requested_proposal_status=requested_proposal_status,
        requested_apply_proposal=requested_apply_proposal,
        requested_ratified=requested_ratified,
        requested_authority_mutation=requested_authority_mutation,
        requested_production_eligible=requested_production_eligible,
        requested_certified=requested_certified,
        feedback_overrides=feedback_overrides,
    )

