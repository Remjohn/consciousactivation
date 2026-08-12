# Stage 1 State Machine

Referenced by `SKILL.md` Section 9. This is the only legal sequence of states for a harness. No state may be skipped, and no artifact may jump directly from `JSON_GENERATED`-equivalent output to `STAGE1_COMPLETE`.

```text
DISCOVERED
    ↓
SELECTED_BY_OPERATOR        (the only "approval" this system recognizes — see SKILL.md §0)
    ↓
LOADED                      (data-integrity receipt recorded — SKILL.md §3)
    ↓
OBSERVED
    ↓
OBSERVATION_VALIDATED
    ↓
TAXONOMY_RESOLVED           (canonical / variant / novel_candidate / unknown per item)
    ↓
VISUAL_SYNTAX_VALIDATED
    ↓
DEDUPLICATED                (by syntax_hash, not layout_fingerprint prose)
    ↓
CONTRACT_VALIDATED          (technical_status assigned: PASS | REVIEW | BLOCKED | FAIL)
    ↓
OPERATOR_REVIEWED           (operator_disposition assigned: APPROVE | REVISE | HOLD)
    ↓
COMPILER_READY              (only if technical_status ∈ {PASS, REVIEW} AND disposition == APPROVE)
    ↓
STAGE1_COMPLETE
```

## Terminal / re-entry states

* `BLOCKED` or `FAIL` at `CONTRACT_VALIDATED` → the harness returns to the operator with the contract report; it cannot proceed to `OPERATOR_REVIEWED` → `STAGE1_COMPLETE` regardless of what disposition the operator records. The only path forward is `REVISE` → re-run from the relevant checkpoint (Section "Resumable checkpoints" below).
* `HOLD` at `OPERATOR_REVIEWED` → the harness stops in place. No further processing happens until the operator issues a new Harness Build Call for it.
* `REVISE` at `OPERATOR_REVIEWED` → the harness returns to whichever checkpoint the operator's revision notes indicate needs re-running (does not require restarting from `LOADED` unless the integrity receipt itself is in question).

## Resumable checkpoints

A failed later stage must not force re-running earlier stages unnecessarily. Checkpoint boundaries, one per state transition above from `LOADED` through `CONTRACT_VALIDATED`:

```text
01_input_receipt
02_observation
03_taxonomy_resolution
04_visual_syntax
05_deduplication
06_contract_validation
07_operator_review
08_final_receipt
```

Re-running from checkpoint N re-uses the persisted output of checkpoints 1..N-1 rather than regenerating them, unless the operator explicitly requests a full re-run (e.g. because the integrity receipt at checkpoint 01 no longer matches).
