# Protocol Authoring Guide

## The purpose of Definition Grammar Protocols

These protocols are not ordinary documentation templates. They are **meta-skills for creating canonical object definitions**.

The eventual `Skills.md` implementation for each object class should compile this protocol into:

- task definition
- admissible inputs
- required sections
- forbidden ambiguity
- legal vocabulary
- examples
- hard negatives
- validators
- escalation rules
- output schema

## The prose-to-structure pipeline

```text
Human prose / research / observation
        ↓
Semantic interpretation
        ↓
Artifact classification
        ↓
Definition grammar
        ↓
Object constitution
        ↓
Canonical schema
        ↓
Validation
        ↓
Storage / runtime representation
```

## Multi-language principle

Different stages may use different representational languages:

- **Poetic prose** — exploration, atmosphere, creative discovery
- **Counsel / analytical prose** — interpretation and reasoning
- **Legal prose** — obligations, permissions, prohibitions, boundaries
- **Typed schema** — canonical data representation
- **SQL / function language** — controlled retrieval and execution
- **IR** — executable program representation

The language may change, but semantic identity and lineage must survive the translation.

## Role-before-schema law

The author MUST classify an object before designing fields.

## Definition-length law

No fixed word count is mandatory. The definition must be long enough to establish the distinctions required by its role.

## Example law

No high-leverage object should be canonicalized from definition alone. Examples, counterexamples, and hard negatives should accompany important definitions.

## Final authoring test

Ask:

> Could a competent engineer who has never seen the original discussion implement this object without silently inventing missing semantics?

If not, the definition is not ready.
