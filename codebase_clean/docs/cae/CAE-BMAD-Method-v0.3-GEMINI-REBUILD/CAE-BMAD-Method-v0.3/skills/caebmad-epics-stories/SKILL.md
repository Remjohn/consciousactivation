---
name: caebmad-epics-stories
description: Skill for decomposing PRDs and functional requirements into traceable epics and user stories with testable acceptance criteria.
version: 0.3.0-rebuild
agent: cae-delivery-agent
---

# Skill: caebmad-epics-stories

## 1. Purpose & Invocation
The `caebmad-epics-stories` skill enables the `cae-delivery-agent` and `cae-plan-analyst` to decompose modular PRD modules and functional requirements into actionable epics and user stories.

## 2. Invocation Preconditions
1. At least one approved PRD module exists at `docs/cae-bmad/03_product/modules/PRD-*.md`.
2. Functional Requirements matrix is available.
3. Epic/story schema (`schemas/epic_story.schema.json`) is available.

## 3. Execution Logic
1. **PRD Module Intake:** Read the target PRD module(s) and extract FRs.
2. **Epic Grouping:** Cluster related FRs into cohesive delivery epics (`EPIC-xxx`).
3. **Story Authoring:** For each epic, write user stories in canonical "As a / I want / So that" format with concrete acceptance criteria.
4. **Complexity Estimation:** Descend to `Level 10: MODULE` and `Level 12: FUNCTION` to estimate implementation touch points.
5. **Schema Validation:** Validate against `schemas/epic_story.schema.json`.

## 4. Output Contract
- Epic documents at `docs/cae-bmad/05_planning/EPICS.md`
- Story backlog at `docs/cae-bmad/05_planning/STORIES.md`
- Story readiness checklists
