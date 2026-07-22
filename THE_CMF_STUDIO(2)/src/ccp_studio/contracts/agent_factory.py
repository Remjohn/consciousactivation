"""Agent Factory runtime contracts for TS-CMF-062 through TS-CMF-069."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.skills import SkillUseMode


PERSONA_CODE_PATTERN = re.compile(r"^(?P<department>[A-Z0-9]{3})-(?P<service>[A-Z0-9]{7})-(?P<entity_type>[A-Z]{2})$")


class EntityTypeCode(str, Enum):
    AG = "AG"
    SA = "SA"
    HK = "HK"
    EX = "EX"
    SK = "SK"
    JS = "JS"
    EV = "EV"
    RG = "RG"


class AgentActivationState(str, Enum):
    draft = "draft"
    ready_for_eval = "ready_for_eval"
    active = "active"
    blocked = "blocked"
    deprecated = "deprecated"


class SkillBindingType(str, Enum):
    stable = "stable"
    jit = "jit"


class LifecycleBoundary(str, Enum):
    before_stage = "before_stage"
    after_stage = "after_stage"
    before_tool = "before_tool"
    after_tool = "after_tool"
    before_provider_job = "before_provider_job"
    after_provider_job = "after_provider_job"
    before_review = "before_review"
    before_publishing = "before_publishing"
    before_memory_admission = "before_memory_admission"


class ToolCapabilityKind(str, Enum):
    command = "command"
    query = "query"
    workflow_signal = "workflow_signal"
    dspy_program = "dspy_program"
    provider_adapter = "provider_adapter"
    renderer = "renderer"
    review_action = "review_action"
    projection = "projection"


class AdapterExportTarget(str, Enum):
    google_adk = "google_adk"
    agents_cli = "agents_cli"


class PersonaCodeParts(BaseModel):
    schema_version: Literal["cmf.persona_code_parts.v1"] = "cmf.persona_code_parts.v1"
    department_code: str = Field(min_length=3, max_length=3)
    service_code: str = Field(min_length=7, max_length=7)
    entity_type: EntityTypeCode
    rendered_code: str = Field(min_length=11)


class PersonaRegistryEntry(BaseModel):
    schema_version: Literal["cmf.persona_registry_entry.v1"] = "cmf.persona_registry_entry.v1"
    persona_registry_entry_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-[A-Z]{2}$")
    department_code: str = Field(min_length=3, max_length=3)
    service_code: str = Field(min_length=7, max_length=7)
    entity_type: EntityTypeCode
    display_name: str = Field(min_length=1)
    persona_name: str | None = None
    service_scope: str = Field(min_length=1)
    source_refs: list[str] = Field(min_length=1)
    active: bool = True


class PersonaRegistryReceipt(BaseModel):
    schema_version: Literal["cmf.persona_registry_receipt.v1"] = "cmf.persona_registry_receipt.v1"
    receipt_id: UUID
    entity_code: str = Field(min_length=1)
    decision_code: Literal["accepted", "rejected", "updated", "deactivated"]
    evidence_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    created_at: datetime


class DepartmentSpec(BaseModel):
    schema_version: Literal["cmf.department_spec.v1"] = "cmf.department_spec.v1"
    department_key: str = Field(min_length=3, max_length=3)
    display_name: str = Field(min_length=1)
    pipeline_stage_refs: list[str] = Field(min_length=1)
    owned_object_types: list[str] = Field(min_length=1)
    proof_obligations: list[str] = Field(min_length=1)


class MemoryAccessPolicy(BaseModel):
    schema_version: Literal["cmf.memory_access_policy.v1"] = "cmf.memory_access_policy.v1"
    policy_ref: str = Field(min_length=1)
    scope: Literal["none", "current_object", "current_guest", "current_brand", "approved_cross_guest"]
    allowed_memory_families: list[str] = Field(default_factory=list)
    write_requires_command: bool = True


class AgentRoleSpec(BaseModel):
    schema_version: Literal["cmf.agent_role_spec.v1"] = "cmf.agent_role_spec.v1"
    agent_role_spec_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-AG$")
    department_key: str = Field(min_length=3, max_length=3)
    service_code: str = Field(min_length=7, max_length=7)
    display_name: str = Field(min_length=1)
    persona_name: str | None = None
    goal: str = Field(min_length=1)
    fit_rationale: str = Field(min_length=1)
    pipeline_stage_refs: list[str] = Field(min_length=1)
    active_object_types: list[str] = Field(min_length=1)
    entry_object_contracts: list[str] = Field(min_length=1)
    exit_object_contracts: list[str] = Field(min_length=1)
    allowed_tool_refs: list[str] = Field(min_length=1)
    stable_skill_refs: list[str] = Field(default_factory=list)
    jit_skill_mode_refs: list[SkillUseMode] = Field(default_factory=list)
    sub_agent_refs: list[str] = Field(default_factory=list)
    hook_refs: list[str] = Field(default_factory=list)
    eval_refs: list[str] = Field(min_length=1)
    memory_access_policy_ref: str = Field(min_length=1)
    blocked_actions: list[str] = Field(min_length=1)
    required_receipt_types: list[str] = Field(min_length=1)
    readiness_eval_id: UUID | None = None
    activation_state: AgentActivationState = AgentActivationState.draft
    generated_adapter_hash: str | None = None


class AgentRoleSpecReceipt(BaseModel):
    schema_version: Literal["cmf.agent_role_spec_receipt.v1"] = "cmf.agent_role_spec_receipt.v1"
    receipt_id: UUID
    agent_role_spec_id: UUID
    entity_code: str = Field(min_length=1)
    decision_code: Literal["registered", "activated", "blocked", "deactivated"]
    readiness_eval_id: UUID | None = None
    validation_results: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    created_at: datetime


class SubAgentRoleSpec(BaseModel):
    schema_version: Literal["cmf.sub_agent_role_spec.v1"] = "cmf.sub_agent_role_spec.v1"
    sub_agent_role_spec_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-SA$")
    parent_agent_refs: list[str] = Field(min_length=1)
    invocation_conditions: list[str] = Field(min_length=1)
    input_model_ref: str = Field(min_length=1)
    output_model_ref: str = Field(min_length=1)
    allowed_context_fields: list[str] = Field(min_length=1)
    allowed_tool_refs: list[str] = Field(default_factory=list)
    mutation_policy: Literal["read_only", "parent_delegated_command_only"] = "read_only"
    required_evidence_refs: list[str] = Field(min_length=1)
    blocked_actions: list[str] = Field(min_length=1)
    receipt_type: str = Field(min_length=1)
    active: bool = True


class SubAgentInvocationRequest(BaseModel):
    schema_version: Literal["cmf.sub_agent_invocation_request.v1"] = "cmf.sub_agent_invocation_request.v1"
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    parent_agent_code: str = Field(min_length=1)
    sub_agent_code: str = Field(min_length=1)
    requested_task: str = Field(min_length=1)
    input_payload: dict[str, Any] = Field(default_factory=dict)
    requested_tool_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    attempts_state_mutation: bool = False


class SubAgentOutputEnvelope(BaseModel):
    schema_version: Literal["cmf.sub_agent_output_envelope.v1"] = "cmf.sub_agent_output_envelope.v1"
    sub_agent_code: str = Field(min_length=1)
    parent_agent_code: str = Field(min_length=1)
    output_payload: dict[str, Any] = Field(default_factory=dict)
    evidence_refs: list[str] = Field(min_length=1)
    downstream_parent_decision: str = Field(min_length=1)


class SubAgentReceipt(BaseModel):
    schema_version: Literal["cmf.sub_agent_receipt.v1"] = "cmf.sub_agent_receipt.v1"
    receipt_id: UUID
    sub_agent_code: str = Field(min_length=1)
    parent_agent_code: str = Field(min_length=1)
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    input_hash: str = Field(min_length=1)
    output_hash: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    downstream_parent_decision: str = Field(min_length=1)
    created_at: datetime


class HookSpec(BaseModel):
    schema_version: Literal["cmf.hook_spec.v1"] = "cmf.hook_spec.v1"
    hook_spec_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-HK$")
    lifecycle_boundary: LifecycleBoundary
    trigger_condition: str = Field(min_length=1)
    allowed_checks: list[str] = Field(min_length=1)
    blocked_mutations: list[str] = Field(min_length=1)
    emitted_receipt_type: str = Field(min_length=1)
    failure_behavior: Literal["block", "warn", "handoff"]
    active: bool = True


class ExtensionSpec(BaseModel):
    schema_version: Literal["cmf.extension_spec.v1"] = "cmf.extension_spec.v1"
    extension_spec_id: UUID
    entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-EX$")
    integration_scope: str = Field(min_length=1)
    exposed_tool_refs: list[str] = Field(min_length=1)
    credential_boundary_ref: str | None = None
    canonical_state_authority: Literal["none"] = "none"
    required_receipt_types: list[str] = Field(min_length=1)
    active: bool = True


class HookExecutionReceipt(BaseModel):
    schema_version: Literal["cmf.hook_execution_receipt.v1"] = "cmf.hook_execution_receipt.v1"
    receipt_id: UUID
    hook_spec_id: UUID
    entity_code: str = Field(min_length=1)
    lifecycle_boundary: LifecycleBoundary
    decision_code: Literal["allowed", "blocked", "warned", "handoff"]
    evidence_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    created_at: datetime


class ExtensionMountReceipt(BaseModel):
    schema_version: Literal["cmf.extension_mount_receipt.v1"] = "cmf.extension_mount_receipt.v1"
    receipt_id: UUID
    extension_spec_id: UUID
    entity_code: str = Field(min_length=1)
    decision_code: Literal["mounted", "blocked", "unmounted"]
    exposed_tool_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    created_at: datetime


class SkillBinding(BaseModel):
    schema_version: Literal["cmf.skill_binding.v1"] = "cmf.skill_binding.v1"
    skill_binding_id: UUID
    skill_entity_code: str = Field(pattern=r"^[A-Z0-9]{3}-[A-Z0-9]{7}-(SK|JS)$")
    binding_type: SkillBindingType
    agent_role_ref: str = Field(min_length=1)
    allowed_stage_refs: list[str] = Field(min_length=1)
    allowed_use_modes: list[SkillUseMode] = Field(min_length=1)
    skill_manifest_ref: str | None = None
    jit_compiler_ref: str | None = None
    required_invocation_record: bool
    output_schema_ref: str = Field(min_length=1)
    evaluation_target_refs: list[str] = Field(min_length=1)
    active: bool = False


class SkillBindingReceipt(BaseModel):
    schema_version: Literal["cmf.skill_binding_receipt.v1"] = "cmf.skill_binding_receipt.v1"
    receipt_id: UUID
    skill_binding_id: UUID
    decision_code: Literal["accepted", "blocked", "updated"]
    evidence_refs: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    created_at: datetime


class PrimitiveObligation(BaseModel):
    schema_version: Literal["cmf.primitive_obligation.v1"] = "cmf.primitive_obligation.v1"
    primitive_family: str = Field(min_length=1)
    obligation: str = Field(min_length=1)
    evidence_ref: str = Field(min_length=1)
    required: bool = True


class AgentReadinessEval(BaseModel):
    schema_version: Literal["cmf.agent_readiness_eval.v1"] = "cmf.agent_readiness_eval.v1"
    agent_readiness_eval_id: UUID
    entity_code: str = Field(min_length=1)
    target_spec_ref: str = Field(min_length=1)
    primitive_obligations: list[PrimitiveObligation] = Field(default_factory=list)
    tool_scope_passed: bool
    memory_policy_passed: bool
    eval_bindings_passed: bool
    receipt_obligations_passed: bool
    blocked_actions_passed: bool
    adapter_boundary_passed: bool
    status: Literal["accepted", "revision_required", "blocked"]
    findings: list[str] = Field(default_factory=list)
    created_at: datetime


class AgentReadinessReceipt(BaseModel):
    schema_version: Literal["cmf.agent_readiness_receipt.v1"] = "cmf.agent_readiness_receipt.v1"
    receipt_id: UUID
    agent_readiness_eval_id: UUID
    entity_code: str = Field(min_length=1)
    target_spec_ref: str = Field(min_length=1)
    decision_code: Literal["accepted", "revision_required", "blocked"]
    findings: list[str] = Field(default_factory=list)
    created_at: datetime


class ToolCapabilitySpec(BaseModel):
    schema_version: Literal["cmf.tool_capability_spec.v1"] = "cmf.tool_capability_spec.v1"
    tool_capability_spec_id: UUID
    tool_key: str = Field(min_length=1)
    kind: ToolCapabilityKind
    department_code: str = Field(min_length=3, max_length=3)
    allowed_agent_refs: list[str] = Field(min_length=1)
    allowed_stage_refs: list[str] = Field(min_length=1)
    input_model_ref: str = Field(min_length=1)
    output_model_ref: str = Field(min_length=1)
    idempotency_required: bool
    required_receipt_type: str = Field(min_length=1)
    mutation_boundary: Literal["none", "command_bus", "workflow_command"]
    failure_behavior: Literal["block", "retry", "handoff", "terminal_failure"]
    active: bool = True


class ToolInvocationRequest(BaseModel):
    schema_version: Literal["cmf.tool_invocation_request.v1"] = "cmf.tool_invocation_request.v1"
    tool_key: str = Field(min_length=1)
    requesting_agent_code: str = Field(min_length=1)
    stage_ref: str = Field(min_length=1)
    input_payload: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str | None = None
    requested_mutation_boundary: Literal["none", "command_bus", "workflow_command"] = "none"


class ToolInvocationReceipt(BaseModel):
    schema_version: Literal["cmf.tool_invocation_receipt.v1"] = "cmf.tool_invocation_receipt.v1"
    receipt_id: UUID
    tool_key: str = Field(min_length=1)
    requesting_agent_code: str = Field(min_length=1)
    stage_ref: str = Field(min_length=1)
    decision_code: Literal["allowed", "blocked", "handoff", "duplicate"]
    input_hash: str = Field(min_length=1)
    output_hash: str | None = None
    failure_reasons: list[str] = Field(default_factory=list)
    created_at: datetime


class DepartmentRuntimeRegistry(BaseModel):
    schema_version: Literal["cmf.department_runtime_registry.v1"] = "cmf.department_runtime_registry.v1"
    department_key: str = Field(min_length=3, max_length=3)
    active_agent_refs: list[str] = Field(default_factory=list)
    active_tool_refs: list[str] = Field(default_factory=list)
    active_hook_refs: list[str] = Field(default_factory=list)
    active_extension_refs: list[str] = Field(default_factory=list)


class GeneratedAdapterFile(BaseModel):
    path: str = Field(min_length=1)
    content_hash: str = Field(min_length=1)
    content: str = Field(min_length=1)
    source_spec_refs: list[str] = Field(min_length=1)


class AgentAdapterExport(BaseModel):
    schema_version: Literal["cmf.agent_adapter_export.v1"] = "cmf.agent_adapter_export.v1"
    adapter_export_id: UUID
    target: AdapterExportTarget
    agent_role_spec_id: UUID
    readiness_eval_id: UUID
    generated_files: list[GeneratedAdapterFile] = Field(min_length=1)
    export_status: Literal["generated", "drift_detected", "superseded"] = "generated"
    created_at: datetime


class AdapterDriftFinding(BaseModel):
    schema_version: Literal["cmf.adapter_drift_finding.v1"] = "cmf.adapter_drift_finding.v1"
    finding_id: UUID
    adapter_export_id: UUID
    path: str = Field(min_length=1)
    expected_hash: str = Field(min_length=1)
    observed_hash: str = Field(min_length=1)
    decision_code: Literal["regenerate_required"] = "regenerate_required"


class AdapterExportReceipt(BaseModel):
    schema_version: Literal["cmf.adapter_export_receipt.v1"] = "cmf.adapter_export_receipt.v1"
    receipt_id: UUID
    adapter_export_id: UUID
    target: AdapterExportTarget
    agent_role_spec_id: UUID
    readiness_eval_id: UUID
    decision_code: Literal["generated", "blocked", "drift_detected", "superseded"]
    drift_finding_ids: list[UUID] = Field(default_factory=list)
    generated_file_hashes: list[str] = Field(default_factory=list)
    failure_reasons: list[str] = Field(default_factory=list)
    created_at: datetime


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def parse_persona_code(entity_code: str) -> PersonaCodeParts:
    match = PERSONA_CODE_PATTERN.match(entity_code)
    if not match:
        raise ValueError("persona code must match DDD-XXXXXXX-TT")
    entity_type = EntityTypeCode(match.group("entity_type"))
    return PersonaCodeParts(
        department_code=match.group("department"),
        service_code=match.group("service"),
        entity_type=entity_type,
        rendered_code=entity_code,
    )


def new_persona_registry_receipt(
    *,
    entity_code: str,
    decision_code: Literal["accepted", "rejected", "updated", "deactivated"],
    evidence_refs: list[str] | None = None,
    failure_reasons: list[str] | None = None,
) -> PersonaRegistryReceipt:
    payload = {
        "entity_code": entity_code,
        "decision_code": decision_code,
        "evidence_refs": evidence_refs or [],
        "failure_reasons": failure_reasons or [],
    }
    return PersonaRegistryReceipt(
        receipt_id=uuid4(),
        entity_code=entity_code,
        decision_code=decision_code,
        evidence_refs=evidence_refs or [],
        failure_reasons=failure_reasons or [],
        receipt_hash=stable_hash(payload),
        created_at=utc_now(),
    )

