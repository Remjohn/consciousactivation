from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from _support import ROOT  # type: ignore  # noqa: F401

from ca_runtime.cli import bootstrap_transition
from ca_runtime.database import IdempotencyConflict, ProductDatabase


class RuntimeTests(unittest.TestCase):
    def test_initialize_atomic_transition_and_replay(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            database = ProductDatabase(
                Path(temp_dir) / "product.sqlite3",
                product_id="phase1-test",
                product_version="0.1.0.dev1",
                authority_state="candidate_not_current",
                development_authorized=True,
            )
            health = database.initialize(initialized_at_utc="2026-07-23T12:00:00Z")
            self.assertEqual(health.integrity, "ok")
            transition = bootstrap_transition(
                "phase1-test",
                "0.1.0.dev1",
                now="2026-07-23T12:00:00Z",
            )
            receipt = database.record_transition(
                command_envelope=transition[0],
                command_payload=transition[1],
                event_envelope=transition[2],
                event_payload=transition[3],
                receipt_envelope=transition[4],
            )
            replay = database.record_transition(
                command_envelope=transition[0],
                command_payload=transition[1],
                event_envelope=transition[2],
                event_payload=transition[3],
                receipt_envelope=transition[4],
            )
            self.assertEqual(receipt, replay)
            health = database.health()
            self.assertEqual((health.command_count, health.event_count, health.receipt_count), (1, 1, 1))
            self.assertEqual(len(database.list_events("phase1-test")), 1)

    def test_idempotency_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            database = ProductDatabase(
                Path(temp_dir) / "product.sqlite3",
                product_id="phase1-test",
                product_version="0.1.0.dev1",
                authority_state="candidate_not_current",
                development_authorized=True,
            )
            database.initialize(initialized_at_utc="2026-07-23T12:00:00Z")
            transition = list(bootstrap_transition("phase1-test", "0.1.0.dev1", now="2026-07-23T12:00:00Z"))
            database.record_transition(
                command_envelope=transition[0],
                command_payload=transition[1],
                event_envelope=transition[2],
                event_payload=transition[3],
                receipt_envelope=transition[4],
            )
            changed = dict(transition[0])
            changed["command_type"] = "ca.phase01.changed"
            with self.assertRaises(IdempotencyConflict):
                database.record_transition(
                    command_envelope=changed,
                    command_payload=transition[1],
                    event_envelope=transition[2],
                    event_payload=transition[3],
                    receipt_envelope=transition[4],
                )


if __name__ == "__main__":
    unittest.main()
