"""In-memory repository for Batch 2 asset and program compiler objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.asset_program_compilers import (
    AnimationStudioMigrationManifest,
    AvatarExportReceipt,
    AvatarExportWorkerJob,
    CarouselAtlasRouteReceipt,
    CarouselBuilderProgram,
    CarouselExportReceipt,
    CarouselSequencePlan,
    CarouselSlideLibrary,
    ContentSequenceProgram,
    ExpressionIngredientInventory,
    GeometricsSceneSpec,
    GoldenFixtureResult,
    HeadlessFrameRenderReceipt,
    HeadlessFrameRenderRequest,
    InterviewBriefV2Plan,
    LiveIngredientCoverageTracker,
    PackageLearningReceipt,
    RegistryBundleLoadReceipt,
    RigEditOperation,
    SequenceEvalReceipt,
    SequencingRegistryKernel,
    SingleImageEvalReviewReceipt,
    SingleImageProviderJobPlan,
    SingleImageRegistrySnapshot,
    SingleImageRouteDecision,
    SingleImageSkiaScene,
    SkiaRenderBinding,
    SkiaRenderReceipt,
    StillVisualLayerMaterialization,
    SuperVisualFamilyContract,
    TwoDCharacterGenesis,
    TwoDCharacterProviderAdapterDecision,
    TwoDCharacterRenderReceipt,
    TwoDCharacterRepairPlan,
    TwoDCharacterRig,
    TwoDCharacterSceneProgram,
    VideoEditProgram,
)


@dataclass
class InMemoryAssetProgramCompilerRepository:
    registry_load_receipts: dict[UUID, RegistryBundleLoadReceipt] = field(default_factory=dict)
    animation_migration_manifests: dict[UUID, AnimationStudioMigrationManifest] = field(default_factory=dict)
    rig_edit_operations: dict[UUID, RigEditOperation] = field(default_factory=dict)
    headless_frame_render_requests: dict[UUID, HeadlessFrameRenderRequest] = field(default_factory=dict)
    headless_frame_render_receipts: dict[UUID, HeadlessFrameRenderReceipt] = field(default_factory=dict)
    avatar_export_jobs: dict[UUID, AvatarExportWorkerJob] = field(default_factory=dict)
    avatar_export_receipts: dict[UUID, AvatarExportReceipt] = field(default_factory=dict)
    geometrics_scene_specs: dict[UUID, GeometricsSceneSpec] = field(default_factory=dict)
    skia_render_bindings: dict[UUID, SkiaRenderBinding] = field(default_factory=dict)
    skia_render_receipts: dict[UUID, SkiaRenderReceipt] = field(default_factory=dict)
    carousel_slide_libraries: dict[UUID, CarouselSlideLibrary] = field(default_factory=dict)
    carousel_sequence_plans: dict[UUID, CarouselSequencePlan] = field(default_factory=dict)
    carousel_builder_programs: dict[UUID, CarouselBuilderProgram] = field(default_factory=dict)
    carousel_export_receipts: dict[UUID, CarouselExportReceipt] = field(default_factory=dict)
    carousel_atlas_route_receipts: dict[UUID, CarouselAtlasRouteReceipt] = field(default_factory=dict)
    single_image_registry_snapshots: dict[UUID, SingleImageRegistrySnapshot] = field(default_factory=dict)
    single_image_route_decisions: dict[UUID, SingleImageRouteDecision] = field(default_factory=dict)
    supervisual_family_contracts: dict[UUID, SuperVisualFamilyContract] = field(default_factory=dict)
    single_image_provider_job_plans: dict[UUID, SingleImageProviderJobPlan] = field(default_factory=dict)
    still_visual_layer_materializations: dict[UUID, StillVisualLayerMaterialization] = field(default_factory=dict)
    single_image_skia_scenes: dict[UUID, SingleImageSkiaScene] = field(default_factory=dict)
    single_image_eval_review_receipts: dict[UUID, SingleImageEvalReviewReceipt] = field(default_factory=dict)
    golden_fixture_results: dict[UUID, GoldenFixtureResult] = field(default_factory=dict)
    video_edit_programs: dict[UUID, VideoEditProgram] = field(default_factory=dict)
    two_d_character_genesis_records: dict[UUID, TwoDCharacterGenesis] = field(default_factory=dict)
    two_d_character_rigs: dict[UUID, TwoDCharacterRig] = field(default_factory=dict)
    two_d_character_adapter_decisions: dict[UUID, TwoDCharacterProviderAdapterDecision] = field(default_factory=dict)
    two_d_character_scene_programs: dict[UUID, TwoDCharacterSceneProgram] = field(default_factory=dict)
    two_d_character_render_receipts: dict[UUID, TwoDCharacterRenderReceipt] = field(default_factory=dict)
    two_d_character_repair_plans: dict[UUID, TwoDCharacterRepairPlan] = field(default_factory=dict)
    sequencing_kernels: dict[UUID, SequencingRegistryKernel] = field(default_factory=dict)
    interview_brief_v2_plans: dict[UUID, InterviewBriefV2Plan] = field(default_factory=dict)
    live_coverage_trackers: dict[UUID, LiveIngredientCoverageTracker] = field(default_factory=dict)
    expression_ingredient_inventories: dict[UUID, ExpressionIngredientInventory] = field(default_factory=dict)
    content_sequence_programs: dict[UUID, ContentSequenceProgram] = field(default_factory=dict)
    sequence_eval_receipts: dict[UUID, SequenceEvalReceipt] = field(default_factory=dict)
    package_learning_receipts: dict[UUID, PackageLearningReceipt] = field(default_factory=dict)

    def put_registry_load_receipt(self, item: RegistryBundleLoadReceipt) -> RegistryBundleLoadReceipt:
        self.registry_load_receipts[item.registry_bundle_load_receipt_id] = item
        return item

    def put_animation_migration_manifest(self, item: AnimationStudioMigrationManifest) -> AnimationStudioMigrationManifest:
        self.animation_migration_manifests[item.animation_studio_migration_manifest_id] = item
        return item

    def put_rig_edit_operation(self, item: RigEditOperation) -> RigEditOperation:
        self.rig_edit_operations[item.rig_edit_operation_id] = item
        return item

    def put_headless_frame_render_request(self, item: HeadlessFrameRenderRequest) -> HeadlessFrameRenderRequest:
        self.headless_frame_render_requests[item.headless_frame_render_request_id] = item
        return item

    def put_headless_frame_render_receipt(self, item: HeadlessFrameRenderReceipt) -> HeadlessFrameRenderReceipt:
        self.headless_frame_render_receipts[item.headless_frame_render_receipt_id] = item
        return item

    def put_avatar_export_job(self, item: AvatarExportWorkerJob) -> AvatarExportWorkerJob:
        self.avatar_export_jobs[item.avatar_export_worker_job_id] = item
        return item

    def put_avatar_export_receipt(self, item: AvatarExportReceipt) -> AvatarExportReceipt:
        self.avatar_export_receipts[item.avatar_export_receipt_id] = item
        return item

    def put_geometrics_scene_spec(self, item: GeometricsSceneSpec) -> GeometricsSceneSpec:
        self.geometrics_scene_specs[item.geometrics_scene_spec_id] = item
        return item

    def put_skia_render_binding(self, item: SkiaRenderBinding) -> SkiaRenderBinding:
        self.skia_render_bindings[item.skia_render_binding_id] = item
        return item

    def put_skia_render_receipt(self, item: SkiaRenderReceipt) -> SkiaRenderReceipt:
        self.skia_render_receipts[item.skia_render_receipt_id] = item
        return item

    def put_carousel_slide_library(self, item: CarouselSlideLibrary) -> CarouselSlideLibrary:
        self.carousel_slide_libraries[item.carousel_slide_library_id] = item
        return item

    def put_carousel_sequence_plan(self, item: CarouselSequencePlan) -> CarouselSequencePlan:
        self.carousel_sequence_plans[item.carousel_sequence_plan_id] = item
        return item

    def put_carousel_builder_program(self, item: CarouselBuilderProgram) -> CarouselBuilderProgram:
        self.carousel_builder_programs[item.carousel_builder_program_id] = item
        return item

    def put_carousel_export_receipt(self, item: CarouselExportReceipt) -> CarouselExportReceipt:
        self.carousel_export_receipts[item.carousel_export_receipt_id] = item
        return item

    def put_carousel_atlas_route_receipt(self, item: CarouselAtlasRouteReceipt) -> CarouselAtlasRouteReceipt:
        self.carousel_atlas_route_receipts[item.carousel_atlas_route_receipt_id] = item
        return item

    def put_single_image_registry_snapshot(self, item: SingleImageRegistrySnapshot) -> SingleImageRegistrySnapshot:
        self.single_image_registry_snapshots[item.single_image_registry_snapshot_id] = item
        return item

    def put_single_image_route_decision(self, item: SingleImageRouteDecision) -> SingleImageRouteDecision:
        self.single_image_route_decisions[item.single_image_route_decision_id] = item
        return item

    def put_supervisual_family_contract(self, item: SuperVisualFamilyContract) -> SuperVisualFamilyContract:
        self.supervisual_family_contracts[item.supervisual_family_contract_id] = item
        return item

    def put_single_image_provider_job_plan(self, item: SingleImageProviderJobPlan) -> SingleImageProviderJobPlan:
        self.single_image_provider_job_plans[item.single_image_provider_job_plan_id] = item
        return item

    def put_still_visual_layer_materialization(self, item: StillVisualLayerMaterialization) -> StillVisualLayerMaterialization:
        self.still_visual_layer_materializations[item.still_visual_layer_materialization_id] = item
        return item

    def put_single_image_skia_scene(self, item: SingleImageSkiaScene) -> SingleImageSkiaScene:
        self.single_image_skia_scenes[item.single_image_skia_scene_id] = item
        return item

    def put_single_image_eval_review_receipt(self, item: SingleImageEvalReviewReceipt) -> SingleImageEvalReviewReceipt:
        self.single_image_eval_review_receipts[item.single_image_eval_review_receipt_id] = item
        return item

    def put_golden_fixture_result(self, item: GoldenFixtureResult) -> GoldenFixtureResult:
        self.golden_fixture_results[item.golden_fixture_result_id] = item
        return item

    def put_video_edit_program(self, item: VideoEditProgram) -> VideoEditProgram:
        self.video_edit_programs[item.video_edit_program_id] = item
        return item

    def put_two_d_character_genesis(self, item: TwoDCharacterGenesis) -> TwoDCharacterGenesis:
        self.two_d_character_genesis_records[item.two_d_character_genesis_id] = item
        return item

    def put_two_d_character_rig(self, item: TwoDCharacterRig) -> TwoDCharacterRig:
        self.two_d_character_rigs[item.two_d_character_rig_id] = item
        return item

    def put_two_d_character_adapter_decision(self, item: TwoDCharacterProviderAdapterDecision) -> TwoDCharacterProviderAdapterDecision:
        self.two_d_character_adapter_decisions[item.two_d_character_provider_adapter_decision_id] = item
        return item

    def put_two_d_character_scene_program(self, item: TwoDCharacterSceneProgram) -> TwoDCharacterSceneProgram:
        self.two_d_character_scene_programs[item.two_d_character_scene_program_id] = item
        return item

    def put_two_d_character_render_receipt(self, item: TwoDCharacterRenderReceipt) -> TwoDCharacterRenderReceipt:
        self.two_d_character_render_receipts[item.two_d_character_render_receipt_id] = item
        return item

    def put_two_d_character_repair_plan(self, item: TwoDCharacterRepairPlan) -> TwoDCharacterRepairPlan:
        self.two_d_character_repair_plans[item.two_d_character_repair_plan_id] = item
        return item

    def put_sequencing_kernel(self, item: SequencingRegistryKernel) -> SequencingRegistryKernel:
        self.sequencing_kernels[item.sequencing_registry_kernel_id] = item
        return item

    def put_interview_brief_v2_plan(self, item: InterviewBriefV2Plan) -> InterviewBriefV2Plan:
        self.interview_brief_v2_plans[item.interview_brief_v2_plan_id] = item
        return item

    def put_live_coverage_tracker(self, item: LiveIngredientCoverageTracker) -> LiveIngredientCoverageTracker:
        self.live_coverage_trackers[item.live_ingredient_coverage_tracker_id] = item
        return item

    def put_expression_ingredient_inventory(self, item: ExpressionIngredientInventory) -> ExpressionIngredientInventory:
        self.expression_ingredient_inventories[item.expression_ingredient_inventory_id] = item
        return item

    def put_content_sequence_program(self, item: ContentSequenceProgram) -> ContentSequenceProgram:
        self.content_sequence_programs[item.content_sequence_program_id] = item
        return item

    def put_sequence_eval_receipt(self, item: SequenceEvalReceipt) -> SequenceEvalReceipt:
        self.sequence_eval_receipts[item.sequence_eval_receipt_id] = item
        return item

    def put_package_learning_receipt(self, item: PackageLearningReceipt) -> PackageLearningReceipt:
        self.package_learning_receipts[item.package_learning_receipt_id] = item
        return item
