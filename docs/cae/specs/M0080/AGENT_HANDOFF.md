# M0080 Agent Handoff

## Status

`IMPLEMENTED — 100% REGRESSION PASS — OPERATOR REVIEW REQUIRED`

M0080 adds four format-specific storyboard program contracts as deterministic
projections of the M0079 `StoryboardRevision`. `EditorialStoryboardRecord`
remains semantic narrative authority; `GraphRevisionRecord` remains immutable
revision authority; the format programs do not create retrieval, asset-rights,
semantic-program, or runtime authority.

## Changed paths

- `packages/ca_runtime/src/ca_runtime/storyboard_programs.py`
- `packages/ca_runtime/src/ca_runtime/__init__.py`
- `packages/ca_runtime/src/ca_runtime/visual_derivative_production_program.py`
- `tests/cae/test_m0080_storyboard_program_contracts.py`
- `docs/cae/specs/M0080/AGENT_HANDOFF.md`
- `docs/cae/specs/M0080/M0080_EVIDENCE_RECEIPT.json`
- `walkthrough.md`

## Contract mapping

| Contract | Grammar and deterministic constraints |
|---|---|
| `VideoStoryboardProgram` | Non-empty temporal scenes; non-overlapping ordered shots; downstream video/OpenChatCut surface remains execution authority |
| `CarouselStoryboardProgram` | Contiguous scene-to-slide progression; each slide has source-grounded elements |
| `SuperVisualStoryboardProgram` | Integer basis-point geometry, visible bounded rectangles, safe canvas bounds |
| `PresentationStoryboardProgram` | Contiguous slides; positive unique per-slide build steps |

All four compile the same `StoryboardRevision` into a common immutable
`StoryboardExpression`, preserving session, revision, EditorialStoryboard,
semantic-program, harness, and evidence lineage identifiers. Canonical hashing
rejects unsupported payloads instead of accepting arbitrary model output.

## Dependency / fixture resolution

The prior stop snapshot reported missing `psycopg`; the current Git checkout
already has `psycopg 3.3.4`, matching the declared runtime dependency. The
focused baseline then exposed a genuine missing import in
`visual_derivative_production_program.py`; importing
`require_current_tenant_context` resolved the eight lifecycle failures without
changing assertions or weakening isolation checks.

The requested `CAE-M0080_BUNDLE` and `COMPONENT_CONTRACT.yaml` were not
present in the checkout. The implementation therefore used the canonical
M0080 mandate and the supplied campaign Authority Pack under
`archive/mandates_implementation/CAE_Visual_Production_Storyboard_M0073_M0096_v1/AUTHORITY_PACK/`.
This limitation is recorded in the evidence receipt.

## Verification

The focused M0080 contract suite passed 4/4. The mandated M0079/M39/
visual-derivative/archetype baseline passed 35/35. The complete M0074–M0080
storyboard regression passed 71/71 (100%). Exact commands and evidence classes
are in `M0080_EVIDENCE_RECEIPT.json`.

## Limitations

- Native OpenChatCut, Slidev, reveal.js, and external runtime reachability are not claimed.
- Rendered visual quality, source-rights confirmation, and final creative judgment remain operator decisions.
- Pydantic deprecation warnings remain non-failing and do not alter acceptance criteria.

## Exact commit SHA

Recorded by the implementation commit and finalized in the evidence update.

## Operator decision requested

`APPROVE`, `APPROVE-WITH-LIMITATIONS`, or `REJECT`.
