from __future__ import annotations

import importlib.util
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import time

import pytest


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "packages"
    / "ca_runtime"
    / "src"
    / "ca_runtime"
    / "sqlite_tuning.py"
)
_spec = importlib.util.spec_from_file_location(
    "ca_runtime_sqlite_tuning_m056",
    MODULE_PATH,
)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"Cannot load SQLite tuning module from {MODULE_PATH}")
_sqlite_tuning = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _sqlite_tuning
_spec.loader.exec_module(_sqlite_tuning)

SQLiteBackgroundCheckpointer = _sqlite_tuning.SQLiteBackgroundCheckpointer
SQLiteTuningConfig = _sqlite_tuning.SQLiteTuningConfig
SQLiteTuningVerificationError = _sqlite_tuning.SQLiteTuningVerificationError
checkpoint_sqlite = _sqlite_tuning.checkpoint_sqlite
configure_sqlite_connection = _sqlite_tuning.configure_sqlite_connection
open_sqlite_connection = _sqlite_tuning.open_sqlite_connection
verify_sqlite_connection = _sqlite_tuning.verify_sqlite_connection


def _run_python_script(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )


def test_default_policy_encodes_inv_wal_001() -> None:
    config = SQLiteTuningConfig()
    assert config.busy_timeout_ms == 60_000
    assert config.mmap_size_bytes == 256 * 1024 * 1024
    assert config.wal_autocheckpoint_pages == 1_000
    assert config.checkpoint_mode == "PASSIVE"


