"""MOSS-TTS provider adapter boundary for TS-CMF-011."""

from __future__ import annotations

from uuid import uuid4

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.voice import ProviderReceipt


class MossTtsAdapter:
    provider_name = "moss_tts"

    def synthesize_bridge(self, *, text: str, voice_profile_ref: str) -> ProviderReceipt:
        return ProviderReceipt(
            schema_version="cmf.provider_receipt.v1",
            provider_receipt_id=uuid4(),
            provider_name=self.provider_name,
            operation="synthesize_voice_bridge",
            artifact_uri=f"provider://moss-tts/{uuid4()}.wav",
            metadata={"text_hash": str(abs(hash(text))), "voice_profile_ref": voice_profile_ref},
            created_at=utc_now(),
        )
