# Atomic Harness Builder independent engineering QA audit

Audit date: 2026-07-16  
Audited snapshot: `D:\Work\CONSCIOUS_ACTIVATIONS\_PARALLEL\BUILDER_QA_SNAPSHOT`  
Governed `PYTHONPATH`: `src;.`  
Verdict: **FAIL_P0_OR_P1**

## Executive result

The synthetic Builder Core is not independently trustworthy in this snapshot, regardless of its existing Story Completion Receipts.

The decisive failure is `BQA-P0-001`: an `AtomicHarnessDefinition` can have its task, goal, success condition, input/output contracts, evaluation requirements, repair policy, compatibility claim, authority identity, and governed section evidence rewritten; after recomputing its hash, the production domain validator accepts it and a new receipt can be issued. ST-07.04 target validation then attests to the altered object by self-consistency rather than reconstructing its meaning from governed authority.

Five P1 findings independently block completion: the governed suite fails in both fresh runs and ST-07.04 has no governed tests; post-commit observation failure returns failure despite a committed result; the in-memory optimistic-concurrency check loses one of two accepted writes; run lifecycle state and its receipt-bearing command record are not atomic; and ZIP identity can bind the hash of one archive to the members of another.

Finding count: **1 P0, 5 P1, 3 P2, 1 P3**.

## Scope and isolation

The canonical Builder repository was copied before audit. Source and target copy counts were both 997 files. All execution, inspection, and reproduction work used the snapshot. No product code or Story implementation was changed. Reports were written only under `_PARALLEL_REPORTS`.

The audit evaluated the code and governed inputs present in the snapshot. It did not infer completion from Story Completion Receipts, and it did not broaden the synthetic Story scope into future Builder product behavior.

## Required execution results

### Full governed suite

Command, executed twice in fresh processes:

```powershell
$env:PYTHONPATH='src;.'
$env:PYTHONDONTWRITEBYTECODE='1'
python -B -m pytest -q -p no:cacheprovider
```

| Run | Passed | Failed | Warning | Duration | Result |
|---:|---:|---:|---:|---:|---|
| 1 | 422 | 5 | 1 | 58.87 s | FAIL |
| 2 | 422 | 5 | 1 | 51.36 s | FAIL |

The failure set was identical. All five tests reject the two ST-07.04 source modules because duplicated historical exact-source inventories were not updated:

- `src/cmf_builder/application/target_validation_commands.py`
- `src/cmf_builder/domain/target_package_validation.py`

The failing tests are the exact-source architecture tests owned by ST-01.01, ST-01.01 synthetic proof, ST-01.02, ST-02.05, and ST-03.03. The snapshot's ST-07.04 allowlist requires five test modules in addition to `__init__.py`; none exists, and the ST-07.04 completion directory is absent.

### Python compilation

All 158 Python files were compiled in memory using Python's `compile()` without writing bytecode. Result: **158 passed, 0 failed**.

### Determinism and process independence

Two fresh processes compiled and validated the same synthetic target while varying `PYTHONHASHSEED`, `TZ`, `HOME`, and `TEMP`. Both produced byte-identical validation and receipt identities:

- report: `sha256:7cc93b8fcf30ad19aa0476b7a20bf6a897229e7bf59ea04c3fd222709aa1dee3`
- receipt: `sha256:36834498359bd61e8c888f59640b312ebdf542f239a953676239ce0f243c1bea`

The active source contains no direct calls to current time, `random`, `uuid4`, environment lookup, or current-working-directory lookup. Canonical JSON uses sorted keys; mappings are frozen in canonical order; active filesystem traversals are sorted. No mutable list/dict/set function defaults or simple unreachable top-level statements after an unconditional return/raise were found.

This positive result does not cure the P0: deterministic hashing faithfully reproduces an unauthorized rewritten meaning when validation permits that meaning.

### Absolute-path scan

A text scan found 58 Windows absolute-path occurrences across 16 files. Material current examples are:

- `contracts/integration/DELEGATION_CONTRACT_PIN.yaml` contains an absolute `D:/Work/.../1.1.0-rc.4` location;
- `stage1/generate_stage1_evidence.py` has an absolute default source root;
- `stage1/STAGE1_EVIDENCE_SUMMARY.json` serializes absolute PRD and source roots;
- `stage1/ARCHITECTURE_BASELINE_MANIFEST.yaml` serializes local source locations.

Other hits are mostly historical test-command captures, archive-recovery evidence, or test-only path rejection literals. They do not establish release-byte corruption. Current target-validation canonical bytes themselves contain no workspace path.

