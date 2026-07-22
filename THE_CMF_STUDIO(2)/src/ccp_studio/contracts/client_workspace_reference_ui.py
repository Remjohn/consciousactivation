from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from ccp_studio.contracts.project_workspace_artifact_store import (
    ArtifactCategory,
    ArtifactRef,
    ArtifactStorageState,
    WorkspaceStatus,
    validate_relative_path,
    validate_safe_token,
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ReferenceRightsStatus(str, Enum):
    UNKNOWN = "unknown"
    OWNED = "owned"
    LICENSED = "licensed"
    CLIENT_PROVIDED = "client_provided"
    PUBLIC_DOMAIN = "public_domain"
    FAIR_USE_REVIEW = "fair_use_review"
    RESTRICTED = "restricted"
    REJECTED = "rejected"


class ReferenceApprovalState(str, Enum):
    PENDING = "pending"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class ClientWorkspaceCreateRequest(BaseModel):
    client_id: str
    client_slug: str
    brand_id: str
    brand_context_version_id: str
    display_name: str | None = None
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        validate_safe_token(self.client_slug, "client_slug")
        if not self.client_id:
            raise ValueError("client_id is required")
        if not self.brand_id:
            raise ValueError("brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")


class ClientWorkspaceReadModel(BaseModel):
    client_workspace_id: str
    client_id: str
    client_slug: str
    brand_id: str
    brand_context_version_id: str
    workspace_relative_path: str
    status: WorkspaceStatus
    folder_map: dict[str, str]
    display_name: str | None = None
    notes: str | None = None
    created_at: str


class BrandContextVersionCreateRequest(BaseModel):
    client_workspace_id: str
    brand_id: str
    brand_context_version_id: str
    context_label: str
    source_note: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.client_workspace_id:
            raise ValueError("client_workspace_id is required")
        if not self.brand_id:
            raise ValueError("brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.context_label:
            raise ValueError("context_label is required")


class BrandContextVersionReadModel(BaseModel):
    brand_context_version_id: str
    brand_id: str
    client_workspace_id: str
    context_label: str
    source_note: str | None = None
    created_at: str = Field(default_factory=_now_iso)


class ReferenceAssetRegisterRequest(BaseModel):
    client_workspace_id: str
    run_id: str | None = None
    filename: str
    content_type: str
    category: ArtifactCategory = ArtifactCategory.REFERENCE
    relative_path: str | None = None
    sha256: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    tags: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    rights_status: ReferenceRightsStatus
    approval_state: ReferenceApprovalState
    notes: str | None = None
    storage_state: ArtifactStorageState = ArtifactStorageState.REGISTERED

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.client_workspace_id:
            raise ValueError("client_workspace_id is required")
        if not self.filename:
            raise ValueError("filename is required")
        normalized_filename = self.filename.replace("\\", "/")
        if "/" in normalized_filename or ".." in normalized_filename.split("/"):
            raise ValueError("filename cannot contain path separators or traversal")
        if self.relative_path is not None:
            self.relative_path = validate_relative_path(self.relative_path, "reference relative_path")
        if self.storage_state == ArtifactStorageState.MATERIALIZED and not self.sha256:
            raise ValueError("Materialized reference requires sha256")
        if self.rights_status is None:
            raise ValueError("rights_status is required")
        if self.approval_state is None:
            raise ValueError("approval_state is required")


class ReferenceAssetReadModel(BaseModel):
    artifact_ref_id: str
    artifact_id: str
    client_workspace_id: str
    client_slug: str
    run_id: str | None = None
    category: ArtifactCategory
    relative_path: str
    uri: str
    content_type: str | None = None
    sha256: str | None = None
    size_bytes: int | None = None
    tags: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    rights_status: ReferenceRightsStatus
    approval_state: ReferenceApprovalState
    notes: str | None = None
    storage_state: ArtifactStorageState = ArtifactStorageState.REGISTERED
    provider_calls_executed: bool = False
    generation_triggered: bool = False
    created_at: str

    @classmethod
    def from_artifact(
        cls,
        artifact: ArtifactRef,
        *,
        rights_status: ReferenceRightsStatus,
        approval_state: ReferenceApprovalState,
        notes: str | None = None,
        size_bytes: int | None = None,
    ) -> "ReferenceAssetReadModel":
        return cls(
            artifact_ref_id=artifact.artifact_ref_id,
            artifact_id=artifact.artifact_id,
            client_workspace_id=artifact.client_workspace_id,
            client_slug=artifact.client_slug,
            run_id=artifact.run_id,
            category=artifact.category,
            relative_path=artifact.relative_path,
            uri=artifact.uri or "",
            content_type=artifact.content_type,
            sha256=artifact.sha256,
            size_bytes=size_bytes if size_bytes is not None else artifact.size_bytes,
            tags=list(artifact.tags),
            source_refs=list(artifact.source_refs),
            rights_status=rights_status,
            approval_state=approval_state,
            notes=notes,
            storage_state=artifact.storage_state,
            created_at=artifact.created_at,
        )


class ReferenceAssetUpdateRequest(BaseModel):
    tags: list[str] | None = None
    rights_status: ReferenceRightsStatus | None = None
    approval_state: ReferenceApprovalState | None = None
    notes: str | None = None


class ReferenceLibraryReadModel(BaseModel):
    client_workspace_id: str
    references: list[ReferenceAssetReadModel]
    counts_by_approval_state: dict[str, int]
    counts_by_rights_status: dict[str, int]

