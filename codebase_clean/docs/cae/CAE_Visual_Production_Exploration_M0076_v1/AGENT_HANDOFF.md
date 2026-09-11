# AGENT_HANDOFF — M0076

**Status:** EXECUTED_WITH_OPERATOR_REVIEW_REQUIRED
**Mandate:** M0076 — DramaClaw Exploratory Canvas and Agent Interaction Extraction
**Decision requested:** `APPROVE-WITH-LIMITATIONS` (operator may instead choose `APPROVE` or `REJECT`)

## Files added

- `docs/cae/CAE_Visual_Production_Exploration_M0076_v1/README.md` — bounded reference component contract and invariants.
- `docs/cae/CAE_Visual_Production_Exploration_M0076_v1/DRAMACLAW_UPSTREAM_TO_CAE_MAPPING.md` — exact upstream paths, adopted/excluded behavior, license and authority mapping.
- `docs/cae/CAE_Visual_Production_Exploration_M0076_v1/exploratory_canvas_reference.py` — pure in-memory exploration state/reference.
- `docs/cae/CAE_Visual_Production_Exploration_M0076_v1/M0076_EVIDENCE_RECEIPT.json` — machine-readable evidence receipt.
- `tests/cae/test_m0076_exploratory_canvas_reference.py` — focused acceptance tests.

## Rationale

Brownfield audit found canonical CAE storyboard/program/receipt records already present in `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py` and the existing editorial compilation path. No duplicate storyboard or semantic-program authority was created. The implementation is isolated and cannot persist or mutate canonical CAE state.

The reference adopts only the minimum DramaClaw interaction grammar: revisioned exploration, node history, explicit approval for agent commands, grouping/locking, reversible branches, and a promotion request carrying canonical storyboard/candidate references plus provenance. A `run_node` operation is recorded as an exploration proposal only.

## Exact upstream reference

Repository: `https://github.com/dramaclaw/dramaclaw`
Reference: `main`, web-visible current commit `c62b409` on 2026-09-10.
License: Elastic License 2.0. No DramaClaw source code was copied or imported.
Exact source paths inspected: `src/novelvideo/freezone/canvas_store.py`, `src/novelvideo/freezone/history.py`, `src/novelvideo/freezone/canvas_lock.py`, `src/novelvideo/chat/dramaclaw_mcp.py`, `NOTICE`, and `docs/en/concepts/features.md`.

The current upstream README says the infinite canvas and pipeline operate as dual tracks, and describes agent-on-canvas control as in development with browser approval. Interactive stories/branching is also marked in development on `feat/canvas-fmv`; it was therefore not treated as released executable behavior.

## Test commands / results

`pytest -q tests/cae/test_m0076_exploratory_canvas_reference.py`
Result: **5 passed in 0.04s**.

Tests cover success/history/group/lock/branch/replay; a plausible good-looking-but-wrong locked edit; unauthorized agent mutation; stale revision rejection; and promotion provenance/operator-receipt requirements.

## What the tests do not prove

They do not prove DramaClaw runtime availability, MCP/REST reachability, browser approval UI behavior, external model execution, deployed persistence, or perceptual/creative quality. No native external runtime proof was substituted with mocks.

## Authority / completion limitations

Two literal constitutional mandate paths are absent but have current exact equivalents under `governance/program-control/00_CONSTITUTION/current-v1.1/`. The mandatory dated 2026-09-10 Authority Pack build-plan is absent with no equivalent in the supplied snapshot. The supplied archive also contains no `.git` metadata, so an exact CAE Git commit SHA and cross-agent merge ownership cannot be established. The DramaClaw web evidence exposed only short SHA `c62b409`; the full upstream SHA was not available through the inspected evidence surface.

These are recorded as `OPERATOR_DECISION_REQUIRED`; no authority file, canonical state, or shared contract was modified.

## Exact commit SHA

CAE commit SHA: **UNAVAILABLE_IN_SUPPLIED_SNAPSHOT** (`.git` metadata absent). Historical M72/M0073 evidence referenced other commits, but those do not establish the current supplied snapshot commit and are not substituted.

## Rollback

Rollback is isolated to the five added paths above. No pre-existing CAE source, registry, canonical state, or external source file was changed.

## Operator gate

Please explicitly select one: `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.

Recommended: `APPROVE-WITH-LIMITATIONS`, limited to behavioral/reference extraction pending the missing dated Authority Pack and a capture of the exact CAE commit SHA in the real Git worktree.
