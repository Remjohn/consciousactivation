from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

import pytest

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.category_commands import (
    BindHarnessCategoryCommand,
    CategoryBindingCommandRejected,
    CategoryBindingService,
    InMemoryCategoryBindingRepository,
    InMemoryCategoryObservationSink,
)


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml"
ACTIVATIVE = ROOT / "tests/fixtures/productization/manifests/activative_expression.json"
NOW = datetime(2026, 7, 16, tzinfo=timezone.utc)


def _service() -> tuple[CategoryBindingService, InMemoryCategoryBindingRepository, InMemoryCategoryObservationSink]:
    authority = AuthorityService(
        actors=(
            Actor("compiler-code", ActorKind.CODE),
            Actor("external-actor", ActorKind.EXTERNAL),
        ),
        grants=(
            AuthorityGrant(
                actor_id="compiler-code",
                actions=frozenset({Action.BIND_HARNESS_CATEGORY}),
                resource_id="*",
                expires_at=NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                actor_id="external-actor",
                actions=frozenset({Action.BIND_HARNESS_CATEGORY}),
                resource_id="*",
                expires_at=NOW + timedelta(days=1),
            ),
        ),
    )
    repository = InMemoryCategoryBindingRepository()
    observations = InMemoryCategoryObservationSink()
    return CategoryBindingService(authority, repository, observations), repository, observations


def _command(command_id: str = "bind-1", actor_id: str = "compiler-code") -> BindHarnessCategoryCommand:
    payload = json.loads(ACTIVATIVE.read_text(encoding="utf-8"))
    return BindHarnessCategoryCommand(
        command_id=command_id,
        harness_id="activative-expression-contract",
        harness_version="1.0.0",
        mode="activative",
        category_ids=(payload["category_id"],),
        activative_input=payload["activative_input"],
        registry_bytes=REGISTRY.read_bytes(),
        actor_id=actor_id,
        now=NOW,
        correlation_id="corr-1",
        causation_id="cause-1",
    )


def test_command_commits_once_and_replay_returns_original_receipt() -> None:
    service, repository, observations = _service()
    first = service.bind(_command())
    second = service.bind(_command())
    assert first == second
    assert repository.binding_count == 1
    assert repository.receipt_count == 1
    assert [item.event_name for item in observations.items] == [
        "ST-06.01:CategoryBindingCommitted",
        "ST-06.01:CategoryBindingReplayReturned",
    ]


def test_conflicting_command_and_unauthorized_actor_fail_closed() -> None:
    service, repository, observations = _service()
    service.bind(_command())
    conflict = _command()
    object.__setattr__(conflict, "category_ids", ("carousels",))
    with pytest.raises(CategoryBindingCommandRejected, match="different payload"):
        service.bind(conflict)
    with pytest.raises(CategoryBindingCommandRejected, match="actor"):
        service.bind(_command("bind-external", "external-actor"))
    assert repository.binding_count == 1
    assert observations.items[-1].outcome == "FAIL"


def test_injected_atomic_failure_leaves_zero_partial_state() -> None:
    service, repository, observations = _service()
    repository.inject_failure_before_commit()
    with pytest.raises(CategoryBindingCommandRejected, match="Injected"):
        service.bind(_command())
    assert repository.binding_count == 0
    assert repository.receipt_count == 0
    assert observations.items[-1].outcome == "FAIL"

