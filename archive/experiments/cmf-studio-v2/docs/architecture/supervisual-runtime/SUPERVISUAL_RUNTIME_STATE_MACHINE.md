# SuperVisual Runtime State Machine

## Variant path

```text
draft
context_ready
preproduction_ready
reference_board_ready
composition_options_ready
composition_locked
materialization_planned
assets_materialized
render_ready
rendered
evaluated
approval_ready
approved
exported
```

Alternative states:

```text
revision_required
failed
archived
```

## Transition laws

```text
Cannot lock composition before composition options exist.
Cannot create provider blueprints before composition_locked.
Cannot materialize provider jobs before provider blueprints exist.
Cannot render before required materialized assets exist.
Cannot approve before evaluation passes.
Cannot export before approval.
Cannot mutate approved variant in place.
Cannot set 16:9 as delivery frame profile.
```
