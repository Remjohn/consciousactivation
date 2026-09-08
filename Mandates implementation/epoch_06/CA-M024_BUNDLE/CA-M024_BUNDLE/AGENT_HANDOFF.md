# CA-M024 — Preliminary Auth Policy

## Mandate ID & Title

**Mandate ID:** `CA-M024`  
**Mandate Title:** `Preliminary Auth Policy`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py` | Added an immutable preliminary authorization policy/request model, deterministic permission and hard resource-quota evaluator, structured denial gap reporting, policy hashing, and a fail-closed downstream execution gate for exploratory, drafting, and non-production runs. | `FR-024`: no execution is authorized unless authentication, execution-specific permission, non-production boundary, and every configured hard quota pass. |
| `tests/interview_intelligence/test_ca_m024_preliminary_auth.py` | Added 19 self-contained executable tests covering positive paths, each permission/quota failure, multi-gap reporting, production denial, policy integrity, deterministic evidence, false-proof rejection, and downstream non-invocation on denial. | Executable evidence demonstrates that valid exploratory/drafting/non-production requests pass while invalid authorization or exhausted resource bounds fail closed. |

## Files Added and Files Modified

### Files Added

- `services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py` — new CA-M024 implementation surface; the repository did not contain the requested module.
- `tests/interview_intelligence/test_ca_m024_preliminary_auth.py` — new direct tests for the requested implementation surface.

### Files Modified

- None.

## Exact paste instructions and post-apply commands

Copy the two bundled files to these exact repository destinations, preserving directory structure:

```text
services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py
 tests/interview_intelligence/test_ca_m024_preliminary_auth.py
```

No database migration, schema migration, generated artifact, setup change, or script update is required by this bounded implementation.

From repository root, run:

```bash
PYTHONPATH=services/interview-intelligence/src pytest -q tests/interview_intelligence/test_ca_m024_preliminary_auth.py
python -m py_compile services/interview-intelligence/src/cae_interview_intelligence/preliminary_auth.py
```

## Test Command

```bash
PYTHONPATH=services/interview-intelligence/src pytest -q tests/interview_intelligence/test_ca_m024_preliminary_auth.py
```

## Expected Test Results

**19 automated tests, all passing.**

Sandbox result:

```text
19 passed in 0.21s
```

A broader `tests/interview_intelligence` collection was also attempted. Three pre-existing tests could not be collected because the sandbox environment is missing the unrelated `psycopg` dependency required by `ca_runtime`; the CA-M024 suite itself is dependency-self-contained and passed 19/19.
