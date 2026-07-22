# Format Intelligence Integration Mapping

Format Intelligence V1 consumes source-backed extraction packets from Narrative Story Doctor / Content Extraction Intelligence and compiles format-specific realization programs. It does not read raw transcripts as its primary input and it does not invent missing ingredients.

## Compiler Boundary

```text
Narrative Story Doctor / Extraction Intelligence
-> GenericExtractionPacketRef
-> FormatIntelligenceProgram
-> FormatCommanderVerdict
-> EngineAdapterPayload
-> Visual Preproduction / Asset Intelligence / Style Route / Composition / Component Engine
```

Extraction Intelligence answers:

```text
What did the interview actually give us?
```

Format Intelligence answers:

```text
How should this extracted meaning be expressed inside this specific content format?
```

## Extraction Packet To Format Program Mapping

| Narrative Story Doctor Output | Format Intelligence Program | Primary Format Law | Downstream Engine Target |
|---|---|---|---|
| `Format01StoryExtractionPacket` | `Format01CinematicStoryProgram` | Requires A-roll story spine, emotional change map, and cut-question chain. | Video Editing Engine / Cinematic Story Commentary |
| `Format02ExplainerExtractionPacket` | `Format02AvatarPaperCutExplainerProgram` | Requires teachable mechanism, concept nodes, diagram sequence, and avatar or paper-cut policy. | 2D Character Animation / Paper-Cut Explainer / Video Editing Engine |
| `Format03ReactionExtractionPacket` | `Format03LivingCommentaryReactionProgram` | Requires proof or quote surface and a reaction angle. | Living Commentary Reaction Engine / Video Editing Engine |
| `Format04ConsciousReactionExtractionPacket` | `Format04ConsciousReactionEditingProgram` | Requires debate tension and reaction UI surface. | Conscious Reactions Editing / Ranking / Poll / Debate UI Engines |
| `SuperVisualExtractionPacket` | `SuperVisualFormatProgram` | Requires one single source truth, visual hook, and edge product. | SuperVisual Builder |
| `CarouselExtractionPacket` | `CarouselFormatProgram` | Requires closure contract and continuous sequence grammar. | Carousel Engine |
| `MemeVisualExtractionPacket` | `MemeVisualFormatProgram` | Requires meme mechanism and risk boundary. | Meme Visual Engine |
| `PollVisualExtractionPacket` | `PollVisualFormatProgram` | Requires at least two meaningful options. | Poll Visual Engine |
| `ReactionSeedPacket` | `ReactionSeedFormatProgram` | May store only; does not require immediate production. | Reaction Seed Store / Future Reaction Engine |

## Generic Extraction Reference

All Narrative Story Doctor outputs should be normalized into `GenericExtractionPacketRef` before entering `FormatIntelligenceService`.

Required fields:

- `packet_id`
- `source_system`
- `format_id`
- `source_span_refs`
- `payload`

The payload carries packet-specific facts such as:

- `a_roll_story_spine`
- `cut_question_chain`
- `teachable_mechanism`
- `proof_or_quote_surface`
- `debate_tension`
- `single_source_truth`
- `carousel_thesis`
- `closure_contract`
- `meme_mechanism`
- `poll_options`

Format Intelligence can reject a packet if required payload ingredients are missing. It must not infer missing ingredients from tone, brief expectations, or generic format conventions.

## Downstream Target Chain

`FormatIntelligenceProgram` is not final production output. It is the recipe contract consumed by downstream systems:

```text
FormatIntelligenceProgram
-> Visual Preproduction
-> Asset Intelligence
-> Style Route
-> Composition
-> Component Engine
```

Target-specific examples:

- `Format01CinematicStoryProgram` should feed video composition, A-roll editing, memory-object policy, B-roll policy, subtitle policy, sound doctrine, and proof policy.
- `Format02AvatarPaperCutExplainerProgram` should feed visual preproduction, paper-cut layer planning, 2D character/avatar performance policy, concept-node diagrams, rough notation targets, and motion doctrine.
- `Format03LivingCommentaryReactionProgram` should feed reaction surface policy, quote/proof cards, human reaction framing, subtitle timing, and proof-preserving edits.
- `Format04ConsciousReactionEditingProgram` should feed reaction UI surfaces, ranking/poll/debate templates, score states, faster motion doctrine, and tighter memetic cue policy.
- `SuperVisualFormatProgram` should feed SuperVisual composition hypotheses and layer stack decisions.
- `CarouselFormatProgram` should feed Carousel sequence grammar, slide roles, claim mapping, and closure-contract enforcement.

## Authorization And Adapter Boundary

Every format program must pass through `FormatCommanderVerdict` before an `EngineAdapterPayload` can be compiled.

Authorization requires:

- required ingredient checklist pass;
- source span refs present;
- memetic cue policy compliance;
- style route policy compliance;
- render requirement compliance;
- no provider calls during final render.

`EngineAdapterPayload` then carries the authorized recipe into a component engine. Component engines consume this payload; they do not invent new format doctrine.

## Not Wired In This Branch

This branch does not directly wire:

- Narrative Story Doctor services into `FormatIntelligenceService`;
- `SuperVisualFormatProgram` into `SuperVisualBuilderService`;
- `CarouselFormatProgram` into `CarouselEngineService`;
- Video format programs into Remotion, FFmpeg, Motion Canvas, or the Video Editing Engine;
- real Visual Preproduction, Asset Intelligence, Style Route, provider, or render calls.

Those integrations should happen after the deterministic V1 compiler and tests remain stable.
