from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

def _now_iso(): return datetime.now(timezone.utc).isoformat()
def new_id(prefix): return f"{prefix}_{uuid4().hex[:12]}"

class PassStatus(str, Enum): PASS='pass'; WARN='warn'; FAIL='fail'
class PipelineRecipeId(str, Enum):
    FORMAT02_GOLDEN_PATH='format02_golden_path'; AVATAR_LIBRARY_GENERATION='avatar_library_generation'; SUPERVISUAL_FROM_EXPRESSION_MOMENT='supervisual_from_expression_moment'; CAROUSEL_FROM_EXPRESSION_MOMENT='carousel_from_expression_moment'; FORMAT01_STORY_VIDEO='format01_story_video'
class PipelineStepKind(str, Enum):
    SOURCE_INTAKE='source_intake'; EXTRACTION='extraction'; FORMAT_COMPILE='format_compile'; COMPOSITION='composition'; AVATAR_ASSET='avatar_asset'; PROVIDER_SAMPLE='provider_sample'; PROVIDER_BATCH='provider_batch'; TIMELINE='timeline'; RENDER='render'; QA='qa'; REVIEW='review'; APPROVAL='approval'; EXPORT='export'; PUBLISH='publish'
class PipelineRunStatus(str, Enum): CREATED='created'; PLANNED='planned'; BLOCKED='blocked'; RUNNING='running'; SUCCEEDED='succeeded'; FAILED='failed'; CANCELLED='cancelled'
class PipelineStepStatus(str, Enum): PLANNED='planned'; BLOCKED='blocked'; RUNNING='running'; SUCCEEDED='succeeded'; FAILED='failed'; SKIPPED='skipped'; APPROVAL_REQUIRED='approval_required'
class PipelineArtifactRole(str, Enum): INPUT='input'; SOURCE_REF='source_ref'; INTERMEDIATE='intermediate'; PROVIDER_OUTPUT='provider_output'; RENDER_OUTPUT='render_output'; QA_RECEIPT='qa_receipt'; APPROVAL_RECEIPT='approval_receipt'; EXPORT='export'; TEMPLATE_PREVIEW='template_preview'; AVATAR_ASSET='avatar_asset'
class PipelineArtifactStorageState(str, Enum): POINTER_ONLY='pointer_only'; MATERIALIZED='materialized'
class PipelineApprovalGateType(str, Enum): OPERATOR_APPROVAL='operator_approval'; SAMPLE_FIRST='sample_first'; QA_PASS='qa_pass'; PUBLISH_APPROVAL='publish_approval'
class PipelineApprovalStatus(str, Enum): PENDING='pending'; APPROVED='approved'; REJECTED='rejected'; BLOCKED='blocked'
class PipelineBlockerSeverity(str, Enum): INFO='info'; WARNING='warning'; BLOCKING='blocking'

class PipelineRunBlocker(BaseModel):
    pipeline_run_blocker_id: str = Field(default_factory=lambda:new_id('pipeline_blocker'))
    code: str; message: str; severity: PipelineBlockerSeverity = PipelineBlockerSeverity.BLOCKING; step_id: str|None=None; recoverable: bool=True; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if not self.code or not self.message: raise ValueError('PipelineRunBlocker requires code and message')

class PipelineArtifactRef(BaseModel):
    pipeline_artifact_ref_id: str = Field(default_factory=lambda:new_id('pipeline_artifact'))
    role: PipelineArtifactRole; uri: str; source_ref_ids: list[str]=Field(default_factory=list)
    artifact_ref_id: str|None=None; provider_output_asset_ref_id: str|None=None; render_result_id: str|None=None; evaluation_receipt_id: str|None=None
    workspace_id: str|None=None; run_id: str|None=None; storage_state: PipelineArtifactStorageState=PipelineArtifactStorageState.POINTER_ONLY; sha256: str|None=None; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if not self.uri: raise ValueError('PipelineArtifactRef requires uri')
        if self.storage_state == PipelineArtifactStorageState.MATERIALIZED and not self.sha256: raise ValueError('Materialized PipelineArtifactRef requires sha256')

