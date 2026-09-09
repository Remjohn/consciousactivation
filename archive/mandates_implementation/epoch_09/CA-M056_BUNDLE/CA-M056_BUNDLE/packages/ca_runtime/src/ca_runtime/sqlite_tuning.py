"""SQLite WAL concurrency tuning for CAE state stores.

CA-M056 / INV-WAL-001

This module owns the SQLite connection policy used by CAE state-store callers.
The policy is intentionally observable on the live connection: callers can
configure a connection and immediately verify the effective PRAGMA values.

The module never uses a process-local mutex as a substitute for SQLite's
locking semantics. Cross-process coordination is delegated to SQLite itself,
with a 60-second busy timeout by default. A dedicated background checkpoint
connection can periodically run PASSIVE checkpoints without sharing an
application connection across threads.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
import threading
from typing import Literal

CheckpointMode = Literal["PASSIVE", "FULL", "RESTART", "TRUNCATE"]


class SQLiteTuningError(RuntimeError):
    """Base error for SQLite tuning failures."""


class SQLiteTuningVerificationError(SQLiteTuningError):
    """Raised when a live connection does not satisfy the tuning policy."""


@dataclass(frozen=True, slots=True)
class SQLiteTuningConfig:
    """Canonical CA-M056 SQLite tuning policy.

    The defaults are deliberately explicit so a caller gets the same policy
    regardless of which code path created its SQLite connection.
    """

    busy_timeout_ms: int = 60_000
    mmap_size_bytes: int = 256 * 1024 * 1024
    wal_autocheckpoint_pages: int = 1_000
    synchronous: Literal["NORMAL", "FULL"] = "NORMAL"
    checkpoint_interval_seconds: float = 5.0
    checkpoint_mode: CheckpointMode = "PASSIVE"

    def __post_init__(self) -> None:
        if self.busy_timeout_ms <= 0:
            raise ValueError("busy_timeout_ms must be positive")
        if self.mmap_size_bytes < 0:
            raise ValueError("mmap_size_bytes must be non-negative")
        if self.wal_autocheckpoint_pages <= 0:
            raise ValueError("wal_autocheckpoint_pages must be positive")
        if self.synchronous not in {"NORMAL", "FULL"}:
            raise ValueError("synchronous must be 'NORMAL' or 'FULL'")
        if self.checkpoint_interval_seconds <= 0:
            raise ValueError("checkpoint_interval_seconds must be positive")
        if self.checkpoint_mode not in {"PASSIVE", "FULL", "RESTART", "TRUNCATE"}:
            raise ValueError(
                "checkpoint_mode must be PASSIVE, FULL, RESTART, or TRUNCATE"
            )


@dataclass(frozen=True, slots=True)
class SQLiteTuningSnapshot:
    """Effective live SQLite settings observed from a connection."""

    journal_mode: str
    busy_timeout_ms: int
    mmap_size_bytes: int
    wal_autocheckpoint_pages: int
    synchronous: int
    synchronous_name: str


@dataclass(frozen=True, slots=True)
class SQLiteCheckpointResult:
    """Result returned by a SQLite WAL checkpoint."""

    mode: CheckpointMode
    busy: int
    wal_frames: int
    checkpointed_frames: int


def _query_int(connection: sqlite3.Connection, pragma: str) -> int:
    row = connection.execute(f"PRAGMA {pragma}").fetchone()
    if row is None:
        raise SQLiteTuningVerificationError(f"PRAGMA {pragma} returned no row")
    return int(row[0])


def configure_sqlite_connection(
    connection: sqlite3.Connection,
    config: SQLiteTuningConfig | None = None,
) -> SQLiteTuningSnapshot:
    """Apply CA-M056 policy and verify the result on the live connection.

    ``journal_mode`` is deliberately queried after setting it. This makes WAL
    a runtime property rather than a configuration assertion.
    """

    policy = config or SQLiteTuningConfig()

    journal_row = connection.execute("PRAGMA journal_mode=WAL").fetchone()
    if journal_row is None or str(journal_row[0]).lower() != "wal":
        observed = None if journal_row is None else str(journal_row[0])
        raise SQLiteTuningVerificationError(
            f"SQLite WAL initialization failed; observed journal_mode={observed!r}"
        )

    connection.execute(f"PRAGMA busy_timeout={policy.busy_timeout_ms}")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute(f"PRAGMA synchronous={policy.synchronous}")
    connection.execute(f"PRAGMA mmap_size={policy.mmap_size_bytes}")
    connection.execute(f"PRAGMA wal_autocheckpoint={policy.wal_autocheckpoint_pages}")

    snapshot = verify_sqlite_connection(connection, policy)
    return snapshot


def open_sqlite_connection(
    db_path: str | Path,
    config: SQLiteTuningConfig | None = None,
    *,
    isolation_level: str | None = "",
) -> sqlite3.Connection:
    """Open and configure a CAE SQLite connection.

    ``timeout`` is set from the same policy as the live ``busy_timeout`` so
    sqlite3's connection-level wait policy and SQLite's PRAGMA agree.
    """

    policy = config or SQLiteTuningConfig()
    connection = sqlite3.connect(
        str(db_path),
        timeout=policy.busy_timeout_ms / 1000,
        isolation_level=isolation_level,
        check_same_thread=False,
    )
    try:
        configure_sqlite_connection(connection, policy)
    except Exception:
        connection.close()
        raise
    return connection


def verify_sqlite_connection(
    connection: sqlite3.Connection,
    config: SQLiteTuningConfig | None = None,
) -> SQLiteTuningSnapshot:
    """Verify tuning against the live connection and return observed values."""

    policy = config or SQLiteTuningConfig()
    journal_mode = str(
        connection.execute("PRAGMA journal_mode").fetchone()[0]
    ).lower()
    busy_timeout_ms = _query_int(connection, "busy_timeout")
    mmap_size_bytes = _query_int(connection, "mmap_size")
    wal_autocheckpoint_pages = _query_int(connection, "wal_autocheckpoint")
    synchronous = _query_int(connection, "synchronous")

    synchronous_names = {0: "OFF", 1: "NORMAL", 2: "FULL", 3: "EXTRA"}
    synchronous_name = synchronous_names.get(synchronous, f"UNKNOWN({synchronous})")

    snapshot = SQLiteTuningSnapshot(
        journal_mode=journal_mode,
        busy_timeout_ms=busy_timeout_ms,
        mmap_size_bytes=mmap_size_bytes,
        wal_autocheckpoint_pages=wal_autocheckpoint_pages,
        synchronous=synchronous,
        synchronous_name=synchronous_name,
    )

    mismatches: list[str] = []
    if snapshot.journal_mode != "wal":
        mismatches.append(f"journal_mode={snapshot.journal_mode!r}, expected 'wal'")
    if snapshot.busy_timeout_ms != policy.busy_timeout_ms:
        mismatches.append(
            f"busy_timeout_ms={snapshot.busy_timeout_ms}, expected {policy.busy_timeout_ms}"
        )
    if snapshot.mmap_size_bytes != policy.mmap_size_bytes:
        mismatches.append(
            f"mmap_size_bytes={snapshot.mmap_size_bytes}, expected {policy.mmap_size_bytes}"
        )
    if snapshot.wal_autocheckpoint_pages != policy.wal_autocheckpoint_pages:
        mismatches.append(
            "wal_autocheckpoint_pages="
            f"{snapshot.wal_autocheckpoint_pages}, expected "
            f"{policy.wal_autocheckpoint_pages}"
        )
    expected_synchronous = {"NORMAL": 1, "FULL": 2}[policy.synchronous]
    if snapshot.synchronous != expected_synchronous:
        mismatches.append(
            f"synchronous={snapshot.synchronous_name!r}, expected {policy.synchronous!r}"
        )

    if mismatches:
        raise SQLiteTuningVerificationError("; ".join(mismatches))

    return snapshot


def checkpoint_sqlite(
    connection: sqlite3.Connection,
    mode: CheckpointMode = "PASSIVE",
) -> SQLiteCheckpointResult:
    """Run a WAL checkpoint and return SQLite's live checkpoint counters."""

    normalized_mode = mode.upper()
    if normalized_mode not in {"PASSIVE", "FULL", "RESTART", "TRUNCATE"}:
        raise ValueError(f"unsupported SQLite checkpoint mode: {mode!r}")
    row = connection.execute(
        f"PRAGMA wal_checkpoint({normalized_mode})"
    ).fetchone()
    if row is None or len(row) != 3:
        raise SQLiteTuningError("SQLite WAL checkpoint returned an invalid result")
    return SQLiteCheckpointResult(
        mode=normalized_mode,  # type: ignore[arg-type]
        busy=int(row[0]),
        wal_frames=int(row[1]),
        checkpointed_frames=int(row[2]),
    )


