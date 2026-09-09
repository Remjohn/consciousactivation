# FR-CA-01-014 — Director Note / Prose-to-Directive Translation

## Requirement
Human Director Notes SHALL be preserved as immutable human intent and MAY be translated into typed directives for runtime use.

## Pattern
`Human prose → semantic interpretation → candidate directive → canonical typed directive → validation → program/runtime effect`

## Example
Human note:
“Do not make this motivational. Make it feel like recognition.”

Structured directive:
```yaml
intent_type: perceptual_directive
target: archetype
desired_effect: recognition
forbidden_effect: generic_motivation
evidence: director_note#...
```

The typed directive does not replace the original note. It is a derived operational representation.
