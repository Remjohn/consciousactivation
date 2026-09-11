# CA-M042 — Atomic CAS State Transitions in SQLite

## 1. Identity and status

- **Mandate ID:** `CA-M042`
- **Canonical question:** `Q41`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-CAS-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q34–Q40 execution spine; existing aggregate version/state/receipt implementation
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; related SQLite schema/migrations; focused state-transition tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement the ratified atomic compare-and-swap contract for CAE program-state mutation so that every authoritative state transition is committed only when the persisted aggregate version still equals the executor’s expected version. The current defect class is a Python-level read-modify-write sequence that allows two workers to observe the same version and both construct apparently valid next states. The objective is therefore not merely to “add locking” or make a test pass; it is to move the correctness predicate into SQLite itself, use the repository’s transaction conventions, and prove that a mutation succeeds exactly once when its expected version matches and fails closed when it does not. The implementation must preserve the existing state machine, receipt semantics, workspace fencing, and downstream replay assumptions.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic meaning comes from the Master 57-question canon and the Q41 decision in the convergence ledger. Runtime authority is the canonical CAE state store and the repository’s state-runtime transaction path. Change/promotion authority remains the Operator and governed repository process; an agent may implement and test but may not invent an alternate state authority. PostgreSQL/Supabase remains the intended operational authority where the architecture says so, but this specific Q41 contract is explicitly a SQLite atomic CAS boundary in the runtime surfaces named by the decision. The executor must not reinterpret the existence of an aggregate version field as proof of atomicity. The controlling predicate is the database operation itself: `UPDATE ... SET ... version = version + 1 WHERE ... version = expected_version`, executed inside the appropriate transaction boundary and judged by affected-row count.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q41`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q41`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q41` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; related SQLite schema/migrations; focused state-transition tests`
- Q41 decision text in `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`; current state-runtime implementation; directly referenced SQLite schema/migration/test files; any existing receipt-writing helper that the CAS transition invokes.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M042` / `Q41` as defined by the ratified canon and the physical surfaces named above.

The exact scope is the authoritative state-mutation path for the Q41 aggregate transition contract: schema/migration support for versioned aggregates if required; a typed/internal CAS primitive or equivalent existing helper; transaction configuration needed to preserve the atomic predicate; transition construction that passes the expected version; and executable positive/negative/concurrency tests. The output must include enough evidence to demonstrate one-success/one-failure behavior under competing writers. Inputs are the current aggregate identity, workspace/tenant scope where applicable, expected version, proposed next state, and any receipt payload required by the already-existing transition contract. Outputs are either one durable committed mutation with incremented version or a deterministic CAS conflict/error with no partial state change. Operators allowed are the repository executor for code/tests and the Operator for approval. Validators must exercise actual SQLite behavior, not mocks only.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; related SQLite schema/migrations; focused state-transition tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not redesign the state machine, replace SQLite, introduce a distributed locking service, weaken version checks, perform a second read after a failed CAS and silently retry as though the original write succeeded, or mutate unrelated authorization/replay/lease/security semantics. Do not rely on process-local mutexes as the correctness mechanism; such a mutex cannot establish the required database-level single-writer predicate across processes. Do not claim success because two sequential unit calls pass. Do not write directly to tables from tests in a way that bypasses the state-runtime function under test. If the current schema or transaction mode conflicts with Q41, classify the collision before editing. If a shared migration or receipt schema is needed by another mandate, preserve one integration owner and stop if ownership is ambiguous.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

First inventory the existing aggregate update flow and identify every place that can mutate `cae_program_state_aggregates`. Trace the read of the current version, construction of the next state, receipt creation, and commit boundary. Replace only the authoritative mutation primitive with the smallest safe CAS operation. Use the repository’s transaction mode and ensure the compare predicate, state update, and version increment happen in one atomic database transaction. The affected-row count must be the success criterion. A zero-row update is a conflict/failure, not a success requiring semantic guessing. Ensure receipt creation is consistent with commit semantics: a receipt must not falsely claim a transition that the CAS rejected. Preserve workspace/aggregate predicates where they already exist so CAS cannot become a tenant-fencing bypass. Add focused tests for expected-version success, stale-version rejection, competing writers, no partial write on failure, and retry behavior that is explicitly distinguished from duplicate commit. Where possible, use two real connections or worker contexts to demonstrate the race that the old Python read-modify-write allowed. Record exact commands and observed row counts. Do not broaden the work into the Q42 cryptographic chain or Q44 reconciliation implementation except where the existing receipt path is directly invoked and must remain intact.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Required proof is executable evidence at the real SQLite persistence boundary. Record the exact test command, Python/runtime version, SQLite configuration, fixture setup, and result. The positive proof must show an update from version N to N+1 when the predicate matches. The negative proof must show version N+1 remains unchanged when a stale actor presents N. The concurrency proof must show competing actors do not both commit the same logical transition. The verifier must state what it measures and what it does not measure: it proves atomic CAS semantics and single-row commit behavior; it does not prove distributed consensus or correctness of every other state transition. False-proof countercase: two calls protected by one in-process mutex can pass while two independent worker processes still race; reject that as insufficient environment fidelity. Schema evidence may prove the version column exists, but only `EXECUTABLE`/`TEST` evidence proves the database predicate is authoritative. Human/operator validation is required for final promotion if shared state semantics changed.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop if the authoritative mutation path cannot be located, if a shared migration requires an unowned integration decision, if the repository transaction mode makes the stated CAS predicate unsafe, or if concurrency evidence cannot be produced at the real boundary. Stop after the Q41 proof and control-state update; do not begin Q42.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Use an isolated commit and the repository’s migration conventions. If the change proves unsafe, revert the CAS implementation without deleting historical receipts or state-transition evidence. Do not “repair” a bad historical state by overwriting the evidence. If a migration is forward-only, document the recovery procedure and preserve a clean path to redeploy. If partial changes have reached a test database only, rebuild or reset the disposable fixture. If production-like state has been touched and recovery requires policy choice, stop with `OPERATOR_DECISION_REQUIRED` rather than improvising.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M042` based on whether the executable evidence proves atomic SQLite CAS semantics, stale-write rejection, and one-success/one-failure concurrency behavior at the canonical state-runtime boundary.

## 13. 200–300 word activation prompt

Execute `CA-M042` only. Read `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`, `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`, the Q41 decision in `docs/cae/cae_master_57_question_convergence_canon.md` and `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`, plus `docs/cae/Architecture.md`, `docs/cae/UI.md`, and the current `program_state_runtime.py`/SQLite schema and tests. Implement `INV-CAS-001`: authoritative state mutations must use an atomic SQLite compare-and-swap predicate against the expected version, with the database affected-row count determining success. Scope is the state mutation primitive, necessary schema/migration support, transaction boundary, receipt consistency, and real concurrency tests. Do not redesign the state machine, replace SQLite, add distributed locks, or implement Q42–Q48. Do not accept an in-process mutex or mocked repository as proof. Prove a successful N→N+1 update, stale-version rejection with no partial commit, and concurrent competing writers where only one logical winner commits. Record exact environment, commands, fixture method, evidence classes, and limitations. If the CAS boundary collides with a shared migration or receipt change owned elsewhere, classify the collision and stop. Completion requires changed-file evidence, exact executable test evidence, negative proof, false-proof countercase, control-state update, commit SHA, and the Operator decision request: approve or reject `CA-M042`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

