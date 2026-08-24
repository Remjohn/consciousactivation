# Derived Artifact Definition Grammar Protocol

## Artifact class

`DERIVED_ARTIFACT`

## Purpose

Defines an object computed from upstream evidence, state, canonical definitions, relations, operators, or prior artifacts.

## Definition grammar

Use:

**Derivation Inputs + Computation/Inference + Result Purpose + Provenance + Confidence + Reproducibility + Non-Canonical Boundary**

## Examples

`EdgeProduct`, `ContentSpecies`, `SpeciesHypothesis`, `CompositionPlan`, `RenderBlueprint`, `SceneInstance`.

## Mandatory requirements

Every derived artifact MUST retain:

- upstream lineage
- derivation method/version
- confidence where relevant
- generated-at timestamp
- canonical dependencies
- reproducibility information where practical

## Constitutional law

Derived artifacts MUST NOT silently become canonical definitions because they were successful.

## Hard negatives

- derived artifact presented as ontology
- derived object missing lineage
- derived object treated as immutable truth
- derived object mutating source evidence
