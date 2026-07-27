---
title: JIT Skill and Execution Capsule Architecture Addendum
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# JIT Skill and Execution Capsule Architecture

## Historical intent

The original CCP JIT Skill concept solved a real problem: a large design brief contained many archetypes, modules, constraints, and runtime variables whose values depended on upstream decisions. The system therefore needed to compile the final active branch into an execution-ready prompt or skill at the moment of use.

The next Builder preserves that intent while separating durable and ephemeral layers.

## Four layers

### 1. Canonical Skill

A reusable, versioned, parameter-independent procedural capability with a typed design, completion criteria, failure modes, references, behavior tests, maturity, and a portable skill package.

### 2. Harness-local Skill Adaptation

A declared ecological mutation of a Canonical Skill for one atomic harness. It binds local ontology, legal variation, format grammar, failure modes, and evaluation without forking a new canonical identity unnecessarily.

### 3. Skill Composition Recipe

A parameterized plan identifying canonical skills, adaptations, reasoning modules, conditional references, runtime binding schema, output contract, evaluator hooks, and context policy for one phase or execution path.

### 4. JIT Execution Capsule

An ephemeral runtime artifact compiled after bindings and authority resolve. It contains only the active instructions, selected capability procedures, harness adaptations, direct evidence, conditional references, constraints, output contract, completion criteria, model policy, and compilation receipt for one phase.

## Original design-brief migration

A large archetype brief should be decomposed into:

```text
Archetype Constitution
+ Skill Composition Recipe
+ Runtime Binding Schema
+ Compilation and Degradation Gates
+ Examples and evaluation fixtures
```

The JIT compiler then selects only the current branch and produces a capsule. This prevents the original large brief from becoming a permanent monolithic prompt while retaining its invariants and runtime-dependent intelligence.

## Deterministic assembly

The compiler—not the model—owns:

- recipe and version selection;
- dependency and authority resolution;
- conflict and degradation policy;
- reference loading;
- context budgeting;
- output-contract binding;
- capsule hashing and receipts.

The model owns only the bounded semantic or creative transformation authorized by the phase.
