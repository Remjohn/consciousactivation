# Phase Readiness Matrix

| Phase | Minimum proof | Failure if absent |
|---|---|---|
| 5 | actual AgentInvocation reaches runtime boundary | agentic runtime remains unproven |
| 6 | Program-owned and standalone Agent executions share typed contract/gates | Agents remain isolated building blocks |
| 7 | executable workflow IR + deterministic control-flow behavior | workflow remains descriptive |
| 8 | real CAE SDLC run + visible trace + repeated certification | no production confidence |

## Non-negotiable

A phase-close gate cannot be satisfied by document presence alone.


## StateM-aligned cross-phase non-negotiables

- State entry refreshes applicable context and records a hash-linked inclusion/exclusion trace.
- Blocking transfer checks execute before target-state commit; failure retains the source state and its evidence.
- Repair is state-preserving until the same transition obligations pass or a terminal failure is recorded.
- Static control definition is distinct from mutable per-run state/history.
- Agent and Operator projections read the same canonical run/control truth.
- Procedural lessons are versioned and validated through existing authority; hidden Agent memory is not a control source.


