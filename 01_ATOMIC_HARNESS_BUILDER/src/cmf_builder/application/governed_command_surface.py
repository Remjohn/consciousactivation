"""Stable governed command surface for OD-AM-004 / ST-10.09."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class GovernedCommandError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class CommandType(str, Enum):
    LIST_RUNS = "LIST_RUNS"
    INSPECT_RUN = "INSPECT_RUN"
    EXPLORE_GRAPH = "EXPLORE_GRAPH"
    INSPECT_DECISION = "INSPECT_DECISION"
    REVIEW_GENESIS_DECISION = "REVIEW_GENESIS_DECISION"
    TRACE_SKILL = "TRACE_SKILL"
    INSPECT_OWNERSHIP = "INSPECT_OWNERSHIP"
    VIEW_AUTHORIZATION_TRAJECTORY = "VIEW_AUTHORIZATION_TRAJECTORY"
    MONITOR_WORKFLOW = "MONITOR_WORKFLOW"
    EXPORT_RECEIPT = "EXPORT_RECEIPT"
    EXPORT_EVIDENCE_BUNDLE = "EXPORT_EVIDENCE_BUNDLE"


READ_ONLY = frozenset(CommandType)


@dataclass(frozen=True)
class GovernedCommand:
    command_id: str
    command_type: CommandType
    operator_identity: str
    authority_requirement: str
    input_contract: dict[str, Any]
    requested_scope: str
    source_revision: str
    execution_timestamp: str

    @property
    def command_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "command_type": self.command_type.value,
            "operator_identity": self.operator_identity,
            "authority_requirement": self.authority_requirement,
            "input_contract": self.input_contract,
            "requested_scope": self.requested_scope,
            "source_revision": self.source_revision,
            "execution_timestamp": self.execution_timestamp,
        }


@dataclass(frozen=True)
class CommandReceipt:
    command_identity: str
    result_status: str
    result_identity: str
    receipt_identity: str
    export_identity: str | None
    limitations: tuple[str, ...]
    production_ready: bool = False
    certified: bool = False


class InMemoryCommandLedger:
    def __init__(self) -> None:
        self._receipts: dict[str, CommandReceipt] = {}

    def execute(self, command: GovernedCommand, *, authority_granted: bool, result_payload: dict[str, Any]) -> CommandReceipt:
        if not authority_granted:
            raise GovernedCommandError("COMMAND_AUTHORITY_DENIED", "authority must validate before execution")
        if command.command_type not in READ_ONLY:
            raise GovernedCommandError("UNKNOWN_COMMAND", "unknown command")
        if not command.input_contract:
            raise GovernedCommandError("INVALID_COMMAND_INPUT", "input contract is required")
        if command.command_identity in self._receipts:
            return self._receipts[command.command_identity]
        if result_payload.get("invalidated_as_active"):
            raise GovernedCommandError("INVALIDATED_RECORD_EXPORT_ACTIVE", "invalidated records cannot export as active")
        if result_payload.get("absolute_path"):
            raise GovernedCommandError("PORTABLE_EXPORT_ABSOLUTE_PATH", "portable exports cannot contain absolute local paths")
        if result_payload.get("secret"):
            raise GovernedCommandError("SECRET_IN_COMMAND_RECEIPT", "secrets cannot enter command receipts")
        if result_payload.get("production_ready") or result_payload.get("certified"):
            raise GovernedCommandError("DEVELOPMENT_EXPORTED_AS_PRODUCTION_CERTIFICATION", "development cannot export as production/certification")
        result_identity = sha256_of(result_payload)
        export_identity = result_identity if command.command_type in {CommandType.EXPORT_RECEIPT, CommandType.EXPORT_EVIDENCE_BUNDLE} else None
        receipt_identity = sha256_of(
            {
                "command_identity": command.command_identity,
                "result_status": "PASS",
                "result_identity": result_identity,
                "export_identity": export_identity,
                "limitations": ["offline_development_only"],
            }
        )
        receipt = CommandReceipt(command.command_identity, "PASS", result_identity, receipt_identity, export_identity, ("offline_development_only",))
        self._receipts[command.command_identity] = receipt
        return receipt


def export_receipt_bundle(source_identities: tuple[str, ...], source_hashes: dict[str, str], included_objects: tuple[dict[str, Any], ...], redacted_objects: tuple[str, ...]) -> dict[str, Any]:
    payload = {
        "export_schema_version": "cmf-builder-portable-receipt-export/v1",
        "source_identities": list(source_identities),
        "source_hashes": source_hashes,
        "included_objects": list(included_objects),
        "excluded_redacted_objects": list(redacted_objects),
        "limitations": ["offline_development_only", "not_production", "not_certification"],
        "production_ready": False,
        "certified": False,
    }
    payload["deterministic_manifest"] = sha256_of(payload)
    payload["export_identity"] = sha256_of(payload)
    return payload
