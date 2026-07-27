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


class QwenImageAdapter(BaseProviderAdapter):
    provider_id = ProviderId.QWEN_IMAGE
    capability_ids = [
        ProviderCapabilityId.IMAGE_GENERATE,
        ProviderCapabilityId.IMAGE_EDIT,
        ProviderCapabilityId.IMAGE_REFERENCE_EDIT,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, http: ProviderHttpClient | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.QWEN_IMAGE,
                enabled=False,
                transport_mode=ProviderTransportMode.DISABLED,
                base_url=os.getenv("QWEN_IMAGE_ENDPOINT"),
                model_name="qwen-image",
                credential_ref=ProviderCredentialRef(provider_id=ProviderId.QWEN_IMAGE, env_var_name="QWEN_API_KEY"),
                extra={"transport_options": ["dashscope_http", "self_hosted_http", "runninghub_workflow", "comfyui_workflow"]},
            )
        )
        self.http = http or ProviderHttpClient()
        self.storage = storage or ProviderOutputStorage()

    def build_payload(self, request: ProviderExecutionRequest) -> dict:
        return {
            "model": self.config.model_name,
            "prompt": request.prompt_contract.primary_prompt,
            "negative_prompt": request.prompt_contract.negative_prompt,
            "frame_profile": request.frame_profile,
            "reference_assets": [asset.uri for asset in request.reference_assets if asset.uri],
        }

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        if not self.config.base_url:
            raise RuntimeError("QwenImageAdapter requires QWEN_IMAGE_ENDPOINT or configured base_url")
        payload = self.build_payload(request)
        api_key = os.getenv(self.config.credential_ref.env_var_name) if self.config.credential_ref else None
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        response = self.http.post_json(url=self.config.base_url, payload=payload, headers=headers, timeout=request.timeout_seconds)
        provider_request_id = response.get("id") or response.get("request_id") or f"qwen_{request.provider_execution_request_id}"
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
            status=ProviderExecutionStatus.RUNNING,
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        return []
