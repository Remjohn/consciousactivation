from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.format_profiles import (
    CompiledProfileRegistry,
    ProfileCompilationError,
    compile_structural_profile_registry,
)


class ProfileCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompileCategoryProfilesCommand:
    command_id: str
    registry_id: str
    registry_version: str
    category_registry_bytes: bytes
    compatibility_bytes: bytes
    conversational_registry_bytes: bytes
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class ProfileCompilationReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    command_payload_hash: str
    registry_id: str
    registry_version: str
    registry_hash: str
    outcome: str


@dataclass(frozen=True, slots=True)
class ProfileObservation:
    event_name: str
    outcome: str
    story_id: str
    command_id: str
    artifact_identity: str
    authority_identity: str
    version: str
    provenance: tuple[str, ...]
    correlation_id: str
    causation_id: str
    failure_context: str | None


class InMemoryProfileObservationSink:
    def __init__(self) -> None:
        self._items: list[ProfileObservation] = []

    @property
    def items(self) -> tuple[ProfileObservation, ...]:
        return tuple(self._items)

    def emit(self, item: ProfileObservation) -> None:
        self._items.append(item)


class InMemoryProfileRegistryRepository:
    def __init__(self) -> None:
        self._registries: dict[str, CompiledProfileRegistry] = {}
        self._receipts: dict[str, ProfileCompilationReceipt] = {}
        self._payload_hashes: dict[str, str] = {}
        self._fail_before_commit = False

    @property
    def registry_count(self) -> int:
        return len(self._registries)

    @property
    def receipt_count(self) -> int:
        return len(self._receipts)

    def inject_failure_before_commit(self) -> None:
        self._fail_before_commit = True

    def command_state(self, command_id: str) -> tuple[str, ProfileCompilationReceipt] | None:
        if command_id not in self._receipts:
            return None
        return self._payload_hashes[command_id], self._receipts[command_id]

    def commit(
        self,
        command: CompileCategoryProfilesCommand,
        payload_hash: str,
        registry: CompiledProfileRegistry,
        receipt: ProfileCompilationReceipt,
    ) -> None:
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise ProfileCommandRejected("Injected atomic profile registry commit failure.")
        existing = self._registries.get(command.registry_id)
        if existing is not None and existing.registry_hash != registry.registry_hash:
            raise ProfileCommandRejected(
                "An immutable profile registry identity already has different content."
            )
        self._registries[command.registry_id] = registry
        self._payload_hashes[command.command_id] = payload_hash
        self._receipts[command.command_id] = receipt


class ProfileCompilationService:
    def __init__(self, authority: AuthorityService, repository: InMemoryProfileRegistryRepository, observations: InMemoryProfileObservationSink) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def compile(self, command: CompileCategoryProfilesCommand) -> ProfileCompilationReceipt:
        payload_hash = _payload_hash(command)
        prior = self._repository.command_state(command.command_id)
        if prior is not None:
            prior_hash, prior_receipt = prior
            if prior_hash != payload_hash:
                self._reject(command, "Command identity was reused with a different payload.")
            self._observe(command, "ST-06.02:ProfileRegistryReplayReturned", "PASS", None)
            return prior_receipt
        try:
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.COMPILE_CATEGORY_PROFILES,
                resource_id=command.registry_id,
                now=command.now,
            )
            registry = compile_structural_profile_registry(
                category_registry_bytes=command.category_registry_bytes,
                compatibility_bytes=command.compatibility_bytes,
                conversational_registry_bytes=command.conversational_registry_bytes,
            )
            if command.registry_id != registry.registry_id or command.registry_version != registry.registry_version:
                raise ProfileCommandRejected("Command registry identity is not governed.")
            receipt = _receipt(command, payload_hash, registry)
            self._repository.commit(command, payload_hash, registry, receipt)
        except (AuthorityDenied, ProfileCompilationError, ProfileCommandRejected) as error:
            self._reject(command, str(error))
        self._observe(command, "ST-06.02:ProfileRegistryCompiled", "PASS", None)
        return receipt

    def _reject(self, command: CompileCategoryProfilesCommand, detail: str) -> None:
        self._observe(command, "ST-06.02:ProfileRegistryRejected", "FAIL", detail)
        raise ProfileCommandRejected(detail)

    def _observe(self, command: CompileCategoryProfilesCommand, event: str, outcome: str, failure: str | None) -> None:
        self._observations.emit(
            ProfileObservation(
                event_name=event,
                outcome=outcome,
                story_id="ST-06.02",
                command_id=command.command_id,
                artifact_identity=command.registry_id,
                authority_identity=command.actor_id,
                version=command.registry_version,
                provenance=("ST-06.01:StoryCompletionReceipt",),
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=failure,
            )
        )


def _payload_hash(command: CompileCategoryProfilesCommand) -> str:
    value = {
        "command_id": command.command_id,
        "registry_id": command.registry_id,
        "registry_version": command.registry_version,
        "category_registry_hash": sha256(command.category_registry_bytes).hexdigest(),
        "compatibility_hash": sha256(command.compatibility_bytes).hexdigest(),
        "conversational_registry_hash": sha256(command.conversational_registry_bytes).hexdigest(),
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
    }
    return f"sha256:{sha256(_canonical_json(value)).hexdigest()}"


def _receipt(command: CompileCategoryProfilesCommand, payload_hash: str, registry: CompiledProfileRegistry) -> ProfileCompilationReceipt:
    value = {
        "command_id": command.command_id,
        "command_payload_hash": payload_hash,
        "registry_id": registry.registry_id,
        "registry_version": registry.registry_version,
        "registry_hash": registry.registry_hash,
        "outcome": "STRUCTURAL_PROFILE_REGISTRY_COMPILED_UNCERTIFIED",
    }
    digest = sha256(_canonical_json(value)).hexdigest()
    return ProfileCompilationReceipt(
        receipt_id=f"profile-compilation-receipt_{digest}",
        receipt_hash=f"sha256:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        registry_id=registry.registry_id,
        registry_version=registry.registry_version,
        registry_hash=registry.registry_hash,
        outcome="STRUCTURAL_PROFILE_REGISTRY_COMPILED_UNCERTIFIED",
    )


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
