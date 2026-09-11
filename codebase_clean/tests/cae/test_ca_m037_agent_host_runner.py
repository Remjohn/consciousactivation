"""CA-M037 executable evidence for Agent Invocation Host Runner."""

from __future__ import annotations

import time
from typing import Any, Mapping

import pytest

from ca_runtime.agent_host_runner import (
    AgentHostRunner,
    ByteQuotaExceededError,
    HostRunnerConfig,
    InputSanitizationError,
    IsolatedRuntimeContainer,
    ProviderFailoverError,
    ProviderSpec,
    SideEffectClass,
    ToolPolicyViolationError,
    ToolSpec,
    TurnLimitExceededError,
    WallClockTimeoutError,
    deterministic_token_count,
)


def provider_success(request: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"response_text": "done"}


def provider_fail(request: Mapping[str, Any]) -> Mapping[str, Any]:
    raise RuntimeError("provider unavailable")


def provider_fallback(request: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"response_text": "fallback"}


def provider_tool_once(request: Mapping[str, Any]) -> Mapping[str, Any]:
    messages = request["messages"]
    tool_results = [m for m in messages if m.get("role") == "tool"]
    if not tool_results:
        return {
            "response_text": "",
            "tool_calls": [{"name": "read_tool", "arguments": {"query": "status"}}],
        }
    return {"response_text": "tool complete"}


def provider_always_tool(request: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "response_text": "",
        "tool_calls": [{"name": "read_tool", "arguments": {"query": "again"}}],
    }


def tool_success(argument: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"ok": True, "args": argument["arguments"]}


def tool_network(argument: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"network": True}


def provider_large_response(request: Mapping[str, Any]) -> Mapping[str, Any]:
    return {"response_text": "x" * 5_000}


def provider_slow(request: Mapping[str, Any]) -> Mapping[str, Any]:
    time.sleep(0.20)
    return {"response_text": "too late"}


class TestPositiveLiveHostRunner:
    """EXECUTABLE positive path at the authoritative host boundary."""

    def test_real_provider_call_completes_inside_isolated_runtime(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_success)],
            config=HostRunnerConfig(
                max_turns=5,
                wall_clock_timeout_ms=1_000,
                byte_quota=16_384,
            ),
        )

        receipt = runner.run(
            {
                "agent_id": "agent-1",
                "model_id": "model-a",
                "prompt": "hello",
                "system_prompt": "reason",
                "tools": [],
            }
        )

        assert receipt.final_response == "done"
        assert receipt.provider_name == "primary"
        assert receipt.execution_isolated is True
        assert receipt.turns == 1
        assert receipt.token_usage.total_tokens == (
            receipt.token_usage.prompt_tokens + receipt.token_usage.completion_tokens
        )

    def test_deterministic_token_accounting_is_provider_independent(self):
        left = deterministic_token_count("hello world")
        right = deterministic_token_count("hello world")
        assert left == right
        assert left == (len("hello world".encode("utf-8")) + 3) // 4


class TestProviderFailover:
    """Positive and negative provider failover evidence."""

    def test_primary_failure_fails_over_to_next_provider(self):
        calls: list[str] = []

        def primary(request: Mapping[str, Any]) -> Mapping[str, Any]:
            calls.append("primary")
            raise RuntimeError("primary down")

        def fallback(request: Mapping[str, Any]) -> Mapping[str, Any]:
            calls.append("fallback")
            return {"response_text": "recovered"}

        runner = AgentHostRunner(
            providers=[
                ProviderSpec("primary", primary),
                ProviderSpec("fallback", fallback),
            ],
            config=HostRunnerConfig(wall_clock_timeout_ms=1_000, byte_quota=16_384),
        )

        receipt = runner.run(
            {
                "agent_id": "agent-1",
                "model_id": "model-a",
                "prompt": "hello",
                "system_prompt": "reason",
                "tools": [],
            }
        )

        assert calls == ["primary", "fallback"]
        assert receipt.provider_name == "fallback"
        assert receipt.failover_count == 1

    def test_all_provider_failures_fail_closed(self):
        runner = AgentHostRunner(
            providers=[
                ProviderSpec("primary", provider_fail),
                ProviderSpec("fallback", provider_fail),
            ],
            config=HostRunnerConfig(wall_clock_timeout_ms=1_000, byte_quota=16_384),
        )

        with pytest.raises(ProviderFailoverError) as exc_info:
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "hello",
                    "system_prompt": "reason",
                    "tools": [],
                }
            )
        assert exc_info.value.reason_code == "ERR_PROVIDER_EXHAUSTED"


