# CA-M045 — Worker Restart and Zombie Lease Reconciliation

## 1. Identity and status

- **Mandate ID:** `CA-M045`
- **Canonical question:** `Q44`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-REC-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q34–Q41 lease and state semantics; existing execution aggregate schema
- **Primary physical surfaces:** `api/main.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; lease schema/migration; reconciliation tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement startup reconciliation for expired worker leases so that orphaned executions do not remain permanently stuck in `RUNNING` after a worker crash. The contract is that the runtime records lease ownership and expiry durably, then on service startup identifies leases whose expiration time has passed, transitions those aggregates to `PAUSED` through the authoritative state path, and emits a signed/auditable receipt describing the reconciliation. The purpose is fault-tolerant recovery without pretending the system knows more than it does: an expired lease establishes loss of current worker ownership, not successful completion or semantic failure of the underlying work.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority is the Q44 decision and architecture fault-tolerance doctrine. Runtime authority is the canonical execution aggregate/lease state and startup lifecycle. Change authority remains operator-governed. The reconciler may move an expired execution from an active ownership state to the explicitly ratified recovery state `PAUSED`, but it may not invent business outcomes, delete evidence, or resume work automatically unless the existing architecture already says so. Workspace and aggregate identity remain part of the authority boundary. A lease record in a projection or log does not override the authoritative aggregate state.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q44`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q44`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q44` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `api/main.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; lease schema/migration; reconciliation tests`
- Q44 decision in ledger; architecture lease/fault-tolerance sections; `api/main.py::lifespan`; aggregate schema/migrations; state transition/receipt helpers; tests around startup and lease expiry.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M045` / `Q44` as defined by the ratified canon and the physical surfaces named above.

Implement only the durable lease fields and startup reconciliation necessary for expired orphan detection: `lease_worker_id`, `lease_expires_at`, schema/migration support, a startup reconciliation hook, an idempotent reconciliation operation, and executable tests. Inputs are persisted execution aggregates, their lease metadata, current time, and existing state/receipt infrastructure. Outputs are reconciled `PAUSED` aggregates with a durable audit receipt where expiration predicates match. Operators allowed are executor and Operator. Validators must cover active unexpired lease preservation, expired lease pause, repeated startup idempotency, wrong workspace/aggregate isolation, and receipt creation.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `api/main.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; lease schema/migration; reconciliation tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not automatically mark work successful, failed, or completed merely because a lease expired. Do not delete or reset historical transition evidence. Do not revive an expired worker by extending the lease silently. Do not use a process-local list of “known workers” as authoritative state. Do not scan or mutate aggregates outside the declared workspace/tenant scope. Do not implement distributed consensus or a new scheduler. Do not make startup reconciliation rewrite already reconciled `PAUSED` state repeatedly. Do not confuse clock skew handling with business logic; use the repository’s defined time source and document limitations. If time semantics or lease ownership are materially undefined, stop rather than inventing policy.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace how execution leases are currently acquired, refreshed, and released. Add the minimum schema support for durable worker identity and expiration if missing. Implement a startup hook in the existing application lifecycle that invokes reconciliation against the canonical state store. The operation must atomically identify eligible expired leases, verify the current state and lease owner/expiry predicate, transition the aggregate to `PAUSED`, and create the appropriate audit/transition receipt using existing state machinery. Make the operation idempotent: a second startup should not generate a second logical reconciliation transition for the same already-paused aggregate. Test an unexpired lease remains untouched, an expired lease is paused, a non-running aggregate is not incorrectly changed, and two reconciliation invocations do not double-apply the transition. Exercise workspace predicates and ensure one workspace cannot reconcile another. Keep the time comparison deterministic in tests using the repository’s clock abstraction or controlled fixture time where available. Do not add auto-resume behavior.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Evidence must exercise the startup/runtime boundary, not a helper function alone. Required proof includes schema/migration evidence, executable startup reconciliation, negative proof for unexpired leases, idempotency proof, and tenant/workspace isolation. The verifier measures expired-lease detection and safe state recovery to `PAUSED`; it does not prove that all worker failures will always be detected instantaneously, nor that clock skew is globally eliminated. False-proof countercase: directly setting a row to `PAUSED` in a test fixture and asserting the row changed; that bypasses the startup reconciliation path and proves nothing about integration. Environment fidelity requires the application lifecycle or an equivalent real entry point. Human review is required if the recovery state semantics differ from the ratified Q44 decision.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop if lease ownership is not authoritative, time semantics are undefined, reconciliation cannot be made idempotent, or startup integration would create cross-workspace mutations. Stop after Q44 evidence and operator request.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Rollback code and migrations using repository conventions. Never delete reconciliation receipts. If the startup hook misbehaves, disable the hook through a governed code rollback rather than editing affected historical rows. For forward-only migrations, preserve the schema and revert only runtime behavior if the architecture allows. Any ambiguous production recovery must be escalated to the Operator.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M045` based on executable proof that expired worker leases are reconciled to `PAUSED` exactly once, with durable evidence and workspace-safe predicates.

## 13. 200–300 word activation prompt

Execute `CA-M045` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q44 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, `api/main.py`, the current aggregate/lease schema, and state transition/receipt tests. Implement `INV-REC-001`: on startup, expired worker leases must be detected in the canonical state store and reconciled to `PAUSED` with an audit receipt. Scope is lease metadata/schema, startup hook, idempotent reconciliation, and focused tests. Do not auto-resume, infer business success/failure, rewrite historical evidence, or implement Q45–Q48. Prove that an unexpired lease is preserved, an expired running lease becomes `PAUSED`, a second startup does not duplicate the logical reconciliation, and workspace fencing prevents cross-tenant reconciliation. Exercise the real startup/lifecycle boundary or the repository-equivalent integration entry point; direct SQL fixture mutation is not sufficient. Record exact time/environment assumptions and limitations around clock skew. Stop on undefined lease authority, time semantics, or unsafe shared-state ownership. Completion requires changed files, exact executable evidence, evidence classes, false-proof countercase, control-state update, commit SHA, and the Operator decision request: approve or reject `CA-M045`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

