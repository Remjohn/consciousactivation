from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
import json

from cmf_builder.skills.jit_capsule import JITCapsuleError, PhaseLocalJITCapsule


class CapsuleLifecycleError(ValueError):
    """A capsule lifecycle command is unauthorized, unpinned, or inconsistent."""


class CapsuleState(str, Enum):
    PINNED = "PINNED"
    VERIFIED = "VERIFIED"
    ACTIVE = "ACTIVE"
    DISPOSED = "DISPOSED"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True, slots=True)
class CapsuleLifecycleReceipt:
    receipt_id: str
    command_id: str
    operation: str
    capsule_id: str
    capsule_hash: str
    package_hash: str
    authority_id: str
    prior_state: str | None
    resulting_state: str
    replay_status: str
    historical_reproducible: bool
    receipt_hash: str

    @classmethod
    def create(
        cls,
        *,
        command_id: str,
        operation: str,
        capsule: PhaseLocalJITCapsule,
        authority_id: str,
        prior_state: CapsuleState | None,
        resulting_state: CapsuleState,
        replay_status: str = "NEW_COMMIT",
    ) -> "CapsuleLifecycleReceipt":
        payload = {
            "schema": "cmf-builder-capsule-lifecycle-receipt/v1",
            "command_id": command_id,
            "operation": operation,
            "capsule_id": capsule.capsule_id,
            "capsule_hash": capsule.capsule_hash,
            "package_hash": capsule.skill_package_hash,
            "authority_id": authority_id,
            "prior_state": prior_state.value if prior_state else None,
            "resulting_state": resulting_state.value,
            "replay_status": replay_status,
            "historical_reproducible": True,
        }
        digest = sha256(_canonical_bytes(payload)).hexdigest()
        return cls(
            receipt_id=f"capsule-lifecycle:{operation}:{digest[:24]}",
            command_id=command_id,
            operation=operation,
            capsule_id=capsule.capsule_id,
            capsule_hash=capsule.capsule_hash,
            package_hash=capsule.skill_package_hash,
            authority_id=authority_id,
            prior_state=payload["prior_state"],
            resulting_state=resulting_state.value,
            replay_status=replay_status,
            historical_reproducible=True,
            receipt_hash=digest,
        )


@dataclass(frozen=True, slots=True)
class _LifecycleRecord:
    capsule: PhaseLocalJITCapsule
    state: CapsuleState


