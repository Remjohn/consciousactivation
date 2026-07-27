"""FastAPI adapter for TS-CMF-062 through TS-CMF-069 Agent Factory."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.agent_factory import (
    AdapterExportReceipt,
    AdapterExportTarget,
    AgentReadinessEval,
    AgentRoleSpec,
    PersonaCodeParts,
    PersonaRegistryEntry,
    SkillBinding,
    SkillBindingReceipt,
    SubAgentRoleSpec,
    ToolCapabilitySpec,
    ToolInvocationReceipt,
    ToolInvocationRequest,
)
from ccp_studio.services.agent_factory_service import AgentFactoryService


router = APIRouter(prefix="/api/v1/agent-factory", tags=["agent-factory"])
_agent_factory_service = AgentFactoryService()


class ActivateAgentRoleRequest(BaseModel):
    entity_code: str
    readiness_eval_id: UUID


class ExportAdapterRequest(BaseModel):
    entity_code: str
    target: AdapterExportTarget


def set_agent_factory_service(service: AgentFactoryService) -> None:
    global _agent_factory_service
    _agent_factory_service = service


def get_agent_factory_service() -> AgentFactoryService:
    return _agent_factory_service


@router.get("/persona-codes/{entity_code}", response_model=PersonaCodeParts)
def validate_persona_code(
    entity_code: str,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> PersonaCodeParts:
    return service.validate_persona_code(entity_code)


@router.post("/personas", response_model=PersonaRegistryEntry)
def register_persona(
    entry: PersonaRegistryEntry,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> PersonaRegistryEntry:
    return service.register_persona(entry)


@router.post("/agent-roles", response_model=AgentRoleSpec)
def register_agent_role(
    spec: AgentRoleSpec,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> AgentRoleSpec:
    return service.register_agent_role_spec(spec)


@router.post("/agent-roles/activate", response_model=AgentRoleSpec)
def activate_agent_role(
    request: ActivateAgentRoleRequest,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> AgentRoleSpec:
    return service.activate_agent_role_spec(request.entity_code, readiness_eval_id=request.readiness_eval_id)


@router.post("/sub-agents", response_model=SubAgentRoleSpec)
def register_sub_agent(
    spec: SubAgentRoleSpec,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> SubAgentRoleSpec:
    return service.register_sub_agent_role_spec(spec)


@router.post("/skills", response_model=SkillBinding)
def bind_skill(
    binding: SkillBinding,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> SkillBinding:
    return service.bind_skill(binding)


@router.post("/skills/{skill_binding_id}/activate", response_model=SkillBinding)
def activate_skill(
    skill_binding_id: UUID,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> SkillBinding:
    return service.activate_skill_binding(skill_binding_id)


@router.post("/readiness-evals", response_model=AgentReadinessEval)
def run_readiness_eval(
    readiness_eval: AgentReadinessEval,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> AgentReadinessEval:
    return service.run_agent_readiness_eval(readiness_eval)


@router.post("/tools", response_model=ToolCapabilitySpec)
def register_tool(
    tool: ToolCapabilitySpec,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> ToolCapabilitySpec:
    return service.register_tool_capability(tool)


@router.post("/tools/invoke", response_model=ToolInvocationReceipt)
def invoke_tool(
    request: ToolInvocationRequest,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> ToolInvocationReceipt:
    return service.invoke_tool_capability(request)


@router.post("/adapter-exports", response_model=AdapterExportReceipt)
def export_adapter(
    request: ExportAdapterRequest,
    service: AgentFactoryService = Depends(get_agent_factory_service),
) -> AdapterExportReceipt:
    return service.export_agent_adapter(entity_code=request.entity_code, target=request.target)

