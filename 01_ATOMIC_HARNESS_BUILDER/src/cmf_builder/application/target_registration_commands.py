from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.compilation_targets import (
    CompilationTargetRegistry,
    TargetAuthorityRejected,
    TargetRegistryRejected,
    TargetSelectionRejected,
    TargetSelectionResult,
    TargetVersionConflict,
    select_compilation_target,
)


class TargetRegistrationCommandRejected(RuntimeError):
    pass


# ST-07.01 intentionally grants one bounded target-control capability because
# registration, selection and non-destructive rollback operate on one immutable
# registry aggregate. The scope does not authorize target compilation or any
# external product behavior.
REGISTER_COMPILATION_TARGETS_CAPABILITY_SCOPE = frozenset(
    {"register_registry", "select_target", "rollback_registry"}
)


@dataclass(frozen=True, slots=True)
class RegisterTargetRegistryCommand:
    command_id: str
    registry: CompilationTargetRegistry
    actor_id: str
    expected_active_registry_hash: str | None
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class SelectCompilationTargetCommand:
    command_id: str
    run_id: str
    requested_target_ids: tuple[str, ...]
    actor_id: str
    expected_active_registry_hash: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class RollbackTargetRegistryCommand:
    command_id: str
    registry_id: str
    target_registry_hash: str
    actor_id: str
    expected_active_registry_hash: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class TargetRegistryReceipt:
    receipt_id: str
    command_id: str
    command_payload_hash: str
    registry_id: str
    registry_version: str
    registry_hash: str
    authority_identity: str
    target_count: int
    external_compatibility: str
    outcome: str
    production_ready: bool = False
    certified: bool = False

    @property
    def receipt_hash(self) -> str:
        return f"sha256:{sha256(_canonical_json(self.canonical_dict())).hexdigest()}"

    def canonical_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "command_id": self.command_id,
            "command_payload_hash": self.command_payload_hash,
            "registry_id": self.registry_id,
            "registry_version": self.registry_version,
            "registry_hash": self.registry_hash,
            "authority_identity": self.authority_identity,
            "target_count": self.target_count,
            "external_compatibility": self.external_compatibility,
            "outcome": self.outcome,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }


@dataclass(frozen=True, slots=True)
class TargetRegistrationObservation:
    event_name: str
    outcome: str
    command_id: str
    registry_id: str
    registry_version: str
    artifact_identity: str
    authority_identity: str
    correlation_id: str
    causation_id: str
    failure_context: str | None


class InMemoryTargetObservationSink:
    def __init__(self) -> None:
        self._items: list[TargetRegistrationObservation] = []
        self._fail_next_emit = False

    @property
    def items(self) -> tuple[TargetRegistrationObservation, ...]:
        return tuple(self._items)

    def emit(self, observation: TargetRegistrationObservation) -> None:
        if self._fail_next_emit:
            self._fail_next_emit = False
            raise TargetRegistrationCommandRejected("Injected atomic target-observation failure.")
        self._items.append(observation)

    def inject_failure_before_emit(self) -> None:
        self._fail_next_emit = True

    def checkpoint(self) -> int:
        return len(self._items)

    def restore(self, checkpoint: int) -> None:
        del self._items[checkpoint:]


