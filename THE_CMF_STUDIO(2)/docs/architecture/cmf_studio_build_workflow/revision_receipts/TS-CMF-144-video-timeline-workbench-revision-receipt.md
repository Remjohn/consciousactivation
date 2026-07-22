---
title: "TS-CMF-144 Video Timeline Workbench Revision Receipt"
spec_id: "TS-CMF-144"
date: "2026-06-26"
protocol: "CMF/ERA3 Spec Revision"
status: "complete"
---

# TS-CMF-144 Video Timeline Workbench Revision Receipt

## DECISION LOG

No architect-only decision was required. The audit findings were protocol and implementation-detail gaps, not conflicting architecture decisions.

## REVISIONS APPLIED

**Fix 1 - Schema and primitive integrity**

Resolves: `TS-CMF-144 | LENS 2 | CRITICAL`

Updated Section 3 to require exact primitive registry IDs and at least three distinct primitive IDs for composition-bearing segments. Updated Section 9 with `TimelineMarker`, `TimelineEditCommand`, marker/status fields on `VideoTimelineWorkbenchState`, and command scope/version/hash fields.

**Fix 2 - Concrete operator-web file ownership**

Resolves: `TS-CMF-144 | LENS 3 | WARNING`

Updated Section 7 with concrete file targets under `operator-web/src/screens`, `operator-web/src/components/timeline`, `operator-web/src/api`, `operator-web/src/state`, `operator-web/src/fixtures`, and `operator-web/src/styles`.

**Fix 3 - Executable CBAR gates**

Resolves: `TS-CMF-144 | LENS 4 | CRITICAL`

Updated Section 13 with executable thresholds and downstream consequences for frame alignment, primitive coverage, proxy/final parity, stale state, scope isolation, hard blockers, and OTIO coverage.

**Fix 4 - Telegram and provider boundary**

Resolves: `TS-CMF-144 | LENS 3 | WARNING`

Updated Section 12 to limit Telegram to notification, quick status, PWA deep-link handoff, and structured revision requests. Telegram cannot submit `TimelineEditCommand` or final approval.

**Fix 5 - Fixture mode safety**

Resolves: `TS-CMF-144 | LENS 5 | WARNING`

Updated Sections 8, 12, 14, and 16 to make fixture mode explicit, visibly bannered, and forbidden as a silent production fallback.

**Fix 6 - Format-specific timeline representation**

Resolves: `TS-CMF-144 | LENS 1 | WARNING`

Updated Section 8 to describe how `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC` appear in the preview and lane model, including PaperCut/2D avatar lanes, reaction UI lanes, human cutout lanes, proof inserts, and cinematic pacing markers.

## VERIFICATION CHECKLIST

| Check | Result |
|---|---|
| Spec keeps CMF/ERA3 18-section structure | Pass |
| Files Read section preserved | Pass |
| FR-CMF trace preserved | Pass |
| Pipeline trace preserved | Pass |
| Command Bus boundary preserved | Pass |
| Browser source-of-truth prohibited | Pass |
| Schema orphan fixed | Pass |
| Fixture fallback hardened | Pass |
| Telegram boundary hardened | Pass |
| Acceptance criteria expanded | Pass |

