# SuperVisual + Carousel Format Program Adapters V1.1

These adapters let SuperVisual and Carousel consume `FormatIntelligenceProgram` outputs without rewriting the engines.

## SuperVisual

```text
SuperVisualFormatProgram
→ SuperVisualBuilderFormatAdapterInput
```

## Carousel

```text
CarouselFormatProgram
→ CarouselEngineFormatAdapterInput
```

The adapters preserve:

```text
brand_context_version_id
source_span_refs
composition grammar
layer stack
style route policy
eval gates
render requirements
engine target
```
