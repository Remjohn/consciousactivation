"""Generative provider adapter service for TS-CMF-044."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.generative_adapters import (
    GenerativeEvaluationState,
    GenerativeProviderOutput,
    GenerativeProviderRequest,
    ProviderMetadata,
    new_generative_adapter_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.providers.generative import current_generative_adapters
from ccp_studio.repositories.generative_adapters import InMemoryGenerativeAdapterRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.provider_operations_service import ProviderOperationsService


APPROVED_GENERATIVE_PROVIDER_NAMES = {
    "gpt_image_2",
    "flux_2_klein_9b",
    "qwen_image_layered",
    "sam3",
    "lavasr",
    "moss_tts",
}


class GenerativeProviderError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class GenerativeProviderService:
    provider_operations: ProviderOperationsService
    repository: InMemoryGenerativeAdapterRepository = field(default_factory=InMemoryGenerativeAdapterRepository)

    def __post_init__(self) -> None:
        if not self.provider_operations.repository.capabilities:
            self.provider_operations.seed_current_cmf_capabilities()
        for adapter in current_generative_adapters():
            self.provider_operations.adapters[adapter.provider_name] = adapter

    def submit_generative_provider_job(
        self,
        *,
        provider_capability_id: str,
        organization_id: UUID,
        brand_id: UUID,
        actor_id: UUID,
        purpose: str,
        input_artifact_hashes: list[str],
        input_types: list[str],
        parameters: dict[str, Any],
        idempotency_key: str,
        prompt_hash: str | None = None,
        consent_record_version_ids: list[UUID] | None = None,
        requires_consent_compatibility: bool = False,
        evaluation_target_id: UUID | None = None,
        command_id: UUID | None = None,
    ) -> GenerativeProviderOutput:
        prior_request = self.repository.request_for_idempotency(organization_id, brand_id, idempotency_key)
        if prior_request is not None:
            prior_output = next(
                (item for item in self.repository.outputs.values() if item.generative_provider_request_id == prior_request.generative_provider_request_id),
                None,
            )
            if prior_output is not None:
                return prior_output
        capability = self.provider_operations.repository.capabilities.get(provider_capability_id)
        if capability is None or not capability.active:
            raise GenerativeProviderError("PROVIDER_CAPABILITY_UNAVAILABLE", "Approved generative provider capability is required.")
        if capability.provider_name not in APPROVED_GENERATIVE_PROVIDER_NAMES:
            raise GenerativeProviderError("GENERATIVE_PROVIDER_NOT_APPROVED", "Provider is not approved for generative adapter routing.")
        request = GenerativeProviderRequest(
            schema_version="cmf.generative_provider_request.v1",
            generative_provider_request_id=uuid4(),
            provider_capability_id=provider_capability_id,
            organization_id=organization_id,
            brand_id=brand_id,
            actor_id=actor_id,
            purpose=purpose,
            input_artifact_hashes=input_artifact_hashes,
            input_types=input_types,
            prompt_hash=prompt_hash,
            parameters=parameters,
            consent_record_version_ids=consent_record_version_ids or [],
            requires_consent_compatibility=requires_consent_compatibility,
            evaluation_target_id=evaluation_target_id,
            idempotency_key=idempotency_key,
            created_at=utc_now(),
        )
        self.validate_generative_provider_consent(request)
        request = self.repository.put_request(request)
        provider_receipt = self.provider_operations.execute_provider_job(
            provider_capability_id=provider_capability_id,
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=actor_id,
            input_artifact_hashes=input_artifact_hashes,
            input_types=input_types,
            prompt_hash=prompt_hash,
            parameters=parameters,
            idempotency_key=f"generative-provider:{idempotency_key}",
            command_id=command_id,
        )
        response = self.provider_operations.repository.latest_response_for_job(provider_receipt.provider_job_id)
        if response is None:
            raise GenerativeProviderError("PROVIDER_RESPONSE_REQUIRED", "Provider response is required for generative output normalization.")
        metadata_payload = response.response_metadata.get("provider_metadata")
        if not metadata_payload:
            self.repository.put_receipt(
                new_generative_adapter_receipt(
                    actor_id=actor_id,
                    decision_code="GENERATIVE_PROVIDER_RECEIPT_VALIDATION_FAILED",
                    generative_provider_request_id=request.generative_provider_request_id,
                    provider_receipt_id=provider_receipt.provider_receipt_id,
                    evidence_refs=["PROVIDER_METADATA_REQUIRED"],
                    command_id=command_id,
                )
            )
            raise GenerativeProviderError("PROVIDER_METADATA_REQUIRED", "Provider/model metadata is required before receipt validation.")
        metadata = ProviderMetadata(**metadata_payload)
        output_hash = provider_receipt.output_artifact_hashes[0]
        extension = response.response_metadata.get("raw_extension", "bin")
        output = self.repository.put_output(
            GenerativeProviderOutput(
                schema_version="cmf.generative_provider_output.v1",
                provider_output_id=uuid4(),
                generative_provider_request_id=request.generative_provider_request_id,
                provider_job_id=provider_receipt.provider_job_id,
                provider_receipt_id=provider_receipt.provider_receipt_id,
                raw_output_uri=f"brands/{brand_id}/provider-raw/{metadata.provider_name}/{provider_receipt.provider_job_id}/{output_hash}.{extension}",
                output_hash=output_hash,
                metadata=metadata,
                evaluation_state=GenerativeEvaluationState.pending_evaluation,
                consent_record_version_ids=request.consent_record_version_ids,
                created_at=utc_now(),
            )
        )
        self.repository.put_receipt(
            new_generative_adapter_receipt(
                actor_id=actor_id,
                decision_code="GENERATIVE_PROVIDER_OUTPUT_NORMALIZED",
                generative_provider_request_id=request.generative_provider_request_id,
                provider_output_id=output.provider_output_id,
                provider_receipt_id=provider_receipt.provider_receipt_id,
                evaluation_state=output.evaluation_state,
                evidence_refs=[output.raw_output_uri, output.output_hash, metadata.model_or_workflow_version],
                command_id=command_id,
            )
        )
        return output

    def validate_generative_provider_consent(self, request: GenerativeProviderRequest) -> dict[str, Any]:
        if request.requires_consent_compatibility and not request.consent_record_version_ids:
            self.repository.put_receipt(
                new_generative_adapter_receipt(
                    actor_id=request.actor_id,
                    decision_code="GENERATIVE_PROVIDER_CONSENT_BLOCKED",
                    generative_provider_request_id=request.generative_provider_request_id,
                    evidence_refs=["CONSENT_COMPATIBILITY_REQUIRED"],
                )
            )
            raise GenerativeProviderError("CONSENT_COMPATIBILITY_REQUIRED", "Source-compatible provider inputs require consent refs.")
        return {
            "validated": True,
            "consent_record_version_ids": [str(item) for item in request.consent_record_version_ids],
        }

    def evaluate_generated_asset(
        self,
        *,
        provider_output_id: UUID,
        actor_id: UUID,
        passed: bool,
        notes: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> GenerativeProviderOutput:
        output = self._output(provider_output_id)
        state = GenerativeEvaluationState.passed if passed else GenerativeEvaluationState.failed
        updated = output.model_copy(update={"evaluation_state": state})
        self.repository.put_output(updated)
        self.repository.put_receipt(
            new_generative_adapter_receipt(
                actor_id=actor_id,
                decision_code="GENERATED_ASSET_EVALUATED",
                generative_provider_request_id=updated.generative_provider_request_id,
                provider_output_id=updated.provider_output_id,
                provider_receipt_id=updated.provider_receipt_id,
                evaluation_state=updated.evaluation_state,
                evidence_refs=notes or [],
                command_id=command_id,
            )
        )
        return updated

    def promote_generated_asset(
        self,
        *,
        provider_output_id: UUID,
        actor_id: UUID,
        command_id: UUID | None = None,
    ) -> GenerativeProviderOutput:
        output = self._output(provider_output_id)
        if output.evaluation_state != GenerativeEvaluationState.passed:
            blocked = output.model_copy(update={"evaluation_state": GenerativeEvaluationState.promotion_blocked})
            self.repository.put_output(blocked)
            self.repository.put_receipt(
                new_generative_adapter_receipt(
                    actor_id=actor_id,
                    decision_code="GENERATED_ASSET_PROMOTION_BLOCKED",
                    generative_provider_request_id=blocked.generative_provider_request_id,
                    provider_output_id=blocked.provider_output_id,
                    provider_receipt_id=blocked.provider_receipt_id,
                    evaluation_state=blocked.evaluation_state,
                    evidence_refs=["GENERATED_ASSET_EVALUATION_NOT_PASSED"],
                    command_id=command_id,
                )
            )
            raise GenerativeProviderError("GENERATED_ASSET_EVALUATION_NOT_PASSED", "Generated output must pass evaluation before promotion.")
        promoted = output.model_copy(update={"evaluation_state": GenerativeEvaluationState.promoted, "promoted_asset_id": uuid4()})
        self.repository.put_output(promoted)
        self.repository.put_receipt(
            new_generative_adapter_receipt(
                actor_id=actor_id,
                decision_code="GENERATED_ASSET_PROMOTED",
                generative_provider_request_id=promoted.generative_provider_request_id,
                provider_output_id=promoted.provider_output_id,
                provider_receipt_id=promoted.provider_receipt_id,
                evaluation_state=promoted.evaluation_state,
                promoted_asset_id=promoted.promoted_asset_id,
                evidence_refs=[str(promoted.promoted_asset_id)],
                command_id=command_id,
            )
        )
        return promoted

    def _output(self, provider_output_id: UUID) -> GenerativeProviderOutput:
        output = self.repository.outputs.get(provider_output_id)
        if output is None:
            raise GenerativeProviderError("GENERATIVE_PROVIDER_OUTPUT_REQUIRED", "Generative provider output is required.")
        return output


@dataclass
class GenerativeProviderCommandHandler:
    command_type: str
    service: GenerativeProviderService
    aggregate_type: str = "generative_provider_output"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "SubmitGenerativeProviderJobCommand":
            return self.service.submit_generative_provider_job(
                provider_capability_id=payload["provider_capability_id"],
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                actor_id=envelope.actor.actor_id,
                purpose=payload["purpose"],
                input_artifact_hashes=payload["input_artifact_hashes"],
                input_types=payload["input_types"],
                prompt_hash=payload.get("prompt_hash"),
                parameters=payload.get("parameters", {}),
                consent_record_version_ids=[UUID(item) for item in payload.get("consent_record_version_ids", [])],
                requires_consent_compatibility=bool(payload.get("requires_consent_compatibility", False)),
                evaluation_target_id=UUID(payload["evaluation_target_id"]) if payload.get("evaluation_target_id") else None,
                idempotency_key=payload.get("provider_idempotency_key", envelope.idempotency_key),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateGenerativeProviderConsentCommand":
            request = self.service.repository.requests[UUID(payload["generative_provider_request_id"])]
            return self.service.validate_generative_provider_consent(request)
        if self.command_type == "NormalizeGenerativeProviderOutputCommand":
            output = self.service.repository.outputs[UUID(payload["provider_output_id"])]
            return output.model_dump(mode="json")
        if self.command_type == "EvaluateGeneratedAssetCommand":
            return self.service.evaluate_generated_asset(
                provider_output_id=UUID(payload["provider_output_id"]),
                actor_id=envelope.actor.actor_id,
                passed=bool(payload["passed"]),
                notes=payload.get("notes"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockGeneratedAssetPromotionCommand":
            return self.service.promote_generated_asset(
                provider_output_id=UUID(payload["provider_output_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise GenerativeProviderError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("provider_output_id") or payload.get("generative_provider_request_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_generative_provider_command_handlers(bus: CommandBus, service: GenerativeProviderService) -> None:
    for command_type in [
        "SubmitGenerativeProviderJobCommand",
        "ValidateGenerativeProviderConsentCommand",
        "NormalizeGenerativeProviderOutputCommand",
        "EvaluateGeneratedAssetCommand",
        "BlockGeneratedAssetPromotionCommand",
    ]:
        bus.register_handler(GenerativeProviderCommandHandler(command_type=command_type, service=service))
