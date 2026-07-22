"""LavaSR provider adapter boundary for TS-CMF-011."""

from __future__ import annotations

from uuid import uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.voice import ProviderReceipt


class LavaSrAdapter:
    provider_name = "lavasr"

    def restore_audio(self, *, source_audio_uri: str) -> ProviderReceipt:
        return ProviderReceipt(
            schema_version="cmf.provider_receipt.v1",
            provider_receipt_id=uuid4(),
            provider_name=self.provider_name,
            operation="restore_audio",
            artifact_uri=f"provider://lavasr/{uuid4()}.wav",
            metadata={"source_audio_uri": source_audio_uri},
            created_at=utc_now(),
        )
