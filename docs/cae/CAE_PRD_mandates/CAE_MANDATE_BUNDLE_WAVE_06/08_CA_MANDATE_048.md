# CA-M048 — Path Traversal and Tool Sandbox Hardening

## 1. Identity and status

- **Mandate ID:** `CA-M048`
- **Canonical question:** `Q47`
- **Wave:** `06`
- **Status:** `EXECUTION READY — bounded mandate`
- **Primary requirement/invariant:** `INV-SAND-001`
- **Collision primitive:** `COSTLY EXPOSURE`
- **Dependency set:** Q36 context projection; Q37 live invocation; Q46 workspace fencing
- **Primary physical surfaces:** `packages/ca_runtime/src/ca_runtime/agent_invocation.py; tool registry/runner; sandbox path helpers; security tests`
- **Authority chain:** `LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → OPERATOR DECISION → STOP`

## 2. Decision / objective being authorized

Harden the execution sandbox so tools cannot access paths outside the declared workspace roots and system RPC execution is limited to explicitly allowed binaries without shell interpretation. The known defect class is the permissive `tool:default-` bypass in agent invocation that allowed unverified tool calls. The objective is to establish one canonical path-resolution predicate and one explicit execution policy at the runtime boundary. The implementation must demonstrate that path aliases, `..` traversal, symlink tricks where relevant to the existing environment, absolute paths, and unregistered tools are rejected or safely contained according to the current policy.

This mandate is an execution contract, not a descriptive essay. It authorizes only this Q-specific change and its direct proof. The executor must not reinterpret the appearance of adjacent defects as permission to widen the mandate.

## 3. Governing doctrine and authority sources

Semantic authority comes from Q47 and architecture security doctrine. Runtime authority is the agent invocation/tool execution boundary and the declared workspace roots associated with the execution. A tool name supplied by a model is not permission. A path that happens to exist under the process user’s permissions is not permission. The executor must reuse existing `assert_sandboxed_path` or equivalent canonical resolver where available. Change authority remains operator-governed. Shell execution is explicitly prohibited by the decision; if an existing tool absolutely requires a shell, the correct action is to classify that incompatibility rather than silently restoring a bypass.

Primary references are:
1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md` — normative mandate grammar, evidence, anti-centroid, activation, parallelism, and stop behavior.
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md` — agent execution sequence, failure classes, evidence discipline, and stop behavior.
3. `docs/cae/cae_master_57_question_convergence_canon.md` — Master 57-question decision canon, including `Q47`.
4. `docs/cae/Architecture.md` and `docs/cae/UI.md` — canonical architecture and operator/UI boundaries.
5. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` — ratified Q-specific decision and physical code references.
6. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` — implementation-readiness analysis and known repository reality.

## 4. Mandatory reading before action

Before editing, the executor MUST read the complete contents, not excerpts, of:

- `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
- `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
- `docs/cae/cae_master_57_question_convergence_canon.md` and the complete decision text for `Q47`
- `docs/cae/Architecture.md`
- `docs/cae/UI.md`
- `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md` and the `Q47` section
- `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md` for the current implementation/readiness assessment
- `packages/ca_runtime/src/ca_runtime/agent_invocation.py; tool registry/runner; sandbox path helpers; security tests`
- Q47 decision; `agent_invocation.py`; tool registry/dispatch code; path resolution helpers; OS-level test fixtures; architecture sandbox sections; current security tests.

The executor must inspect current repository reality before making any implementation claim. Historical “verified” language is not proof until the current executable path is inspected.

## 5. Exact scope

**Objective.** Implement and prove only `CA-M048` / `Q47` as defined by the ratified canon and the physical surfaces named above.

Implement only the sandbox hardening boundary: remove/disable the unverified default-tool bypass; enforce canonical workspace-root path resolution; restrict system RPC to explicit whitelisted binaries; enforce `shell=False`; and add focused positive/negative tests. Inputs are tool requests, declared tool definitions, workspace roots, paths, and RPC executable identifiers. Outputs are permitted tool calls or fail-closed security errors. Validators must cover nested allowed path, traversal attempt, absolute external path, symlink/alias case where supported, unregistered tool, forbidden binary, and shell metacharacters. Operators allowed are executor and Operator.

**State grammar.** Where the mandate changes authoritative state, the executor must explicitly record `source state → operation → target state`, actor, preconditions, validators, postconditions, receipt/evidence, error route, and recovery path in the completion record.

## 6. Allowed artifacts and file boundary

Allowed changes are limited to `packages/ca_runtime/src/ca_runtime/agent_invocation.py; tool registry/runner; sandbox path helpers; security tests`, their direct tests, and the minimum supporting schema/migration/helper/API change required to make the decision executable. New files are allowed only when they are the smallest direct implementation or proof artifact. Reuse existing runtime objects, receipts, schemas, migrations, security helpers, and registries whenever semantically compatible. Shared migrations and authoritative state changes have one integration owner. Read-only inspection may be parallelized; conflicting writes may not.

## 7. Prohibitions and collision procedure

Do not whitelist the operating system root, current working directory, or a broad parent folder “temporarily.” Do not restore `tool:default-`. Do not use string prefix checks as the sole path containment test. Do not allow shell interpolation, command concatenation, or a hidden shell fallback. Do not turn a failed security test into a pass by excluding the adversarial fixture. Do not redesign the entire tool system. Do not treat model-generated tool metadata as authoritative policy. If a legitimate existing program depends on a currently forbidden capability, record the compatibility collision and stop rather than weakening the invariant.

