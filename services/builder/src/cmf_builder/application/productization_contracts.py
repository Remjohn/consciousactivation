from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping, Protocol


class ProductizationErrorCode(str, Enum):
    INVALID_MANIFEST = "INVALID_MANIFEST"
    INVALID_ACTIVATIVE_INPUT = "INVALID_ACTIVATIVE_INPUT"
    AUTHORITY_REJECTED = "AUTHORITY_REJECTED"
    HASH_MISMATCH = "HASH_MISMATCH"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    STORAGE_INTEGRITY = "STORAGE_INTEGRITY"
    EXPORT_REJECTED = "EXPORT_REJECTED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ProductizationError(Exception):
    def __init__(
        self,
        code: ProductizationErrorCode,
        message: str,
        *,
        field_path: str | None = None,
        context: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.field_path = field_path
        self.context = dict(context or {})


@dataclass(frozen=True, slots=True)
class ActivativeInputContract:
    source_premise_ref: str
    identity_dna_ref: str
    context_premise_ref: str
    resonance_map_ref: str
    matrix_of_edging_ref: str
    activative_intelligence_pack_ref: str
    hidden_pressure: str
    activation_directions: tuple[str, ...]
    roles: tuple[str, ...]
    stance: str
    stakes: tuple[str, ...]
    identity_urges: tuple[str, ...]
    participation_design: str
    intended_reaction: str
    smallest_useful_commitment: str
    evidence_provenance_refs: tuple[str, ...]
    evaluation_contract_ref: str
    wrong_reading_locks: tuple[str, ...]
    reaction_receipt_refs: tuple[str, ...] = ()
    expression_moment_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class OperatorManifestRequest:
    manifest_bytes: bytes
    source_name: str


@dataclass(frozen=True, slots=True)
class OperatorManifestResult:
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: str
    category_id: str | None
    canonical_bytes: bytes
    manifest_hash: str
    normalized: Mapping[str, object]
    activative_input: ActivativeInputContract | None


@dataclass(frozen=True, slots=True)
class DurableRecord:
    record_kind: str
    record_id: str
    version: int
    payload: bytes
    payload_hash: str


@dataclass(frozen=True, slots=True)
class DurableCommandReceipt:
    command_id: str
    payload_hash: str
    result_kind: str
    result_id: str
    result_hash: str


class DurableProductizationRepository(Protocol):
    def initialize(self) -> None: ...

    def commit_record(
        self,
        record: DurableRecord,
        *,
        command_receipt: DurableCommandReceipt,
        expected_version: int | None,
    ) -> DurableCommandReceipt: ...

    def get_record(self, record_kind: str, record_id: str) -> DurableRecord | None: ...

    def get_command_receipt(self, command_id: str) -> DurableCommandReceipt | None: ...

    def verify_integrity(self) -> tuple[str, ...]: ...


@dataclass(frozen=True, slots=True)
class ProductizationCommandRequest:
    command: str
    manifest_path: Path | None = None
    output_path: Path | None = None
    artifact_id: str | None = None


@dataclass(frozen=True, slots=True)
class ProductizationCommandResult:
    command: str
    status: str
    artifact_id: str | None
    artifact_hash: str | None
    receipt_id: str | None
    payload: Mapping[str, object]


class ProductizationApplicationService(Protocol):
    def execute(self, request: ProductizationCommandRequest) -> ProductizationCommandResult: ...


@dataclass(frozen=True, slots=True)
class PortableExportRequest:
    definition_id: str
    destination: Path


@dataclass(frozen=True, slots=True)
class PortableExportResult:
    package_id: str
    package_hash: str
    destination: Path
    file_hashes: tuple[tuple[str, str], ...]
    receipt_id: str


class PortableExportService(Protocol):
    def export(self, request: PortableExportRequest) -> PortableExportResult: ...
