# M08 — Archetype / Format Compatibility

**Status:** PROPOSED
**Depends on:** M03, M06, M07
**Primary requirement:** FR-IP-004

## Objective

Make downstream format/archetype intent an explicit constraint on question acquisition without allowing format to manufacture evidence.

## Core relation

`format/archetype intent + desired response shape + evidence requirement`
`→ question objective / coalition constraints`

## Required compatibility view

Expose, as derived data where possible:

- archetype references;
- format references;
- narrative roles;
- expected response structure;
- why the question is compatible;
- why it is incompatible when it is.

## Syntax principle

Recognizable syntax can reduce structural processing load. The implementation should preserve the distinction between familiar form and novel semantic collision. Do not encode “familiar format” as a reason to override poor evidence.

## Tests

- story-oriented hypothesis prefers episodic evidence;
- mechanism-oriented hypothesis prefers causal/mechanistic evidence;
- a question can be semantically strong but composition-incompatible and therefore rejected for the selected downstream intent;
- archetype labels cannot turn generic responses into story evidence.

## Stop conditions

Stop if the current repository has no authoritative format/archetype identifiers. Do not invent new IDs in the implementation.