class TestStrictRuntimeLimits:
    def test_wall_clock_timeout_terminates_slow_external_call(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("slow", provider_slow)],
            config=HostRunnerConfig(
                wall_clock_timeout_ms=25,
                byte_quota=16_384,
            ),
        )

        with pytest.raises(ProviderFailoverError) as exc_info:
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "hello",
                    "system_prompt": "reason",
                    "tools": [],
                }
            )

        assert "ERR_PROVIDER_EXHAUSTED" == exc_info.value.reason_code

    def test_isolated_container_exposes_direct_timeout_contract(self):
        container = IsolatedRuntimeContainer(
            wall_clock_timeout_ms=10,
            byte_quota=16_384,
        )

        with pytest.raises(WallClockTimeoutError):
            container.call(provider_slow, {"request": "x"})

    def test_provider_output_byte_quota_fails_closed(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("large", provider_large_response)],
            config=HostRunnerConfig(
                wall_clock_timeout_ms=1_000,
                byte_quota=128,
            ),
        )

        with pytest.raises(ProviderFailoverError):
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "hello",
                    "system_prompt": "reason",
                    "tools": [],
                }
            )

    def test_large_input_is_rejected_before_external_execution(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_success)],
            config=HostRunnerConfig(byte_quota=64),
        )

        with pytest.raises(ByteQuotaExceededError) as exc_info:
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "x" * 10_000,
                    "system_prompt": "reason",
                    "tools": [],
                }
            )
        assert exc_info.value.reason_code == "ERR_BYTE_QUOTA_INVOCATION_INPUT"


class TestStructuredInputSanitization:
    def test_nul_is_rejected(self):
        with pytest.raises(InputSanitizationError):
            from ca_runtime.agent_host_runner import sanitize_structured
            sanitize_structured("bad\x00value")

    def test_non_string_object_keys_are_rejected(self):
        with pytest.raises(InputSanitizationError):
            from ca_runtime.agent_host_runner import sanitize_structured
            sanitize_structured({1: "bad"})

    def test_unicode_normalization_is_deterministic(self):
        from ca_runtime.agent_host_runner import sanitize_structured
        assert sanitize_structured("e\u0301") == "é"


class TestToolPolicyAndTurnBound:
    def test_allowed_read_only_tool_executes_and_returns_to_model(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_tool_once)],
            tools=[
                ToolSpec(
                    "read_tool",
                    SideEffectClass.READ_ONLY,
                    tool_success,
                )
            ],
            config=HostRunnerConfig(
                wall_clock_timeout_ms=1_000,
                byte_quota=16_384,
                allowed_side_effect_classes=frozenset({SideEffectClass.READ_ONLY}),
            ),
        )

        receipt = runner.run(
            {
                "agent_id": "agent-1",
                "model_id": "model-a",
                "prompt": "use the tool",
                "system_prompt": "reason",
                "tools": ["read_tool"],
            }
        )

        assert receipt.final_response == "tool complete"
        assert receipt.tool_calls == 1
        assert receipt.side_effect_classes == (SideEffectClass.READ_ONLY.value,)

    def test_disallowed_side_effect_class_fails_closed_before_tool_execution(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_tool_once)],
            tools=[
                ToolSpec(
                    "read_tool",
                    SideEffectClass.NETWORK,
                    tool_network,
                )
            ],
            config=HostRunnerConfig(
                wall_clock_timeout_ms=1_000,
                byte_quota=16_384,
                allowed_side_effect_classes=frozenset({SideEffectClass.READ_ONLY}),
            ),
        )

        with pytest.raises(ToolPolicyViolationError):
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "use the tool",
                    "system_prompt": "reason",
                    "tools": ["read_tool"],
                }
            )

    def test_tool_loop_cannot_exceed_five_turns(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_always_tool)],
            tools=[
                ToolSpec(
                    "read_tool",
                    SideEffectClass.READ_ONLY,
                    tool_success,
                )
            ],
            config=HostRunnerConfig(
                max_turns=5,
                wall_clock_timeout_ms=1_000,
                byte_quota=16_384,
                allowed_side_effect_classes=frozenset({SideEffectClass.READ_ONLY}),
            ),
        )

        with pytest.raises(TurnLimitExceededError) as exc_info:
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "loop forever",
                    "system_prompt": "reason",
                    "tools": ["read_tool"],
                }
            )
        assert exc_info.value.reason_code == "ERR_MAX_TURNS"

    def test_undeclared_tool_fails_closed(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_success)],
            tools=[],
        )

        with pytest.raises(ToolPolicyViolationError):
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "hello",
                    "system_prompt": "reason",
                    "tools": ["not_declared"],
                }
            )


class TestFalseProofCountercases:
    """Guards against tests that merely assert names/configuration."""

    def test_provider_name_in_configuration_is_not_success_without_execution(self):
        runner = AgentHostRunner(
            providers=[ProviderSpec("primary", provider_fail)],
            config=HostRunnerConfig(wall_clock_timeout_ms=1_000),
        )

        with pytest.raises(ProviderFailoverError):
            runner.run(
                {
                    "agent_id": "agent-1",
                    "model_id": "model-a",
                    "prompt": "hello",
                    "system_prompt": "reason",
                    "tools": [],
                }
            )
