# Format Engine Draft Wiring V1.2

## Definition

Format Engine Draft Wiring V1.2 is the thin seam that turns authorized Format Intelligence adapter inputs into draft engine state.

It proves:

```text
source truth
→ extraction packet
→ format program
→ adapter input
→ engine draft state
```

without provider calls, render calls, UI, API, or publishing.

## SuperVisual

```text
SuperVisualBuilderFormatAdapterInput
→ SuperVisualDraftState
```

## Carousel

```text
CarouselEngineFormatAdapterInput
→ CarouselDraftVariantState
```

## Non-goals

```text
No image generation.
No provider execution.
No final render.
No approval.
No publishing.
No full engine rewrite.
```
