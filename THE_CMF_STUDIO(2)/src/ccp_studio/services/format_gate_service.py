from __future__ import annotations

from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


class FormatGateService:
    def __init__(self, service: FormatIntelligenceService | None = None):
        self.service = service or FormatIntelligenceService()

    def authorize(self, program):
        return self.service.authorize_format_program(program)
