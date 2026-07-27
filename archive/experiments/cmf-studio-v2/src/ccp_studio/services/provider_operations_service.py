"""Provider capability registry and job receipt service for TS-CMF-042."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import (
    ProviderCapabilityRecord,
    ProviderCostPolicy,
    ProviderDomainEvent,
    ProviderJob,
    ProviderJobStatus,
    ProviderReceipt,
    ProviderRequest,
    ProviderResponse,
    ProviderRetryPolicy,
    ProviderWebhookEnvelope,
    new_provider_request,
    provider_hash,
)
from ccp_studio.providers.fake_provider import FakeProviderAdapter
from ccp_studio.repositories.provider_jobs import InMemoryProviderOperationsRepository
from ccp_studio.services.command_bus import CommandBus


class ProviderAdapter(Protocol):
    provider_name: str

    def submit(
        self,
        *,
        request: ProviderRequest,
        capability: ProviderCapabilityRecord,
        job: ProviderJob,
    ) -> ProviderResponse:
        ...


class ProviderOperationsError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def default_cost_policies() -> dict[str, ProviderCostPolicy]:
    return {
        "cmf.provider.cost.standard": ProviderCostPolicy(
            schema_version="cmf.provider_cost_policy.v1",
            cost_policy_id="cmf.provider.cost.standard",
            max_cost_amount=25.0,
            currency="USD",
            requires_estimate=True,
        ),
        "cmf.provider.cost.gpu_24_32gb": ProviderCostPolicy(
            schema_version="cmf.provider_cost_policy.v1",
            cost_policy_id="cmf.provider.cost.gpu_24_32gb",
            max_cost_amount=250.0,
            currency="USD",
            requires_estimate=True,
        ),
    }


def default_retry_policies() -> dict[str, ProviderRetryPolicy]:
    return {
        "cmf.provider.retry.standard": ProviderRetryPolicy(
            schema_version="cmf.provider_retry_policy.v1",
            retry_policy_id="cmf.provider.retry.standard",
            max_retries=2,
            retryable_failure_codes=["RATE_LIMIT", "TIMEOUT", "WORKER_UNAVAILABLE"],
        ),
        "cmf.provider.retry.gpu_worker": ProviderRetryPolicy(
            schema_version="cmf.provider_retry_policy.v1",
            retry_policy_id="cmf.provider.retry.gpu_worker",
            max_retries=1,
            retryable_failure_codes=["GPU_WORKER_RESTART", "WORKER_UNAVAILABLE"],
        ),
    }


def current_cmf_provider_capabilities() -> list[ProviderCapabilityRecord]:
    now = utc_now()
    standard_cost = "cmf.provider.cost.standard"
    standard_retry = "cmf.provider.retry.standard"
    return [
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="ideogram_4.composition_plate.v1",
            provider_name="ideogram_4",
            capability_name="composition_plate",
            model_or_workflow_version="ideogram_4",
            allowed_input_types=["scene_spec", "render_contract", "composition_prompt"],
            output_contract="cmf.composition_plate.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.composition_boundary.v1"],
            execution_environment="external_provider_api",
            governance_notes=["Composition director only; final identity and final text are downstream."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="gpt_image_2.image_generation.v1",
            provider_name="gpt_image_2",
            capability_name="image_generation",
            model_or_workflow_version="gpt_image_2",
            allowed_input_types=["scene_spec", "locked_brand_asset", "prompt_hash"],
            output_contract="cmf.visual_candidate.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.visual_candidate.v1"],
            execution_environment="external_provider_api",
            governance_notes=["Current image provider record; not GPT Image legacy naming."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="flux_2_klein_9b.image_generation.v1",
            provider_name="flux_2_klein_9b",
            capability_name="image_generation",
            model_or_workflow_version="flux_2_klein_9b",
            allowed_input_types=["scene_spec", "locked_brand_asset", "prompt_hash"],
            output_contract="cmf.visual_candidate.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.visual_candidate.v1"],
            execution_environment="external_provider_api",
            governance_notes=["Current Flux route; not Flux/Kontext legacy naming."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="qwen_image_layered.layer_generation.v1",
            provider_name="qwen_image_layered",
            capability_name="layer_generation",
            model_or_workflow_version="qwen_image_layered",
            allowed_input_types=["layer_manifest", "locked_brand_asset", "prompt_hash"],
            output_contract="cmf.layer_entry.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.layerability.v1"],
            execution_environment="external_provider_api",
            governance_notes=["Layered asset route for editable downstream composition."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="sam3.segmentation_mask.v1",
            provider_name="sam3",
            capability_name="segmentation_mask",
            model_or_workflow_version="sam3",
            allowed_input_types=["visual_candidate", "layer_manifest"],
            output_contract="cmf.segmentation_mask.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.mask_quality.v1"],
            execution_environment="external_provider_api",
            governance_notes=["Masking route for downstream layer repair and decomposition."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="comfyui_docker_gpu.render_worker.v1",
            provider_name="comfyui_docker_gpu",
            capability_name="render_worker",
            model_or_workflow_version="comfyui_docker_24gb_32gb_vram",
            allowed_input_types=["workflow_json", "layer_manifest", "render_contract"],
            output_contract="cmf.render_output.v1",
            cost_policy_id="cmf.provider.cost.gpu_24_32gb",
            retry_policy_id="cmf.provider.retry.gpu_worker",
            evaluation_requirement_ids=["cmf.eval.render_artifact_integrity.v1"],
            execution_environment="self_hosted_aws_or_google_cloud_gpu_24gb_32gb_vram",
            governance_notes=["Self-hosted ComfyUI Docker worker on AWS or Google Cloud GPU."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="lavasr.audio_restoration.v1",
            provider_name="lavasr",
            capability_name="audio_restoration",
            model_or_workflow_version="lavasr",
            allowed_input_types=["source_audio"],
            output_contract="cmf.repaired_source_voice.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.audio_restoration.v1"],
            execution_environment="provider_adapter",
            governance_notes=["Audio restoration receipt must remain distinct from source voice authority."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="moss_tts.synthetic_bridge_voice.v1",
            provider_name="moss_tts",
            capability_name="synthetic_bridge_voice",
            model_or_workflow_version="moss_tts",
            allowed_input_types=["approved_bridge_text", "voice_profile_ref"],
            output_contract="cmf.synthetic_bridge_voice.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.synthetic_bridge_voice.v1"],
            execution_environment="provider_adapter",
            governance_notes=["Synthetic bridge only; never replaces source voice truth."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="remotion.video_render.v1",
            provider_name="remotion",
            capability_name="video_render",
            model_or_workflow_version="remotion",
            allowed_input_types=["assembly_plan", "layer_manifest", "caption_manifest", "audio_mix_manifest"],
            output_contract="cmf.render_output.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.render_artifact_integrity.v1"],
            execution_environment="deterministic_renderer",
            governance_notes=["Deterministic text/layer renderer for final downstream assembly."],
            active=True,
            activated_at=now,
        ),
        ProviderCapabilityRecord(
            schema_version="cmf.provider_capability_record.v1",
            provider_capability_id="motion_canvas.programmatic_animation.v1",
            provider_name="motion_canvas",
            capability_name="programmatic_animation",
            model_or_workflow_version="motion_canvas",
            allowed_input_types=["animation_plan", "layer_manifest"],
            output_contract="cmf.motion_canvas_scene.v1",
            cost_policy_id=standard_cost,
            retry_policy_id=standard_retry,
            evaluation_requirement_ids=["cmf.eval.motion_integrity.v1"],
            execution_environment="deterministic_renderer",
            governance_notes=["Programmatic motion route; renderer cannot approve final business state."],
            active=True,
            activated_at=now,
        ),
    ]


@dataclass
class ProviderOperationsService:
    repository: InMemoryProviderOperationsRepository = field(default_factory=InMemoryProviderOperationsRepository)
    adapters: dict[str, ProviderAdapter] = field(default_factory=dict)
    cost_policies: dict[str, ProviderCostPolicy] = field(default_factory=default_cost_policies)
    retry_policies: dict[str, ProviderRetryPolicy] = field(default_factory=default_retry_policies)

    def seed_current_cmf_capabilities(self) -> list[ProviderCapabilityRecord]:
        return [self.activate_provider_capability(capability) for capability in current_cmf_provider_capabilities()]

    def activate_provider_capability(self, capability: ProviderCapabilityRecord) -> ProviderCapabilityRecord:
        if capability.cost_policy_id not in self.cost_policies:
            raise ProviderOperationsError("COST_POLICY_UNKNOWN", "Provider capability references an unknown cost policy.")
        if capability.retry_policy_id not in self.retry_policies:
            raise ProviderOperationsError("RETRY_POLICY_UNKNOWN", "Provider capability references an unknown retry policy.")
        return self.repository.put_capability(capability)

    def submit_provider_job(
        self,
        *,
        provider_capability_id: str,
        organization_id: UUID,
        brand_id: UUID,
        requested_by_actor_id: UUID,
        input_artifact_hashes: list[str],
        input_types: list[str],
        idempotency_key: str,
        correlation_id: UUID | None = None,
        complete_editing_session_id: UUID | None = None,
        scene_spec_id: UUID | None = None,
        prompt_hash: str | None = None,
        parameters: dict[str, Any] | None = None,
        command_id: UUID | None = None,
    ) -> ProviderJob:
        prior = self.repository.job_for_idempotency(organization_id, brand_id, idempotency_key)
        if prior is not None:
            return prior
        capability = self._active_capability(provider_capability_id)
        request = new_provider_request(
            provider_capability_id=provider_capability_id,
            organization_id=organization_id,
            brand_id=brand_id,
            requested_by_actor_id=requested_by_actor_id,
            complete_editing_session_id=complete_editing_session_id,
            scene_spec_id=scene_spec_id,
            input_artifact_hashes=input_artifact_hashes,
            input_types=input_types,
            prompt_hash=prompt_hash,
            parameters=parameters,
            idempotency_key=idempotency_key,
            correlation_id=correlation_id or uuid4(),
        )
        self._validate_request_against_capability(request, capability)
        request = self.repository.put_request(request)
        request_hash = provider_hash(request.model_dump(mode="json"))
        now = utc_now()
        job = self.repository.put_job(
            ProviderJob(
                schema_version="cmf.provider_job.v1",
                provider_job_id=uuid4(),
                provider_request_id=request.provider_request_id,
                provider_capability_id=capability.provider_capability_id,
                provider_name=capability.provider_name,
                capability_name=capability.capability_name,
                model_or_workflow_version=capability.model_or_workflow_version,
                status=ProviderJobStatus.submitted,
                retry_count=0,
                cost_policy_id=capability.cost_policy_id,
                retry_policy_id=capability.retry_policy_id,
                evaluation_requirement_ids=capability.evaluation_requirement_ids,
                request_hash=request_hash,
                submitted_at=now,
                updated_at=now,
            )
        )
        self.repository.remember_idempotency(request, job.provider_job_id)
        adapter = self.adapters.get(capability.provider_name, FakeProviderAdapter(provider_name=capability.provider_name))
        response = self.repository.put_response(adapter.submit(request=request, capability=capability, job=job))
        job = job.model_copy(update={"provider_correlation_id": response.provider_correlation_id, "updated_at": utc_now()})
        self.repository.put_job(job)
        self.repository.append_event(
            ProviderDomainEvent(
                schema_version="cmf.provider_domain_event.v1",
                provider_event_id=uuid4(),
                event_type="ProviderJobSubmitted",
                provider_job_id=job.provider_job_id,
                payload={"command_id": str(command_id) if command_id else None},
                created_at=utc_now(),
            )
        )
        return job

    def execute_provider_job(self, **kwargs: Any) -> ProviderReceipt:
        job = self.submit_provider_job(**kwargs)
        existing = self.repository.receipt_for_job(job.provider_job_id)
        if existing is not None:
            return existing
        response = self.repository.latest_response_for_job(job.provider_job_id)
        if response is None:
            raise ProviderOperationsError("PROVIDER_RESPONSE_REQUIRED", "Provider response is required before receipt normalization.")
        return self.normalize_provider_response(response=response)

    def normalize_provider_response(
        self,
        *,
        response: ProviderResponse | None = None,
        provider_job_id: UUID | None = None,
        status: ProviderJobStatus | str | None = None,
        output_artifact_hashes: list[str] | None = None,
        cost_amount: float | None = None,
        failure_code: str | None = None,
        response_metadata: dict[str, Any] | None = None,
        provider_correlation_id: str | None = None,
    ) -> ProviderReceipt:
        if response is None:
            if provider_job_id is None or status is None or provider_correlation_id is None:
                raise ProviderOperationsError("PROVIDER_RESPONSE_REQUIRED", "Provider response data is incomplete.")
            response = ProviderResponse(
                schema_version="cmf.provider_response.v1",
                provider_response_id=uuid4(),
                provider_job_id=provider_job_id,
                provider_correlation_id=provider_correlation_id,
                status=ProviderJobStatus(status),
                output_artifact_hashes=output_artifact_hashes or [],
                cost_amount=cost_amount,
                failure_code=failure_code,
                response_metadata=response_metadata or {},
                received_at=utc_now(),
            )
            self.repository.put_response(response)
        job = self._job(response.provider_job_id)
        request = self.repository.requests[job.provider_request_id]
        response_hash = provider_hash(response.model_dump(mode="json"))
        retry_count = int(response.response_metadata.get("retry_count", job.retry_count))
        event_type = "ProviderReceiptValidated"
        receipt = self.repository.put_receipt(
            ProviderReceipt(
                schema_version="cmf.provider_receipt.v2",
                provider_receipt_id=uuid4(),
                provider_job_id=job.provider_job_id,
                provider_request_id=job.provider_request_id,
                provider_capability_id=job.provider_capability_id,
                provider_name=job.provider_name,
                capability_name=job.capability_name,
                model_or_workflow_version=job.model_or_workflow_version,
                status=response.status,
                output_artifact_hashes=response.output_artifact_hashes,
                cost_amount=response.cost_amount,
                retry_count=retry_count,
                failure_code=response.failure_code,
                request_hash=job.request_hash,
                response_hash=response_hash,
                provider_correlation_id=response.provider_correlation_id,
                created_domain_event_type=event_type,
                created_at=utc_now(),
            )
        )
        job = job.model_copy(
            update={
                "status": response.status,
                "retry_count": retry_count,
                "provider_correlation_id": response.provider_correlation_id,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_job(job)
        self.repository.append_event(
            ProviderDomainEvent(
                schema_version="cmf.provider_domain_event.v1",
                provider_event_id=uuid4(),
                event_type=event_type,
                provider_job_id=job.provider_job_id,
                provider_receipt_id=receipt.provider_receipt_id,
                payload={"response_hash": response_hash, "request_brand_id": str(request.brand_id)},
                created_at=utc_now(),
            )
        )
        if response.status == ProviderJobStatus.succeeded:
            self.repository.append_event(
                ProviderDomainEvent(
                    schema_version="cmf.provider_domain_event.v1",
                    provider_event_id=uuid4(),
                    event_type="ProviderJobCompleted",
                    provider_job_id=job.provider_job_id,
                    provider_receipt_id=receipt.provider_receipt_id,
                    payload={"output_artifact_hashes": response.output_artifact_hashes},
                    created_at=utc_now(),
                )
            )
        return receipt

    def process_provider_webhook(self, envelope: ProviderWebhookEnvelope) -> ProviderReceipt:
        prior_receipt_id = self.repository.webhook_idempotency_index.get(envelope.idempotency_key)
        if prior_receipt_id is not None:
            return self.repository.receipts[prior_receipt_id]
        self.repository.put_webhook(envelope)
        job_id = self.repository.job_by_provider_correlation_id.get(envelope.provider_correlation_id)
        if job_id is None:
            raise ProviderOperationsError("PROVIDER_JOB_NOT_FOUND", "Webhook correlation ID does not match a provider job.")
        status = ProviderJobStatus(envelope.payload.get("status", ProviderJobStatus.succeeded.value))
        receipt = self.normalize_provider_response(
            provider_job_id=job_id,
            status=status,
            output_artifact_hashes=envelope.payload.get("output_artifact_hashes", []),
            cost_amount=envelope.payload.get("cost_amount"),
            failure_code=envelope.payload.get("failure_code"),
            response_metadata=envelope.payload.get("response_metadata", {"webhook": True}),
            provider_correlation_id=envelope.provider_correlation_id,
        )
        self.repository.webhook_idempotency_index[envelope.idempotency_key] = receipt.provider_receipt_id
        self.repository.append_event(
            ProviderDomainEvent(
                schema_version="cmf.provider_domain_event.v1",
                provider_event_id=uuid4(),
                event_type="ProviderWebhookProcessed",
                provider_job_id=job_id,
                provider_receipt_id=receipt.provider_receipt_id,
                payload={"provider_webhook_id": str(envelope.provider_webhook_id)},
                created_at=utc_now(),
            )
        )
        return receipt

    def validate_provider_receipt(self, provider_receipt_id: UUID) -> ProviderReceipt:
        receipt = self.repository.receipts.get(provider_receipt_id)
        if receipt is None:
            raise ProviderOperationsError("PROVIDER_RECEIPT_REQUIRED", "Provider receipt is required.")
        self._active_capability(receipt.provider_capability_id)
        return receipt

    def _active_capability(self, provider_capability_id: str) -> ProviderCapabilityRecord:
        capability = self.repository.capabilities.get(provider_capability_id)
        if capability is None or not capability.active:
            raise ProviderOperationsError("PROVIDER_CAPABILITY_UNAVAILABLE", "Provider capability is unavailable.")
        return capability

    def _job(self, provider_job_id: UUID) -> ProviderJob:
        job = self.repository.jobs.get(provider_job_id)
        if job is None:
            raise ProviderOperationsError("PROVIDER_JOB_REQUIRED", "Provider job is required.")
        return job

    def _validate_request_against_capability(self, request: ProviderRequest, capability: ProviderCapabilityRecord) -> None:
        unsupported = sorted(set(request.input_types) - set(capability.allowed_input_types))
        if unsupported:
            raise ProviderOperationsError("PROVIDER_INPUT_TYPE_UNSUPPORTED", "Provider request includes unsupported input types.")
        policy = self.cost_policies[capability.cost_policy_id]
        if policy.requires_estimate and "estimated_cost_amount" not in request.parameters:
            raise ProviderOperationsError("COST_ESTIMATE_REQUIRED", "Provider request requires an estimated cost amount.")
        estimated_cost = float(request.parameters.get("estimated_cost_amount", 0.0))
        if estimated_cost > policy.max_cost_amount:
            raise ProviderOperationsError("COST_POLICY_EXCEEDED", "Provider request exceeds its cost policy.")


@dataclass
class ProviderOperationsCommandHandler:
    command_type: str
    service: ProviderOperationsService
    aggregate_type: str = "provider_job"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward", "provider_webhook"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ActivateProviderCapabilityCommand":
            capability = ProviderCapabilityRecord(schema_version="cmf.provider_capability_record.v1", **payload["capability"])
            return self.service.activate_provider_capability(capability).model_dump(mode="json")
        if self.command_type == "SubmitProviderJobCommand":
            job = self.service.submit_provider_job(
                provider_capability_id=payload["provider_capability_id"],
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                requested_by_actor_id=envelope.actor.actor_id,
                complete_editing_session_id=UUID(payload["complete_editing_session_id"]) if payload.get("complete_editing_session_id") else None,
                scene_spec_id=UUID(payload["scene_spec_id"]) if payload.get("scene_spec_id") else None,
                input_artifact_hashes=payload["input_artifact_hashes"],
                input_types=payload["input_types"],
                prompt_hash=payload.get("prompt_hash"),
                parameters=payload.get("parameters"),
                idempotency_key=payload.get("provider_idempotency_key", envelope.idempotency_key),
                correlation_id=envelope.correlation_id,
                command_id=envelope.command_id,
            )
            return job.model_dump(mode="json")
        if self.command_type == "NormalizeProviderResponseCommand":
            receipt = self.service.normalize_provider_response(
                provider_job_id=UUID(payload["provider_job_id"]),
                status=payload["status"],
                output_artifact_hashes=payload.get("output_artifact_hashes", []),
                cost_amount=payload.get("cost_amount"),
                failure_code=payload.get("failure_code"),
                response_metadata=payload.get("response_metadata"),
                provider_correlation_id=payload["provider_correlation_id"],
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "ProcessProviderWebhookCommand":
            envelope_payload = payload["webhook"]
            receipt = self.service.process_provider_webhook(
                ProviderWebhookEnvelope(
                    schema_version="cmf.provider_webhook_envelope.v1",
                    provider_webhook_id=UUID(envelope_payload.get("provider_webhook_id", str(uuid4()))),
                    provider_name=envelope_payload["provider_name"],
                    provider_correlation_id=envelope_payload["provider_correlation_id"],
                    payload=envelope_payload["payload"],
                    idempotency_key=envelope_payload["idempotency_key"],
                    received_at=utc_now(),
                )
            )
            return receipt.model_dump(mode="json")
        if self.command_type == "ValidateProviderReceiptCommand":
            return self.service.validate_provider_receipt(UUID(payload["provider_receipt_id"])).model_dump(mode="json")
        raise ProviderOperationsError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("provider_job_id") or payload.get("provider_receipt_id") or payload.get("scene_spec_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        result_id = payload.get("provider_job_id")
        if isinstance(result_id, str):
            return UUID(result_id)
        return envelope.brand_id


def register_provider_operations_command_handlers(bus: CommandBus, service: ProviderOperationsService) -> None:
    for command_type in [
        "ActivateProviderCapabilityCommand",
        "SubmitProviderJobCommand",
        "NormalizeProviderResponseCommand",
        "ProcessProviderWebhookCommand",
        "ValidateProviderReceiptCommand",
        "FailProviderCapabilityUnavailableCommand",
    ]:
        bus.register_handler(ProviderOperationsCommandHandler(command_type=command_type, service=service))
