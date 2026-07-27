from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4
import re
import hashlib

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


_SAFE_TOKEN_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,96}$")


def validate_safe_token(value: str, field_name: str) -> str:
    if not value or not _SAFE_TOKEN_RE.match(value):
        raise ValueError(f"{field_name} must be a safe token: letters, numbers, underscore, hyphen; no path separators")
    return value


def validate_relative_path(value: str, field_name: str = "relative_path") -> str:
    if not value:
        raise ValueError(f"{field_name} is required")
    pure = PurePosixPath(value.replace("\\", "/"))
    if pure.is_absolute():
        raise ValueError(f"{field_name} cannot be absolute")
    if ".." in pure.parts:
        raise ValueError(f"{field_name} cannot contain path traversal")
    if any(part in {"", "."} for part in pure.parts):
        raise ValueError(f"{field_name} cannot contain empty/current path parts")
    return str(pure)


def path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class WorkspaceStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    QUARANTINED = "quarantined"


class ArtifactCategory(str, Enum):
    BRAND = "brand"
    REFERENCE = "reference"
    AVATAR = "avatar"
    REAL_LIFE_CUTOUT = "real_life_cutout"
    TEMPLATE = "template"
    IDEOGRAM_PLATE = "ideogram_plate"
    FLUX_EDIT = "flux_edit"
    CUTOUT = "cutout"
    AUDIO = "audio"
    TIMELINE = "timeline"
    RENDER = "render"
    EXPORT = "export"
    RECEIPT = "receipt"
    MANIFEST = "manifest"
    OTHER = "other"


class ArtifactStorageState(str, Enum):
    REGISTERED = "registered"
    MATERIALIZED = "materialized"
    MISSING = "missing"
    QUARANTINED = "quarantined"


class ArtifactSensitivity(str, Enum):
    PUBLIC = "public"
    CLIENT_PRIVATE = "client_private"
    INTERNAL = "internal"
    RESTRICTED = "restricted"


class LineageRelation(str, Enum):
    GENERATED_FROM = "generated_from"
    EDITED_FROM = "edited_from"
    DERIVED_FROM = "derived_from"
    RENDERED_FROM = "rendered_from"
    EXPORTED_FROM = "exported_from"
    EVALUATED_BY = "evaluated_by"


class WorkspacePathPolicy(BaseModel):
    workspace_root: str = "client_workspaces"
    allow_absolute_root: bool = False
    create_missing_directories: bool = True
    enforce_slug_paths: bool = True
    forbid_path_traversal: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        root = Path(self.workspace_root)
        if root.is_absolute() and not self.allow_absolute_root:
            raise ValueError("Absolute workspace_root requires allow_absolute_root=True")
        if self.forbid_path_traversal:
            validate_relative_path(self.workspace_root, "workspace_root")


class ClientWorkspace(BaseModel):
    client_workspace_id: str = Field(default_factory=lambda: new_id("client_workspace"))
    client_id: str
    client_slug: str
    brand_id: str
    brand_context_version_id: str
    workspace_root: str = "client_workspaces"
    workspace_relative_path: str | None = None
    status: WorkspaceStatus = WorkspaceStatus.ACTIVE
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        validate_safe_token(self.client_slug, "client_slug")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if self.workspace_relative_path is None:
            self.workspace_relative_path = f"{self.workspace_root}/{self.client_slug}"
        validate_relative_path(self.workspace_relative_path, "workspace_relative_path")


class WorkspaceFolderMap(BaseModel):
    workspace_folder_map_id: str = Field(default_factory=lambda: new_id("folder_map"))
    client_workspace_id: str
    root: str
    brand: str
    references: str
    libraries: str
    avatar_library: str
    real_life_cutouts_library: str
    templates_library: str
    runs: str

    def all_paths(self) -> list[str]:
        return [
            self.root,
            self.brand,
            self.references,
            self.libraries,
            self.avatar_library,
            self.real_life_cutouts_library,
            self.templates_library,
            self.runs,
        ]


