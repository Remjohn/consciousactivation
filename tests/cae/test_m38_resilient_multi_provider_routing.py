"""CA-M038 Test Suite — Resilient Multi-Provider Routing.

Mandate:  CA-M038  (Wave 05, Canon Q38 / INV-ROUT-001)
Evidence: EXECUTABLE positive path, negative/fail-closed path, regression,
          backoff timing, canonical provider order, token-cap removal.

Verification classes required by mandate §9
-------------------------------------------
- EXECUTABLE positive path: call succeeds via primary (Groq) or a subsequent tier
  when the primary is simulated-failed.
- EXECUTABLE negative path: when all tiers fail, the run fails closed with
  ProviderExhaustedError (or ProductionExecutionModeViolationError when routed
  through AgentInvocationRuntime.execute).
- Evidence that the 500-token hard cap no longer aborts legitimate requests:
  request max_tokens > 500 succeeds; the router never truncates it.
- Integration evidence at the real routing boundary (ProviderRouter + runtime).
- False-proof countercase: a test that merely asserts provider *names* are
  present in a list would prove naming, not failover — we test actual routing
  *decisions* by injecting failures.
- Environment fidelity: tests use injected stub callables; no live credentials
  required; simulated failover is provable.

Regression guard (adjacent behaviour)
--------------------------------------
- AgentInvocationRuntime.execute continues to work in TEST_FIXTURE mode without
  a router (existing callers are unaffected).
- InvocationIntegrityError is still raised on tampered invocations.

Run
---
::

    pytest tests/cae/test_m38_resilient_multi_provider_routing.py -v
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from ca_runtime.provider_router import (
    BackoffPolicy,
    InferenceRequest,
    InferenceResponse,
    ProviderConfigurationError,
    ProviderDescriptor,
    ProviderExhaustedError,
    ProviderRouter,
    ProviderTierFailure,
    build_canonical_provider_router,
    CANONICAL_PROVIDER_ORDER,
)


# ---------------------------------------------------------------------------
# Helpers / stubs
# ---------------------------------------------------------------------------

_NO_SLEEP = lambda _: None  # noqa: E731  — eliminate backoff waits in tests


def _ok_response(provider_name: str, tier_index: int = 0, text: str = "OK") -> InferenceResponse:
    """Return a synthetic successful InferenceResponse."""
    return InferenceResponse(
        response_text=text,
        parsed_json=None,
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        latency_micros=10_000,
        provider_class=f"{provider_name.capitalize()}Provider",
        provider_name=provider_name,
        tier_index=tier_index,
    )


def _always_succeed(name: str, *, text: str = "OK") -> callable:
    """Return a client function that always succeeds."""
    def _fn(req: InferenceRequest) -> InferenceResponse:
        return _ok_response(name, text=text)
    return _fn


def _always_fail(name: str, error: Optional[Exception] = None) -> callable:
    """Return a client function that always raises."""
    exc = error or RuntimeError(f"{name} unavailable")

    def _fn(req: InferenceRequest) -> InferenceResponse:
        raise exc
    return _fn


def _fail_then_succeed(name: str, fail_count: int) -> callable:
    """Fail the first ``fail_count`` calls, then succeed."""
    state = {"calls": 0}

    def _fn(req: InferenceRequest) -> InferenceResponse:
        state["calls"] += 1
        if state["calls"] <= fail_count:
            raise RuntimeError(f"{name} transient error #{state['calls']}")
        return _ok_response(name)
    return _fn


def _canonical_providers(*, groq_fn=None, openrouter_fn=None, openai_fn=None):
    """Build the canonical 3-tier provider list with optional overrides."""
    return [
        ProviderDescriptor("groq", groq_fn or _always_succeed("groq")),
        ProviderDescriptor("openrouter", openrouter_fn or _always_succeed("openrouter")),
        ProviderDescriptor("openai", openai_fn or _always_succeed("openai")),
    ]


def _make_request(max_tokens: int = 1024) -> InferenceRequest:
    return InferenceRequest(
        prompt="Reason about this.",
        system_prompt="You are a CAE agent.",
        temperature=0.2,
        max_tokens=max_tokens,
        model_id="gemini-2.5-pro",
    )


# ---------------------------------------------------------------------------
# §1 — Provider order and configuration
# ---------------------------------------------------------------------------

class TestCanonicalProviderOrder:
    """Verify the canonical provider order constant (Canon Q38)."""

    def test_canonical_order_is_groq_openrouter_openai(self):
        assert CANONICAL_PROVIDER_ORDER == ("groq", "openrouter", "openai")

    def test_router_preserves_provider_order(self):
        router = ProviderRouter(
            providers=_canonical_providers(),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        assert router.provider_names == ("groq", "openrouter", "openai")

    def test_router_raises_on_empty_providers(self):
        with pytest.raises(ProviderConfigurationError, match="At least one"):
            ProviderRouter(providers=[], _sleep_fn=_NO_SLEEP)

    def test_build_canonical_factory_helper(self):
        router = build_canonical_provider_router(
            groq_client_fn=_always_succeed("groq"),
            openrouter_client_fn=_always_succeed("openrouter"),
            openai_client_fn=_always_succeed("openai"),
            _sleep_fn=_NO_SLEEP,
        )
        assert router.provider_names == ("groq", "openrouter", "openai")


# ---------------------------------------------------------------------------
# §2 — EXECUTABLE positive path: primary succeeds
# ---------------------------------------------------------------------------

class TestPositivePath:
    """Primary-provider success path (INV-ROUT-001 positive)."""

    def test_primary_provider_succeeds_returns_response(self):
        router = ProviderRouter(
            providers=_canonical_providers(groq_fn=_always_succeed("groq", text="groq-ok")),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())
        assert resp.response_text == "groq-ok"
        assert resp.provider_name == "groq"
        assert resp.tier_index == 0

    def test_primary_success_does_not_invoke_lower_tiers(self):
        calls: List[str] = []

        def _groq(req):
            calls.append("groq")
            return _ok_response("groq")

        def _openrouter(req):
            calls.append("openrouter")
            return _ok_response("openrouter")

        def _openai(req):
            calls.append("openai")
            return _ok_response("openai")

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _groq),
                ProviderDescriptor("openrouter", _openrouter),
                ProviderDescriptor("openai", _openai),
            ],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        router.route(_make_request())
        assert calls == ["groq"], "Only primary should be called on success"

    def test_token_budget_passed_through_unchanged(self):
        """CA-M038 core: max_tokens > 500 must be passed as-is (no cap)."""
        received_max_tokens: List[int] = []

        def _groq(req: InferenceRequest) -> InferenceResponse:
            received_max_tokens.append(req.max_tokens)
            return _ok_response("groq")

        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _groq)],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        router.route(_make_request(max_tokens=4096))
        assert received_max_tokens == [4096], (
            "Router must not cap max_tokens — the 500-token limit has been removed (CA-M038)"
        )

    def test_large_token_budget_8k(self):
        """Prove the 500-token cap is gone: a request for 8192 tokens succeeds."""
        received: List[int] = []

        def _client(req: InferenceRequest) -> InferenceResponse:
            received.append(req.max_tokens)
            resp = _ok_response("groq")
            resp.completion_tokens = 4000  # simulate large response
            resp.total_tokens = 4100
            return resp

        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _client)],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request(max_tokens=8_192))
        assert received[0] == 8_192
        assert resp.total_tokens == 4100


# ---------------------------------------------------------------------------
# §3 — Failover: primary fails, secondary/tertiary succeeds
# ---------------------------------------------------------------------------

class TestFailoverRouting:
    """Simulated primary-provider failure → successful failover."""

    def test_failover_to_openrouter_when_groq_fails(self):
        router = ProviderRouter(
            providers=_canonical_providers(
                groq_fn=_always_fail("groq"),
                openrouter_fn=_always_succeed("openrouter", text="openrouter-ok"),
            ),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())
        assert resp.provider_name == "openrouter"
        assert resp.response_text == "openrouter-ok"
        assert resp.tier_index == 1

    def test_failover_to_openai_when_groq_and_openrouter_fail(self):
        router = ProviderRouter(
            providers=_canonical_providers(
                groq_fn=_always_fail("groq"),
                openrouter_fn=_always_fail("openrouter"),
                openai_fn=_always_succeed("openai", text="openai-ok"),
            ),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())
        assert resp.provider_name == "openai"
        assert resp.response_text == "openai-ok"
        assert resp.tier_index == 2

    def test_failover_preserves_full_request(self):
        """The fallback provider receives the original request unchanged."""
        received: List[InferenceRequest] = []

        def _openrouter(req: InferenceRequest) -> InferenceResponse:
            received.append(req)
            return _ok_response("openrouter")

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _always_fail("groq")),
                ProviderDescriptor("openrouter", _openrouter),
            ],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        req = _make_request(max_tokens=2048)
        router.route(req)
        assert received[0].max_tokens == 2048
        assert received[0].prompt == req.prompt
        assert received[0].temperature == req.temperature

    def test_transient_failure_then_same_tier_succeeds_on_retry(self):
        """Multi-attempt per tier: fails once, then succeeds on retry (still same tier)."""
        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _fail_then_succeed("groq", fail_count=1))],
            backoff_policy=BackoffPolicy(attempts_per_tier=2),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())
        assert resp.provider_name == "groq"
        assert resp.tier_index == 0


# ---------------------------------------------------------------------------
# §4 — EXECUTABLE negative path: all tiers exhausted → fail-closed
# ---------------------------------------------------------------------------

class TestFailClosedExhaustion:
    """All tiers fail → ProviderExhaustedError (INV-ROUT-001 negative)."""

    def test_all_tiers_fail_raises_provider_exhausted_error(self):
        router = ProviderRouter(
            providers=_canonical_providers(
                groq_fn=_always_fail("groq"),
                openrouter_fn=_always_fail("openrouter"),
                openai_fn=_always_fail("openai"),
            ),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        with pytest.raises(ProviderExhaustedError) as exc_info:
            router.route(_make_request())

        err = exc_info.value
        assert err.reason_code == "PROVIDER_EXHAUSTED"
        assert "groq" in err.attempted_providers
        assert "openrouter" in err.attempted_providers
        assert "openai" in err.attempted_providers
        assert len(err.failure_log) >= 3  # at least one failure entry per tier

    def test_exhausted_error_message_contains_all_providers(self):
        router = ProviderRouter(
            providers=_canonical_providers(
                groq_fn=_always_fail("groq"),
                openrouter_fn=_always_fail("openrouter"),
                openai_fn=_always_fail("openai"),
            ),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        with pytest.raises(ProviderExhaustedError) as exc_info:
            router.route(_make_request())

        msg = str(exc_info.value)
        assert "groq" in msg
        assert "openrouter" in msg
        assert "openai" in msg

    def test_single_provider_exhausted_also_fails_closed(self):
        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _always_fail("groq"))],
            backoff_policy=BackoffPolicy(attempts_per_tier=2),
            _sleep_fn=_NO_SLEEP,
        )
        with pytest.raises(ProviderExhaustedError):
            router.route(_make_request())

    def test_exhausted_error_not_swallowed_by_routing_layer(self):
        """Prove: fail-closed means ProviderExhaustedError propagates, never silent empty result."""
        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _always_fail("groq"))],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        result = None
        error_raised = False
        try:
            result = router.route(_make_request())
        except ProviderExhaustedError:
            error_raised = True

        assert error_raised, "ProviderExhaustedError must propagate — never silently return None"
        assert result is None


# ---------------------------------------------------------------------------
# §5 — Backoff behaviour
# ---------------------------------------------------------------------------

class TestBackoffPolicy:
    """Verify exponential backoff between attempts."""

    def test_backoff_wait_grows_exponentially(self):
        bp = BackoffPolicy(base_seconds=1.0, max_seconds=60.0)
        assert bp.wait_seconds(0) == 1.0   # 1 * 2^0
        assert bp.wait_seconds(1) == 2.0   # 1 * 2^1
        assert bp.wait_seconds(2) == 4.0   # 1 * 2^2
        assert bp.wait_seconds(3) == 8.0   # 1 * 2^3

    def test_backoff_is_capped_at_max_seconds(self):
        bp = BackoffPolicy(base_seconds=1.0, max_seconds=5.0)
        assert bp.wait_seconds(10) == 5.0  # should not exceed max

    def test_sleep_is_called_between_attempts(self):
        sleep_calls: List[float] = []

        def _counting_sleep(seconds: float) -> None:
            sleep_calls.append(seconds)

        # 2 attempts per tier, first fails → should sleep once before second attempt
        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _fail_then_succeed("groq", fail_count=1)),
            ],
            backoff_policy=BackoffPolicy(base_seconds=1.0, attempts_per_tier=2),
            _sleep_fn=_counting_sleep,
        )
        router.route(_make_request())
        assert len(sleep_calls) == 1
        assert sleep_calls[0] == 1.0  # base * 2^0

    def test_no_sleep_after_last_exhausted_attempt(self):
        """The router must NOT sleep after the very last failing attempt."""
        sleep_calls: List[float] = []

        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _always_fail("groq"))],
            backoff_policy=BackoffPolicy(base_seconds=1.0, attempts_per_tier=1),
            _sleep_fn=lambda s: sleep_calls.append(s),
        )
        with pytest.raises(ProviderExhaustedError):
            router.route(_make_request())

        # With 1 attempt per tier and 1 tier, the single failure is the last one
        # → no sleep should occur after it
        assert sleep_calls == []

    def test_sleep_between_tier_transitions(self):
        """Sleep occurs during tier transition when primary tier's last attempt fails."""
        sleep_calls: List[float] = []

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _always_fail("groq")),
                ProviderDescriptor("openrouter", _always_succeed("openrouter")),
            ],
            backoff_policy=BackoffPolicy(base_seconds=2.0, attempts_per_tier=1),
            _sleep_fn=lambda s: sleep_calls.append(s),
        )
        router.route(_make_request())
        # groq fails on attempt 0 → sleep(2.0) → openrouter succeeds
        assert sleep_calls == [2.0]


