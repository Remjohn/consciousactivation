# AGENT_HANDOFF — M0075 Jellyfish Surgical Storyboard Workspace Extraction

**Status:** BLOCKED_OPERATOR_REVIEW_REQUIRED
**Operator decision requested:** `APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`

## Files added / modified

### Added
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/README.md`
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/M0075_JELLYFISH_MAPPING.json`
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/M0075_EXTERNAL_SOURCE_INDEX.md`
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/validate_m0075_extraction.py`
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/M0075_EVIDENCE_RECEIPT.json`
- `docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/AGENT_HANDOFF.md`
- `tests/cae/test_m0075_jellyfish_extraction_reference.py`

### Modified
- None.

No files under `engines/storyboard/`, `packages/`, `services/`, or application runtime were modified.

## Rationale

The current CAE brownfield already has `EditorialStoryboardRecord` as the semantic storyboard authority and `PreparationGraphStore` as the existing immutable revision authority. Adding a parallel Jellyfish project/shot/revision model would violate the mandate's no-duplicate-authority rule and would also create a new canonical object where none currently exists.

The extraction therefore binds the minimum useful Jellyfish behaviors as a reference contract: readiness aggregation, candidate confirmation/ignore patterns, reusable asset context, explicit inspection state, and immutable versioning. The mapping uses existing CAE authorities rather than copying Jellyfish's domain model.

## External source evidence

Repository: `https://github.com/Forget-C/Jellyfish`

License: Apache-2.0, verified from the exact current `LICENSE` path.

Exact current files individually inspected:
- `backend/app/services/studio/shot_preparation_state.py`
- `backend/app/services/studio/shot_extracted_candidates.py`
- `backend/app/services/studio/shot_assets.py`
- `backend/app/models/studio_shots.py`
- `backend/app/services/studio/shots.py`

Relevant symbols are recorded in `M0075_JELLYFISH_MAPPING.json`.

The exact 40-character `main` commit SHA was not retrievable from this execution environment. A GitHub Actions page exposed `a967819` as an abbreviated main reference, but it is intentionally not represented as an exact SHA.

## Authority evidence

The requested root-level constitution and precedence-contract paths are absent. The supplied snapshot contains their current-v1.1 counterparts under `governance/program-control/00_CONSTITUTION/current-v1.1/`.

The mandated `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md` is absent from the supplied snapshot. This remains an operator-level blocker and was not inferred from lower-order documentation.

The supplied repository snapshot has no `.git` metadata. Historical M72 evidence records `8fb3733cc6a750560532f87f98af2fe24c229528`, but that SHA is explicitly historical and is not claimed as the M0075 commit.

## Tests

Commands and observed results:

`python docs/cae/CAE_Visual_Production_Storyboard_Extraction_M0075_v1/validate_m0075_extraction.py`

Result: `M0075 reference extraction validation: PASS`

`pytest -q tests/cae/test_m0075_jellyfish_extraction_reference.py`

Result: `5 passed in 0.18s`

These tests are reference-contract tests. They do not establish native external runtime reachability, visual quality, or production UI operation.

## State / authorization mapping

### Revision editing
- Actor: operator
- Preconditions: current latest CAE revision is known
- Validator: `PreparationGraphStore.save_graph_revision()` base revision check
- Postcondition: new immutable `GraphRevisionRecord`
- Receipt: existing governed operator receipt where a decision is made
- Error: `StaleBaseRevisionError`
- Recovery: reload latest revision and save a new revision from that base

### Candidate review
- Actor: operator
- Preconditions: source/evidence lineage and eligibility available
- Validator: existing CAE candidate/editorial authority
- Postcondition: canonical candidate state changes only through existing CAE paths
- Receipt: `EditorialDecisionReceiptRecord`
- Error: authority/eligibility rejection
- Recovery: retain candidate, create a new governed decision

### Visual inspection
- Actor: operator
- Preconditions: source lineage visible and preview labeled as presentation evidence
- Validator: semantic/provenance validators remain separate
- Postcondition: preview informs review only; it cannot promote semantic correctness by itself
- Receipt: operator decision receipt when a decision is recorded
- Error: `OPERATOR_DECISION_REQUIRED`
- Recovery: repair, reject, or request another candidate/reference

## Scope / exclusions

No new storyboard authority, retrieval system, asset store, UI authority, VAE state model, generation runtime, provider wiring, migration, or external runtime integration was introduced. No Jellyfish source code was copied.

## Rollback

Only the newly added M0075 campaign artifact/test files need rollback. No pre-existing CAE application state was mutated.

## Exact commit SHA

**CAE source commit SHA:** `UNAVAILABLE_IN_SUPPLIED_SNAPSHOT`

**Historical M72 SHA:** `8fb3733cc6a750560532f87f98af2fe24c229528` (historical evidence only)

**M0075 workspace Git commit:** `UNAVAILABLE`; the supplied snapshot contains no `.git` metadata and creating a synthetic repository commit would not recover the original CAE lineage.

## Final operator gate

This bundle is intentionally not self-promoting. The evidence supports only:

`APPROVE-WITH-LIMITATIONS` — reference extraction accepted subject to the documented authority/source SHA gaps and without claiming external runtime or visual acceptance.

Full `APPROVE` requires the missing Authority Pack and exact Git/source commit identifiers to be supplied and re-verified, plus any later UI/runtime validation required for visual production acceptance.
