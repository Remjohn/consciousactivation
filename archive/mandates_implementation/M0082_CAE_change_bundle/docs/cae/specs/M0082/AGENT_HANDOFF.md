# M0082 Agent Handoff

## Status

`IMPLEMENTED — FOCUSED TESTS PASS — OPERATOR REVIEW REQUIRED`

M0082 adds a deterministic, pure Editorial Expression Calculus over the existing CAE runtime domain. It extends the M0079/M0080 chain without creating a second semantic, storyboard, retrieval, format, asset-rights, VAE, or state authority.

## Files added / modified

- `packages/ca_runtime/src/ca_runtime/editorial_expression_calculus.py` — added bounded grammar schema, format/scene profile registry, integer-only calculus, deterministic output digest, and fail-closed source-quality validation.
- `packages/ca_runtime/src/ca_runtime/__init__.py` — exported the M0082 calculator through the existing CAE runtime namespace.
- `tests/cae/test_m0082_editorial_expression_calculus.py` — added 7 focused tests covering success, replay determinism, profile selection, source-quality/evidence rejection, unsupported profiles, and a contrastive grammar change.
- `docs/cae/specs/M0082/M0082_EDITORIAL_EXPRESSION_CALCULUS.md` — implementation/reference specification and evidence limitations.
- `docs/cae/specs/M0082/M0082_EVIDENCE_RECEIPT.json` — machine-readable evidence record.

## Authority mapping

| M0082 concern | Existing authority | Boundary |
|---|---|---|
| semantic meaning | canonical CAE semantic/storyboard records | M0082 does not create or mutate meaning |
| editable storyboard / revisions | M0079 `StoryboardRevision`, `GraphRevisionRecord` | M0082 consumes only structural grammar |
| format surface grammar | M0080 program contracts | M0082 supplies tuning bounds only |
| source lineage | existing evidence references | M0082 requires non-empty unique refs and a quality floor |
| transformation execution | downstream `TransformationIntent` / `TransformationRecipe` / `MotionPlan` | M0082 does not execute or persist transforms |
| operator promotion | existing operator gates/receipts | M0082 never self-promotes |

## Implementation rationale

A single pure module was selected because the brownfield audit found the canonical downstream objects already present in `packages/ca_runtime/src/ca_runtime/storyboard_session.py` and the format contracts already present in `storyboard_programs.py`. A new persistence layer, service, or state machine would have duplicated authority.

The calculus uses integer basis points and integer milliseconds to preserve canonical replay parity and avoid the repository's existing prohibition on floating-point canonical contract values.

## Tests

Primary command:

`PYTHONPATH=packages/ca_contracts/src pytest -p no:asyncio -q tests/cae/test_m0082_editorial_expression_calculus.py`

Observed result:

`8 passed in 0.17s`

The focused suite itself enumerates all 24 declared format/scene combinations and checks each result against the selected profile bounds.

The normal repository package import path could not be executed in this sandbox because pre-existing dependencies `psycopg` and `cmf_builder` are absent. No test was weakened or skipped to hide that environmental fact. The focused tests therefore load the pure M0082 module directly and prove the calculus itself.

## External sources

No external repository source was adopted or vendored for M0082. No external runtime was invoked. The implementation has no external-provider reachability claim.

Historical M0078 behavior was inspected as CAE brownfield context but was not copied as source code.

## Authority-source status

The supplied archive snapshot did not contain the separately mandated dated Authority Pack files, but the authoritative repository `main` branch currently contains them under `docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/`. The Authority Pack manifest explicitly states that these files are frozen campaign inputs for M0073–M0096 v2 and that agents must read them directly.

Direct repository sources inspected:

- `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/AUTHORITY_PACK_MANIFEST.md`
- `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md`
- `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/01_CAE_Product_Update_Visual_Asset_Editor.md`
- `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/02_CAE_PRD_Update_Visual_Asset_Studio.md`
- `https://github.com/Remjohn/consciousactivation/blob/main/docs/AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/03_CONSCIOUS_E_MOTION_EDITING_STANDARDS_v2.md`

Constitutional sources remain the brownfield repository equivalents inspected at:

- `governance/program-control/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
- `governance/program-control/00_CONSTITUTION/current-v1.1/governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`

The Authority Pack supports the M0082 direction: it explicitly places Editorial Expression Calculus between Narrative Editing Grammar and Transformation Intent, calls for deterministic numeric parameters for pace, shot/hold/cut timing, occupancy, scale, motion, density, contrast, salience and intervention frequency, and preserves CAE as the semantic/contract authority.

## Evidence classes

- `EXECUTABLE`: M0082 calculator implementation.
- `SCHEMA`: grammar/output/profile models and bounded validation.
- `TEST`: focused deterministic/negative/contrastive test suite.
- `DOCUMENT`: specification and handoff.
- `HYPOTHESIS`: numeric tuning constants and their initial calibration bounds.
- `OPERATOR_DECISION_REQUIRED`: normal package import environment gap, lack of perceptual/native-runtime evidence, and final operator calibration/approval of numeric bounds.

## Limitations

The implementation does not prove visual semantic correctness, perceptual quality, source-rights approval, native renderer/provider reachability, or final creative judgment. The numeric constants remain initial deterministic calibration defaults and require operator review/calibration against real visual output.

The uploaded archive contains no `.git` directory, so its original source commit cannot be recovered from the archive. The GitHub repository currently exposes a Sep 10, 2026 `main` history entry at short SHA `1238dda`, but that is not asserted as the archive's source commit and is not substituted for exact archive provenance.

## Exact implementation SHA

`IMPLEMENTATION_COMMIT_SHA: 963d0c7ac7267d552f8c542c724c850722a66119`

This is the synthetic local snapshot implementation commit created outside the source tree. It identifies the exact post-edit tree captured for this mandate; it is **not** represented as the upstream repository's original commit SHA.

## Operator decision requested

`APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.

The recommended review lane is `APPROVE-WITH-LIMITATIONS` pending operator review/calibration of the numeric bounds and later perceptual/native-runtime validation.
