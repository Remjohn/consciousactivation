from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class GoldenPathStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    PASS = "pass"
    FAIL = "fail"


class GoldenPathStageName(str, Enum):
    FIXTURE_LOAD = "fixture_load"
    EXTRACTION_COMPILE = "extraction_compile"
    FORMAT_PROGRAM_COMPILE = "format_program_compile"
    COMPOSITION_SCENES_COMPILE = "composition_scenes_compile"
    AVATAR_PLANS_COMPILE = "avatar_plans_compile"
    VIDEO_TIMELINE_COMPILE = "video_timeline_compile"
    FAKE_RENDER_COMPILE = "fake_render_compile"
    EVAL_RUN = "eval_run"
    EXPORT_COMPILE = "export_compile"


class GoldenPathRecipeSpec(BaseModel):
    recipe_id: str = "format02_health_myth_golden_path_v1"
    name: str = "Format 02 Health Myth Golden Path"
    format_id: str = "format_02_avatar_papercut_explainer"
    expected_scene_count: int = 8
    stage_names: list[GoldenPathStageName] = Field(default_factory=lambda: list(GoldenPathStageName))
    fake_render_only: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.fake_render_only:
            raise ValueError("Golden Path V1 is fake-render only")


class Format02GoldenPathSceneSeed(BaseModel):
    scene_id: str
    scene_role: str
    concept_statement: str
    headline_text: str
    audience_proxy: str
    audience_proxy_sfl_function: str
    hero_object_asset_id: str
    hero_object_source_ref: str
    hero_object_role: str = "hero_object"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.scene_id or not self.concept_statement or not self.headline_text:
            raise ValueError("Scene seed requires scene_id, concept_statement, and headline_text")
        if not self.audience_proxy_sfl_function:
            raise ValueError("Scene seed requires audience proxy SFL function")


class Format02GoldenPathInput(BaseModel):
    golden_path_input_id: str = Field(default_factory=lambda: new_id("golden_input"))
    brand_id: str
    brand_context_version_id: str
    source_truth: str
    transcript_text: str
    interview_brief: dict[str, Any]
    scene_seeds: list[Format02GoldenPathSceneSeed]
    source_span_refs: list[str] = Field(default_factory=lambda: ["span_1"])

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.source_span_refs:
            raise ValueError("source_span_refs are required")
        if len(self.scene_seeds) != 8:
            raise ValueError("Format 02 Golden Path requires exactly 8 scene seeds")


class GoldenPathStageResult(BaseModel):
    golden_path_stage_result_id: str = Field(default_factory=lambda: new_id("golden_stage"))
    stage_name: GoldenPathStageName
    status: GoldenPathStatus
    output_refs: dict[str, Any] = Field(default_factory=dict)
    receipt_refs: dict[str, Any] = Field(default_factory=dict)
    blockers: list[str] = Field(default_factory=list)
    started_at: str = Field(default_factory=_now_iso)
    completed_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.status == GoldenPathStatus.PASS:
            raise ValueError("Stage with blockers cannot pass")


class GoldenPathObjectSpineMap(BaseModel):
    golden_path_object_spine_map_id: str = Field(default_factory=lambda: new_id("spine_map"))
    brand_context_version_id: str
    source_expression_session_ref: str | None = None
    complete_editing_session_ref: str | None = None
    expression_moment_refs: list[str] = Field(default_factory=list)
    asset_route_receipt_refs: list[str] = Field(default_factory=list)
    scene_spec_refs: list[str] = Field(default_factory=list)
    composition_job_refs: list[str] = Field(default_factory=list)
    render_output_refs: list[str] = Field(default_factory=list)
    evaluation_receipt_refs: list[str] = Field(default_factory=list)
    approval_event_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required in object spine map")


class Format02GoldenPathOutput(BaseModel):
    format02_golden_path_output_id: str = Field(default_factory=lambda: new_id("golden_output"))
    brand_context_version_id: str
    source_span_refs: list[str]
    extraction_packet_id: str
    format_program_id: str
    format_program_authorized: bool
    scene_program_ids: list[str]
    composition_decision_receipt_ids: list[str]
    composition_locked_count: int
    avatar_performance_plan_ids: list[str]
    audience_proxy_plan_ids: list[str]
    video_timeline_program_id: str
    remotion_input_props_id: str
    otio_audit_timeline_id: str
    proxy_render_receipt_id: str
    evaluation_receipt_id: str
    final_render_receipt_id: str
    approval_packet_id: str
    export_pack_id: str
    no_lip_sync: bool
    fake_render_only: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.scene_program_ids) != 8:
            raise ValueError("Golden path output requires 8 scene programs")
        if len(self.avatar_performance_plan_ids) != 8:
            raise ValueError("Golden path output requires 8 avatar plans")
        if len(self.audience_proxy_plan_ids) != 8:
            raise ValueError("Golden path output requires 8 audience proxy plans")
        if self.composition_locked_count != 8:
            raise ValueError("All 8 compositions must lock")
        if not self.no_lip_sync:
            raise ValueError("Golden path requires no lip sync")
        if not self.source_span_refs:
            raise ValueError("Golden path output requires source_span_refs")


class GoldenPathBlocker(BaseModel):
    golden_path_blocker_id: str = Field(default_factory=lambda: new_id("golden_blocker"))
    stage_name: GoldenPathStageName
    code: str
    message: str


class GoldenPathReceipt(BaseModel):
    golden_path_receipt_id: str = Field(default_factory=lambda: new_id("golden_receipt"))
    run_id: str
    pass_status: GoldenPathStatus
    stage_result_ids: list[str]
    output_id: str | None = None
    blockers: list[GoldenPathBlocker] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.pass_status == GoldenPathStatus.PASS:
            raise ValueError("GoldenPathReceipt with blockers cannot pass")


class GoldenPathRun(BaseModel):
    golden_path_run_id: str = Field(default_factory=lambda: new_id("golden_run"))
    recipe: GoldenPathRecipeSpec
    input: Format02GoldenPathInput
    stage_results: list[GoldenPathStageResult] = Field(default_factory=list)
    object_spine_map: GoldenPathObjectSpineMap | None = None
    output: Format02GoldenPathOutput | None = None
    receipt: GoldenPathReceipt | None = None
    status: GoldenPathStatus = GoldenPathStatus.CREATED
    created_at: str = Field(default_factory=_now_iso)
