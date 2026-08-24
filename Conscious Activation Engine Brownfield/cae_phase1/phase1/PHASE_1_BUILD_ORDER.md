# Phase 1 Build Order

## Objective
Move from Phase 0 doctrine to a buildable canonical architecture without prematurely coding the entire ecosystem.

## Stage 1 — Canonical Register

Ratify the candidate object set and classify each object across:

- artifact class
- plane
- canonicality
- mutability
- epistemic status
- authority status
- lifecycle

## Stage 2 — Brownfield Audit

Inspect `consciousactivation-main` and map current implementations to the candidate objects. The result must distinguish what exists in code, what exists only as YAML/specification, what is duplicated, and what lacks relationships/state/runtime.

## Stage 3 — Relationship + State Matrix

Define high-value relations and state machines before physical database design.

## Stage 4 — Physical Data Design

Derive PostgreSQL tables, JSONB boundaries, vectors, events, views, and authorized functions from the canonical model.

## Stage 5 — Technical Specification Convergence

Select the highest-value FRs for technical specification. The first candidates should be:

- canonical registry
- object constitution validation
- relation/state model
- evidence/lineage
- brownfield reconciliation
- authorized semantic functions
- error taxonomy
- anti-centroid patrol

## Stage 6 — Phase Gate

Phase 1 is complete only when:

- the repository audit is complete enough to classify existing behavior;
- canonical objects have constitutional definitions or explicit pending status;
- core relations and states are specified;
- the physical data design is traceable to the conceptual model;
- technical specifications identify migration strategy and tests.
