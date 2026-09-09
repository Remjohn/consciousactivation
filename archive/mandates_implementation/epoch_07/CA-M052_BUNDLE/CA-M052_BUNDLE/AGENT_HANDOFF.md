# CA-M052 — Subject Constitution Voice DNA

## Mandate ID & Title

**Mandate ID:** `CA-M052`  
**Mandate Title:** `Subject Constitution Voice DNA`  
**Governing invariant:** `INV-VOICE-001`  
**Decision:** Q51 / Subject Constitution & Voice DNA  

### Scope authority note

The canonical CA-M052 mandate document in `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_07/04_CA_MANDATE_052.md` identifies the authoritative implementation surface as:

- `services/collision-intelligence/src/cae_collision_intelligence/composer.py`
- `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py`

The user-supplied target `services/interview/src/conscious_activations_interview_expression/voice_dna.py` does not exist in the supplied repository archive, and the canonical mandate does not authorize creating a parallel implementation there. That path was therefore not added; implementation remains on the canonical Q51 surfaces.

## Summary Table (File changed | What changed | Invariant proven)

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/collision-intelligence/src/cae_collision_intelligence/composer.py` | Added immutable tenant/subject-bound `VoiceDNAProfile`; deterministic acoustic and linguistic feature extraction; character-exact quote verification with speaker attribution; contrastive anti-genericization scoring; configurable fail-closed voice-drift gate; structured verification report. | `INV-VOICE-001`: synthesis cannot pass when quote fidelity, Voice DNA drift, or subject-specific distinctiveness fails. |
| `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py` | Added serialized runtime Voice DNA request contract; COMPOSER-lane verification boundary; rejection receipt persistence through the existing evaluation-receipt store; optional strict `voice_dna_required` integration into hypothesis composition. | `INV-VOICE-001` reaches the runtime boundary and persists explicit rejection evidence before re-raising a typed gate failure. |
| `tests/phase4/test_ca_m052_voice_dna.py` | Added 10 self-contained mandate tests covering extraction, immutable binding, positive acceptance, quote mismatch, attribution mismatch, genericized false-proof rejection, acoustic drift, stale/cross-tenant binding, persistent rejection receipt, and compose-boundary blocking. | Positive + negative + false-proof countercase are executable and deterministic. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Modified

1. `services/collision-intelligence/src/cae_collision_intelligence/composer.py`  
   **Rationale:** Canonical Q51/FR-051 implementation surface. Adds the actual Voice DNA feature extraction and synthesis gate rather than placing logic in an unreferenced helper.

2. `packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py`  
   **Rationale:** Canonical runtime boundary named by Q51. Enforces COMPOSER-lane verification and persists explicit rejected-synthesis evidence.

### Files Added

3. `tests/phase4/test_ca_m052_voice_dna.py`  
   **Rationale:** Direct mandate-specific executable proof suite. It uses actual SQLite persistence for the rejection-receipt assertion while isolating unavailable repository-wide runtime dependencies so the CA-M052 proof remains runnable in the supplied sandbox.

No migration file was added: rejection evidence reuses the existing `hypothesis_evaluation_receipt` schema, so no database schema change is required.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Copy the three files from this bundle into the repository at exactly these destinations, replacing the two existing implementation files and adding the new test file:

```text
services/collision-intelligence/src/cae_collision_intelligence/composer.py
packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py
tests/phase4/test_ca_m052_voice_dna.py
```

No migration is required for CA-M052 because the implementation records rejection evidence through the existing `hypothesis_evaluation_receipt` table.

For a normal repository environment, install the repository’s declared packages/dependencies before running the full suite. The runtime package declares `psycopg[binary]>=3.2,<4`; the supplied sandbox did not contain that dependency and network installation was unavailable.

Post-apply verification commands:

```bash
PYTHONPATH=services/collision-intelligence/src pytest -q tests/phase4/test_ca_m052_voice_dna.py

PYTHONPATH=services/collision-intelligence/src pytest -q \
  tests/collision_intelligence/test_collision_composition.py \
  tests/collision_intelligence/test_four_world_intersection.py \
  tests/collision_intelligence/test_collision_domain_contracts.py \
  tests/collision_intelligence/test_collision_adversarial_cases.py

python -m compileall -q \
  services/collision-intelligence/src/cae_collision_intelligence/composer.py \
  packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py \
  tests/phase4/test_ca_m052_voice_dna.py
```

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH=services/collision-intelligence/src pytest -q \
  tests/phase4/test_ca_m052_voice_dna.py \
  tests/collision_intelligence/test_collision_composition.py \
  tests/collision_intelligence/test_four_world_intersection.py \
  tests/collision_intelligence/test_collision_domain_contracts.py \
  tests/collision_intelligence/test_collision_adversarial_cases.py
```

## Expected Test Results (number of automated tests, all passing)

**Expected:** `17 passed`  
**Observed:** `17 passed in 3.11s`

Mandate-specific breakdown: **10/10 passing**.  
Affected collision-intelligence regressions: **7/7 passing**.

### Evidence classes

- **SCHEMA:** `VoiceDNAProfile`, `VoiceDNAVerificationRequest`, and structured gate/quote-diff report types.
- **EXECUTABLE:** acoustic/linguistic extractors, exact quote matching, drift scoring, anti-genericization gate, runtime COMPOSER-lane verifier, and rejection receipt path.
- **TEST:** 10 CA-M052 tests plus 7 affected regression tests, all passing in the supplied sandbox.
- **DOCUMENT:** Q51/FR-051 and CA-M052 canonical mandate contract.

### False-proof countercase proven

A polished generic script containing an accurate quote and reporting a `generic_style_score=0.99` is still rejected because the project-specific terminology/cadence distinctiveness gate fails. Generic style scoring is recorded as evidence but never used as a substitute for Voice DNA preservation.

### Environment fidelity limitation

A broader repository suite was attempted. Collection was blocked by the supplied environment’s missing `psycopg` dependency (and the package dependency was not downloadable because the sandbox has no network access). No test was weakened or hidden to manufacture a green result. The CA-M052 proof itself is fully runnable and passed 10/10; affected collision-intelligence regressions passed 7/7.

### Commit SHA

**Unavailable.** The supplied `codebase_clean(1).zip` contains no `.git` metadata, so no authoritative commit SHA can be captured or honestly fabricated. The three delivered files were SHA-256 hashed in the execution workspace:

```text
954cea76f0b271450321438f287d454c7a20410895452c15de18625023f0d6ae  services/collision-intelligence/src/cae_collision_intelligence/composer.py
7f80f345f026702565316af23dadb8b588789f40f8c4beae737b23ad56972797  packages/ca_runtime/src/ca_runtime/collision_hypothesis_program.py
df1334bdd351c03446229c2e58d0fc14b5b5028a98eae8cb6f06dfb7bdeae96b  tests/phase4/test_ca_m052_voice_dna.py
```

### Rollback / recovery status

No database migration or application-state mutation was performed by the execution agent. Rollback is therefore normal file restoration through version control after the bundle is applied. No immutable receipts from the target repository were altered.

### Operator decision requested

**APPROVE**, **REJECT with findings**, or **DEFER with named remediation**.
