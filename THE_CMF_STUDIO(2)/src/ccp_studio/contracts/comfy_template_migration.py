"""ComfyUI template migration contracts for TS-CMF-046."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class WorkerAssetStatus(str, Enum):
    draft = "draft"
    active = "active"
    inactive = "inactive"
    revalidation_required = "revalidation_required"
    rejected = "rejected"


class ComfyWorkflowInputContract(BaseModel):
    schema_version: Literal["cmf.comfy_workflow_input_contract.v1"]
    input_name: str = Field(min_length=1)
    input_type: str = Field(min_length=1)
    required: bool = True
    validation_rule: str | None = None


class ComfyWorkflowOutputContract(BaseModel):
    schema_version: Literal["cmf.comfy_workflow_output_contract.v1"]
    output_contract: str = Field(min_length=1)
    version: str = Field(min_length=1)
    expected_artifact_types: list[str] = Field(min_length=1)


class TemplateCompatibilityNote(BaseModel):
    schema_version: Literal["cmf.template_compatibility_note.v1"]
    note_type: str = Field(min_length=1)
    note: str = Field(min_length=1)
    severity: str = Field(default="medium")


class MigratedComfyWorkflowAsset(BaseModel):
    schema_version: Literal["cmf.migrated_comfy_workflow_asset.v1"]
    comfy_workflow_asset_id: UUID
    legacy_source_path: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    storage_uri: str = Field(min_length=1)
    required_inputs: list[ComfyWorkflowInputContract] = Field(min_length=1)
    output_contract: ComfyWorkflowOutputContract
    compatibility_notes: list[TemplateCompatibilityNote] = Field(default_factory=list)
    known_defects: list[str] = Field(default_factory=list)
    eval_target: str = Field(min_length=1)
    eval_passed: bool
    reviewer_id: UUID
    status: WorkerAssetStatus
    created_at: datetime
    updated_at: datetime


class TemplateMigrationReceipt(BaseModel):
    schema_version: Literal["cmf.template_migration_receipt.v1"]
    template_migration_receipt_id: UUID
    comfy_workflow_asset_id: UUID | None = None
    legacy_source_path: str | None = None
    content_hash: str | None = None
    storage_uri: str | None = None
    required_input_names: list[str] = Field(default_factory=list)
    output_contract: str | None = None
    known_defects: list[str] = Field(default_factory=list)
    eval_target: str | None = None
    reviewer_id: UUID | None = None
    status: WorkerAssetStatus
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def comfy_template_hash(template_json: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(template_json, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_template_migration_receipt(
    *,
    actor_id: UUID,
    status: WorkerAssetStatus,
    decision_code: str,
    evidence_refs: list[str],
    asset: MigratedComfyWorkflowAsset | None = None,
    command_id: UUID | None = None,
) -> TemplateMigrationReceipt:
    return TemplateMigrationReceipt(
        schema_version="cmf.template_migration_receipt.v1",
        template_migration_receipt_id=uuid4(),
        comfy_workflow_asset_id=asset.comfy_workflow_asset_id if asset else None,
        legacy_source_path=asset.legacy_source_path if asset else None,
        content_hash=asset.content_hash if asset else None,
        storage_uri=asset.storage_uri if asset else None,
        required_input_names=[item.input_name for item in asset.required_inputs] if asset else [],
        output_contract=asset.output_contract.output_contract if asset else None,
        known_defects=asset.known_defects if asset else [],
        eval_target=asset.eval_target if asset else None,
        reviewer_id=asset.reviewer_id if asset else None,
        status=status,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
