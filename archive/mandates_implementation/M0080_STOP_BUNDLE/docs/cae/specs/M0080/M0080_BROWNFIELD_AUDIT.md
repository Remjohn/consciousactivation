# M0080 — Brownfield Audit / Stop Record

**Status:** `BLOCKED_OPERATOR_REVIEW_REQUIRED`
**Mandate:** `M0080`
**Campaign batch:** `A1 CORE CONTRACTS`
**Execution date:** `2026-09-10`

## Stop condition

M0080 was not implemented because required authority inputs named by the mandate are unavailable in the supplied repository snapshot. The mandate explicitly requires a stop when required authority is unavailable. No contract, runtime, manifest, or test implementation was invented around the missing source.

## Repository snapshot identity

- Input archive: `/mnt/data/codebase_clean(5).zip`
- Input archive SHA-256: `755aa85bed2e41a608e908de88d027c52f419bf3ad2829bcab9a4b0e0eeac2a2`
- `.git` metadata: absent
- Exact current Git commit SHA: **not establishable from the supplied snapshot**
- Historical nearby commit recorded by the M0079 receipt: `9d22849cc8b2d7457e0e979a83e249ff4a50213a`; this is not asserted as the current snapshot SHA.

## Mandatory authority input audit

### Missing exact paths

1. `docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
2. `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
3. `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
4. `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
5. `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
6. `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`

The current tree contains a governed constitutional equivalent for the first two items under `governance/program-control/00_CONSTITUTION/current-v1.1/`, but M0080 names the literal paths and does not authorize silent substitution. The dated Authority Pack files were not found anywhere in the supplied snapshot.

## Brownfield findings that were safely established

### Canonical storyboard authority already exists

- `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py::EditorialStoryboardRecord` is the existing canonical semantic storyboard object.
- `packages/ca_runtime/src/ca_runtime/preparation_graph_store.py::GraphRevisionRecord` is the existing immutable revision authority.
- `packages/ca_runtime/src/ca_runtime/storyboard_session.py` (M0079) already projects editable storyboard session/revision behavior around those authorities and explicitly states that it does not own semantic meaning, candidate selection, asset rights, or runtime execution.
- `tests/cae/test_m0079_storyboard_session_revision.py` is the existing focused regression surface for that shared storyboard layer.

### Existing format-adjacent Programs already exist

- `programs/editorial_storyboard_program/` compiles grounded narrative storyboards and remains the semantic storyboard authority surface.
- `programs/video_edit_program/` already owns source-grounded video edit compilation/render/QA and therefore is downstream/adjacent behavior, not permission to create a competing semantic storyboard model.
- `programs/visual_derivative_production_program/` already owns source-grounded `CAROUSEL`, `SUPERVISUAL`, and animation derivative realization with deterministic source extraction, composition compilation, dual-axis QA, and release authorization.

These observations support adapting existing authorities rather than creating duplicate objects, but they do **not** define the missing M0080 format-specific composition grammar. That grammar must be derived from the missing Authority Pack before implementation.

## Testability findings

The intended focused baseline suite was attempted:

```text
pytest -q tests/cae/test_m0079_storyboard_session_revision.py tests/phase4/test_m39_storyboard_semantic_compile.py tests/cae/test_visual_derivative_production_program.py tests/cae/test_ca_m005_format_archetype_gate.py
```

Observed result: test collection stopped with `ModuleNotFoundError: No module named 'psycopg'` from `packages/ca_runtime/src/ca_runtime/database.py` imported by `ca_runtime.__init__`. Therefore no baseline test result is being presented as a green acceptance proof.

## Implementation intentionally withheld

The following requested M0080 contracts were **not** created:

- `VideoStoryboardProgram`
- `CarouselStoryboardProgram`
- `SuperVisualStoryboardProgram`
- `PresentationStoryboardProgram`

No schema, state machine, program manifest, compiler, or format-specific test was authored because the missing Authority Pack is the mandated source for the format-specific composition grammar and constraints. Implementing without it would violate M0080's stop condition and create unsupported authority assumptions.

## Operator decision required

Re-open/continue M0080 only after the missing literal authority inputs are supplied or the operator explicitly amends the mandate's required-source boundary. The decision must remain one of:

- `APPROVE`
- `APPROVE-WITH-LIMITATIONS`
- `REJECT`

For this blocked execution, an approval is not a promotion of unimplemented contracts.
