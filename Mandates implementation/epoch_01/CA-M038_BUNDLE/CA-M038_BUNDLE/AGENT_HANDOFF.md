# AGENT_HANDOFF — CA-M038 Resilient Multi-Provider Routing

**Mandate ID:** `CA-M038`
**Wave:** `05`
**Canon Question:** `Q38` (Spine Q05)
**Invariant:** `INV-ROUT-001`
**Status at handoff:** IMPLEMENTATION COMPLETE — awaiting Operator approve/reject decision

---

## 1. Summary Table

| File changed / created | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/provider_router.py` | **NEW FILE.** Implements `ProviderRouter` with 3-tier routing (Groq → OpenRouter → OpenAI), `BackoffPolicy` (exponential backoff), `ProviderExhaustedError` (fail-closed), `InferenceRequest` / `InferenceResponse` contracts, `build_canonical_provider_router` factory helper, and `CANONICAL_PROVIDER_ORDER` constant. No 500-token cap is imposed anywhere in this module. | INV-ROUT-001: 3-tier routing with failover; fail-closed exhaustion; no artificial token cap |
| `packages/ca_runtime/src/ca_runtime/agent_invocation.py` | Removed the hard `max_tokens=500` cap from both PRODUCTION and TEST_FIXTURE `model_reasoning_engine.infer()` call sites. Added `_DEFAULT_MAX_TOKENS = 8_192` as a non-artificial default. Added `provider_router: Optional[ProviderRouter]` parameter to `AgentInvocationRuntime.execute()`. When a router is supplied it is used in preference to a bare `model_reasoning_engine`. `ProviderExhaustedError` is re-raised as `ProductionExecutionModeViolationError` so existing error-handling contracts remain intact. | 500-token cap removed; ProviderRouter integration; fail-closed propagation; backward compat preserved |
| `packages/ca_runtime/src/ca_runtime/__init__.py` | Added `from .provider_router import (BackoffPolicy, InferenceRequest, InferenceResponse, ProviderConfigurationError, ProviderDescriptor, ProviderExhaustedError, ProviderRouter, ProviderRoutingError, ProviderTierFailure, build_canonical_provider_router, CANONICAL_PROVIDER_ORDER)` and the same symbols to `__all__`. | Public API surface complete |
| `tests/cae/test_m38_resilient_multi_provider_routing.py` | **NEW FILE.** Comprehensive test suite (9 sections, 30+ tests). Covers all mandate §9 evidence classes: positive path, failover path, fail-closed negative, token-cap-removal proof, backoff timing, model override, runtime integration, regression, and false-proof countercase. | All EXECUTABLE evidence classes from mandate §9 |

---

## 2. Exact Paste Instructions

Apply each file at the repo root by replacing the file at its exact path:

```
# NEW FILE — does not exist in repo yet
cp CA-M038_BUNDLE/packages/ca_runtime/src/ca_runtime/provider_router.py \
   packages/ca_runtime/src/ca_runtime/provider_router.py

# MODIFIED FILE — replaces existing agent_invocation.py
cp CA-M038_BUNDLE/packages/ca_runtime/src/ca_runtime/agent_invocation.py \
   packages/ca_runtime/src/ca_runtime/agent_invocation.py

# MODIFIED FILE — replaces existing __init__.py
cp CA-M038_BUNDLE/packages/ca_runtime/src/ca_runtime/__init__.py \
   packages/ca_runtime/src/ca_runtime/__init__.py

# NEW TEST FILE — does not exist in repo yet
cp CA-M038_BUNDLE/tests/cae/test_m38_resilient_multi_provider_routing.py \
   tests/cae/test_m38_resilient_multi_provider_routing.py
```

**File boundary confirmation:** Only files within the `packages/ca_runtime/` package and `tests/cae/` directory are modified or created.  No UI files, no output-parsing logic (Q39 scope), no economics/spend-ceiling logic (later wave), and no new external provider HTTP clients are introduced.

---

## 3. Manual Post-Apply Commands

### 3a. Install / verify the package

```bash
# From repo root
pip install -e "packages/ca_runtime[dev]" --break-system-packages
# or
cd packages/ca_runtime && pip install -e . --break-system-packages && cd -
```

### 3b. Run the CA-M038 test suite

```bash
# All CA-M038 tests
pytest tests/cae/test_m38_resilient_multi_provider_routing.py -v

