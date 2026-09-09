# State Definition Grammar Protocol

## Artifact class

`STATE`

## Purpose

Defines a time-bounded condition or configuration of an underlying entity, relationship, semantic field, or process.

## Definition grammar

Use:

**Subject + Condition + Configuration + Temporal Scope + Transition Semantics + History Rule + Boundary**

## Constitutional law

**A state describes a condition of something; it does not replace the thing itself.**

## Definition must establish

- what underlying object is being conditioned
- which dimensions constitute the state
- observation and validity intervals
- state transitions
- entry and exit conditions
- decay / saturation / resolution behavior
- whether the state can coexist with other states
- preservation of historical states

## Example

`ContextualState` is a temporally bounded representation of the condition in which an entity, relationship, or semantic field exists during a specified observation interval. It records the current configuration without redefining the underlying object and may intensify, decay, resolve, saturate, or be superseded. It MUST retain temporal provenance and MUST NOT overwrite historical observations.

## Required constitution sections

- state variables
- initial conditions
- transition map
- terminal states
- temporal validity
- confidence
- evidence
- persistence rules
- validators
- error taxonomy

## Hard negatives

- state stored as a permanent attribute
- current state overwriting history
- state without timestamp/provenance
- state treated as an entity
