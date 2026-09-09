"""Persisted replay verification for CAE program-state executions.

CA-M044 / INV-REPL-001

This module is intentionally verification-only. It reopens the durable SQLite
store, reads the persisted transition/receipt/snapshot ledger, reconstructs
candidate state from explicitly persisted replay inputs (including cached
model completions), and compares each checkpoint with the durable snapshot.
It never writes to the authoritative store and never invokes a model.

The current CAE program-state transition table does not persist ``state_updates``
used by ``UniversalProgramStateRuntime.execute_transition``. Consequently a
run without an explicit persisted replay snapshot/input ledger is reported as
an evidence gap rather than reconstructed from in-memory/runtime defaults.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import sqlite3
from typing import Any, Callable, Iterable, Mapping, Optional, Sequence

from ca_contracts import canonical_sha256
from ca_runtime.merkle_receipt_chain import (
    MerkleReceiptChain,
    ReceiptChainIntegrityError,
)
from ca_runtime.program_state_runtime import (
    ProgramStateTransition,
    _compute_state_hash,
)


REPLAY_SCHEMA_VERSION = "cae.replay.v1"
REPLAY_SNAPSHOT_TABLE_CANDIDATES = (
    "cae_program_state_replay_snapshots",
    "cae_program_state_snapshots",
)


class ReplayVerificationError(RuntimeError):
    """Base error for replay verification failures."""


class ReplayEvidenceGap(ReplayVerificationError):
    """Raised when durable data is insufficient for deterministic replay."""


class ReplayTamperDetected(ReplayVerificationError):
    """Raised when persisted data fails an integrity check."""


@dataclass(frozen=True, slots=True)
class ReplayMismatch:
    """First divergence details, suitable for operator forensics."""

    reason_code: str
    version: Optional[int]
    transition_id: Optional[str]
    receipt_id: Optional[str]
    expected_fingerprint: Optional[str]
    recomputed_fingerprint: Optional[str]
    expected_state: Optional[Mapping[str, Any]]
    recomputed_state: Optional[Mapping[str, Any]]
    field_path: Optional[str]
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ReplayCheckpoint:
    """One durable snapshot checkpoint observed during verification."""

    version: int
    current_state: str
    state_data: Mapping[str, Any]
    state_hash: str
    lifecycle: Optional[str]
    last_receipt_id: Optional[str]


@dataclass(frozen=True, slots=True)
class ReplayStepResult:
    """Per-transition evidence for a successful prefix of the replay."""

    version: int
    transition_id: str
    receipt_id: str
    current_state: str
    state_hash: str
    model_cache_key: Optional[str]
    model_response_sha256: Optional[str]


@dataclass(frozen=True, slots=True)
class ReplayVerificationResult:
    """Structured CA-M044 verification outcome."""

    status: str
    invariant: str
    aggregate_id: str
    workspace_id: str
    cae_run_id: str
    program_id: str
    program_version: str
    verified_versions: tuple[int, ...]
    steps: tuple[ReplayStepResult, ...]
    mismatch: Optional[ReplayMismatch]
    limitations: tuple[str, ...]
    evidence_classes: tuple[str, ...]
    read_only: bool
    model_responses_verified: bool
    final_state_hash: Optional[str]
    persisted_final_state_hash: Optional[str]

    @property
    def passed(self) -> bool:
        return self.status == "PASS"

    @property
    def failed(self) -> bool:
        return self.status in {"FAIL", "EVIDENCE_GAP"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "invariant": self.invariant,
            "aggregate_id": self.aggregate_id,
            "workspace_id": self.workspace_id,
            "cae_run_id": self.cae_run_id,
            "program_id": self.program_id,
            "program_version": self.program_version,
            "verified_versions": list(self.verified_versions),
            "steps": [
                {
                    "version": step.version,
                    "transition_id": step.transition_id,
                    "receipt_id": step.receipt_id,
                    "current_state": step.current_state,
                    "state_hash": step.state_hash,
                    "model_cache_key": step.model_cache_key,
                    "model_response_sha256": step.model_response_sha256,
                }
                for step in self.steps
            ],
            "mismatch": None if self.mismatch is None else {
                "reason_code": self.mismatch.reason_code,
                "version": self.mismatch.version,
                "transition_id": self.mismatch.transition_id,
                "receipt_id": self.mismatch.receipt_id,
                "expected_fingerprint": self.mismatch.expected_fingerprint,
                "recomputed_fingerprint": self.mismatch.recomputed_fingerprint,
                "expected_state": self.mismatch.expected_state,
                "recomputed_state": self.mismatch.recomputed_state,
                "field_path": self.mismatch.field_path,
                "details": dict(self.mismatch.details),
            },
            "limitations": list(self.limitations),
            "evidence_classes": list(self.evidence_classes),
            "read_only": self.read_only,
            "model_responses_verified": self.model_responses_verified,
            "final_state_hash": self.final_state_hash,
            "persisted_final_state_hash": self.persisted_final_state_hash,
        }


ModelResponseCache = Mapping[str, Any] | Callable[[str], Any]
ReplayReducer = Callable[
    [Mapping[str, Any], ProgramStateTransition, Any],
    Mapping[str, Any],
]


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _parse_json(raw: Any, *, label: str) -> dict[str, Any]:
    if isinstance(raw, str):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ReplayTamperDetected(f"{label} contains invalid JSON") from exc
    else:
        value = raw
    if not isinstance(value, dict):
        raise ReplayTamperDetected(f"{label} must be a JSON object")
    return value


def _first_diff_path(left: Any, right: Any, path: str = "$") -> Optional[str]:
    if type(left) is not type(right):
        return path
    if isinstance(left, dict):
        keys = sorted(set(left) | set(right))
        for key in keys:
            if key not in left or key not in right:
                return f"{path}.{key}"
            nested = _first_diff_path(left[key], right[key], f"{path}.{key}")
            if nested:
                return nested
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}.length"
        for index, (a, b) in enumerate(zip(left, right)):
            nested = _first_diff_path(a, b, f"{path}[{index}]")
            if nested:
                return nested
        return None
    return None if left == right else path


def _resolve_model_response(cache: Optional[ModelResponseCache], key: str) -> Any:
    if cache is None:
        raise ReplayEvidenceGap(
            f"model completion cache entry {key!r} is required but no cache was supplied"
        )
    if callable(cache):
        try:
            return cache(key)
        except KeyError as exc:
            raise ReplayEvidenceGap(
                f"model completion cache entry {key!r} is missing"
            ) from exc
    if key not in cache:
        raise ReplayEvidenceGap(f"model completion cache entry {key!r} is missing")
    return cache[key]


def default_replay_reducer(
    state_data: Mapping[str, Any],
    transition: ProgramStateTransition,
    model_response: Any,
) -> Mapping[str, Any]:
    """Replay explicitly persisted state operations without inventing semantics.

    A transition may persist either:
    * ``payload.state_updates`` as the exact deterministic state mutation, or
    * ``payload.model_response_state_updates`` inside a cached model response.

    Any other transition shape is an evidence gap. This avoids guessing how a
    historical program implementation should have interpreted a generic event.
    """

    payload = dict(transition.payload)
    updates = payload.get("state_updates")
    if updates is None and isinstance(model_response, Mapping):
        updates = model_response.get("state_updates")
    if updates is None:
        raise ReplayEvidenceGap(
            f"transition {transition.transition_id!r} has no persisted deterministic state update"
        )
    if not isinstance(updates, Mapping):
        raise ReplayTamperDetected(
            f"transition {transition.transition_id!r} state_updates is not a JSON object"
        )
    next_state = dict(state_data)
    next_state.update(dict(updates))
    return next_state


def _open_connection(source: str | Path | sqlite3.Connection) -> tuple[sqlite3.Connection, bool]:
    if isinstance(source, sqlite3.Connection):
        connection = source
        connection.row_factory = sqlite3.Row
        return connection, False
    db_path = Path(source).resolve()
    connection = sqlite3.connect(f"file:{db_path.as_posix()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection, True


class PersistedReplayVerifier:
    """Read-only SQLite replay verifier for one CAE execution aggregate."""

    def __init__(
        self,
        *,
        db: str | Path | sqlite3.Connection,
        reducer: ReplayReducer = default_replay_reducer,
    ) -> None:
        self._db = db
        self._reducer = reducer

    def verify_run(
        self,
        *,
        aggregate_id: str,
        campaign_id: Optional[str] = None,
        model_response_cache: Optional[ModelResponseCache] = None,
    ) -> ReplayVerificationResult:
        connection, owns_connection = _open_connection(self._db)
        try:
            aggregate = connection.execute(
                "SELECT * FROM cae_program_state_aggregates WHERE aggregate_id = ?",
                (aggregate_id,),
            ).fetchone()
            if aggregate is None:
                raise ReplayEvidenceGap(f"aggregate {aggregate_id!r} is not persisted")

            transitions = self._load_transitions(connection, aggregate_id)
            snapshots, snapshot_table = self._load_snapshots(connection, aggregate_id)
            limitations: list[str] = []
            evidence_classes = {"EXECUTABLE", "TEST"}
            if snapshot_table is None:
                return self._gap_result(
                    aggregate,
                    "PERSISTED_SNAPSHOT_LEDGER_MISSING",
                    limitations=(
                        "Current repository state persists only the latest aggregate snapshot; "
                        "historical post-transition snapshots are not durable.",
                    ),
                )

            receipt_records = self._load_receipts(connection, aggregate, campaign_id)
            self._verify_transition_shape(transitions, int(aggregate["version"]))
            receipt_chain = self._verify_receipt_chain(
                receipt_records,
                aggregate=aggregate,
                campaign_id=campaign_id,
            )
            self._verify_receipt_bindings(transitions, receipt_records)
            _ = receipt_chain
            evidence_classes.add("SCHEMA")

            if not snapshots:
                raise ReplayEvidenceGap(
                    f"snapshot ledger {snapshot_table!r} contains no snapshots for aggregate {aggregate_id!r}"
                )

            snapshot_by_version = {item.version: item for item in snapshots}
            duplicate_versions = len(snapshot_by_version) != len(snapshots)
            if duplicate_versions:
                return self._failure_result(
                    aggregate,
                    ReplayMismatch(
                        reason_code="DUPLICATE_SNAPSHOT_VERSION",
                        version=None,
                        transition_id=None,
                        receipt_id=None,
                        expected_fingerprint=None,
                        recomputed_fingerprint=None,
                        expected_state=None,
                        recomputed_state=None,
                        field_path=None,
                        details={"aggregate_id": aggregate_id},
                    ),
                    limitations=tuple(limitations),
                    evidence_classes=evidence_classes,
                )

            initial_versions = sorted(snapshot_by_version)
            first_version = initial_versions[0]
            initial_snapshot = snapshot_by_version[first_version]
            initial_hash_recomputed = _compute_state_hash(
                aggregate_id=aggregate_id,
                program_id=str(aggregate["program_id"]),
                program_version=str(aggregate["program_version"]),
                current_state=initial_snapshot.current_state,
                version=initial_snapshot.version,
                state_data=dict(initial_snapshot.state_data),
            )
            if initial_snapshot.state_hash != initial_hash_recomputed:
                return self._failure_result(
                    aggregate,
                    ReplayMismatch(
                        reason_code="INITIAL_SNAPSHOT_TAMPER",
                        version=initial_snapshot.version,
                        transition_id=None,
                        receipt_id=initial_snapshot.last_receipt_id,
                        expected_fingerprint=initial_snapshot.state_hash,
                        recomputed_fingerprint=initial_hash_recomputed,
                        expected_state=initial_snapshot.state_data,
                        recomputed_state=None,
                        field_path="$.state_hash",
                        details={"snapshot_table": snapshot_table},
                    ),
                    limitations=tuple(limitations),
                    evidence_classes=evidence_classes,
                )
            state_data = dict(initial_snapshot.state_data)
            current_state = initial_snapshot.current_state
            current_version = initial_snapshot.version
            recomputed_hash = initial_hash_recomputed
            steps: list[ReplayStepResult] = []
            verified_versions: list[int] = [current_version]

            for transition in transitions:
                if transition.expected_version != current_version:
                    return self._failure_result(
                        aggregate,
                        ReplayMismatch(
                            reason_code="TRANSITION_VERSION_GAP",
                            version=transition.committed_version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            expected_fingerprint=None,
                            recomputed_fingerprint=None,
                            expected_state={"version": current_version},
                            recomputed_state={"version": transition.expected_version},
                            field_path="$.expected_version",
                            details={
                                "expected_version": current_version,
                                "recorded_expected_version": transition.expected_version,
                            },
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        limitations=tuple(limitations),
                        evidence_classes=evidence_classes,
                    )

                model_cache_key = self._model_cache_key(transition)
                model_response = None
                model_response_hash = None
                if model_cache_key is not None:
                    model_response = _resolve_model_response(model_response_cache, model_cache_key)
                    model_response_hash = canonical_sha256(model_response)
                    expected_cache_sha = transition.payload.get("model_response_sha256")
                    if expected_cache_sha is None:
                        return self._gap_result(
                            aggregate,
                            "REPLAY_INPUT_INCOMPLETE",
                            version=transition.committed_version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            limitations=tuple(limitations) + (
                                "A cached model completion must carry a persisted canonical SHA-256 fingerprint.",
                            ),
                            steps=steps,
                            verified_versions=verified_versions,
                            evidence_classes=evidence_classes,
                            model_responses_verified=False,
                        )
                    if expected_cache_sha != model_response_hash:
                        return self._failure_result(
                            aggregate,
                            ReplayMismatch(
                                reason_code="MODEL_RESPONSE_TAMPER",
                                version=transition.committed_version,
                                transition_id=transition.transition_id,
                                receipt_id=transition.receipt_id,
                                expected_fingerprint=str(expected_cache_sha),
                                recomputed_fingerprint=model_response_hash,
                                expected_state=None,
                                recomputed_state=None,
                                field_path="$.model_response_sha256",
                                details={"cache_key": model_cache_key},
                            ),
                            steps=steps,
                            verified_versions=verified_versions,
                            limitations=tuple(limitations),
                            evidence_classes=evidence_classes,
                            model_responses_verified=False,
                        )

                try:
                    next_state_data = dict(self._reducer(state_data, transition, model_response))
                except ReplayEvidenceGap as exc:
                    return self._gap_result(
                        aggregate,
                        "REPLAY_INPUT_INCOMPLETE",
                        version=transition.committed_version,
                        transition_id=transition.transition_id,
                        receipt_id=transition.receipt_id,
                        limitations=tuple(limitations) + (str(exc),),
                        steps=steps,
                        verified_versions=verified_versions,
                        evidence_classes=evidence_classes,
                    )

                next_version = transition.committed_version
                if next_version != current_version + 1:
                    return self._failure_result(
                        aggregate,
                        ReplayMismatch(
                            reason_code="NON_CONTIGUOUS_COMMITTED_VERSION",
                            version=next_version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            expected_fingerprint=None,
                            recomputed_fingerprint=None,
                            expected_state={"version": current_version + 1},
                            recomputed_state={"version": next_version},
                            field_path="$.committed_version",
                            details={"prior_version": current_version},
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        limitations=tuple(limitations),
                        evidence_classes=evidence_classes,
                    )

                current_state = transition.to_state
                current_version = next_version
                state_data = next_state_data
                recomputed_hash = _compute_state_hash(
                    aggregate_id=aggregate_id,
                    program_id=str(aggregate["program_id"]),
                    program_version=str(aggregate["program_version"]),
                    current_state=current_state,
                    version=current_version,
                    state_data=state_data,
                )
                expected_snapshot = snapshot_by_version.get(current_version)
                if expected_snapshot is None:
                    return self._gap_result(
                        aggregate,
                        "POST_TRANSITION_SNAPSHOT_MISSING",
                        version=current_version,
                        transition_id=transition.transition_id,
                        receipt_id=transition.receipt_id,
                        limitations=tuple(limitations) + (
                            "A historical snapshot is required for every accepted transition checkpoint.",
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        evidence_classes=evidence_classes,
                    )

                snapshot_hash_recomputed = _compute_state_hash(
                    aggregate_id=aggregate_id,
                    program_id=str(aggregate["program_id"]),
                    program_version=str(aggregate["program_version"]),
                    current_state=expected_snapshot.current_state,
                    version=expected_snapshot.version,
                    state_data=dict(expected_snapshot.state_data),
                )
                if expected_snapshot.state_hash != snapshot_hash_recomputed:
                    return self._failure_result(
                        aggregate,
                        ReplayMismatch(
                            reason_code="PERSISTED_SNAPSHOT_TAMPER",
                            version=expected_snapshot.version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            expected_fingerprint=expected_snapshot.state_hash,
                            recomputed_fingerprint=snapshot_hash_recomputed,
                            expected_state=expected_snapshot.state_data,
                            recomputed_state=None,
                            field_path="$.state_hash",
                            details={"snapshot_table": snapshot_table},
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        limitations=tuple(limitations),
                        evidence_classes=evidence_classes,
                    )

                if expected_snapshot.current_state != current_state or dict(expected_snapshot.state_data) != state_data:
                    field_path = _first_diff_path(
                        dict(expected_snapshot.state_data),
                        state_data,
                    )
                    return self._failure_result(
                        aggregate,
                        ReplayMismatch(
                            reason_code="STATE_PARITY_MISMATCH",
                            version=current_version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            expected_fingerprint=expected_snapshot.state_hash,
                            recomputed_fingerprint=recomputed_hash,
                            expected_state={
                                "current_state": expected_snapshot.current_state,
                                "state_data": expected_snapshot.state_data,
                            },
                            recomputed_state={
                                "current_state": current_state,
                                "state_data": state_data,
                            },
                            field_path=field_path or "$.current_state",
                            details={"snapshot_table": snapshot_table},
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        limitations=tuple(limitations),
                        evidence_classes=evidence_classes,
                    )

                if expected_snapshot.state_hash != recomputed_hash:
                    return self._failure_result(
                        aggregate,
                        ReplayMismatch(
                            reason_code="STATE_HASH_MISMATCH",
                            version=current_version,
                            transition_id=transition.transition_id,
                            receipt_id=transition.receipt_id,
                            expected_fingerprint=expected_snapshot.state_hash,
                            recomputed_fingerprint=recomputed_hash,
                            expected_state=expected_snapshot.state_data,
                            recomputed_state=state_data,
                            field_path="$.state_hash",
                            details={"snapshot_table": snapshot_table},
                        ),
                        steps=steps,
                        verified_versions=verified_versions,
                        limitations=tuple(limitations),
                        evidence_classes=evidence_classes,
                    )

                steps.append(
                    ReplayStepResult(
                        version=current_version,
                        transition_id=transition.transition_id,
                        receipt_id=transition.receipt_id,
                        current_state=current_state,
                        state_hash=recomputed_hash,
                        model_cache_key=model_cache_key,
                        model_response_sha256=model_response_hash,
                    )
                )
                verified_versions.append(current_version)

            final_persisted = self._aggregate_checkpoint(aggregate)
            if final_persisted.version != current_version:
                return self._failure_result(
                    aggregate,
                    ReplayMismatch(
                        reason_code="FINAL_VERSION_MISMATCH",
                        version=final_persisted.version,
                        transition_id=None,
                        receipt_id=final_persisted.last_receipt_id,
                        expected_fingerprint=str(final_persisted.version),
                        recomputed_fingerprint=str(current_version),
                        expected_state={"version": final_persisted.version},
                        recomputed_state={"version": current_version},
                        field_path="$.version",
                        details={},
                    ),
                    steps=steps,
                    verified_versions=verified_versions,
                    limitations=tuple(limitations),
                    evidence_classes=evidence_classes,
                )

            if final_persisted.current_state != current_state or dict(final_persisted.state_data) != state_data:
                return self._failure_result(
                    aggregate,
                    ReplayMismatch(
                        reason_code="FINAL_STATE_MISMATCH",
                        version=current_version,
                        transition_id=None,
                        receipt_id=final_persisted.last_receipt_id,
                        expected_fingerprint=final_persisted.state_hash,
                        recomputed_fingerprint=recomputed_hash,
                        expected_state={
                            "current_state": final_persisted.current_state,
                            "state_data": final_persisted.state_data,
                        },
                        recomputed_state={
                            "current_state": current_state,
                            "state_data": state_data,
                        },
                        field_path=_first_diff_path(
                            {
                                "current_state": final_persisted.current_state,
                                "state_data": final_persisted.state_data,
                            },
                            {
                                "current_state": current_state,
                                "state_data": state_data,
                            },
                        ),
                        details={},
                    ),
                    steps=steps,
                    verified_versions=verified_versions,
                    limitations=tuple(limitations),
                    evidence_classes=evidence_classes,
                )

            if final_persisted.state_hash != recomputed_hash:
                return self._failure_result(
                    aggregate,
                    ReplayMismatch(
                        reason_code="FINAL_STATE_HASH_MISMATCH",
                        version=current_version,
                        transition_id=None,
                        receipt_id=final_persisted.last_receipt_id,
                        expected_fingerprint=final_persisted.state_hash,
                        recomputed_fingerprint=recomputed_hash,
                        expected_state=final_persisted.state_data,
                        recomputed_state=state_data,
                        field_path="$.state_hash",
                        details={},
                    ),
                    steps=steps,
                    verified_versions=verified_versions,
                    limitations=tuple(limitations),
                    evidence_classes=evidence_classes,
                )

            limitations.append(
                "The verifier proves deterministic reconstitution from persisted replay inputs and snapshots; "
                "it does not prove external model/provider determinism beyond the supplied cached completions."
            )
            return ReplayVerificationResult(
                status="PASS",
                invariant="INV-REPL-001",
                aggregate_id=str(aggregate["aggregate_id"]),
                workspace_id=str(aggregate["workspace_id"]),
                cae_run_id=str(aggregate["cae_run_id"]),
                program_id=str(aggregate["program_id"]),
                program_version=str(aggregate["program_version"]),
                verified_versions=tuple(verified_versions),
                steps=tuple(steps),
                mismatch=None,
                limitations=tuple(limitations),
                evidence_classes=tuple(sorted(evidence_classes)),
                read_only=True,
                model_responses_verified=all(step.model_cache_key is None or step.model_response_sha256 is not None for step in steps),
                final_state_hash=recomputed_hash,
                persisted_final_state_hash=final_persisted.state_hash,
            )
        except ReplayEvidenceGap as exc:
            return self._gap_result(
                    aggregate,
                    "REPLAY_EVIDENCE_GAP",
                    limitations=(str(exc),),
                )
        except ReplayTamperDetected as exc:
            return self._failure_result(
                aggregate,
                ReplayMismatch(
                    reason_code="REPLAY_INPUT_TAMPER",
                    version=None,
                    transition_id=None,
                    receipt_id=None,
                    expected_fingerprint=None,
                    recomputed_fingerprint=None,
                    expected_state=None,
                    recomputed_state=None,
                    field_path=None,
                    details={"error": str(exc)},
                ),
                limitations=(),
                evidence_classes={"EXECUTABLE"},
            )
        except ReceiptChainIntegrityError as exc:
            return self._failure_result(
                aggregate,
                ReplayMismatch(
                    reason_code="RECEIPT_CHAIN_INTEGRITY_FAILURE",
                    version=None,
                    transition_id=None,
                    receipt_id=None,
                    expected_fingerprint=None,
                    recomputed_fingerprint=None,
                    expected_state=None,
                    recomputed_state=None,
                    field_path=None,
                    details={"error": str(exc)},
                ),
                limitations=(),
                evidence_classes={"EXECUTABLE"},
            )
        finally:
            if owns_connection:
                connection.close()

    def _load_transitions(
        self,
        connection: sqlite3.Connection,
        aggregate_id: str,
    ) -> list[ProgramStateTransition]:
        rows = connection.execute(
            "SELECT * FROM cae_program_state_transitions WHERE aggregate_id = ? ORDER BY committed_version ASC",
            (aggregate_id,),
        ).fetchall()
        transitions: list[ProgramStateTransition] = []
        for row in rows:
            transitions.append(
                ProgramStateTransition(
                    transition_id=str(row["transition_id"]),
                    aggregate_id=str(row["aggregate_id"]),
                    from_state=str(row["from_state"]),
                    to_state=str(row["to_state"]),
                    transition_name=str(row["transition_name"]),
                    trigger_operation=str(row["trigger_operation"]),
                    lane=row["lane"],
                    actor_id=str(row["actor_id"]),
                    payload=_parse_json(row["payload"], label=f"transition {row['transition_id']} payload"),
                    expected_version=int(row["expected_version"]),
                    committed_version=int(row["committed_version"]),
                    receipt_id=str(row["receipt_id"]),
                    timestamp=str(row["timestamp"]),
                )
            )
        # ProgramStateTransition expects an AuthorityLane object. Importing the enum
        # lazily keeps the reader code obvious without changing runtime authority.
        from ca_runtime.pi_adapter import AuthorityLane
        return [
            ProgramStateTransition(
                transition_id=t.transition_id,
                aggregate_id=t.aggregate_id,
                from_state=t.from_state,
                to_state=t.to_state,
                transition_name=t.transition_name,
                trigger_operation=t.trigger_operation,
                lane=AuthorityLane(t.lane),
                actor_id=t.actor_id,
                payload=t.payload,
                expected_version=t.expected_version,
                committed_version=t.committed_version,
                receipt_id=t.receipt_id,
                timestamp=t.timestamp,
            )
            for t in transitions
        ]

    def _load_snapshots(
        self,
        connection: sqlite3.Connection,
        aggregate_id: str,
    ) -> tuple[list[ReplayCheckpoint], Optional[str]]:
        for table in REPLAY_SNAPSHOT_TABLE_CANDIDATES:
            if not _table_exists(connection, table):
                continue
            rows = connection.execute(
                f"SELECT version, current_state, state_data, state_hash, lifecycle, last_receipt_id "
                f"FROM {table} WHERE aggregate_id = ? ORDER BY version ASC",
                (aggregate_id,),
            ).fetchall()
            snapshots = [
                ReplayCheckpoint(
                    version=int(row["version"]),
                    current_state=str(row["current_state"]),
                    state_data=_parse_json(row["state_data"], label=f"snapshot v{row['version']} state_data"),
                    state_hash=str(row["state_hash"]),
                    lifecycle=None if row["lifecycle"] is None else str(row["lifecycle"]),
                    last_receipt_id=None if row["last_receipt_id"] is None else str(row["last_receipt_id"]),
                )
                for row in rows
            ]
            return snapshots, table
        return [], None

    def _load_receipts(
        self,
        connection: sqlite3.Connection,
        aggregate: sqlite3.Row,
        campaign_id: Optional[str],
    ) -> list[dict[str, Any]]:
        table = "cae_merkle_receipts"
        if not _table_exists(connection, table):
            raise ReplayEvidenceGap("Q42 persisted receipt chain table is missing")
        rows = connection.execute(
            f"SELECT * FROM {table} WHERE workspace_id = ? AND execution_id = ? ORDER BY sequence ASC",
            (str(aggregate["workspace_id"]), str(aggregate["cae_run_id"])),
        ).fetchall()
        if not rows:
            raise ReplayEvidenceGap("Q42 persisted receipt chain is empty")
        resolved_campaign = campaign_id
        if resolved_campaign is None:
            resolved_campaign = str(rows[0]["campaign_id"])
        if any(str(row["campaign_id"]) != resolved_campaign for row in rows):
            raise ReplayTamperDetected("receipt chain crosses campaign boundaries")
        return [dict(row) for row in rows]

    @staticmethod
    def _verify_receipt_chain(
        records: Sequence[Mapping[str, Any]],
        *,
        aggregate: sqlite3.Row,
        campaign_id: Optional[str],
    ) -> MerkleReceiptChain:
        execution_id = str(aggregate["cae_run_id"])
        workspace_id = str(aggregate["workspace_id"])
        resolved_campaign = campaign_id or str(records[0]["campaign_id"])
        try:
            chain = MerkleReceiptChain.from_records(
                records,
                workspace_id=workspace_id,
                execution_id=execution_id,
                campaign_id=resolved_campaign,
            )
        except Exception as exc:  # Receipt module owns exact integrity classifications.
            raise ReceiptChainIntegrityError(str(exc)) from exc
        return chain

    @staticmethod
    def _verify_receipt_bindings(
        transitions: Sequence[ProgramStateTransition],
        records: Sequence[Mapping[str, Any]],
    ) -> None:
        by_receipt_id = {str(record["receipt_id"]): record for record in records}
        for transition in transitions:
            record = by_receipt_id.get(transition.receipt_id)
            if record is None:
                raise ReplayEvidenceGap(
                    f"persisted receipt {transition.receipt_id!r} for transition {transition.transition_id!r} is missing"
                )
            if str(record.get("kind")) != "STATE_TRANSITION":
                raise ReplayTamperDetected(
                    f"receipt {transition.receipt_id!r} is not a STATE_TRANSITION receipt"
                )
            if str(record.get("subject_id")) != transition.transition_id:
                raise ReplayTamperDetected(
                    f"receipt {transition.receipt_id!r} is bound to subject {record.get('subject_id')!r}, "
                    f"not transition {transition.transition_id!r}"
                )
            payload = record.get("payload")
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except json.JSONDecodeError as exc:
                    raise ReplayTamperDetected(
                        f"receipt {transition.receipt_id!r} payload contains invalid JSON"
                    ) from exc
            if not isinstance(payload, Mapping):
                raise ReplayTamperDetected(
                    f"receipt {transition.receipt_id!r} payload is not a JSON object"
                )
            expected = {
                "from_state": transition.from_state,
                "to_state": transition.to_state,
                "transition_name": transition.transition_name,
                "trigger_operation": transition.trigger_operation,
                "lane": transition.lane.value,
                "expected_version": transition.expected_version,
                "committed_version": transition.committed_version,
                "timestamp": transition.timestamp,
                "payload": dict(transition.payload),
            }
            for key, expected_value in expected.items():
                if payload.get(key) != expected_value:
                    raise ReplayTamperDetected(
                        f"receipt {transition.receipt_id!r} does not match transition field {key!r}"
                    )

    @staticmethod
    def _verify_transition_shape(
        transitions: Sequence[ProgramStateTransition],
        final_version: int,
    ) -> None:
        seen_ids: set[str] = set()
        seen_versions: set[int] = set()
        for index, transition in enumerate(transitions):
            if transition.transition_id in seen_ids:
                raise ReplayTamperDetected("duplicate transition_id in persisted ledger")
            seen_ids.add(transition.transition_id)
            if transition.committed_version in seen_versions:
                raise ReplayTamperDetected("duplicate committed_version in persisted ledger")
            seen_versions.add(transition.committed_version)
            if transition.expected_version >= transition.committed_version:
                raise ReplayTamperDetected(
                    f"transition {transition.transition_id!r} has non-incrementing versions"
                )
            if transition.from_state == transition.to_state and not transition.payload.get("state_updates"):
                # Same-state transitions are legal in principle; do not classify as an error.
                pass
        if transitions and transitions[-1].committed_version != final_version:
            raise ReplayEvidenceGap(
                f"transition ledger ends at version {transitions[-1].committed_version}, "
                f"but authoritative aggregate is at version {final_version}"
            )

    @staticmethod
    def _model_cache_key(transition: ProgramStateTransition) -> Optional[str]:
        raw = transition.payload.get("model_cache_key")
        return None if raw is None else str(raw)

    @staticmethod
    def _aggregate_checkpoint(row: sqlite3.Row) -> ReplayCheckpoint:
        return ReplayCheckpoint(
            version=int(row["version"]),
            current_state=str(row["current_state"]),
            state_data=_parse_json(row["state_data"], label="aggregate state_data"),
            state_hash=str(row["state_hash"]),
            lifecycle=None if row["lifecycle"] is None else str(row["lifecycle"]),
            last_receipt_id=None if row["last_receipt_id"] is None else str(row["last_receipt_id"]),
        )

    @staticmethod
    def _gap_result(
        aggregate: sqlite3.Row,
        reason_code: str,
        *,
        version: Optional[int] = None,
        transition_id: Optional[str] = None,
        receipt_id: Optional[str] = None,
        limitations: Sequence[str] = (),
        steps: Sequence[ReplayStepResult] = (),
        verified_versions: Sequence[int] = (),
        evidence_classes: Iterable[str] = ("EXECUTABLE",),
    ) -> ReplayVerificationResult:
        mismatch = ReplayMismatch(
            reason_code=reason_code,
            version=version,
            transition_id=transition_id,
            receipt_id=receipt_id,
            expected_fingerprint=None,
            recomputed_fingerprint=None,
            expected_state=None,
            recomputed_state=None,
            field_path=None,
            details={},
        )
        return ReplayVerificationResult(
            status="EVIDENCE_GAP",
            invariant="INV-REPL-001",
            aggregate_id=str(aggregate["aggregate_id"]),
            workspace_id=str(aggregate["workspace_id"]),
            cae_run_id=str(aggregate["cae_run_id"]),
            program_id=str(aggregate["program_id"]),
            program_version=str(aggregate["program_version"]),
            verified_versions=tuple(verified_versions),
            steps=tuple(steps),
            mismatch=mismatch,
            limitations=tuple(limitations),
            evidence_classes=tuple(sorted(set(evidence_classes))),
            read_only=True,
            model_responses_verified=False,
            final_state_hash=None,
            persisted_final_state_hash=str(aggregate["state_hash"]),
        )

    @staticmethod
    def _failure_result(
        aggregate: sqlite3.Row,
        mismatch: ReplayMismatch,
        *,
        steps: Sequence[ReplayStepResult] = (),
        verified_versions: Sequence[int] = (),
        limitations: Sequence[str] = (),
        evidence_classes: Iterable[str] = ("EXECUTABLE",),
        model_responses_verified: bool = True,
    ) -> ReplayVerificationResult:
        return ReplayVerificationResult(
            status="FAIL",
            invariant="INV-REPL-001",
            aggregate_id=str(aggregate["aggregate_id"]),
            workspace_id=str(aggregate["workspace_id"]),
            cae_run_id=str(aggregate["cae_run_id"]),
            program_id=str(aggregate["program_id"]),
            program_version=str(aggregate["program_version"]),
            verified_versions=tuple(verified_versions),
            steps=tuple(steps),
            mismatch=mismatch,
            limitations=tuple(limitations),
            evidence_classes=tuple(sorted(set(evidence_classes))),
            read_only=True,
            model_responses_verified=model_responses_verified,
            final_state_hash=None,
            persisted_final_state_hash=str(aggregate["state_hash"]),
        )


def replay_and_verify_run(
    db: str | Path | sqlite3.Connection,
    *,
    aggregate_id: str,
    campaign_id: Optional[str] = None,
    model_response_cache: Optional[ModelResponseCache] = None,
    reducer: ReplayReducer = default_replay_reducer,
) -> ReplayVerificationResult:
    """Reopen persisted storage and verify one execution run end-to-end.

    The same persisted source may be verified repeatedly; this function never
    issues INSERT/UPDATE/DELETE/DDL statements.
    """

    return PersistedReplayVerifier(db=db, reducer=reducer).verify_run(
        aggregate_id=aggregate_id,
        campaign_id=campaign_id,
        model_response_cache=model_response_cache,
    )


__all__ = [
    "ModelResponseCache",
    "PersistedReplayVerifier",
    "ReplayCheckpoint",
    "ReplayEvidenceGap",
    "ReplayMismatch",
    "ReplayReducer",
    "ReplayStepResult",
    "ReplayTamperDetected",
    "ReplayVerificationError",
    "ReplayVerificationResult",
    "default_replay_reducer",
    "replay_and_verify_run",
]
