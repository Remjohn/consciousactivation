---
title: "TS-CMF-144 Video Timeline Workbench Spec Audit"
spec_id: "TS-CMF-144"
date: "2026-06-26"
protocol: "CMF/ERA3 5-Lens Spec Audit"
status: "revised-in-same-pass"
---

# TS-CMF-144 Video Timeline Workbench Spec Audit

## PASS

No zero-flag pass was issued before revision. The spec was structurally complete but required operational hardening before implementation.

## FLAGS

**[TS-CMF-144] | LENS 2 | SEVERITY: CRITICAL**
- **Finding:** Section 8 and frontmatter named `TimelineMarker` and `TimelineEditCommand`, but Section 9 did not define those schema objects and primitive references were not required to use exact registry IDs.
- **Location:** Sections 3, 8, and 9.
- **Required Action:** Add explicit `TimelineMarker` and `TimelineEditCommand` Pydantic schemas, add marker fields to `VideoTimelineWorkbenchState`, and require at least three exact primitive IDs for composition-bearing segments or a blocker receipt.

**[TS-CMF-144] | LENS 3 | SEVERITY: WARNING**
- **Finding:** Section 7 defined UI components generically but did not name concrete files in the current `operator-web` structure, creating a risk that implementation would expand the monolithic `App.jsx`.
- **Location:** Section 7.
- **Required Action:** Add concrete React file targets for the route, provider, timeline components, API client, draft reducer, fixtures, and timeline styles.

**[TS-CMF-144] | LENS 4 | SEVERITY: CRITICAL**
- **Finding:** CBAR gates existed but lacked executable thresholds for frame alignment, primitive coverage, proxy/final parity, stale versions, scope isolation, hard blockers, and OTIO coverage.
- **Location:** Sections 13 and 14.
- **Required Action:** Add numeric/deterministic thresholds and downstream consequences for each gate, then connect them to acceptance criteria and tests.

**[TS-CMF-144] | LENS 3 | SEVERITY: WARNING**
- **Finding:** The PWA/Telegram boundary did not explicitly prohibit Telegram from submitting frame-level timeline edits or final video approval.
- **Location:** Section 12.
- **Required Action:** State that Telegram can notify, deep link, and create structured revision requests only, while timeline edits and final approval remain PWA/Command Bus governed.

**[TS-CMF-144] | LENS 5 | SEVERITY: WARNING**
- **Finding:** Fixture mode was mentioned, but production fallback behavior was not defined, leaving a path for mock `data.js` to masquerade as live timeline truth.
- **Location:** Sections 8, 12, 14, and 16.
- **Required Action:** Add explicit fixture flag requirements, visible fixture banner behavior, production unavailable/stale behavior, and tests that reject silent fixture fallback.

**[TS-CMF-144] | LENS 1 | SEVERITY: WARNING**
- **Finding:** The four video formats were named, but their timeline-specific visual and structural representation was under-specified for implementation.
- **Location:** Sections 2 and 8.
- **Required Action:** Add per-format timeline composition expectations for `SV-CSC`, `SV-EDU`, `SV-FRB`, and `SV-RRC`, including preview emphasis and lane obligations.

## SUMMARY STATISTICS

| Metric | Count |
|---|---:|
| Total specs reviewed | 1 |
| Specs with zero flags | 0 |
| Total CRITICAL flags | 2 |
| Total WARNING flags | 4 |
| Total NOTE flags | 0 |
| DEP-IDs flagged as PROPOSED requiring registration | 0 |
| Cross-spec consistency issues requiring arbitration | 0 |

