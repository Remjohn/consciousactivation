from __future__ import annotations

import base64

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
from ccp_studio.providers.provider_storage import ProviderOutputStorage


_ONE_BY_ONE_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


class FakeImageAdapter(BaseProviderAdapter):
    provider_id = ProviderId.FAKE_IMAGE
    capability_ids = [
        ProviderCapabilityId.IMAGE_GENERATE,
        ProviderCapabilityId.IMAGE_EDIT,
        ProviderCapabilityId.MASK_GENERATE,
        ProviderCapabilityId.OBJECT_SEGMENT,
    ]

    def __init__(self, config: ProviderAdapterConfig | None = None, storage: ProviderOutputStorage | None = None):
        super().__init__(
            config
            or ProviderAdapterConfig(
                provider_id=ProviderId.FAKE_IMAGE,
                enabled=True,
                transport_mode=ProviderTransportMode.FAKE,
                model_name="fake-image-v1",
            )
        )
        self.storage = storage or ProviderOutputStorage()

    def submit(self, request: ProviderExecutionRequest) -> ProviderSubmissionReceipt:
        payload = {"prompt": request.prompt_contract.primary_prompt, "frame_profile": request.frame_profile}
        return ProviderSubmissionReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=f"fake_req_{request.provider_execution_request_id}",
            request_payload_hash=self._payload_hash(payload),
            idempotency_key=request.idempotency_key,
        )

    def poll(self, request: ProviderExecutionRequest, submission: ProviderSubmissionReceipt) -> ProviderPollReceipt:
        return ProviderPollReceipt(
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            provider_request_id=submission.provider_request_id,
            status=ProviderExecutionStatus.SUCCEEDED,
            provider_output_refs=["fake_inline_png"],
        )

    def download_outputs(self, request: ProviderExecutionRequest, poll: ProviderPollReceipt) -> list[ProviderOutputAsset]:
        output_type = ProviderOutputType.MASK if request.provider_capability_id == ProviderCapabilityId.MASK_GENERATE else ProviderOutputType.IMAGE
        asset = self.storage.save_bytes(
            brand_id=request.brand_id,
            request_id=request.provider_execution_request_id,
            provider_id=self.provider_id,
            data=_ONE_BY_ONE_PNG,
            filename=f"{output_type.value}.png",
            output_type=output_type,
            mime_type="image/png",
            metadata={"fake": True, "model": self.config.model_name},
        )
        return [asset]
