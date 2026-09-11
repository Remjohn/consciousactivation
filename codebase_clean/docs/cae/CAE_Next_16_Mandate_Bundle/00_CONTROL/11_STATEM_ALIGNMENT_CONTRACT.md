# StateM Alignment Contract — M49–M64

**Status:** Bundle control amendment v1.1.0  
**Purpose:** make the StateM reliability principles explicit, testable, and subordinate to CAE authority without creating a second workflow/state engine.

## Source and boundary

Primary research reference: **StateM: Stateful Execution for Long-Horizon Agents**, https://arxiv.org/pdf/2608.15089  
Research is a design reference only. It does not override CAE constitutions, Programs, Harnesses, State, Hooks, Operations, Receipts, or Operator authority.

## Principles adopted into this bundle

1. **State is a context-and-contract boundary.** A state transition is not merely a label change; entering a state establishes the phase-local instructions, durable progress, valid outgoing transitions, and evidence obligations relevant to that state.
2. **Refresh control context at state entry.** Long-horizon execution must not depend on an ever-growing mutable prompt. State entry loads/recompiles the minimum durable context relevant to the new state and records what was included and excluded.
3. **Keep control outside the model.** Executable transition conditions, timeouts, retry counts, hooks, and persistence are host/runtime concerns. The Agent may reason within the state but cannot redefine the state's control law.
4. **Use checked transfer semantics.** A transition follows the ordered protocol: validate edge exists → run blocking pre-transfer checks → persist/out-hook obligations → evaluate edge guards/transition hooks → commit target state and history → run target entry/in-hook refresh. Failure keeps execution in the source state and records the failed obligation.
5. **Preserve recoverable state.** Repair is state-preserving by default. A failed check does not silently advance the run, reset the session, or erase evidence. Repair re-enters the same state's obligations before another transition attempt.
6. **Separate static control profile from mutable run state.** The reusable state/workflow definition is immutable/versioned for the run; current state, history, hook/check outcomes, evidence, and recovery anchors belong to the per-run record.
7. **Expose one shared control surface.** The Agent runtime and Operator must inspect the same canonical state/runbook projection. UI/CLI projections are readers/adapters, not competing authorities.
8. **Treat procedural learning as versioned practice, not hidden memory.** Repeated failure can yield a proposed state-local practice/check/constraint/verification action, but promotion requires explicit validation, versioning, provenance, and operator/authority acceptance. No self-authored rule becomes binding merely because an Agent generated it.
9. **Do not over-decompose the executive Agent.** State boundaries should be used for durable control/context refresh; they do not require splitting one coherent Agent task into many node-local model calls.
10. **Independent evidence remains stronger than self-attestation.** StateM-style orchestration is not itself a correctness oracle. Certification must distinguish host checks, external predicates, manual/operator attestations, and Agent self-review.

## CAE mapping / non-duplication rules

| StateM idea | Existing CAE authority to reuse | Bundle obligation |
|---|---|---|
| Runbook | Program/Harness/Workflow definition + existing State model | M57–M59 formalize deterministic semantics without inventing a parallel state ontology |
| Per-run state | Existing Run/State/Event/Checkpoint persistence | M55/M59/M64 prove state/history are durable and replayable |
| State-local context | `JITContextCapsule`, retrieval/Skill/package projections | M51/M52/M53 require refresh at state/phase boundary |
| Entry/exit hooks | Existing Hook authority | M57/M59 require ordered hook semantics and receipts |
| Transfer checks/guards | Existing gate/validator/transition mechanisms | M54/M59/M60 make failed checks blocking and source-state preserving |
| Operator shared control | Program operator runtime + Studio trace/projections | M63 uses canonical execution truth for Agent and human views |
| Versioned practice | Existing Skill/evaluation/governance lifecycle | M64 validates and versions reusable lessons; no hidden memory authority |

## Mandatory invariants for this wave

- No state transition without a canonical state identifier and a valid edge.
- No target-state execution begins until required pre-transfer checks and persistence complete.
- Failed blocking checks leave the run in the source state and expose the failure reason/evidence.
- State entry recomputes or selects phase-local context using the current authoritative state/run record; stale prior-state context may not silently persist when it is no longer applicable.
- A retry/repair may reuse the same Agent Session, but it must retain the current state, failed obligations, prior receipts, and bounded retry budget.
- Operator and Agent views read the same run/control projection; neither view invents authoritative state.
- Procedural lessons are advisory until validated and versioned through the existing governance/Skill authority.
- A passing Agent self-report is never sufficient by itself for a blocking transition.

## Required evidence shape

For a representative run, retain a machine-readable chain containing at minimum:

`run_id → static control profile/version → source_state → entry_context_hash → state-local evidence → attempted edge → pre-transfer checks → hook outcomes → target_state (or source-state retention) → transition receipt`.

For a repair:

`failed obligation → source state retained → repair action → bounded retry count → refreshed state-local context → re-check → transition or terminal failure`.

For a procedural lesson:

`failure → observed cause → proposed practice → provenance → validation evidence → version/lifecycle state → promotion/rejection decision`.

## Explicit non-goals

This amendment does **not** authorize importing StateM's runbook format, replacing CAE State with a new state machine, replacing the existing workflow compiler, allowing arbitrary Agent-created transitions, or treating Agent memory as canonical procedural state.