class InMemoryCapsuleLifecycle:
    """Atomic, deterministic lifecycle for pinned phase-local capsules.

    This is a Builder-owned lifecycle model, not a provider execution runtime.
    Historical capsule bytes are retained after disposal or invalidation.
    """

    def __init__(self, *, authorized_actor_ids: tuple[str, ...]) -> None:
        if not authorized_actor_ids or any(not value.strip() for value in authorized_actor_ids):
            raise CapsuleLifecycleError("At least one explicit lifecycle authority is required.")
        self._authorized = frozenset(authorized_actor_ids)
        self._records: dict[str, _LifecycleRecord] = {}
        self._commands: dict[str, tuple[str, CapsuleLifecycleReceipt]] = {}

    def pin(self, *, command_id: str, capsule: PhaseLocalJITCapsule, actor_id: str, inject_failure: bool = False) -> CapsuleLifecycleReceipt:
        capsule.canonical_dict()
        replay = self._replay(command_id, "pin", capsule, actor_id)
        if replay is not None:
            return replay
        return self._transition(command_id, "pin", capsule, actor_id, None, CapsuleState.PINNED, inject_failure)

    def load(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "load", record.capsule, actor_id)
        if replay is not None:
            return replay
        if record.state in {CapsuleState.DISPOSED, CapsuleState.INVALIDATED}:
            raise CapsuleLifecycleError("Disposed or invalidated capsules cannot be loaded for use.")
        return self._transition(command_id, "load", record.capsule, actor_id, record.state, record.state, False)

    def verify(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str, inject_failure: bool = False) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "verify", record.capsule, actor_id)
        if replay is not None:
            return replay
        if record.state is not CapsuleState.PINNED:
            raise CapsuleLifecycleError("Only an exact pinned capsule may be verified.")
        record.capsule.canonical_dict()
        return self._transition(command_id, "verify", record.capsule, actor_id, record.state, CapsuleState.VERIFIED, inject_failure)

    def activate(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str, inject_failure: bool = False) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "activate", record.capsule, actor_id)
        if replay is not None:
            return replay
        if record.state is not CapsuleState.VERIFIED:
            raise CapsuleLifecycleError("No unverified, disposed, or invalidated capsule may activate.")
        return self._transition(command_id, "activate", record.capsule, actor_id, record.state, CapsuleState.ACTIVE, inject_failure)

    def dispose(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str, inject_failure: bool = False) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "dispose", record.capsule, actor_id)
        if replay is not None:
            return replay
        if record.state is not CapsuleState.ACTIVE:
            raise CapsuleLifecycleError("Only an active capsule may be safely disposed.")
        return self._transition(command_id, "dispose", record.capsule, actor_id, record.state, CapsuleState.DISPOSED, inject_failure)

    def invalidate(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str, inject_failure: bool = False) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "invalidate", record.capsule, actor_id)
        if replay is not None:
            return replay
        if record.state is CapsuleState.INVALIDATED:
            raise CapsuleLifecycleError("An invalidated capsule cannot be reused or invalidated again.")
        return self._transition(command_id, "invalidate", record.capsule, actor_id, record.state, CapsuleState.INVALIDATED, inject_failure)

    def reproduce_historical(self, *, command_id: str, capsule_id: str, capsule_hash: str, package_hash: str, actor_id: str) -> CapsuleLifecycleReceipt:
        record = self._require_exact(capsule_id, capsule_hash, package_hash)
        replay = self._replay(command_id, "reproduce", record.capsule, actor_id)
        if replay is not None:
            return replay
        record.capsule.canonical_dict()
        return self._transition(command_id, "reproduce", record.capsule, actor_id, record.state, record.state, False)

    def state_of(self, capsule_id: str) -> CapsuleState | None:
        record = self._records.get(capsule_id)
        return record.state if record else None

    def historical_capsule(self, capsule_id: str) -> PhaseLocalJITCapsule:
        record = self._records.get(capsule_id)
        if record is None:
            raise KeyError(capsule_id)
        record.capsule.canonical_dict()
        return record.capsule

    def _transition(
        self,
        command_id: str,
        operation: str,
        capsule: PhaseLocalJITCapsule,
        actor_id: str,
        prior: CapsuleState | None,
        result: CapsuleState,
        inject_failure: bool,
    ) -> CapsuleLifecycleReceipt:
        self._authorize(actor_id)
        payload = {
            "operation": operation,
            "capsule_id": capsule.capsule_id,
            "capsule_hash": capsule.capsule_hash,
            "package_hash": capsule.skill_package_hash,
            "actor_id": actor_id,
        }
        command_hash = sha256(_canonical_bytes(payload)).hexdigest()
        if inject_failure:
            raise CapsuleLifecycleError("Injected atomic lifecycle failure.")
        receipt = CapsuleLifecycleReceipt.create(
            command_id=command_id,
            operation=operation,
            capsule=capsule,
            authority_id=actor_id,
            prior_state=prior,
            resulting_state=result,
        )
        # State and command become visible together after every validation succeeds.
        self._records[capsule.capsule_id] = _LifecycleRecord(capsule=capsule, state=result)
        self._commands[command_id] = (command_hash, receipt)
        return receipt

    def _replay(
        self,
        command_id: str,
        operation: str,
        capsule: PhaseLocalJITCapsule,
        actor_id: str,
    ) -> CapsuleLifecycleReceipt | None:
        duplicate = self._commands.get(command_id)
        if duplicate is None:
            return None
        payload = {
            "operation": operation,
            "capsule_id": capsule.capsule_id,
            "capsule_hash": capsule.capsule_hash,
            "package_hash": capsule.skill_package_hash,
            "actor_id": actor_id,
        }
        if duplicate[0] != sha256(_canonical_bytes(payload)).hexdigest():
            raise CapsuleLifecycleError("Conflicting reuse of a lifecycle command id.")
        return duplicate[1]

    def _authorize(self, actor_id: str) -> None:
        if actor_id not in self._authorized:
            raise CapsuleLifecycleError("The actor lacks capsule lifecycle authority.")

    def _require_exact(self, capsule_id: str, capsule_hash: str, package_hash: str) -> _LifecycleRecord:
        if not capsule_hash or not package_hash:
            raise CapsuleLifecycleError("Unpinned capsule or package use is forbidden.")
        record = self._records.get(capsule_id)
        if record is None:
            raise CapsuleLifecycleError("The pinned capsule does not exist.")
        if record.capsule.capsule_hash != capsule_hash or record.capsule.skill_package_hash != package_hash:
            raise CapsuleLifecycleError("Capsule or package hash mismatch; silent upgrade is forbidden.")
        try:
            record.capsule.canonical_dict()
        except JITCapsuleError as error:
            raise CapsuleLifecycleError(str(error)) from error
        return record


def _canonical_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
