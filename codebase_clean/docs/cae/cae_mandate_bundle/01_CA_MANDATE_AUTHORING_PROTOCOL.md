# CAE Mandate Authoring Protocol

**Status:** Proposed governed authoring standard, derived from the existing CAE Gemini execution program and mandate exemplars.

## Purpose

This protocol defines how a CAE execution mandate is written so that Gemini can execute one bounded phase without interpreting the mandate as permission to redesign the architecture.

## Required mandate grammar

Every mandate SHALL contain these sections in this order:

1. Identity and status
2. Decision / objective being authorized
3. Governing doctrine and authority sources
4. Mandatory reading before action
5. Exact scope
6. Allowed artifacts and file boundary
7. Prohibitions and collision procedure
8. Required work / implementation behavior
9. Verification and evidence standard
10. Completion and stop condition
11. Rollback / recovery
12. Operator decision
13. 200–300 word activation prompt

## Semantic rule

A mandate is an execution contract, not a descriptive essay. Each paragraph must answer at least one of:

- what is being changed;
- what is explicitly not being changed;
- which source of truth controls the decision;
- what evidence must exist;
- how failure is handled;
- when the agent must stop.

## Authority grammar

Every mandate must distinguish:

- source of meaning;
- runtime authority;
- change/promotion authority.

A repository source, YAML registry, PostgreSQL projection, runtime state, or receipt may not inherit authority merely because it exists.

## Scope grammar

Each mandate must name:

- objective;
- dependencies;
- allowed files or logical artifacts;
- prohibited surfaces;
- inputs;
- outputs;
- operators allowed;
- validators required;
- stop condition.

“Improve” or “finish” without an explicit boundary is prohibited.

## Evidence grammar

Every substantive claim must declare evidence class. Recommended classes:

`EXECUTABLE`, `SCHEMA`, `MIGRATION`, `REGISTRY_SOURCE`, `DOCUMENT`, `TEST`, `HYPOTHESIS`, `OPERATOR_DECISION_REQUIRED`.

A semantic judgment is not deterministic evidence unless independently verified.

## State grammar

If the mandate changes state, define:

```text
source state
→ operation
→ target state
```

and specify:

- actor;
- preconditions;
- validators;
- postconditions;
- receipt;
- error route;
- recovery path.

## Anti-centroid grammar

Every mandate that creates content, reasoning, or evaluative output must include at least one contrastive failure. The failure must describe a plausible “good-looking but wrong” result and why it violates project-specific invariants.

## Taste / reward-hacking grammar

A test is insufficient if it can pass without establishing the intended property. Every material verifier should state:

- what it actually measures;
- what it does not measure;
- one false-proof countercase;
- one environment-fidelity requirement;
- whether human/operator validation is required.

## Activation prompt grammar

The activation prompt is a compact execution key. It must include:

- mandate ID;
- authority references;
- exact scope;
- prohibitions;
- required evidence;
- stop condition;
- operator decision requested.

It does not replace the mandate and must never authorize adjacent work.

## Parallelism rule

Parallel execution is permitted only when outputs are independently mergeable and cannot establish conflicting authority. Shared registries, shared state, migrations, and operator decisions have one integration owner.

## Final rule

A mandate is complete only when the requested artifact exists, the declared proof standard is met, limitations are recorded, the control-state record is updated, the exact commit is captured, and the operator decision is explicitly requested.