class InMemoryTargetRegistryRepository:
    def __init__(self) -> None:
        self._registries: dict[str, CompilationTargetRegistry] = {}
        self._active_by_id: dict[str, str] = {}
        self._payload_hashes: dict[str, str] = {}
        self._receipts: dict[str, TargetRegistryReceipt | TargetSelectionResult] = {}
        self._fail_before_commit = False

    def inject_failure_before_commit(self) -> None:
        self._fail_before_commit = True

    def command_state(
        self, command_id: str
    ) -> tuple[str, TargetRegistryReceipt | TargetSelectionResult] | None:
        if command_id not in self._receipts:
            return None
        return self._payload_hashes[command_id], self._receipts[command_id]

    def active(self, registry_id: str) -> CompilationTargetRegistry:
        try:
            return self._registries[self._active_by_id[registry_id]]
        except KeyError as error:
            raise TargetRegistrationCommandRejected("Active target registry does not exist.") from error

    def history(self, registry_id: str) -> tuple[CompilationTargetRegistry, ...]:
        return tuple(
            sorted(
                (item for item in self._registries.values() if item.registry_id == registry_id),
                key=lambda item: item.registry_hash,
            )
        )

    def commit_registry(
        self,
        *,
        command_id: str,
        payload_hash: str,
        registry: CompilationTargetRegistry,
        receipt: TargetRegistryReceipt,
        expected_active_registry_hash: str | None,
    ) -> None:
        current = self._active_by_id.get(registry.registry_id)
        if current == registry.registry_hash:
            existing = self._registries[current]
            if existing != registry:
                raise TargetVersionConflict("Registry identity conflicts with immutable content.")
            payloads = dict(self._payload_hashes)
            receipts = dict(self._receipts)
            payloads[command_id] = payload_hash
            receipts[command_id] = receipt
            if self._fail_before_commit:
                self._fail_before_commit = False
                raise TargetRegistrationCommandRejected("Injected atomic target-registry failure.")
            self._payload_hashes, self._receipts = payloads, receipts
            return
        if current != expected_active_registry_hash:
            raise TargetVersionConflict("Active target registry changed from the governed expectation.")
        existing = self._registries.get(registry.registry_hash)
        if existing is not None and existing != registry:
            raise TargetVersionConflict("Registry identity conflicts with immutable content.")
        registries = dict(self._registries)
        active = dict(self._active_by_id)
        payloads = dict(self._payload_hashes)
        receipts = dict(self._receipts)
        registries[registry.registry_hash] = registry
        active[registry.registry_id] = registry.registry_hash
        payloads[command_id] = payload_hash
        receipts[command_id] = receipt
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise TargetRegistrationCommandRejected("Injected atomic target-registry failure.")
        self._registries, self._active_by_id = registries, active
        self._payload_hashes, self._receipts = payloads, receipts

    def commit_selection(
        self, *, command_id: str, payload_hash: str, result: TargetSelectionResult
    ) -> None:
        payloads = dict(self._payload_hashes)
        receipts = dict(self._receipts)
        payloads[command_id] = payload_hash
        receipts[command_id] = result
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise TargetRegistrationCommandRejected("Injected atomic target-selection failure.")
        self._payload_hashes, self._receipts = payloads, receipts

    def rollback(
        self,
        *,
        command_id: str,
        payload_hash: str,
        registry_id: str,
        registry_hash: str,
        expected_active_registry_hash: str,
        receipt: TargetRegistryReceipt,
    ) -> CompilationTargetRegistry:
        target = self._registries.get(registry_hash)
        if target is None or target.registry_id != registry_id:
            raise TargetVersionConflict("Rollback target is not in the immutable registry history.")
        if self._active_by_id.get(registry_id) != expected_active_registry_hash:
            raise TargetVersionConflict("Active target registry changed from the rollback expectation.")
        active = dict(self._active_by_id)
        payloads = dict(self._payload_hashes)
        receipts = dict(self._receipts)
        active[registry_id] = registry_hash
        payloads[command_id] = payload_hash
        receipts[command_id] = receipt
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise TargetRegistrationCommandRejected("Injected atomic target-registry rollback failure.")
        self._active_by_id = active
        self._payload_hashes, self._receipts = payloads, receipts
        return target