# ---------------------------------------------------------------------------
# §6 — Model override per tier
# ---------------------------------------------------------------------------

class TestModelOverride:
    """Provider-specific model_id_override is applied correctly."""

    def test_model_override_applied_for_fallback_tier(self):
        received_model_ids: List[str] = []

        def _openrouter(req: InferenceRequest) -> InferenceResponse:
            received_model_ids.append(req.model_id)
            return _ok_response("openrouter")

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _always_fail("groq")),
                ProviderDescriptor("openrouter", _openrouter, model_id_override="openai/gpt-4o"),
            ],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        req = _make_request()
        router.route(req)
        assert received_model_ids == ["openai/gpt-4o"]

    def test_no_override_passes_original_model_id(self):
        received_model_ids: List[str] = []

        def _groq(req: InferenceRequest) -> InferenceResponse:
            received_model_ids.append(req.model_id)
            return _ok_response("groq")

        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _groq)],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        req = _make_request()
        req = InferenceRequest(
            prompt=req.prompt,
            system_prompt=req.system_prompt,
            temperature=req.temperature,
            max_tokens=req.max_tokens,
            model_id="my-custom-model",
        )
        router.route(req)
        assert received_model_ids == ["my-custom-model"]


# ---------------------------------------------------------------------------
# §7 — Integration: ProviderRouter + AgentInvocationRuntime
# ---------------------------------------------------------------------------