class RunArtifactDirectory(BaseModel):
    run_artifact_directory_id: str = Field(default_factory=lambda: new_id("run_dir"))
    client_workspace_id: str
    client_slug: str
    run_id: str
    workspace_root: str = "client_workspaces"
    run_root: str | None = None
    artifacts: str | None = None
    receipts: str | None = None
    assets: str | None = None
    asset_references: str | None = None
    asset_ideogram_plates: str | None = None
    asset_flux_edits: str | None = None
    asset_avatar: str | None = None
    asset_cutouts: str | None = None
    asset_audio: str | None = None
    timeline: str | None = None
    renders: str | None = None
    exports: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        validate_safe_token(self.client_slug, "client_slug")
        validate_safe_token(self.run_id, "run_id")
        base = f"{self.workspace_root}/{self.client_slug}/runs/{self.run_id}"
        self.run_root = self.run_root or base
        self.artifacts = self.artifacts or f"{base}/artifacts"
        self.receipts = self.receipts or f"{base}/receipts"
        self.assets = self.assets or f"{base}/assets"
        self.asset_references = self.asset_references or f"{base}/assets/references"
        self.asset_ideogram_plates = self.asset_ideogram_plates or f"{base}/assets/ideogram_plates"
        self.asset_flux_edits = self.asset_flux_edits or f"{base}/assets/flux_edits"
        self.asset_avatar = self.asset_avatar or f"{base}/assets/avatar"
        self.asset_cutouts = self.asset_cutouts or f"{base}/assets/cutouts"
        self.asset_audio = self.asset_audio or f"{base}/assets/audio"
        self.timeline = self.timeline or f"{base}/timeline"
        self.renders = self.renders or f"{base}/renders"
        self.exports = self.exports or f"{base}/exports"
        for field in self.all_paths():
            validate_relative_path(field, "run_artifact_directory_path")

    def all_paths(self) -> list[str]:
        return [
            self.run_root,
            self.artifacts,
            self.receipts,
            self.assets,
            self.asset_references,
            self.asset_ideogram_plates,
            self.asset_flux_edits,
            self.asset_avatar,
            self.asset_cutouts,
            self.asset_audio,
            self.timeline,
            self.renders,
            self.exports,
        ]


class ArtifactRef(BaseModel):
    artifact_ref_id: str = Field(default_factory=lambda: new_id("artifact_ref"))
    artifact_id: str
    client_workspace_id: str
    client_slug: str
    run_id: str | None = None
    category: ArtifactCategory
    relative_path: str
    uri: str | None = None
    storage_state: ArtifactStorageState = ArtifactStorageState.REGISTERED
    sensitivity: ArtifactSensitivity = ArtifactSensitivity.CLIENT_PRIVATE
    content_type: str | None = None
    sha256: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    tags: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        validate_safe_token(self.artifact_id, "artifact_id")
        validate_safe_token(self.client_slug, "client_slug")
        if self.run_id is not None:
            validate_safe_token(self.run_id, "run_id")
        self.relative_path = validate_relative_path(self.relative_path, "artifact relative_path")
        if self.uri is None:
            self.uri = f"workspace://{self.client_slug}/{self.relative_path}"
        if self.storage_state == ArtifactStorageState.MATERIALIZED and not self.sha256:
            raise ValueError("Materialized artifact requires sha256")


class ArtifactVersion(BaseModel):
    artifact_version_id: str = Field(default_factory=lambda: new_id("artifact_version"))
    artifact_ref_id: str
    version: int = Field(ge=1)
    sha256: str
    relative_path: str
    created_by: str = "system"
    created_at: str = Field(default_factory=_now_iso)
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        validate_relative_path(self.relative_path, "artifact version relative_path")
        if not self.sha256:
            raise ValueError("ArtifactVersion requires sha256")


class ArtifactManifest(BaseModel):
    artifact_manifest_id: str = Field(default_factory=lambda: new_id("artifact_manifest"))
    client_workspace_id: str
    run_id: str | None = None
    manifest_name: str
    artifact_refs: list[ArtifactRef]
    version_refs: list[ArtifactVersion] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.manifest_name:
            raise ValueError("ArtifactManifest requires manifest_name")
        if not self.artifact_refs:
            raise ValueError("ArtifactManifest requires artifact_refs")
        workspace_ids = {artifact.client_workspace_id for artifact in self.artifact_refs}
        if workspace_ids != {self.client_workspace_id}:
            raise ValueError("All artifact refs must belong to manifest workspace")
        if self.run_id:
            for artifact in self.artifact_refs:
                if artifact.run_id and artifact.run_id != self.run_id:
                    raise ValueError("Run manifest cannot include artifacts from a different run")


class ArtifactLineage(BaseModel):
    artifact_lineage_id: str = Field(default_factory=lambda: new_id("artifact_lineage"))
    source_artifact_ref_ids: list[str]
    derived_artifact_ref_id: str
    relation: LineageRelation
    operation: str
    tool_or_service: str | None = None
    source_receipt_refs: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_artifact_ref_ids:
            raise ValueError("ArtifactLineage requires source_artifact_ref_ids")
        if not self.derived_artifact_ref_id:
            raise ValueError("ArtifactLineage requires derived_artifact_ref_id")
        if self.derived_artifact_ref_id in self.source_artifact_ref_ids:
            raise ValueError("ArtifactLineage cannot derive artifact from itself")


class ArtifactReceipt(BaseModel):
    artifact_receipt_id: str = Field(default_factory=lambda: new_id("artifact_receipt"))
    artifact_ref_id: str
    receipt_type: str
    pass_status: PassStatus
    checks: dict[str, Any] = Field(default_factory=dict)
    blockers: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.receipt_type:
            raise ValueError("ArtifactReceipt requires receipt_type")
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("ArtifactReceipt with blockers cannot pass")


class WorkspaceMaterializationReceipt(BaseModel):
    workspace_materialization_receipt_id: str = Field(default_factory=lambda: new_id("workspace_materialization"))
    client_workspace_id: str
    created_paths: list[str]
    existing_paths: list[str] = Field(default_factory=list)
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("Workspace materialization with blockers cannot pass")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
