# Planning Requirements Extraction Baseline

Status: `CONFIRMED`

Extraction validation authority: `REQUIREMENTS_EXTRACTION_VALIDATION_REPORT.json`

Epic-design gate: `SATISFIED_STEP_2_AUTHORIZED`

## Scope

This is Step 1 of `handoff/EPICS_AND_STORIES_HANDOFF.md`. It normalizes every authoritative planning obligation before any epic or story is designed. It contains no production implementation and deliberately leaves `epic_ids` and `story_ids` empty.

## Inventory Counts

| Authority type | Count |
|---|---:|
| Functional requirements | 210 |
| Non-functional requirements | 53 |
| Locked decisions | 33 |
| Accepted ADR obligations | 18 |
| Approved UX clauses | 51 |
| Readiness hard gates | 15 |
| Binding anti-goals | 22 |
| Constitutional amendment obligations | 8 |
| **Total** | **410** |

## FR/NFR Coverage Verdicts

| Verdict | Count |
|---|---:|
| `DEFERRED` | 1 |
| `NEEDS_EMPIRICAL_PROTOTYPE` | 38 |
| `NEW_IMPLEMENTATION` | 216 |
| `NOT_APPLICABLE` | 8 |

The verdicts are copied from `docs/tech-specs/REQUIREMENT_COVERAGE_MATRIX.csv`; this extraction does not reclassify requirements.

## Active Blocker Exposure

- `BD-004` affects 83 inventory rows.
- `BD-007` affects 46 inventory rows.
- `BD-008` affects 69 inventory rows.
- `BD-010` affects 47 inventory rows.
- `BD-014` affects 39 inventory rows.

Resolved blocker IDs remain in `blocking_decisions` for provenance. Only currently unresolved external or empirical blockers appear in `active_blockers`.

## Normalized Schema

Each inventory row includes full normative text, enforcement or acceptance evidence, release scope, the existing coverage verdict where applicable, planning disposition, feature/domain, specs and architecture owners, requirement/ADR/decision/UX links, verification strategy, concrete source evidence, repository coverage basis, blocker provenance, active blockers, and future Epic/Story assignment fields.

## Source Authority

- `governance/REQUIREMENTS_REGISTRY.json`
- `governance/DECISION_REGISTER.json`
- `governance/ARCHITECTURAL_PROHIBITIONS.json`
- `governance/READINESS_HARD_GATES.yaml`
- `sources/CCP_ACTIVATIVE_INTELLIGENCE_VISUAL_NARRATIVE_CONSTITUTION_V1_1.md`
- `docs/product-authority/BUILDER_V1_2_CONSTITUTIONAL_ALIGNMENT_AMENDMENT.md`
- `governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
- `docs/contracts/CONTRACT_REGISTRY.yaml`
- `docs/tech-specs/REQUIREMENT_COVERAGE_MATRIX.csv`
- `docs/architecture/ARCHITECTURE_TRACEABILITY_MATRIX.csv`
- `docs/architecture/ADR_REGISTER.yaml` and individual ADRs
- `docs/ux/HARNESS_CONTROL_TOWER_UX_CONTRACT.md`
- `docs/ux/CONTROL_TOWER_UX_TRACEABILITY_MATRIX.csv`

## Confirmation Gate

Human product authority confirmed this inventory as the complete planning baseline on 2026-07-14. The receipt is `V1_2_INVENTORY_CONFIRMATION_RECEIPT.yaml`. Confirmation accepted coverage and extraction, not implementation readiness. Step 2 was subsequently authorized through `EPIC_STEP_2_AUTHORIZATION_RECEIPT.yaml` and completed as a proposed Epic design. Step 3 remains unauthorized, and the five external or empirical blockers remain open.
