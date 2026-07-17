from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Mapping

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.category_binding import CategoryBinding, CategoryBindingError


class CategoryBindingCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class BindHarnessCategoryCommand:
    command_id: str
    harness_id: str
    harness_version: str
    mode: str
    category_ids: tuple[str, ...]
    activative_input: Mapping[str, object] | None
    registry_bytes: bytes
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class CategoryBindingReceipt:
    receipt_id: str
    receipt_hash: str
    command_id: str
    command_payload_hash: str
    binding_hash: str
    harness_id: str
    harness_version: str
    category_id: str | None
    outcome: str


@dataclass(frozen=True, slots=True)
class CategoryBindingObservation:
    event_name: str
    outcome: str
    command_id: str
    harness_id: str
    correlation_id: str
    causation_id: str
    detail: str


class InMemoryCategoryObservationSink:
    def __init__(self) -> None:
        self._items: list[CategoryBindingObservation] = []

    @property
    def items(self) -> tuple[CategoryBindingObservation, ...]:
        return tuple(self._items)

    def emit(self, observation: CategoryBindingObservation) -> None:
        self._items.append(observation)


class InMemoryCategoryBindingRepository:
    def __init__(self) -> None:
        self._bindings: dict[str, CategoryBinding] = {}
        self._receipts: dict[str, CategoryBindingReceipt] = {}
        self._command_payloads: dict[str, str] = {}
        self._fail_before_commit = False

    @property
    def binding_count(self) -> int:
        return len(self._bindings)

    @property
    def receipt_count(self) -> int:
        return len(self._receipts)

    def inject_failure_before_commit(self) -> None:
        self._fail_before_commit = True

    def command_state(
        self, command_id: str
    ) -> tuple[str, CategoryBindingReceipt] | None:
        receipt = self._receipts.get(command_id)
        payload_hash = self._command_payloads.get(command_id)
        if receipt is None or payload_hash is None:
            return None
        return payload_hash, receipt

    def commit(
        self,
        *,
        command_id: str,
        command_payload_hash: str,
        binding: CategoryBinding,
        receipt: CategoryBindingReceipt,
    ) -> None:
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise CategoryBindingCommandRejected("Injected atomic category commit failure.")
        binding_key = f"{binding.harness_id}@{binding.harness_version}"
        existing = self._bindings.get(binding_key)
        if existing is not None and existing != binding:
            raise CategoryBindingCommandRejected(
                "An immutable Harness version already has a different category binding."
            )
        # All validation precedes these writes; in-memory assignment cannot expose a
        # partial state between them to a repository caller.
        self._bindings[binding_key] = binding
        self._command_payloads[command_id] = command_payload_hash
        self._receipts[command_id] = receipt


class CategoryBindingService:
    def __init__(
        self,
        authority: AuthorityService,
        repository: InMemoryCategoryBindingRepository,
        observations: InMemoryCategoryObservationSink,
    ) -> None:
        self._authority = authority
        self._repository = repository
        self._observations = observations

    def bind(self, command: BindHarnessCategoryCommand) -> CategoryBindingReceipt:
        payload_hash = _command_payload_hash(command)
        prior = self._repository.command_state(command.command_id)
        if prior is not None:
            prior_payload_hash, prior_receipt = prior
            if prior_payload_hash != payload_hash:
                self._reject(command, "Command identity was reused with a different payload.")
            self._observe(
                command,
                event_name="ST-06.01:CategoryBindingReplayReturned",
                outcome="PASS",
                detail="Original immutable receipt returned without duplicate state.",
            )
            return prior_receipt
        try:
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.BIND_HARNESS_CATEGORY,
                resource_id=command.harness_id,
                now=command.now,
            )
            binding = CategoryBinding.create(
                harness_id=command.harness_id,
                harness_version=command.harness_version,
                mode=command.mode,
                category_ids=command.category_ids,
                activative_input=command.activative_input,
                registry_bytes=command.registry_bytes,
            )
            receipt = _receipt(command, payload_hash, binding)
            self._repository.commit(
                command_id=command.command_id,
                command_payload_hash=payload_hash,
                binding=binding,
                receipt=receipt,
            )
        except (AuthorityDenied, CategoryBindingError, CategoryBindingCommandRejected) as error:
            self._reject(command, str(error))
        self._observe(
            command,
            event_name="ST-06.01:CategoryBindingCommitted",
            outcome="PASS",
            detail="Immutable structural category binding and receipt committed.",
        )
        return receipt

    def _reject(self, command: BindHarnessCategoryCommand, detail: str) -> None:
        self._observe(
            command,
            event_name="ST-06.01:CategoryBindingRejected",
            outcome="FAIL",
            detail=detail,
        )
        raise CategoryBindingCommandRejected(detail)

    def _observe(
        self,
        command: BindHarnessCategoryCommand,
        *,
        event_name: str,
        outcome: str,
        detail: str,
    ) -> None:
        self._observations.emit(
            CategoryBindingObservation(
                event_name=event_name,
                outcome=outcome,
                command_id=command.command_id,
                harness_id=command.harness_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                detail=detail,
            )
        )


def _command_payload_hash(command: BindHarnessCategoryCommand) -> str:
    value = {
        "command_id": command.command_id,
        "harness_id": command.harness_id,
        "harness_version": command.harness_version,
        "mode": command.mode,
        "category_ids": list(command.category_ids),
        "activative_input": command.activative_input,
        "registry_hash": f"sha256:{sha256(command.registry_bytes).hexdigest()}",
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
    }
    return f"sha256:{sha256(_canonical_json(value)).hexdigest()}"


def _receipt(
    command: BindHarnessCategoryCommand,
    payload_hash: str,
    binding: CategoryBinding,
) -> CategoryBindingReceipt:
    values = {
        "schema_version": "cmf-builder-category-binding-receipt/v1",
        "command_id": command.command_id,
        "command_payload_hash": payload_hash,
        "binding_hash": binding.binding_hash,
        "harness_id": binding.harness_id,
        "harness_version": binding.harness_version,
        "category_id": binding.category_id,
        "outcome": "STRUCTURAL_CATEGORY_BOUND_UNCERTIFIED",
    }
    digest = sha256(_canonical_json(values)).hexdigest()
    return CategoryBindingReceipt(
        receipt_id=f"category-binding-receipt_{digest}",
        receipt_hash=f"sha256:{digest}",
        command_id=command.command_id,
        command_payload_hash=payload_hash,
        binding_hash=binding.binding_hash,
        harness_id=binding.harness_id,
        harness_version=binding.harness_version,
        category_id=binding.category_id,
        outcome="STRUCTURAL_CATEGORY_BOUND_UNCERTIFIED",
    )


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
