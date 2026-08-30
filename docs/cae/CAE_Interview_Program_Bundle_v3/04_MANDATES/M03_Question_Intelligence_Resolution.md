# M03 — Question Intelligence Resolution

**Status:** PROPOSED
**Depends on:** M01, M02, approved Question Intelligence synthesis
**Primary requirements:** FR-IP-003, FR-IP-004

## Objective

Implement the question-resolution layer that turns a selected hypothesis into a question objective, evidence requirement, candidate mechanism coalition, response shape, and derived Question IR—without canonizing unaudited primitives.

## Required upstream chain

`selected hypothesis → question objective → evidence requirement → candidate mechanism coalition → derived Question IR → natural-language candidates`

## Mechanism policy

Use only mechanisms admitted by the approved synthesis. A mechanism remains `PROMOTION_CANDIDATE`, `MERGE_CANDIDATE`, or `RESEARCH_MORE` until a separate promotion authority says otherwise.

## Required dimensions

The resolver must be able to represent, at least as derived fields:

- psychological/semantic target resolution;
- answer resolution;
- information completeness target;
- evidence mode;
- temporal orientation;
- social reference frame;
- interactional fit;
- epistemic posture;
- downstream archetype/format compatibility.

## Required tests

- same hypothesis can produce distinct syntactic realizations without changing its semantic target;
- a regeneration request cannot silently change locked hypothesis/evidence dimensions;
- unaudited mechanism cannot be treated as canonical;
- question candidate retains audit and upstream provenance;
- question candidate can be rejected for poor downstream compatibility even when structurally valid.

## Stop conditions

Stop if implementation requires a new canonical Question Primitive registry or object without a separate promotion decision.