def test_configure_and_verify_queries_live_pragmas(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    config = SQLiteTuningConfig(
        mmap_size_bytes=128 * 1024 * 1024,
        wal_autocheckpoint_pages=250,
        checkpoint_interval_seconds=0.05,
    )
    connection = sqlite3.connect(db_path)
    try:
        snapshot = configure_sqlite_connection(connection, config)
        assert snapshot.journal_mode == "wal"
        assert snapshot.busy_timeout_ms == config.busy_timeout_ms
        assert snapshot.mmap_size_bytes == config.mmap_size_bytes
        assert snapshot.wal_autocheckpoint_pages == config.wal_autocheckpoint_pages
        assert snapshot.synchronous_name == config.synchronous
        assert verify_sqlite_connection(connection, config) == snapshot
    finally:
        connection.close()


def test_wal_mode_persists_across_reopen(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    first = open_sqlite_connection(db_path)
    try:
        first.execute("CREATE TABLE state (id INTEGER PRIMARY KEY, value TEXT)")
        first.commit()
    finally:
        first.close()

    reopened = open_sqlite_connection(db_path)
    try:
        assert reopened.execute("PRAGMA journal_mode").fetchone()[0].lower() == "wal"
        assert verify_sqlite_connection(reopened).journal_mode == "wal"
    finally:
        reopened.close()


def test_separate_process_reopens_with_live_wal_policy(tmp_path: Path) -> None:
    """A worker in a separate Python process sees the persisted WAL policy."""

    db_path = tmp_path / "process_reopen.db"
    connection = open_sqlite_connection(db_path)
    connection.execute("CREATE TABLE state (id INTEGER PRIMARY KEY, value TEXT)")
    connection.commit()
    connection.close()

    script = f"""
import sys
sys.path.insert(0, {str(MODULE_PATH.parent)!r})
from sqlite_tuning import open_sqlite_connection, verify_sqlite_connection
connection = open_sqlite_connection({str(db_path)!r})
snapshot = verify_sqlite_connection(connection)
print(
    snapshot.journal_mode,
    snapshot.busy_timeout_ms,
    snapshot.mmap_size_bytes,
    snapshot.wal_autocheckpoint_pages,
    flush=True,
)
connection.close()
"""
    result = _run_python_script(script)
    fields = result.stdout.strip().split()
    assert fields == ["wal", "60000", str(256 * 1024 * 1024), "1000"]


def test_each_independent_connection_receives_the_same_policy(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    config = SQLiteTuningConfig(busy_timeout_ms=60_000)
    first = open_sqlite_connection(db_path, config)
    second = open_sqlite_connection(db_path, config)
    try:
        assert verify_sqlite_connection(first, config) == verify_sqlite_connection(
            second, config
        )
        assert first.execute("PRAGMA busy_timeout").fetchone()[0] == 60_000
        assert second.execute("PRAGMA busy_timeout").fetchone()[0] == 60_000
    finally:
        first.close()
        second.close()


def test_verify_rejects_live_connection_with_wrong_busy_timeout(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    connection = sqlite3.connect(db_path)
    try:
        config = SQLiteTuningConfig(busy_timeout_ms=60_000)
        configure_sqlite_connection(connection, config)
        connection.execute("PRAGMA busy_timeout=1")
        with pytest.raises(SQLiteTuningVerificationError, match="busy_timeout_ms"):
            verify_sqlite_connection(connection, config)
    finally:
        connection.close()


def test_checkpoint_returns_live_sqlite_wal_counters(tmp_path: Path) -> None:
    db_path = tmp_path / "state.db"
    connection = open_sqlite_connection(
        db_path,
        SQLiteTuningConfig(wal_autocheckpoint_pages=100_000),
    )
    try:
        connection.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)")
        connection.commit()
        for _index in range(100):
            connection.execute("INSERT INTO data(value) VALUES (?)", ("x" * 1000,))
        connection.commit()
        result = checkpoint_sqlite(connection, "PASSIVE")
        assert result.mode == "PASSIVE"
        assert result.busy in (0, 1)
        assert result.wal_frames >= 0
        assert result.checkpointed_frames >= 0
        assert result.checkpointed_frames <= result.wal_frames
    finally:
        connection.close()


def test_background_checkpointer_runs_on_a_dedicated_connection(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "state.db"
    config = SQLiteTuningConfig(
        wal_autocheckpoint_pages=100_000,
        checkpoint_interval_seconds=0.05,
    )
    connection = open_sqlite_connection(db_path, config)
    try:
        connection.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)")
        connection.commit()
        with SQLiteBackgroundCheckpointer(db_path, config) as checkpointer:
            for _index in range(200):
                connection.execute(
                    "INSERT INTO data(value) VALUES (?)",
                    ("payload" * 30,),
                )
            connection.commit()

            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline and checkpointer.last_result is None:
                time.sleep(0.01)

            assert checkpointer.last_result is not None
            assert checkpointer.last_error is None
    finally:
        connection.close()


def test_independent_connections_wait_on_sqlite_write_lock(tmp_path: Path) -> None:
    db_path = tmp_path / "concurrency.db"
    ready = threading.Event()
    outcome: dict[str, float] = {}
    errors: list[BaseException] = []

    def holder() -> None:
        connection = open_sqlite_connection(
            db_path,
            SQLiteTuningConfig(busy_timeout_ms=10_000),
        )
        try:
            connection.execute(
                "CREATE TABLE workers (id INTEGER PRIMARY KEY, value TEXT)"
            )
            connection.commit()
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("INSERT INTO workers(value) VALUES ('holder')")
            ready.set()
            time.sleep(0.75)
            connection.commit()
        except BaseException as error:
            errors.append(error)
            ready.set()
        finally:
            connection.close()

    def contender() -> None:
        ready.wait(timeout=5)
        connection = None
        try:
            started = time.monotonic()
            connection = open_sqlite_connection(
                db_path,
                SQLiteTuningConfig(busy_timeout_ms=3_000),
            )
            connection.execute(
                "INSERT INTO workers(value) VALUES ('contender')"
            )
            connection.commit()
            outcome["elapsed"] = time.monotonic() - started
        except BaseException as error:
            errors.append(error)
        finally:
            if connection is not None:
                connection.close()

    first = threading.Thread(target=holder)
    second = threading.Thread(target=contender)
    first.start()
    second.start()
    first.join(timeout=5)
    second.join(timeout=5)

    assert not first.is_alive()
    assert not second.is_alive()
    assert errors == []
    assert outcome["elapsed"] >= 0.50


def test_process_local_lock_is_not_treated_as_distributed_sqlite_proof(
    tmp_path: Path,
) -> None:
    """An unrelated in-process mutex cannot replace SQLite connection locking."""

    db_path = tmp_path / "false_proof.db"
    bootstrap = open_sqlite_connection(db_path)
    local_lock = threading.Lock()
    local_lock.acquire()
    try:
        bootstrap.execute(
            "CREATE TABLE workers (id INTEGER PRIMARY KEY, value TEXT)"
        )
        bootstrap.commit()
        bootstrap.execute("BEGIN IMMEDIATE")
        bootstrap.execute("INSERT INTO workers(value) VALUES ('parent')")

        outcome: dict[str, object] = {}

        def worker() -> None:
            connection = open_sqlite_connection(
                db_path,
                SQLiteTuningConfig(busy_timeout_ms=200),
            )
            try:
                try:
                    connection.execute(
                        "INSERT INTO workers(value) VALUES ('child')"
                    )
                    connection.commit()
                    outcome["status"] = "unexpected-success"
                except sqlite3.OperationalError as error:
                    outcome["status"] = str(error).lower()
            finally:
                connection.close()

        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=3)

        assert not thread.is_alive()
        assert "locked" in str(outcome["status"])
        assert local_lock.locked()
    finally:
        local_lock.release()
        bootstrap.rollback()
        bootstrap.close()


def test_background_checkpointer_recovers_after_transient_lock(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "recovery.db"
    config = SQLiteTuningConfig(checkpoint_interval_seconds=0.05)
    connection = open_sqlite_connection(db_path, config)
    blocker = None
    try:
        connection.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, value TEXT)")
        connection.commit()

        blocker = sqlite3.connect(db_path, timeout=0.1)
        configure_sqlite_connection(
            blocker,
            SQLiteTuningConfig(
                busy_timeout_ms=100,
                checkpoint_interval_seconds=0.05,
            ),
        )
        blocker.execute("BEGIN IMMEDIATE")
        blocker.execute("INSERT INTO data(value) VALUES ('blocked')")

        with SQLiteBackgroundCheckpointer(db_path, config) as checkpointer:
            time.sleep(0.15)
            blocker.rollback()
            blocker.close()
            blocker = None

            deadline = time.monotonic() + 2.0
            while time.monotonic() < deadline:
                if checkpointer.last_result is not None:
                    break
                time.sleep(0.01)

            assert checkpointer.last_result is not None
            assert checkpointer.last_error is None
    finally:
        if blocker is not None:
            blocker.close()
        connection.close()
