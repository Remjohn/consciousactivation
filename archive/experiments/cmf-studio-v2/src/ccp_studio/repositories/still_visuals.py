"""In-memory repository for still visual parent programs."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.still_visuals import (
    ProviderMaterializationPlan,
    StillVisualApprovalReceipt,
    StillVisualCompositionProgram,
    StillVisualEvalSummary,
    StillVisualExportManifest,
    StillVisualFamilyRoute,
    StillVisualRenderManifest,
    StillVisualReviewReadModel,
    StillVisualRevisionCommand,
    TelegramStillVisualReviewCard,
)
from ccp_studio.contracts.supervisual_grammar import (
    SuperVisualFeelMatrixEntry,
    SuperVisualGrammarRecord,
    SuperVisualGrammarRouteDecision,
    SuperVisualPrimitiveCoverageReceipt,
)


@dataclass
class InMemoryStillVisualRepository:
    programs: dict[UUID, StillVisualCompositionProgram] = field(default_factory=dict)
    routes: dict[UUID, StillVisualFamilyRoute] = field(default_factory=dict)
    provider_plans: dict[UUID, ProviderMaterializationPlan] = field(default_factory=dict)
    render_manifests: dict[UUID, StillVisualRenderManifest] = field(default_factory=dict)
    eval_summaries: dict[UUID, StillVisualEvalSummary] = field(default_factory=dict)
    review_read_models: dict[UUID, StillVisualReviewReadModel] = field(default_factory=dict)
    telegram_cards: dict[UUID, TelegramStillVisualReviewCard] = field(default_factory=dict)
    approval_receipts: dict[UUID, StillVisualApprovalReceipt] = field(default_factory=dict)
    revision_commands: dict[UUID, StillVisualRevisionCommand] = field(default_factory=dict)
    export_manifests: dict[UUID, StillVisualExportManifest] = field(default_factory=dict)
    grammar_records: dict[str, SuperVisualGrammarRecord] = field(default_factory=dict)
    feel_matrix_entries: dict[str, SuperVisualFeelMatrixEntry] = field(default_factory=dict)
    grammar_route_decisions: dict[UUID, SuperVisualGrammarRouteDecision] = field(default_factory=dict)
    primitive_coverage_receipts: dict[UUID, SuperVisualPrimitiveCoverageReceipt] = field(default_factory=dict)

    def put_program(self, item: StillVisualCompositionProgram) -> StillVisualCompositionProgram:
        self.programs[item.still_visual_composition_program_id] = item
        return item

    def put_route(self, item: StillVisualFamilyRoute) -> StillVisualFamilyRoute:
        self.routes[item.still_visual_family_route_id] = item
        return item

    def put_provider_plan(self, item: ProviderMaterializationPlan) -> ProviderMaterializationPlan:
        self.provider_plans[item.provider_materialization_plan_id] = item
        return item

    def put_render_manifest(self, item: StillVisualRenderManifest) -> StillVisualRenderManifest:
        self.render_manifests[item.still_visual_render_manifest_id] = item
        return item

    def put_eval_summary(self, item: StillVisualEvalSummary) -> StillVisualEvalSummary:
        self.eval_summaries[item.still_visual_eval_summary_id] = item
        return item

    def put_review_read_model(self, item: StillVisualReviewReadModel) -> StillVisualReviewReadModel:
        self.review_read_models[item.still_visual_review_read_model_id] = item
        return item

    def put_telegram_card(self, item: TelegramStillVisualReviewCard) -> TelegramStillVisualReviewCard:
        self.telegram_cards[item.telegram_still_visual_review_card_id] = item
        return item

    def put_approval_receipt(self, item: StillVisualApprovalReceipt) -> StillVisualApprovalReceipt:
        self.approval_receipts[item.still_visual_approval_receipt_id] = item
        return item

    def put_revision_command(self, item: StillVisualRevisionCommand) -> StillVisualRevisionCommand:
        self.revision_commands[item.still_visual_revision_command_id] = item
        return item

    def put_export_manifest(self, item: StillVisualExportManifest) -> StillVisualExportManifest:
        self.export_manifests[item.still_visual_export_manifest_id] = item
        return item

    def put_grammar_record(self, item: SuperVisualGrammarRecord) -> SuperVisualGrammarRecord:
        self.grammar_records[item.grammar_code] = item
        return item

    def put_feel_matrix_entry(self, item: SuperVisualFeelMatrixEntry) -> SuperVisualFeelMatrixEntry:
        self.feel_matrix_entries[item.subtype] = item
        return item

    def put_grammar_route_decision(self, item: SuperVisualGrammarRouteDecision) -> SuperVisualGrammarRouteDecision:
        self.grammar_route_decisions[item.supervisual_grammar_route_decision_id] = item
        return item

    def put_primitive_coverage_receipt(self, item: SuperVisualPrimitiveCoverageReceipt) -> SuperVisualPrimitiveCoverageReceipt:
        self.primitive_coverage_receipts[item.supervisual_primitive_coverage_receipt_id] = item
        return item
