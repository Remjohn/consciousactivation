"""Stable accessible operator shell for OD-AM-005 / ST-10.10."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class ShellError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class OutputMode(str, Enum):
    HUMAN = "HUMAN"
    MACHINE = "MACHINE"


class ShellCommand(str, Enum):
    HELP = "help"
    RUN_LIST = "run list"
    RUN_INSPECT = "run inspect"
    GRAPH_EXPLORE = "graph explore"
    DECISION_INSPECT = "decision inspect"
    GENESIS_REVIEW = "genesis review"
    SKILL_TRACE = "skill trace"
    OWNERSHIP_INSPECT = "ownership inspect"
    AUTH_TRAJECTORY = "auth trajectory"
    WORKFLOW_MONITOR = "workflow monitor"
    RECEIPT_EXPORT = "receipt export"
    EVIDENCE_EXPORT = "evidence export"
    INGEST = "ingest"
    BUILD = "build"
    INSPECT = "inspect"
    EXPORT = "export"


READ_ONLY_COMMANDS = frozenset(ShellCommand)
NEEDS_SUBJECT = {
    ShellCommand.RUN_INSPECT,
    ShellCommand.GRAPH_EXPLORE,
    ShellCommand.DECISION_INSPECT,
    ShellCommand.GENESIS_REVIEW,
    ShellCommand.SKILL_TRACE,
    ShellCommand.OWNERSHIP_INSPECT,
    ShellCommand.AUTH_TRAJECTORY,
    ShellCommand.WORKFLOW_MONITOR,
    ShellCommand.RECEIPT_EXPORT,
    ShellCommand.EVIDENCE_EXPORT,
}


@dataclass(frozen=True)
class ShellRequest:
    raw_command: str
    command: ShellCommand
    subject: str
    operator_identity: str
    authority_identity: str
    output_mode: OutputMode = OutputMode.MACHINE
    revision: str = "development"

    @property
    def command_identity(self) -> str:
        return sha256_of(
            {
                "command": self.command.value,
                "subject": self.subject,
                "operator_identity": self.operator_identity,
                "authority_identity": self.authority_identity,
                "output_mode": self.output_mode.value,
                "revision": self.revision,
            }
        )


@dataclass(frozen=True)
class ShellResponse:
    command_identity: str
    status: str
    exit_code: int
    output_mode: OutputMode
    payload: dict[str, Any]
    message: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "command_identity": self.command_identity,
            "status": self.status,
            "exit_code": self.exit_code,
            "output_mode": self.output_mode.value,
            "payload": self.payload,
            "message": self.message,
        }


def parse_shell_command(raw: str, *, operator_identity: str, authority_identity: str, output_mode: OutputMode = OutputMode.MACHINE) -> ShellRequest:
    if not operator_identity or not authority_identity:
        raise ShellError("SHELL_AUTHORITY_REQUIRED", "operator and authority identity are required")
    normalized = " ".join(raw.strip().split())
    if not normalized:
        raise ShellError("EMPTY_COMMAND", "command is required")
    mode_match = re.search(r"\s+--(json|human)$", normalized)
    if mode_match:
        output_mode = OutputMode.MACHINE if mode_match.group(1) == "json" else OutputMode.HUMAN
        normalized = normalized[: mode_match.start()].strip()
    for command in sorted(ShellCommand, key=lambda item: len(item.value), reverse=True):
        if normalized == command.value:
            subject = "ALL"
        elif normalized.startswith(command.value + " "):
            subject = normalized[len(command.value) + 1 :].strip()
        else:
            continue
        if command in NEEDS_SUBJECT and subject == "ALL":
            raise ShellError("SHELL_SUBJECT_REQUIRED", "command requires a subject", command=command.value)
        if re.match(r"^[A-Za-z]:[/\\]", subject) or subject.startswith(("/", "\\")):
            raise ShellError("PORTABLE_PATH_REQUIRED", "shell subjects must be portable identifiers")
        return ShellRequest(raw, command, subject, operator_identity, authority_identity, output_mode)
    raise ShellError("UNKNOWN_SHELL_COMMAND", "unknown governed shell command", raw=raw)


def shell_help() -> dict[str, Any]:
    commands = [
        {"command": command.value, "read_only": command in READ_ONLY_COMMANDS, "requires_subject": command in NEEDS_SUBJECT}
        for command in sorted(ShellCommand, key=lambda item: item.value)
    ]
    return {
        "shell": "cmf-builder-governed-operator-shell",
        "accessibility": ["no_color_required", "deterministic_order", "machine_readable_output", "keyboard_only"],
        "commands": commands,
        "production_ready": False,
        "certified": False,
    }


def execute_shell_request(request: ShellRequest, data: dict[str, Any], *, authority_granted: bool = True) -> ShellResponse:
    if not authority_granted:
        return ShellResponse(request.command_identity, "REJECTED", 13, request.output_mode, {"reason": "AUTHORITY_DENIED"}, "authority denied")
    if data.get("secret") or data.get("credential"):
        return ShellResponse(request.command_identity, "REJECTED", 70, request.output_mode, {"reason": "SECRET_EXCLUDED"}, "secret excluded")
    if data.get("hidden_mutation"):
        return ShellResponse(request.command_identity, "REJECTED", 71, request.output_mode, {"reason": "HIDDEN_MUTATION_REJECTED"}, "hidden mutation rejected")
    payload = shell_help() if request.command is ShellCommand.HELP else {"subject": request.subject, "result": data, "stable_order": sorted(data)}
    return ShellResponse(request.command_identity, "OK", 0, request.output_mode, payload, "ok")
