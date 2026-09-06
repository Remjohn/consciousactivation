# CA-M044 — Persisted Replay Verification Engine

## 1. Identity and status

- **Mandate ID:** `CA-M044`
- **Canonical question:** `Q43`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-REPL-001`
- **Collision primitive:** `PREDICTION VIOLATION`
- **Dependency set:** Q41 CAS; Q42 receipt chain; existing state snapshot model
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; replay verifier/tests; persisted SQLite snapshots/transitions`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement the persisted replay verification engine so a completed or paused CAE run can be reconstructed from durable transition records and checked for bit-for-bit parity against the recorded SQLite state snapshots. The decision is not a generic “replay feature.” It is a forensic verifier that proves the recorded sequence of accepted transitions can regenerate the stored state deterministically, while using the cryptographic receipt lineage from Q42 as an additional integrity constraint. The verifier must read persisted records, step through them in canonical order, reconstitute state, compare hashes or equivalent canonical state fingerprints, and report the first divergence with enough evidence to locate the failing transition. It must not silently repair state or rewrite history.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority comes from Q43 and the Master Canon. Runtime authority is the durable SQLite transition/snapshot ledger, not an in-memory copy retained by a running worker. The replay verifier is a verification tool, not a new state-authority path. It may read durable state and reconstruct a candidate state, but it must not promote its result into authoritative state automatically. Change/promotion authority remains the Operator. The verifier’s canonical ordering and state serialization must reuse existing runtime definitions wherever available. If the system does not have enough durable information to deterministically reconstruct a field, the correct output is an explicit evidence gap, not a guessed value.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q43`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q43`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q43` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; replay verifier/tests; persisted SQLite snapshots/transitions`
- Q43 decision, Q42 receipt-chain implementation, current snapshot/state-hash code, replay-related tests/helpers, and any runtime functions that define canonical state serialization.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M044` / `Q43` as defined by the ratified canon and the physical surfaces named above.

Implement `replay_and_verify_run()` or the project-equivalent only for the persisted state path. It may include a verifier API, CLI/test entry point, deterministic reconstruction helper, mismatch report structure, and focused tests. Inputs are a persisted execution/run identifier, its transition records, snapshot/state records, and Q42 receipt chain. Outputs are a verification result containing pass/fail, first mismatch location, expected and recomputed fingerprints, receipt/transition identifiers, and limitations. Operators allowed are executor and Operator. Validators must cover a multi-step replay pass, state mutation sequence, receipt-chain continuity, a single-field corruption, a reordered/missing transition, and a tampered snapshot. No automatic repair is allowed.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; replay verifier/tests; persisted SQLite snapshots/transitions`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not use live in-memory state as the primary replay source. Do not regenerate a snapshot and overwrite the stored snapshot to make parity pass. Do not skip a transition because it “looks redundant.” Do not use a weaker comparison such as equal object counts or selected field equality where the contract requires bit-for-bit/canonical state parity. Do not convert a failed replay into success by changing the verifier until the mismatch disappears. Do not claim that one happy-path replay proves historical determinism across all state shapes. Do not implement new execution semantics, model calls, or workflow steps as part of replay. If a state field is nondeterministic by design, it must have an explicit canonicalization rule already established by the architecture; otherwise record a limitation and stop.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Map the persisted transition sequence to the state machine’s actual reducer/transition semantics. Determine the canonical starting state and the exact state serialization/fingerprint used by the runtime or defined by the existing receipt system. Reconstruct state from the first accepted state through each persisted transition, verifying Q42 parent hashes as you go. After each step, compare the reconstructed state fingerprint to the durable snapshot associated with that point. On success, emit an ordered verification record. On failure, stop at the first divergence and emit enough context to identify the transition, receipt, version, and field or serialized fragment that differs. Include cases where the transition row is removed, duplicated, reordered, or the snapshot is altered. Ensure the verifier does not rely on mutable wall-clock values, unordered map iteration, or current runtime defaults that differ from the recorded state. The implementation should be deterministic and rerunnable against the same database without changing anything. Add a test that proves replay is read-only with respect to authoritative state. Do not expand into live-execution recovery or startup reconciliation; those are Q44.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Evidence must be executable and persisted. Positive proof requires replaying a run from durable SQLite records and achieving exact parity for every recorded checkpoint. Negative proofs must include at least one snapshot mutation and one transition mutation or omission, with verification failing at the first affected point. The verifier must state what it measures: deterministic reconstitution and parity against recorded state. It does not by itself prove model output determinism outside the persisted transition inputs. False-proof countercase: replay from a current in-memory aggregate or newly generated fixture and compare it to itself; reject as circular. Environment-fidelity requires the verifier to reopen the persisted data store, not reuse the original runtime object graph. Operator review is required for any accepted limitation involving fields that are not currently canonically serializable.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop on any missing durable transition/input required to reproduce state, an undefined serialization rule, or a mismatch whose root cause cannot be localized. Stop after recording the verifier result and limitation set; do not auto-repair, replay into production, or start Q44.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

The verifier should be read-only. Rollback is therefore limited to code/test changes. Revert the verifier implementation if unsafe; do not modify persisted historical snapshots or transitions. Any test fixtures corrupted during adversarial tests must be disposable and recreated. If a production-like database is found inconsistent, preserve it for evidence and escalate with `OPERATOR_DECISION_REQUIRED` rather than rewriting it.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M044` based on whether persisted replay proves bit-for-bit/canonical parity and identifies tampering/divergence without mutating authoritative state.

## 13. 200–300 word activation prompt

Execute `CA-M044` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q43 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, the Q42 receipt-chain path, current SQLite snapshot/state-hash logic, and replay tests/helpers. Implement `INV-REPL-001`: replay must sequentially reconstruct state from persisted transitions, verify receipt lineage, and prove parity against durable SQLite snapshots/fingerprints. Scope is the read-only replay verifier, deterministic reconstruction/serialization helpers, mismatch reporting, and tests. Do not repair state, mutate snapshots, run new model inference, or implement Q44–Q48. Prove positive replay from reopened persisted storage and negative replay after a snapshot mutation plus a transition omission/reorder/tamper. Reject in-memory self-comparison or freshly generated fixture comparison as false proof. The verifier must report the first divergence with exact transition/receipt/version evidence and must state what it does not prove about external model determinism. Stop if required state cannot be reconstructed without inventing semantics. Record exact commands, environment, evidence classes, limitations, control-state impact, and commit SHA. Completion requires the Operator decision request: approve or reject `CA-M044`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

