# M0076 — DramaClaw Upstream → CAE Mapping

**Evidence posture:** behavioral reference only. No DramaClaw source code is copied into CAE.

## Authority finding

The uploaded CAE snapshot has no `.git` metadata, so cross-agent worktree collision ownership and an exact CAE commit SHA cannot be established from the supplied artifact. Two mandated constitutional paths are absent at their literal locations but have exact current equivalents under `governance/program-control/00_CONSTITUTION/current-v1.1/`. The dated 2026-09-10 Authority Pack build-plan path is absent with no equivalent found in the snapshot. This is recorded as `OPERATOR_DECISION_REQUIRED`; it does not justify changing existing authority files.

## Current upstream

- Repository: `https://github.com/dramaclaw/dramaclaw`
- Branch/reference inspected: `main`
- Current web-visible commit: `c62b409` (GitHub exposes the short SHA on the current commit page; full SHA was not available through the supplied web evidence surface).
- License: Elastic License 2.0 (source-available). `NOTICE` also states that the ELv2 grant does not grant trademark rights and points to additional dependency notices.
- No upstream source code was imported.

## Upstream → CAE behavior map

| DramaClaw source path / symbol | Observed behavior | CAE adoption | Classification |
|---|---|---|---|
| `src/novelvideo/freezone/canvas_store.py` — `CanvasStore` and canvas revision/history machinery | Durable canvas state, revisions, conflict/stale-write protection, bounded payloads, atomic writes | Deterministic **reference grammar only**: explicit revision precondition and stale-command rejection. Do not duplicate its storage layer. | `HYPOTHESIS` + `EXECUTABLE` reference test |
| `src/novelvideo/freezone/history.py` — generation history helpers | Append-oriented per-node generation history, restore/delete semantics, media retained | Adopt immutable per-node history concept; local reference uses immutable tuples and restore-as-new-entry. | `HYPOTHESIS` + `EXECUTABLE` reference test |
| `src/novelvideo/freezone/canvas_lock.py` — canvas locking | Per-canvas lock to serialize writers | Adopt lock/guard concept for node mutations in exploration reference. CAE canonical locking remains authoritative elsewhere. | `HYPOTHESIS` + `EXECUTABLE` reference test |
| `src/novelvideo/chat/dramaclaw_mcp.py` — thin MCP bridge | Agent tools route through REST API and schema/auth guards | Adopt the **separation** principle only: agent command is a proposal/command that must pass a deterministic validator and explicit approval. No MCP/runtime integration. | `HYPOTHESIS` + `EXECUTABLE` reference test |
| `docs/en/concepts/features.md` — XiaHua + Xia Director | Infinite canvas, node history, dual-track exploration/pipeline, grouping/locking, promotion; agent canvas control documented as in development | Adopt interaction pattern, not authority model. Promotion becomes a request referencing canonical storyboard/candidate and operator receipt; no canonical mutation here. | `DOCUMENT` / `HYPOTHESIS` |
| `NOTICE` | ELv2 and trademark/third-party attribution boundaries | Record license boundary; do not copy source code or branding. | `REGISTRY_SOURCE` |

## Included

Infinite/reversible canvas state; per-node history; explicit operator-approved agent commands; stale revision protection; grouping; locking; exploration branches; promotion request carrying canonical storyboard/candidate references and source provenance.

## Excluded

DramaClaw persistence implementation; REST/MCP integration; hosted runtime; model gateway; agent identity/authority; canonical CAE storyboard/state mutation; Visual Chat as an authority; source code copying; ELv2 licensing assumptions beyond this behavioral extraction; interactive-story/Ink compilation on `feat/canvas-fmv` because the current README marks that work as in development.

## Canonical CAE reuse points

The current CAE snapshot already contains `EditorialStoryboardRecord`, `SemanticProgramRecord`, `CompositionHandoffRecord`, and `EditorialDecisionReceiptRecord` in `packages/ca_runtime/src/ca_runtime/editorial_discovery_store.py`. M0076 deliberately does **not** create replacement records. The promotion request is an adapter-shaped handoff that later integration may translate into these existing canonical records after operator promotion.

## State grammar

`EXPLORATION_REVISION_N`
→ approved command + revision validator + lock guard
→ `EXPLORATION_REVISION_N+1`

`EXPLORATION_BRANCH`
→ operator-selected promotion + canonical-reference/provenance validation
→ `PROMOTION_REQUEST` (no canonical mutation)

`PROMOTION_REQUEST`
→ downstream CAE operator/program gate (outside M0076)
→ canonical storyboard/semantic/composition state, only if independently authorized.
