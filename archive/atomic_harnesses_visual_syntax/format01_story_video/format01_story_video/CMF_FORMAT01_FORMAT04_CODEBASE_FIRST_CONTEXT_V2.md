# CMF Studio Format 01 + Format 04 Codebase-First Drill Context V2

## Why this update exists

The previous context document was wrong in one important way: it treated the Format 01 composition board as if it were the main source of truth. That was not correct.

After inspecting `THE_CMF_STUDIO(2).zip`, Format 01 is clearly more mature than the board alone suggests. The codebase already contains a substantial Conscious Scene Builder system with scene templates, containers, components, effect stacks, research-backed selection rules, cognitive-load scoring, and runtime binding concepts.

This V2 document replaces the earlier board-first framing with a **codebase-first** framing.

Core correction:

> For mature formats, read the existing system first. Use visual boards as specimens, not as the canonical scene atlas.

The current CMF doctrine still applies:

> Visual syntax first. BBOX + WHY. Then primitive coalition. Then format/dish/runtime eval.

But for Format 01, the first step is:

```text
existing scene builder template
→ scene family / container / component / roll
→ visual recipe / effects / CLS / research overlay
→ BBOX + WHY mapping
→ primitive and runtime binding
```

not:

```text
visual board → invent six scenes
```

---

# 1. Grounded codebase findings for Format 01

## 1.1 Conscious Scene Builder Library

The key file is:

```text
reference/conscious-rivers/src/ccp/harness/intelligence/frameworks/intelligence_frameworks_scene_builder_library.md
```

I parsed **60 named scene templates** from this markdown library. The scene families include:

```text
HOOK
SETUP
CHALLENGE
JUXTAPOSITION
TURNING_POINT
RESOLUTION
ENCOURAGING_CHANGE
SYMBOLIC_ECHO
FRAME_CONTRAST
THE_TEASE
VOICE_OF_TRUTH
ARCHETYPAL_MOMENT
DEMONSTRATION
EVIDENCE
COMMUNITY
PAUSE
VIBE
VISION
```

This is the real Format 01-style scene grammar source, not the six-panel visual board.

The generated companion file in this bundle:

```text
format01_scene_builder_library_index.json
```

contains the parsed scene IDs, names, types, CLS values, elements, visual recipes, and effects.

## 1.2 Compiled Scene Builder Runtime

The codebase also contains:

```text
reference/conscious-rivers/src/ccp/harness/intelligence/scene_intelligence/runtime/scene_builder.runtime.json
```

From this runtime asset:

```json
{
  "runtime_asset_id": "SIRT-SCENE-BUILDER-v1",
  "runtime_version": "1.0.0",
  "active_containers_count": 6,
  "active_components_count": 19,
  "runtime_scene_templates_count": 25,
  "effect_library_count": 100,
  "evidence_refs_count": 52,
  "runtime_file": "reference/conscious-rivers/src/ccp/harness/intelligence/scene_intelligence/runtime/scene_builder.runtime.json",
  "scene_template_ids": [
    "HOOK-1-AB-2",
    "HOOK-2-B-1",
    "HOOK-3-BA-2",
    "HOOK-4-BA-2",
    "HOOK-5-AE-2",
    "SETUP-1-B-1",
    "SETUP-2-B-Montage-3-4",
    "SETUP-3-B-1",
    "SETUP-4-AB-2",
    "CHALLENGE-1-B-Montage-3-5",
    "CHALLENGE-2-AC-2",
    "CHALLENGE-3-B-Montage-4-6",
    "CHALLENGE-4-B-1",
    "TURNING_POINT-1-B-1",
    "TURNING_POINT-2-B-1",
    "TURNING_POINT-3-BB-2",
    "TURNING_POINT-4-BA-2",
    "RESOLUTION-1-B-1",
    "RESOLUTION-2-C-1",
    "RESOLUTION-3-B-1",
    "RESOLUTION-4-A-1",
    "VISION-1-B-Montage-3-4",
    "VISION-2-C-1",
    "VISION-3-C-1",
    "VISION-4-B-1"
  ]
}
```

This is important because it means the system already has a **runtime scene intelligence asset**. New Format Builder work should bind to this runtime instead of creating a parallel scene-template system.

## 1.3 Format 01 documentation and registries

Other grounded files include:

```text
docs/architecture/format-intelligence/FORMAT_01_CINEMATIC_STORY.md
docs/architecture/video-editing-engine/FORMAT_01_REALIZATION.md
registries/canonical/narrative_story_doctor/format01_story_extraction_profile.v1.json
registries/canonical/format_intelligence/format_required_ingredients.v1.json
registries/canonical/format_intelligence/format_activation_conditions.v1.json
registries/canonical/format_intelligence/format_composition_grammars.v1.json
registries/canonical/format_intelligence/format_forbidden_patterns.v1.json
registries/canonical/format_intelligence/sub_formats.v1.json
registries/canonical/format_intelligence/video_format_profiles.v1.json
```

