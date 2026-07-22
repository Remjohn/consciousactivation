# Conscious Activations Specification Lifecycle V3

This package separates **permanent workflow law** from **campaign-specific instructions**.

## Permanent lifecycle

```text
WRITE
→ INDEPENDENT AUDIT
→ REVISE ONLY FROM FINDINGS
→ INDEPENDENT RE-AUDIT
→ ACCEPTED_FOR_BUILD + HASH LOCK
→ DEVELOPMENT CAPSULE
→ ONE-SPEC BUILD
→ INTEGRATION ACCEPTANCE
```

A Tech Spec is never buildable merely because it was written. It becomes buildable only after an independent audit, any required revision, a fresh independent re-audit, an immutable accepted hash, satisfied upstream dependencies, and a one-spec Development Capsule.

## Included Skills

1. `CA_SPEC_LIFECYCLE_CONTROLLER_SKILL.md`
2. `CA_TECH_SPEC_WRITE_SKILL.md`
3. `CA_TECH_SPEC_AUDIT_SKILL.md`
4. `CA_TECH_SPEC_REVISE_SKILL.md`
5. `CA_TECH_SPEC_REAUDIT_ACCEPT_SKILL.md`
6. `CA_TECH_SPEC_BUILD_SKILL.md`

## Included campaign prompts

1. Program Control convergence
2. Canonical specification reconciliation
3. Full Tech Spec writing factory
4. Independent audit factory
5. Revision factory
6. Re-audit and acceptance factory
7. Development Capsule and build-readiness factory
8. Shared-contract build wave
9. AIR and AHP build waves
10. Imported-interview semantic vertical
11. Rendered batch, Studio correction, and HumanResolution proof

## Recommended models

| Work | Model |
|---|---|
| Authority, product ownership, cross-spec arbitration, final convergence | GPT-5.6 Sol Extra High |
| One bounded Tech Spec, one bounded audit, one bounded revision, one bounded build | GPT-5.6 Sol High |
| Hard semantic vertical integration or unresolved architecture | GPT-5.6 Sol Extra High |

No prompt can guarantee that an agent will never fail. These Skills reduce failure by making ambiguity, missing inputs, path collisions, authority conflicts, and incomplete proof explicit stop conditions.


## V3.1 source-gate correction

V3.1 distinguishes blocking authority/current-implementation/unique-evidence sources from optional research references. Missing optional references create source-gap notices and cannot be cited, but do not stop unrelated specification work. See `HOTFIX_P02_SRC_001.md`.
