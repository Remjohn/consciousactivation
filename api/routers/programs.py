"""TS-CAE-PROG-001 -- Governed Program Registry and Discovery API.

Endpoints:
- GET /api/programs: List registered program packages with SHA-256 fingerprints
- GET /api/programs/{program_id}: Detailed inspection of program package, authority lanes, and skills
- POST /api/programs/{program_id}/preflight: Fail-closed preflight validation for tenant session
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ca_runtime.program_registry import (
    ProgramNotFoundError,
    ProgramPackage,
    ProgramPreflightResult,
    ProgramRegistry,
    ProgramStatus,
    get_program_registry,
)

logger = logging.getLogger("conscious_activations.api.programs")

router = APIRouter()


class ProgramSummaryResponse(BaseModel):
    program_id: str
    version: str
    status: str
    purpose: str
    lanes: List[str]
    manifest_sha256: str
    package_sha256: str
    skills_count: int
    operations_count: int


class ProgramListResponse(BaseModel):
    programs: List[ProgramSummaryResponse]
    total: int


class PreflightRequest(BaseModel):
    workspace_id: str = Field(..., min_length=1)
    context_refs: List[str] = Field(default_factory=list)
    version: Optional[str] = Field(default=None)


def get_registry() -> ProgramRegistry:
    return get_program_registry()


@router.get("", response_model=ProgramListResponse)
def list_programs(
    status: Optional[ProgramStatus] = Query(default=None, description="Filter by program status"),
    registry: ProgramRegistry = Depends(get_registry),
) -> ProgramListResponse:
    """Lists all registered program packages."""
    pkgs = registry.list_programs(status=status)
    summaries = [
        ProgramSummaryResponse(
            program_id=pkg.program_id,
            version=pkg.version,
            status=pkg.manifest.status.value,
            purpose=pkg.manifest.purpose,
            lanes=pkg.manifest.lanes,
            manifest_sha256=pkg.manifest_sha256,
            package_sha256=pkg.package_sha256,
            skills_count=len(pkg.manifest.skills),
            operations_count=len(pkg.manifest.operations),
        )
        for pkg in pkgs
    ]
    return ProgramListResponse(programs=summaries, total=len(summaries))


@router.get("/{program_id}", response_model=Dict[str, Any])
def get_program_details(
    program_id: str,
    version: Optional[str] = Query(default=None, description="Specific SemVer version"),
    registry: ProgramRegistry = Depends(get_registry),
) -> Dict[str, Any]:
    """Inspects a registered program package."""
    try:
        return registry.inspect_program(program_id=program_id, version=version)
    except ProgramNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program '{program_id}' not found",
        )


@router.post("/{program_id}/preflight", response_model=ProgramPreflightResult)
def preflight_program(
    program_id: str,
    request: PreflightRequest,
    registry: ProgramRegistry = Depends(get_registry),
) -> ProgramPreflightResult:
    """Performs a fail-closed preflight check on a program package for an operator session."""
    try:
        return registry.preflight(
            program_id=program_id,
            workspace_id=request.workspace_id,
            context_refs=request.context_refs,
            version=request.version,
        )
    except ProgramNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program '{program_id}' not found",
        )
