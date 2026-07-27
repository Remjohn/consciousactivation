from __future__ import annotations

import os

from ccp_studio.contracts.provider_adapters import (
    ProviderAdapterConfig,
    ProviderCapabilityId,
    ProviderCredentialRef,
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderId,
    ProviderOutputAsset,
    ProviderPollReceipt,
    ProviderSubmissionReceipt,
    ProviderTransportMode,
)
from ccp_studio.providers.base import BaseProviderAdapter
from ccp_studio.providers.provider_http import ProviderHttpClient
from ccp_studio.providers.provider_storage import ProviderOutputStorage


class OpenAIImageAdapter(BaseProviderAdapter):
    provider_id = ProviderId.OPENAI_IMAGE
    capability_ids = [
        ProviderCapabilityId.IMAGE_GENERATE,
        ProviderCapabilityId.IMAGE_EDIT,
        ProviderCapabilityId.IMAGE_INPAINT,
        ProviderCapabilityId.IMAGE_REFERENCE_EDIT,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, http: ProviderHttpClient | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.OPENAI_IMAGE,
                enabled=False,
                transport_mode=ProviderTransportMode.HTTP,
                base_url="https://api.openai.com",
                model_name="gpt-image-1",
                credential_ref=ProviderCredentialRef(provider_id=ProviderId.OPENAI_IMAGE, env_var_name="OPENAI_API_KEY"),
            )
        )
        self.http = http or ProviderHttpClient()
        self.storage = storage or ProviderOutputStorage()

    def map_frame_profile_to_size(self, frame_profile: str) -> str:
        if frame_profile.startswith("9:16") or frame_profile.startswith("4:5"):
            return "1024x1536"
        if frame_profile.startswith("16:9"):
            return "1536x1024"
        return "1024x1024"

    def build_payload(self, request: ProviderExecutionRequest) -> dict:
        payload = {
            "model": self.config.model_name,
            "prompt": request.prompt_contract.primary_prompt,
            "size": self.map_frame_profile_to_size(request.frame_profile),
        }
        if request.prompt_contract.negative_prompt:
            payload["negative_prompt"] = request.prompt_contract.negative_prompt
        return payload

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        payload = self.build_payload(request)
        api_key = os.getenv(self.config.credential_ref.env_var_name) if self.config.credential_ref else None
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        response = self.http.post_json(
            url=f"{self.config.base_url}/v1/images/generations",
            payload=payload,
            headers=headers,
            timeout=request.timeout_seconds,
        )
        provider_request_id = response.get("id") or f"openai_sync_{request.provider_execution_request_id}"
        return ProviderSubmissionReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=provider_request_id,
            request_payload_hash=self._payload_hash(payload),
            idempotency_key=request.idempotency_key,
            raw_response_redacted={"response_keys": sorted(response.keys())},
        )

    def poll(self, request: ProviderExecutionRequest, submission: ProviderSubmissionReceipt) -> ProviderPollReceipt:
        return ProviderPollReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=submission.provider_request_id,
            status=ProviderExecutionStatus.SUCCEEDED,
            raw_response_redacted={"sync": True},
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        # Project-specific live normalization should extract b64_json or URLs from the stored provider response.
        return []