## Highest-severity findings

### BQA-P0-001 — Definition authority and receipt trust can be self-rewritten

`AtomicHarnessDefinition.validate()` checks upstream IDs and hashes for many structural objects, but it never reconstructs or compares several material semantic fields. It only requires `authority_identity` to be nonblank. It validates each section's shape, then derives `expected_sections` from the candidate's own section IDs; it does not compare each section's evidence mapping and basis to the governed source map.

A controlled reproduction changed:

- task, goal, and success condition;
- input and output contracts;
- evaluation requirements;
- repair/retry policy;
- compatibility status to `production_ready`;
- authority identity to `unratified-actor`;
- one required section's source evidence to `invented-local-authority` with basis `ungoverned`.

After recomputing the canonical identity, domain validation returned `ACCEPTED`, and `AtomicHarnessDefinitionReceipt.create()` issued receipt `atomic-harness-definition-receipt_d2c0b9c30ad222df70be9a1ff0589a95dddc92eb80545decb399004c6cf27fa7`.

ST-07.04 compounds this: `AtomicContentHarnessValidationReport.create()` creates PASS dimensions with declarations such as `complete_authoritative_lineage_reproduced` and `all_target_specific_gates_passed`, but its validator compares hashes and references to the same candidate definition rather than independently validating the definition against upstream governed inputs.

Correction belongs to **ST-07.04**: reconstruct every semantic field and section mapping from the pinned definition input/upstream artifacts, validate the ratified authority identity, and mutation-test each field before a target-validation receipt can be issued.

### BQA-P1-002 — Governed regression state and ST-07.04 evidence are incomplete

The full suite fails identically twice. Independent AST analysis shows 43 internal source files, zero external imports, and zero domain/application/adapter layer violations: the new modules are architecturally internal, but five copied exact-file lists reject them.

This is more than test maintenance because the new ST-07.04 path has zero of its five governed test modules and no completion evidence. The current validator is therefore unprotected precisely where the P0 and post-commit ambiguity occur.

Correction belongs to **ST-07.04**.

### BQA-P1-003 — Post-commit observation ambiguity

The target-validation service commits run event, report, receipt, and command record, then emits observations. Injecting a failing observation sink caused:

- caller-visible `RuntimeError: observation_sink_unavailable`;
- stream version 24 and active validation reference persisted;
- one report, one receipt, and the command record persisted;
- a second failed observation attempt from the catch block, marked as if not committed.

This needs an atomic outbox or a typed post-commit telemetry state. Correction belongs to **ST-07.04**.

### BQA-P1-004 — Lost update under optimistic concurrency

`InMemoryRunRepository._validated_append()` checks the current tuple and returns it; the caller assigns the enlarged tuple later without synchronization. With a barrier between those steps, two writers at expected version 2 both returned success, but only `evt-a` remained in the three-event stream and `evt-b` was lost.

Correction belongs to **later productization**: the expected-version compare and write must be one atomic operation.

### BQA-P1-005 — Run state and receipt-bearing record are not atomic

Run lifecycle commands call `append()`, construct a receipt, then call `save_command_record()`; checkpoint creation inserts another separate write. Injecting command-record storage failure during `create_run()` raised to the caller but left a run with `RunCreated` and `TargetProfileSelected` events and no command record. This creates authoritative state without the corresponding idempotent receipt surface.

Later Story repository commits correctly group their artifacts, receipts, command record, and events behind prevalidation and a failure guard. The original run-command path has not adopted that model. Correction belongs to **later productization**.

### BQA-P1-006 — ZIP hash/member split-read

`diagnose()` reads and hashes ZIP bytes, then `_scan_zip()` reopens the path. A controlled swap between those operations was accepted: the reported hash was archive A's `f10cc7...`, while the actual archive during member scan was B's `6640e6...`, and the accepted descriptor was `second.txt` from B.

Correction belongs to **later productization**: hash and inspect one immutable byte sequence or file handle.

## Remaining findings

| ID | Severity | Finding | Owner |
|---|---|---|---|
| BQA-P2-007 | P2 | `add_checkpoint()` silently overwrites a prior checkpoint with the same ID; corruption fallback works, but the original checkpoint record is lost. | later productization |
| BQA-P2-008 | P2 | Five repeated exact-source inventories protect import/layer rules but also create repetitive maintenance stops for legitimate modules. | later productization |
| BQA-P2-009 | P2 | Active integration configuration and generated Stage 1 evidence contain absolute machine paths. | later productization |
| BQA-P3-010 | P3 | `pytest-asyncio` loop-scope behavior is not explicitly configured. | later productization |

