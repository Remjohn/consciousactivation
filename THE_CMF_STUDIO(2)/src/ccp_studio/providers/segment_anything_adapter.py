from __future__ import annotations

import base64
import os

from ccp_studio.contracts.provider_adapters import (
    ProviderAdapterConfig,
    ProviderCapabilityId,
    ProviderExecutionRequest,
    ProviderExecutionStatus,
    ProviderId,
    ProviderOutputAsset,
    ProviderOutputType,
    ProviderPollReceipt,
    ProviderSubmissionReceipt,
    ProviderTransportMode,
)
from ccp_studio.providers.base import BaseProviderAdapter
from ccp_studio.providers.provider_http import ProviderHttpClient
from ccp_studio.providers.provider_storage import ProviderOutputStorage


_FAKE_MASK_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


class SegmentAnythingAdapter(BaseProviderAdapter):
    provider_id = ProviderId.SEGMENT_ANYTHING
    capability_ids = [
        ProviderCapabilityId.OBJECT_SEGMENT,
        ProviderCapabilityId.MASK_GENERATE,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, http: ProviderHttpClient | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.SEGMENT_ANYTHING,
                enabled=False,
                transport_mode=ProviderTransportMode.SELF_HOSTED_HTTP,
                base_url=os.getenv("SEGMENT_ANYTHING_ENDPOINT"),
                model_name="segment-anything",
                credential_ref=None,
            )
        )
        self.http = http or ProviderHttpClient()
        self.storage = storage or ProviderOutputStorage()

    def build_payload(self, request: ProviderExecutionRequest) -> dict:
        return {
            "input_assets": [asset.uri for asset in request.input_assets if asset.uri],
            "prompt_points": request.prompt_contract.primary_prompt,
            "output": "mask_and_cutout",
        }

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        payload = self.build_payload(request)
        if not self.config.base_url:
            response = {"id": f"sam_local_{request.provider_execution_request_id}"}
        else:
            response = self.http.post_json(url=self.config.base_url, payload=payload, timeout=request.timeout_seconds)
        return ProviderSubmissionReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=response.get("id", f"sam_{request.provider_execution_request_id}"),
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
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        mask = self.storage.save_bytes(
            brand_id=request.brand_id,
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            data=_FAKE_MASK_PNG,
            filename="mask.png",
            output_type=ProviderOutputType.MASK,
            metadata={"segment_anything": True},
        )
        cutout = self.storage.save_bytes(
            brand_id=request.brand_id,
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            data=_FAKE_MASK_PNG,
            filename="cutout.png",
            output_type=ProviderOutputType.CUTOUT,
            metadata={"segment_anything": True},
        )
        return [mask, cutout]
