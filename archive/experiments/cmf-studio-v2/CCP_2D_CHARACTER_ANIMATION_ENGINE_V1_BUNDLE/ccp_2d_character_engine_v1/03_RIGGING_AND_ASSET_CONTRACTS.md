# Rigging and Asset Contracts

## 1. PSD normalization

A valid production PSD must preserve full-canvas coordinates for every layer. Individual layers must not be destructively cropped unless the crop rectangle and canvas transform are recorded.

Each layer requires:

```json
{
  "layer_id": "forearm_L",
  "semantic_type": "forearm",
  "side": "left",
  "source_name": "left-arm-2",
  "draw_order": 42,
  "canvas_rect": [408, 612, 310, 492],
  "pivot_hint": [0.49, 0.11],
  "parent_hint": "upper_arm_L",
  "mask_ids": [],
  "material_id": "paper_skin_v1",
  "sha256": "..."
}
```

## 2. Layer graph

The layer graph stores:

- parent/child groups;
- sibling drawing order;
- semantic body part;
- source texture;
- masks;
- attachment role;
- material binding;
- visibility defaults;
- deformation margin.

Draw-order changes must be explicit timeline events.

## 3. Bone graph

Each bone stores:

- bone ID;
- parent ID;
- setup translation;
- setup rotation;
- scale and shear;
- pivot coordinates;
- rotation limits;
- bend preference;
- constraint memberships.

## 4. Mesh bundle

Large mesh data belongs in binary sidecars referenced by URI and hash.

For each mesh:

- rest vertices;
- UVs;
- triangle indices;
- bone indices;
- normalized weights;
- boundary contour;
- deformation safety bounds;
- associated attachment;
- material ID.

## 5. Masks and clipping

Masks must be explicit assets with stable IDs.

Use clipping for:

- irises inside eye whites;
- mouth interior;
- clothing overlap;
- hair behind face;
- props passing behind hands;
- paper edge reveal.

## 6. Shape-key bundle

Each shape key stores:

- target mesh;
- delta sidecar;
- legal range;
- compatible keys;
- exclusion group;
- approved extreme-frame previews.

## 7. Hand library

Recommended attachment variants:

```text
rest
open
point
pinch
fist
thumb_up
hold_card
hold_phone
hold_cup
hand_on_heart
thinking
```

Every variant must share wrist anchor, canvas, material, and lighting.

## 8. Mouth library

Recommended mouth attachments:

```text
REST
MBP
ETC
E
AI
O
U
FV
L
SMILE
FROWN
```

The engine may blend small shape-key changes on top of attachment swaps.

## 9. Gaze library

Semantic targets:

```text
camera
interviewer
memory_left
memory_right
teaching_object
quote_card
poll_A
poll_B
audience
down_reflective
```

Each gaze target defines iris position, optional head offset, blink policy, and return policy.

## 10. Costume and prop skins

Costumes and props are modular attachments, not duplicated rigs.

Examples:

```text
founder_black_tshirt
formal_green_blazer
paper_cut_blue_shirt
podcast_casual
fitness_outfit

tea_cup
paper_arrow
notebook
phone
microphone
sign_board
```

Micro-Semiotic Anchors are implemented as approved costume or prop variants.

## 11. Warp deformation export

If the target runtime lacks a native warp-deformer concept:

1. sample the source parameter range;
2. evaluate the deformed lattice;
3. apply the deformation to rest vertices;
4. calculate per-vertex deltas;
5. emit deform keyframes;
6. validate golden frames against the authoring preview.

## 12. Rig release gate

A CharacterRigVersion may be locked only after:

- semantic layer QC;
- hidden-region QC;
- pivot QC;
- mesh inversion test;
- extreme-pose test;
- hand/prop attachment test;
- face and eye clipping test;
- mouth library test;
- costume-switch test;
- deterministic export test;
- operator approval.
