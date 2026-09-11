# Gemini Mandate Execution Protocol

This protocol is designed to make Interview Program mandates executable in the same discipline as the repository's existing one-harness execution prompts.

## One mandate, one run

Run exactly one mandate per Gemini activation. Do not batch multiple mandates. A mandate may call multiple tests/commands, but it has one bounded objective, one implementation boundary, and one completion receipt.

## Execution sequence

1. **Load authority.** Read the mandate, referenced PRD/spec sections, current relevant `AGENTS.md`, and the exact implementation sources named by M01 or the preceding receipt.
2. **Reconnaissance.** Inspect the current branch; never trust a previous session's symbol/path assertion without checking it.
3. **Plan.** State the exact files likely to change, dependencies, tests, and stop conditions.
4. **Execute.** Make the smallest change that satisfies the mandate. Do not invent architecture.
5. **Reread.** Re-read every changed file immediately after writing.
6. **Verify.** Run the actual repository test/lint/type/runtime commands applicable to the changed paths.
7. **Reality check.** For semantic claims, prove a real persisted/runtime path where required by the mandate.
8. **Document.** Update PRD/spec/gap-ledger surfaces in the same session when durable product/technical truth changes, following the repository's current maintenance law.
9. **Report.** Return exact files changed, tests, runtime evidence, claims proved, claims unproved, open risks, and commit hash if code was changed.
10. **Stop.** Do not continue automatically into the next mandate.

## Mandatory prohibitions

- Do not create `InterviewHarnessV2`, `QuestionSystem`, `ContentHypothesis`, or canonical `QuestionProgram` merely to satisfy the mandate.
- Do not move AIR-owned objects into Composer.
- Do not declare success from mocked adapters or receipts alone.
- Do not silently expand scope.
- Do not overwrite a current Operator decision from stale state.
- Do not hide uncertainty; classify it.

## Claim vocabulary

Use only:

- `VERIFIED` — demonstrated by direct evidence in this run;
- `PARTIALLY_VERIFIED` — some but not all required evidence exists;
- `UNVERIFIED` — asserted but not demonstrated;
- `BLOCKED` — cannot proceed without a decision/owner/dependency;
- `NOT_APPLICABLE` — explicitly justified.

## Completion receipt shape

```yaml
mandate_id: Mxx
status: ACCEPTED|EXECUTED_PENDING_REVIEW|BLOCKED
commit: <hash-or-null>
changed_files: []
tests:
  - command: <actual command>
    result: PASS|FAIL
    evidence: <summary>
runtime_evidence: []
claims_verified: []
claims_unverified: []
open_gaps: []
operator_decisions_needed: []
```
