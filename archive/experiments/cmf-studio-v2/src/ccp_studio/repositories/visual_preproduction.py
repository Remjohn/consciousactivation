from __future__ import annotations

from dataclasses import dataclass, field

from ccp_studio.contracts.visual_preproduction import (
    ConstraintGateCReport,
    PRIMALAnalysis,
    StoryboardCommanderVerdict,
    StoryboardIngredientSet,
    VAEDecoderReport,
    VisualAnalystReport,
    VisualBeatPlan,
    VisualPreproductionPacket,
    VisualPreproductionRequest,
    VisualSchema,
)


@dataclass
class InMemoryVisualPreproductionRepository:
    requests: dict[str, VisualPreproductionRequest] = field(default_factory=dict)
    visual_schemas: dict[str, VisualSchema] = field(default_factory=dict)
    ingredient_sets: dict[str, StoryboardIngredientSet] = field(default_factory=dict)
    beat_plans: dict[str, VisualBeatPlan] = field(default_factory=dict)
    primal_reports: dict[str, PRIMALAnalysis] = field(default_factory=dict)
    vae_reports: dict[str, VAEDecoderReport] = field(default_factory=dict)
    gate_c_reports: dict[str, ConstraintGateCReport] = field(default_factory=dict)
    analyst_reports: dict[str, VisualAnalystReport] = field(default_factory=dict)
    commander_verdicts: dict[str, StoryboardCommanderVerdict] = field(default_factory=dict)
    packets: dict[str, VisualPreproductionPacket] = field(default_factory=dict)

    def upsert_request(self, request: VisualPreproductionRequest) -> VisualPreproductionRequest:
        self.requests[request.visual_preproduction_request_id] = request
        return request

    def upsert_visual_schema(self, schema: VisualSchema) -> VisualSchema:
        self.visual_schemas[schema.visual_schema_id] = schema
        return schema

    def upsert_ingredient_set(self, ingredients: StoryboardIngredientSet) -> StoryboardIngredientSet:
        self.ingredient_sets[ingredients.storyboard_ingredient_set_id] = ingredients
        return ingredients

    def upsert_beat_plan(self, beat_plan: VisualBeatPlan) -> VisualBeatPlan:
        self.beat_plans[beat_plan.visual_beat_plan_id] = beat_plan
        return beat_plan

    def upsert_primal(self, primal: PRIMALAnalysis) -> PRIMALAnalysis:
        self.primal_reports[primal.primal_analysis_id] = primal
        return primal

    def upsert_vae(self, vae: VAEDecoderReport) -> VAEDecoderReport:
        self.vae_reports[vae.vae_decoder_report_id] = vae
        return vae

    def upsert_gate_c(self, report: ConstraintGateCReport) -> ConstraintGateCReport:
        self.gate_c_reports[report.constraint_gate_c_report_id] = report
        return report

    def upsert_analyst_report(self, report: VisualAnalystReport) -> VisualAnalystReport:
        self.analyst_reports[report.visual_analyst_report_id] = report
        return report

    def upsert_commander_verdict(self, verdict: StoryboardCommanderVerdict) -> StoryboardCommanderVerdict:
        self.commander_verdicts[verdict.storyboard_commander_verdict_id] = verdict
        return verdict

    def upsert_packet(self, packet: VisualPreproductionPacket) -> VisualPreproductionPacket:
        self.packets[packet.visual_preproduction_packet_id] = packet
        return packet
