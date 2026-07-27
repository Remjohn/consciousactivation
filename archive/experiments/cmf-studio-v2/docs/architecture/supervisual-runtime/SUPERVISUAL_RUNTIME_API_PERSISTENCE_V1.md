# SuperVisual Runtime API + Persistence V1

## Definition

SuperVisual Runtime API + Persistence V1 makes SuperVisual production stateful, resumable, inspectable, versioned, and UI-ready.

It is not a single endpoint that returns an image.

Correct runtime shape:

```text
Project
→ Variant
→ Build Run
→ Step Runs
→ Receipts
→ Artifacts
→ Evaluation
→ Approval
→ Export
```

## Responsibilities

```text
create project
create variant
start build run
record step runs
persist lineage
persist snapshots
append events
execute typed commands
lock composition
record provider blueprints/receipts
record render/eval receipts
approve variant
export variant
```

## Non-responsibilities

```text
real provider execution
full creative reasoning
UI rendering
publishing scheduling
asset binary storage
```

This runtime stores references to those systems.
