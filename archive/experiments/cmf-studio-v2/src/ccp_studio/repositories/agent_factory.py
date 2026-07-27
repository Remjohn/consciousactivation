"""Agent Factory repository for TS-CMF-062 through TS-CMF-069."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.agent_factory import (
    AdapterDriftFinding,
    AdapterExportReceipt,
    AgentAdapterExport,
    AgentReadinessEval,
    AgentReadinessReceipt,
    AgentRoleSpec,
    AgentRoleSpecReceipt,
    DepartmentRuntimeRegistry,
    DepartmentSpec,
    ExtensionMountReceipt,
    ExtensionSpec,
    HookExecutionReceipt,
    HookSpec,
    PersonaRegistryEntry,
    PersonaRegistryReceipt,
    SkillBinding,
    SkillBindingReceipt,
    SubAgentReceipt,
    SubAgentRoleSpec,
    ToolCapabilitySpec,
    ToolInvocationReceipt,
)


@dataclass
class InMemoryAgentFactoryRepository:
    personas: dict[str, PersonaRegistryEntry] = field(default_factory=dict)
    persona_receipts: dict[UUID, PersonaRegistryReceipt] = field(default_factory=dict)
    departments: dict[str, DepartmentSpec] = field(default_factory=dict)
    agent_roles: dict[str, AgentRoleSpec] = field(default_factory=dict)
    agent_role_receipts: dict[UUID, AgentRoleSpecReceipt] = field(default_factory=dict)
    sub_agent_roles: dict[str, SubAgentRoleSpec] = field(default_factory=dict)
    sub_agent_receipts: dict[UUID, SubAgentReceipt] = field(default_factory=dict)
    hook_specs: dict[str, HookSpec] = field(default_factory=dict)
    hook_receipts: dict[UUID, HookExecutionReceipt] = field(default_factory=dict)
    extension_specs: dict[str, ExtensionSpec] = field(default_factory=dict)
    extension_receipts: dict[UUID, ExtensionMountReceipt] = field(default_factory=dict)
    skill_bindings: dict[UUID, SkillBinding] = field(default_factory=dict)
    skill_binding_receipts: dict[UUID, SkillBindingReceipt] = field(default_factory=dict)
    readiness_evals: dict[UUID, AgentReadinessEval] = field(default_factory=dict)
    readiness_receipts: dict[UUID, AgentReadinessReceipt] = field(default_factory=dict)
    tool_capabilities: dict[str, ToolCapabilitySpec] = field(default_factory=dict)
    tool_invocation_receipts: dict[UUID, ToolInvocationReceipt] = field(default_factory=dict)
    department_runtime_registries: dict[str, DepartmentRuntimeRegistry] = field(default_factory=dict)
    adapter_exports: dict[UUID, AgentAdapterExport] = field(default_factory=dict)
    adapter_export_receipts: dict[UUID, AdapterExportReceipt] = field(default_factory=dict)
    adapter_drift_findings: dict[UUID, AdapterDriftFinding] = field(default_factory=dict)
    tool_idempotency_index: dict[str, UUID] = field(default_factory=dict)

    def put_persona(self, entry: PersonaRegistryEntry) -> PersonaRegistryEntry:
        self.personas[entry.entity_code] = entry
        return entry

    def put_persona_receipt(self, receipt: PersonaRegistryReceipt) -> PersonaRegistryReceipt:
        self.persona_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_department(self, department: DepartmentSpec) -> DepartmentSpec:
        self.departments[department.department_key] = department
        return department

    def put_agent_role(self, spec: AgentRoleSpec) -> AgentRoleSpec:
        self.agent_roles[spec.entity_code] = spec
        return spec

    def put_agent_role_receipt(self, receipt: AgentRoleSpecReceipt) -> AgentRoleSpecReceipt:
        self.agent_role_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_sub_agent_role(self, spec: SubAgentRoleSpec) -> SubAgentRoleSpec:
        self.sub_agent_roles[spec.entity_code] = spec
        return spec

    def put_sub_agent_receipt(self, receipt: SubAgentReceipt) -> SubAgentReceipt:
        self.sub_agent_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_hook_spec(self, spec: HookSpec) -> HookSpec:
        self.hook_specs[spec.entity_code] = spec
        return spec

    def put_hook_receipt(self, receipt: HookExecutionReceipt) -> HookExecutionReceipt:
        self.hook_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_extension_spec(self, spec: ExtensionSpec) -> ExtensionSpec:
        self.extension_specs[spec.entity_code] = spec
        return spec

    def put_extension_receipt(self, receipt: ExtensionMountReceipt) -> ExtensionMountReceipt:
        self.extension_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_skill_binding(self, binding: SkillBinding) -> SkillBinding:
        self.skill_bindings[binding.skill_binding_id] = binding
        return binding

    def put_skill_binding_receipt(self, receipt: SkillBindingReceipt) -> SkillBindingReceipt:
        self.skill_binding_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_readiness_eval(self, readiness_eval: AgentReadinessEval) -> AgentReadinessEval:
        self.readiness_evals[readiness_eval.agent_readiness_eval_id] = readiness_eval
        return readiness_eval

    def put_readiness_receipt(self, receipt: AgentReadinessReceipt) -> AgentReadinessReceipt:
        self.readiness_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_tool_capability(self, tool: ToolCapabilitySpec) -> ToolCapabilitySpec:
        self.tool_capabilities[tool.tool_key] = tool
        return tool

    def put_tool_invocation_receipt(
        self,
        receipt: ToolInvocationReceipt,
        *,
        idempotency_key: str | None = None,
    ) -> ToolInvocationReceipt:
        self.tool_invocation_receipts[receipt.receipt_id] = receipt
        if idempotency_key:
            self.tool_idempotency_index[idempotency_key] = receipt.receipt_id
        return receipt

    def tool_receipt_for_idempotency(self, idempotency_key: str) -> ToolInvocationReceipt | None:
        receipt_id = self.tool_idempotency_index.get(idempotency_key)
        return self.tool_invocation_receipts.get(receipt_id) if receipt_id else None

    def put_department_runtime_registry(self, registry: DepartmentRuntimeRegistry) -> DepartmentRuntimeRegistry:
        self.department_runtime_registries[registry.department_key] = registry
        return registry

    def put_adapter_export(self, export: AgentAdapterExport) -> AgentAdapterExport:
        self.adapter_exports[export.adapter_export_id] = export
        return export

    def put_adapter_export_receipt(self, receipt: AdapterExportReceipt) -> AdapterExportReceipt:
        self.adapter_export_receipts[receipt.receipt_id] = receipt
        return receipt

    def put_adapter_drift_finding(self, finding: AdapterDriftFinding) -> AdapterDriftFinding:
        self.adapter_drift_findings[finding.finding_id] = finding
        return finding

