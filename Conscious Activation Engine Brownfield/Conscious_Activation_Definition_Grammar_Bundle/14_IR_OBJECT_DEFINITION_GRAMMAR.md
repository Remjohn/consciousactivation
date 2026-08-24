# Intermediate Representation Object Definition Grammar Protocol

## Artifact class

`IR`

## Purpose

Defines an executable intermediate representation that preserves validated semantic intent while remaining independent of a specific final rendering or runtime target where possible.

## Definition grammar

Use:

**Source Semantics + Normalized Structure + Execution Intent + Constraints + Dependencies + Lowering Rules + Validation Requirements + Target Independence**

## Examples

`SemanticProgram`, `CompositionIR`, `VideoEditProgram`, executable content manifests.

## Definition must establish

- what source objects are being compiled
- what has been normalized
- what must remain invariant
- what target-specific details are deferred
- how the IR is validated
- what lowering passes produce executable output

## Constitutional law

An IR MUST NOT re-infer upstream semantic truth if the relevant meaning has already been validated. It should carry authorized decisions forward.

## Hard negatives

- IR that contains uncontrolled natural-language instructions only
- IR that silently changes semantic meaning
- IR coupled unnecessarily to one renderer
- IR without versioning or validation
