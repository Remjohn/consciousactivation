# CA-M049 — Program Registry Immutability and Manifest Pinning

## 1. Identity and status

- **Mandate ID:** `CA-M049`
- **Canonical question:** `Q48`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-REG-001`
- **Collision primitive:** `LATENT PATTERN ARTICULATION`
- **Dependency set:** Q24–Q30 governance/release contracts; Q34 execution dispatch; Q46 workspace identity as applicable
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_registry.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; registry/aggregate schema; release/initialization tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement registry immutability and manifest pinning so a released program package cannot be overwritten under the same identity and version. The execution aggregate must retain `manifest_sha256` and `package_sha256` (or the already-canonical equivalents) sufficient to prove that the bytes used by an execution match the released package identity. The purpose is to prevent silent drift between what was approved/released and what a later run resolves from the program registry. A registry update is therefore a versioned promotion operation, not an overwrite-in-place convenience.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority is Q48 and the Master Canon. Runtime authority is the program registry plus the execution initialization path that resolves a program. Release/registry authority is distinct from filesystem or Git working-tree state; a package existing on disk is not automatically an authorized release. The executor must bind initialization to a `RELEASED` status or equivalent canonical gate as ratified. Change/promotion authority remains Operator-controlled. The system must preserve the distinction between source package revision, released package identity, and active execution binding. If a package digest changes, the correct semantic action is a new version/release, not silent replacement.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q48`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q48`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q48` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/program_registry.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; registry/aggregate schema; release/initialization tests`
- Q48 decision; `program_registry.py`; program-state initialization; registry schema/migrations; program manifests; release manifest and initialization tests; current registry status enum/transition logic.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M049` / `Q48` as defined by the ratified canon and the physical surfaces named above.

Implement registry immutability and pinning only: required manifest/package digest columns; release-status gating during initialization; overwrite rejection without version increment; durable binding of the resolved digests to execution state; and positive/negative tests. Inputs are a program package, version, manifest, package bytes/digest, registry status, and initialization request. Outputs are either a valid immutable release registration/binding or a deterministic rejection. Operators allowed are executor and Operator. Validators must prove initial registration, released initialization, same-version overwrite rejection, changed-version acceptance, digest mismatch detection, and execution pinning.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/program_registry.py; packages/ca_runtime/src/ca_runtime/program_state_runtime.py; registry/aggregate schema; release/initialization tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not allow a released package to be overwritten because the name/version matches. Do not treat a filesystem modification time as package identity. Do not recompute a digest at execution and silently accept a mismatch against a stored released digest. Do not auto-bump versions without an explicit governed operation. Do not mutate historical execution bindings. Do not create a second registry just for immutability. Do not rewrite release manifests or Q29 artifacts unless this mandate’s direct registry binding requires a narrowly bounded compatibility change. Do not claim immutability because a Python dictionary resists mutation during one process; the durable registry must enforce it.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace registration, release, initialization, and execution aggregate creation. Add the minimal durable digest fields and/or use existing fields where present. Enforce a registry rule that a `RELEASED` package identity cannot be replaced without a version increment or new identity. Make initialization reject a released record whose current package/manifest digest does not match the pinned values. Bind the exact resolved `manifest_sha256` and `package_sha256` to the execution aggregate so later verification can prove what was actually used. Add tests for first registration, release, attempted overwrite, new version registration, digest mismatch, and two runs against the same released version. Inspect filesystem/package loading to ensure the digest being pinned is computed from the same canonical bytes that execution consumes. Keep this work within registry integrity; do not implement the later DAG, economics, benchmarking, telemetry, or release-seal questions.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Evidence must reach the real registry and initialization boundary. Positive proof: register/release a package, initialize an execution, and verify stored pins equal the exact bytes resolved by the runner. Negative proof: mutate the package under the same version and show initialization/re-registration fails closed; also attempt a manifest/package digest mismatch and show rejection. Another proof must show a new version can be registered without modifying the old release. False-proof countercase: protecting an in-memory registry object with a Python setter while the persistence layer still permits overwrite. Reject. The verifier measures durable registry immutability and execution pinning; it does not prove the artifact is globally immutable across every deployment filesystem. Operator validation is required for any legacy-version migration policy.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop on a registry authority collision, inability to distinguish released from mutable states, or legacy packages with unknown byte identity that would require ungoverned backfill. Stop after proving Q48 and updating control state; this mandate does not authorize Q49.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Use isolated schema/runtime commits and the project migration conventions. Preserve released package records and execution pins. If a new pinning field cannot be populated safely for legacy rows, leave them explicitly unverified and record the limitation rather than inventing hashes from changing files. Never rewrite historical execution bindings to match a mutated package.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M049` based on proof that released program packages are immutable by identity/version and that executions are pinned to exact manifest/package digests at the canonical registry/initialization boundary.

## 13. 200–300 word activation prompt

Execute `CA-M049` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q48 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, `packages/ca_runtime/src/ca_runtime/program_registry.py`, program-state initialization, registry schema/migrations, program manifests, and release/initialization tests. Implement `INV-REG-001`: released program packages are immutable, same-version overwrite is prohibited, and execution initialization is pinned to exact `manifest_sha256` and `package_sha256` values. Scope is registry schema/status gating, immutable registration behavior, digest computation/binding, and focused verification. Do not create a parallel registry, auto-bump versions, mutate historical execution bindings, or implement Q49–Q57. Prove first registration/release, successful execution initialization with exact pin equality, same-version overwrite rejection after real byte mutation, digest mismatch rejection, and new-version registration without altering the old release. Reject the false proof where only an in-memory dictionary is protected while persistence remains mutable. Exercise the real registry and package-loading path. Record exact commands, bytes/digests inspected, evidence classes, limitations, and control-state impact. Stop on legacy package identity gaps requiring an ungoverned migration. Completion requires changed files, executable proof, commit SHA, and the Operator decision request: approve or reject `CA-M049`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

