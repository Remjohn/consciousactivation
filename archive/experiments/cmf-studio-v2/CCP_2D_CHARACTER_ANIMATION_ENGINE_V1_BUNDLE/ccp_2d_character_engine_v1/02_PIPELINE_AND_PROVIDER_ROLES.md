# Provider and Pipeline Responsibilities

## 1. Provider boundary rule

Every provider implements a narrow typed contract. No provider owns the full workflow.

```text
Python harness decides meaning and routing.
Providers execute bounded transformations.
The operator approves promoted assets.
Renderers consume frozen contracts.
```

## 2. See-Through provider

### Input

- approved rig-aware source illustration;
- character identity reference;
- target canonical part tags;
- desired output resolution;
- decomposition policy.

### Output

- layered PSD candidate;
- semantic masks;
- depth map;
- inferred drawing order;
- hidden-region inpainting;
- decomposition report;
- model/version receipt.

### Does not own

- final semantic approval;
- pivots;
- meshes;
- bones;
- animation;
- production release.

### Production caveat

Treat it as the default route only for supported illustration/anime-like characters. Real-photo or mixed-media personal-brand assets require alternate decomposition routing.

---

## 3. Qwen-Image-Layered provider

### Role

General-purpose semantic RGBA decomposition for flat generated scenes or mixed-media character art.

### Best uses

- photo-paper-cut character layers;
- props and costumes;
- complex generated poster scenes;
- recovery of reusable layers from composition plates.

### Output

- ordered RGBA layers;
- semantic grouping proposal;
- alpha-quality report.

### Follow-up

SAM3 refines precise masks; GPT Image/Flux repairs missing or contaminated regions.

---

## 4. SAM3 provider

### Role

Precise segmentation, alpha cleanup, object isolation, and tracking.

### Uses

- portrait cutout refinement;
- hand and prop isolation;
- layer-edge repair;
- background removal;
- mask generation for inpainting;
- tracked cutouts from source interview footage.

SAM3 is not a layered rig generator.

---

## 5. GPT Image / Flux provider

### Role

- rig-aware master-art generation;
- identity-preserving edits;
- hidden-region repair;
- costume and hand variants;
- paper texture harmonization;
- targeted correction after QC failure.

### Restriction

The provider output is always a candidate asset. It cannot be referenced by production programs until approved and versioned.

---

## 6. Stretchy Studio authoring adapter

### Role

- PSD import;
- hierarchy normalization;
- pivot editing;
- heuristic or DWPose-assisted rigging;
- mesh generation;
- limb weighting;
- shape-key authoring;
- direct vertex keyframes;
- audio-synced preview;
- runtime export.

### CCP integration

Create an importer/exporter that translates Stretchy project data into canonical Pydantic contracts.

The `.stretch` project remains an authoring artifact, not semantic source of truth.

---

## 7. Spine compiler/runtime provider

### Role

- bones;
- slots;
- skins;
- attachments;
- weighted meshes;
- animation tracks;
- deform timelines;
- clipping;
- IK constraints;
- layered playback.

### Important build rules

- pin editor/export/runtime versions;
- preserve local-space pivots;
- convert coordinate systems explicitly;
- bake unsupported warp deformations into deform timelines;
- review license requirements before distribution.

---

## 8. Motion Canvas choreography provider

### Input

Frozen `TwoDCharacterProgram` scene choreography section.

### Owns

- scene-level motion;
- camera movement;
- character placement;
- diagram timing;
- teaching object paths;
- procedural arrows and transitions.

### Does not own

- acting-state selection;
- transcript interpretation;
- brand doctrine;
- final approval.

---

## 9. Remotion compositor

### Input

- frozen program;
- character runtime bundle or RGBA plate;
- subtitles;
- scene assets;
- brand render profile.

### Owns

- final frame composition;
- deterministic typography;
- platform safe zones;
- scene sequencing;
- background and overlay layers;
- final render invocation.

### Randomness

All procedural jitter uses explicit seeds.

---

## 10. FFmpeg finishing provider

### Owns

- video/audio mux;
- codec and pixel format;
- loudness normalization;
- voice-priority music ducking;
- trim and padding;
- preview derivatives;
- final master verification.

### Does not own

- semantic timing;
- gestures;
- scene structure;
- subtitles;
- identity decisions.
