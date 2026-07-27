from __future__ import annotations

from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


class FormatProgramCompilerService:
    def __init__(self, service: FormatIntelligenceService | None = None):
        self.service = service or FormatIntelligenceService()

    def compile(self, context, packet):
        return self.service.compile_format_program(context, packet)