class CompilationTargetService:
    def __init__(
        self,
        authority: AuthorityService,
        repository: InMemoryTargetRegistryRepository,
        observations: InMemoryTargetObservationSink,
    ) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def register(self, command: RegisterTargetRegistryCommand) -> TargetRegistryReceipt:
        payload_hash = _register_payload_hash(command)
        prior = self._replay(command.command_id, payload_hash)
        if prior is not None:
            if not isinstance(prior, TargetRegistryReceipt):
                raise TargetRegistrationCommandRejected("Command identity belongs to another result type.")
            try:
                self._observe_register(command, "ST-07.01:TargetRegistryReplayReturned", "PASS", None)
            except TargetRegistrationCommandRejected:
                # The durable command result is authoritative on replay. A
                # retryable observation outage must not turn committed success
                # into a false command failure.
                pass
            return prior
        try:
            self._authorize(command.actor_id, command.registry.registry_id, command.now)
            if command.actor_id != command.registry.authority_ref.authority:
                raise TargetAuthorityRejected(
                    "Registry authority evidence does not identify the acting actor."
                )
            receipt = _registry_receipt(command, payload_hash)
            observation_checkpoint = self._observations.checkpoint()
            self._observe_register(command, "ST-07.01:TargetRegistryRegistered", "PASS", None)
            self._repository.commit_registry(
                command_id=command.command_id,
                payload_hash=payload_hash,
                registry=command.registry,
                receipt=receipt,
                expected_active_registry_hash=command.expected_active_registry_hash,
            )
        except (
            AuthorityDenied,
            TargetAuthorityRejected,
            TargetRegistryRejected,
            TargetVersionConflict,
            TargetRegistrationCommandRejected,
        ) as error:
            if "observation_checkpoint" in locals():
                self._observations.restore(observation_checkpoint)
            self._observe_register(command, "ST-07.01:TargetRegistryRejected", "FAIL", str(error))
            raise TargetRegistrationCommandRejected(str(error)) from error
        return receipt

    def select(self, command: SelectCompilationTargetCommand) -> TargetSelectionResult:
        payload_hash = _selection_payload_hash(command)
        prior = self._replay(command.command_id, payload_hash)
        if prior is not None:
            if not isinstance(prior, TargetSelectionResult):
                raise TargetRegistrationCommandRejected("Command identity belongs to another result type.")
            try:
                self._observe_selection(
                    command, "ST-07.01:TargetSelectionReplayReturned", "PASS", prior.selection.selection_hash, None
                )
            except TargetRegistrationCommandRejected:
                # Preserve the already committed result under degraded
                # replay-only observability.
                pass
            return prior
        try:
            registry = self._repository.active("compilation-target-registry")
            if registry.registry_hash != command.expected_active_registry_hash:
                raise TargetVersionConflict(
                    "Active target registry changed from the selection expectation."
                )
            self._authorize(command.actor_id, registry.registry_id, command.now)
            result = select_compilation_target(
                run_id=command.run_id,
                registry=registry,
                requested_target_ids=command.requested_target_ids,
                actor_id=command.actor_id,
            )
            observation_checkpoint = self._observations.checkpoint()
            self._observe_selection(
                command, "ST-07.01:TargetSelectionAccepted", "PASS", result.selection.selection_hash, None
            )
            self._repository.commit_selection(
                command_id=command.command_id, payload_hash=payload_hash, result=result
            )
        except (
            AuthorityDenied,
            TargetAuthorityRejected,
            TargetSelectionRejected,
            TargetVersionConflict,
            TargetRegistrationCommandRejected,
        ) as error:
            if "observation_checkpoint" in locals():
                self._observations.restore(observation_checkpoint)
            self._observe_selection(
                command, "ST-07.01:TargetSelectionRejected", "FAIL", command.command_id, str(error)
            )
            raise TargetRegistrationCommandRejected(str(error)) from error
        return result

    def rollback(self, command: RollbackTargetRegistryCommand) -> TargetRegistryReceipt:
        payload_hash = _rollback_payload_hash(command)
        prior = self._replay(command.command_id, payload_hash)
        if prior is not None:
            if not isinstance(prior, TargetRegistryReceipt):
                raise TargetRegistrationCommandRejected("Command identity belongs to another result type.")
            return prior
        try:
            current = self._repository.active(command.registry_id)
            self._authorize(command.actor_id, command.registry_id, command.now)
            target = next(
                (
                    item
                    for item in self._repository.history(command.registry_id)
                    if item.registry_hash == command.target_registry_hash
                ),
                None,
            )
            if target is None:
                raise TargetVersionConflict("Rollback target is not in the immutable registry history.")
            if command.actor_id != target.authority_ref.authority:
                raise TargetAuthorityRejected("Rollback actor is not the governed registry authority.")
            receipt = _rollback_receipt(command, payload_hash, target)
            observation_checkpoint = self._observations.checkpoint()
            success_observation = TargetRegistrationObservation(
                event_name="ST-07.01:TargetRegistryRolledBack",
                outcome="PASS",
                command_id=command.command_id,
                registry_id=command.registry_id,
                registry_version=target.registry_version,
                artifact_identity=target.registry_hash,
                authority_identity=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=None,
            )
            self._observations.emit(success_observation)
            self._repository.rollback(
                command_id=command.command_id,
                payload_hash=payload_hash,
                registry_id=command.registry_id,
                registry_hash=command.target_registry_hash,
                expected_active_registry_hash=command.expected_active_registry_hash,
                receipt=receipt,
            )
        except (
            AuthorityDenied,
            TargetAuthorityRejected,
            TargetVersionConflict,
            TargetRegistrationCommandRejected,
        ) as error:
            if "observation_checkpoint" in locals():
                self._observations.restore(observation_checkpoint)
            self._observations.emit(
                TargetRegistrationObservation(
                    event_name="ST-07.01:TargetRegistryRollbackRejected",
                    outcome="FAIL",
                    command_id=command.command_id,
                    registry_id=command.registry_id,
                    registry_version=current.registry_version if "current" in locals() else "NOT_AVAILABLE",
                    artifact_identity=command.target_registry_hash,
                    authority_identity=command.actor_id,
                    correlation_id=command.correlation_id,
                    causation_id=command.causation_id,
                    failure_context=str(error),
                )
            )
            raise TargetRegistrationCommandRejected(str(error)) from error
        return receipt

    def _authorize(self, actor_id: str, resource_id: str, now: datetime) -> None:
        self._authority.authorize(
            actor_id=actor_id,
            action=Action.REGISTER_COMPILATION_TARGETS,
            resource_id=resource_id,
            now=now,
        )

    def _replay(
        self, command_id: str, payload_hash: str
    ) -> TargetRegistryReceipt | TargetSelectionResult | None:
        prior = self._repository.command_state(command_id)
        if prior is None:
            return None
        prior_hash, result = prior
        if prior_hash != payload_hash:
            raise TargetRegistrationCommandRejected(
                "Command identity was reused with a different payload."
            )
        return result

    def _observe_register(
        self,
        command: RegisterTargetRegistryCommand,
        event_name: str,
        outcome: str,
        failure: str | None,
    ) -> None:
        self._observations.emit(
            TargetRegistrationObservation(
                event_name=event_name,
                outcome=outcome,
                command_id=command.command_id,
                registry_id=command.registry.registry_id,
                registry_version=command.registry.registry_version,
                artifact_identity=command.registry.registry_hash,
                authority_identity=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )

    def _observe_selection(
        self,
        command: SelectCompilationTargetCommand,
        event_name: str,
        outcome: str,
        artifact_identity: str,
        failure: str | None,
    ) -> None:
        self._observations.emit(
            TargetRegistrationObservation(
                event_name=event_name,
                outcome=outcome,
                command_id=command.command_id,
                registry_id="compilation-target-registry",
                registry_version="ACTIVE_OR_NOT_AVAILABLE",
                artifact_identity=artifact_identity,
                authority_identity=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )


def _registry_receipt(
    command: RegisterTargetRegistryCommand, payload_hash: str
) -> TargetRegistryReceipt:
    registry = command.registry
    digest = sha256(
        _canonical_json(
            {
                "command_id": command.command_id,
                "command_payload_hash": payload_hash,
                "registry_hash": registry.registry_hash,
                "authority_identity": command.actor_id,
                "target_count": len(registry.profiles),
                "external_compatibility": "EXTERNAL_VALIDATION_PENDING",
                "outcome": "OUTCOME_VERIFIED",
                "production_ready": False,
                "certified": False,
            }
        )
    ).hexdigest()
    return TargetRegistryReceipt(
        receipt_id=f"ST-07.01:TargetRegistry:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        registry_id=registry.registry_id,
        registry_version=registry.registry_version,
        registry_hash=registry.registry_hash,
        authority_identity=command.actor_id,
        target_count=len(registry.profiles),
        external_compatibility="EXTERNAL_VALIDATION_PENDING",
        outcome="OUTCOME_VERIFIED",
    )


def _rollback_receipt(
    command: RollbackTargetRegistryCommand,
    payload_hash: str,
    target: CompilationTargetRegistry,
) -> TargetRegistryReceipt:
    digest = sha256(
        _canonical_json(
            {
                "command_id": command.command_id,
                "command_payload_hash": payload_hash,
                "registry_hash": target.registry_hash,
                "authority_identity": command.actor_id,
                "outcome": "ROLLBACK_VERIFIED",
            }
        )
    ).hexdigest()
    return TargetRegistryReceipt(
        receipt_id=f"ST-07.01:TargetRegistryRollback:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        registry_id=target.registry_id,
        registry_version=target.registry_version,
        registry_hash=target.registry_hash,
        authority_identity=command.actor_id,
        target_count=len(target.profiles),
        external_compatibility="EXTERNAL_VALIDATION_PENDING",
        outcome="ROLLBACK_VERIFIED",
    )


def _register_payload_hash(command: RegisterTargetRegistryCommand) -> str:
    return f"sha256:{sha256(_canonical_json({'kind': 'register', 'command_id': command.command_id, 'registry': command.registry.canonical_dict(), 'actor_id': command.actor_id, 'expected_active_registry_hash': command.expected_active_registry_hash, 'now': command.now.isoformat(), 'correlation_id': command.correlation_id, 'causation_id': command.causation_id})).hexdigest()}"


def _selection_payload_hash(command: SelectCompilationTargetCommand) -> str:
    return f"sha256:{sha256(_canonical_json({'kind': 'select', 'command_id': command.command_id, 'run_id': command.run_id, 'requested_target_ids': list(command.requested_target_ids), 'actor_id': command.actor_id, 'expected_active_registry_hash': command.expected_active_registry_hash, 'now': command.now.isoformat(), 'correlation_id': command.correlation_id, 'causation_id': command.causation_id})).hexdigest()}"


def _rollback_payload_hash(command: RollbackTargetRegistryCommand) -> str:
    return f"sha256:{sha256(_canonical_json({'kind': 'rollback', 'command_id': command.command_id, 'registry_id': command.registry_id, 'target_registry_hash': command.target_registry_hash, 'actor_id': command.actor_id, 'expected_active_registry_hash': command.expected_active_registry_hash, 'now': command.now.isoformat(), 'correlation_id': command.correlation_id, 'causation_id': command.causation_id})).hexdigest()}"


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")