class PipelineApprovalGate(BaseModel):
    pipeline_approval_gate_id: str = Field(default_factory=lambda:new_id('pipeline_gate'))
    gate_id: str; gate_type: PipelineApprovalGateType; required: bool=True; status: PipelineApprovalStatus=PipelineApprovalStatus.PENDING; approved_by: str|None=None
    blockers: list[PipelineRunBlocker]=Field(default_factory=list); required_sample_types: list[str]=Field(default_factory=list); approved_sample_types: list[str]=Field(default_factory=list)
    @property
    def pass_status(self): return PassStatus.PASS if self.status == PipelineApprovalStatus.APPROVED and not self.blockers else PassStatus.FAIL
    def __init__(self, **d):
        super().__init__(**d)
        if not self.gate_id: raise ValueError('PipelineApprovalGate requires gate_id')
        if self.status == PipelineApprovalStatus.APPROVED and not self.approved_by: raise ValueError('Approved PipelineApprovalGate requires approved_by')
        if self.status == PipelineApprovalStatus.APPROVED and self.blockers: raise ValueError('Approved PipelineApprovalGate cannot contain blockers')
        if self.gate_type == PipelineApprovalGateType.SAMPLE_FIRST and self.status == PipelineApprovalStatus.APPROVED:
            if set(self.required_sample_types) - set(self.approved_sample_types): raise ValueError('Sample-first gate cannot approve until required sample types are approved')

class PipelineRecipeStep(BaseModel):
    step_id: str; display_name: str; step_kind: PipelineStepKind; required: bool=True; depends_on: list[str]=Field(default_factory=list)
    approval_gate_id: str|None=None; produces_artifact_roles: list[PipelineArtifactRole]=Field(default_factory=list); existing_service_refs: list[str]=Field(default_factory=list); orchestration_stage_ref: str|None=None
    def __init__(self, **d):
        super().__init__(**d)
        if not self.step_id: raise ValueError('PipelineRecipeStep requires step_id')
        if self.step_id in self.depends_on: raise ValueError('PipelineRecipeStep cannot depend on itself')

class PipelineRecipe(BaseModel):
    pipeline_recipe_id: str = Field(default_factory=lambda:new_id('pipeline_recipe'))
    recipe_id: PipelineRecipeId; version: str='1.0.0'; display_name: str; description: str; steps: list[PipelineRecipeStep]; approval_gates: list[PipelineApprovalGate]=Field(default_factory=list); required_input_artifact_roles: list[PipelineArtifactRole]=Field(default_factory=list); reuse_orchestration_spine: bool=True; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if not self.steps: raise ValueError('PipelineRecipe requires steps')
        ids=[s.step_id for s in self.steps]
        if len(ids)!=len(set(ids)): raise ValueError('PipelineRecipe cannot contain duplicate step ids')
        ids_set=set(ids)
        for s in self.steps:
            missing=set(s.depends_on)-ids_set
            if missing: raise ValueError(f'PipelineRecipe step {s.step_id} depends on missing steps: {sorted(missing)}')
        gates=[g.gate_id for g in self.approval_gates]
        if len(gates)!=len(set(gates)): raise ValueError('PipelineRecipe cannot contain duplicate approval gate ids')
        for s in self.steps:
            if s.approval_gate_id and s.approval_gate_id not in set(gates): raise ValueError(f'PipelineRecipe step {s.step_id} references missing approval gate')

class PipelineStepRun(BaseModel):
    pipeline_step_run_id: str = Field(default_factory=lambda:new_id('pipeline_step_run'))
    step_id: str; step_kind: PipelineStepKind; status: PipelineStepStatus=PipelineStepStatus.PLANNED; depends_on_step_ids: list[str]=Field(default_factory=list); input_artifact_ids: list[str]=Field(default_factory=list); output_artifact_ids: list[str]=Field(default_factory=list); approval_gate_id: str|None=None; orchestration_stage_execution_id: str|None=None; started_at: str|None=None; completed_at: str|None=None
    def __init__(self, **d):
        super().__init__(**d)
        if not self.step_id: raise ValueError('PipelineStepRun requires step_id')
        if self.status == PipelineStepStatus.SUCCEEDED and not self.completed_at: raise ValueError('Succeeded PipelineStepRun requires completed_at')

