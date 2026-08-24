# Coding Agent Note — CAE State Control & StateM Reference

## Current instruction

The CAE architecture is adopting a PostgreSQL/Supabase-authoritative state model with StateM-inspired procedural control semantics.

Do not interpret this as a request to install StateM as CAE's database or workflow source of truth.

## Required architecture

```text
PostgreSQL/Supabase
    authoritative state + history + events + receipts

Typed CAE semantic operations
    authorized read/write interface

Skills.md / runbooks / reasoning programs
    procedural doctrine + state-local instructions + transition contracts

Agent
    broad reasoning autonomy inside authorized state boundaries

Validators
    independent transition evidence

Events + receipts
    immutable execution trace
```

## StateM reference

Read and cite before making any actual code-reuse decision:

- https://github.com/henryqin1997/statem
- https://arxiv.org/abs/2608.15089

StateM is a design/implementation reference for:

- state boundaries;
- checked transitions;
- state-local context;
- run-local dynamic checks;
- recovery routing;
- durable procedural history;
- stop/handoff control.

Do not copy benchmark-specific runbook rules into CAE.

## Before coding

Inspect the current repository for:

- existing Supabase/PostgreSQL tables;
- receipt chain;
- state-like models;
- events;
- pipelines;
- agents;
- services;
- circuit breakers;
- memory tiers;
- existing Skills.md / harness execution infrastructure.

Produce a mapping:

```text
CAE State Object
→ existing table/model/service
→ existing event/receipt infrastructure
→ required migration
→ required semantic operation
→ required transition contract
→ tests
```

## Required implementation behavior

Do not implement normal agent state changes through raw ad-hoc SQL writes.

Prefer typed semantic operations such as:

```text
get_current_run_state()
get_legal_transitions()
evaluate_transition()
request_transition()
record_transition_receipt()
```

Use database transactions for state + event + receipt where feasible.

Preserve history.

Do not treat agent self-attestation as independent proof.

Do not allow a green proxy metric to promote a state when the underlying semantic, evidence, environment, taste, or anti-centroid requirement is still unverified.

## State boundary rule

A state gives the agent a current context and contract. It does not dictate the model's internal reasoning inside that state.

Keep the primary agent's reasoning loop coherent. Add state boundaries where they preserve durable context or enforce consequential handoffs.

## Required deliverables for state-control implementation

1. brownfield state inventory;
2. canonical state/transition model;
3. semantic operation registry;
4. database migration plan;
5. transition service;
6. event/receipt integration;
7. harness/runbook integration;
8. state-transition tests;
9. reward-hacking countertests;
10. environment-fidelity proof packet.
