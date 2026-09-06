# CA-M043 — Cryptographic Merkle Receipt Chaining

## 1. Identity and status

- **Mandate ID:** `CA-M043`
- **Canonical question:** `Q42`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-MERK-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q41 atomic state transition semantics; existing transition receipt model
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; cae_program_state_transitions schema/migrations; receipt hashing helpers/tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Implement the ratified cryptographic receipt-chain contract so that each persisted state transition carries a canonical receipt payload digest and an explicit parent receipt digest linking it to its immediate predecessor. The goal is tamper evidence and deterministic lineage, not merely adding three columns to a table. The chain must be constructed from a canonical serialization that is stable across replay and verification, and each transition must preserve the causal order already represented by the state machine. The resulting chain must make it possible to detect a missing predecessor, mutated payload, altered parent pointer, or reordered transition sequence. The implementation must remain compatible with Q41’s atomic transition semantics: a receipt for a rejected CAS must not be persisted as though the transition occurred.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Meaning is governed by the Q42 decision and the Master Canon. Runtime authority is the canonical transition ledger and state-runtime receipt path. Cryptographic authority is the exact canonical serialization and hashing function chosen within the existing CAE receipt model; the executor may implement that function only where the decision provides sufficient definition, and must stop when a materially undefined serialization choice would become a new architecture decision. Promotion authority remains the Operator. A simple hash chain is not automatically a full Merkle tree; for this mandate, the project decision specifically requires predecessor-linked `parent_receipt_sha256` and payload/receipt digests. The executor must distinguish that concrete contract from any broader tree or DAG claim.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q42`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q42`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q42` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; cae_program_state_transitions schema/migrations; receipt hashing helpers/tests`
- Q42 decision in ledger; architecture receipt/replay sections; existing transition schema/helpers; any current receipt examples, tests, or serialization utilities; current migrations.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M043` / `Q42` as defined by the ratified canon and the physical surfaces named above.

Implement only the persisted transition receipt chain: schema/migration fields `parent_receipt_sha256`, `receipt_sha256`, and `receipt_payload` where absent; canonical payload serialization; digest construction; parent lookup; durable persistence; validation helpers; and tests proving chain integrity. Inputs are one accepted state transition and the prior committed receipt context. Outputs are an immutable transition receipt with exact payload and hashes plus verifier evidence. Operators allowed are executor and Operator. Validators must test first-transition root behavior, child-parent linkage, deterministic re-hashing, tampered payload detection, tampered parent detection, and chain break detection. Existing state transition ordering and Q41 CAS semantics are dependencies, not permission to rewrite them.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/program_state_runtime.py; cae_program_state_transitions schema/migrations; receipt hashing helpers/tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not replace the project’s transition model with a blockchain, external ledger, or new cryptographic service. Do not call a hash “Merkle” merely because it is SHA-256. Do not silently choose mutable timestamps, unordered dictionaries, process IDs, or environment-specific values in canonical serialization unless the existing contract explicitly requires them; unstable inputs destroy replay parity. Do not retroactively rewrite old receipts to make them appear chained. Do not permit a child receipt to claim a parent that does not exist or belongs to another execution/workspace. Do not weaken verification to ignore a digest mismatch. Do not include secret material in receipt payloads merely to make provenance stronger. If the repository lacks a ratified serialization rule necessary for deterministic hashing, stop and classify the gap instead of inventing a novel rule without an authority decision.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace the current transition persistence path and identify when a successful transition becomes durable. Define the canonical receipt payload from existing state-transition fields plus only the data required by the Q42 contract. Serialize deterministically using the project’s existing serialization conventions where possible. Compute `receipt_sha256` over the canonical payload representation, set `parent_receipt_sha256` to the prior receipt digest for the same execution chain, and persist the exact payload used for verification. Establish the root condition explicitly for the first transition. Add validators that recompute the digest from stored payload, verify the stored parent exists and is the immediate predecessor, detect gaps and branch anomalies, and reject workspace/execution identity mismatches. Ensure failure paths do not write phantom receipts. Add migration tests and backward-compatibility handling for legacy rows only if the repository already requires it; do not fabricate historical parent hashes. Provide a focused verifier command or test entry point that can be rerun against persisted data. Record whether the project’s implementation is a predecessor-linked hash chain or a broader Merkle structure; do not overclaim.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Proof must include schema/migration evidence and executable cryptographic verification. At least one positive run must create a multi-transition chain and independently recompute every digest. Negative tests must mutate payload bytes, parent digest, or transition ordering and prove verification fails. Another negative case must delete a predecessor row or point to a receipt from another execution/workspace and show chain rejection. The verifier must state that it measures deterministic digest linkage and tamper detection, not collision resistance beyond the chosen hash function or a generalized DAG invariant. False-proof countercase: a test that hashes an in-memory Python object before persistence and then compares the same object to itself; that proves almost nothing about canonical persisted serialization and must be rejected. Environment-fidelity requires reading the values back from SQLite. Operator validation is required if canonical serialization changes the long-term receipt contract.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop on undefined canonical serialization that would require an unratified semantic choice, on migration conflicts, on pre-existing receipts whose authority cannot be established, or when a digest verification failure cannot be classified. Stop after proving Q42 and recording the exact chain behavior; do not implement replay or recovery automatically.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Rollback by isolated migration/commit reversal where supported, while preserving any created evidence in disposable fixtures. Never edit historical production receipts in place. If a migration is forward-only, retain the old reader only as long as repository conventions permit and record the compatibility limitation. Any partially migrated durable data must be handled through the project’s existing migration recovery path. If recovery would require generating historical hashes, stop for Operator decision.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M043` based on whether the stored transition ledger has deterministic parent-linked receipt hashes and executable tamper detection at the real persistence boundary.

## 13. 200–300 word activation prompt

Execute `CA-M043` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q42 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, and the current transition schema/migrations, receipt helpers, and `program_state_runtime.py`. Implement `INV-MERK-001`: every accepted state transition must persist a canonical receipt payload, `receipt_sha256`, and `parent_receipt_sha256` linking to its immediate predecessor. Scope is receipt schema/migration, deterministic serialization, hash construction, parent linkage, verification, and focused tests. Do not implement Q43 replay, Q44 reconciliation, Q45 preemption, or unrelated cryptographic infrastructure. Reuse existing CAE receipt conventions; do not call a simple hash chain a broader Merkle DAG. Prove a multi-transition positive chain by rereading persisted rows and recomputing every digest. Prove negative cases for mutated payload, mutated parent hash, missing predecessor, and cross-execution/workspace linkage. Reject in-memory self-comparisons as proof. Record evidence classes, exact commands, environment, and the limitation that hashing does not by itself prove every replay property. Stop if canonical serialization is materially underspecified and would require a new architectural decision. Completion requires changed files, schema/migration evidence, executable verifier output, limitations, control-state update, commit SHA, and the Operator decision request: approve or reject `CA-M043`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

