# Execution Packet Definition Grammar Protocol

## Artifact class

`EXECUTION_PACKET`

## Purpose

Defines a typed, runtime-safe payload that moves between programs, agents, tools, validators, or services.

## Definition grammar

Use:

**Runtime Purpose + Required Inputs + Typed Payload + Validity Conditions + Consumer Contract + Lineage + Expiration / Scope + Error Semantics**

## Required design principles

An execution packet should be:

- typed
- bounded
- serializable
- lineage-preserving
- versioned
- consumer-specific
- validation-ready

## Examples

`InvariantFieldPacket`, `RepresentationGeometryPacket`, `ArchetypalGeometryPacket`, `SubliminalFunctionStackPacket`, `SpeciesHypothesisPacket`, `DirectionalIntegrityReport`.

## Hard negatives

- packet containing arbitrary prose with no schema
- packet accepted without version compatibility
- packet whose fields have ambiguous ownership
- packet used as permanent database truth

## Runtime rule

Packets transport state and decisions. They do not redefine canonical ontology.
