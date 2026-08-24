# Object Definition Quality Gate

Before an object definition becomes canonical, the authoring agent MUST answer every applicable question below.

## Identity

- Is the canonical name unambiguous?
- Are aliases controlled?
- Are nearest neighbors named?

## Role

- Is the architectural role explicit?
- Is the artifact class correct?
- Is the primary ontological plane explicit?

## Definition

- Does the definition contain the class-specific grammar?
- Does it establish identity/function/boundary where applicable?
- Does it avoid merely restating the name?

## Boundaries

- Is the object distinct from its nearest neighbors?
- Are likely confusions explicitly prohibited?

## Lifecycle

- Is it canonical, dynamic, immutable evidence, or derived?
- What changes?
- What must never mutate?

## Relationships

- Are source/target directions explicit?
- Are cardinality and temporal semantics defined where applicable?

## Provenance

- Can the object be traced to supporting evidence?
- Is evidence status explicit where research claims are involved?

## Execution

- What operations are authorized?
- What operations are prohibited?
- Which validators guard it?
- Which errors can occur?

## Storage

- Which fields belong in strict columns?
- Which belong in relations?
- Which are evolving JSONB attributes?
- Does fuzzy retrieval require embeddings?
- Does temporal history require events?

## Examples

- Is there at least one valid positive example?
- Is there at least one realistic hard negative or nearest-neighbor contrast?

## Canonicalization gate

An object MUST NOT be promoted to canonical status unless the definition, taxonomy, schema, provenance, and nearest-neighbor boundaries are sufficiently mature to support deterministic agent use.
