from __future__ import annotations

from ccp_studio.contracts.provider_adapters import ProviderId
from ccp_studio.providers.fake_image_adapter import FakeImageAdapter
from ccp_studio.providers.openai_image_adapter import OpenAIImageAdapter
from ccp_studio.providers.ideogram_adapter import IdeogramAdapter
from ccp_studio.providers.bfl_flux_adapter import BFLFluxAdapter
from ccp_studio.providers.qwen_image_adapter import QwenImageAdapter
from ccp_studio.providers.segment_anything_adapter import SegmentAnythingAdapter


class ProviderAdapterRegistry:
    def __init__(self):
        self._adapters = {
            ProviderId.FAKE_IMAGE: FakeImageAdapter(),
            ProviderId.OPENAI_IMAGE: OpenAIImageAdapter(),
            ProviderId.IDEOGRAM: IdeogramAdapter(),
            ProviderId.BFL_FLUX: BFLFluxAdapter(),
            ProviderId.QWEN_IMAGE: QwenImageAdapter(),
            ProviderId.SEGMENT_ANYTHING: SegmentAnythingAdapter(),
        }

    def get(self, provider_id: ProviderId):
        return self._adapters[provider_id]

    def register(self, provider_id: ProviderId, adapter) -> None:
        self._adapters[provider_id] = adapter

    def list_provider_ids(self) -> list[ProviderId]:
        return list(self._adapters.keys())
