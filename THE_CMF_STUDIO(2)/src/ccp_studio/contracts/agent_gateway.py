"""Pi Agent Gateway contracts for TS-CMF-002."""

from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AgentGatewayDecisionStatus(str, Enum):
    allowed = "allowed"
    blocked = "blocked"


class AgentActionRequest(BaseModel):
    schema_version: Literal["cmf.agent_action_request.v1"]
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    actor_or_service: str = Field(min_length=1)
    requested_action: str = Field(min_length=1)
    requested_target: str = Field(min_length=1)
    source_evidence_refs: list[str] = Field(default_factory=list)
    upstream_receipt_ids: list[UUID] = Field(default_factory=list)


class AgentGatewayDecision(BaseModel):
    schema_version: Literal["cmf.agent_gateway_decision.v1"]
    status: AgentGatewayDecisionStatus
    code: str
    message: str
    handoff_packet_id: UUID | None = None
    blocked_action: str | None = None
