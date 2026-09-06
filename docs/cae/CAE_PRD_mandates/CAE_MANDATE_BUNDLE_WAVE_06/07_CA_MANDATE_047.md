# CA-M047 — Multi-Tenant Workspace Isolation

## 1. Identity and status

- **Mandate ID:** `CA-M047`
- **Canonical question:** `Q46`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-TEN-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q34–Q45 runtime state/control; existing workspace model
- **Primary physical surfaces:** `api/routers/programs.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; storage root resolution; auth/workspace tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement strict workspace/tenant fencing so execution, state, receipts, storage roots, and cryptographic lineage cannot cross an authorized workspace boundary. The decision requires mandatory `X-Workspace-ID` route fencing, composite `(aggregate_id, workspace_id)` persistence predicates, partitioned storage roots, and inclusion of workspace identity in Merkle hashing. The core objective is not merely to add a request header. It is to establish one consistent workspace identity across API admission, database queries, filesystem/object storage resolution, and cryptographic identity. A request that omits, mismatches, or attempts to substitute another workspace must fail closed before sensitive state is returned or mutated.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority is the Q46 decision, the Master Canon, and architecture security doctrine. Runtime authority is the authenticated workspace context and the canonical persistence/storage predicates that enforce it. A user name, campaign identifier, or path naming convention does not establish workspace authority. The executor must reuse existing authentication and workspace abstractions, not infer permission from identity similarity. Cryptographic authority includes workspace identity in the chain where ratified. Operator authority governs promotion of the security change. If the current deployment model does not provide an authoritative workspace source, stop rather than trusting a client-supplied header by itself.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q46`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q46`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q46` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `api/routers/programs.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; storage root resolution; auth/workspace tests`
- Q46 decision; architecture tenant/security sections; `api/routers/programs.py`; state-runtime storage query code; storage-root helpers; auth/workspace middleware; tests and migrations touching workspace IDs.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M047` / `Q46` as defined by the ratified canon and the physical surfaces named above.

Implement the minimum cross-layer workspace fence: mandatory workspace context at relevant program/execution routes; validation against the authenticated authority; composite database predicates; workspace-partitioned storage path/root resolution; and inclusion of workspace ID in the existing receipt/hash identity where explicitly required. Inputs are authenticated request context, workspace ID, aggregate IDs, and storage identifiers. Outputs are correctly scoped reads/writes or fail-closed authorization errors. Validators must include same-workspace positive access, missing-workspace rejection, cross-workspace read rejection, cross-workspace write rejection, storage path escape/alias cases, and cryptographic identity separation where applicable.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `api/routers/programs.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; storage root resolution; auth/workspace tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not rely on UI filters, client-side IDs, or a route parameter alone for tenant isolation. Do not duplicate the same aggregate ID into a global query and “check workspace later.” Do not use path prefixes as the only security barrier. Do not add a global superuser bypass for convenience. Do not silently fall back to a default workspace. Do not alter unrelated business semantics. Do not change historical Merkle records in place to inject workspace identity unless a ratified migration explicitly authorizes it. If existing data lacks a workspace and cannot be safely attributed, stop for an Operator migration decision.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace workspace identity from request entry through authorization, runtime state calls, persistence, and storage. Make the required workspace header/context mandatory where the Q46 boundary says it is mandatory and verify that the authenticated principal is allowed to use that workspace. Update authoritative SQL predicates to bind both aggregate and workspace, preventing accidental global lookups. Update storage root resolution to partition objects by workspace using canonical path resolution rather than string concatenation. Where Q46 requires workspace identity in Merkle hashing, add it at the canonical receipt serialization boundary and ensure the change is deterministic. Add a hostile test matrix: valid workspace A, missing header, valid principal with workspace B, aggregate ID collision across A/B, and path alias/traversal attempts. Verify error behavior does not leak cross-workspace existence unnecessarily. Keep the change within security fencing; do not refactor the whole auth stack.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Proof must exercise API, database, and storage boundaries. A positive test should retrieve and mutate only a resource in the authorized workspace. Negative proof must show cross-workspace read and write fail closed even when the attacker knows the aggregate ID. Include an equivalent storage-path test. If Merkle identity is changed, verify that two otherwise identical receipts from different workspaces produce distinct canonical hashes and that verifier behavior respects the workspace field. False-proof countercase: hiding another workspace’s record in a UI list while a direct API query still returns it. Reject. Evidence must name the tested principal/workspace combinations and database/storage environment. This mandate proves fencing, not general application security.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop on any authoritative workspace-source ambiguity, data rows with no safe workspace ownership, or a migration that would require ungoverned historical reattribution. Stop after cross-layer proof; do not implement sandboxing or registry changes.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Rollback application predicates and middleware through an isolated commit. Preserve historical records. If a schema migration added workspace keys, follow migration conventions and do not erase populated attribution. Quarantine ambiguous legacy records rather than moving them silently. Security regressions discovered during testing must block promotion until resolved.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M047` based on proof that workspace identity is enforced consistently at API, database, storage, and applicable receipt/hash boundaries, with cross-workspace access failing closed.

## 13. 200–300 word activation prompt

Execute `CA-M047` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q46 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, `api/routers/programs.py`, state-runtime persistence/storage code, workspace/auth helpers, and relevant tests. Implement `INV-TEN-001`: workspace isolation must be enforced at API, database, storage, and required cryptographic identity boundaries. Scope is mandatory workspace context/fencing, composite `(aggregate_id, workspace_id)` predicates, partitioned storage roots, and workspace inclusion in the existing Merkle/receipt identity where explicitly required. Do not rely on UI filtering, client IDs, default-workspace fallbacks, or a late “check workspace” after a global query. Prove positive same-workspace access, missing/mismatched workspace rejection, cross-workspace read/write rejection, aggregate-ID collision isolation, and storage path separation. Reject the false proof where the UI hides another tenant but direct API access still succeeds. Record principal/workspace combinations, exact tests, evidence classes, and limitations. Stop on legacy records without safe ownership or an ungoverned migration requirement. Completion requires changed files, executable security evidence, control-state update, commit SHA, and the Operator decision request: approve or reject `CA-M047`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

