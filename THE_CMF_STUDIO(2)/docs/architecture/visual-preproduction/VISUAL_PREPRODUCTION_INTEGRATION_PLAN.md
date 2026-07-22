# Visual Preproduction V1 Integration Plan

## Integration with Asset Intelligence

Visual Preproduction emits typed asset requirements. Asset Intelligence retrieves and scores candidates.

```text
VisualSchema
↓
StoryboardIngredientSet
↓
AssetRequirement[]
↓
AssetIntelligenceService.retrieve_candidates(...)
↓
VisualReferenceBoard
↓
VisualPreproductionPacket references board/results
```

Visual Preproduction should not do unmanaged asset search.

## Integration with SuperVisual

```text
SuperVisualBuilderService
↓
VisualPreproductionService.compile_visual_schema(...)
↓
VisualPreproductionService.compile_storyboard_ingredients(...)
↓
AssetIntelligenceService.retrieve_candidates(...)
↓
SuperVisual reference board
↓
composition hypotheses
↓
composition lock
```

Use:

```text
lite = simple single visual
standard = premium/editorial SuperVisual
```

## Integration with Carousel

Carousel should use full-batch preproduction for sequence-level coherence:

```text
carousel sequence strategy
↓
batch VisualSchema
↓
slide-level VisualBeatPlan
↓
PRIMAL per slide
↓
VAE per slide
↓
Constraint Gate C across sequence
↓
Visual Analyst
↓
Storyboard Commander
```

## Integration with Video

Video is the heaviest consumer:

```text
Transcript Beat Map
↓
Viewer-State Sequence
↓
Visual Beat Plan
↓
Scene / B-roll / Insert Requirements
↓
PRIMAL per scene
↓
VAE per scene
↓
Constraint Gate C
↓
Visual Analyst
↓
Storyboard Commander
↓
Timeline composition
```

## Integration with Style Route Engine

Visual Preproduction produces:

```text
style_route_constraints
style_route_recommendations
forbidden_style_routes
source_reference_requirements
visual_schema_requirements
```

Style Route Engine chooses the actual route.
