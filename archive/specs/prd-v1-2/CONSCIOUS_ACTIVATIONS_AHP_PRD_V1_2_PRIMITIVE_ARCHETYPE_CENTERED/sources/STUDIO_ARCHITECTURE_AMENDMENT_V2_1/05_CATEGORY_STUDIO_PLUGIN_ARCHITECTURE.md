# Category-Native Studio Plugin Architecture

## Decision

Build one Conscious Activations Studio application with several category-native Studio
modules.

Do not build a separately deployed product for every Category.

## Shared Studio shell

```text
Workspace selector
Project browser
Campaign launcher
Harness catalog
Binding editor
Live run graph
Review inbox
Evidence and receipts
Artifacts and publishing
Workers, providers, budgets and system health
```

## Category-native modules

### Interview Expression Studio

Owns:
- Complete Expression Session;
- guest/audience context;
- Expression Moments;
- Ingredient Inventory;
- Asset Package Spec;
- downstream launch decisions.

### Static Composition Studio

Contains two modes sharing Skia, PRETEXT, BBOX, visual ingredients and evaluation:

```text
Carousel Studio
SuperVisual Studio
```

Each mode has its own sequence/hierarchy behaviors without becoming a separate
application.

### Video Production Studio

Owns:
- source footage and assets;
- automated edit plan;
- timeline supervision;
- candidate comparison;
- captions, audio and motion;
- Remotion, HyperFrames and FFmpeg outputs;
- revision requests.

### Visual Asset Studio

Owns:
- VAE demands;
- candidates;
- SAM3;
- Lucida;
- GNM;
- ComfyUI;
- asset repair and acceptance.

### Knowledge and Programmed Model Studio

Owns:
- Skills and Steering Recipes;
- retrieval evidence;
- JIT Capsules;
- datasets;
- benchmarks;
- Programmed Model claims;
- shadow replay and promotion.

### Future Character Performance Studio

Status:
`DEFERRED_AWAITING_FORMAT02_HARNESS`.

It is registered only after the current Harness exists.

## Harness-to-Studio routing

Every Harness declares its primary and supporting Studio surfaces.

```yaml
studio_surface_binding:
  primary_surface: VIDEO_PRODUCTION_STUDIO
  supporting_surfaces:
    - VISUAL_ASSET_STUDIO
    - KNOWLEDGE_MODEL_STUDIO
  operator_entry_policy: EXCEPTION_ONLY
```

The Studio surface does not change Harness meaning. It presents the relevant state,
tools, artifacts, evidence and human decisions.