class TestAgentInvocationRuntimeIntegration:
    """Integration evidence at the real routing boundary."""

    @pytest.fixture
    def _minimal_invocation(self):
        """Build a minimal, verifiable AgentInvocation for use in integration tests."""
        from ca_runtime import (
            AccessMode,
            AgentDefinition,
            AgentInvocationCompiler,
            AgentLifecycleState,
            AgentModelPolicy,
            AgentPromptReference,
            AuthorityLane,
            CapabilityProjection,
            CapabilityScope,
            ContextItem,
            ContextPrecedenceLayer,
            JITContextCompiler,
            SkillMaturity,
            SkillPackageRef,
        )

        agent = AgentDefinition(
            agent_id="TestReasoningAgent",
            version="1.0.0",
            name="Test Reasoning Agent",
            purpose="Unit test agent for CA-M038.",
            authority_lane=AuthorityLane.HUNTER,
            lifecycle_state=AgentLifecycleState.APPROVED,
            model_policy=AgentModelPolicy(
                preferred_model="gemini-2.5-pro",
                temperature=0.2,
                temperature_bps=2000,
                token_budget=4096,
                fallback_models=["gemini-2.5-flash"],
                timeout_seconds=30,
            ),
            prompt_reference=AgentPromptReference(
                instructions_ref="instructions.md",
                system_prompt_template="You are a test agent.",
            ),
        )

        skill = SkillPackageRef(
            skill_id="test_skill",
            version="1.0.0",
            maturity=SkillMaturity.STABLE,
            procedure_ref="skills/test/SKILL.md",
            package_sha256="b" * 64,
            allowed_tools=("tool:read",),
            forbidden_actions=(),
        )

        cap = CapabilityProjection(
            capability_id="cap_read",
            owner_product="cae",
            scope=CapabilityScope.FILESYSTEM,
            mode=AccessMode.READ_ONLY,
            workspace_bound=True,
            approval_required=False,
            sandbox_required=False,
            audit_mode="LOGGED",
            bound_tools=("tool:read",),
        )

        ctx_item = ContextItem.create(
            context_id="ctx_001",
            layer=ContextPrecedenceLayer.AGENT_INSTRUCTIONS,
            source_ref="test",
            content="Test context content.",
            inclusion_reason="test",
        )

        workspace_id = uuid4()
        capsule = JITContextCompiler.assemble(
            workspace_id=workspace_id,
            lane=AuthorityLane.HUNTER,
            actor_id="actor:operator-hunter",
            program_id="program:research_canonicalization",
            harness_id="harness:atomic_hunter",
            agent_id="TestReasoningAgent",
            model_id="gemini-2.5-pro",
            capabilities=[cap],
            skills=[(skill, "Procedure: test procedure")],
        )

        inv = AgentInvocationCompiler.compile(
            agent=agent,
            capsule=capsule,
            workspace_id=workspace_id,
            model_id="gemini-2.5-pro",
            model_provider="groq",
            skills=[skill],
        )
        return inv

    def test_runtime_uses_provider_router_in_production_mode(self, _minimal_invocation):
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        called_providers: List[str] = []

        def _groq_fn(req: InferenceRequest) -> InferenceResponse:
            called_providers.append("groq")
            resp = _ok_response("groq", text=json.dumps({"status": "ok"}))
            return resp

        router = build_canonical_provider_router(
            groq_client_fn=_groq_fn,
            openrouter_client_fn=_always_succeed("openrouter"),
            openai_client_fn=_always_succeed("openai"),
            _sleep_fn=_NO_SLEEP,
        )

        receipt = AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.PRODUCTION,
            provider_router=router,
        )

        assert receipt.raw_response_text == json.dumps({"status": "ok"})
        assert called_providers == ["groq"]
        assert not receipt.is_synthetic

    def test_runtime_fails_closed_when_all_router_tiers_exhausted(self, _minimal_invocation):
        from ca_runtime import AgentInvocationRuntime, ExecutionMode
        from ca_runtime.agent_invocation import ProductionExecutionModeViolationError

        router = build_canonical_provider_router(
            groq_client_fn=_always_fail("groq"),
            openrouter_client_fn=_always_fail("openrouter"),
            openai_client_fn=_always_fail("openai"),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )

        with pytest.raises(ProductionExecutionModeViolationError) as exc_info:
            AgentInvocationRuntime.execute(
                _minimal_invocation,
                mode=ExecutionMode.PRODUCTION,
                provider_router=router,
            )

        assert "exhausted" in str(exc_info.value).lower()

    def test_runtime_failover_to_openrouter_in_production_mode(self, _minimal_invocation):
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        router = build_canonical_provider_router(
            groq_client_fn=_always_fail("groq"),
            openrouter_client_fn=_always_succeed("openrouter", text="openrouter-response"),
            openai_client_fn=_always_fail("openai"),
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )

        receipt = AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.PRODUCTION,
            provider_router=router,
        )

        assert receipt.raw_response_text == "openrouter-response"
        assert not receipt.is_synthetic

    def test_runtime_accepts_large_max_tokens_without_cap(self, _minimal_invocation):
        """CA-M038 core: runtime must NOT impose a 500-token cap."""
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        received_tokens: List[int] = []

        def _groq(req: InferenceRequest) -> InferenceResponse:
            received_tokens.append(req.max_tokens)
            return _ok_response("groq")

        router = build_canonical_provider_router(
            groq_client_fn=_groq,
            openrouter_client_fn=_always_succeed("openrouter"),
            openai_client_fn=_always_succeed("openai"),
            _sleep_fn=_NO_SLEEP,
        )

        AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.PRODUCTION,
            provider_router=router,
        )

        assert received_tokens, "Groq client must have been called"
        assert received_tokens[0] > 500, (
            f"CA-M038: expected max_tokens > 500 but got {received_tokens[0]}. "
            "The 500-token hard cap has been removed."
        )