**Collision procedure.** If a collision appears with an existing invariant, authority source, schema, migration, receipt, state machine, workspace rule, or security boundary: (1) stop before the conflicting edit; (2) identify the controlling source; (3) classify the collision as implementation defect, stale documentation, dependency gap, or `OPERATOR_DECISION_REQUIRED`; (4) make the minimum correction only if this mandate clearly owns it; otherwise record the collision and stop. The executor must not silently resolve ambiguity by choosing the easiest implementation.

## 8. Required work / implementation behavior

Trace every tool invocation entry point from model output through registry lookup, path validation, and process/RPC launch. Remove the bypass that permits unverified tool classes to execute. Establish or reuse a canonical root-resolution helper that resolves the requested path and compares it against the allowed workspace roots using filesystem-aware semantics appropriate to the repository. Verify that the normalized result remains within an approved root. Enforce explicit tool registry membership and executable allowlist. Pass argument arrays directly with `shell=False`. Add adversarial tests that use known escape patterns, alternate separators where relevant, absolute paths, `..` segments, and symlink fixtures if the platform permits deterministic tests. Validate that allowed files still work and that an unregistered tool is rejected before execution. Keep all changes within the invocation and sandbox boundary.

The executor must separate facts, hypotheses, and Operator decisions in the working record. A test that proves a local helper but bypasses the canonical authority boundary must be labeled insufficient rather than promoted to success.

## 9. Verification and evidence standard

Required evidence is executable at the actual invocation layer. Positive proof must show an allowed tool/path executes successfully. Negative proof must show traversal, out-of-root access, unregistered tool, forbidden binary, and shell-injection-shaped arguments are rejected before execution. The verifier measures sandbox enforcement and execution policy; it does not prove kernel/container isolation or every OS-specific filesystem corner case. False-proof countercase: a unit test that calls `assert_sandboxed_path()` correctly while the production tool runner still has a separate bypass path. Reject. Environment fidelity requires testing the real runner/dispatcher path for at least one representative invocation. Operator validation is required for known tool compatibility gaps.

Every material claim must carry an evidence class selected from `EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, or `OPERATOR_DECISION_REQUIRED`. Record exact commands, environment, fixture class, result, and limitation. Do not claim `VERIFIED` solely from prose, snapshots, mocks, or a green test suite whose fidelity is weaker than the invariant.

## 10. Completion and stop condition

Stop on any remaining bypass path, ambiguous workspace root, or legitimate dependency that requires forbidden shell behavior without an explicit authority decision. Stop after Q47 security evidence; do not modify program registry or economics.

Completion additionally requires the requested artifact/behavior to exist, its proof standard to pass, limitations to be recorded, the control-state record to be updated if one exists, and the exact commit SHA to be captured. After that, ask the Operator decision below and stop. The executor must not begin the next canonical question automatically.

## 11. Rollback / recovery

Rollback only the bounded sandbox changes. Preserve failed-security evidence and test cases. Do not restore the removed bypass merely to recover convenience without an Operator decision. If a legitimate tool stops working, either adapt it through the declared tool boundary or record the incompatibility; do not bypass the sandbox.

## 12. Operator decision

The completion report must include changed files, exact tests/commands, evidence classes and locators, the mandate-specific false-proof result, residual limitations, control-state impact, and exact commit SHA.

**Requested decision:** Approve or reject `CA-M048` based on executable proof that tool/path execution is confined to declared workspace roots and system RPC is restricted to explicit allowlisted binaries with shell interpretation disabled.

## 13. 200–300 word activation prompt

Execute `CA-M048` only. Read the Mandate Authoring Protocol, Gemini execution skill, Q47 in the Master Canon and convergence ledger, `docs/cae/Architecture.md`, `packages/ca_runtime/src/ca_runtime/agent_invocation.py`, tool registry/runner code, sandbox helpers, and security tests. Implement `INV-SAND-001`: remove the unverified `tool:default-` bypass, enforce canonical sandbox path resolution against declared workspace roots, restrict system RPC to explicit allowlisted binaries, and use `shell=False`. Scope is the tool invocation/security boundary and focused tests. Do not redesign the tool system, add broad filesystem permissions, restore shell fallback, or implement Q48 or later questions. Prove an allowed invocation succeeds and adversarial cases fail: `..` traversal, absolute out-of-root path, alias/symlink case where supported, unregistered tool, forbidden binary, and shell-injection-shaped arguments. Reject the false proof where the helper is tested but production has another bypass path; exercise the real runner/dispatcher. Record OS/environment fidelity and limitations. Stop on any unresolved bypass or dependency requiring a prohibited shell behavior. Completion requires changed files, exact executable evidence, evidence classes, false-proof result, control-state update, commit SHA, and the Operator decision request: approve or reject `CA-M048`. Before changing any file, distinguish observed repository facts from assumptions, preserve existing canonical identifiers and migration ownership, and make every negative result explicit. Report exactly what was inspected, what was changed, what was not changed, and which proof remains unavailable. Never turn an implementation convenience into a new architectural authority.

