# CAE-BMAD Documentation and Planning Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M05  
**Scope:** Agent responsibilities, modular PRD authoring, functional requirements matrix, epic/story decomposition, and plan genealogy for the Documentation (Level 02) and Plan (Level 03) operating levels.

---

## 1. Purpose

Before any code or architecture work begins, CAE-BMAD requires a governed documentation and planning layer that:
1. **Decomposes reconstructed product intent** (from M04) into modular, traceable PRD modules.
2. **Compiles atomic functional requirements** (FR-xxx) with testable acceptance criteria.
3. **Sequences delivery** through epic/story decomposition tied to PRD modules and FRs.
4. **Preserves CCP modular PRD tradition** — the original Conscious Platform used a modular, indexed PRD pattern where each product capability had its own self-contained specification module.

---

## 2. Agent Architecture for Levels 02–03

```text
Level 02: DOCUMENTATION
  ├── cae-documentation-analyst   — Audits all specs, detects drift, validates reference integrity
  └── cae-prd-agent               — Authors modular PRD modules and the FR matrix

Level 03: PLAN
  ├── cae-plan-analyst            — Tracks plan genealogy, milestone dependencies, execution gaps
  └── cae-delivery-agent          — Decomposes PRDs and FRs into epics and user stories
```

### 2.1 Agent Coordination Protocol
1. `cae-documentation-analyst` audits existing documentation and reports drift findings.
2. `cae-prd-agent` consumes the Product Reconstruction Record (M04) and emits modular PRD modules.
3. `cae-plan-analyst` maps historical milestone genealogy and identifies execution gaps.
4. `cae-delivery-agent` decomposes PRDs into epics and stories with concrete acceptance criteria.

---

## 3. Modular PRD Standard

Each PRD module is a self-contained specification document with:

| Field | Requirement |
|---|---|
| `module_id` | Pattern `PRD-xxx` (e.g. `PRD-001`) |
| `title` | Descriptive module title |
| `capability_pillar` | One of the 5 capability pillars from M04 |
| `source_lineage` | Array of `SRC-xxx` references with fidelity status |
| `functional_requirements` | Array of `FR-xxx` entries, each with description, testability flag, and acceptance criteria |
| `acceptance_criteria` | Module-level acceptance criteria |

### 3.1 Functional Requirement Standard
Every FR must be:
- **Atomic:** Tests exactly one behavior.
- **Testable:** The `testable` flag must be `true`; vague requirements are rejected.
- **Traceable:** Must cite at least one upstream source (`SRC-xxx`) and one downstream acceptance criterion.

---

## 4. Epic/Story Decomposition Standard

Each epic groups related FRs into a cohesive delivery unit:

| Field | Requirement |
|---|---|
| `epic_id` | Pattern `EPIC-xxx` (e.g. `EPIC-001`) |
| `prd_modules` | Array of `PRD-xxx` references |
| `functional_requirements` | Array of `FR-xxx` references |
| `stories` | Array of user stories with `STORY-xxxx` IDs |

Each story uses the canonical format:
- **As a** `<persona>`
- **I want** `<capability>`
- **So that** `<business value>`
- Plus concrete, testable acceptance criteria.

---

## 5. Plan Genealogy and Milestone Tracking

The `cae-plan-analyst` maintains:
1. **Historical milestone register** tracing M01–M72+ legacy milestones.
2. **Dependency DAG** showing which epics block which downstream work.
3. **Execution gap register** identifying planned deliverables that were bypassed or partially delivered.
