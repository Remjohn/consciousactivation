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
from cmf_builder.application.handoff_commands import (
    CompilePhaseHandoffsCommand,
    DecideInternalHandoffCommand,
    IssueInternalHandoffCommand,
    PhaseHandoffCommandService,
)
from cmf_builder.domain.handoff import (
    PHASE_HANDOFF_INPUT_PATH,
    PHASE_HANDOFF_INPUT_SHA256,
    GovernedHandoffArtifact,
    InternalHandoffDecisionAction,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_04_03 import build_context as build_phase_context
from tests.stories.st_04_03 import compile_command as compile_phase_command


CONTRACT_ID = "ratified_boundary_to_governed_contract_v1"
SENDER_PHASE = "ratified_boundary_ready"
RECEIVER_PHASE = "governed_contract_ready"
RECEIVER_AUTHORITY = "cmf_builder.constitutional_validation"


def build_context(*, seed: str = "ST-04.04", root=ROOT):
    phases, atomicity, repository, observations, run_id, _ = build_phase_context(
        seed=f"{seed}-phases", root=root
    )
    phase_receipt = phases.compile(compile_phase_command(run_id))
    actors = tuple(
        Actor(actor_id, kind)
        for actor_id, kind in (
            ("architect-1", ActorKind.HUMAN),
            ("code-1", ActorKind.CODE),
            ("agent-1", ActorKind.AGENT),
            ("external-1", ActorKind.EXTERNAL),
        )
    )
    grants = tuple(
        AuthorityGrant(
            actor_id=actor.actor_id,
            actions=frozenset(Action),
            resource_id="*",
            expires_at=NOW + timedelta(days=1),
        )
        for actor in actors
    )
    service = PhaseHandoffCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_800_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return service, atomicity, repository, observations, run_id, phase_receipt


def compile_command(
    run_id: str,
    *,
    command_id: str = "phase-handoffs-1",
    actor_id: str = "code-1",
    expected_version: int = 16,
    handoff_input_path: str = PHASE_HANDOFF_INPUT_PATH,
    handoff_input_sha256: str = PHASE_HANDOFF_INPUT_SHA256,
) -> CompilePhaseHandoffsCommand:
    return CompilePhaseHandoffsCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-04-04-correlation-1",
        causation_id="ST-04.03:StoryCompletionReceipt",
        handoff_input_path=handoff_input_path,
        handoff_input_sha256=handoff_input_sha256,
    )


def governed_artifacts(service, repository, run_id: str) -> tuple[GovernedHandoffArtifact, ...]:
    graph = service.get_active(run_id)
    boundary = repository.get_atomic_boundary(graph.boundary_ref)
    record = repository.get_command_record("atomicity-decision-1")
    assert boundary is not None and record is not None
    receipt = record.result
    return tuple(
        sorted(
            (
                GovernedHandoffArtifact(
                    field="frozen_atomic_boundary_ref",
                    artifact_id=boundary.boundary_id,
                    artifact_hash=boundary.content_hash,
                    version=boundary.version,
                    lineage_refs=graph.lineage_refs,
                ),
                GovernedHandoffArtifact(
                    field="boundary_validation_receipt_ref",
                    artifact_id=receipt.receipt_id,
                    artifact_hash=receipt.receipt_hash,
                    version="1.0.0",
                    lineage_refs=graph.lineage_refs,
                ),
            ),
            key=lambda item: item.field,
        )
    )


def issue_command(
    run_id: str,
    artifacts: tuple[GovernedHandoffArtifact, ...],
    *,
    command_id: str = "internal-handoff-issue-1",
    actor_id: str = "code-1",
    expected_version: int = 17,
    sender_phase: str = SENDER_PHASE,
    receiver_phase: str = RECEIVER_PHASE,
) -> IssueInternalHandoffCommand:
    return IssueInternalHandoffCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-04-04-correlation-2",
        causation_id="phase-handoffs-1",
        contract_id=CONTRACT_ID,
        sender_phase=sender_phase,
        receiver_phase=receiver_phase,
        artifacts=artifacts,
    )


def decision_command(
    run_id: str,
    handoff_id: str,
    *,
    command_id: str = "internal-handoff-decision-1",
    actor_id: str = "code-1",
    expected_version: int = 18,
    receiver_phase: str = RECEIVER_PHASE,
    receiver_authority: str = RECEIVER_AUTHORITY,
    action: InternalHandoffDecisionAction = InternalHandoffDecisionAction.ACCEPTED,
    reason_code: str = "CONTRACT_AND_ARTIFACTS_VALID",
    reason: str = "The exact governed contract and immutable artifacts validate.",
) -> DecideInternalHandoffCommand:
    return DecideInternalHandoffCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-04-04-correlation-3",
        causation_id="internal-handoff-issue-1",
        handoff_id=handoff_id,
        receiver_phase=receiver_phase,
        receiver_authority=receiver_authority,
        action=action,
        reason_code=reason_code,
        reason=reason,
    )
