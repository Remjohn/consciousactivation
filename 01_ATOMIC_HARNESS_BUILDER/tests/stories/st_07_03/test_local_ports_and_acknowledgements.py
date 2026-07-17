from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.external_handoff_commands import (
    CompileExternalHandoffCommand,
    ExternalHandoffCommandRejected,
    ExternalHandoffService,
    InMemoryExternalHandoffObservationSink,
    InMemoryExternalHandoffRepository,
    LocalDelegationHandoffTestDouble,
    LocalVisualAssetDemandTestDouble,
)
from cmf_builder.domain.external_handoff_contracts import (
    DELEGATION_TARGET,
    EXTERNAL_VALIDATION_PENDING,
    LOCAL_TEST_DOUBLE_ONLY,
    VAE_TARGET,
)
from test_external_handoff_contracts import handoff_input


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def context():
    authority = AuthorityService(
        actors=(Actor("handoff-code", ActorKind.CODE), Actor("unauthorized", ActorKind.CODE)),
        grants=(AuthorityGrant("handoff-code", frozenset({Action.COMPILE_EXTERNAL_HANDOFFS}), "*", NOW + timedelta(days=1)),),
    )
    repo = InMemoryExternalHandoffRepository()
    observations = InMemoryExternalHandoffObservationSink()
    vae = LocalVisualAssetDemandTestDouble()
    delegation = LocalDelegationHandoffTestDouble()
    return ExternalHandoffService(
        authority=authority,
        repository=repo,
        observations=observations,
        vae_port=vae,
        delegation_port=delegation,
    ), repo, observations, vae, delegation


def command(target_id: str, *, command_id: str | None = None, actor="handoff-code"):
    return CompileExternalHandoffCommand(
        command_id=command_id or f"compile-{target_id}",
        handoff_input=handoff_input(target_id),
        actor_id=actor,
        now=NOW,
        correlation_id="corr-st0703",
        causation_id="ST-07.02",
    )


@pytest.mark.parametrize("target_id", (VAE_TARGET, DELEGATION_TARGET))
def test_local_ports_acknowledge_without_external_acceptance(target_id: str) -> None:
    service, _, observations, vae, delegation = context()
    result = service.compile_and_acknowledge(command(target_id))
    assert result.acknowledgement.authority == LOCAL_TEST_DOUBLE_ONLY
    assert result.acknowledgement.external_acceptance is False
    assert result.compatibility.external_compatibility == EXTERNAL_VALIDATION_PENDING
    assert result.result_boundary.external_result_received is False
    assert observations.items[-1].outcome == "PASS"
    assert len(vae.calls if target_id == VAE_TARGET else delegation.calls) == 1


def test_command_replay_returns_original_and_conflict_fails() -> None:
    service, repo, _, vae, _ = context()
    original = command(VAE_TARGET)
    first = service.compile_and_acknowledge(original)
    assert service.compile_and_acknowledge(original) == first
    assert len(vae.calls) == 1
    assert repo.command_state(original.command_id) is not None
    with pytest.raises(ExternalHandoffCommandRejected, match="conflicting payload"):
        service.compile_and_acknowledge(replace(original, correlation_id="changed"))


def test_wrong_port_target_and_unauthorized_actor_fail_closed() -> None:
    service, repo, observations, _, _ = context()
    with pytest.raises(ExternalHandoffCommandRejected):
        service.compile_and_acknowledge(command(VAE_TARGET, actor="unauthorized"))
    assert repo.command_state(f"compile-{VAE_TARGET}") is None
    assert observations.items[-1].outcome == "FAIL"


def test_od_branch_rejects_arbitrary_or_external_port_implementations() -> None:
    authority = AuthorityService(
        actors=(Actor("handoff-code", ActorKind.CODE),),
        grants=(AuthorityGrant("handoff-code", frozenset({Action.COMPILE_EXTERNAL_HANDOFFS}), "*", NOW + timedelta(days=1)),),
    )

    class UnsealedPort(LocalVisualAssetDemandTestDouble):
        pass

    with pytest.raises(ExternalHandoffCommandRejected, match="exact local VAE test double"):
        ExternalHandoffService(
            authority=authority,
            repository=InMemoryExternalHandoffRepository(),
            observations=InMemoryExternalHandoffObservationSink(),
            vae_port=UnsealedPort(),
            delegation_port=LocalDelegationHandoffTestDouble(),
        )


def test_injected_commit_failure_leaves_no_command_state() -> None:
    service, repo, observations, _, delegation = context()
    repo.inject_failure_before_commit()
    with pytest.raises(ExternalHandoffCommandRejected, match="Injected"):
        service.compile_and_acknowledge(command(DELEGATION_TARGET))
    assert repo.command_state(f"compile-{DELEGATION_TARGET}") is None
    assert delegation.calls == []
    assert tuple(item.outcome for item in observations.items) == ("FAIL",)


def test_observation_and_local_port_failures_leave_zero_partial_state() -> None:
    service, repo, observations, vae, _ = context()
    observations.inject_failure_before_emit()
    with pytest.raises(ExternalHandoffCommandRejected, match="observation"):
        service.compile_and_acknowledge(command(VAE_TARGET, command_id="observation-failure"))
    assert repo.command_state("observation-failure") is None
    assert vae.calls == []
    assert tuple(item.outcome for item in observations.items) == ("FAIL",)

    vae.inject_failure_before_record()
    with pytest.raises(ExternalHandoffCommandRejected, match="local-port"):
        service.compile_and_acknowledge(command(VAE_TARGET, command_id="port-failure"))
    assert repo.command_state("port-failure") is None
    assert vae.calls == []
    assert observations.items[-1].outcome == "FAIL"
