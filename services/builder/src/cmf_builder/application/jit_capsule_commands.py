from __future__ import annotations

from dataclasses import dataclass, fields
from hashlib import sha256
import json

from cmf_builder.skills.jit_capsule import ContextRequirement, JITCapsuleError, PhaseLocalJITCapsule


@dataclass(frozen=True, slots=True)
class AssembleJITCapsuleCommand:
    command_id: str
    actor_id: str
    phase_id: str
    skill_id: str
    skill_version: str
    skill_package_hash: str
    minimum_context_ref: str
    minimum_context_hash: str
    requirements: tuple[ContextRequirement, ...]
    supplied_context_ids: tuple[str, ...]
    authority_refs: tuple[str, ...]
    input_contract_ref: str
    output_contract_ref: str
    acceptance_test_refs: tuple[str, ...]
    failure_and_stop_conditions: tuple[str, ...]
    observability_requirements: tuple[str, ...]
    rollback_requirements: tuple[str, ...]
    wrong_reading_locks: tuple[str, ...]
    semantic_lineage_refs: tuple[str, ...]
    evaluation_status: str


@dataclass(frozen=True, slots=True)
class JITCapsuleObservation:
    story_id: str
    event_name: str
    command_id: str
    actor_id: str
    phase_id: str
    artifact_identity: str | None
    outcome: str
    failure_context: dict[str, str]


class JITCapsuleCommandService:
    STORY_ID = "ST-05.04"

    def __init__(self, *, authorized_actor_ids: tuple[str, ...]) -> None:
        self._authorized = frozenset(authorized_actor_ids)
        self._commands: dict[str, tuple[str, PhaseLocalJITCapsule]] = {}
        self._capsules: dict[str, PhaseLocalJITCapsule] = {}
        self.observations: list[JITCapsuleObservation] = []

    def assemble(self, command: AssembleJITCapsuleCommand, *, inject_failure: bool = False) -> PhaseLocalJITCapsule:
        payload_hash = _command_hash(command)
        duplicate = self._commands.get(command.command_id)
        if duplicate:
            if duplicate[0] != payload_hash:
                self._reject(command, "CONFLICTING_COMMAND", "Command payload changed.")
            self._observe(command, duplicate[1], "jit_capsule_replayed", "PASS", {})
            return duplicate[1]
        if command.actor_id not in self._authorized:
            self._reject(command, "UNAUTHORIZED", "Actor lacks JIT capsule authority.")
        try:
            capsule = PhaseLocalJITCapsule.assemble(
                phase_id=command.phase_id,
                skill_id=command.skill_id,
                skill_version=command.skill_version,
                skill_package_hash=command.skill_package_hash,
                minimum_context_ref=command.minimum_context_ref,
                minimum_context_hash=command.minimum_context_hash,
                requirements=command.requirements,
                supplied_context_ids=command.supplied_context_ids,
                authority_refs=command.authority_refs,
                input_contract_ref=command.input_contract_ref,
                output_contract_ref=command.output_contract_ref,
                acceptance_test_refs=command.acceptance_test_refs,
                failure_and_stop_conditions=command.failure_and_stop_conditions,
                observability_requirements=command.observability_requirements,
                rollback_requirements=command.rollback_requirements,
                wrong_reading_locks=command.wrong_reading_locks,
                semantic_lineage_refs=command.semantic_lineage_refs,
                evaluation_status=command.evaluation_status,
            )
            if inject_failure:
                raise JITCapsuleError("Injected atomic JIT capsule failure.")
            self._capsules[capsule.capsule_id] = capsule
            self._commands[command.command_id] = (payload_hash, capsule)
            self._observe(command, capsule, "jit_capsule_committed", "PASS", {})
            return capsule
        except Exception as error:
            self._observe(
                command,
                None,
                "jit_capsule_rejected",
                "FAIL",
                {"code": type(error).__name__, "message": str(error)},
            )
            raise

    def get(self, capsule_id: str) -> PhaseLocalJITCapsule:
        capsule = self._capsules.get(capsule_id)
        if capsule is None:
            raise KeyError(capsule_id)
        capsule.canonical_dict()
        return capsule

    def invalidate(self, capsule_id: str) -> None:
        if capsule_id not in self._capsules:
            raise KeyError(capsule_id)
        del self._capsules[capsule_id]

    def _reject(self, command: AssembleJITCapsuleCommand, code: str, message: str) -> None:
        self._observe(command, None, "jit_capsule_rejected", "FAIL", {"code": code, "message": message})
        raise JITCapsuleError(message)

    def _observe(self, command: AssembleJITCapsuleCommand, capsule: PhaseLocalJITCapsule | None, event: str, outcome: str, failure: dict[str, str]) -> None:
        self.observations.append(
            JITCapsuleObservation(
                story_id=self.STORY_ID,
                event_name=event,
                command_id=command.command_id,
                actor_id=command.actor_id,
                phase_id=command.phase_id,
                artifact_identity=capsule.capsule_id if capsule else None,
                outcome=outcome,
                failure_context=failure,
            )
        )


def _command_hash(command: AssembleJITCapsuleCommand) -> str:
    payload = {
        name: (
            [item.canonical_dict() for item in value]
            if name == "requirements"
            else list(value)
            if isinstance(value, tuple)
            else value
        )
        for name, value in ((field.name, getattr(command, field.name)) for field in fields(command))
    }
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