# ---------------------------------------------------------------------------
# §8 — Regression: existing runtime behaviour is unaffected by CA-M038
# ---------------------------------------------------------------------------

class TestRegressionExistingBehaviour:
    """Ensure CA-M038 does not break existing runtime contracts."""

    @pytest.fixture
    def _minimal_invocation(self):
        """Duplicate minimal fixture for this class (pytest fixtures are class-scoped)."""
        from ca_runtime import (
            AccessMode,
            AgentDefinition,
            AgentInvocationCompiler,
            AgentLifecycleState,
            AgentModelPolicy,
            AgentPromptReference,
            AuthorityLane,
            CapabilityProjection,
            CapabilityScope,
            ContextItem,
            ContextPrecedenceLayer,
            JITContextCompiler,
            SkillMaturity,
            SkillPackageRef,
        )

        agent = AgentDefinition(
            agent_id="RegressionAgent",
            version="1.0.0",
            name="Regression Agent",
            purpose="Regression test agent for CA-M038.",
            authority_lane=AuthorityLane.HUNTER,
            lifecycle_state=AgentLifecycleState.APPROVED,
            model_policy=AgentModelPolicy(
                preferred_model="gemini-2.5-pro",
                temperature=0.2,
                temperature_bps=2000,
                token_budget=2048,
                fallback_models=["gemini-2.5-flash"],
                timeout_seconds=30,
            ),
            prompt_reference=AgentPromptReference(
                instructions_ref="instructions.md",
                system_prompt_template="You are a regression test agent.",
            ),
        )

        skill = SkillPackageRef(
            skill_id="regression_skill",
            version="1.0.0",
            maturity=SkillMaturity.STABLE,
            procedure_ref="skills/regression/SKILL.md",
            package_sha256="c" * 64,
            allowed_tools=("tool:read",),
            forbidden_actions=(),
        )

        cap = CapabilityProjection(
            capability_id="cap_read",
            owner_product="cae",
            scope=CapabilityScope.FILESYSTEM,
            mode=AccessMode.READ_ONLY,
            workspace_bound=True,
            approval_required=False,
            sandbox_required=False,
            audit_mode="LOGGED",
            bound_tools=("tool:read",),
        )

        ctx_item = ContextItem.create(
            context_id="ctx_reg_001",
            layer=ContextPrecedenceLayer.AGENT_INSTRUCTIONS,
            source_ref="regression_test",
            content="Regression context.",
            inclusion_reason="test",
        )

        workspace_id = uuid4()
        capsule = JITContextCompiler.assemble(
            workspace_id=workspace_id,
            lane=AuthorityLane.HUNTER,
            actor_id="actor:operator-hunter",
            program_id="program:research_canonicalization",
            harness_id="harness:atomic_hunter",
            agent_id="RegressionAgent",
            model_id="gemini-2.5-pro",
            capabilities=[cap],
            skills=[(skill, "Procedure: regression procedure")],
        )

        return AgentInvocationCompiler.compile(
            agent=agent,
            capsule=capsule,
            workspace_id=workspace_id,
            model_id="gemini-2.5-pro",
            model_provider="groq",
            skills=[skill],
        )

    def test_test_fixture_mode_without_router_still_works(self, _minimal_invocation):
        """Existing callers not passing provider_router must remain unaffected."""
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        receipt = AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.TEST_FIXTURE,
        )

        assert receipt.is_synthetic
        assert receipt.output_contract_passed

    def test_test_fixture_mode_with_inference_fn_still_works(self, _minimal_invocation):
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        def _inf_fn(inv):
            return {
                "response_text": "regression-check",
                "parsed_json": {"result": "ok"},
                "prompt_tokens": 10,
                "completion_tokens": 5,
                "latency_micros": 1000,
            }

        receipt = AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.TEST_FIXTURE,
            inference_fn=_inf_fn,
        )

        assert receipt.raw_response_text == "regression-check"

    def test_integrity_check_still_raises_on_tampered_invocation(self, _minimal_invocation):
        """Anti-tamper: InvocationIntegrityError must still fire after CA-M038."""
        from ca_runtime import InvocationIntegrityError

        # Directly access the dataclass and produce a tampered version by
        # reconstructing with a wrong sha256
        inv = _minimal_invocation
        import dataclasses
        tampered = dataclasses.replace(inv, invocation_sha256="0" * 64)
        with pytest.raises(InvocationIntegrityError):
            tampered.verify_integrity()

    def test_provider_router_preferred_over_model_reasoning_engine(self, _minimal_invocation):
        """When both provider_router and model_reasoning_engine are supplied, router wins."""
        from ca_runtime import AgentInvocationRuntime, ExecutionMode

        engine_called = []

        class FakeEngine:
            def infer(self, **kwargs):
                engine_called.append(True)
                resp = MagicMock()
                resp.response_text = "engine-response"
                resp.parsed_json = None
                resp.prompt_tokens = 10
                resp.completion_tokens = 5
                resp.total_tokens = 15
                resp.latency_micros = 5000
                resp.provider_class = "FakeEngineProvider"
                return resp

        router_called = []

        def _groq(req):
            router_called.append(True)
            return _ok_response("groq", text="router-response")

        router = build_canonical_provider_router(
            groq_client_fn=_groq,
            openrouter_client_fn=_always_succeed("openrouter"),
            openai_client_fn=_always_succeed("openai"),
            _sleep_fn=_NO_SLEEP,
        )

        receipt = AgentInvocationRuntime.execute(
            _minimal_invocation,
            mode=ExecutionMode.PRODUCTION,
            provider_router=router,
            model_reasoning_engine=FakeEngine(),
        )

        assert receipt.raw_response_text == "router-response", (
            "ProviderRouter must take precedence over model_reasoning_engine (CA-M038)"
        )
        assert router_called, "Router must have been called"
        assert not engine_called, "Legacy engine must NOT be called when router is present"


