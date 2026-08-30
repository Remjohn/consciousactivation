# Source Authority Register

## Authority states

- **CURRENT / live repository:** source inspected from the current public repository.
- **CURRENT DRAFT:** repository document exists but explicitly warns that it is not yet authoritative.
- **BUNDLE-PROVISIONAL:** this v3 document introduces a proposed contract that requires ratification before build authority.
- **CONVERSATION-DERIVED:** decision reconstructed from the supplied conversation export; must not be treated as repository authority until incorporated into the appropriate spec/PRD.

## Repository authorities inspected

| Source | State | Use in this bundle |
|---|---|---|
| `docs/PRD/CURRENT.md` | CURRENT DRAFT | PRD process, FR/story mapping, maintenance discipline |
| `docs/tech-specs/TS-APP-COMPOSER-001.md` | CURRENT repository spec | Composer ownership, object contracts, downstream/upstream boundaries |
| `services/interview-composer/` | CURRENT repository code | Existing service ownership and integration boundary |
| `services/interview-composer/AGENTS.md` | CURRENT repository guidance | Prohibitions on AIR-owned object construction inside Composer |
| `docs/MANDATE_01_builder_schema_update.md` | CURRENT mandate precedent | Brownfield mandate style: verified state, exact enforcement point, scope, acceptance |
| `docs/ONE_HARNESS_BUILD_PROMPT.md` | CURRENT execution precedent | One task/run, explicit input/output, ordered steps, stop gate, verification |
| `docs/cae/CAE_Question_Intelligence_Audit_Bundle_v4/audits/` | CURRENT audit corpus referenced in supplied conversation | Research evidence for Question Intelligence synthesis |

## Critical repository finding

`docs/PRD/CURRENT.md` currently states in its header that it is **DRAFT — DO NOT YET TREAT AS AUTHORITATIVE**, while also declaring a maintenance rule requiring relevant PRD sections to be updated in the same session when work changes them. This bundle therefore uses the PRD as the current product-planning source but does not claim ratification of the new Interview Program requirements. Any implementation pass must preserve this distinction and perform the appropriate PRD/spec maintenance in the same session.

## Composer boundary

The Composer tech spec states that the service owns the Guest Research Package, Activative Interview Brief, and Composer Session and treats the human operator as the consumer of record for the current composing surface. It also documents the existing planning-lineage/Brief boundary and explicit upstream dependencies. This bundle therefore extends the existing Composer rather than defining a replacement interview engine.

## Runtime-authority caution

This bundle never assumes that a conversational concept is already a live repository symbol. Every implementation mandate requires a fresh brownfield check of the actual branch before editing. If a symbol, route, schema, repository, or owner differs from the bundle's expectation, the agent must stop and reconcile rather than invent a replacement.
