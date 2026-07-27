---
revision_id: "REVISION-CMF-TS-062-070"
title: "CMF Frontier Tech Spec Revision Receipt - TS-CMF-062 through TS-CMF-070"
status: "accepted"
created_at: "2026-06-22"
audit_source: "THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/audit_reports/TS-CMF-062-070-frontier-audit.md"
protocol_source:
  - "THE CMF STUDIO/docs/architecture/april_updates/TRIGGER_COMMAND_REVISION.md"
  - "THE CMF STUDIO/docs/architecture/april_updates/PROMPT_Spec_Revision.md"
---

# Revision Receipt

## Decision Log

**Decision 1 - Agent Factory Requirement Trace IDs**

Epic 11 is governed by PRD module requirements `PRD-CMF-10.00` through `PRD-CMF-10.08` and supporting `PRD-CMF-02.03` through `PRD-CMF-02.05`, not by newly invented `FR-CMF` IDs. Because the current `RequirementTrace` contract stores a required `fr_id` string, the Agent Factory tech-spec frontmatter now uses the relevant PRD requirement IDs in `fr_ids` while preserving the same values in `module_requirement_ids`.

**Decision 2 - JIT Skill Modes Are First-Class**

Interview engineering, narrative induction, source expression contrast, and scene prompt support after route are first-class JIT use modes. They are not aliases for generic script writing. Scene prompt support is explicitly downstream of approved source expression, route receipt, and Complete Editing Session.

## Per-Spec Revisions

### TS-CMF-062 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.00`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-063 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.01`, `PRD-CMF-02.03`, and `PRD-CMF-02.05`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-064 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.02`, `PRD-CMF-02.03`, and `PRD-CMF-02.05`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-065 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.03` and `PRD-CMF-10.04`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-066 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.05`.
- Replaced soft use-mode language with mandatory migration of `SkillUseMode` to include `interview_engineering`, `narrative_induction`, `source_expression_contrast`, and `scene_prompt_support_after_route`.
- Added explicit `SkillUseMode` enum values to the primary output schema.
- Added acceptance criteria and testing requirements for the new JIT modes and the post-route scene prompt gate.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.
- Resolves: `TS-CMF-066 / TS-CMF-015 | LENS 5 | CRITICAL`.

---

### TS-CMF-067 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.06`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-068 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.08`, `PRD-CMF-02.04`, and `PRD-CMF-02.05`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-069 - Required Fixes

- Populated `fr_ids` with `PRD-CMF-10.07` and `PRD-CMF-02.04`.
- Resolves: `TS-CMF-062 through TS-CMF-069 | LENS 1 | WARNING`.

---

### TS-CMF-015 - Dependency Repair

- Added `interview_engineering`, `narrative_induction`, `source_expression_contrast`, and `scene_prompt_support_after_route` to the documented `SkillUseMode` enum.
- Added fallback behavior for `SCENE_PROMPT_SUPPORT_PRE_ROUTE_BLOCKED`.
- Added acceptance criteria and testing requirements for the new use modes.
- Resolves: `TS-CMF-066 / TS-CMF-015 | LENS 5 | CRITICAL`.

---

## Workflow Artifact Repair

- Created `THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/audit_reports`.
- Created `THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/revision_receipts`.
- Created `THE CMF STUDIO/docs/architecture/cmf_studio_build_workflow/build_receipts`.
- Wrote this revision receipt and the matching frontier audit report.
- Resolves: `CMF Build Workflow Ledger | LENS 5 | WARNING`.

## Final Acceptance

`TS-CMF-062` through `TS-CMF-070` are accepted for build after revision. The next implementation sequence should begin at `TS-CMF-062` and continue through `TS-CMF-070`, with a small dependency repair to runtime `SkillUseMode` before or during `TS-CMF-066`.
