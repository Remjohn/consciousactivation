# PROMPT 08 — Shared Contract Build Wave

**Controller/integrator:** GPT-5.6 Sol Extra High  
**Per-spec builders:** GPT-5.6 Sol High  
**Parallel:** Limited. Shared canonical schemas and compatibility policy are serialized; language bindings, fixtures, and isolated consumer tests may run in parallel after schema bytes freeze.

Build the accepted shared-contract specifications using `CA_TECH_SPEC_BUILD_SKILL.md`.

Do not implement AIR/AHP application services. Do not render media. Do not begin VAE Stage 5. Do not call/train models.

## Required gate

Prompt 07 passes; each target spec is accepted/hash-locked and has a valid capsule.

## Build order

1. canonical object identities and field authority;
2. semantic schemas;
3. execution schemas;
4. compatibility/versioning/migrations;
5. canonical serialization/hash helpers;
6. generated Python/TypeScript declarations;
7. positive/negative fixtures;
8. product consumer-conformance fixtures;
9. release manifest/receipt/clean-room validation.

Each child builds one accepted spec only. Spec defects cause `BUILD_AMBIGUITY` and return to Prompt 04/05/06.

Publish a local, non-production, uncertified shared release. Stop after clean-room and consumer-conformance pass.
