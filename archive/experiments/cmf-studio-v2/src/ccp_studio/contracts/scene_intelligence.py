"""Scene intelligence contracts for TS-CMF-041."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class BiologicalArcContainer(str, Enum):
    hook = "hook"
    setup = "setup"
    challenge = "challenge"
    turning_point = "turning_point"
    resolution = "resolution"
    vision = "vision"


class AssetRollRole(str, Enum):
    a_roll = "a_roll"
    b_roll = "b_roll"
    c_roll = "c_roll"
    d_roll = "d_roll"
    e_roll = "e_roll"


class SceneContainerPlan(BaseModel):
    schema_version: Literal["cmf.scene_container_plan.v1"]
    scene_container_plan_id: UUID
    scene_spec_id: UUID
    container: BiologicalArcContainer
    source_expression_moment_id: UUID
    selection_rationale: str = Field(min_length=1)
    constraints: list[str] = Field(min_length=1)
    registry_ref: str = Field(min_length=1)
    created_at: datetime


class SceneComponentSelection(BaseModel):
    schema_version: Literal["cmf.scene_component_selection.v1"]
    scene_component_selection_id: UUID
    scene_container_plan_id: UUID
    scene_spec_id: UUID
    component_registry_ref: str = Field(min_length=1)
    valid_for_container: bool
    satisfied_constraints: list[str] = Field(min_length=1)
    violated_constraints: list[str] = Field(default_factory=list)
    selection_rationale: str = Field(min_length=1)
    created_at: datetime


class CreativeSubsystemDecision(BaseModel):
    schema_version: Literal["cmf.creative_subsystem_decision.v1"]
    creative_subsystem_decision_id: UUID
    scene_spec_id: UUID
    subsystem_registry_ref: str = Field(min_length=1)
    decision: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    created_at: datetime


class AssetRollItem(BaseModel):
    schema_version: Literal["cmf.asset_roll_item.v1"]
    asset_roll_item_id: UUID
    role: AssetRollRole
    asset_ref: str | None = None
    function: str = Field(min_length=1)
    source_or_license_state: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class AssetRollPlan(BaseModel):
    schema_version: Literal["cmf.asset_roll_plan.v1"]
    asset_roll_plan_id: UUID
    scene_spec_id: UUID
    items: list[AssetRollItem] = Field(min_length=1)
    created_at: datetime


class SceneIntelligenceAuditView(BaseModel):
    schema_version: Literal["cmf.scene_intelligence_audit_view.v1"]
    scene_spec_id: UUID
    source_expression_moment_id: UUID
    asset_route_receipt_id: UUID
    scene_container_plan_id: UUID
    scene_component_selection_id: UUID
    creative_subsystem_decision_ids: list[UUID]
    asset_roll_plan_id: UUID
    composition_job_ids: list[UUID] = Field(default_factory=list)
    assembly_plan_ids: list[UUID] = Field(default_factory=list)
    sonic_plan_ids: list[UUID] = Field(default_factory=list)
    approval_event_ids: list[UUID] = Field(default_factory=list)


class SceneIntelligenceReceipt(BaseModel):
    schema_version: Literal["cmf.scene_intelligence_receipt.v1"]
    scene_intelligence_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    scene_spec_id: UUID | None = None
    scene_container_plan_id: UUID | None = None
    scene_component_selection_id: UUID | None = None
    creative_subsystem_decision_ids: list[UUID] = Field(default_factory=list)
    asset_roll_plan_id: UUID | None = None
    registry_versions: dict[str, str] = Field(default_factory=dict)
    validation_passed: bool
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def new_scene_intelligence_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    validation_passed: bool,
    decision_code: str,
    evidence_refs: list[str],
    scene_spec_id: UUID | None = None,
    scene_container_plan_id: UUID | None = None,
    scene_component_selection_id: UUID | None = None,
    creative_subsystem_decision_ids: list[UUID] | None = None,
    asset_roll_plan_id: UUID | None = None,
    registry_versions: dict[str, str] | None = None,
    command_id: UUID | None = None,
) -> SceneIntelligenceReceipt:
    return SceneIntelligenceReceipt(
        schema_version="cmf.scene_intelligence_receipt.v1",
        scene_intelligence_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        scene_spec_id=scene_spec_id,
        scene_container_plan_id=scene_container_plan_id,
        scene_component_selection_id=scene_component_selection_id,
        creative_subsystem_decision_ids=creative_subsystem_decision_ids or [],
        asset_roll_plan_id=asset_roll_plan_id,
        registry_versions=registry_versions or {},
        validation_passed=validation_passed,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
