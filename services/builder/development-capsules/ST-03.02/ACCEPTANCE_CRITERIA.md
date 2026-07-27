# Acceptance Criteria

1. Given one active question, when the declared human records an answer and final
   decision, then they remain separate immutable attributable artifacts.
2. The transaction atomically stores the answer, decision, IR amendment, memory,
   receipt, event and observation intents.
3. Agent, code, external, expired, wrong-resource and unknown authority fail closed.
4. Replayed approval is rejected; command retry returns the original receipt only.
5. Decision value must be one declared option and must target the selected unratified
   Draft Harness Model path.
6. Provisional advisory material never becomes ratified without the human decision.
7. Dependency completion deterministically unlocks descendants; terminal cascade lock
   is true only when all graph decisions are ratified.
8. Contradictory locks, stale/invalidated inputs and altered lineage fail closed.
9. Identical governed inputs produce byte-identical artifacts and receipts.
10. Resume reconstructs decisions and outstanding nodes without replaying answers.
11. Reopen invalidates affected amendments and descendant decisions without deleting
    historical bytes.
12. Observability, rollback, architecture and all predecessor regressions pass.
