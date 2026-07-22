# Video Studio Timeline Adoption Decision

## Decision

Archive the current `VideoTimelineWorkbench.jsx` timeline implementation as a
noncanonical prototype. Reuse only its useful product shell, route, API/view-model
patterns, receipt concepts, and review interactions.

Do not build a timeline widget from scratch.

## Canonical architecture

```text
existing CMF edit decisions and timeline contracts
        ↓
Timeline Adapter
        ↓
adopted timeline UI foundation
        ↔
Remotion Player preview
        ↓
operator direct manipulation or text request
        ↓
typed ChangeRequestProgram
        ↓
Pipeline validation and affected-node rerun
        ↓
Remotion / HyperFrames / FFmpeg realization
```

The timeline UI is a projection and correction surface. It is not the source of
workflow meaning.

## Candidate foundations to evaluate

### Candidate A — Official Remotion Timeline / Editor Starter

Strengths:
- native synchronization with Remotion Player;
- track, item, drag/drop, timing and keyframe-oriented patterns;
- fastest route to a Remotion-native interface.

Constraint:
- commercial product/licensing decision.

### Candidate B — Elah timeline/editor foundation

Strengths:
- Apache-2.0;
- integer-frame time model;
- React timeline package;
- tracks, clips, trim, split, snapping and preview infrastructure;
- renderer-agnostic.

Use:
- timeline UI and interaction foundation while Remotion remains final temporal
  composition/render embodiment.

### Candidate C — Twick Studio/timeline

Strengths:
- full React timeline/canvas/player packages;
- AI captions and cloud/export integration;
- S3 and GCS upload paths.

Constraint:
- Sustainable Use License and product-distribution terms require an explicit adoption
  decision.

### Candidate D — limited open Remotion editor examples

Use only as reference or bootstrap after exact license review. Do not copy code from a
repository that lacks an explicit compatible license.

## Selection campaign

Run a two-day spike using the same accepted CMF edit-decision fixture.

Measure:

- frame-accurate scrubbing;
- multi-track video/audio/text/caption support;
- trim, split, move, ripple and snapping;
- Remotion Player synchronization;
- JSON serialization;
- mapping to existing CMF edit decisions;
- performance with representative projects;
- accessibility and keyboard operation;
- license fit;
- effort to integrate typed correction commands.

## Recommendation

Use the official Remotion Timeline when the commercial license is acceptable.

Otherwise use Elah as the preferred open-source timeline interaction foundation and
connect it to Remotion Player and the existing CMF edit-decision contract.

Do not adopt a full client-side renderer as the product rendering authority merely
because its timeline UI is attractive.
