"""TS-APP-API-002 -- Harness Library API.

Four routes backed by a filesystem scan of exported AtomicHarnessDefinition
packages (Gap 1: the Builder itself has no listing capability -- see
docs/tech-specs/TS-APP-API-002.md section 1). The library-scanning helpers
that the spec describes as a separate `api/harness_library.py` module are
kept here, inlined, so this feature ships as a single self-contained file
(see the apply guide shipped alongside this file for why).

Field names below (``content["production_eligible"]``, the
``category_binding`` shapes, the envelope returned by
``PortableAtomicHarnessDefinition.from_payload_bytes`` /
``.content``, ``ProductizationCommandRequest``/``Result`` field names, and
the CONFLICT/NOT_FOUND/INVALID_MANIFEST semantics of
``BuilderProductizationService.execute``) were all confirmed directly
against the real classes in
``services/builder/src/cmf_builder/...`` -- not inferred from the spec's
citations alone.
"""
from __future__ import annotations

import logging
import os
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel

from ca_contracts import utc_now_rfc3339

from api.dependencies import get_builder
from api.errors import ErrorResponse

from cmf_builder.application.productization_contracts import (
    ProductizationCommandRequest,
    ProductizationError,
    ProductizationErrorCode,
)
from cmf_builder.domain.portable_export import (
    PortableAtomicHarnessDefinition,
    PortableDefinitionInvalid,
)

logger = logging.getLogger("ca.api.harness_library")

router = APIRouter()

DEFINITION_ENTRY = "atomic_harness_definition.json"


# ---------------------------------------------------------------------------
# Library scanning (spec section 3, 5, 7 Stage 1 -- inlined from the spec's
# proposed api/harness_library.py; see apply guide).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LibraryEntry:
    definition: PortableAtomicHarnessDefinition
    package_file: str
    package_hash: str
    added_at: str | None  # RFC 3339, from file mtime -- NON-AUTHORITATIVE


def _read_package(path: Path) -> LibraryEntry | None:
    try:
        archive_bytes = path.read_bytes()
        with zipfile.ZipFile(path) as archive:
            payload = archive.read(DEFINITION_ENTRY)
        definition = PortableAtomicHarnessDefinition.from_payload_bytes(payload)
    except (OSError, zipfile.BadZipFile, KeyError, PortableDefinitionInvalid) as error:
        logger.warning(
            "harness_library: skipping unreadable package file=%s error=%s",
            path.name,
            error,
        )
        return None
    mtime = path.stat().st_mtime
    added_at = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return LibraryEntry(
        definition=definition,
        package_file=path.name,
        package_hash=f"sha256:{sha256(archive_bytes).hexdigest()}",
        added_at=added_at,
    )


def list_library(root: Path) -> list[LibraryEntry]:
    if not root.is_dir():
        return []
    entries: list[LibraryEntry] = []
    for path in sorted(root.glob("*.zip")):
        entry = _read_package(path)
        if entry is not None:
            entries.append(entry)
    entries.sort(key=lambda e: (e.added_at or "", e.definition.definition_id), reverse=True)
    return entries


def find_by_definition_id(root: Path, definition_id: str) -> LibraryEntry | None:
    path = root / f"{definition_id}.zip"
    if not path.is_file():
        return None
    return _read_package(path)


# ---------------------------------------------------------------------------
# Dependency -- CA_HARNESS_LIBRARY_ROOT (spec section 7 Stage 0)
#
# api/config.py's AppConfig has no ca_harness_library_root field in this
# codebase yet, and this ticket's packaging is scoped to this router file
# plus tests only (no changes to api/config.py or api/dependencies.py). This
# dependency therefore resolves the same default the spec's Stage 0 patch
# would have added to AppConfig -- {CA_DATA_ROOT}/harness-library, overridable
# by CA_HARNESS_LIBRARY_ROOT -- directly from existing state. If a future
# change does add config.ca_harness_library_root, it is honored automatically.
# ---------------------------------------------------------------------------


