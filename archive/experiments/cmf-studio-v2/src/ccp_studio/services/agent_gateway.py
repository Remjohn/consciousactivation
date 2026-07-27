"""Constrained Pi Agent Gateway for TS-CMF-002."""

from __future__ import annotations

from dataclasses import dataclass

from ccp_studio.contracts.agent_gateway import (
    AgentActionRequest,
    AgentGatewayDecision,
    AgentGatewayDecisionStatus,
)
from ccp_studio.services.orchestration import OrchestrationService, OrchestrationValidationError


@dataclass
class PiAgentGateway:
    orchestration_service: OrchestrationService

    def request_action(self, request: AgentActionRequest) -> AgentGatewayDecision:
        try:
            plan = self.orchestration_service.repository.get_plan(
                request.stage_execution_plan_id
            )
            if plan is None:
                raise OrchestrationValidationError(
                    "STAGE_EXECUTION_PLAN_NOT_FOUND",
                    "StageExecutionPlan does not exist.",
                )

            packet = self.orchestration_service.create_agent_handoff_packet(
                orchestration_run_id=request.orchestration_run_id,
                stage_execution_plan_id=request.stage_execution_plan_id,
                recipient_type="agent",
                recipient_name=request.actor_or_service,
                source_evidence_refs=request.source_evidence_refs,
                upstream_receipt_ids=request.upstream_receipt_ids,
                allowed_actions=[request.requested_action],
            )
            return AgentGatewayDecision(
                schema_version="cmf.agent_gateway_decision.v1",
                status=AgentGatewayDecisionStatus.allowed,
                code="ACTION_ALLOWED",
                message="Action allowed through stage-bound handoff packet.",
                handoff_packet_id=packet.handoff_packet_id,
            )
        except OrchestrationValidationError as exc:
            return AgentGatewayDecision(
                schema_version="cmf.agent_gateway_decision.v1",
                status=AgentGatewayDecisionStatus.blocked,
                code=exc.code,
                message=exc.message,
                blocked_action=request.requested_action,
            )
