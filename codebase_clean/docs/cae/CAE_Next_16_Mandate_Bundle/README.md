# CAE Next 16 Mandate Bundle — M49–M64

This is the controlled follow-on wave after CAE M01–M48.

## What this bundle changes

The next wave is organized around two problems exposed by the brownfield/runtime audit:

1. **Agent execution convergence:** Agent identity, packages, local CAE.md context, actual invocation, Program binding, typed outputs, gates, repair and standalone sessions.
2. **Workflow engineering:** executable primitives, Workflow IR, deterministic control flow, Step Contracts, the CAE Software Development Life Cycle factory, isolation, operator commands, visual trace and final certification.

## Reference doctrine

The bundle uses the existing CAE Mandate Authoring Protocol and 48-mandate package grammar, including mandatory reading, prohibitions, evidence, false-proof testing, rollback, operator decisions and phase-close synchronization. The same prior bundle explicitly requires `CURRENT.md` synchronization at phase close and distinguishes documented/code-existing/test/runtime/operator-accepted claims.

SSSF is used as a reference implementation of the agents-plus-code factory pattern: deterministic Python owns the workflow, Agents perform bounded phases, typed handoffs cross seams, gates determine acceptance, repairs can preserve a live session, and a SQLite trace powers operator observation. CAE adopts those execution patterns while preserving CAE authority, state, receipts, canonical knowledge and Program/Harness boundaries.

## Execution rule

Hand M49, M50, ... to the coding agent one at a time. Do not blanket-authorize the entire phase. Each mandate ends at an operator gate.

Run:

```bash
python 07_VALIDATION/validate_bundle.py
```

before handing the bundle to the execution environment.


## v1.1.0 reliability amendment — StateM alignment

This bundle is amended to make the StateM reliability principles explicit without introducing a second workflow/state engine. The authoritative cross-mandate contract is `00_CONTROL/11_STATEM_ALIGNMENT_CONTRACT.md`. The amendment requires state-boundary context refresh, ordered checked transitions, source-state retention on failed blocking checks, durable per-run recovery evidence, one shared Agent/Operator control projection, and versioned/validated procedural practice.
