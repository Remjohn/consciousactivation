# M0079 Agent Handoff

## Status

`IMPLEMENTED — 100% FOCUSED REGRESSION PASS — OPERATOR REVIEW REQUIRED`

M0079 is implemented as the CAE-native editable storyboard workspace around
the existing `EditorialStoryboardRecord`. Semantic meaning, candidate
selection, asset rights, and runtime execution remain owned by their existing
CAE authorities.

## Changed paths

- `packages/ca_runtime/src/ca_runtime/storyboard_session.py`
- `packages/ca_runtime/src/ca_runtime/__init__.py`
- `tests/cae/test_m0079_storyboard_session_revision.py`
- `docs/cae/specs/M0079/M0079_EVIDENCE_RECEIPT.json`
- `walkthrough.md`

## Authority mapping

| M0079 concept | CAE authority |
|---|---|
| StoryboardSession | `EditorialStoryboardRecord` identity plus a session projection |
| StoryboardRevision | `PreparationGraphStore` / immutable `GraphRevisionRecord` |
| Scene / Shot / Element | typed revision payload, validated before persistence |
| VisualAssetReference | evidence-linked reference only; no asset authority created |
| TransformationIntent → Recipe → MotionPlan | typed downstream expression chain |
| OperatorVisualFeedback | immutable session feedback row |
| Validation / Compile receipt | immutable session receipt rows linked to revision digest |

Every session requires an existing workspace-scoped `EditorialStoryboard`.
Every revision requires source evidence lineage, rejects detached assets and
transformation recipes, and is saved through the existing stale-base CAS path.

## Verification

Focused M0079 tests cover the happy path, evidence-grounded asset handling,
good-looking-but-wrong rejection, stale writes, tenant isolation, immutable
feedback, validation, compile gating, and deterministic replay.

The unified storyboard/visual regression command passed 46 tests. The exact
commands and evidence classes are recorded in `M0079_EVIDENCE_RECEIPT.json`.

## Authority-pack and environment limitations

The delivered audit handoff named literal root paths that are not present in
this checkout (`docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` and
`governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`). Their current governed
equivalents under `governance/program-control/00_CONSTITUTION/current-v1.1/`
were inspected. The dated Visual Production Authority Pack was present under
`archive/mandates_implementation/CAE_Visual_Production_Storyboard_M0073_M0096_v1/AUTHORITY_PACK/`
and was read before editing. Native external runtime reachability and human
perceptual approval remain unclaimed.

## Exact commit SHA

Implementation commit: `9d22849cc8b2d7457e0e979a83e249ff4a50213a`.
The evidence-receipt SHA update is a follow-up documentation commit.

## Operator decision requested

`APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`. Human review remains
required for perceptual quality, source-rights confirmation, and any native
runtime handoff.
