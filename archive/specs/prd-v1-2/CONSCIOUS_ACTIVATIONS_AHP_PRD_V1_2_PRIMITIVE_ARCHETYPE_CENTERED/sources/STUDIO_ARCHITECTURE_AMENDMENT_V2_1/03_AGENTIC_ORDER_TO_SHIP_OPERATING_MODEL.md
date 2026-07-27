# Agentic Order-to-Ship Operating Model

## Product behavior

The Atomic Harness is the conductor.

The Studio is the supervisory and correction surface.

The operator is not expected to manually create the edit, composition, or asset plan.

## Main lifecycle

```text
ORDER
  workspace
  project
  objective
  sources
  target outputs
  initial content seeds
  taste direction
  budget and deadline

COMPILE
  select Harness
  bind capabilities, Skills, tools, runtimes, evaluators and workers
  compile Minimum Complete Context

EXECUTE
  launch Workflow Nodes
  generate meaningful candidates
  validate contracts
  evaluate results
  repair bounded failures
  continue downstream

SUPERVISE
  stream progress and artifacts to category Studio
  interrupt only at configured human gates, ambiguous taste boundaries,
  budget changes, or genuine execution exceptions

CORRECT
  operator supplies natural-language or direct-manipulation request
  Revision Compiler produces a typed ChangeRequestProgram
  validators check the program
  Pipeline reruns only affected nodes

SHIP
  final evaluation
  operator publication policy
  export or publish
  receipts and programming material
```

## Autonomy modes

```yaml
autonomy_modes:
  AUTOPILOT:
    behavior: execute to ship and interrupt only on genuine exception

  REVIEW_BEFORE_SHIP:
    behavior: execute completely, then request one final acceptance

  CHECKPOINTED:
    behavior: pause only at declared creative checkpoints

  SHADOW:
    behavior: execute and evaluate without publication authority
```

The default target for mature Harnesses is `AUTOPILOT` or `REVIEW_BEFORE_SHIP`.

## New required specs

- `TS-CAS-AUT-001` — Campaign Order, Seed, Taste, Budget, and Output Contract
- `TS-CAS-AUT-002` — Harness Autonomy Modes and Human-Gate Policy
- `TS-CAS-AUT-003` — Exception-Only Supervision and Selective Rerun
- `TS-CAS-AUT-004` — Ship, Export, Publication, and Post-Production Evidence
