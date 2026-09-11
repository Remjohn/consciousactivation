# M0074 Wind Comic → CAE surgical extraction mapping

**Evidence classes:** `EXECUTABLE`, `SCHEMA`, `DOCUMENT`, `TEST`, `OPERATOR_DECISION_REQUIRED`.

## External source identity

- Upstream URL: `https://github.com/ChrisChen667788/wind-comic`
- Pinned upstream commit: `15b94078eece85496892d74933fa8193105dc96f`
- License: MIT (`LICENSE` at the pinned commit; copyright ChrisChen667788, 2026).
- Method: exact raw source files at the pinned commit were inspected; README claims were used only as discovery context.

## Adopted behaviors

| Wind Comic source | Exact symbol / behavior inspected | CAE adaptation | Evidence class |
|---|---|---|---|
| `lib/pull-sheet.ts` | `PullSheetShot`, `buildPullSheetFromScript()` | Deterministic shot-keyed projection/export; derived timing remains observation-only | `EXECUTABLE` |
| `lib/pull-sheet-import.ts` | `parseCsv`, `parsePullSheetRows`, `mergePullSheetIntoScript` | Strict CSV round-trip parsing, whitelist merge, changed-field summary, unknown-shot reporting; no canonical mutation | `EXECUTABLE` |
| `components/project/cinema-timeline.tsx` | timeline edit state/history, move/resize concepts | Deterministic timeline geometry/audit only; no UI/Yjs/runtime adoption | `EXECUTABLE` |
| `lib/timeline-tracks.ts` | track construction / timing primitives | Timing projection/audit shape; no track authority copied | `EXECUTABLE` |
| `lib/style-bible.ts` | canonical key-art style anchor concept | Explicit `styleAnchorRef` lineage carried on shot references; no image generation | `SCHEMA` / `EXECUTABLE` |
| `lib/consistency-policy.ts` | scene anchor + character reference selection policy | CAE-supplied scene/style anchor validation; does not select provider refs or generate | `SCHEMA` / `EXECUTABLE` |
| `lib/comments.ts` | target refs, threading, append comment semantics | Immutable in-memory feedback/revision append model; canonical persistence remains CAE-owned | `SCHEMA` / `EXECUTABLE` |
| `components/project/shot-workshop-tab.tsx` | per-shot workshop / isolated shot actions | Isolated shot workshop is represented as proposal-level data operations; provider re-render omitted | `DOCUMENT` / `EXECUTABLE` |

## Explicit exclusions

1. `services/hybrid-orchestrator.ts` and all generation-provider orchestration: excluded.
2. Provider regeneration endpoints and provider-specific 4K generation: excluded.
3. Yjs awareness/collaboration and remote cursor/segment-lock runtime: excluded.
4. Wind Comic database schema, notification transport, email delivery, and application persistence: excluded.
5. Wind Comic agent/provider architecture: excluded.
6. Wind Comic semantic program authority: excluded; CAE semantic meaning remains upstream.
7. Any direct mutation of CAE canonical timeline/storyboard state: excluded. The adapter only returns proposals/validation reports.

## CAE brownfield anchors

- Canonical editorial storyboard object: `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py` → `EditorialStoryboardRecord` (`EXECUTABLE` / `SCHEMA`).
- Canonical storyboard compilation: `packages/ca_runtime/src/ca_runtime/editorial_discovery_program.py` → `compile_editorial_storyboard` (`EXECUTABLE`).
- Canonical storyboard state machine: `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` → `STORYBOARD_STATE_MACHINE_V1` (`SCHEMA` / `EXECUTABLE`).
- Canonical timeline edit path: `api/services/human_resolution.py` (`EXECUTABLE`), with CAS/stale checks and before/after evidence.
- Canonical timeline projection: `api/routers/campaigns.py` and `apps/web/src/api/campaigns.ts` (`EXECUTABLE` / `SCHEMA`).
- Evidence-first retrieval authority: `docs/cae/CAE_Product_Brief/10_Media_Intelligence_Asset_Intelligence_Evidence_Retrieval.md` (`DOCUMENT`).

## Source-relevant observations

- Wind Comic's pull-sheet import makes the shot number the immutable key and excludes derived `startSec`/`endSec` from round-trip writes.
- Wind Comic's timeline provides multi-track retiming/resize and edit history; this extraction keeps only deterministic geometry/audit, not collaborative runtime.
- Wind Comic's style-bible and consistency policy use explicit visual anchors. CAE receives only the lineage/provenance concept; the selection/generation authority remains in CAE.
- Wind Comic comments use target references and threaded replies; the extraction retains immutable revision identity and target linkage but leaves persistence/notifications to CAE.
