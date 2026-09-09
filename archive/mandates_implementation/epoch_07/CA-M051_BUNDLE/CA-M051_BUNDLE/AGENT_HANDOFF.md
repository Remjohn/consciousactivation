# Mandate ID & Title

**CA-M051 — Model Economics & Quotas**

**Governing invariant:** `INV-ECON-001`

The authoritative CA-M051 mandate at `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/03_CA_MANDATE_051.md` identifies `packages/ca_runtime/src/ca_runtime/agent_invocation.py` and `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` as the canonical implementation surfaces. The prompt-listed `services/pipeline/src/cmf_pipeline/economics/quota_engine.py` does not exist in the supplied repository and is not named by the authoritative mandate, so it was not introduced as an unauthorized parallel implementation.

# Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/agent_invocation.py` | Added economic authorization/settlement contracts, provider-reported usage and cost propagation, economic receipt fields, production accounting gating, and rejection of synthetic `inference_fn` execution when a state-bound production invocation is economically governed. | Provider usage reaches the canonical execution receipt; economically governed dispatch cannot proceed without an admissible accounting controller/source. |
| `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | Added workspace/aggregate hard budget reservations, provider request/token rolling limits, micro-cost rate-card fallback, fail-closed unmetered-cost rejection, durable economic state in aggregate JSON, 3-state circuit breaker, idempotent charge protection, tenant binding, and budget/rate-limit receipts. | Execution is blocked before provider dispatch when available quota is exhausted; actual provider spend is settled into canonical state; overruns and failures are receipted; retries cannot double-charge. |
| `tests/pipeline/test_ca_m051_quota_engine.py` | Added self-contained CA-M051 unit/integration coverage for budgets, provider limits, circuit states, persistence, tenant isolation, invocation-bound enforcement, real execution settlement, double-charge prevention, overrun receipts, and unmetered-cost fail-closed behavior. | `INV-ECON-001` behavior is executable and regression-tested. |

# Files Added and Files Modified

## Files Added

**`tests/pipeline/test_ca_m051_quota_engine.py`**

Rationale: New mandate-specific tests exercising the complete economic gate and the canonical invocation/runtime integration without modifying unrelated test infrastructure.

## Files Modified

**`packages/ca_runtime/src/ca_runtime/agent_invocation.py`**

Rationale: This is the canonical model-invocation boundary identified by CA-M051. It now authorizes economically governed invocations before provider execution, captures provider-reported token/cost usage, settles usage before downstream output validation, and carries the economic receipt/status into the immutable invocation receipt.

**`packages/ca_runtime/src/ca_runtime/program_state_runtime.py`**

Rationale: This is the canonical program-state/economic accounting boundary identified by CA-M051. Economic reservations, aggregate/workspace ceilings, provider rate windows, circuit-breaker state, usage aggregation, receipts, and persistence are attached to the authoritative state aggregate.

# Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. From the repository root, copy the three bundled files to the exact repository destinations, preserving directory structure:
   - `packages/ca_runtime/src/ca_runtime/agent_invocation.py`
   - `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
   - `tests/pipeline/test_ca_m051_quota_engine.py`

2. No database migration is required. CA-M051 persists economic accounting inside the existing `ProgramStateAggregate.state_data` JSON payload, so the implementation does not add a new schema/table migration.

3. Verify syntax:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/agent_invocation.py packages/ca_runtime/src/ca_runtime/program_state_runtime.py tests/pipeline/test_ca_m051_quota_engine.py
```

4. Run the mandate verification:

```bash
pytest -q tests/pipeline/test_ca_m051_quota_engine.py
```

5. Production callers using CA-M051 must construct a `ProgramStateEconomicQuotaController` with the applicable `EconomicPolicy` and pass it to `AgentInvocationRuntime.execute(...)` together with the invocation cost ceiling. The controller must run under the correct tenant context.

# Test Command

```bash
pytest -q tests/pipeline/test_ca_m051_quota_engine.py
```

# Expected Test Results

**14 automated CA-M051 tests, all passing (14 passed).**

Additional scoped regression verification in the supplied sandbox: the existing CA-M052/M038/M067 invocation-related suites passed **51/51** tests. Broader legacy CA-M072/state-runtime tests were not used as a mandate pass/fail criterion because the supplied archive's sandbox lacks its PostgreSQL dependency and program-discovery environment; those failures are environment/baseline-related rather than CA-M051 test failures.

## Operator decision required by CA-M051

**APPROVE / REJECT / DEFER:** operator action remains required for final mandate ratification.

**Commit SHA:** unavailable because the supplied `codebase_clean(1).zip` archive contains no `.git` metadata. The three bundled file SHA-256 digests are:

- `agent_invocation.py`: `a88a24f42ed076d00fb3ebd67ecf931ab01ae0bd4f89e15a67280b3393973494`
- `program_state_runtime.py`: `cf56a058117013e8baf694fa69cfafe296e77234011b0e6fe2789e8ab7d03768`
- `test_ca_m051_quota_engine.py`: `358a2f2e68f730490ca8ea8dd0bdb277420b8cd9521edc616a5e69314ccaf448`
