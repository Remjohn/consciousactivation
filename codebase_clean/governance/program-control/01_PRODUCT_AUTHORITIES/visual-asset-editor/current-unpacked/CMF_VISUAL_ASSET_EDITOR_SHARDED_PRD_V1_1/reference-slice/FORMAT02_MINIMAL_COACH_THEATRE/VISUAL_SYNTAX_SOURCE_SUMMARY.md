# Format 02 Visual Syntax Source Summary

## Canonical source entries

- `VISUAL SYNTAX BUILDER/CCP_VISUAL_SONIC_COMPOSITION_SYNTAX_DOCTRINE_V1_INTEGRATION_BUNDLE/docs/architecture/visual-sonic-composition-syntax/FORMAT02_MINIMAL_COACH_THEATRE.md`
- `VISUAL SYNTAX BUILDER/CCP_VISUAL_SONIC_COMPOSITION_SYNTAX_DOCTRINE_V1_INTEGRATION_BUNDLE/registries/canonical/skills/format02_scene_syntax.select/SKILL.md`
- `VISUAL SYNTAX BUILDER/CCP_VISUAL_SONIC_COMPOSITION_SYNTAX_DOCTRINE_V1_INTEGRATION_BUNDLE/registries/canonical/visual_sonic_composition_syntax/format02_ingredient_identities.json`

## Source-derived laws

# Format 02 Minimal Coach Theatre

## Active element law
Maximum 3 active elements:
1. Guide character/body/gesture.
2. Text field/paper card/written thought.
3. Meaning object/proof/diagram/icon.

## Hard laws
- 9:16 vertical.
- No lip sync.
- Big negative space.
- Deterministic text.
- Prop carrying requires attachment points.
- Avoid default centered front-facing gaze.
- Remotion-first runtime.

## Ingredient identity record

```json
{
  "format": "format_02_minimal_coach_theatre",
  "active_element_limit": 3,
  "ingredients": [
    "guide_character",
    "text_field",
    "meaning_object"
  ],
  "hard_laws": [
    "9:16",
    "no_lip_sync",
    "deterministic_text",
    "big_negative_space",
    "remotion_first"
  ]
}
```

## Product interpretation for Release 1

These source laws establish that asset production is not generic illustration. A valid character asset must be produced for a specific scene-syntax role and must leave room for the deterministic text and meaning-object system owned by the harness.

The Visual Asset Editor therefore needs explicit registries and contracts for:

- character identity;
- pose and body state;
- expression;
- gaze;
- gesture;
- prop attachment;
- environment/world state;
- camera and crop suitability;
- transparent and layered delivery;
- continuity across multiple scenes;
- recurrence in Visual Syntax context.

The editor does not generate or own lip sync for this reference profile.

## Required Visual Syntax context fields

```text
scene_id
sequence_position
active_element_count
character_syntactic_role
text_field_bbox
meaning_object_bbox
character_bbox_intent
gaze_relationship
gesture_relationship
negative_space_requirement
recurrence_intent
activative_function
```

## Architecture questions to resolve

- Which exact Atomic Harness promise within Format 02 becomes the reference target?
- Which recurring character identity is authorized for the first identity LoRA or adapter proof?
- Which pose/expression/gesture taxonomy is sufficient for limited production?
- Which output layers and masks must Remotion receive?
- Which VLM labels best distinguish skepticism, concern, recognition, conviction, and contempt?
