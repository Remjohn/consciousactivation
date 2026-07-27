from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
from typing import Protocol

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService
from cmf_builder.domain.external_handoff_contracts import (
    DELEGATION_TARGET,
    EXTERNAL_VALIDATION_PENDING,
    LOCAL_TEST_DOUBLE_ONLY,
    VAE_TARGET,
    CompiledExternalHandoffRequest,
    ExternalHandoffInput,
    HandoffAuthorityRejected,
    HandoffContractRejected,
    LocalCompatibilityValidationReceipt,
    compile_external_handoff,
    validate_local_contract,
)


class ExternalHandoffCommandRejected(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class CompileExternalHandoffCommand:
    command_id: str
    handoff_input: ExternalHandoffInput
    actor_id: str
    now: datetime
    correlation_id: str
    causation_id: str


@dataclass(frozen=True, slots=True)
class LocalHandoffAcknowledgement:
    acknowledgement_id: str
    request_identity: str
    target_identity: str
    acknowledged_contract_version: str
    acknowledged_payload_hash: str
    test_double_identity: str
    authority_identity: str
    outcome: str
    failure_context: str
    authority: str = LOCAL_TEST_DOUBLE_ONLY
    external_acceptance: bool = False

    def __post_init__(self) -> None:
        if self.target_identity not in {VAE_TARGET, DELEGATION_TARGET}:
            raise HandoffContractRejected("Local acknowledgement target is not governed.")
        if self.authority != LOCAL_TEST_DOUBLE_ONLY or self.external_acceptance:
            raise HandoffAuthorityRejected("Local test-double acknowledgement is not external acceptance.")
        if self.outcome != "ACKNOWLEDGED_BY_LOCAL_TEST_DOUBLE" or self.failure_context != "NONE":
            raise HandoffContractRejected("Local acknowledgement has an unsupported outcome.")
        if self.request_identity != self.acknowledged_payload_hash:
            raise HandoffContractRejected("Local acknowledgement payload does not match the request.")
        if self.target_identity == DELEGATION_TARGET:
            if (
                self.acknowledged_contract_version != "1.1.0-rc.4"
                or self.test_double_identity != "local-delegation-rc4-fixture-port/v1"
            ):
                raise HandoffContractRejected("Delegation acknowledgement is not bound to the RC4 local fixture.")
        elif (
            self.acknowledged_contract_version != "builder-local-vae-interface/v1"
            or self.test_double_identity != "local-vae-fixture-port/v1"
        ):
            raise HandoffContractRejected("VAE acknowledgement is not bound to its local fixture.")
        expected = f"ST-07.03:LocalAck:{sha256(_canonical_json(self.identity_dict())).hexdigest()}"
        if self.acknowledgement_id != expected:
            raise HandoffContractRejected("Local acknowledgement identity is not deterministic.")

    def identity_dict(self) -> dict[str, object]:
        return {
            "request_identity": self.request_identity,
            "target_identity": self.target_identity,
            "acknowledged_contract_version": self.acknowledged_contract_version,
            "acknowledged_payload_hash": self.acknowledged_payload_hash,
            "test_double_identity": self.test_double_identity,
            "authority_identity": self.authority_identity,
            "outcome": self.outcome,
            "failure_context": self.failure_context,
            "authority": self.authority,
            "external_acceptance": self.external_acceptance,
        }


@dataclass(frozen=True, slots=True)
class LocalExternalResultEnvelope:
    request_identity: str
    target_identity: str
    status: str
    result_hash: str | None
    error_code: str | None
    reconciliation_required: bool
    external_result_received: bool = False

    def __post_init__(self) -> None:
        if self.target_identity not in {VAE_TARGET, DELEGATION_TARGET}:
            raise HandoffContractRejected("Local result target is not governed.")
        if not self.request_identity.startswith("sha256:") or len(self.request_identity) != 71:
            raise HandoffContractRejected("Local result request identity is invalid.")
        if self.status not in {"LOCAL_ACKNOWLEDGED", "LOCAL_REJECTED", "LOCAL_PARTIAL"}:
            raise HandoffContractRejected("External result boundary has an unsupported local status.")
        if self.external_result_received:
            raise HandoffAuthorityRejected("ST-07.03 cannot claim receipt of an external product result.")
        if self.status == "LOCAL_ACKNOWLEDGED" and (self.result_hash is None or self.error_code is not None):
            raise HandoffContractRejected("Acknowledged local result must be hash-bound and error-free.")
        if self.result_hash is not None and (
            not self.result_hash.startswith("sha256:") or len(self.result_hash) != 71
        ):
            raise HandoffContractRejected("Local result hash is invalid.")
        if self.status == "LOCAL_ACKNOWLEDGED" and self.reconciliation_required:
            raise HandoffContractRejected("Acknowledged local result cannot require reconciliation.")
        if self.status != "LOCAL_ACKNOWLEDGED" and self.error_code is None:
            raise HandoffContractRejected("Partial or rejected local result requires a typed error.")


@dataclass(frozen=True, slots=True)
class ExternalHandoffCommandResult:
    request: CompiledExternalHandoffRequest
    acknowledgement: LocalHandoffAcknowledgement
    compatibility: LocalCompatibilityValidationReceipt
    result_boundary: LocalExternalResultEnvelope

    def __post_init__(self) -> None:
        if not (
            self.request.request_hash
            == self.acknowledgement.request_identity
            == self.compatibility.request_identity
            == self.result_boundary.request_identity
        ):
            raise HandoffContractRejected("Handoff result identities are not linked.")
        if not (
            self.request.target_id
            == self.acknowledgement.target_identity
            == self.compatibility.target_profile_identity
            == self.result_boundary.target_identity
        ):
            raise HandoffContractRejected("Handoff result target identities are not linked.")
        if self.acknowledgement.acknowledged_payload_hash != self.request.request_hash:
            raise HandoffContractRejected("Acknowledged payload does not link to the compiled request.")
        if self.acknowledgement.authority_identity != self.request.authority_ref.authority:
            raise HandoffAuthorityRejected("Acknowledgement authority does not link to the request authority.")
        if self.acknowledgement.acknowledged_contract_version != self.request.local_contract_pin:
            raise HandoffContractRejected("Acknowledged contract version does not link to the request.")
        if self.compatibility.local_contract_pin != self.request.local_contract_pin:
            raise HandoffContractRejected("Validation contract pin does not link to the request.")
        if self.compatibility.output_hash != self.result_boundary.result_hash:
            raise HandoffContractRejected("Local validation output does not link to the result boundary.")
        if self.result_boundary.status != "LOCAL_ACKNOWLEDGED":
            raise HandoffContractRejected("Successful handoff result cannot carry a partial or rejected status.")


@dataclass(frozen=True, slots=True)
class ExternalHandoffObservation:
    event_name: str
    outcome: str
    command_id: str
    target_id: str
    artifact_identity: str
    authority_identity: str
    correlation_id: str
    causation_id: str
    failure_context: str | None


class VisualAssetDemandPort(Protocol):
    def acknowledge(self, request: CompiledExternalHandoffRequest) -> LocalHandoffAcknowledgement: ...
    def record_acknowledgement(self, request_hash: str) -> None: ...
    def checkpoint(self) -> int: ...
    def restore(self, checkpoint: int) -> None: ...


class DelegationHandoffPort(Protocol):
    def acknowledge(self, request: CompiledExternalHandoffRequest) -> LocalHandoffAcknowledgement: ...
    def record_acknowledgement(self, request_hash: str) -> None: ...
    def checkpoint(self) -> int: ...
    def restore(self, checkpoint: int) -> None: ...


class _LocalFixturePort:
    def __init__(self, *, target_id: str, identity: str) -> None:
        self.target_id = target_id
        self.identity = identity
        self.calls: list[str] = []
        self._fail_before_record = False

    def acknowledge(self, request: CompiledExternalHandoffRequest) -> LocalHandoffAcknowledgement:
        if request.target_id != self.target_id:
            raise HandoffContractRejected("Local port received the wrong governed target.")
        values = {
            "request_identity": request.request_hash,
            "target_identity": request.target_id,
            "acknowledged_contract_version": request.local_contract_pin,
            "acknowledged_payload_hash": request.request_hash,
            "test_double_identity": self.identity,
            "authority_identity": request.authority_ref.authority,
            "outcome": "ACKNOWLEDGED_BY_LOCAL_TEST_DOUBLE",
            "failure_context": "NONE",
            "authority": LOCAL_TEST_DOUBLE_ONLY,
            "external_acceptance": False,
        }
        return LocalHandoffAcknowledgement(
            acknowledgement_id=f"ST-07.03:LocalAck:{sha256(_canonical_json(values)).hexdigest()}",
            **values,
        )

    def record_acknowledgement(self, request_hash: str) -> None:
        if self._fail_before_record:
            self._fail_before_record = False
            raise ExternalHandoffCommandRejected("Injected atomic local-port failure.")
        self.calls.append(request_hash)

    def inject_failure_before_record(self) -> None:
        self._fail_before_record = True

    def checkpoint(self) -> int:
        return len(self.calls)

    def restore(self, checkpoint: int) -> None:
        del self.calls[checkpoint:]


class LocalVisualAssetDemandTestDouble(_LocalFixturePort):
    def __init__(self) -> None:
        super().__init__(target_id=VAE_TARGET, identity="local-vae-fixture-port/v1")


class LocalDelegationHandoffTestDouble(_LocalFixturePort):
    def __init__(self) -> None:
        super().__init__(target_id=DELEGATION_TARGET, identity="local-delegation-rc4-fixture-port/v1")


class InMemoryExternalHandoffObservationSink:
    def __init__(self) -> None:
        self._items: list[ExternalHandoffObservation] = []
        self._fail_before_emit = False

    @property
    def items(self) -> tuple[ExternalHandoffObservation, ...]:
        return tuple(self._items)

    def emit(self, value: ExternalHandoffObservation) -> None:
        if self._fail_before_emit:
            self._fail_before_emit = False
            raise ExternalHandoffCommandRejected("Injected atomic handoff-observation failure.")
        self._items.append(value)

    def inject_failure_before_emit(self) -> None:
        self._fail_before_emit = True

    def checkpoint(self) -> int:
        return len(self._items)

    def restore(self, checkpoint: int) -> None:
        del self._items[checkpoint:]


class InMemoryExternalHandoffRepository:
    def __init__(self) -> None:
        self._payloads: dict[str, str] = {}
        self._results: dict[str, ExternalHandoffCommandResult] = {}
        self._fail_before_commit = False

    def inject_failure_before_commit(self) -> None:
        self._fail_before_commit = True

    def command_state(self, command_id: str) -> tuple[str, ExternalHandoffCommandResult] | None:
        if command_id not in self._results:
            return None
        return self._payloads[command_id], self._results[command_id]

    def commit(self, command_id: str, payload_hash: str, result: ExternalHandoffCommandResult) -> None:
        payloads = dict(self._payloads)
        results = dict(self._results)
        payloads[command_id] = payload_hash
        results[command_id] = result
        if self._fail_before_commit:
            self._fail_before_commit = False
            raise ExternalHandoffCommandRejected("Injected atomic external-handoff failure.")
        self._payloads, self._results = payloads, results

    def checkpoint(self) -> tuple[dict[str, str], dict[str, ExternalHandoffCommandResult]]:
        return dict(self._payloads), dict(self._results)

    def restore(
        self, checkpoint: tuple[dict[str, str], dict[str, ExternalHandoffCommandResult]]
    ) -> None:
        self._payloads, self._results = checkpoint


class ExternalHandoffService:
    def __init__(
        self,
        *,
        authority: AuthorityService,
        repository: InMemoryExternalHandoffRepository,
        observations: InMemoryExternalHandoffObservationSink,
        vae_port: VisualAssetDemandPort,
        delegation_port: DelegationHandoffPort,
    ) -> None:
        if type(vae_port) is not LocalVisualAssetDemandTestDouble:
            raise ExternalHandoffCommandRejected("OD-AM-001 permits only the exact local VAE test double.")
        if type(delegation_port) is not LocalDelegationHandoffTestDouble:
            raise ExternalHandoffCommandRejected("OD-AM-001 permits only the exact local Delegation test double.")
        self._authority = authority
        self._repository = repository
        self._observations = observations
        self._ports = {VAE_TARGET: vae_port, DELEGATION_TARGET: delegation_port}

    def compile_and_acknowledge(self, command: CompileExternalHandoffCommand) -> ExternalHandoffCommandResult:
        try:
            payload_hash = _payload_hash(command)
        except HandoffContractRejected as error:
            self._observations.emit(
                ExternalHandoffObservation(
                    event_name="ST-07.03:LocalExternalHandoffRejected",
                    outcome="FAIL",
                    command_id=command.command_id,
                    target_id=command.handoff_input.target_id,
                    artifact_identity=command.command_id,
                    authority_identity=command.actor_id,
                    correlation_id=command.correlation_id,
                    causation_id=command.causation_id,
                    failure_context=str(error),
                )
            )
            raise ExternalHandoffCommandRejected(str(error)) from error
        prior = self._repository.command_state(command.command_id)
        if prior is not None:
            prior_hash, result = prior
            if prior_hash != payload_hash:
                raise ExternalHandoffCommandRejected("Command identity was reused with a conflicting payload.")
            return result
        try:
            self._authority.authorize(
                actor_id=command.actor_id,
                action=Action.COMPILE_EXTERNAL_HANDOFFS,
                resource_id=command.handoff_input.request_id,
                now=command.now,
            )
            if command.handoff_input.authority_ref.authority != command.actor_id:
                raise HandoffAuthorityRejected("Handoff authority does not identify the acting actor.")
            request = compile_external_handoff(command.handoff_input)
            repository_checkpoint = self._repository.checkpoint()
            observation_checkpoint = self._observations.checkpoint()
            port = self._ports[request.target_id]
            port_checkpoint = port.checkpoint()
            acknowledgement = self._ports[request.target_id].acknowledge(request)
            compatibility = validate_local_contract(request)
            boundary = LocalExternalResultEnvelope(
                request_identity=request.request_hash,
                target_identity=request.target_id,
                status="LOCAL_ACKNOWLEDGED",
                result_hash=compatibility.output_hash,
                error_code=None,
                reconciliation_required=False,
            )
            result = ExternalHandoffCommandResult(request, acknowledgement, compatibility, boundary)
            success_observation = ExternalHandoffObservation(
                event_name="ST-07.03:LocalExternalHandoffAcknowledged",
                outcome="PASS",
                command_id=command.command_id,
                target_id=request.target_id,
                artifact_identity=request.request_hash,
                authority_identity=command.actor_id,
                correlation_id=command.correlation_id,
                causation_id=command.causation_id,
                failure_context=None,
            )
            self._observations.emit(success_observation)
            self._repository.commit(command.command_id, payload_hash, result)
            port.record_acknowledgement(request.request_hash)
        except (AuthorityDenied, HandoffContractRejected, HandoffAuthorityRejected, ExternalHandoffCommandRejected) as error:
            if "repository_checkpoint" in locals():
                self._repository.restore(repository_checkpoint)
                self._observations.restore(observation_checkpoint)
                port.restore(port_checkpoint)
            self._observations.emit(
                ExternalHandoffObservation(
                    event_name="ST-07.03:LocalExternalHandoffRejected",
                    outcome="FAIL",
                    command_id=command.command_id,
                    target_id=command.handoff_input.target_id,
                    artifact_identity=command.command_id,
                    authority_identity=command.actor_id,
                    correlation_id=command.correlation_id,
                    causation_id=command.causation_id,
                    failure_context=str(error),
                )
            )
            raise ExternalHandoffCommandRejected(str(error)) from error
        return result


def _payload_hash(command: CompileExternalHandoffCommand) -> str:
    value = {
        "command_id": command.command_id,
        "handoff_input": {
            "request_id": command.handoff_input.request_id,
            "request_version": command.handoff_input.request_version,
            "target_id": command.handoff_input.target_id,
            "run_ref": command.handoff_input.run_ref.canonical_dict(),
            "atomic_harness_definition_ref": command.handoff_input.atomic_harness_definition_ref.canonical_dict(),
            "atomic_harness_definition_receipt_ref": command.handoff_input.atomic_harness_definition_receipt_ref.canonical_dict(),
            "st_07_02_completion_receipt_sha256": command.handoff_input.st_07_02_completion_receipt_sha256,
            "source": command.handoff_input.source.canonical_dict(),
            "semantic_lineage": [ref.canonical_dict() for ref in command.handoff_input.semantic_lineage],
            "wrong_reading_locks": [item.canonical_dict() for item in command.handoff_input.wrong_reading_locks],
            "inherited_parent_locks": [item.canonical_dict() for item in command.handoff_input.inherited_parent_locks],
            "authority_ref": command.handoff_input.authority_ref.canonical_dict(),
            "local_contract_pin": command.handoff_input.local_contract_pin,
            "production_ready": command.handoff_input.production_ready,
            "certified": command.handoff_input.certified,
        },
        "actor_id": command.actor_id,
        "now": command.now.isoformat(),
        "correlation_id": command.correlation_id,
        "causation_id": command.causation_id,
    }
    return f"sha256:{sha256(_canonical_json(value)).hexdigest()}"


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")