def get_harness_library_root(request: Request) -> Path:
    config = request.app.state.config
    configured = getattr(config, "ca_harness_library_root", None)
    if configured is not None:
        return Path(configured)
    env_override = os.environ.get("CA_HARNESS_LIBRARY_ROOT")
    if env_override:
        return Path(env_override)
    return Path(config.ca_data_root) / "harness-library"


# ---------------------------------------------------------------------------
# Response models (spec section 6)
# ---------------------------------------------------------------------------


class HarnessSummary(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    category_name: str | None
    classification: list[str]
    capability_requirements: list[str]
    production_ready: bool
    certified: bool
    package_file: str
    package_hash: str
    added_at: str | None


class HarnessDetail(HarnessSummary):
    goal: str
    success_condition: str
    atomic_boundary: str
    input_contract: dict
    output_contract: dict
    minimum_complete_context: list[str]
    acceptance_tests: list[str]
    authority_chain: list[str]
    provenance_refs: list[str]
    execution_plan: list[str]
    category_binding: dict
    activative_intelligence: dict | None
    lineage: list[str]
    compiler_id: str
    compiler_version: str
    schema_id: str
    schema_version: str


class BuildHarnessResponse(BaseModel):
    definition_id: str
    definition_hash: str
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    package_file: str
    package_hash: str
    ingest_receipt_id: str
    build_receipt_id: str
    export_receipt_id: str


class EligibilityResponse(BaseModel):
    definition_id: str
    harness_category: str | None
    source_category: str
    status: str
    reason: str | None


# ---------------------------------------------------------------------------
# Error mapping (spec section 6 table)
# ---------------------------------------------------------------------------

_STATUS_FOR_ERROR: dict[ProductizationErrorCode, int] = {
    ProductizationErrorCode.INVALID_MANIFEST: 400,
    ProductizationErrorCode.INVALID_ACTIVATIVE_INPUT: 400,
    ProductizationErrorCode.AUTHORITY_REJECTED: 422,
    ProductizationErrorCode.HASH_MISMATCH: 500,
    ProductizationErrorCode.NOT_FOUND: 404,
    ProductizationErrorCode.CONFLICT: 409,
    ProductizationErrorCode.STORAGE_INTEGRITY: 500,
    ProductizationErrorCode.EXPORT_REJECTED: 500,
    ProductizationErrorCode.INTERNAL_ERROR: 500,
}


def _error_response(error_code: str, message: str) -> dict:
    return ErrorResponse(
        error_code=error_code,
        message=message,
        timestamp=utc_now_rfc3339(),
    ).model_dump()


def _raise_for(error: ProductizationError) -> None:
    status_code = _STATUS_FOR_ERROR.get(error.code, 500)
    raise HTTPException(
        status_code=status_code,
        detail=_error_response(error.code.value, str(error)),
    )


# ---------------------------------------------------------------------------
# Projections (spec section 5)
# ---------------------------------------------------------------------------


def _summary_from_entry(entry: LibraryEntry) -> HarnessSummary:
    content = entry.definition.content
    binding = content["category_binding"]
    return HarnessSummary(
        definition_id=entry.definition.definition_id,
        definition_hash=entry.definition.definition_hash,
        manifest_id=str(content["manifest_id"]),
        manifest_version=str(content["manifest_version"]),
        task_id=str(content["task_id"]),
        mode=str(content["mode"]),
        category_id=binding.get("category_id"),
        category_name=binding.get("category_name"),
        classification=list(content["classification"]),
        capability_requirements=list(content.get("capability_requirements") or []),
        production_ready=bool(content["production_eligible"]),
        certified=bool(content["certified"]),
        package_file=entry.package_file,
        package_hash=entry.package_hash,
        added_at=entry.added_at,
    )


def _detail_from_entry(entry: LibraryEntry) -> HarnessDetail:
    content = entry.definition.content
    summary = _summary_from_entry(entry)
    return HarnessDetail(
        **summary.model_dump(),
        goal=str(content["goal"]),
        success_condition=str(content["success_condition"]),
        atomic_boundary=str(content["atomic_boundary"]),
        input_contract=dict(content["input_contract"]),
        output_contract=dict(content["output_contract"]),
        minimum_complete_context=list(content["minimum_complete_context"]),
        acceptance_tests=list(content["acceptance_tests"]),
        authority_chain=list(content["authority_chain"]),
        provenance_refs=list(content["provenance_refs"]),
        execution_plan=list(content["execution_plan"]),
        category_binding=dict(content["category_binding"]),
        activative_intelligence=(
            dict(content["activative_intelligence"])
            if content["activative_intelligence"] is not None
            else None
        ),
        lineage=list(content["lineage"]),
        compiler_id=str(content["compiler_id"]),
        compiler_version=str(content["compiler_version"]),
        schema_id=str(content["schema_id"]),
        schema_version=str(content["schema_version"]),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get("", response_model=list[HarnessSummary])
def list_harnesses(library_root: Path = Depends(get_harness_library_root)):
    try:
        entries = list_library(library_root)
    except OSError as error:
        # Section 8: CA_HARNESS_LIBRARY_ROOT exists but is unreadable (bad
        # permissions, not a directory, etc.) -- flagged in the spec as a
        # required addition beyond the literal Stage 1 code, since a missing
        # directory is already handled by list_library() returning [].
        raise HTTPException(
            status_code=500,
            detail=_error_response(
                "LIBRARY_UNREADABLE", f"Harness library directory is unreadable: {error}"
            ),
        ) from error
    return [_summary_from_entry(entry) for entry in entries]


@router.get("/{definition_id}", response_model=HarnessDetail)
def get_harness(
    definition_id: str,
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    entry = find_by_definition_id(library_root, definition_id)
    if entry is not None:
        return _detail_from_entry(entry)

    try:
        result = builder.execute(
            ProductizationCommandRequest(command="inspect", artifact_id=definition_id)
        )
    except ProductizationError as error:
        _raise_for(error)
        raise AssertionError("unreachable")  # pragma: no cover

    if result.payload.get("record_kind") != "atomic_harness_definition":
        # Either a manifest_id (ingested but never built) or an unexpected
        # record kind -- neither is a Harness.
        raise HTTPException(
            status_code=404,
            detail=_error_response(
                "NOT_FOUND", f"No Harness with id '{definition_id}' exists."
            ),
        )

    artifact = result.payload["artifact"]["definition"]
    binding = artifact["category_binding"]
    return HarnessDetail(
        definition_id=result.artifact_id,
        definition_hash=result.artifact_hash,
        manifest_id=artifact["manifest_id"],
        manifest_version=artifact["manifest_version"],
        task_id=artifact["task_id"],
        mode=artifact["mode"],
        category_id=binding.get("category_id"),
        category_name=binding.get("category_name"),
        classification=artifact["classification"],
        capability_requirements=artifact.get("capability_requirements") or [],
        production_ready=bool(artifact["production_eligible"]),
        certified=bool(artifact["certified"]),
        package_file="",
        package_hash="",
        added_at=None,
        goal=artifact["goal"],
        success_condition=artifact["success_condition"],
        atomic_boundary=artifact["atomic_boundary"],
        input_contract=artifact["input_contract"],
        output_contract=artifact["output_contract"],
        minimum_complete_context=artifact["minimum_complete_context"],
        acceptance_tests=artifact["acceptance_tests"],
        authority_chain=artifact["authority_chain"],
        provenance_refs=artifact["provenance_refs"],
        execution_plan=artifact["execution_plan"],
        category_binding=binding,
        activative_intelligence=artifact["activative_intelligence"],
        lineage=artifact["lineage"],
        compiler_id=artifact["compiler_id"],
        compiler_version=artifact["compiler_version"],
        schema_id=artifact["schema_id"],
        schema_version=artifact["schema_version"],
    )


@router.post("/build", response_model=BuildHarnessResponse, status_code=201)
async def build_harness(
    request: Request,
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    manifest_bytes = await request.body()

    # Builder's _ingest() requires a filesystem path, not bytes (spec section
    # 3). library_root's parent is used as the tmp dir so the temp file and
    # the eventual destination live on the same filesystem/volume.
    library_root.parent.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(
        suffix=".manifest.json", delete=False, dir=library_root.parent
    )
    tmp_path = Path(tmp.name)
    build_result = None
    try:
        tmp.write(manifest_bytes)
        tmp.close()

        try:
            ingest_result = builder.execute(
                ProductizationCommandRequest(command="ingest", manifest_path=tmp_path)
            )
            build_result = builder.execute(
                ProductizationCommandRequest(
                    command="build", artifact_id=ingest_result.artifact_id
                )
            )
            library_root.mkdir(parents=True, exist_ok=True)
            destination = library_root / f"{build_result.artifact_id}.zip"
            export_result = builder.execute(
                ProductizationCommandRequest(
                    command="export",
                    artifact_id=build_result.artifact_id,
                    output_path=destination,
                )
            )
        except ProductizationError as error:
            _raise_for(error)
            raise AssertionError("unreachable")  # pragma: no cover
    finally:
        tmp_path.unlink(missing_ok=True)

    entry = find_by_definition_id(library_root, build_result.artifact_id)
    if entry is None:
        raise HTTPException(
            status_code=500,
            detail=_error_response(
                "INTERNAL_ERROR",
                "Export reported success but the package is not readable.",
            ),
        )

    logger.info(
        "harness build succeeded definition_id=%s manifest_id=%s "
        "ingest_receipt=%s build_receipt=%s export_receipt=%s",
        entry.definition.definition_id,
        ingest_result.artifact_id,
        ingest_result.receipt_id,
        build_result.receipt_id,
        export_result.receipt_id,
    )

    content = entry.definition.content
    binding = content["category_binding"]
    return BuildHarnessResponse(
        definition_id=entry.definition.definition_id,
        definition_hash=entry.definition.definition_hash,
        manifest_id=str(content["manifest_id"]),
        manifest_version=str(content["manifest_version"]),
        task_id=str(content["task_id"]),
        mode=str(content["mode"]),
        category_id=binding.get("category_id"),
        package_file=entry.package_file,
        package_hash=entry.package_hash,
        ingest_receipt_id=ingest_result.receipt_id,
        build_receipt_id=build_result.receipt_id,
        export_receipt_id=export_result.receipt_id,
    )


@router.get("/{definition_id}/eligibility", response_model=EligibilityResponse)
def check_eligibility(
    definition_id: str,
    source_category: str = Query(..., min_length=1),
    library_root: Path = Depends(get_harness_library_root),
    builder=Depends(get_builder),
):
    detail = get_harness(definition_id, library_root=library_root, builder=builder)

    if detail.mode == "generic":
        return EligibilityResponse(
            definition_id=definition_id,
            harness_category=None,
            source_category=source_category,
            status="NOT_APPLICABLE",
            reason="Harness is category-neutral (generic mode); it has no category to match.",
        )

    harness_category = detail.category_binding.get("category_id")
    if harness_category == source_category:
        return EligibilityResponse(
            definition_id=definition_id,
            harness_category=harness_category,
            source_category=source_category,
            status="ELIGIBLE",
            reason=None,
        )

    return EligibilityResponse(
        definition_id=definition_id,
        harness_category=harness_category,
        source_category=source_category,
        status="INELIGIBLE",
        reason=(
            f"Harness is bound to category '{harness_category}', "
            f"not '{source_category}'."
        ),
    )
