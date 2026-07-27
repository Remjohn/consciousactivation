# SuperVisual Runtime Object Model

## Main objects

```text
SuperVisualProject
SuperVisualVariant
SuperVisualLineage
SuperVisualSnapshot
SuperVisualBuildRun
SuperVisualStepRun
SuperVisualEvent
SuperVisualCommand
```

## Project

Top-level production container. It owns the immutable `brand_context_version_id`.

## Variant

A versioned output candidate. Variants are mutable until approved. Approved variants cannot be mutated in place.

## Lineage

References upstream and downstream artifacts:

```text
primitive coalition
visual preproduction packet
asset reference board
style route decision
route production specs
provider blueprints/receipts
composition decision
layer plan
render contract/receipt
evaluation receipt
approval receipt
export pack
```

## Snapshot

A UI-ready state snapshot so the frontend can render without reconstructing state from every table.

## Event

Append-only audit trail.

## Command

Typed UI/agent action with idempotency.
