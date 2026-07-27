from __future__ import annotations

from dataclasses import dataclass, field

from ccp_studio.contracts.style_route_runtime import (
    CACProductionSpec,
    GMGExpertSelection,
    GMGProductionSpec,
    GMGVerbatimNounMap,
    PaperCutArtifactSpec,
    PaperCutEditorialSpec,
    ProviderJobBlueprint,
    RouteProductionSpec,
    StyleRouteDecision,
    StyleRouteDecisionRequest,
    StyleRouteEvaluationReceipt,
    StyleRoutePreconditionReport,
    StyleRouteRepairInstruction,
    StyleRouteSourcePacket,
    StyleRouteUsageReceipt,
)


@dataclass
class InMemoryStyleRouteEngineRepository:
    requests: dict[str, StyleRouteDecisionRequest] = field(default_factory=dict)
    precondition_reports: dict[str, StyleRoutePreconditionReport] = field(default_factory=dict)
    decisions: dict[str, StyleRouteDecision] = field(default_factory=dict)
    source_packets: dict[str, StyleRouteSourcePacket] = field(default_factory=dict)
    noun_maps: dict[str, GMGVerbatimNounMap] = field(default_factory=dict)
    cac_specs: dict[str, CACProductionSpec] = field(default_factory=dict)
    gmg_selections: dict[str, GMGExpertSelection] = field(default_factory=dict)
    gmg_specs: dict[str, GMGProductionSpec] = field(default_factory=dict)
    paper_artifact_specs: dict[str, PaperCutArtifactSpec] = field(default_factory=dict)
    paper_editorial_specs: dict[str, PaperCutEditorialSpec] = field(default_factory=dict)
    route_specs: dict[str, RouteProductionSpec] = field(default_factory=dict)
    provider_blueprints: dict[str, ProviderJobBlueprint] = field(default_factory=dict)
    evaluation_receipts: dict[str, StyleRouteEvaluationReceipt] = field(default_factory=dict)
    repair_instructions: dict[str, StyleRouteRepairInstruction] = field(default_factory=dict)
    usage_receipts: dict[str, StyleRouteUsageReceipt] = field(default_factory=dict)

    def upsert_request(self, item: StyleRouteDecisionRequest) -> StyleRouteDecisionRequest:
        self.requests[item.style_route_decision_request_id] = item
        return item

    def upsert_precondition_report(self, item: StyleRoutePreconditionReport) -> StyleRoutePreconditionReport:
        self.precondition_reports[item.style_route_precondition_report_id] = item
        return item

    def upsert_decision(self, item: StyleRouteDecision) -> StyleRouteDecision:
        self.decisions[item.style_route_decision_id] = item
        return item

    def upsert_source_packet(self, item: StyleRouteSourcePacket) -> StyleRouteSourcePacket:
        self.source_packets[item.style_route_source_packet_id] = item
        return item

    def upsert_noun_map(self, item: GMGVerbatimNounMap) -> GMGVerbatimNounMap:
        self.noun_maps[item.gmg_verbatim_noun_map_id] = item
        return item

    def upsert_cac_spec(self, item: CACProductionSpec) -> CACProductionSpec:
        self.cac_specs[item.cac_production_spec_id] = item
        return item

    def upsert_gmg_selection(self, item: GMGExpertSelection) -> GMGExpertSelection:
        self.gmg_selections[item.gmg_expert_selection_id] = item
        return item

    def upsert_gmg_spec(self, item: GMGProductionSpec) -> GMGProductionSpec:
        self.gmg_specs[item.gmg_production_spec_id] = item
        return item

    def upsert_paper_artifact_spec(self, item: PaperCutArtifactSpec) -> PaperCutArtifactSpec:
        self.paper_artifact_specs[item.paper_cut_artifact_spec_id] = item
        return item

    def upsert_paper_editorial_spec(self, item: PaperCutEditorialSpec) -> PaperCutEditorialSpec:
        self.paper_editorial_specs[item.paper_cut_editorial_spec_id] = item
        return item

    def upsert_route_spec(self, item: RouteProductionSpec) -> RouteProductionSpec:
        self.route_specs[item.route_production_spec_id] = item
        return item

    def upsert_provider_blueprint(self, item: ProviderJobBlueprint) -> ProviderJobBlueprint:
        self.provider_blueprints[item.provider_job_blueprint_id] = item
        return item

    def upsert_evaluation(self, item: StyleRouteEvaluationReceipt) -> StyleRouteEvaluationReceipt:
        self.evaluation_receipts[item.style_route_evaluation_receipt_id] = item
        return item

    def upsert_repair_instruction(self, item: StyleRouteRepairInstruction) -> StyleRouteRepairInstruction:
        self.repair_instructions[item.style_route_repair_instruction_id] = item
        return item

    def upsert_usage(self, item: StyleRouteUsageReceipt) -> StyleRouteUsageReceipt:
        self.usage_receipts[item.style_route_usage_receipt_id] = item
        return item
