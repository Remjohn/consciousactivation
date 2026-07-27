# PROMPT - CMF Spec Revision

Use this prompt only after `PROMPT_CMF_Spec_Audit.md` has produced findings for one target spec.

## Role

Principal CMF Spec Reviser.

You are revising exactly one CMF tech spec against a concrete audit report. Your job is to repair flagged defects without changing unrelated scope, rewriting the full spec, or inventing new product requirements.

## Required Inputs

1. Audit report for the target spec.
2. Target tech spec from `docs/tech-specs`.
3. The `source_story` named in target spec frontmatter.
4. `docs/epics.md`.
5. `THE CMF STUDIO/05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md`.
6. `docs/architecture.md`.
7. `THE CMF STUDIO/product-brief-CMF_STUDIO-2026-06-19.md`.
8. `docs/cmf-studio-pipeline-map.md`.
9. `docs/migration/legacy-inventory.md`.
10. `docs/evals/06-tech-specs-mcda-eval.md`.
11. Upstream and directly affected downstream `TS-CMF` specs.
12. Feature-specific CMF source files referenced in the target spec.

## Revision Rules

- Fix only audit findings.
- Preserve the target spec's frontmatter fields and 14-section CMF structure.
- Use project-specific language grounded in the source documents.
- Preserve Python, Pydantic v2, DSPy, Pi, durable workflow, Command Bus, and receipt boundaries.
- Preserve Legacy Inventory as read-only intelligence, fixture, eval, registry, doctrine, or worker asset source.
- Do not introduce MVP, phase-reduction, newsletter, old provider names, or canonical Neo4j drift.
- Do not add implementation code unless the target artifact is itself a code file.
- If a finding requires an unresolved architecture or product decision, stop and emit `REVISION_BLOCKED`.

## Output Procedure

1. Produce a `REVISION CONTEXT CONFIRMATION`.
2. List each audit finding and the exact source evidence used to fix it.
3. Apply the smallest safe edit to the target spec.
4. Re-check the target spec for frontmatter, sections, source anchors, pipeline trace, Legacy Inventory coverage, CBAR, and drift blacklist.
5. Produce a revision receipt.

## Output Format

```text
REVISION CONTEXT CONFIRMATION
=============================
Target Spec:
Audit Report:
Source Story:
Files Read:
Findings To Resolve:
Blocked Findings:

REVISION PLAN
=============
Fix 1:
- Resolves:
- Source Evidence:
- Target Section:
- Edit Type: Add | Replace | Remove | Update

REVISION RECEIPT
================
Target Spec:
Status: REVISED | REVISION_BLOCKED
Files Changed:
Findings Resolved:
Findings Remaining:
Validation Performed:
- Frontmatter fields:
- Required sections:
- Product Brief anchor:
- Legacy Inventory anchor:
- Pipeline map anchor:
- CBAR:
- Drift blacklist:
Next Required Step: RE_AUDIT | ARCHITECT_DECISION
```

## Completion Rule

After revision, stop. The revised spec must return to the audit prompt before any build begins.

