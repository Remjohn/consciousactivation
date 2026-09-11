---
spec_id: TS-APP-INTERVIEW-OPERATOR-STUDIO-001
title: Operator Hypothesis and Question Studio

document_class: TECH_SPEC
product: Conscious Activations
module: interview-program-operator-studio
quality_state: WRITTEN_PENDING_AUDIT
authority_state: PROPOSED
build_authority: false
prepared: 2026-08-30
---

# TS-APP-INTERVIEW-OPERATOR-STUDIO-001

## 0. Purpose

Provide the human control surface between upstream candidate generation and authorized Interview Brief launch.

This is an extension of the current Composer user experience, not a second interview product.

## 1. User outcome

An Operator can inspect why a candidate exists, understand its intended evidence and downstream use, decide whether it is worth pursuing, provide structured feedback, request constrained alternatives, lock meaningful dimensions, assemble a portfolio, compile the existing Brief, and explicitly authorize launch.

## 2. Candidate card minimum information

Each candidate view should expose, where available:

- candidate/provenance identifier;
- upstream activation/hypothesis reference;
- Audience cognitive-island/current-state alignment;
- Guest semantic territory;
- world/research signals;
- collision statement;
- target tension/edge;
- expected contradiction or discrepancy;
- question objective;
- mechanism coalition or candidate mechanism references;
- expected evidence;
- answer/response shape;
- archetype/format/narrative-role compatibility;
- selection diagnostics;
- source/audit provenance;
- status/version.

## 3. Operator actions

`KEEP | REJECT | EDIT | REGENERATE | DEFER | LOCK`

The UI may also support an explicit final `APPROVE_FOR_LAUNCH` action that is not equivalent to KEEP.

## 4. Regeneration semantics

Regeneration is constrained editing, not free rewriting.

When the Operator locks a dimension, that dimension becomes immutable for the regeneration request. Examples:

- hypothesis locked → do not change collision claim;
- evidence requirement locked → do not weaken/replace required evidence;
- archetype locked → do not change downstream structure;
- Guest territory locked → do not substitute a different life domain;
- only syntax/posture unlocked → regenerate question wording/mechanism realization within those boundaries.

Every regeneration result retains parent candidate lineage and records the Operator feedback that caused it.

## 5. Concurrency

Use the repository's current persistence/versioning conventions. The Studio must not allow a stale client to silently overwrite a newer Operator decision.

Minimum required behavior:

- stale version rejection or explicit merge/review;
- idempotent duplicate submission;
- authoritative server-side lock enforcement;
- server-side approval enforcement.

## 6. Launch rules

A candidate may not be launchable merely because:

- the UI renders it;
- it has a high score;
- it passed schema validation;
- a model returned `PASS`;
- a client supplied `operator_approved=true`.

Launch requires a persisted, authoritative Operator approval state associated with the current selected portfolio/Brief version.

## 7. Reality-contact acceptance

The final Studio proof must demonstrate:

`real candidate source`
`→ real retrieval`
`→ real Operator action`
`→ real persistence`
`→ real Brief compilation`
`→ fresh readback
`→ authorized launch decision`.

## 8. Brownfield constraints

The implementation must reuse existing application shell, route, auth, API, repository, and UI component conventions after inspection. If a required surface does not exist, document the exact gap and owner before adding it.
