# Timeline Reuse Decision — V1.1 (Unchanged by GNM Boundary Correction)

## Decision

The campaign will not build a new timeline engine.

## Existing timeline sources

```text
THE_CMF_STUDIO(2).zip/
  src/ccp_studio/contracts/video_editing_engine.py
  src/ccp_studio/services/video_editing_engine_service.py
  src/ccp_studio/services/video_timeline_service.py
  src/ccp_studio/contracts/video_timeline_workbench.py
  src/ccp_studio/services/video_timeline_workbench_service.py
  src/ccp_studio/contracts/sonic_timeline.py
  src/ccp_studio/services/sonic_timeline_service.py
```

## Runtime mapping

```text
Accepted edit decisions
    ├── Remotion props, Sequence, Series, components, captions, and frame logic
    ├── HyperFrames HTML/CSS/GSAP timeline
    └── FFmpeg trim/cut/concat/audio/filter/encode graph
```

## Why an edit-decision contract still exists

Remotion is one embodiment. The Pipeline must also:

- route to HyperFrames or FFmpeg;
- validate before rendering;
- replay execution;
- inspect and amend decisions;
- record attribution and receipts;
- keep model output independent of renderer source code.

The contract is not a second timeline engine. It is the typed plan consumed by the
existing engines.

## Prohibited duplication

- New generic timeline database.
- New custom frame scheduler.
- New timeline editor UI.
- New cut/track object model unless the existing model cannot represent an accepted
  requirement and a compatibility amendment is approved.
