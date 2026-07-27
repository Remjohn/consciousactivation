# Visual Preproduction V1 Object Model

## Canonical pipeline

```text
VisualPreproductionRequest
↓
VisualSchema
↓
StoryboardIngredientSet
↓
VisualBeatPlan
↓
PRIMALAnalysis
↓
VAEDecoderReport
↓
ConstraintGateCReport
↓
VisualAnalystReport
↓
StoryboardCommanderVerdict
↓
VisualPreproductionPacket
```

## Main objects

### VisualSchema

The canonical visual research output. It captures recognizable real-world context, environment logic, human context, object logic, light, color, tropes, source authority, negative-space risks, style constraints, and asset requirements.

### VisualFamiliarityElementAssessment

Typed checklist item for the 16 Elements of Visual Familiarity. Each element must be filled or explicitly marked not applicable with a reason.

### StoryboardIngredientSet

Converts VisualSchema into production ingredients: character anchors, environment anchors, object anchors, proof objects, memory objects, micro-semiotic anchors, style references, composition references, lighting requirements, shot requirements, and asset retrieval requirements.

### VisualBeatPlan

Maps a source beat/slide/scene/single-image directive to visual logic: viewer-state target, visual question, payoff, shot type, T-Code, V-Code, kinetic verb, camera moral stance, environment, subject, object, light, forbidden visuals, and style constraints.

### PRIMALAnalysis

Typed analysis for:
- Feeling
- Body Truth
- Environment
- Timestamp / Temporal Context
- Uniqueness

### VAEDecoderReport

Semantic check, shadow filter, anti-cliché gate, forbidden interpretations, generic visual risks, primitive drift risks, source drift risks, and repair recommendations.

### ConstraintGateCReport

Hard gate for character anchor, lighting/cliché, source authority, word count physics, shot distribution, cascade lock, style route compatibility, frame profile compatibility, and asset coverage.

### VisualAnalystReport

Detailed validation of T-Code, V-Code, character anchor consistency, environment logic, source accuracy, arc progression, uniqueness, camera directive passthrough, lighting preset validity, kinetic verb validity, and prompt physics.

### StoryboardCommanderVerdict

Batch-level authorization for carousel sequence, video scene batch, motion sequence, or high-value storyboard packet.

### VisualPreproductionPacket

Frozen output consumed by SuperVisual, Carousel, Video, Style Route, Composition, and Provider Job Planning.