These establish that Format 01 requires:

```text
A-roll story spine
emotional change map
cut-question chain
memory or proof object
B-roll contrast / foreshadowing function
power phrase plan
sonic story arc seed
```

and forbids:

```text
generic stock B-roll
pretty shot with no story function
synthetic primary delivery
sound overcompensation
text overload
motion outrunning the voice
```

## 1.4 Existing research overlay

The Scene Builder Library includes a research-backed intelligence overlay grounded in:

```text
LC4MP
Mayer multimedia principles
neurocinematics
eye-tracking continuity
peak-end theory
Kuleshov logic
audiovisual congruence
color PAD mapping
camera-motion research
```

This overlay defines:

```text
base CLS
target attention mode
ISC priority
memory role
AV congruence mode
continuity requirement
text policy
recommended duration
max primary visual units
peak-end weight
```

This is exactly the type of intelligence the new Visual + Sonic Composition Syntax doctrine should preserve and extend.

---

# 2. Corrected Format 01 interpretation

Format 01 should now be described as:

```text
A-roll-led Cinematic Story Commentary with a mature Conscious Scene Builder library,
research-backed scene selection rules, A/B/C/E-roll roles, CAC/GMG/Cinematic B-roll
routes, effect stacks, cognitive-load logic, and Video Editing Engine laws.
```

Do not reduce it to:

```text
a six-scene cinematic story board
```

The six-panel image board is useful as a visual specimen, but it is only one board. It can help Drill-me one visual style, but it must not override the existing 60-scene library or runtime scene builder.

---

# 3. Updated Format 01 workstream plan

## 3.1 Do not invent scenes first

The Format 01 workstream must begin with a mapping task:

```text
scene_builder_library.scene_id
→ scene family
→ elements / rolls
→ visual_recipe
→ effects
→ CLS
→ research contract
→ BBOX + WHY requirements
→ visual primitives
→ sonic primitives
→ design primitives
→ business primitives
→ memetic expression primitives if human/pose/gaze appears
→ runtime owner
→ QA gates
```

## 3.2 Scene Builder to BBOX + WHY bridge

Every existing scene template should become a BBOX + WHY candidate. For example:

```json
{
  "scene_id": "HOOK-2-B-1",
  "name": "The Cinematic Foreshadow",
  "existing_visual_recipe": "Single, slow, mysterious B-Roll shot + Cryptic VO.",
  "new_mapping_needed": {
    "bbox_why_map": "required",
    "source_reference_policy": "required",
    "visual_primitives": ["attention_path", "negative_space", "visual_rhythm"],
    "sonic_primitives": ["silence", "breath_pause", "emotional_bed"],
    "qa_gates": ["no_generic_broll", "source_or_symbolic_function_present"]
  }
}
```

## 3.3 Preserve existing scene IDs

Do not rename the scene IDs until a migration plan exists. Scene IDs such as:

```text
HOOK-1-AB-2
SETUP-3-B-1
CHALLENGE-2-AC-2
TURNING_POINT-4-BA-2
RESOLUTION-4-A-1
EVIDENCE-1-C-1
PAUSE-4-A-1
VISION-3-C-1
```

are already part of the system. The Format Builder should add syntax metadata to them, not erase them.

## 3.4 Updated Format 01 Drill-me prompt

Use this prompt in the next Format 01 chat:

```text
CMF FORMAT 01 CODEBASE-FIRST DRILL-ME MODE

Do not invent Format 01 scenes.
Do not summarize the visual board first.

First inspect the codebase files:
- reference/conscious-rivers/src/ccp/harness/intelligence/frameworks/intelligence_frameworks_scene_builder_library.md
- reference/conscious-rivers/src/ccp/harness/intelligence/scene_intelligence/runtime/scene_builder.runtime.json
- docs/architecture/format-intelligence/FORMAT_01_CINEMATIC_STORY.md
- docs/architecture/video-editing-engine/FORMAT_01_REALIZATION.md
- registries/canonical/narrative_story_doctor/format01_story_extraction_profile.v1.json
- registries/canonical/format_intelligence/

Then produce:
1. scene template count
2. scene family taxonomy
3. roll/element taxonomy
4. existing effects and runtime summary
5. research overlay summary
6. gaps against Visual + Sonic Composition Syntax Doctrine
7. BBOX + WHY mapping plan for every scene family
8. Drill-me prompts per scene family
9. migration strategy that preserves existing scene IDs

Only after this audit may you Drill-me a visual board specimen.
```

---

# 4. Format 01 risks and protections

## Risk: generic cinematic montage

