"""Pydantic schemas for Visual Asset Editor (VAE) Delegation API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VAEAdmissionRequest(BaseModel):
    workspace_id: str = Field(..., description="Target tenant workspace ID")
    program_id: str = Field(default="vae_delegation_program", description="Target program ID")
    demand_payload: Dict[str, Any] = Field(..., description="Canonical VisualAssetDemand contract payload")
    operator_id: str = Field(..., description="Authoritative operator actor ID")


class VAEAdmissionResponse(BaseModel):
    status: str
    aggregate_id: str
    request_id: str
    demand_hash: str
    scene_index: int
    admitted_at: str


class VAEJobExecutionRequest(BaseModel):
    aggregate_id: str = Field(..., description="Active delegation aggregate ID")
    worker_id: str = Field(..., description="Executing worker/agent actor ID")
    producer_actor_id: Optional[str] = Field(default=None, description="Producer agent actor ID")
    evaluator_actor_id: Optional[str] = Field(default=None, description="Evaluator agent actor ID")
    force_render_fail: bool = Field(default=False, description="Simulate technical render failure for contrastive testing")
    semantic_qa: Optional[Dict[str, Any]] = Field(default=None, description="Independent semantic QA evaluation")


class VAEJobExecutionResponse(BaseModel):
    status: str
    aggregate_id: str
    plan_id: str
    artifact_id: str
    candidate_uri: str
    mask_uri: Optional[str] = None
    cutout_uri: Optional[str] = None
    gnm_uri: Optional[str] = None
    technical_verdict: str
    evaluated_at: str


class VAEResultAcknowledgementRequest(BaseModel):
    aggregate_id: str = Field(..., description="Active delegation aggregate ID")
    operator_id: str = Field(..., description="Authoritative operator actor ID")
    decision: str = Field(default="ACCEPTED", description="Operator gate decision (ACCEPTED / REJECTED)")
    consumption_authorized: bool = Field(default=True, description="Authoritative downstream consumption authorization")


class VAEResultAcknowledgementResponse(BaseModel):
    status: str
    aggregate_id: str
    acknowledgement_id: str
    receipt_id: str
    receipt_sha256: str
    consumption_authorized: bool
    decision: str
    acknowledged_at: str


class VAEStatusResponse(BaseModel):
    status: str
    lifecycle_state: str
    storage_root: str
    delegation_root: str
    contracts_version: str
    repository: Dict[str, Any]
