from __future__ import annotations

from threading import Barrier, Lock, Thread
from time import sleep

import pytest

from cmf_builder.adapters.in_memory_run_repository import InMemoryRunRepository
from cmf_builder.application.ports import CommandRecord, ConcurrencyConflict
from cmf_builder.application.run_commands import CommandReceipt
from tests.stories.st_01_01 import NOW, build_service, create_command


def _competing_event(run, *, event_id: str, command_id: str):
    _, event = run.resume(
        checkpoint_id=None,
        event_id=event_id,
        command_id=command_id,
        actor_id="architect-1",
        timestamp=NOW,
        correlation_id="BQA-P1-004",
        causation_id="concurrent-writer",
    )
    return event


def test_raw_compare_and_append_is_one_synchronized_operation() -> None:
    service, repository, _, _, _ = build_service()
    created = service.create_run(create_command())
    run = repository.load_run(created.run_id)
    events = (
        _competing_event(run, event_id="event-concurrent-a", command_id="writer-a"),
        _competing_event(run, event_id="event-concurrent-b", command_id="writer-b"),
    )
    original = repository._validated_append

    def delayed_check(*args, **kwargs):
        current = original(*args, **kwargs)
        sleep(0.05)
        return current

    repository._validated_append = delayed_check
    start = Barrier(2)
    outcomes: list[object] = []
    outcome_lock = Lock()

    def writer(event) -> None:
        start.wait()
        try:
            repository.append(created.run_id, 2, (event,))
            outcome: object = "PASS"
        except Exception as error:  # captured for exact cross-thread assertion
            outcome = error
        with outcome_lock:
            outcomes.append(outcome)

    threads = [Thread(target=writer, args=(event,)) for event in events]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)

    assert all(not thread.is_alive() for thread in threads)
    assert sum(item == "PASS" for item in outcomes) == 1
    assert sum(isinstance(item, ConcurrencyConflict) for item in outcomes) == 1
    assert repository.event_count(created.run_id) == 3


class BarrierRunRepository(InMemoryRunRepository):
    def __init__(self) -> None:
        super().__init__()
        self.start = Barrier(2)

    def commit_run_command(self, **kwargs) -> None:
        self.start.wait()
        return super().commit_run_command(**kwargs)


@pytest.mark.parametrize("attempt", range(10))
def test_atomic_winner_retains_its_event_and_command_record(attempt: int) -> None:
    repository = BarrierRunRepository()
    bootstrap, source_repository, _, _, _ = build_service()
    created = bootstrap.create_run(create_command())
    repository._streams[created.run_id] = source_repository.events(created.run_id)
    run = repository.load_run(created.run_id)
    attempts = []
    for suffix in ("a", "b"):
        command_id = f"writer-{suffix}"
        event = _competing_event(
            run,
            event_id=f"event-concurrent-{attempt}-{suffix}",
            command_id=command_id,
        )
        receipt = CommandReceipt(
            receipt_id=f"receipt-{suffix}",
            command_id=command_id,
            run_id=created.run_id,
            event_ids=(event.event_id,),
            outcome="PASS",
            authority_identity="architect-1",
            artifact_identity=f"artifact-{suffix}",
            provenance="ST-01.01",
        )
        attempts.append((command_id, event, receipt))

    outcomes: list[tuple[str, object]] = []
    guard = Lock()

    def writer(command_id, event, receipt) -> None:
        try:
            repository.commit_run_command(
                run_id=created.run_id,
                expected_version=2,
                events=(event,),
                command_id=command_id,
                command_record=CommandRecord(
                    payload_hash=f"sha256:{command_id}", result=receipt
                ),
                checkpoint=None,
            )
            result: object = "PASS"
        except Exception as error:
            result = error
        with guard:
            outcomes.append((command_id, result))

    threads = [Thread(target=writer, args=attempt) for attempt in attempts]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)

    assert sum(result == "PASS" for _, result in outcomes) == 1
    assert sum(isinstance(result, ConcurrencyConflict) for _, result in outcomes) == 1
    winner = next(command_id for command_id, result in outcomes if result == "PASS")
    stored_event = repository.events(created.run_id)[-1]
    record = repository.get_command_record(winner)
    assert stored_event.command_id == winner
    assert record is not None
    assert record.result.event_ids == (stored_event.event_id,)
