# Evaluations, Approval, and Repair

## 1. Character Genesis gates

### Identity

- likeness;
- age consistency;
- skin tone;
- hair and silhouette;
- body proportion;
- approved stylization;
- no unwanted beautification.

### Decomposition

- semantic labels;
- hidden-region completeness;
- alpha quality;
- layer fusion;
- draw order;
- material continuity.

### Rig

- pivots;
- joint bending;
- mesh inversion;
- mask leakage;
- eye clipping;
- mouth deformation;
- costume and prop compatibility;
- runtime export parity.

## 2. Per-program gates

### Source alignment

- beat map pinned;
- source words preserved;
- timing confidence;
- no unapproved synthetic speech;
- exact audio duration.

### Performance

- emotional match;
- gesture timing;
- gaze logic;
- mouth sync;
- transition legality;
- motion restraint;
- performance diversity.

### Primitive and doctrine compliance

- target primitives expressed;
- prohibited primitives absent;
- Negative Space respected;
- trauma safety respected;
- Micro-Semiotic Anchors subtle;
- character does not make unsupported claims.

### Technical

- no missing textures;
- no alpha bleed;
- no frame drift;
- no audio clipping;
- correct output size;
- reproducibility receipt complete.

## 3. Preview hierarchy

### Rig Debug Preview

Display bones, pivots, meshes, masks, weights, draw order, and attachment IDs.

### Performance Blocking Preview

Display a neutral background plus:

- transcript;
- beat name;
- acting state;
- gesture markers;
- gaze target;
- primitive target;
- viseme label.

### Final Composition Preview

Full scene, subtitles, audio, SFX, and platform framing.

## 4. Typed repair commands

Supported command families:

```text
MOVE_PIVOT
REPAIR_MASK
REORDER_LAYER
REPLACE_ATTACHMENT
REPLACE_HAND_POSE
CHANGE_ACTING_STATE
REDUCE_GESTURE_AMPLITUDE
SHIFT_GESTURE_STROKE
CHANGE_GAZE_TARGET
REMAP_VISEME
CHANGE_COSTUME_SKIN
ATTACH_PROP
DETACH_PROP
REMOVE_MICRO_SEMIOTIC_ANCHOR
REDUCE_PAPER_JITTER
CHANGE_MIX_DURATION
```

Each command creates a new version or revision. Approved versions are immutable.

## 5. Operator approval lifecycle

```text
draft
→ compiled
→ automatic_eval_failed | blocking_preview_ready
→ revision_requested | final_preview_ready
→ approved_for_render
→ rendering
→ rendered
→ final_qc
→ approved_for_publish
→ archived
```

## 6. Receipt chain

Every final output records:

- context IDs;
- character version IDs;
- program hash;
- repair history;
- evaluation results;
- operator ID and approval timestamp;
- runtime versions;
- asset hashes;
- final output hashes.
