"""In-memory repository for Batch 1 composition runtime objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.composition_runtime import (
    BeatMapCompilationReceipt,
    CompositionApprovalReadModel,
    CompositionBeatMap,
    CompositionEvalSuiteRun,
    CompositionOperatorApprovalReceipt,
    CompositionPreflightReceipt,
    CompositionRuntimeBinding,
    CompositionRuntimeBindingReceipt,
    CompositionTemplateApprovalReceipt,
    CompositionTemplateFamily,
    CompositionTemplateJson,
    ContentAssetCodeReservation,
    FourVideoFormatPlan,
    IdeogramProductionBridgeReceipt,
    IntegrationAdapterDecision,
    IntegrationCandidate,
    LayerExtractionResult,
    MicroSemioticAnchorSelection,
    OpenSourceTemplateConversion,
    PaperCutRuntimeManifest,
    PaperCutRuntimeReceipt,
    PerformanceStateSelection,
    RendererPropsCompilationReceipt,
    RendererPropsManifest,
    ResolvedBrandGenesisSubstrate,
    ReviewReadModel,
    SceneTemplateBinding,
    SceneTemplateBindingReceipt,
    VisualFeelContract,
)


@dataclass
class InMemoryCompositionRuntimeRepository:
    scene_template_bindings: dict[UUID, SceneTemplateBinding] = field(default_factory=dict)
    scene_template_binding_receipts: dict[UUID, SceneTemplateBindingReceipt] = field(default_factory=dict)
    composition_templates: dict[UUID, CompositionTemplateJson] = field(default_factory=dict)
    composition_template_approval_receipts: dict[UUID, CompositionTemplateApprovalReceipt] = field(default_factory=dict)
    approval_read_models: dict[UUID, CompositionApprovalReadModel] = field(default_factory=dict)
    integration_candidates: dict[UUID, IntegrationCandidate] = field(default_factory=dict)
    integration_adapter_decisions: dict[UUID, IntegrationAdapterDecision] = field(default_factory=dict)
    four_video_format_plans: dict[UUID, FourVideoFormatPlan] = field(default_factory=dict)
    visual_feel_contracts: dict[UUID, VisualFeelContract] = field(default_factory=dict)
    composition_preflight_receipts: dict[UUID, CompositionPreflightReceipt] = field(default_factory=dict)
    brand_genesis_substrates: dict[UUID, ResolvedBrandGenesisSubstrate] = field(default_factory=dict)
    beat_maps: dict[UUID, CompositionBeatMap] = field(default_factory=dict)
    beat_map_receipts: dict[UUID, BeatMapCompilationReceipt] = field(default_factory=dict)
    runtime_bindings: dict[UUID, CompositionRuntimeBinding] = field(default_factory=dict)
    runtime_binding_receipts: dict[UUID, CompositionRuntimeBindingReceipt] = field(default_factory=dict)
    template_families: dict[str, CompositionTemplateFamily] = field(default_factory=dict)
    asset_code_reservations: dict[str, ContentAssetCodeReservation] = field(default_factory=dict)
    performance_state_selections: dict[UUID, PerformanceStateSelection] = field(default_factory=dict)
    papercut_manifests: dict[UUID, PaperCutRuntimeManifest] = field(default_factory=dict)
    papercut_receipts: dict[UUID, PaperCutRuntimeReceipt] = field(default_factory=dict)
    micro_semiotic_anchor_selections: dict[UUID, MicroSemioticAnchorSelection] = field(default_factory=dict)
    ideogram_bridge_receipts: dict[UUID, IdeogramProductionBridgeReceipt] = field(default_factory=dict)
    layer_extraction_results: dict[UUID, LayerExtractionResult] = field(default_factory=dict)
    renderer_props_manifests: dict[UUID, RendererPropsManifest] = field(default_factory=dict)
    renderer_props_receipts: dict[UUID, RendererPropsCompilationReceipt] = field(default_factory=dict)
    open_source_template_conversions: dict[UUID, OpenSourceTemplateConversion] = field(default_factory=dict)
    eval_suite_runs: dict[UUID, CompositionEvalSuiteRun] = field(default_factory=dict)
    review_read_models: dict[UUID, ReviewReadModel] = field(default_factory=dict)
    operator_approval_receipts: dict[UUID, CompositionOperatorApprovalReceipt] = field(default_factory=dict)

    def put_scene_template_binding(self, item: SceneTemplateBinding) -> SceneTemplateBinding:
        self.scene_template_bindings[item.scene_template_binding_id] = item
        return item

    def put_scene_template_binding_receipt(self, item: SceneTemplateBindingReceipt) -> SceneTemplateBindingReceipt:
        self.scene_template_binding_receipts[item.scene_template_binding_receipt_id] = item
        return item

    def put_composition_template(self, item: CompositionTemplateJson) -> CompositionTemplateJson:
        self.composition_templates[item.composition_template_id] = item
        return item

    def put_template_approval_receipt(self, item: CompositionTemplateApprovalReceipt) -> CompositionTemplateApprovalReceipt:
        self.composition_template_approval_receipts[item.composition_template_approval_receipt_id] = item
        return item

    def put_approval_read_model(self, item: CompositionApprovalReadModel) -> CompositionApprovalReadModel:
        self.approval_read_models[item.review_read_model_id] = item
        return item

    def put_integration_candidate(self, item: IntegrationCandidate) -> IntegrationCandidate:
        self.integration_candidates[item.integration_candidate_id] = item
        return item

    def put_integration_adapter_decision(self, item: IntegrationAdapterDecision) -> IntegrationAdapterDecision:
        self.integration_adapter_decisions[item.integration_adapter_decision_id] = item
        return item

    def put_four_video_format_plan(self, item: FourVideoFormatPlan) -> FourVideoFormatPlan:
        self.four_video_format_plans[item.four_video_format_plan_id] = item
        return item

    def put_visual_feel_contract(self, item: VisualFeelContract) -> VisualFeelContract:
        self.visual_feel_contracts[item.visual_feel_contract_id] = item
        return item

    def put_composition_preflight_receipt(self, item: CompositionPreflightReceipt) -> CompositionPreflightReceipt:
        self.composition_preflight_receipts[item.composition_preflight_receipt_id] = item
        return item

    def put_brand_genesis_substrate(self, item: ResolvedBrandGenesisSubstrate) -> ResolvedBrandGenesisSubstrate:
        self.brand_genesis_substrates[item.resolved_brand_genesis_substrate_id] = item
        return item

    def put_beat_map(self, item: CompositionBeatMap) -> CompositionBeatMap:
        self.beat_maps[item.composition_beat_map_id] = item
        return item

    def put_beat_map_receipt(self, item: BeatMapCompilationReceipt) -> BeatMapCompilationReceipt:
        self.beat_map_receipts[item.beat_map_compilation_receipt_id] = item
        return item

    def put_runtime_binding(self, item: CompositionRuntimeBinding) -> CompositionRuntimeBinding:
        self.runtime_bindings[item.composition_runtime_binding_id] = item
        return item

    def put_runtime_binding_receipt(self, item: CompositionRuntimeBindingReceipt) -> CompositionRuntimeBindingReceipt:
        self.runtime_binding_receipts[item.composition_runtime_binding_receipt_id] = item
        return item

    def put_template_family(self, item: CompositionTemplateFamily) -> CompositionTemplateFamily:
        self.template_families[item.family_code] = item
        return item

    def put_asset_code_reservation(self, item: ContentAssetCodeReservation) -> ContentAssetCodeReservation:
        self.asset_code_reservations[item.content_asset_code] = item
        return item

    def put_performance_state_selection(self, item: PerformanceStateSelection) -> PerformanceStateSelection:
        self.performance_state_selections[item.performance_state_selection_id] = item
        return item

    def put_papercut_manifest(self, item: PaperCutRuntimeManifest) -> PaperCutRuntimeManifest:
        self.papercut_manifests[item.papercut_runtime_manifest_id] = item
        return item

    def put_papercut_receipt(self, item: PaperCutRuntimeReceipt) -> PaperCutRuntimeReceipt:
        self.papercut_receipts[item.papercut_runtime_receipt_id] = item
        return item

    def put_micro_semiotic_anchor_selection(self, item: MicroSemioticAnchorSelection) -> MicroSemioticAnchorSelection:
        self.micro_semiotic_anchor_selections[item.micro_semiotic_anchor_selection_id] = item
        return item

    def put_ideogram_bridge_receipt(self, item: IdeogramProductionBridgeReceipt) -> IdeogramProductionBridgeReceipt:
        self.ideogram_bridge_receipts[item.ideogram_production_bridge_receipt_id] = item
        return item

    def put_layer_extraction_result(self, item: LayerExtractionResult) -> LayerExtractionResult:
        self.layer_extraction_results[item.layer_extraction_result_id] = item
        return item

    def put_renderer_props_manifest(self, item: RendererPropsManifest) -> RendererPropsManifest:
        self.renderer_props_manifests[item.renderer_props_manifest_id] = item
        return item

    def put_renderer_props_receipt(self, item: RendererPropsCompilationReceipt) -> RendererPropsCompilationReceipt:
        self.renderer_props_receipts[item.renderer_props_compilation_receipt_id] = item
        return item

    def put_open_source_template_conversion(self, item: OpenSourceTemplateConversion) -> OpenSourceTemplateConversion:
        self.open_source_template_conversions[item.open_source_template_conversion_id] = item
        return item

    def put_eval_suite_run(self, item: CompositionEvalSuiteRun) -> CompositionEvalSuiteRun:
        self.eval_suite_runs[item.composition_eval_suite_run_id] = item
        return item

    def put_review_read_model(self, item: ReviewReadModel) -> ReviewReadModel:
        self.review_read_models[item.review_read_model_id] = item
        return item

    def put_operator_approval_receipt(self, item: CompositionOperatorApprovalReceipt) -> CompositionOperatorApprovalReceipt:
        self.operator_approval_receipts[item.composition_operator_approval_receipt_id] = item
        return item
