"""Approved generative provider adapters for TS-CMF-044."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import (
    ProviderCapabilityRecord,
    ProviderJob,
    ProviderJobStatus,
    ProviderRequest,
    ProviderResponse,
    provider_hash,
)


@dataclass
class GenerativeProviderAdapter:
    provider_name: str
    model_or_workflow_version: str
    raw_extension: str = "bin"
    include_metadata: bool = True

    def submit(
        self,
        *,
        request: ProviderRequest,
        capability: ProviderCapabilityRecord,
        job: ProviderJob,
    ) -> ProviderResponse:
        provider_response_id = f"{self.provider_name}:{uuid4()}"
        output_hash = provider_hash(
            {
                "provider_job_id": job.provider_job_id,
                "provider_name": self.provider_name,
                "model_or_workflow_version": self.model_or_workflow_version,
                "input_artifact_hashes": request.input_artifact_hashes,
                "prompt_hash": request.prompt_hash,
                "parameters": request.parameters,
            }
        )
        metadata = {
            "schema_version": "cmf.provider_metadata.v1",
            "provider_name": self.provider_name,
            "model_or_workflow_version": self.model_or_workflow_version,
            "seed": request.parameters.get("seed"),
            "config_values": request.parameters.get("config_values", {}),
            "provider_response_id": provider_response_id,
        }
        response_metadata = {
            "provider_name": self.provider_name,
            "capability_name": capability.capability_name,
            "raw_extension": self.raw_extension,
            "evaluation_required": True,
        }
        if self.include_metadata:
            response_metadata["provider_metadata"] = metadata
        return ProviderResponse(
            schema_version="cmf.provider_response.v1",
            provider_response_id=uuid4(),
            provider_job_id=job.provider_job_id,
            provider_correlation_id=provider_response_id,
            status=ProviderJobStatus.succeeded,
            output_artifact_hashes=[output_hash],
            cost_amount=float(request.parameters.get("estimated_cost_amount", 0.0)),
            response_metadata=response_metadata,
            received_at=utc_now(),
        )


class GPTImage2Adapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("gpt_image_2", "gpt_image_2", "png", include_metadata)


class Flux2Klein9BAdapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("flux_2_klein_9b", "flux_2_klein_9b", "png", include_metadata)


class QwenImageLayeredAdapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("qwen_image_layered", "qwen_image_layered", "json", include_metadata)


class SAM3Adapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("sam3", "sam3", "png", include_metadata)


class LavaSRGenerativeAdapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("lavasr", "lavasr", "wav", include_metadata)


class MossTTSGenerativeAdapter(GenerativeProviderAdapter):
    def __init__(self, *, include_metadata: bool = True):
        super().__init__("moss_tts", "moss_tts", "wav", include_metadata)


def current_generative_adapters() -> list[GenerativeProviderAdapter]:
    return [
        GPTImage2Adapter(),
        Flux2Klein9BAdapter(),
        QwenImageLayeredAdapter(),
        SAM3Adapter(),
        LavaSRGenerativeAdapter(),
        MossTTSGenerativeAdapter(),
    ]
