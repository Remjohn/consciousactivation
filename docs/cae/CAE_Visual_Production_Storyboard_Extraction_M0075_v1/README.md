# M0075 — Jellyfish Surgical Storyboard Workspace Extraction

**Status:** BLOCKED_OPERATOR_REVIEW_REQUIRED
**Mandate:** M0075
**Campaign batch:** B1 REPOSITORY EXTRACTION

## Decision state

This bundle records the maximum bounded extraction that can be established honestly from the supplied CAE snapshot and current read-only Jellyfish web evidence. No CAE application/runtime file was modified.

The implementation stop was triggered by two mandate-level evidence blockers already present in the M0073 brownfield state:

1. `AUTHORITY_PACK/CAE_Visual_Production_Update_2026-09-10/00_REPOSITORY_TO_PRODUCT_BUILD_PLAN.md` is absent from the supplied snapshot and is also not present in the public repository root examined for the current CAE main branch.
2. The supplied CAE snapshot has no `.git` metadata, so the source repository commit SHA cannot be truthfully recovered from the attachment.
3. The current Jellyfish implementation files were individually inspected through exact raw-source URLs, but the exact 40-character tip SHA for `main` could not be verified in this execution environment. A current abbreviated workflow reference (`a967819`) was observed, but is not promoted to an exact source commit.

Per the mandate stop condition, no runtime integration, migration, new canonical object, or copied upstream code was introduced.

## Brownfield finding

CAE already has the authoritative building blocks required for a surgical mapping:

- `EditorialStoryboardRecord` remains the canonical storyboard semantic object.
- `EditorialDecisionReceiptRecord` is the existing immutable operator audit surface for selection/rejection/modification/locking/comparison/regeneration actions.
- `ContentCandidateRecord` already carries version and predecessor lineage.
- `PreparationGraphStore` is the existing revision authority, with immutable revisions, stale-base rejection, historical inspection, and immutable run bindings.
- Existing M39 storyboard→semantic-program tests already establish evidence lineage, operator selection, wrong-reading locks, unapproved asset blocking, timing continuity, and cross-workspace isolation.

No `StoryboardSession` or `StoryboardRevision` canonical object exists in the supplied tree. This bundle therefore treats those mandate terms as **mapping concepts**, not permission to create duplicate authority. `StoryboardSession` maps to the existing `EditorialStoryboardRecord` plus a CAE preparation graph; `StoryboardRevision` maps to `GraphRevisionRecord`.

## Adopted minimum behavior

| Jellyfish behavior | CAE mapping | Evidence class | Decision |
|---|---|---|---|
| Shot preparation readiness aggregate | Derived presentation over `EditorialStoryboardRecord`, semantic-program inputs, evidence/asset eligibility, and preparation graph | REGISTRY_SOURCE + SCHEMA | Adopt pattern only |
| Candidate confirmation / ignore lifecycle | Existing `EditorialDecisionReceiptRecord` + canonical candidate state; no Jellyfish status table | REGISTRY_SOURCE + EXECUTABLE | Adopt through existing authority |
| Reuse/link existing character/scene/prop/costume assets | Existing evidence/asset authority and storyboard `planned_inserts`; no Jellyfish asset store | REGISTRY_SOURCE + SCHEMA | Adopt pattern only |
| WYSIWYG editing with explicit save boundary | `PreparationGraphStore.save_graph_revision()`; each operator edit creates an immutable revision | EXECUTABLE | Adopt |
| Visual inspection / preview | Presentation-only review surface; preview cannot promote semantic correctness | DOCUMENT + OPERATOR_DECISION_REQUIRED | Adopt constraint |
| Version history / stale editor rejection | `GraphRevisionRecord`, `base_revision_id`, `StaleBaseRevisionError` | EXECUTABLE + TEST | Adopt |

## Explicit exclusions

Excluded from the extraction are the Jellyfish DB schema and project/task authority model, provider wiring, generation runtime, frontend state authority, model selection, background task infrastructure, and any direct external-runtime invocation. No Jellyfish source code was copied.

The evidence-first ordering remains CAE-owned: `RETRIEVE → TRANSFORM → COMPOSE → GENERATE`. Jellyfish behavior does not change that ordering and is not treated as semantic authority.

## Operator gate

The safe disposition for this bundle is **APPROVE-WITH-LIMITATIONS** only if the operator accepts the evidence gaps listed above. Full approval requires re-opening the mandate after the missing Authority Pack and exact repository/source commit identifiers are supplied and re-verified.
