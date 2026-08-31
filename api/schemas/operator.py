"""
api.schemas.operator
--------------------
FastAPI Pydantic models for M46: Programs + Artifacts + Chat Operator Application.

Enforces:
- Anti-Stale CAS Concurrency headers & payloads
- 4-Lane separation
- Complete cryptographic lineage schemas
- Full execution trace projections
- Chat supervision request/response schemas
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProgramExecutionSummaryResponse(BaseModel):
    aggregate_id: str
    workspace_id: str
    program_id: str
    program_version: str
    lifecycle: str
    current_state: str
    version: int
    state_hash: str
    last_receipt_id: Optional[str] = None
    created_at: str
    updated_at: str


class ProgramExecutionListResponse(BaseModel):
    executions: List[ProgramExecutionSummaryResponse]
    total: int


class ProgramExecutionDetailResponse(BaseModel):
    aggregate: ProgramExecutionSummaryResponse
    state_data: Dict[str, Any]
    allowable_transitions: List[str]
    transition_contracts: Dict[str, Any] = Field(default_factory=dict)
    active_lane: Optional[str] = None


class RunProgramRequest(BaseModel):
    program_id: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    actor_id: str = Field(default="operator")
    initial_data: Optional[Dict[str, Any]] = None
    context_claims: Optional[List[str]] = None


class PauseExecutionRequest(BaseModel):
    actor_id: str = Field(default="operator")
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class ResumeExecutionRequest(BaseModel):
    actor_id: str = Field(default="operator")
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class ApproveGateRequest(BaseModel):
    actor_id: str = Field(default="operator")
    gate_id: str = Field(default="HUMAN_GATE")
    decision: str = Field(default="APPROVE")
    notes: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class RejectGateRequest(BaseModel):
    actor_id: str = Field(default="operator")
    gate_id: str = Field(default="HUMAN_GATE")
    rejection_reason: str = Field(..., min_length=1)
    disposition_route: str = Field(default="RETURN_TO_HUNTER")
    feedback_notes: Optional[str] = None
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class RepairExecutionRequest(BaseModel):
    actor_id: str = Field(default="operator")
    repair_action: str = Field(..., min_length=1)
    repair_payload: Dict[str, Any] = Field(default_factory=dict)
    target_state: Optional[str] = None
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class ChatCommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    workspace_id: str = Field(..., min_length=1)
    actor_id: str = Field(default="operator")
    current_aggregate_id: Optional[str] = None
    expected_version: Optional[int] = None
    expected_state_sha256: Optional[str] = None


class ChatCommandResponse(BaseModel):
    command: str
    action_type: str
    lane: str
    success: bool
    message: str
    aggregate_id: Optional[str] = None
    state_version: Optional[int] = None
    state_hash: Optional[str] = None
    receipt_id: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class LineageNodeResponse(BaseModel):
    node_id: str
    node_type: str
    label: str
    sha256: str
    lane: str
    receipt_ref: Optional[str] = None
    timestamp: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LineageEdgeResponse(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    transformation_op: str
    lane: str
    receipt_ref: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ArtifactLineageGraphResponse(BaseModel):
    aggregate_id: str
    artifact_id: Optional[str] = None
    is_lossless: bool
    verification_status: str
    nodes: List[LineageNodeResponse]
    edges: List[LineageEdgeResponse]
    root_evidence_ids: List[str]
    terminal_artifact_ids: List[str]
    verification_digest: str


class ExecutionTraceNodeResponse(BaseModel):
    step_index: int
    transition_id: str
    transition_name: str
    trigger_operation: str
    lane: str
    actor_id: str
    from_state: str
    to_state: str
    committed_version: int
    receipt_id: str
    timestamp: str
    duration_ms: Optional[float] = None
    status: str
    payload_summary: Dict[str, Any] = Field(default_factory=dict)


class ExecutionTraceProjectionResponse(BaseModel):
    aggregate_id: str
    workspace_id: str
    program_id: str
    program_version: str
    lifecycle: str
    current_state: str
    version: int
    state_hash: str
    last_receipt_id: Optional[str] = None
    created_at: str
    updated_at: str
    allowable_transitions: List[str]
    trace_nodes: List[ExecutionTraceNodeResponse]
    blockers: List[str]
