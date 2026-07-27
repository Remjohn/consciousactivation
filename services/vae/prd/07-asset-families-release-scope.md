---
title: Asset Families and Release Scope
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
asset_family_count: 8
---

# Asset Families and Release Scope

## Canonical asset-family ontology

### AF-01 — Documentary and Photographic Evidence

Real-world/editorial photography, archival evidence, screenshots, documents, products, places, events, and human action.

### AF-02 — Human and Character Assets

Real-person portraits, non-identifiable human subjects, 2D characters, identities, poses, expressions, gestures, gaze, props, and interactions.

### AF-03 — Illustrated and Generated Scenes

Symbolic tableaux, narrative/editorial illustration, conceptual scenes, environment plates, and object studies.

### AF-04 — UI, Interface, and Screen Surfaces

App interfaces, chat surfaces, dashboards, social posts, browser frames, device mockups, and data panels.

### AF-05 — Diagrammatic and Informational Assets

Charts, graphs, frameworks, matrices, timelines, maps, comparison boards, processes, and annotated proof.

### AF-06 — Typography and Graphic Elements

Titles, labels, badges, quote cards, captions, numbers, verdict markers, shape systems, and textures.

### AF-07 — Compositing and Scene Components

Cutouts, foreground/background plates, overlays, masks, shadows, reflections, particles, and depth layers.

### AF-08 — Motion and Temporal Assets

Video clips, loops, transitions, animated backgrounds, character animation, kinetic typography, camera moves, and effects.

## Certification states

```text
represented
→ experimental
→ benchmarked
→ shadow
→ limited-production
→ production-certified
→ deprecated
→ retired
```

A family may be represented structurally without being eligible for production routing.

## Release 1 production claim

Release 1 is anchored to **AF-02 Human and Character Assets** for the **2D Character Animation** category and **Format 02 Minimal Coach Theatre**. The certified slice must cover:

- character identity;
- pose;
- expression;
- gesture;
- gaze;
- held or interacted-with props;
- simple environment/scene plate;
- transparent character cutout;
- continuity;
- composition-conditioned geometry;
- ComfyUI generation and transformation;
- independent VLM evaluation;
- targeted repair;
- immutable promotion and result delivery;
- downstream Remotion composition consumption.

A limited subset of AF-03 may be used for environment or simple illustrated scene support, but it must be separately identified in the release receipt.

## Structurally represented, initially uncertified

- complex documentary acquisition and external retrieval;
- advanced UI reconstruction;
- advanced data visualization;
- long-form or multi-shot video generation;
- complex character animation and lip sync;
- advanced VFX;
- general-purpose human capture operations.

The product and Control Tower must not imply production support for these capabilities before their own benchmark and certification gates pass.
