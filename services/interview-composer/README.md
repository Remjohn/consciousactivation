# Interview Composer

Development-only Guest Research Package and Activative Interview Brief runtime.

This package is a structural sibling of `services/interview/` (the
`conscious_activations_interview_expression` product), not a fork of it. It owns
three object types outright:

- `guest_research_package` — name, source URLs, and uploaded reference documents.
- `activative_interview_brief` — operator-authored tension hypothesis, Matrix of
  Edging seed, planned question sequence, and expression targets.
- `composer_session` — a session linking a Brief to a real AIR
  `relationship_activation_state` / `reelcast_progression_program`.

## Boundary

See `AGENTS.md` for the allowed/prohibited boundary declaration. In short:

- Composer may **read** AIR's repository (to cross-validate Brand Context /
  Voice DNA refs and to call `Phase9ActivativeService.compile_relationship_program`).
- Composer may **never write** to AIR's repository, and never constructs
  `matrix_of_edging` / `activation_hypothesis` / `activation_hypothesis_portfolio`
  / `psychological_role_tension_contract` objects (GAP-007 territory).

## Controlling spec

`docs/tech-specs/TS-APP-COMPOSER-001.md` (Interview Composer Service Integration).
