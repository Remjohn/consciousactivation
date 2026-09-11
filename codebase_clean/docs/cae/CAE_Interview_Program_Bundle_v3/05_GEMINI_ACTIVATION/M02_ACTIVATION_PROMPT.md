# Gemini Activation Prompt — M02

You are executing **exactly one** CAE Interview Program mandate: **M02**. Do not execute another mandate in this run.

## Mission
Implement the derived hypothesis candidate adapter and diversity-aware working selection using existing authority.

## Authority to load first

1. `00_GOVERNANCE/03_PRD_DELTA.md`
2. `02_TECH_SPEC/01_TS_INTERVIEW_PROGRAM_001.md`
3. `04_MANDATES/M02_Hypothesis_Portfolio_Adapter.md`
4. `05_GEMINI_ACTIVATION/00_MANDATE_EXECUTION_PROTOCOL.md`
5. the repository's current relevant `AGENTS.md` and controlling tech spec(s)
6. the predecessor mandate receipt named by `03_EXECUTION_PLAN/03_IMPLEMENTATION_MATRIX.yaml` if present

## Required behavior

- Read the current repository before writing.
- Verify every symbol/path/owner against the current branch.
- State the exact files you intend to change before editing.
- Make the smallest brownfield-compatible change.
- Reread changed files after each write.
- Run actual tests/verification commands; do not substitute “should pass.”
- Update PRD/spec/gap-ledger surfaces in the same session when durable truth changes, following repository convention.
- Do not invent a new canonical object, route, registry, service owner, or identifier.
- Stop and report `BLOCKED` when ownership or architecture is ambiguous.

## Special Interview Program rules

- Existing Interview Composer remains the integration boundary.
- AIR-owned activation objects remain upstream-owned.
- Question primitives remain provisional unless independently promoted.
- ~96, 16–24, and ~32 are planning targets, not correctness quotas.
- Operator authorization is required before launch.
- Guest-stated evidence, system inference, and Guest-validated interpretation remain distinct.
- Format/archetype compatibility constrains acquisition but cannot manufacture evidence.

## Stop point

When this mandate's objective and acceptance criteria are satisfied, stop. Do not continue to the next mandate.

## Final report

Return the exact receipt shape from `00_MANDATE_EXECUTION_PROTOCOL.md`, including: changed files, actual commands/tests, runtime evidence where required, verified/unverified claims, open gaps, operator decisions needed, and commit hash if code changed.
