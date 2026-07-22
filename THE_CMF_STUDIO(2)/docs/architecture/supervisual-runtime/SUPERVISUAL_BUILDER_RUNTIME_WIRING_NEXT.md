# SuperVisual Builder Runtime Wiring Next Steps

This branch adds the SuperVisual runtime shell: persistent projects, variants, build runs, step runs, events, commands, snapshots, and API access. The next phase should wire this runtime to the SuperVisual builder layer without hiding production state inside one opaque `build()` call.

## Runtime Ownership

`SuperVisualRuntimeService` should remain the owner of state transitions, commands, idempotency, append-only events, snapshots, approval gates, export gates, and persistence.

Builder services should own production intelligence and return typed receipts or DTOs. They should not directly approve, export, mutate approved variants, or write runtime state without going through the runtime service.

If `SuperVisualBuilderService` is introduced or consolidated later, it should adapt the current still-visual, asset program, provider-request, Asset Intelligence, Visual Preproduction, Style Route, and provider materialization services behind explicit step methods.

## Recommended Builder Step Surface

The runtime should call builder-equivalent methods in this order:

```text
compile_context(...)
compile_reference_board(...)
generate_composition_hypotheses(...)
lock_composition(...)
compile_layer_plan(...)
compile_provider_blueprints(...)
materialize_assets(...)
compile_render_contract(...)
render_variant(...)
evaluate_variant(...)
```

Each method should return a typed output that the runtime can persist into the variant lineage, step run, snapshot, and event log.

## Step Output Mapping

`compile_context(...)` should produce context lineage, brand context refs, interview brief refs, transcript refs, primitive coalition refs, and missing-context blockers.

`compile_reference_board(...)` should call Asset Intelligence when available and return candidates, rights/use-mode decisions, missing ingredient gaps, and usage obligations.

`generate_composition_hypotheses(...)` should call Visual Preproduction and Style Route services when available and return composition options, frame profile, style route, visual schema, storyboard ingredients, and primitive compliance notes.

`lock_composition(...)` should freeze one composition option and record why it satisfies the requested frame, format, primitive coalition, and style route.

`compile_layer_plan(...)` should convert the locked composition into UI-ready and render-ready layers, including copy blocks, generated asset slots, source references, masks, annotations, and export-safe bounds.

`compile_provider_blueprints(...)` should prepare provider job blueprints only after composition lock and source/reference checks. It should not call paid providers directly.

`materialize_assets(...)` should call provider materialization through the provider orchestration wrapper, record provider receipts, and store generated outputs as assets or ingredient variants. Provider outputs are ingredients, not final SuperVisual renders.

`compile_render_contract(...)` should produce the deterministic render plan, frame profile, canvas size, layer ordering, typography constraints, asset refs, and reproducibility metadata.

`render_variant(...)` should produce preview and export artifact references without mutating approved/exported variants in place.

`evaluate_variant(...)` should produce eval receipts, primitive compliance status, blockers, and approval readiness.

## Runtime Guardrails

The runtime must continue to enforce:

```text
composition options required before composition lock
composition lock required before provider blueprints
provider blueprints required before materialization
composition lock required before render
passing eval required before approval
approval required before export
approved/exported variants cannot mutate in place
16:9 cannot be used as a delivery frame profile
commands are idempotent
events are append-only
```

## API And UI Handoff

Phase 2 should connect SuperVisual Studio UI to the runtime API and render the cockpit from project detail responses, variant snapshots, events, step runs, provider receipts, eval receipts, and available actions.

The UI should trigger typed commands and step endpoints. It should not modify project or variant JSON directly, and it should not bypass approval, eval, or export gates.

## Non-Goals For This Branch

This branch does not wire the SuperVisual Studio frontend, live paid providers, Carousel, Video, or a full renderer. It prepares the backend runtime and persistence layer those systems should use.
