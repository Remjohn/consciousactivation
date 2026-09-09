# CA-M054 — Unified Telemetry Flywheel

## Mandate ID & Title

**Mandate ID:** CA-M054  
**Mandate Title:** Unified Telemetry Flywheel  
**Execution status:** **STOPPED — OPERATOR DECISION REQUIRED**  
**Requested invariant:** `INV-TEL-001`  
**Canonical mandate invariant in `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/06_CA_MANDATE_054.md`:** `INV-TELEM-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| None | No implementation or test files were changed because the canonical CA-M054 mandate declares an authority/scope collision with the supplied execution brief. | Not proven; execution is intentionally stopped before unauthorized boundary expansion. |

### Blocking collision

The supplied execution brief names:

- `services/pipeline/src/cmf_pipeline/telemetry/flywheel.py`
- `tests/pipeline/test_ca_m054_telemetry_flywheel.py`
- invariant `INV-TEL-001`

The repository's canonical CA-M054 mandate, `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/06_CA_MANDATE_054.md`, instead states:

- **Governing invariant:** `INV-TELEM-001`
- **Primary implementation surface:** `packages/ca_runtime/src/ca_runtime/factory_observability.py`
- **Primary implementation surface:** `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- **Allowed implementation behavior:** six-class telemetry taxonomy, genuine operator gate capture, PII-redacted preference pairs, versioned export, and read-only training derivations.

The same repository also contains `docs/cae/PROMPT_REFERENCE_BLOCKS.md`, which explicitly lists CA-M054 as:

- **Invariant:** `INV-TEL-001`
- **Targets:** `services/pipeline/src/cmf_pipeline/telemetry/flywheel.py` and `tests/pipeline/test_ca_m054_telemetry_flywheel.py`
- **Acceptance criterion:** aggregate structured telemetry, execution latencies, token consumption, and failure diagnostics across pipeline services.

These are materially different authorities. The CA-M054 mandate itself requires a stop on undeclared file boundaries / authority conflicts rather than a locally convenient interpretation.

### Repository-state observations

- `services/pipeline/src/cmf_pipeline/telemetry/flywheel.py` is absent from the supplied repository snapshot.
- `services/pipeline/tests/pipeline/test_ca_m054_telemetry_flywheel.py` is absent from the supplied repository snapshot.
- `packages/ca_runtime/src/ca_runtime/factory_observability.py` exists.
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` exists.
- The uploaded repository snapshot does not include `.git`, so an exact commit SHA cannot be captured from this evidence package.

## Files Added and Files Modified

### Files Added

**Repository destination:** none.

No code/test artifact was added because the target pipeline surface is not authorized by the canonical CA-M054 mandate currently present in the repository.

### Files Modified

**Repository destination:** none.

No existing repository file was modified. In particular, the canonical `packages/ca_runtime` files were not changed, because the supplied execution brief directs implementation to a different subsystem and the mandate requires a collision decision before scope expansion or reinterpretation.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

**Do not paste or apply implementation changes from this bundle.**

This bundle is a collision handoff, not an implementation patch.

Operator decision required before execution can continue:

1. Resolve which authority governs CA-M054:
   - **Canonical mandate document:** `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/06_CA_MANDATE_054.md` (`INV-TELEM-001`, `packages/ca_runtime/...`)
   - **Repository mandate index / execution brief:** `docs/cae/PROMPT_REFERENCE_BLOCKS.md` and the supplied mandate details (`INV-TEL-001`, `services/pipeline/...`)
2. Record the decision in the repository's governing control/decision mechanism.
3. If the pipeline interpretation is approved, issue an explicit bounded-scope authority update naming the exact pipeline files and acceptance criteria.
4. Only after that decision should an implementation bundle be generated and applied.
5. No database migration, deployment, or post-apply script is authorized by this collision handoff.

### Evidence classes

- `DOCUMENT`: conflicting CA-M054 scope/invariant authorities were located in repository documentation.
- `EXECUTABLE`: repository state inspection confirmed the canonical `packages/ca_runtime` files exist and the supplied pipeline target files do not.
- `TEST`: mandate-specific tests were not executed because the required implementation boundary is unresolved.
- `OPERATOR_DECISION_REQUIRED`: authority/scope collision must be resolved before implementation.

### Rollback / recovery status

No repository mutation occurred, so there is no code, schema, receipt, telemetry, benchmark record, or derived artifact requiring rollback from this execution attempt.

## Test Command (exact pytest/test command to verify)

Once the scope authority is resolved to the supplied pipeline mandate, the exact targeted command should be:

```bash
pytest -q tests/pipeline/test_ca_m054_telemetry_flywheel.py
```

A broader repository regression command may be selected only after the targeted mandate test is present and passing.

## Expected Test Results (number of automated tests, all passing)

**Current execution:** `0` mandate-specific tests executed; **PASS RATE: not applicable** because execution stopped before any unauthorized implementation or test-file creation.

**Required completion condition after operator resolution:** the mandate-specific suite must run with **100% passing automated tests**, including:
- positive acceptance coverage,
- negative/blocked behavior,
- the false-proof countercase,
- and any process/persistence fidelity checks material to the resolved invariant.

## Operator decision requested

Please record exactly one decision against this collision:

- **APPROVE** — authorize the pipeline `INV-TEL-001` interpretation and its declared file boundary, or
- **REJECT** — retain the canonical `packages/ca_runtime` CA-M054 interpretation, or
- **DEFER** — named remediation/authority update required before implementation.

**No decision has been inferred from the green/absent test state.**

## Commit SHA

**Unavailable in the supplied snapshot:** the uploaded repository archive contains no `.git` metadata, so an exact commit SHA cannot be captured without an external repository checkout/reference.