Format 01 already has enough cinematic scene ideas. Its risk is not shortage of scenes. Its risk is misusing the scene builder to produce pretty but source-weak montage.

Protection:

```text
A-roll spine check
source-span refs
B-roll story function
memory/proof object binding
cut-question chain
sonic story arc
no generic stock B-roll
CLS rhythm validator
```

## Risk: new doctrine overwriting old intelligence

The Visual + Sonic Composition Syntax Doctrine must not replace the Scene Builder. It should extend it.

Protection:

```text
legacy scene ID preservation
scene_template_binding_receipts
runtime asset version tracking
BBOX + WHY as additional metadata
no parallel scene atlas unless explicitly migrated
```

---

# 5. Format 04 codebase-backed context

Format 04 is less scene-builder-mature than Format 01, but it is not a blank slate either.

Grounded files include:

```text
docs/architecture/format-intelligence/FORMAT_04_CONSCIOUS_REACTIONS.md
docs/architecture/video-editing-engine/FORMAT_04_REALIZATION.md
docs/architecture/format-intelligence/FORMAT_INTELLIGENCE_INTEGRATION_MAPPING.md
docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md
registries/canonical/format_intelligence/sub_formats.v1.json
registries/canonical/format_intelligence/format_memetic_cue_policies.v1.json
registries/canonical/format_intelligence/format_required_ingredients.v1.json
```

These establish that Format 04 requires:

```text
debate tension
reaction UI surface
ranking / poll / score / tier state
meme mechanism
high-arousal justification
```

and forbids:

```text
zoom spam
meme cue trivializing serious source
ranking surface without real tension
score state not tied to argument shift
```

The Video Editing Engine adds hard laws:

```text
debate tension required
reaction UI surface required
zoom event needs argument shift
memetic cue spacing >= 10 seconds
seriousness gate protects source meaning
```

## 5.1 Format 04 runtime binding is already specified

The key spec is:

```text
docs/tech-specs/TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md
```

That spec explicitly says reaction templates must not become a parallel template system. They must bind to the existing CMF scene intelligence model: container, component, scene template, effect stack, text policy, cognitive load, attention mode, continuity requirement, and asset-roll role.

It defines compatibility rules for reaction templates such as:

```text
VRS-SPLIT
TRK-TIER
RNK-BLIND
RNK-PROPOSAL
ELM-BRACKET
MIR-QUIZ
AUTH-LADDER
```

This aligns strongly with the Format 04 visual board. The board should be mapped into these template route codes, not invented as unrelated dish IDs.

## 5.2 Corrected Format 04 interpretation

Format 04 should be described as:

```text
Conscious Reactions Editing: a high-arousal, Remotion-native reaction UI format
for debate, ranking, tournament, tier-list, myth-breaking, score-state, and
participatory clips, requiring reaction UI surface, debate tension, memetic policy,
and scene-template runtime binding.
```

The visual board is useful because it shows UI composition candidates, but the codebase already contains the route/template direction.

## 5.3 Format 04 Drill-me prompt

```text
CMF FORMAT 04 CODEBASE-FIRST DRILL-ME MODE

Do not invent reaction templates.
First inspect:
- FORMAT_04_CONSCIOUS_REACTIONS.md
- FORMAT_04_REALIZATION.md
- TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md
- format_intelligence registries
- reaction template route contracts if present

Then map the selected visual board specimen to:
1. reaction template code candidate
2. runtime scene template candidate
3. reaction UI surface BBOX
4. ranking/poll/score/tier state BBOX
5. human reaction BBOX
6. caption/prompt BBOX
7. evidence/source requirements
8. motion/memetic cue policy
9. Remotion ownership
10. QA gates

Block if:
- no debate tension
- no reaction UI surface
- ranking has no argument shift
- meme cue trivializes serious source
- zoom event lacks argument shift
- scene-template binding is missing
```

---

# 6. Updated bundle guidance

The previous `CMF_FORMAT01_FORMAT04_DRILL_CONTEXT_BUNDLE` should be replaced by this V2 bundle.

New included files:

```text
CMF_FORMAT01_FORMAT04_CODEBASE_FIRST_CONTEXT_V2.md
format01_scene_builder_library_index.json
format01_runtime_scene_builder_summary.json
```

The Format 01 visual board remains useful only as a specimen. It should not be treated as the system’s scene atlas.

---

# 7. Final corrected principle

For Format 01:

```text
Map existing intelligence first. Add BBOX + WHY second. Only invent after gaps are proven.
```

For Format 04:

```text
Bind visual board dishes to existing reaction template route and scene-template runtime binding logic.
```

For both:

```text
visual specimen
→ codebase source check
→ BBOX + WHY
→ primitive bindings
→ runtime binding
→ QA gates
→ Drill-me approval
```
