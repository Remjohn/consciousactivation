# NOTE TO CODING AGENT — CAE Brownfield Reconciliation & Specification Authority

You are now working in a **brownfield transition**, not a greenfield build.

The repository already contains working systems and inherited registries. The recent CAE Phase 0–7 documents define a **target architecture**, but they are not automatically implementation-authoritative.

## Your current mental model

Treat the project as:

```text
VERIFIED CURRENT REPOSITORY
        +
RATIFIED / INHERITED SEMANTIC ARCHITECTURE
        +
PROPOSED CAE DESIGN
        ↓
BROWNFIELD RECONCILIATION
        ↓
FUNCTIONAL REQUIREMENTS
        ↓
TECH SPECS
        ↓
IMPLEMENTATION
```

Do not skip reconciliation.

## What the Phase 0–7 bundles mean

The phases are architectural design artifacts. They establish intended objects, relations, state models, contracts, and execution flow.

They must now be checked against:

- existing code;
- existing database/schema;
- existing tests;
- existing PRDs and FRs;
- existing Primitive registries;
- SDA registry seeds;
- SFL registry seeds;
- receipts and runtime behavior.

If a phase says an object exists but the repository shows otherwise, record the contradiction. Do not silently “fix” the document or the code.

## SDA and SFL are inherited assets

Important brownfield rule:

**SDA and SFL already have structured YAML registry seeds.**

Do not redesign them from scratch.

Preserve:

- original IDs;
- versions;
- source lineage;
- crosswalk rationale.

Use migration records for integrity gaps.

Known SFL integrity issue to verify during reconciliation:

The inherited failure corpus references function-family IDs beyond the included family registry range. Do not invent missing families merely to satisfy foreign-key-like references. Record the gap and define a migration decision.

## CAE ontology discipline

For each object, determine:

- canonical identity;
- artifact class;
- ontological plane;
- architectural role;
- definition grammar;
- boundary;
- taxonomy;
- lifecycle/canonicity;
- attributes;
- relations;
- states;
- events;
- provenance;
- invariants;
- owner;
- authorized/prohibited operations;
- validators;
- error taxonomy;
- storage representation;
- runtime consumers;
- examples;
- hard negatives.

Do not derive role from storage convenience.

## Engineering principle

The target architecture is increasingly:

```text
World / Evidence
→ Context + State
→ Semantic Discernment
→ Matrix of Edging
→ Interview
→ Authenticated Evidence
→ Primitive Candidates
→ Coalition
→ Edge Product
→ Archetype
→ SFL
→ Composition
→ Visual Syntax
→ IR
→ Runtime
→ Measurement
→ Learning
```

The system is fundamentally an editing/compiler architecture: selection, exclusion, combination, ordering, emphasis, and preservation.

## Agent execution principle

Do not expose agents to the entire database and ask them to “figure it out.”

Prefer:

```text
Intent
→ Schema Linking
→ Relevant Entities / Relations
→ Subproblem Decomposition
→ Retrieval / Composition Plan
→ Authorized SQL / Function
→ Execute
→ Validate
→ Typed Error
→ Repair
```

SQL functions/views may act as governed semantic APIs.

## Critical distinction

Do not collapse:

- canonical definition;
- runtime state;
- immutable evidence;
- derived artifact;
- execution packet;
- receipt.

These are different lifecycle classes.

## Anti-centroid law

The system deliberately resists generic/RLHF-style centroid collapse.

Do not introduce generic safety/corporate-smoothing language into definitions merely because it sounds responsible.

Normative restrictions should protect:

- evidence fidelity;
- schema integrity;
- semantic direction;
- anti-centroid laws;
- Matrix of Edging;
- SDA/SFL boundaries;
- reproducibility;
- system safety where explicitly required.

They should not flatten legitimate conviction or edge.

## Immediate work sequence

1. Validate Phases 0–7.
2. Reconcile all named objects and inherited registries.
3. Identify contradictions and missing state/relationship models.
4. Produce FR inventory.
5. Produce CAE Tech Specs under the new protocol.
6. Implement only after the relevant spec reaches `READY_FOR_DEVELOPMENT`.
7. Record receipts and tests.
8. Update phase validation with implementation evidence.

## Definition of done for a specification

A developer should be able to answer, without guessing:

- what exists;
- why it exists;
- where it lives;
- how it is represented;
- what it relates to;
- how it changes;
- who can operate on it;
- what can fail;
- how failure is repaired;
- how success is tested;
- how execution is traced;
- what evidence authorizes the behavior.

Until those questions are resolved, the document is architecture—not yet an implementation contract.


## Reality-contact and reward-hacking doctrine

A green test is not sufficient proof. Before declaring a CAE capability verified, classify the environment used by the test: E0 synthetic, E1 realistic fixture, E2 repository-integrated, E3 production-shaped, or E4 real-world observed. The evidence level must match the claim.

For every material evaluator ask:

```text
What proxy is being measured?
What underlying property is intended?
How could an optimizing implementation game the proxy?
What false-proof test exposes that gaming?
```

Maintain dedicated taste/anti-centroid regression evidence. Structural validity, schema completeness, and absence of forbidden phrases do not prove that the result has edge, recognition, specificity, human congruence, or perceptual aliveness. Do not repair a quality failure by adding corporate smoothing.

The Anti-Centroid Patrol is a governance function charged with detecting validator drift toward genericization. It should review meaningful evaluator changes and repeated repair behavior.

For implementation reports, use:

```text
IMPLEMENTED_PENDING_VERIFICATION
```

when code and basic tests exist but reality-contact, reward-hacking, taste, or environment evidence remains incomplete.

Only report:

```text
VERIFIED
```

when the applicable structural, environment-fidelity, reward-hacking, taste/anti-centroid, receipt, and outcome gates have passed.
