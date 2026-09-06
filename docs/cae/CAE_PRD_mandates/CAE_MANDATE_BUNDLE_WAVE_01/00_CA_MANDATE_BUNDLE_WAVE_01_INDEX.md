# CAE Mandate Bundle — Wave 01

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_01`  
**Scope:** Canonical Questions Q01–Q08  
**Status:** Execution-ready mandate bundle  
**Date:** 2026-09-06

## Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. Master 57-Question Decision & Convergence Canon
3. CAE Product Brief / PRDs / Functional Requirements
4. `UI.md`
5. `Architecture.md`
6. Individual mandates in this bundle
7. Repository implementation and executable evidence

## Wave strategy

Wave 01 deliberately follows the first eight canonical questions in order:

`Audience layers → dual-context convergence → Subject Constitution → causal ordering → format/archetype feasibility → Activative/Elicitation linkage → Activative derivation → frozen content portfolio`

These mandates are bounded. They do not claim that later questions are implemented merely because their interfaces are prepared.

## Execution rule

Execute one mandate at a time unless the Operator explicitly authorizes parallelism and the outputs are independently mergeable. Shared state, migrations, registries, and authority decisions have one integration owner.

Every mandate requires repository inspection, positive and negative executable evidence, exact evidence locators, explicit distinction between documented claims and executable proof, no adjacent-mandate implementation, exact commit SHA, and explicit Operator approval/rejection before proceeding.

## Files

| File | Canonical question | Invariant / requirement |
|---|---:|---|
| `02_CA_MANDATE_001.md` | Q01 | `INV-AUD-001 / FR-AUD-001` |
| `03_CA_MANDATE_002.md` | Q02 | `FR-CONV-001` |
| `04_CA_MANDATE_003.md` | Q03 | `INV-SUB-001` |
| `05_CA_MANDATE_004.md` | Q04 | `INV-CAUSAL-001` |
| `06_CA_MANDATE_005.md` | Q05 | `FR-ARCH-001` |
| `07_CA_MANDATE_006.md` | Q06 | `FR-ELIC-001` |
| `08_CA_MANDATE_007.md` | Q07 | `INV-ACT-001` |
| `09_CA_MANDATE_008.md` | Q08 | `FR-PORT-001` |

## Status discipline

The Master Canon contains ratified decisions and may describe a production-authorized target state. The mandate executor must not convert those statements into false claims about the current repository. Completion of each mandate is determined by executable evidence from the actual codebase.

## Bundle completion

Wave 01 is complete only when all eight mandates independently meet their evidence standards and receive the required Operator decisions. A green result for one mandate does not imply green results for the others.
