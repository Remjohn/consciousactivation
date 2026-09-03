# Mandatory File Policy

## Definition

"Equivalent" does not mean "a shorter file with the same title."

A CAE equivalent must preserve or exceed the substantive behavior of the capability it replaces.

Therefore:

- a CAE Product Brief skill must contain actual facilitation/validation/production instructions;
- a CAE PRD skill must contain actual PRD workflow mechanics;
- a CAE Architecture skill must contain actual architecture workflow mechanics;
- a CAE Epics/Stories skill must contain actual decomposition/readiness mechanics;
- a CAE UX skill must contain actual interaction/design mechanics;
- a CAE Review skill must contain actual adversarial review mechanics.

## Word-count policy

The validator can enforce minimum word counts.

For CAE-created equivalent files, minimums are intentionally conservative and should not fall below
the corresponding upstream scope.

Where an upstream version is substantially expanded, update the CAE minimum accordingly.

The goal is not a vanity word count. The goal is to prevent the prior failure mode where a serious workflow
was reduced to a short routing paragraph.

## Structural parity

Major equivalents should contain:

- SKILL.md
- customize.toml
- step files
- assets/templates where relevant
- references where relevant
- explicit activation/read/execute/finalize rules
- completion semantics
- failure semantics
- routing/handoff semantics

The CAE bundle must not call a two-paragraph file a replacement for a multi-step workflow.