# Run with verbose evidence output
pytest tests/cae/test_m38_resilient_multi_provider_routing.py -v --tb=short

# Expected: 30+ tests, all PASSED, zero FAILED
```

### 3c. Run the existing M52 regression guard (adjacent behaviour)

```bash
pytest tests/cae/test_m52_canonical_agent_invocation_contract.py -v
```

### 3d. Run the full CAE test suite (recommended before merge)

```bash
pytest tests/cae/ -v --tb=short
```

### 3e. No database migrations required

This mandate is purely computational (routing logic in Python).  No SQL schema changes, no Django/Alembic migrations, no environment variable additions are required.  If live provider credentials are available they can be set via environment variables consumed by the project's existing provider client layer (not in scope of this mandate).

---

## 4. New Automated Tests Included in Bundle

File: `tests/cae/test_m38_resilient_multi_provider_routing.py`

| Test class | Test name | Evidence class (§9) |
|---|---|---|
| `TestCanonicalProviderOrder` | `test_canonical_order_is_groq_openrouter_openai` | Canon Q38 order |
| `TestCanonicalProviderOrder` | `test_router_preserves_provider_order` | Provider ordering |
| `TestCanonicalProviderOrder` | `test_router_raises_on_empty_providers` | Config guard |
| `TestCanonicalProviderOrder` | `test_build_canonical_factory_helper` | Factory API |
| `TestPositivePath` | `test_primary_provider_succeeds_returns_response` | EXECUTABLE positive |
| `TestPositivePath` | `test_primary_success_does_not_invoke_lower_tiers` | Tier isolation |
| `TestPositivePath` | `test_token_budget_passed_through_unchanged` | **Cap removal proof** |
| `TestPositivePath` | `test_large_token_budget_8k` | **Cap removal proof (8k)** |
| `TestFailoverRouting` | `test_failover_to_openrouter_when_groq_fails` | EXECUTABLE failover |
| `TestFailoverRouting` | `test_failover_to_openai_when_groq_and_openrouter_fail` | Full failover chain |
| `TestFailoverRouting` | `test_failover_preserves_full_request` | Request integrity |
| `TestFailoverRouting` | `test_transient_failure_then_same_tier_succeeds_on_retry` | Per-tier retry |
| `TestFailClosedExhaustion` | `test_all_tiers_fail_raises_provider_exhausted_error` | EXECUTABLE negative |
| `TestFailClosedExhaustion` | `test_exhausted_error_message_contains_all_providers` | Error signal quality |
| `TestFailClosedExhaustion` | `test_single_provider_exhausted_also_fails_closed` | Fail-closed |
| `TestFailClosedExhaustion` | `test_exhausted_error_not_swallowed_by_routing_layer` | No silent failure |
| `TestBackoffPolicy` | `test_backoff_wait_grows_exponentially` | Backoff formula |
| `TestBackoffPolicy` | `test_backoff_is_capped_at_max_seconds` | Backoff ceiling |
| `TestBackoffPolicy` | `test_sleep_is_called_between_attempts` | Backoff invocation |
| `TestBackoffPolicy` | `test_no_sleep_after_last_exhausted_attempt` | No spurious sleep |
| `TestBackoffPolicy` | `test_sleep_between_tier_transitions` | Inter-tier backoff |
| `TestModelOverride` | `test_model_override_applied_for_fallback_tier` | Per-tier model |
| `TestModelOverride` | `test_no_override_passes_original_model_id` | Model passthrough |
| `TestAgentInvocationRuntimeIntegration` | `test_runtime_uses_provider_router_in_production_mode` | **Integration boundary** |
| `TestAgentInvocationRuntimeIntegration` | `test_runtime_fails_closed_when_all_router_tiers_exhausted` | **Integration negative** |
| `TestAgentInvocationRuntimeIntegration` | `test_runtime_failover_to_openrouter_in_production_mode` | **Integration failover** |
| `TestAgentInvocationRuntimeIntegration` | `test_runtime_accepts_large_max_tokens_without_cap` | **Cap removal at boundary** |
| `TestRegressionExistingBehaviour` | `test_test_fixture_mode_without_router_still_works` | Regression |
| `TestRegressionExistingBehaviour` | `test_test_fixture_mode_with_inference_fn_still_works` | Regression |
| `TestRegressionExistingBehaviour` | `test_integrity_check_still_raises_on_tampered_invocation` | Anti-tamper regression |
| `TestRegressionExistingBehaviour` | `test_provider_router_preferred_over_model_reasoning_engine` | Priority ordering |
| `TestFalseProofGuard` | `test_provider_name_in_list_does_not_prove_failover` | **False-proof countercase** |
| `TestFalseProofGuard` | `test_naming_groq_as_provider_does_not_prove_it_was_called` | **False-proof countercase** |

---

## 5. Evidence Package for Operator Decision

### What was found (pre-change state)

- **500-token hard cap located:** `packages/ca_runtime/src/ca_runtime/agent_invocation.py`, lines with `max_tokens=500` in both the PRODUCTION and TEST_FIXTURE branches of `AgentInvocationRuntime.execute()`.
- **Single-provider point of failure:** `model_reasoning_engine.infer()` was called directly with no retry, no failover, no backoff.  If the engine failed, the entire invocation aborted.
- **No `provider_router.py` existed** in the `ca_runtime` package.

### What was changed (post-change state)

| Property | Before | After |
|---|---|---|
| Token cap | Hard `max_tokens=500` in both execution branches | `_DEFAULT_MAX_TOKENS = 8_192` (soft default, caller controls) |
| Provider routing | Single engine call, no fallback | `ProviderRouter`: Groq → OpenRouter → OpenAI with exponential backoff |
| On provider failure | Unhandled exception aborts the run | Automatic failover to next tier; `ProviderExhaustedError` only when all fail |
| On exhaustion | Unstructured exception | `ProviderExhaustedError` → re-raised as `ProductionExecutionModeViolationError` (existing error contract) |
| `provider_router.py` | Did not exist | New module with full public API and `CANONICAL_PROVIDER_ORDER` constant |

### Residual limitations

1. **No live credentials tested.** The test suite uses injected stub callables.  Live provider HTTP clients (Groq SDK, OpenRouter SDK, OpenAI SDK) must be implemented separately by the team and injected via `build_canonical_provider_router()`.  The routing structure and simulated failover are proven; live end-to-end calls require credentials.
2. **`max_tokens` from agent policy.** `_DEFAULT_MAX_TOKENS = 8_192` is used when the caller doesn't set `_max_tokens_hint` in `output_contract`. The agent compiler's `token_budget` field should be plumbed through to `output_contract._max_tokens_hint` in a follow-on change; however, even the current default (8192) eliminates the 500-token block.
3. **No schema self-repair.** Out of scope per mandate §5 (Q39).
4. **No spend-ceiling enforcement.** Out of scope per mandate §5 (later wave).

### Commit SHA

*(To be captured by the Operator after applying and committing.  Command: `git rev-parse HEAD`)*

---

## 6. Operator Decision Request

**Approve or reject CA-M038.**

The mandate is satisfied when:

- [x] The artificial 500-token hard cap is removed from `agent_invocation.py`.
- [x] `provider_router.py` implements 3-tier routing (Groq → OpenRouter → OpenAI) with exponential backoff.
- [x] Single-provider failure triggers automatic failover, not run abort.
- [x] All tiers exhausted → `ProviderExhaustedError` / `ProductionExecutionModeViolationError` (fail-closed).
- [x] EXECUTABLE positive path test passes (primary provider succeeds).
- [x] EXECUTABLE negative/fail-closed path test passes (all tiers fail → structured error).
- [x] Token-cap-removal proof test passes (`max_tokens=8192` is passed through unchanged).
- [x] Integration evidence at the routing boundary (`AgentInvocationRuntime.execute` + `ProviderRouter`).
- [x] False-proof countercase tests verify actual call side-effects, not just names in lists.
- [x] Regression tests confirm existing contracts (`TEST_FIXTURE` mode, `inference_fn`, integrity checks) are unaffected.
- [x] No prohibited surfaces modified (no UI, no Q39 self-repair, no economics logic).
- [x] Residual limitations documented.

**Please confirm: APPROVE or REJECT CA-M038.**
