from __future__ import annotations

from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


class FormatEnginePacketAdapterService:
    def __init__(self, service: FormatIntelligenceService | None = None):
        self.service = service or FormatIntelligenceService()

    def compile_payload(self, program):
        return self.service.compile_engine_adapter_payload(program)
