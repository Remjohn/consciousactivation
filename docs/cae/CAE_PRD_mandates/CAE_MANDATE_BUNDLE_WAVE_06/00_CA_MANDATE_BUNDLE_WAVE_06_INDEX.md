# CAE Mandate Bundle — Wave 06

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_06`  
**Scope:** Canonical Questions **Q41–Q48**  
**Mandates:** `CA-M042` through `CA-M049`  
**Status:** `EXECUTION READY — bounded mandate bundle`  
**Prepared:** `2026-09-06`

## 1. Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. `docs/cae/cae_mandate_bundle/02_CA_GEMINI_MANDATE_EXECUTION_SKILL.md`
3. `docs/cae/cae_master_57_question_convergence_canon.md` and Q41–Q48 decision text
4. `docs/cae/Architecture.md`
5. `docs/cae/UI.md`
6. `Context Chat/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md`
7. `Context Chat/ChatGPT-Assess PRD Implementation Readiness-20260906-1534.md`
8. Wave 01, Wave 02, and Wave 04 mandate bundles present in the working context
9. The Q41–Q48 physical implementation surfaces and their direct tests

The authoring protocol is normative for the 13-section mandate grammar, authority separation, state grammar, anti-centroid controls, activation prompts, parallelism, evidence, and stop behavior. Runtime authority remains the canonical runtime; mandate prose never becomes runtime authority.

## 2. Wave 06 objective

Wave 06 establishes the **state-concurrency → cryptographic lineage → forensic replay → fault recovery → operator preemption → tenant fencing → sandbox enforcement → registry immutability** tranche. It hardens the vertical execution spine beginning at Q41 and carries its security/integrity guarantees through Q48.

Canonical sequence:

```text
Q41 Atomic SQLite CAS
        ↓
Q42 Parent-linked receipt hashes
        ↓
Q43 Persisted replay parity
        ↓
Q44 Expired lease reconciliation
        ↓
Q45 Real operator preemption
        ↓
Q46 Workspace isolation
        ↓
Q47 Tool/path sandbox hardening
        ↓
Q48 Program registry immutability + manifest pinning
```

The key boundary is that each later mandate consumes the prior proof without acquiring permission to rewrite it. Q41 owns atomic state mutation. Q42 owns durable receipt lineage. Q43 owns read-only forensic replay. Q44 owns startup recovery from expired leases. Q45 owns real operator abort. Q46 owns tenant/workspace fencing. Q47 owns tool/path execution containment. Q48 owns registry release immutability and exact package/manifest pinning.

## 3. Mandate map

| File | Mandate ID | Canon | Mandate | Primary surface | Dependency |
|---|---|---:|---|---|---|
| `02_CA_MANDATE_042.md` | `CA-M042` | Q41 | Atomic CAS State Transitions in SQLite | `program_state_runtime.py; SQLite state schema/tests` | Q34–Q40 |
| `03_CA_MANDATE_043.md` | `CA-M043` | Q42 | Cryptographic Merkle Receipt Chaining | `program_state_runtime.py; transition schema/migrations` | Q41 |
| `04_CA_MANDATE_044.md` | `CA-M044` | Q43 | Persisted Replay Verification Engine | `program_state_runtime.py; replay tests` | Q41–Q42 |
| `05_CA_MANDATE_045.md` | `CA-M045` | Q44 | Worker Restart and Zombie Lease Reconciliation | `api/main.py; state runtime; lease schema/tests` | Q34–Q41 |
| `06_CA_MANDATE_046.md` | `CA-M046` | Q45 | Real Operator Control and Preemption | `program_operator_runtime.py; programs router; cancellation path` | Q34–Q44 |
| `07_CA_MANDATE_047.md` | `CA-M047` | Q46 | Multi-Tenant Workspace Isolation | `programs router; state runtime; storage roots` | Q34–Q45 |
| `08_CA_MANDATE_048.md` | `CA-M048` | Q47 | Path Traversal and Tool Sandbox Hardening | `agent_invocation.py; tool runner; sandbox helpers` | Q36–Q46 |
| `09_CA_MANDATE_049.md` | `CA-M049` | Q48 | Program Registry Immutability and Manifest Pinning | `program_registry.py; state initialization; registry schema` | Q24–Q30, Q34, Q46 |

## 4. Inherited architecture contracts

Wave 06 executors must preserve these already-ratified laws: role precedes schema; evidence precedes inference; semantic definitions are versioned; operational state is dynamic; evidence is immutable; derived artifacts are reproducible; the API is the canonical boundary; runtime state is authoritative; typed semantic operations are preferred over arbitrary writes; UI is projection/control rather than authority; a score is not evidence; and automated tests must be declared with their real fidelity.

For Q41–Q45, the dominant concern is **state integrity under concurrency and failure**. For Q46–Q48, the dominant concern is **security and immutable execution identity**. No Wave 06 mandate may weaken an earlier constitutional invariant to obtain a convenient happy path.

## 5. Wave-level false-proof suite

The eight mandates collectively must reject at least these plausible but invalid results:

1. a Python mutex that appears to serialize writes but fails across worker processes;
2. receipt hashes computed from an in-memory object rather than persisted canonical payload;
3. replay that reconstructs current memory instead of reopening durable history;
4. a startup routine that directly sets `PAUSED` without exercising the authoritative transition path;
5. an abort endpoint that changes a row to `CANCELLED` while active work continues;
6. a UI that hides another tenant while the API still permits direct access;
7. a sandbox helper that passes while a separate production bypass still executes tools;
8. an in-memory registry that rejects overwrites while the persistent registry permits them.

## 6. Parallelism and integration ownership

Read-only repository inspection and test discovery may be parallelized. Shared state schema, receipt schema, migration, workspace predicates, security middleware, registry status, and other authority-bearing changes require one integration owner. Q41 and Q42 must not introduce conflicting state/receipt migrations. Q46 security changes must preserve Q41/Q42 workspace predicates and cryptographic lineage. Q48 may consume release/policy identifiers from prior waves but may not silently alter release authority.

## 7. Control-state / execution rule

Every mandate follows:

`LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE WITHIN FILE BOUNDARY → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → REQUEST OPERATOR DECISION → STOP`

Each mandate contains its own 200–300 word activation prompt. The activation prompt is a compact execution key and never expands the mandate authority.

## 8. Completion

Wave 06 is complete only when CA-M042 through CA-M049 independently satisfy their declared proof standards, limitations are recorded, control state is updated, exact commit SHAs are captured by their executors, and the Operator explicitly closes the wave. Completion of Q41–Q48 does not authorize Q49 onward.

## 9. Naming

Wave 06 continues the bundle naming sequence established by Waves 01, 02, and 04: Q41–Q48 are authored as `CA-M042` through `CA-M049`, with filenames `CA_MANDATE_042` through `CA_MANDATE_049`. This keeps bundle execution IDs distinct from the canonical question numbers while preserving continuity.
