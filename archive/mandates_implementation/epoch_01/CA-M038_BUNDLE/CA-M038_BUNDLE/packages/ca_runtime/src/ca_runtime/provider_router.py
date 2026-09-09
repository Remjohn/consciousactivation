"""Resilient Multi-Provider Routing for the CAE Reasoning Engine.

Mandate:  CA-M038  (Wave 05, Spine Q05 / Canon Q38)
Invariant: INV-ROUT-001

Implements 3-tier provider routing (Groq → OpenRouter → OpenAI) with
exponential backoff and automatic failover so that a single-provider
failure does not abort an agent run.

Key design principles
---------------------
- **Fail-closed**: when all tiers are exhausted the call raises
  ``ProviderExhaustedError``; it never silently returns an empty result.
- **No artificial token cap**: callers control ``max_tokens``; this
  module does not impose a 500-token (or any other) hard ceiling.
- **Minimal surface**: the router wraps any callable that accepts an
  ``InferenceRequest`` and returns an ``InferenceResponse``.  Actual
  HTTP clients are injected by the caller so the router remains
  unit-testable without network access.
- **No schema self-repair**: output-contract validation is the
  responsibility of ``AgentInvocationRuntime`` (Q39 scope).

State transition (per Canon Q38)
---------------------------------
source  : single provider + hard 500-token cap
op      : remove cap; route Groq → OpenRouter → OpenAI with backoff/failover
target  : resilient 3-tier routing; single-provider failure does not abort the run
error   : all tiers exhausted → ``ProviderExhaustedError`` (fail-closed)
recovery: retry under backoff or Operator intervention
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

logger = logging.getLogger("ca_runtime.provider_router")


# ---------------------------------------------------------------------------
# Public constants — canonical provider order (Canon Q38 / INV-ROUT-001)
# ---------------------------------------------------------------------------

CANONICAL_PROVIDER_ORDER: Tuple[str, ...] = ("groq", "openrouter", "openai")

#: Default backoff base in seconds.  Each attempt waits base * 2^attempt seconds.
DEFAULT_BACKOFF_BASE_SECONDS: float = 1.0

#: Maximum wait between retries (seconds).
DEFAULT_BACKOFF_MAX_SECONDS: float = 30.0

#: Number of attempts per provider tier before moving to the next.
DEFAULT_ATTEMPTS_PER_TIER: int = 2


# ---------------------------------------------------------------------------
# Typed request / response contracts
# ---------------------------------------------------------------------------

@dataclass
class InferenceRequest:
    """Provider-agnostic inference request.

    ``max_tokens`` is caller-controlled; the router imposes **no** hard cap.
    """
    prompt: str
    system_prompt: str
    temperature: float
    max_tokens: int                   # caller sets this — no hard cap here
    model_id: str                     # logical model name (may be overridden per-tier)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceResponse:
    """Provider-agnostic inference response."""
    response_text: str
    parsed_json: Optional[Dict[str, Any]]
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_micros: int
    provider_class: str
    provider_name: str
    tier_index: int                   # 0 = primary, 1 = first fallback, 2 = second fallback


# ---------------------------------------------------------------------------
# Error taxonomy
# ---------------------------------------------------------------------------

class ProviderRoutingError(RuntimeError):
    """Base error for provider routing failures."""

    def __init__(self, message: str, *, reason_code: str = "PROVIDER_ROUTING_ERROR"):
        super().__init__(message)
        self.reason_code = reason_code


class ProviderTierFailure(ProviderRoutingError):
    """A single provider tier failed (may still be retried or failed-over)."""

    def __init__(self, provider: str, attempt: int, cause: Exception):
        super().__init__(
            f"Provider '{provider}' failed on attempt {attempt}: {cause}",
            reason_code="PROVIDER_TIER_FAILURE",
        )
        self.provider = provider
        self.attempt = attempt
        self.cause = cause


class ProviderExhaustedError(ProviderRoutingError):
    """All configured provider tiers were exhausted without a successful response.

    This is the canonical fail-closed signal — callers must not silently
    swallow this error.
    """

    def __init__(self, attempted: Sequence[str], failure_log: Sequence[str]):
        attempted_str = " → ".join(attempted)
        super().__init__(
            f"All provider tiers exhausted ({attempted_str}). "
            f"The reasoning engine cannot complete this request. "
            f"Failures: {list(failure_log)}",
            reason_code="PROVIDER_EXHAUSTED",
        )
        self.attempted_providers = list(attempted)
        self.failure_log = list(failure_log)


class ProviderConfigurationError(ProviderRoutingError):
    """Router is misconfigured (e.g. empty provider list)."""

    def __init__(self, detail: str):
        super().__init__(
            f"ProviderRouter misconfiguration: {detail}",
            reason_code="PROVIDER_CONFIGURATION_ERROR",
        )


# ---------------------------------------------------------------------------
# Backoff policy
# ---------------------------------------------------------------------------

@dataclass
class BackoffPolicy:
    """Exponential backoff configuration.

    wait(attempt) = min(base * 2^attempt, max_seconds)
    """
    base_seconds: float = DEFAULT_BACKOFF_BASE_SECONDS
    max_seconds: float = DEFAULT_BACKOFF_MAX_SECONDS
    attempts_per_tier: int = DEFAULT_ATTEMPTS_PER_TIER

    def wait_seconds(self, attempt: int) -> float:
        """Return the wait duration for the given zero-based attempt index."""
        raw = self.base_seconds * (2 ** attempt)
        return min(raw, self.max_seconds)


# ---------------------------------------------------------------------------
# Provider descriptor
# ---------------------------------------------------------------------------

@dataclass
class ProviderDescriptor:
    """Describes one provider tier in the routing chain.

    ``client_fn`` is the callable that performs the actual inference.
    It receives an ``InferenceRequest`` and must return an
    ``InferenceResponse`` or raise an exception on failure.

    Keeping the client as an injected callable allows the router to be
    tested without live network access (the test simply injects a stub).
    """
    name: str
    client_fn: Callable[[InferenceRequest], InferenceResponse]
    model_id_override: Optional[str] = None    # if set, overrides request.model_id for this tier


# ---------------------------------------------------------------------------
# Core router
# ---------------------------------------------------------------------------

class ProviderRouter:
    """3-tier resilient provider router with exponential backoff.

    Usage
    -----
    ::

        router = ProviderRouter(
            providers=[
                ProviderDescriptor("groq", groq_client_fn),
                ProviderDescriptor("openrouter", openrouter_client_fn),
                ProviderDescriptor("openai", openai_client_fn),
            ],
            backoff_policy=BackoffPolicy(),
        )
        response = router.route(request)   # raises ProviderExhaustedError if all fail

    Canon Q38 / INV-ROUT-001
    --------------------------
    - Provider order: Groq → OpenRouter → OpenAI (or the project-equivalent
      order passed at construction time).
    - On any exception from a tier, the router waits (exponential backoff)
      then retries up to ``backoff_policy.attempts_per_tier`` times before
      moving to the next tier.
    - When all tiers are exhausted: raises ``ProviderExhaustedError`` (fail-closed).
    - No artificial token cap is imposed.
    """

    def __init__(
        self,
        providers: Sequence[ProviderDescriptor],
        backoff_policy: Optional[BackoffPolicy] = None,
        *,
        _sleep_fn: Callable[[float], None] = time.sleep,   # injectable for tests
    ) -> None:
        if not providers:
            raise ProviderConfigurationError("At least one provider tier must be configured.")
        self._providers: List[ProviderDescriptor] = list(providers)
        self._backoff: BackoffPolicy = backoff_policy or BackoffPolicy()
        self._sleep = _sleep_fn

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def route(self, request: InferenceRequest) -> InferenceResponse:
        """Route ``request`` through the provider chain.

        Attempts each provider up to ``backoff_policy.attempts_per_tier``
        times with exponential backoff between attempts.  On tier
        exhaustion, moves to the next tier.  If all tiers fail, raises
        ``ProviderExhaustedError``.

        This method never imposes a max_tokens cap — the value on
        ``request.max_tokens`` is passed as-is to whichever provider
        ultimately handles the request.
        """
        attempted_providers: List[str] = []
        failure_log: List[str] = []

        for tier_index, provider in enumerate(self._providers):
            provider_name = provider.name
            attempted_providers.append(provider_name)

            # Build the request for this tier (may override model_id)
            tier_request = self._build_tier_request(request, provider)

            for attempt in range(self._backoff.attempts_per_tier):
                try:
                    logger.debug(
                        "CA-M038 routing attempt tier=%d provider=%s attempt=%d max_tokens=%d",
                        tier_index, provider_name, attempt, tier_request.max_tokens,
                    )
                    start_us = _monotonic_us()
                    response = provider.client_fn(tier_request)
                    elapsed_us = _monotonic_us() - start_us

                    # Attach routing metadata to the response
                    response.provider_name = provider_name
                    response.tier_index = tier_index
                    if response.latency_micros == 0:
                        response.latency_micros = elapsed_us

                    logger.info(
                        "CA-M038 success tier=%d provider=%s attempt=%d tokens=%d",
                        tier_index, provider_name, attempt, response.total_tokens,
                    )
                    return response

                except Exception as exc:  # noqa: BLE001
                    failure = ProviderTierFailure(provider_name, attempt, exc)
                    failure_log.append(str(failure))
                    logger.warning(
                        "CA-M038 tier=%d provider=%s attempt=%d failed: %s",
                        tier_index, provider_name, attempt, exc,
                    )

                    # Backoff before next attempt (but not after the last attempt
                    # of the last tier — we raise immediately after the loop)
                    is_last_attempt = (attempt == self._backoff.attempts_per_tier - 1)
                    is_last_tier = (tier_index == len(self._providers) - 1)
                    if not (is_last_attempt and is_last_tier):
                        wait = self._backoff.wait_seconds(attempt)
                        logger.debug(
                            "CA-M038 backing off %.2fs before next attempt (tier=%d attempt=%d)",
                            wait, tier_index, attempt,
                        )
                        self._sleep(wait)

        # All tiers exhausted — fail closed
        raise ProviderExhaustedError(attempted_providers, failure_log)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_tier_request(
        self,
        request: InferenceRequest,
        provider: ProviderDescriptor,
    ) -> InferenceRequest:
        """Return a (possibly model-overridden) copy of ``request`` for ``provider``."""
        if provider.model_id_override:
            return InferenceRequest(
                prompt=request.prompt,
                system_prompt=request.system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                model_id=provider.model_id_override,
                extra=dict(request.extra),
            )
        return request

    @property
    def provider_names(self) -> Tuple[str, ...]:
        """Ordered names of the configured provider tiers."""
        return tuple(p.name for p in self._providers)


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def build_canonical_provider_router(
    groq_client_fn: Callable[[InferenceRequest], InferenceResponse],
    openrouter_client_fn: Callable[[InferenceRequest], InferenceResponse],
    openai_client_fn: Callable[[InferenceRequest], InferenceResponse],
    *,
    groq_model_override: Optional[str] = None,
    openrouter_model_override: Optional[str] = None,
    openai_model_override: Optional[str] = None,
    backoff_policy: Optional[BackoffPolicy] = None,
    _sleep_fn: Callable[[float], None] = time.sleep,
) -> ProviderRouter:
    """Build the canonical Groq → OpenRouter → OpenAI router (INV-ROUT-001).

    Provider functions are injected so the router remains testable without
    live credentials.  Pass ``_sleep_fn=lambda _: None`` in tests to
    eliminate backoff waits.
    """
    providers = [
        ProviderDescriptor("groq", groq_client_fn, model_id_override=groq_model_override),
        ProviderDescriptor("openrouter", openrouter_client_fn, model_id_override=openrouter_model_override),
        ProviderDescriptor("openai", openai_client_fn, model_id_override=openai_model_override),
    ]
    return ProviderRouter(providers=providers, backoff_policy=backoff_policy, _sleep_fn=_sleep_fn)


# ---------------------------------------------------------------------------
# Internal utilities
# ---------------------------------------------------------------------------

def _monotonic_us() -> int:
    """Return current monotonic time in microseconds."""
    return int(time.monotonic() * 1_000_000)