class SQLiteBackgroundCheckpointer:
    """Periodically checkpoint a database using a dedicated SQLite connection."""

    def __init__(
        self,
        db_path: str | Path,
        config: SQLiteTuningConfig | None = None,
    ) -> None:
        self.db_path = Path(db_path)
        self.config = config or SQLiteTuningConfig()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_result: SQLiteCheckpointResult | None = None
        self._last_error: BaseException | None = None
        self._lock = threading.Lock()

    @property
    def last_result(self) -> SQLiteCheckpointResult | None:
        with self._lock:
            return self._last_result

    @property
    def last_error(self) -> BaseException | None:
        with self._lock:
            return self._last_error

    def start(self) -> None:
        """Start the background checkpoint worker once."""

        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run,
            name="cae-sqlite-wal-checkpointer",
            daemon=True,
        )
        self._thread.start()

    def stop(self, timeout: float | None = None) -> None:
        """Stop the worker and close its dedicated SQLite connection."""

        self._stop_event.set()
        thread = self._thread
        if thread is not None:
            thread.join(timeout)
            if thread.is_alive():
                raise SQLiteTuningError("background SQLite checkpointer did not stop")
        self._thread = None

    def __enter__(self) -> "SQLiteBackgroundCheckpointer":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop(timeout=max(1.0, self.config.checkpoint_interval_seconds * 2))

    def _run(self) -> None:
        connection: sqlite3.Connection | None = None
        try:
            while not self._stop_event.is_set():
                if connection is None:
                    try:
                        connection = open_sqlite_connection(
                            self.db_path,
                            self.config,
                            isolation_level="",
                        )
                    except (sqlite3.Error, SQLiteTuningError) as error:
                        with self._lock:
                            self._last_error = error
                        self._stop_event.wait(self.config.checkpoint_interval_seconds)
                        continue
                try:
                    result = checkpoint_sqlite(
                        connection,
                        self.config.checkpoint_mode,
                    )
                    with self._lock:
                        self._last_result = result
                        self._last_error = None
                except (sqlite3.Error, SQLiteTuningError) as error:
                    with self._lock:
                        self._last_error = error
                    if connection is not None:
                        connection.close()
                        connection = None
                self._stop_event.wait(self.config.checkpoint_interval_seconds)
        finally:
            if connection is not None:
                try:
                    connection.close()
                except sqlite3.Error:
                    pass