# ---------------------------------------------------------------------------
# §9 — False-proof countercase guard
# ---------------------------------------------------------------------------

class TestFalseProofGuard:
    """Prove these tests cannot be fooled by provider *names* alone."""

    def test_provider_name_in_list_does_not_prove_failover(self):
        """A router with groq/openrouter/openai in its list does NOT prove failover
        unless those providers are actually called in the right order.
        This test proves that the fixture is sensitive to calling order."""
        call_order: List[str] = []

        def _groq(req):
            call_order.append("groq")
            raise RuntimeError("groq down")

        def _openrouter(req):
            call_order.append("openrouter")
            return _ok_response("openrouter")

        def _openai(req):
            call_order.append("openai")
            return _ok_response("openai")

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", _groq),
                ProviderDescriptor("openrouter", _openrouter),
                ProviderDescriptor("openai", _openai),
            ],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())

        # This proves CALLING ORDER, not just name presence
        assert call_order == ["groq", "openrouter"], (
            "Provider call order must follow Groq → OpenRouter → OpenAI;"
            " openai was not needed because openrouter succeeded"
        )
        assert resp.provider_name == "openrouter"

    def test_naming_groq_as_provider_does_not_prove_it_was_called(self):
        """Merely asserting provider_name == 'groq' on a string would be trivially fakeable.
        We verify by capturing actual call side-effects."""
        actually_called = []

        def _groq(req):
            actually_called.append(True)
            return _ok_response("groq")

        router = ProviderRouter(
            providers=[ProviderDescriptor("groq", _groq)],
            backoff_policy=BackoffPolicy(attempts_per_tier=1),
            _sleep_fn=_NO_SLEEP,
        )
        resp = router.route(_make_request())

        assert actually_called, "The client function must actually be called — name alone proves nothing"
        assert resp.provider_name == "groq"
