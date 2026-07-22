from __future__ import annotations

from ccp_studio.services.format_intelligence_service import FormatIntelligenceService


class FormatSubFormatRouterService:
    def __init__(self, service: FormatIntelligenceService | None = None):
        self.service = service or FormatIntelligenceService()

    def route(self, packet):
        return self.service.route_sub_format(packet)
