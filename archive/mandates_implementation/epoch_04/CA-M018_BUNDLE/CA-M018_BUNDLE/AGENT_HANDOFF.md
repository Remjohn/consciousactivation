# CA-M018 — Hierarchical Context Lineage — Agent Handoff

**Mandate ID:** `CA-M018`  
**Requirement / Invariant:** `FR-CTX-001` / `INV-CTX-001`  
**Title:** Hierarchical Context Lineage  

## 1. Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/context_lineage.py` | **New module.** Defines immutable hierarchical context nodes (`CAMPAIGN` → `EPISODE` → `TURN`), deterministic revision hashes, `ContextLineageTree` with cycle detection, orphan prevention, parent-level enforcement, full-hierarchy require, and fail-closed ref validation. | FR-CTX-001 / INV-CTX-001: every admitted context carries explicit parent lineage; cycles, orphans, missing parents, level skips, and hash forgery are rejected. |
| `tests/phase4/test_ca_m018_context_lineage.py` | **New test suite.** Positive path (full tree admit + path/ancestor queries), negative paths (missing parent, orphan ref, cycle, wrong level, forged hash, empty/duplicate tree), immutability, and lightweight `validate_hierarchy_refs`. | Executable evidence that hierarchy is structurally enforced, not optional fields. |

## 2. Exact paste instructions

Replace / add the following paths inside the repository root:

```
CA-M018_BUNDLE/services/interview/src/conscious_activations_interview_expression/context_lineage.py
  → services/interview/src/conscious_activations_interview_expression/context_lineage.py

CA-M018_BUNDLE/tests/phase4/test_ca_m018_context_lineage.py
  → tests/phase4/test_ca_m018_context_lineage.py
```

Both files are new; no existing files are overwritten.

## 3. Manual post-apply commands

None required (no migrations, no package metadata changes, no generated code).

Optional verification (operator may run; agent did not execute tests per mandate instruction):

```bash
pytest tests/phase4/test_ca_m018_context_lineage.py -q
```

## 4. New automated tests included in the bundle

- `tests/phase4/test_ca_m018_context_lineage.py`

  Coverage groups:
  - Mandate identity constants
  - Valid full hierarchy construction and `require_full_hierarchy`
  - Lineage path / ancestors ordering
  - Deterministic revision hashes
  - Multi-turn under one episode
  - Reject turn/episode without parent
  - Reject campaign with parent
  - Reject orphan parent_ref not present in tree
  - `validate_hierarchy_refs` missing episode/campaign
  - Cycle detection (standalone + tree admission)
  - Forged revision_hash rejection
  - Immutable provenance assertion
  - Tree hash sensitivity to node set
  - Duplicate identity / empty tree rejection
  - Wrong parent level (skip-tier) rejection
  - Frozen model immutability
  - Invalid SHA on `ImmutableRef`

## Residual limitations

- Module is scoped to the interview-expression package as authorized by the mandate target files. Integration into `packages/ca_runtime/.../program_state_runtime.py` or evidence-fragment write paths is out of scope for this bounded mandate and must be taken up by a subsequent wiring mandate if required.
- Recovery that invents missing parents is intentionally not implemented (fail-closed only).
- Multi-campaign forests are rejected; exactly one CAMPAIGN root per tree is required.

## Operator decision request

Approve or reject `CA-M018` based on whether the evidence above proves that hierarchical context lineage (Turn → Episode → Campaign) is structurally enforced with immutable revision hashes, cycle detection, and orphan prevention at the module boundary.
