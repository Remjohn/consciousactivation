"""Agent Factory service for TS-CMF-062 through TS-CMF-069."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.agent_factory import (
    AdapterDriftFinding,
    AdapterExportReceipt,
    AdapterExportTarget,
    AgentAdapterExport,
    AgentActivationState,
    AgentReadinessEval,
    AgentReadinessReceipt,
    AgentRoleSpec,
    AgentRoleSpecReceipt,
    DepartmentRuntimeRegistry,
    DepartmentSpec,
    ExtensionMountReceipt,
    ExtensionSpec,
    GeneratedAdapterFile,
    HookExecutionReceipt,
    HookSpec,
    PersonaCodeParts,
    PersonaRegistryEntry,
    PersonaRegistryReceipt,
    SkillBinding,
    SkillBindingReceipt,
    SkillBindingType,
    SubAgentInvocationRequest,
    SubAgentOutputEnvelope,
    SubAgentReceipt,
    SubAgentRoleSpec,
    ToolCapabilitySpec,
    ToolInvocationReceipt,
    ToolInvocationRequest,
    content_hash,
    new_persona_registry_receipt,
    parse_persona_code,
    stable_hash,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.skills import SkillUseMode
from ccp_studio.repositories.agent_factory import InMemoryAgentFactoryRepository


class AgentFactoryError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


VAGUE_SERVICE_CODES = {"AUROREX", "GENRICX", "PROMPTX", "AGENTXX", "HELPERX", "MISCXXX"}
GENERIC_SCOPE_TERMS = {"generic", "prompt-only", "miscellaneous", "helper", "assistant without scope"}
MUTATION_BLOCKERS = {"direct_repository_write", "direct_canonical_write", "bypass_command_bus"}
FORBIDDEN_JIT_MODES = {"few_shot", "few_shot_only", "generic_script_prompt"}


@dataclass
class AgentFactoryService:
    repository: InMemoryAgentFactoryRepository = field(default_factory=InMemoryAgentFactoryRepository)

    def validate_persona_code(self, entity_code: str) -> PersonaCodeParts:
        try:
            return parse_persona_code(entity_code)
        except ValueError as exc:
            raise AgentFactoryError("PERSONA_CODE_INVALID", str(exc)) from exc

    def register_persona(self, entry: PersonaRegistryEntry) -> PersonaRegistryEntry:
        failure_reasons = self._persona_failures(entry)
        if failure_reasons:
            self.repository.put_persona_receipt(
                new_persona_registry_receipt(
                    entity_code=entry.entity_code,
                    decision_code="rejected",
                    evidence_refs=entry.source_refs,
                    failure_reasons=failure_reasons,
                )
            )
            raise AgentFactoryError("PERSONA_REGISTRY_REJECTED", "; ".join(failure_reasons))
        if entry.entity_code in self.repository.personas:
            failure_reasons = ["entity_code already registered"]
            self.repository.put_persona_receipt(
                new_persona_registry_receipt(
                    entity_code=entry.entity_code,
                    decision_code="rejected",
                    evidence_refs=entry.source_refs,
                    failure_reasons=failure_reasons,
                )
            )
            raise AgentFactoryError("PERSONA_CODE_DUPLICATE", "Persona code already exists.")
        self.repository.put_persona(entry)
        self.repository.put_persona_receipt(
            new_persona_registry_receipt(
                entity_code=entry.entity_code,
                decision_code="accepted",
                evidence_refs=entry.source_refs,
            )
        )
        return entry

    def deactivate_persona(self, entity_code: str, *, evidence_refs: list[str] | None = None) -> PersonaRegistryReceipt:
        entry = self.repository.personas.get(entity_code)
        if entry is None:
            raise AgentFactoryError("PERSONA_CODE_NOT_FOUND", "Persona code is not registered.")
        self.repository.personas[entity_code] = entry.model_copy(update={"active": False})
        receipt = new_persona_registry_receipt(
            entity_code=entity_code,
            decision_code="deactivated",
            evidence_refs=evidence_refs or [],
        )
        return self.repository.put_persona_receipt(receipt)

    def register_department(self, spec: DepartmentSpec) -> DepartmentSpec:
        return self.repository.put_department(spec)

    def register_agent_role_spec(self, spec: AgentRoleSpec) -> AgentRoleSpec:
        self._require_persona(spec.entity_code, expected_type="AG")
        parts = self.validate_persona_code(spec.entity_code)
        if spec.department_key != parts.department_code or spec.service_code != parts.service_code:
            raise AgentFactoryError("AGENT_ROLE_PERSONA_MISMATCH", "AgentRoleSpec must match persona code parts.")
        if not MUTATION_BLOCKERS.intersection(set(spec.blocked_actions)):
            raise AgentFactoryError("AGENT_ROLE_MUTATION_BLOCKER_REQUIRED", "AgentRoleSpec must block direct canonical writes.")
        registered = self.repository.put_agent_role(spec)
        self.repository.put_agent_role_receipt(self._agent_role_receipt(spec, "registered"))
        return registered

    def run_agent_readiness_eval(self, readiness_eval: AgentReadinessEval) -> AgentReadinessEval:
        if readiness_eval.entity_code not in self.repository.agent_roles:
            raise AgentFactoryError("READINESS_TARGET_NOT_FOUND", "Agent role spec must exist before readiness eval.")
        findings = list(readiness_eval.findings)
        if not readiness_eval.primitive_obligations or not any(item.required for item in readiness_eval.primitive_obligations):
            findings.append("primitive_obligation_required")
        if not readiness_eval.tool_scope_passed:
            findings.append("tool_scope_failed")
        if not readiness_eval.memory_policy_passed:
            findings.append("memory_policy_failed")
        if not readiness_eval.eval_bindings_passed:
            findings.append("eval_bindings_failed")
        if not readiness_eval.receipt_obligations_passed:
            findings.append("receipt_obligations_failed")
        if not readiness_eval.blocked_actions_passed:
            findings.append("blocked_actions_failed")
        if not readiness_eval.adapter_boundary_passed:
            findings.append("adapter_boundary_failed")
        status = "accepted" if not findings else ("blocked" if "memory_policy_failed" in findings else "revision_required")
        accepted_eval = readiness_eval.model_copy(update={"status": status, "findings": findings, "created_at": readiness_eval.created_at or utc_now()})
        self.repository.put_readiness_eval(accepted_eval)
        receipt = AgentReadinessReceipt(
            receipt_id=uuid4(),
            agent_readiness_eval_id=accepted_eval.agent_readiness_eval_id,
            entity_code=accepted_eval.entity_code,
            target_spec_ref=accepted_eval.target_spec_ref,
            decision_code=accepted_eval.status,
            findings=findings,
            created_at=utc_now(),
        )
        self.repository.put_readiness_receipt(receipt)
        return accepted_eval

    def activate_agent_role_spec(self, entity_code: str, *, readiness_eval_id: UUID) -> AgentRoleSpec:
        spec = self.repository.agent_roles.get(entity_code)
        if spec is None:
            raise AgentFactoryError("AGENT_ROLE_NOT_FOUND", "Agent role spec is not registered.")
        readiness_eval = self.repository.readiness_evals.get(readiness_eval_id)
        if readiness_eval is None or readiness_eval.entity_code != entity_code or readiness_eval.status != "accepted":
            self.repository.put_agent_role_receipt(
                self._agent_role_receipt(spec, "blocked", readiness_eval_id=readiness_eval_id, failure_reasons=["accepted readiness eval required"])
            )
            raise AgentFactoryError("AGENT_READINESS_REQUIRED", "Active agents require an accepted readiness eval.")
        activated = spec.model_copy(update={"activation_state": AgentActivationState.active, "readiness_eval_id": readiness_eval_id})
        self.repository.put_agent_role(activated)
        self.repository.put_agent_role_receipt(self._agent_role_receipt(activated, "activated", readiness_eval_id=readiness_eval_id))
        return activated

    def register_sub_agent_role_spec(self, spec: SubAgentRoleSpec) -> SubAgentRoleSpec:
        self._require_persona(spec.entity_code, expected_type="SA")
        for parent_code in spec.parent_agent_refs:
            parent = self.repository.agent_roles.get(parent_code)
            if parent is None:
                raise AgentFactoryError("SUB_AGENT_PARENT_NOT_FOUND", "Sub-agent parent AgentRoleSpec is required.")
            extra_tools = set(spec.allowed_tool_refs).difference(parent.allowed_tool_refs)
            if extra_tools:
                raise AgentFactoryError("SUB_AGENT_TOOL_SCOPE_EXCEEDED", "Sub-agent tools must be a subset of parent tools.")
        if "direct_canonical_write" not in spec.blocked_actions and spec.mutation_policy == "read_only":
            raise AgentFactoryError("SUB_AGENT_MUTATION_BLOCKER_REQUIRED", "Read-only sub-agents must block direct canonical writes.")
        return self.repository.put_sub_agent_role(spec)

    def invoke_sub_agent(self, request: SubAgentInvocationRequest, output: SubAgentOutputEnvelope) -> SubAgentReceipt:
        spec = self.repository.sub_agent_roles.get(request.sub_agent_code)
        if spec is None or not spec.active:
            raise AgentFactoryError("SUB_AGENT_NOT_ACTIVE", "Sub-agent role spec must be active.")
        if request.parent_agent_code not in spec.parent_agent_refs:
            raise AgentFactoryError("SUB_AGENT_PARENT_SCOPE_BLOCKED", "Sub-agent cannot run outside parent scope.")
        extra_tools = set(request.requested_tool_refs).difference(spec.allowed_tool_refs)
        if extra_tools:
            raise AgentFactoryError("SUB_AGENT_TOOL_SCOPE_EXCEEDED", "Sub-agent requested an unallowed tool.")
        if request.attempts_state_mutation and spec.mutation_policy == "read_only":
            raise AgentFactoryError("SUB_AGENT_MUTATION_FORBIDDEN", "Read-only sub-agents cannot mutate canonical state.")
        if not output.evidence_refs:
            raise AgentFactoryError("SUB_AGENT_EVIDENCE_REQUIRED", "Sub-agent output requires evidence refs.")
        receipt = SubAgentReceipt(
            receipt_id=uuid4(),
            sub_agent_code=request.sub_agent_code,
            parent_agent_code=request.parent_agent_code,
            orchestration_run_id=request.orchestration_run_id,
            stage_execution_plan_id=request.stage_execution_plan_id,
            input_hash=stable_hash(request.input_payload),
            output_hash=stable_hash(output.output_payload),
            evidence_refs=output.evidence_refs,
            downstream_parent_decision=output.downstream_parent_decision,
            created_at=utc_now(),
        )
        return self.repository.put_sub_agent_receipt(receipt)

    def register_hook_spec(self, spec: HookSpec) -> HookSpec:
        self._require_persona(spec.entity_code, expected_type="HK")
        checks = " ".join(spec.allowed_checks).lower()
        if any(term in checks for term in ["creative rewrite", "creative synthesis", "prompt generation"]):
            raise AgentFactoryError("HOOK_CREATIVE_REASONING_BLOCKED", "Hooks must remain deterministic lifecycle checks.")
        return self.repository.put_hook_spec(spec)

    def run_hook(
        self,
        *,
        entity_code: str,
        evidence_refs: list[str] | None = None,
        requested_mutation: str | None = None,
        blocker_present: bool = False,
    ) -> HookExecutionReceipt:
        spec = self.repository.hook_specs.get(entity_code)
        if spec is None or not spec.active:
            raise AgentFactoryError("HOOK_NOT_ACTIVE", "HookSpec must be active.")
        failure_reasons: list[str] = []
        if requested_mutation and requested_mutation in spec.blocked_mutations:
            failure_reasons.append("blocked_mutation_requested")
        if blocker_present and spec.failure_behavior == "block":
            failure_reasons.append("lifecycle_blocker_present")
        decision = "blocked" if failure_reasons else "allowed"
        receipt = HookExecutionReceipt(
            receipt_id=uuid4(),
            hook_spec_id=spec.hook_spec_id,
            entity_code=spec.entity_code,
            lifecycle_boundary=spec.lifecycle_boundary,
            decision_code=decision,
            evidence_refs=evidence_refs or [],
            failure_reasons=failure_reasons,
            created_at=utc_now(),
        )
        return self.repository.put_hook_receipt(receipt)

    def register_extension_spec(self, spec: ExtensionSpec) -> ExtensionSpec:
        self._require_persona(spec.entity_code, expected_type="EX")
        if spec.canonical_state_authority != "none":
            raise AgentFactoryError("EXTENSION_CANONICAL_AUTHORITY_FORBIDDEN", "Extensions cannot own canonical truth.")
        return self.repository.put_extension_spec(spec)

    def mount_extension(self, entity_code: str) -> ExtensionMountReceipt:
        spec = self.repository.extension_specs.get(entity_code)
        if spec is None or not spec.active:
            raise AgentFactoryError("EXTENSION_NOT_ACTIVE", "ExtensionSpec must be active.")
        receipt = ExtensionMountReceipt(
            receipt_id=uuid4(),
            extension_spec_id=spec.extension_spec_id,
            entity_code=spec.entity_code,
            decision_code="mounted",
            exposed_tool_refs=spec.exposed_tool_refs,
            created_at=utc_now(),
        )
        return self.repository.put_extension_receipt(receipt)

    def bind_skill(self, binding: SkillBinding) -> SkillBinding:
        expected_type = "JS" if binding.binding_type == SkillBindingType.jit else "SK"
        self._require_persona(binding.skill_entity_code, expected_type=expected_type)
        if binding.agent_role_ref not in self.repository.agent_roles:
            raise AgentFactoryError("SKILL_AGENT_ROLE_NOT_FOUND", "Skill binding requires a registered AgentRoleSpec.")
        self._validate_skill_binding(binding)
        return self.repository.put_skill_binding(binding)

    def activate_skill_binding(self, skill_binding_id: UUID) -> SkillBinding:
        binding = self.repository.skill_bindings.get(skill_binding_id)
        if binding is None:
            raise AgentFactoryError("SKILL_BINDING_NOT_FOUND", "Skill binding not found.")
        self._validate_skill_binding(binding)
        active_binding = binding.model_copy(update={"active": True})
        self.repository.put_skill_binding(active_binding)
        self.repository.put_skill_binding_receipt(
            SkillBindingReceipt(
                receipt_id=uuid4(),
                skill_binding_id=active_binding.skill_binding_id,
                decision_code="accepted",
                evidence_refs=[active_binding.agent_role_ref, active_binding.output_schema_ref],
                created_at=utc_now(),
            )
        )
        return active_binding

    def register_tool_capability(self, tool: ToolCapabilitySpec) -> ToolCapabilitySpec:
        for agent_ref in tool.allowed_agent_refs:
            if agent_ref not in self.repository.agent_roles:
                raise AgentFactoryError("TOOL_AGENT_SCOPE_NOT_FOUND", "ToolCapabilitySpec references unknown agent.")
        if tool.mutation_boundary == "none" and tool.kind.value in {"command", "workflow_signal", "provider_adapter", "renderer", "review_action"}:
            raise AgentFactoryError("TOOL_MUTATION_BOUNDARY_REQUIRED", "Mutating tools require Command Bus or workflow command boundary.")
        return self.repository.put_tool_capability(tool)

    def invoke_tool_capability(self, request: ToolInvocationRequest, *, output_payload: dict[str, Any] | None = None) -> ToolInvocationReceipt:
        if request.idempotency_key:
            prior = self.repository.tool_receipt_for_idempotency(request.idempotency_key)
            if prior:
                return prior.model_copy(update={"decision_code": "duplicate"})
        tool = self.repository.tool_capabilities.get(request.tool_key)
        if tool is None or not tool.active:
            receipt = self._tool_receipt(request, "handoff", failure_reasons=["tool_capability_missing"], output_payload=output_payload)
            return self.repository.put_tool_invocation_receipt(receipt, idempotency_key=request.idempotency_key)
        failure_reasons: list[str] = []
        if request.requesting_agent_code not in tool.allowed_agent_refs:
            failure_reasons.append("agent_scope_blocked")
        if request.stage_ref not in tool.allowed_stage_refs:
            failure_reasons.append("stage_scope_blocked")
        if tool.idempotency_required and not request.idempotency_key:
            failure_reasons.append("idempotency_key_required")
        if request.requested_mutation_boundary != tool.mutation_boundary:
            failure_reasons.append("mutation_boundary_mismatch")
        decision = "blocked" if failure_reasons else "allowed"
        receipt = self._tool_receipt(request, decision, failure_reasons=failure_reasons, output_payload=output_payload)
        return self.repository.put_tool_invocation_receipt(receipt, idempotency_key=request.idempotency_key)

    def build_department_runtime_registry(self, department_key: str) -> DepartmentRuntimeRegistry:
        registry = DepartmentRuntimeRegistry(
            department_key=department_key,
            active_agent_refs=[
                code
                for code, spec in self.repository.agent_roles.items()
                if spec.department_key == department_key and spec.activation_state == AgentActivationState.active
            ],
            active_tool_refs=[
                key for key, tool in self.repository.tool_capabilities.items() if tool.department_code == department_key and tool.active
            ],
            active_hook_refs=[
                code for code, hook in self.repository.hook_specs.items() if code.startswith(f"{department_key}-") and hook.active
            ],
            active_extension_refs=[
                code for code, extension in self.repository.extension_specs.items() if code.startswith(f"{department_key}-") and extension.active
            ],
        )
        return self.repository.put_department_runtime_registry(registry)

    def export_agent_adapter(self, *, entity_code: str, target: AdapterExportTarget) -> AdapterExportReceipt:
        spec = self.repository.agent_roles.get(entity_code)
        if spec is None or spec.activation_state != AgentActivationState.active:
            raise AgentFactoryError("ADAPTER_EXPORT_AGENT_NOT_ACTIVE", "Adapter export requires active AgentRoleSpec.")
        if spec.readiness_eval_id is None:
            raise AgentFactoryError("ADAPTER_EXPORT_READINESS_REQUIRED", "Adapter export requires readiness eval.")
        readiness_eval = self.repository.readiness_evals.get(spec.readiness_eval_id)
        if readiness_eval is None or readiness_eval.status != "accepted":
            raise AgentFactoryError("ADAPTER_EXPORT_READINESS_REQUIRED", "Adapter export requires accepted readiness eval.")
        file_content = self._adapter_content(spec, target)
        generated_file = GeneratedAdapterFile(
            path=f"generated/{target.value}/{spec.entity_code}.json",
            content_hash=content_hash(file_content),
            content=file_content,
            source_spec_refs=[
                f"AgentRoleSpec:{spec.agent_role_spec_id}",
                f"AgentReadinessEval:{readiness_eval.agent_readiness_eval_id}",
                *[f"ToolCapabilitySpec:{tool_ref}" for tool_ref in spec.allowed_tool_refs],
                *[f"HookSpec:{hook_ref}" for hook_ref in spec.hook_refs],
            ],
        )
        export = AgentAdapterExport(
            adapter_export_id=uuid4(),
            target=target,
            agent_role_spec_id=spec.agent_role_spec_id,
            readiness_eval_id=readiness_eval.agent_readiness_eval_id,
            generated_files=[generated_file],
            created_at=utc_now(),
        )
        self.repository.put_adapter_export(export)
        receipt = AdapterExportReceipt(
            receipt_id=uuid4(),
            adapter_export_id=export.adapter_export_id,
            target=target,
            agent_role_spec_id=spec.agent_role_spec_id,
            readiness_eval_id=readiness_eval.agent_readiness_eval_id,
            decision_code="generated",
            generated_file_hashes=[generated_file.content_hash],
            created_at=utc_now(),
        )
        self.repository.put_adapter_export_receipt(receipt)
        updated_spec = spec.model_copy(update={"generated_adapter_hash": generated_file.content_hash})
        self.repository.put_agent_role(updated_spec)
        return receipt

    def run_adapter_drift_check(self, *, adapter_export_id: UUID, current_files: dict[str, str]) -> AdapterExportReceipt:
        export = self.repository.adapter_exports.get(adapter_export_id)
        if export is None:
            raise AgentFactoryError("ADAPTER_EXPORT_NOT_FOUND", "Adapter export not found.")
        findings: list[AdapterDriftFinding] = []
        for generated_file in export.generated_files:
            observed = content_hash(current_files.get(generated_file.path, ""))
            if observed != generated_file.content_hash:
                finding = AdapterDriftFinding(
                    finding_id=uuid4(),
                    adapter_export_id=export.adapter_export_id,
                    path=generated_file.path,
                    expected_hash=generated_file.content_hash,
                    observed_hash=observed,
                )
                self.repository.put_adapter_drift_finding(finding)
                findings.append(finding)
        if findings:
            self.repository.put_adapter_export(export.model_copy(update={"export_status": "drift_detected"}))
        receipt = AdapterExportReceipt(
            receipt_id=uuid4(),
            adapter_export_id=export.adapter_export_id,
            target=export.target,
            agent_role_spec_id=export.agent_role_spec_id,
            readiness_eval_id=export.readiness_eval_id,
            decision_code="drift_detected" if findings else "generated",
            drift_finding_ids=[finding.finding_id for finding in findings],
            generated_file_hashes=[file.content_hash for file in export.generated_files],
            created_at=utc_now(),
        )
        return self.repository.put_adapter_export_receipt(receipt)

    def _persona_failures(self, entry: PersonaRegistryEntry) -> list[str]:
        failures: list[str] = []
        parts = self.validate_persona_code(entry.entity_code)
        if entry.department_code != parts.department_code:
            failures.append("department_code does not match entity_code")
        if entry.service_code != parts.service_code:
            failures.append("service_code does not match entity_code")
        if entry.entity_type != parts.entity_type:
            failures.append("entity_type does not match entity_code")
        if entry.service_code in VAGUE_SERVICE_CODES:
            failures.append("service_code is not service-revealing")
        scope = entry.service_scope.lower()
        if any(term in scope for term in GENERIC_SCOPE_TERMS):
            failures.append("service_scope is too generic for runtime authority")
        if len(entry.service_scope.split()) < 3:
            failures.append("service_scope must describe the served operation")
        return failures

    def _require_persona(self, entity_code: str, *, expected_type: str) -> PersonaRegistryEntry:
        entry = self.repository.personas.get(entity_code)
        if entry is None or not entry.active:
            raise AgentFactoryError("PERSONA_CODE_NOT_REGISTERED", "Registered active persona code is required.")
        if entry.entity_type.value != expected_type:
            raise AgentFactoryError("PERSONA_ENTITY_TYPE_MISMATCH", f"Persona code must be type {expected_type}.")
        return entry

    def _validate_skill_binding(self, binding: SkillBinding) -> None:
        if any(mode.value in FORBIDDEN_JIT_MODES for mode in binding.allowed_use_modes):
            raise AgentFactoryError("GENERIC_FEW_SHOT_SKILL_BLOCKED", "Few-shot-only skills cannot become production bindings.")
        if binding.binding_type == SkillBindingType.stable:
            if not binding.skill_manifest_ref:
                raise AgentFactoryError("STABLE_SKILL_MANIFEST_REQUIRED", "Stable skills require a versioned manifest.")
            if binding.required_invocation_record:
                raise AgentFactoryError("STABLE_SKILL_INVOCATION_RECORD_NOT_REQUIRED", "Stable skills do not require JIT invocation records.")
        if binding.binding_type == SkillBindingType.jit:
            required_modes = {
                SkillUseMode.interview_engineering,
                SkillUseMode.narrative_induction,
                SkillUseMode.source_expression_contrast,
                SkillUseMode.transcript_extraction,
                SkillUseMode.routing_support,
                SkillUseMode.evaluation_support,
            }
            if binding.jit_compiler_ref is None or not binding.required_invocation_record:
                raise AgentFactoryError("JIT_INVOCATION_RECORD_REQUIRED", "JIT skills require compiler ref and invocation record.")
            if not set(binding.allowed_use_modes).intersection(required_modes):
                raise AgentFactoryError("JIT_NORTH_STAR_MODE_REQUIRED", "JIT binding must support interview, induction, extraction, routing, or eval modes.")
            if not binding.evaluation_target_refs:
                raise AgentFactoryError("JIT_EVAL_TARGET_REQUIRED", "JIT bindings require eval targets.")

    def _agent_role_receipt(
        self,
        spec: AgentRoleSpec,
        decision_code: str,
        *,
        readiness_eval_id: UUID | None = None,
        failure_reasons: list[str] | None = None,
    ) -> AgentRoleSpecReceipt:
        payload = {
            "agent_role_spec_id": spec.agent_role_spec_id,
            "entity_code": spec.entity_code,
            "decision_code": decision_code,
            "readiness_eval_id": readiness_eval_id,
            "failure_reasons": failure_reasons or [],
        }
        return AgentRoleSpecReceipt(
            receipt_id=uuid4(),
            agent_role_spec_id=spec.agent_role_spec_id,
            entity_code=spec.entity_code,
            decision_code=decision_code,  # type: ignore[arg-type]
            readiness_eval_id=readiness_eval_id,
            validation_results=["agent_role_spec_contract_valid"] if not failure_reasons else [],
            failure_reasons=failure_reasons or [],
            receipt_hash=stable_hash(payload),
            created_at=utc_now(),
        )

    def _tool_receipt(
        self,
        request: ToolInvocationRequest,
        decision_code: str,
        *,
        failure_reasons: list[str],
        output_payload: dict[str, Any] | None,
    ) -> ToolInvocationReceipt:
        return ToolInvocationReceipt(
            receipt_id=uuid4(),
            tool_key=request.tool_key,
            requesting_agent_code=request.requesting_agent_code,
            stage_ref=request.stage_ref,
            decision_code=decision_code,  # type: ignore[arg-type]
            input_hash=stable_hash(request.input_payload),
            output_hash=stable_hash(output_payload or {}) if output_payload is not None else None,
            failure_reasons=failure_reasons,
            created_at=utc_now(),
        )

    @staticmethod
    def _adapter_content(spec: AgentRoleSpec, target: AdapterExportTarget) -> str:
        payload = {
            "target": target.value,
            "entity_code": spec.entity_code,
            "display_name": spec.display_name,
            "goal": spec.goal,
            "active_object_types": spec.active_object_types,
            "allowed_tools": spec.allowed_tool_refs,
            "sub_agents": spec.sub_agent_refs,
            "hooks": spec.hook_refs,
            "memory_policy": spec.memory_access_policy_ref,
            "required_receipts": spec.required_receipt_types,
            "blocked_actions": spec.blocked_actions,
            "source_of_truth": "CMF AgentRoleSpec",
        }
        return stable_hash(payload)