No finding was assigned to ST-11.01. The audited defects either belong to the incomplete ST-07.04 target-validation boundary or to later repository/productization work.

## Invariant assessment

| Audit dimension | Result | Evidence |
|---|---|---|
| Domain-model correctness | FAIL | Definition meaning and section evidence can be rewritten and receipted (`BQA-P0-001`). |
| Command and authority boundaries | FAIL | Authority identity is only nonblank-checked in definition/target validation. |
| Deterministic serialization and hashing | PASS in isolation | Stable across fresh process hash seed, timezone, home, and temp variation. |
| Replay and idempotency | PASS for target validation | Same payload returned the same receipt at version 24; changed payload under the same ID raised `IdempotencyPayloadMismatch`. |
| Optimistic concurrency | FAIL | Two accepted writers, one stored event (`BQA-P1-004`). |
| Atomic commit and rollback | MIXED/FAIL | Later aggregate commits prevalidate atomically; run lifecycle writes do not (`BQA-P1-005`). |
| Invalidation propagation | PASS | Authorized reopen emitted 14 invalidations, including ST-07.04 validation; all descendants became unusable. |
| Historical reproducibility | CONCERN | Invalidated target history remains reproducible, but checkpoint identities can be overwritten. |
| Unsafe path/archive handling | FAIL | Path traversal and ZIP member safety are strong; archive identity has a split-read race (`BQA-P1-006`). |
| Portability | CONCERN | Canonical target output is path-free; active pins/generators and generated evidence leak absolute paths. |
| Missing/flattened semantic lineage | PASS for bounded synthetic scope | The ST-03.03 contract expressly governs five separate Activative lineage keys; all five remain explicit `NOT_APPLICABLE`, never generic notes. Future category/conversational/visual lineage was not misrepresented as implemented. |
| `NOT_APPLICABLE` handling | PASS for bounded scope | Context and skill paths require explicit dispositions, prohibit runtime use, and preserve evidence. |
| Skill registry/necessity consistency | PASS | Empty governed registry, no external/dynamic skills, five capability evidences, five definition capabilities, `NO_NEW_SKILL_REQUIRED`, `NOT_APPLICABLE_NO_GAP`. |
| AtomicHarnessDefinition completeness | SHAPE PASS / MEANING FAIL | 20 required unique sections, all `REQUIRED`; their exact governed evidence/meaning is not enforced (`BQA-P0-001`). |
| In-memory repository consistency | FAIL | Lost update, partial run commit, and checkpoint overwrite. Normal ST-07.04 commit stores report/receipt/record consistently. |
| Architecture import boundaries | PASS | Independent AST scan found zero external imports and zero layer violations. |
| Test brittleness | CONCERN | Five duplicate exact-source inventories. |
| Test blind spots | FAIL | No ST-07.04 governed tests; missing concurrency, semantic rehash, post-commit observation, and archive-swap tests. |
| Dead/unreachable code | PASS for static scan | No simple unreachable top-level statements after unconditional return/raise found. |
| Mutable default/shared-state risk | PASS for defaults / FAIL for repository synchronization | No mutable literal defaults; shared in-memory repository state is unsynchronized. |
| Error type/failure context | FAIL | Most domain errors are typed with context; post-commit observation failure leaks raw `RuntimeError` and misstates commit status. |

## Positive controls

The following controls worked and should be preserved during correction:

- canonical hashes and receipts are deterministic when their inputs are governed;
- target-validation replay does not append a duplicate event;
- same command ID with a changed payload fails typed;
- complete upstream reopen invalidates all 14 current descendants and preserves historical artifacts;
- target-validation repository failure injection is checked before its grouped writes;
- source-directory traversal is sorted;
- ZIP member traversal, symlink, case collision, executable, nested archive, size/count/depth, and decompression-ratio checks fail closed;
- domain/application/adapter import direction is clean;
- data objects are frozen and use no mutable literal defaults;
- the bounded synthetic `NOT_APPLICABLE` and skill-necessity representations are explicit and internally consistent.

## Verdict and correction boundary

**FAIL_P0_OR_P1**

The next engineering action is a bounded correction pass beginning with `BQA-P0-001`, `BQA-P1-002`, and `BQA-P1-003` under ST-07.04 authority, followed by productization work for repository synchronization/atomicity and archive identity. After correction, run the governed suite twice in fresh processes and rerun this independent audit. This report does not authorize Story implementation, Builder Step 4, production eligibility, or certification.
