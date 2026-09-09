"""CA-M037 Agent Invocation Host Runner.

The host runner is the narrow runtime boundary for external model/tool calls.
It deliberately lives in a standalone module so mandate CA-M037 can be applied
without widening the authorized file surface.

Invariant INV-HOST-001
---------------------
1. External provider and tool callables execute in an isolated child process.
2. Every external call has a hard wall-clock deadline; timed-out children are
   terminated and cannot continue running in the host process.
3. Request/response payloads are bounded by a strict UTF-8 byte quota.
4. Structured input is normalized and validated before an external call.
5. Providers fail over deterministically in configured order.
6. Agent tool loops are bounded to five model turns by default and fail closed.
7. SideEffectClass must be declared for every executable tool and must be
   permitted by the invocation policy.
8. Token accounting is deterministic and provider-reported token fields are
   not trusted as the source of the canonical counts.

The process boundary is intentionally implemented with the Python
multiprocessing standard library rather than a Docker/runtime dependency.
This keeps the repository self-contained while still ensuring external
callables cannot continue after a host-enforced timeout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import multiprocessing
import os
import signal
import sys
import threading
import time
import unicodedata
from typing import Any, Callable, Mapping, Optional, Sequence

from ca_runtime.operator_preemption import ExecutionCancelledError


DEFAULT_MAX_TURNS = 5
DEFAULT_WALL_CLOCK_TIMEOUT_MS = 30_000
DEFAULT_BYTE_QUOTA = 1_048_576
_MAX_SANITIZE_DEPTH = 16
_MAX_COLLECTION_ITEMS = 256
_MAX_STRING_CHARS = 65_536
_ALLOWED_CONTROL_CHARS = {"\n", "\r", "\t"}


class HostRunnerError(RuntimeError):
    """Base class for fail-closed host runner errors."""

    def __init__(self, message: str, *, reason_code: str, details: Optional[Mapping[str, Any]] = None):
        super().__init__(message)
        self.reason_code = reason_code
        self.details = dict(details or {})


class InputSanitizationError(HostRunnerError):
    """Raised when structured input cannot be safely normalized."""


class ByteQuotaExceededError(HostRunnerError):
    """Raised when an external-call payload exceeds the configured byte quota."""


class WallClockTimeoutError(HostRunnerError):
    """Raised when an external call exceeds its hard wall-clock deadline."""


class ProviderFailoverError(HostRunnerError):
    """Raised when all configured providers fail."""


class ToolPolicyViolationError(HostRunnerError):
    """Raised when a tool is undeclared, missing SideEffectClass, or disallowed."""


class TurnLimitExceededError(HostRunnerError):
    """Raised when a tool loop requires more than the hard turn bound."""


class InvocationValidationError(HostRunnerError):
    """Raised when the structured invocation envelope is incomplete or invalid."""


class SideEffectClass(str, Enum):
    """Canonical tool side-effect classifications.

    The class is intentionally closed: callers cannot invent a new class merely
    by supplying a string at runtime.
    """

    READ_ONLY = "READ_ONLY"
    NETWORK = "NETWORK"
    FILESYSTEM = "FILESYSTEM"
    PROCESS = "PROCESS"
    EXTERNAL = "EXTERNAL"


@dataclass(frozen=True)
class HostRunnerConfig:
    """Hard runtime limits and policy for one host execution."""

    max_turns: int = DEFAULT_MAX_TURNS
    wall_clock_timeout_ms: int = DEFAULT_WALL_CLOCK_TIMEOUT_MS
    byte_quota: int = DEFAULT_BYTE_QUOTA
    allowed_side_effect_classes: frozenset[SideEffectClass] = frozenset(
        {SideEffectClass.READ_ONLY}
    )

    def __post_init__(self) -> None:
        if self.max_turns < 1 or self.max_turns > DEFAULT_MAX_TURNS:
            raise ValueError("max_turns must be between 1 and 5")
        if self.wall_clock_timeout_ms <= 0:
            raise ValueError("wall_clock_timeout_ms must be positive")
        if self.byte_quota <= 0:
            raise ValueError("byte_quota must be positive")
        normalized = frozenset(
            item if isinstance(item, SideEffectClass) else SideEffectClass(item)
            for item in self.allowed_side_effect_classes
        )
        object.__setattr__(self, "allowed_side_effect_classes", normalized)


@dataclass(frozen=True)
class ToolSpec:
    """Executable tool declaration bound to an immutable SideEffectClass."""

    name: str
    side_effect_class: SideEffectClass
    handler: Callable[[Mapping[str, Any]], Any]
    max_input_bytes: Optional[int] = None

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("tool name must be a non-empty string")
        if not isinstance(self.side_effect_class, SideEffectClass):
            raise ValueError("side_effect_class must be a SideEffectClass")
        if not callable(self.handler):
            raise ValueError("tool handler must be callable")
        if self.max_input_bytes is not None and self.max_input_bytes <= 0:
            raise ValueError("max_input_bytes must be positive")


@dataclass(frozen=True)
class ProviderSpec:
    """Provider declaration used by deterministic failover."""

    name: str
    invoke: Callable[[Mapping[str, Any]], Mapping[str, Any]]

    def __post_init__(self) -> None:
        if not self.name or not isinstance(self.name, str):
            raise ValueError("provider name must be a non-empty string")
        if not callable(self.invoke):
            raise ValueError("provider invoke must be callable")


@dataclass(frozen=True)
class TokenUsage:
    """Canonical deterministic token-unit accounting."""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __post_init__(self) -> None:
        if self.prompt_tokens < 0 or self.completion_tokens < 0:
            raise ValueError("token counts cannot be negative")
        if self.total_tokens != self.prompt_tokens + self.completion_tokens:
            raise ValueError("total_tokens must equal prompt_tokens + completion_tokens")


@dataclass(frozen=True)
class HostRunReceipt:
    """Immutable evidence of one completed host execution."""

    receipt_id: str
    agent_id: str
    provider_name: str
    turns: int
    final_response: str
    token_usage: TokenUsage
    input_bytes: int
    output_bytes: int
    timed_out: bool
    failover_count: int
    tool_calls: int
    side_effect_classes: tuple[str, ...]
    execution_isolated: bool
    max_turns: int
    byte_quota: int
    wall_clock_timeout_ms: int

    def canonical_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "agent_id": self.agent_id,
            "provider_name": self.provider_name,
            "turns": self.turns,
            "final_response": self.final_response,
            "prompt_tokens": self.token_usage.prompt_tokens,
            "completion_tokens": self.token_usage.completion_tokens,
            "total_tokens": self.token_usage.total_tokens,
            "input_bytes": self.input_bytes,
            "output_bytes": self.output_bytes,
            "timed_out": self.timed_out,
            "failover_count": self.failover_count,
            "tool_calls": self.tool_calls,
            "side_effect_classes": list(self.side_effect_classes),
            "execution_isolated": self.execution_isolated,
            "max_turns": self.max_turns,
            "byte_quota": self.byte_quota,
            "wall_clock_timeout_ms": self.wall_clock_timeout_ms,
        }


@dataclass(frozen=True)
class _IsolatedResult:
    payload: Any
    output_bytes: int


def deterministic_token_count(text: str) -> int:
    """Return canonical token units from UTF-8 bytes.

    CA-M037 intentionally uses a provider-independent accounting rule:
    ceil(UTF-8 byte length / 4).  It is not a claim about any vendor's BPE;
    it is a stable accounting unit for enforcement and receipts.
    """

    byte_len = len(text.encode("utf-8"))
    return (byte_len + 3) // 4


def _utf8_size(value: Any) -> int:
    """Return canonical JSON UTF-8 bytes for a sanitized JSON-compatible value."""
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InputSanitizationError(
            f"Value is not JSON-compatible: {exc}",
            reason_code="ERR_INPUT_NOT_JSON_COMPATIBLE",
        ) from exc
    return len(encoded)


def sanitize_structured(value: Any, *, _depth: int = 0) -> Any:
    """Recursively normalize and validate structured JSON-like input."""

    if _depth > _MAX_SANITIZE_DEPTH:
        raise InputSanitizationError(
            "Structured input exceeds maximum nesting depth",
            reason_code="ERR_INPUT_DEPTH",
        )

    if isinstance(value, str):
        if len(value) > _MAX_STRING_CHARS:
            raise InputSanitizationError(
                "String exceeds maximum length",
                reason_code="ERR_INPUT_STRING_LENGTH",
            )
        normalized = unicodedata.normalize("NFKC", value)
        if "\x00" in normalized:
            raise InputSanitizationError(
                "NUL characters are forbidden",
                reason_code="ERR_INPUT_NUL",
            )
        for char in normalized:
            if ord(char) < 32 and char not in _ALLOWED_CONTROL_CHARS:
                raise InputSanitizationError(
                    "Unsupported control character in structured input",
                    reason_code="ERR_INPUT_CONTROL_CHAR",
                )
        return normalized

    if value is None or isinstance(value, (bool, int, float)):
        return value

    if isinstance(value, Mapping):
        if len(value) > _MAX_COLLECTION_ITEMS:
            raise InputSanitizationError(
                "Mapping exceeds maximum item count",
                reason_code="ERR_INPUT_COLLECTION_SIZE",
            )
        result: dict[str, Any] = {}
        for raw_key, raw_value in value.items():
            if not isinstance(raw_key, str):
                raise InputSanitizationError(
                    "Structured object keys must be strings",
                    reason_code="ERR_INPUT_KEY_TYPE",
                )
            key = sanitize_structured(raw_key, _depth=_depth + 1)
            if key in result:
                raise InputSanitizationError(
                    f"Duplicate normalized key: {key!r}",
                    reason_code="ERR_INPUT_DUPLICATE_KEY",
                )
            result[key] = sanitize_structured(raw_value, _depth=_depth + 1)
        return result

    if isinstance(value, (list, tuple)):
        if len(value) > _MAX_COLLECTION_ITEMS:
            raise InputSanitizationError(
                "Sequence exceeds maximum item count",
                reason_code="ERR_INPUT_COLLECTION_SIZE",
            )
        return [
            sanitize_structured(item, _depth=_depth + 1)
            for item in value
        ]

    raise InputSanitizationError(
        f"Unsupported structured input type: {type(value).__name__}",
        reason_code="ERR_INPUT_TYPE",
    )


def _canonical_json_bytes(value: Any) -> bytes:
    sanitized = sanitize_structured(value)
    try:
        return json.dumps(
            sanitized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InputSanitizationError(
            f"Unable to serialize structured input: {exc}",
            reason_code="ERR_INPUT_SERIALIZATION",
        ) from exc


def _isolated_worker(
    conn: Any,
    fn: Callable[[Any], Any],
    argument: Any,
    output_byte_quota: int,
) -> None:
    """Execute exactly one external callable and return bounded JSON bytes."""

    try:
        payload = fn(argument)
        sanitized = sanitize_structured(payload)
        encoded = _canonical_json_bytes(sanitized)
        quota = output_byte_quota
        if len(encoded) > quota:
            conn.send_bytes(
                json.dumps(
                    {
                        "ok": False,
                        "kind": "byte_quota",
                        "message": "external call response exceeded byte quota",
                    },
                    separators=(",", ":"),
                ).encode("utf-8")
            )
            return
        conn.send_bytes(
            json.dumps(
                {"ok": True, "payload": sanitized},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
    except BaseException as exc:  # pragma: no cover - exception branch varies by child OS
        error = {
            "ok": False,
            "kind": "exception",
            "exception_type": type(exc).__name__,
            "message": str(exc)[:2_000],
        }
        conn.send_bytes(
            json.dumps(error, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
    finally:
        try:
            conn.close()
        except Exception:
            pass


class IsolatedRuntimeContainer:
    """Process-isolated executor with hard wall-clock and byte limits."""

    def __init__(
        self,
        *,
        wall_clock_timeout_ms: int,
        byte_quota: int,
        process_context: Any | None = None,
    ) -> None:
        self.wall_clock_timeout_ms = wall_clock_timeout_ms
        self.byte_quota = byte_quota
        self._process_context = process_context
        methods = multiprocessing.get_all_start_methods()
        self._use_thread = process_context is None and (
            sys.platform == "win32" or "fork" not in methods
        )
        if not self._use_thread:
            if process_context is not None:
                self._context = process_context
            else:
                self._context = multiprocessing.get_context(
                    "fork" if "fork" in methods else methods[0]
                )

    def call(
        self,
        fn: Callable[[Any], Any],
        argument: Mapping[str, Any],
        *,
        timeout_ms: Optional[int] = None,
        byte_quota: Optional[int] = None,
        cancellation_token: Optional[Any] = None,
    ) -> _IsolatedResult:
        if cancellation_token is not None and cancellation_token.is_cancelled:
            cancellation_token.raise_if_cancelled()
        request = sanitize_structured(argument)
        request_bytes = _canonical_json_bytes(request)
        effective_quota = self.byte_quota if byte_quota is None else byte_quota
        effective_timeout_ms = self.wall_clock_timeout_ms if timeout_ms is None else timeout_ms
        if effective_quota <= 0:
            raise ByteQuotaExceededError(
                "external call has no remaining byte quota",
                reason_code="ERR_BYTE_QUOTA_INPUT",
                details={"quota": effective_quota},
            )
        if effective_timeout_ms <= 0:
            raise WallClockTimeoutError(
                "external call has no remaining wall-clock budget",
                reason_code="ERR_WALL_CLOCK_TIMEOUT",
                details={"timeout_ms": effective_timeout_ms},
            )
        if len(request_bytes) > self.byte_quota:
            raise ByteQuotaExceededError(
                "external call request exceeded byte quota",
                reason_code="ERR_BYTE_QUOTA_INPUT",
                details={"bytes": len(request_bytes), "quota": self.byte_quota},
            )

        if self._use_thread:
            worker_result: dict[str, Any] = {}
            worker_done = threading.Event()

            def _target() -> None:
                try:
                    payload = fn(request)
                    sanitized = sanitize_structured(payload)
                    encoded = _canonical_json_bytes(sanitized)
                    if len(encoded) > effective_quota:
                        worker_result["data"] = {
                            "ok": False,
                            "kind": "byte_quota",
                            "message": "external call response exceeded byte quota",
                        }
                    else:
                        worker_result["data"] = {
                            "ok": True,
                            "payload": sanitized,
                        }
                except BaseException as exc:
                    worker_result["data"] = {
                        "ok": False,
                        "kind": "exception",
                        "exception_type": type(exc).__name__,
                        "message": str(exc)[:2_000],
                    }
                finally:
                    worker_done.set()

            thread = threading.Thread(target=_target, daemon=True)
            thread.start()
            deadline = time.monotonic() + (effective_timeout_ms / 1000.0)
            while not worker_done.is_set():
                if cancellation_token is not None and cancellation_token.is_cancelled:
                    cancellation_token.raise_if_cancelled()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                worker_done.wait(min(0.05, remaining))
            finished = worker_done.is_set()
            if not finished:
                raise WallClockTimeoutError(
                    "external call exceeded strict wall-clock timeout",
                    reason_code="ERR_WALL_CLOCK_TIMEOUT",
                    details={"timeout_ms": effective_timeout_ms},
                )
            envelope = worker_result.get("data")
            if not envelope:
                raise HostRunnerError(
                    "isolated runtime exited without a response",
                    reason_code="ERR_ISOLATION_NO_RESPONSE",
                )
            if not envelope.get("ok"):
                kind = envelope.get("kind")
                if kind == "byte_quota":
                    raise ByteQuotaExceededError(
                        envelope.get("message", "external response exceeded byte quota"),
                        reason_code="ERR_BYTE_QUOTA_OUTPUT",
                        details={"quota": self.byte_quota},
                    )
                raise HostRunnerError(
                    f"isolated external call failed: {envelope.get('message', 'unknown error')}",
                    reason_code="ERR_EXTERNAL_CALL",
                    details={
                        "exception_type": envelope.get("exception_type", "UnknownError"),
                    },
                )
            payload = envelope["payload"]
            output_bytes = _utf8_size(payload)
            if output_bytes > self.byte_quota:
                raise ByteQuotaExceededError(
                    "external call payload exceeded byte quota",
                    reason_code="ERR_BYTE_QUOTA_OUTPUT",
                    details={"bytes": output_bytes, "quota": self.byte_quota},
                )
            return _IsolatedResult(payload=payload, output_bytes=output_bytes)

        parent_conn, child_conn = self._context.Pipe(duplex=False)
        process = self._context.Process(
            target=_isolated_worker,
            args=(child_conn, fn, request, effective_quota),
        )
        process.daemon = True
        started = time.monotonic()
        try:
            process.start()
        except Exception as exc:
            parent_conn.close()
            child_conn.close()
            raise HostRunnerError(
                f"Could not start isolated runtime process: {exc}",
                reason_code="ERR_ISOLATION_START",
            ) from exc
        finally:
            try:
                child_conn.close()
            except Exception:
                pass

        try:
            deadline = started + (effective_timeout_ms / 1000.0)
            remaining = max(0.0, deadline - time.monotonic())
            while process.is_alive() and remaining > 0:
                if cancellation_token is not None and cancellation_token.is_cancelled:
                    process.terminate()
                    process.join(1.0)
                    if process.is_alive():
                        try:
                            process.kill()
                            process.join(1.0)
                        except AttributeError:
                            pass
                    cancellation_token.raise_if_cancelled()
                process.join(min(0.05, remaining))
                remaining = max(0.0, deadline - time.monotonic())

            if process.is_alive():
                try:
                    process.terminate()
                    process.join(1.0)
                finally:
                    if process.is_alive():
                        try:
                            process.kill()
                            process.join(1.0)
                        except AttributeError:
                            pass
                raise WallClockTimeoutError(
                    "external call exceeded strict wall-clock timeout",
                    reason_code="ERR_WALL_CLOCK_TIMEOUT",
                    details={"timeout_ms": effective_timeout_ms},
                )

            if not parent_conn.poll(0):
                raise HostRunnerError(
                    "isolated runtime exited without a response",
                    reason_code="ERR_ISOLATION_NO_RESPONSE",
                )

            raw = parent_conn.recv_bytes()
            if len(raw) > self.byte_quota:
                raise ByteQuotaExceededError(
                    "isolated runtime response envelope exceeded byte quota",
                    reason_code="ERR_BYTE_QUOTA_OUTPUT",
                    details={"bytes": len(raw), "quota": self.byte_quota},
                )
            envelope = json.loads(raw.decode("utf-8"))
            if not envelope.get("ok"):
                kind = envelope.get("kind")
                if kind == "byte_quota":
                    raise ByteQuotaExceededError(
                        envelope.get("message", "external response exceeded byte quota"),
                        reason_code="ERR_BYTE_QUOTA_OUTPUT",
                        details={"quota": self.byte_quota},
                    )
                raise HostRunnerError(
                    f"isolated external call failed: {envelope.get('message', 'unknown error')}",
                    reason_code="ERR_EXTERNAL_CALL",
                    details={
                        "exception_type": envelope.get("exception_type", "UnknownError"),
                    },
                )
            payload = envelope["payload"]
            output_bytes = _utf8_size(payload)
            if output_bytes > self.byte_quota:
                raise ByteQuotaExceededError(
                    "external call payload exceeded byte quota",
                    reason_code="ERR_BYTE_QUOTA_OUTPUT",
                    details={"bytes": output_bytes, "quota": self.byte_quota},
                )
            return _IsolatedResult(payload=payload, output_bytes=output_bytes)
        finally:
            parent_conn.close()
            if process.is_alive():
                process.terminate()
                process.join(0.5)


def _validate_envelope(invocation: Any) -> Mapping[str, Any]:
    """Extract a strict structured envelope from an AgentInvocation or mapping."""

    if isinstance(invocation, Mapping):
        source = invocation
    else:
        required = ("agent_id", "model_id", "assembled_prompt", "system_prompt")
        missing = [item for item in required if not hasattr(invocation, item)]
        if missing:
            raise InvocationValidationError(
                f"Invocation is missing required fields: {missing}",
                reason_code="ERR_INVOCATION_SHAPE",
            )
        source = {
            "agent_id": getattr(invocation, "agent_id"),
            "model_id": getattr(invocation, "model_id"),
            "prompt": getattr(invocation, "assembled_prompt"),
            "system_prompt": getattr(invocation, "system_prompt"),
            "tools": list(getattr(invocation, "tools", ()) or ()),
        }

    aliases = dict(source)
    if "assembled_prompt" in aliases and "prompt" not in aliases:
        aliases["prompt"] = aliases.pop("assembled_prompt")

    required = ("agent_id", "model_id", "prompt", "system_prompt")
    missing = [key for key in required if key not in aliases]
    if missing:
        raise InvocationValidationError(
            f"Invocation is missing required fields: {missing}",
            reason_code="ERR_INVOCATION_SHAPE",
        )

    envelope = {
        "agent_id": aliases["agent_id"],
        "model_id": aliases["model_id"],
        "prompt": aliases["prompt"],
        "system_prompt": aliases["system_prompt"],
        "messages": aliases.get("messages", []),
        "tools": aliases.get("tools", []),
    }
    return sanitize_structured(envelope)


def _parse_provider_result(result: Mapping[str, Any]) -> tuple[str, list[dict[str, Any]], dict[str, Any]]:
    if not isinstance(result, Mapping):
        raise HostRunnerError(
            "provider response must be a structured object",
            reason_code="ERR_PROVIDER_RESPONSE_TYPE",
        )
    sanitized = sanitize_structured(result)
    response_text = sanitized.get("response_text", sanitized.get("text", ""))
    if not isinstance(response_text, str):
        raise HostRunnerError(
            "provider response text must be a string",
            reason_code="ERR_PROVIDER_RESPONSE_TEXT",
        )

    raw_tool_calls = sanitized.get("tool_calls", [])
    if not isinstance(raw_tool_calls, list):
        raise HostRunnerError(
            "provider tool_calls must be a list",
            reason_code="ERR_PROVIDER_TOOL_CALLS_TYPE",
        )

    tool_calls: list[dict[str, Any]] = []
    for item in raw_tool_calls:
        if not isinstance(item, Mapping):
            raise HostRunnerError(
                "each tool call must be an object",
                reason_code="ERR_PROVIDER_TOOL_CALL_TYPE",
            )
        if set(item.keys()) - {"name", "arguments"}:
            raise HostRunnerError(
                "tool call contains unsupported fields",
                reason_code="ERR_PROVIDER_TOOL_CALL_FIELDS",
            )
        name = item.get("name")
        arguments = item.get("arguments", {})
        if not isinstance(name, str) or not name:
            raise HostRunnerError(
                "tool call name must be a non-empty string",
                reason_code="ERR_PROVIDER_TOOL_NAME",
            )
        if not isinstance(arguments, Mapping):
            raise HostRunnerError(
                "tool call arguments must be a structured object",
                reason_code="ERR_PROVIDER_TOOL_ARGS",
            )
        tool_calls.append({"name": name, "arguments": dict(arguments)})

    return response_text, tool_calls, dict(sanitized)


class AgentHostRunner:
    """Execute a compiled AgentInvocation under INV-HOST-001."""

    def __init__(
        self,
        *,
        providers: Sequence[ProviderSpec],
        tools: Sequence[ToolSpec] = (),
        config: HostRunnerConfig = HostRunnerConfig(),
        container: Optional[IsolatedRuntimeContainer] = None,
    ) -> None:
        if not providers:
            raise ValueError("At least one provider is required")
        provider_names = [provider.name for provider in providers]
        if len(set(provider_names)) != len(provider_names):
            raise ValueError("Provider names must be unique")
        tool_names = [tool.name for tool in tools]
        if len(set(tool_names)) != len(tool_names):
            raise ValueError("Tool names must be unique")
        self.providers = tuple(providers)
        self.tools = {tool.name: tool for tool in tools}
        self.config = config
        self.container = container or IsolatedRuntimeContainer(
            wall_clock_timeout_ms=config.wall_clock_timeout_ms,
            byte_quota=config.byte_quota,
        )

    def run(
        self,
        invocation: Any,
        *,
        allowed_tool_names: Optional[Sequence[str]] = None,
        cancellation_token: Optional[Any] = None,
    ) -> HostRunReceipt:
        if cancellation_token is not None and cancellation_token.is_cancelled:
            cancellation_token.raise_if_cancelled()
        envelope = dict(_validate_envelope(invocation))
        agent_id = envelope["agent_id"]
        prompt = envelope["prompt"]
        system_prompt = envelope["system_prompt"]
        if not isinstance(agent_id, str) or not agent_id:
            raise InvocationValidationError(
                "agent_id must be a non-empty string",
                reason_code="ERR_AGENT_ID",
            )
        if not isinstance(envelope["model_id"], str) or not envelope["model_id"]:
            raise InvocationValidationError(
                "model_id must be a non-empty string",
                reason_code="ERR_MODEL_ID",
            )

        requested_tools = envelope.get("tools", [])
        if not isinstance(requested_tools, list):
            raise InvocationValidationError(
                "invocation tools must be a list",
                reason_code="ERR_INVOCATION_TOOLS",
            )
        permitted_names = set(
            requested_tools if allowed_tool_names is None else allowed_tool_names
        )
        for name in requested_tools:
            if not isinstance(name, str):
                raise InvocationValidationError(
                    "tool names must be strings",
                    reason_code="ERR_TOOL_NAME_TYPE",
                )
            spec = self.tools.get(name)
            if spec is None:
                raise ToolPolicyViolationError(
                    f"Tool '{name}' is not declared by the host",
                    reason_code="ERR_TOOL_UNDECLARED",
                    details={"tool": name},
                )
            if spec.side_effect_class not in self.config.allowed_side_effect_classes:
                raise ToolPolicyViolationError(
                    f"Tool '{name}' side-effect class '{spec.side_effect_class.value}' is not permitted",
                    reason_code="ERR_TOOL_SIDE_EFFECT_CLASS",
                    details={
                        "tool": name,
                        "side_effect_class": spec.side_effect_class.value,
                    },
                )
            if name not in permitted_names:
                raise ToolPolicyViolationError(
                    f"Tool '{name}' is outside the invocation tool policy",
                    reason_code="ERR_TOOL_POLICY",
                )

        model_messages: list[dict[str, Any]] = list(envelope.get("messages", []))
        model_messages.append({"role": "user", "content": prompt})
        total_input_bytes = _utf8_size(
            {
                "agent_id": agent_id,
                "model_id": envelope["model_id"],
                "system_prompt": system_prompt,
                "messages": model_messages,
            }
        )
        if total_input_bytes > self.config.byte_quota:
            raise ByteQuotaExceededError(
                "invocation input exceeded byte quota",
                reason_code="ERR_BYTE_QUOTA_INVOCATION_INPUT",
                details={"bytes": total_input_bytes, "quota": self.config.byte_quota},
            )

        total_prompt_text = f"{system_prompt}\n{prompt}"
        prompt_tokens = deterministic_token_count(total_prompt_text)
        completion_tokens = 0
        turns = 0
        tool_call_count = 0
        failover_count = 0
        final_response = ""
        provider_name = ""
        output_bytes = 0
        used_side_effects: set[str] = set()
        started_at = time.monotonic()
        deadline = started_at + (self.config.wall_clock_timeout_ms / 1000.0)
        bytes_consumed = total_input_bytes

        for turn_index in range(self.config.max_turns):
            turns = turn_index + 1
            request = {
                "agent_id": agent_id,
                "model_id": envelope["model_id"],
                "system_prompt": system_prompt,
                "messages": model_messages,
                "turn": turns,
            }

            if cancellation_token is not None:
                cancellation_token.raise_if_cancelled()
            result, selected_provider, provider_failovers, provider_bytes = self._invoke_with_failover(
                request,
                deadline=deadline,
                remaining_bytes=self.config.byte_quota - bytes_consumed,
                cancellation_token=cancellation_token,
            )
            bytes_consumed += provider_bytes
            provider_name = selected_provider
            failover_count += provider_failovers

            response_text, tool_calls, raw_provider_result = _parse_provider_result(result)
            output_bytes = _utf8_size(raw_provider_result)
            if output_bytes > self.config.byte_quota:
                raise ByteQuotaExceededError(
                    "provider response exceeded byte quota",
                    reason_code="ERR_BYTE_QUOTA_PROVIDER_RESPONSE",
                    details={"bytes": output_bytes, "quota": self.config.byte_quota},
                )

            completion_tokens += deterministic_token_count(response_text)
            final_response = response_text

            if not tool_calls:
                break

            if turns >= self.config.max_turns:
                raise TurnLimitExceededError(
                    "agent tool loop exceeded the hard five-turn limit",
                    reason_code="ERR_MAX_TURNS",
                    details={"max_turns": self.config.max_turns},
                )

            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                spec = self.tools.get(tool_name)
                if spec is None:
                    raise ToolPolicyViolationError(
                        f"Tool '{tool_name}' is not declared by the host",
                        reason_code="ERR_TOOL_UNDECLARED",
                        details={"tool": tool_name},
                    )
                if tool_name not in permitted_names:
                    raise ToolPolicyViolationError(
                        f"Tool '{tool_name}' is outside the invocation tool policy",
                        reason_code="ERR_TOOL_POLICY",
                        details={"tool": tool_name},
                    )
                if not isinstance(spec.side_effect_class, SideEffectClass):
                    raise ToolPolicyViolationError(
                        f"Tool '{tool_name}' has no valid SideEffectClass",
                        reason_code="ERR_TOOL_SIDE_EFFECT_CLASS_MISSING",
                    )
                if spec.side_effect_class not in self.config.allowed_side_effect_classes:
                    raise ToolPolicyViolationError(
                        f"Tool '{tool_name}' side-effect class '{spec.side_effect_class.value}' is not permitted",
                        reason_code="ERR_TOOL_SIDE_EFFECT_CLASS",
                    )

                args = sanitize_structured(tool_call["arguments"])
                args_bytes = _utf8_size(args)
                if spec.max_input_bytes is not None and args_bytes > spec.max_input_bytes:
                    raise ByteQuotaExceededError(
                        f"Tool '{tool_name}' arguments exceed tool byte quota",
                        reason_code="ERR_BYTE_QUOTA_TOOL_INPUT",
                        details={"bytes": args_bytes, "quota": spec.max_input_bytes},
                    )
                if args_bytes > self.config.byte_quota:
                    raise ByteQuotaExceededError(
                        f"Tool '{tool_name}' arguments exceed host byte quota",
                        reason_code="ERR_BYTE_QUOTA_TOOL_INPUT",
                        details={"bytes": args_bytes, "quota": self.config.byte_quota},
                    )

                remaining_time_ms = int(max(0.0, (deadline - time.monotonic()) * 1000.0))
                remaining_bytes = self.config.byte_quota - bytes_consumed
                tool_result = self.container.call(
                    spec.handler,
                    {
                        "arguments": args,
                        "tool_name": tool_name,
                    },
                    timeout_ms=remaining_time_ms,
                    byte_quota=remaining_bytes,
                    cancellation_token=cancellation_token,
                )
                if tool_result.output_bytes > remaining_bytes:
                    raise ByteQuotaExceededError(
                        f"Tool '{tool_name}' result exceeds host byte quota",
                        reason_code="ERR_BYTE_QUOTA_TOOL_OUTPUT",
                    )
                bytes_consumed += tool_result.output_bytes
                tool_call_count += 1
                used_side_effects.add(spec.side_effect_class.value)
                model_messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": sanitize_structured(tool_result.payload),
                    }
                )

        else:
            raise TurnLimitExceededError(
                "agent invocation did not terminate within the hard turn limit",
                reason_code="ERR_MAX_TURNS",
                details={"max_turns": self.config.max_turns},
            )

        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        receipt_material = {
            "agent_id": agent_id,
            "provider_name": provider_name,
            "turns": turns,
            "final_response": final_response,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "input_bytes": total_input_bytes,
            "output_bytes": output_bytes,
            "failover_count": failover_count,
            "tool_calls": tool_call_count,
            "side_effect_classes": sorted(used_side_effects),
            "execution_isolated": True,
            "max_turns": self.config.max_turns,
            "byte_quota": self.config.byte_quota,
            "wall_clock_timeout_ms": self.config.wall_clock_timeout_ms,
        }
        receipt_id = hashlib.sha256(
            json.dumps(
                receipt_material,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

        return HostRunReceipt(
            receipt_id=receipt_id,
            agent_id=agent_id,
            provider_name=provider_name,
            turns=turns,
            final_response=final_response,
            token_usage=usage,
            input_bytes=total_input_bytes,
            output_bytes=output_bytes,
            timed_out=False,
            failover_count=failover_count,
            tool_calls=tool_call_count,
            side_effect_classes=tuple(sorted(used_side_effects)),
            execution_isolated=True,
            max_turns=self.config.max_turns,
            byte_quota=self.config.byte_quota,
            wall_clock_timeout_ms=self.config.wall_clock_timeout_ms,
        )

    def _invoke_with_failover(
        self,
        request: Mapping[str, Any],
        *,
        deadline: float,
        remaining_bytes: int,
        cancellation_token: Optional[Any] = None,
    ) -> tuple[Mapping[str, Any], str, int, int]:
        failures: list[str] = []
        for index, provider in enumerate(self.providers):
            if cancellation_token is not None:
                cancellation_token.raise_if_cancelled()
            remaining_time_ms = int(max(0.0, (deadline - time.monotonic()) * 1000.0))
            if remaining_time_ms <= 0:
                raise WallClockTimeoutError(
                    "host run exceeded its strict wall-clock timeout",
                    reason_code="ERR_WALL_CLOCK_TIMEOUT",
                    details={"timeout_ms": self.config.wall_clock_timeout_ms},
                )
            if remaining_bytes <= 0:
                raise ByteQuotaExceededError(
                    "host run exhausted its strict byte quota",
                    reason_code="ERR_BYTE_QUOTA_OUTPUT",
                    details={"quota": self.config.byte_quota},
                )
            try:
                result = self.container.call(
                    provider.invoke,
                    request,
                    timeout_ms=remaining_time_ms,
                    byte_quota=remaining_bytes,
                    cancellation_token=cancellation_token,
                )
                if not isinstance(result.payload, Mapping):
                    raise HostRunnerError(
                        f"Provider '{provider.name}' returned a non-object response",
                        reason_code="ERR_PROVIDER_RESPONSE_TYPE",
                    )
                return dict(result.payload), provider.name, index, result.output_bytes
            except ExecutionCancelledError:
                raise
            except ByteQuotaExceededError as exc:
                if exc.reason_code == "ERR_BYTE_QUOTA_OUTPUT":
                    failures.append(f"{provider.name}: {exc.reason_code}")
                else:
                    raise
            except InputSanitizationError:
                # Sanitization is a host invariant failure, not provider
                # availability failure, so it must never be hidden by failover.
                raise
            except WallClockTimeoutError as exc:
                # A timed-out provider is a failed tier; move to the next provider.
                failures.append(f"{provider.name}: {exc.reason_code}")
            except (HostRunnerError, OSError, RuntimeError) as exc:
                failures.append(f"{provider.name}: {type(exc).__name__}")

        raise ProviderFailoverError(
            "All configured providers failed during deterministic failover",
            reason_code="ERR_PROVIDER_EXHAUSTED",
            details={"providers": [provider.name for provider in self.providers], "failures": failures},
        )


__all__ = [
    "AgentHostRunner",
    "ByteQuotaExceededError",
    "DEFAULT_BYTE_QUOTA",
    "DEFAULT_MAX_TURNS",
    "DEFAULT_WALL_CLOCK_TIMEOUT_MS",
    "HostRunReceipt",
    "HostRunnerConfig",
    "HostRunnerError",
    "InputSanitizationError",
    "InvocationValidationError",
    "IsolatedRuntimeContainer",
    "ProviderFailoverError",
    "ProviderSpec",
    "SideEffectClass",
    "ToolPolicyViolationError",
    "ToolSpec",
    "TokenUsage",
    "TurnLimitExceededError",
    "WallClockTimeoutError",
    "deterministic_token_count",
    "sanitize_structured",
]