class PipelineStepReceipt(BaseModel):
    pipeline_step_receipt_id: str = Field(default_factory=lambda:new_id('pipeline_step_receipt'))
    pipeline_step_run_id: str; step_id: str; status: PipelineStepStatus; pass_status: PassStatus; output_artifact_ids: list[str]=Field(default_factory=list); blockers: list[PipelineRunBlocker]=Field(default_factory=list); message: str|None=None; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if self.blockers and self.pass_status == PassStatus.PASS: raise ValueError('PipelineStepReceipt cannot pass with blockers')
        if self.status == PipelineStepStatus.SUCCEEDED and self.pass_status == PassStatus.FAIL: raise ValueError('Succeeded PipelineStepReceipt cannot fail')

class PipelineOrchestrationSpineBinding(BaseModel):
    pipeline_orchestration_spine_binding_id: str = Field(default_factory=lambda:new_id('spine_binding'))
    orchestration_run_id: str; stage_plan_refs: dict[str,str]=Field(default_factory=dict); validation_contract_refs: dict[str,str]=Field(default_factory=dict); spine_available: bool=True
    def __init__(self, **d):
        super().__init__(**d)
        if not self.orchestration_run_id: raise ValueError('PipelineOrchestrationSpineBinding requires orchestration_run_id')

class PipelineRun(BaseModel):
    pipeline_run_id: str = Field(default_factory=lambda:new_id('pipeline_run'))
    recipe_id: PipelineRecipeId; recipe_version: str; brand_context_version_id: str; workspace_id: str|None=None; orchestration_run_id: str|None=None; status: PipelineRunStatus=PipelineRunStatus.CREATED; input_artifacts: list[PipelineArtifactRef]=Field(default_factory=list); step_runs: list[PipelineStepRun]=Field(default_factory=list); approval_gates: list[PipelineApprovalGate]=Field(default_factory=list); blockers: list[PipelineRunBlocker]=Field(default_factory=list); reuse_orchestration_spine: bool=True; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if not self.brand_context_version_id: raise ValueError('PipelineRun requires brand_context_version_id')
        if self.reuse_orchestration_spine and self.status in {PipelineRunStatus.PLANNED, PipelineRunStatus.RUNNING} and not self.orchestration_run_id: raise ValueError('Active PipelineRun must bind to orchestration_run_id')
        ids=[s.step_id for s in self.step_runs]
        if len(ids)!=len(set(ids)): raise ValueError('PipelineRun cannot contain duplicate step runs')

class PipelineRecipeValidationReceipt(BaseModel):
    pipeline_recipe_validation_receipt_id: str = Field(default_factory=lambda:new_id('recipe_validation'))
    recipe_id: PipelineRecipeId; pass_status: PassStatus; blockers: list[PipelineRunBlocker]=Field(default_factory=list)
    def __init__(self, **d):
        super().__init__(**d)
        if self.blockers and self.pass_status == PassStatus.PASS: raise ValueError('PipelineRecipeValidationReceipt cannot pass with blockers')

class PipelineRecipeCatalog(BaseModel):
    pipeline_recipe_catalog_id: str = Field(default_factory=lambda:new_id('recipe_catalog'))
    recipes: list[PipelineRecipe]
    def __init__(self, **d):
        super().__init__(**d)
        ids=[r.recipe_id for r in self.recipes]
        if len(ids)!=len(set(ids)): raise ValueError('PipelineRecipeCatalog cannot contain duplicate recipes')

class PipelineRunSummary(BaseModel):
    pipeline_run_summary_id: str = Field(default_factory=lambda:new_id('pipeline_summary'))
    pipeline_run_id: str; recipe_id: PipelineRecipeId; status: PipelineRunStatus; total_steps: int; succeeded_steps: int; failed_steps: int; blocked_steps: int; pending_approval_count: int; artifact_count: int; blockers: list[PipelineRunBlocker]=Field(default_factory=list); next_step_id: str|None=None; created_at: str=Field(default_factory=_now_iso)
    def __init__(self, **d):
        super().__init__(**d)
        if self.succeeded_steps + self.failed_steps + self.blocked_steps > self.total_steps: raise ValueError('PipelineRunSummary step counts exceed total_steps')
