# Lane A — Atomic Harness Pipeline Bridge and Execution Kernel

## Exclusive target paths

```text
04_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/**
04_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application/**
04_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/workflow/**
04_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/cmf_studio/**
04_ATOMIC_HARNESS_PIPELINE/tests/pipeline/**
```

Shared exports and status files require integrator requests.

## Predecessor source

```text
THE_CMF_STUDIO(2).zip/
  src/ccp_studio/contracts/studio_pipeline_recipe_harness.py
  src/ccp_studio/services/pipeline_recipe_service.py
  src/ccp_studio/services/pipeline_run_service.py
  src/ccp_studio/services/pipeline_step_run_service.py
  src/ccp_studio/contracts/composition_runtime.py
  src/ccp_studio/services/composition_runtime_service.py
```

## Deliver

- Installable Pipeline package.
- `AtomicHarnessDefinition` loader.
- `HarnessExecutionBindingManifest`.
- Harness-to-CMF compatibility compiler.
- Workflow Node scheduler.
- Actor/ownership/role/product-boundary classification.
- JIT Capsule intake port.
- Durable run/step/checkpoint/receipt state.
- Replay, resume, cancellation, invalidation.
- Typed runtime and external-product ports.
- CLI: `ingest`, `bind`, `run`, `inspect`, `resume`, `cancel`, `export`.

## Critical rule

Compile current Harness sections into the existing CMF execution objects. Do not define a
second semantic Harness.

## Tests

- current synthetic definition;
- one Activative static definition;
- one edited-video definition;
- tamper/stale/invalidation;
- restart and idempotency;
- cross-product boundary;
- fake-result rejection.
