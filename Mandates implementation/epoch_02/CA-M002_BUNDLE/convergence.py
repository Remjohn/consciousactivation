"""
api/schemas/convergence.py
--------------------------
CA-M002 / FR-CONV-001 — Convergence Gate API Schemas.

These schemas expose the canonical convergence gate state to the operator
surface. The UI MUST NOT use these to make admission decisions; it is a
read-only projection of the authoritative runtime state.

All fields mirror the ConvergenceReceipt data class from
ca_runtime.convergence_gate without adding local semantics.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GuestGenesisRefInput(BaseModel):
    """
    Operator-supplied reference to a ratified Guest Genesis Semantic Territory.
    Used when requesting convergence evaluation for a workspace.
    """
    workspace_id: str = Field(..., description="Tenant workspace identifier")
    territory_id: str = Field(..., description="Ratified semantic territory identifier")
    revision_id: str = Field(..., description="Exact revision identifier of the territory artifact")
    sha256_digest: str = Field(..., min_length=64, max_length=64, description="SHA-256 hex digest of the artifact")
    ratified_state: str = Field(default="TERRITORY_RATIFIED", description="Must be TERRITORY_RATIFIED")
    wrong_reading_locks: List[str] = Field(default_factory=list)
    vocabulary_boundaries: List[str] = Field(default_factory=list)


class AudienceTensionsRefInput(BaseModel):
    """
    Operator-supplied reference to active Audience Tensions from audience_context_program.
    """
    workspace_id: str = Field(..., description="Tenant workspace identifier")
    audience_id: str = Field(..., description="Audience context identifier")
    revision_id: str = Field(..., description="Exact revision identifier of the tensions artifact")
    sha256_digest: str = Field(..., min_length=64, max_length=64, description="SHA-256 hex digest of the artifact")
    tension_state: str = Field(default="TENSIONS_ACTIVE", description="Active state of the tensions artifact")
    tension_count: int = Field(..., ge=1, description="Number of active tensions (must be >= 1)")
    active_tension_labels: List[str] = Field(default_factory=list, description="Named active tension labels")


class EvaluateConvergenceRequest(BaseModel):
    """
    Request body for POST /convergence/{workspace_id}/evaluate.
    Operator submits both upstream artifact references for gate evaluation.
    """
    guest_genesis: GuestGenesisRefInput = Field(..., description="Guest Genesis Semantic Territory reference")
    audience_tensions: AudienceTensionsRefInput = Field(..., description="Audience Tensions reference")


class ConvergenceReceiptResponse(BaseModel):
    """
    Response representing a convergence receipt.
    This is a projection of ca_runtime.convergence_gate.ConvergenceReceipt.
    """
    receipt_id: str
    workspace_id: str
    status: str
    guest_genesis_territory_id: str
    guest_genesis_revision_id: str
    guest_genesis_sha256: str
    audience_tensions_audience_id: str
    audience_tensions_revision_id: str
    audience_tensions_sha256: str
    convergence_digest: str
    convergence_signature: str
    converged_at: str
    gate_version: str
    gate_invariant: str = "FR-CONV-001"
    admitted: bool = Field(..., description="True iff this receipt grants downstream compilation admission")


class ConvergenceGateStateResponse(BaseModel):
    """
    Response for GET /convergence/{workspace_id}/state.
    Projects the current convergence gate state for a workspace.
    This is an operator-inspectable view — it does NOT make authority decisions.
    """
    workspace_id: str
    status: str
    admitted: bool
    gate_invariant: str = "FR-CONV-001"
    receipt: Optional[ConvergenceReceiptResponse] = None
    blocker: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Structured reason if gate is not admitted. Populated only when admitted=False."
    )


class ConvergenceReceiptListResponse(BaseModel):
    """
    Response for GET /convergence/{workspace_id}/receipts.
    Lists all convergence receipts for a workspace, most-recent first.
    """
    workspace_id: str
    receipts: List[ConvergenceReceiptResponse]
    total: int
