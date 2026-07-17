from __future__ import annotations

from dataclasses import dataclass

from cmf_builder.skills.capsule_lifecycle import (
    CapsuleLifecycleError,
    CapsuleLifecycleReceipt,
    CapsuleState,
    InMemoryCapsuleLifecycle,
)
from cmf_builder.skills.jit_capsule import PhaseLocalJITCapsule


@dataclass(frozen=True, slots=True)
class CapsuleLifecycleCommand:
    command_id: str
    operation: str
    actor_id: str
    capsule: PhaseLocalJITCapsule | None = None
    capsule_id: str | None = None
    capsule_hash: str | None = None
    package_hash: str | None = None
    inject_failure: bool = False


@dataclass(frozen=True, slots=True)
class CapsuleLifecycleObservation:
    story_id: str
    event_name: str
    command_id: str
    operation: str
    actor_id: str
    artifact_identity: str | None
    outcome: str
    failure_context: dict[str, str]


class CapsuleLifecycleCommandService:
    STORY_ID = "ST-05.05"
    OPERATIONS = frozenset({"pin", "load", "verify", "activate", "dispose", "invalidate", "reproduce"})

    def __init__(self, *, authorized_actor_ids: tuple[str, ...]) -> None:
        self.lifecycle = InMemoryCapsuleLifecycle(authorized_actor_ids=authorized_actor_ids)
        self.observations: list[CapsuleLifecycleObservation] = []

    def execute(self, command: CapsuleLifecycleCommand) -> CapsuleLifecycleReceipt:
        try:
            if command.operation not in self.OPERATIONS:
                raise CapsuleLifecycleError("Unsupported capsule lifecycle operation.")
            if command.operation == "pin":
                if command.capsule is None:
                    raise CapsuleLifecycleError("Pin requires the exact immutable capsule.")
                receipt = self.lifecycle.pin(
                    command_id=command.command_id,
                    capsule=command.capsule,
                    actor_id=command.actor_id,
                    inject_failure=command.inject_failure,
                )
            else:
                if not command.capsule_id or command.capsule_hash is None or command.package_hash is None:
                    raise CapsuleLifecycleError("Lifecycle operations require exact capsule and package pins.")
                kwargs = {
                    "command_id": command.command_id,
                    "capsule_id": command.capsule_id,
                    "capsule_hash": command.capsule_hash,
                    "package_hash": command.package_hash,
                    "actor_id": command.actor_id,
                }
                if command.operation in {"verify", "activate", "dispose", "invalidate"}:
                    kwargs["inject_failure"] = command.inject_failure
                operation = getattr(self.lifecycle, "reproduce_historical" if command.operation == "reproduce" else command.operation)
                receipt = operation(**kwargs)
            self._observe(command, receipt.capsule_id, "PASS", {})
            return receipt
        except Exception as error:
            self._observe(
                command,
                command.capsule.capsule_id if command.capsule else command.capsule_id,
                "FAIL",
                {"code": type(error).__name__, "message": str(error)},
            )
            raise

    def _observe(self, command: CapsuleLifecycleCommand, artifact: str | None, outcome: str, failure: dict[str, str]) -> None:
        self.observations.append(
            CapsuleLifecycleObservation(
                story_id=self.STORY_ID,
                event_name=f"capsule_lifecycle_{'committed' if outcome == 'PASS' else 'rejected'}",
                command_id=command.command_id,
                operation=command.operation,
                actor_id=command.actor_id,
                artifact_identity=artifact,
                outcome=outcome,
                failure_context=failure,
            )
        )


__all__ = [
    "CapsuleLifecycleCommand",
    "CapsuleLifecycleCommandService",
    "CapsuleLifecycleError",
    "CapsuleLifecycleObservation",
    "CapsuleLifecycleReceipt",
    "CapsuleState",
    "InMemoryCapsuleLifecycle",
]
