# Acceptance Criteria

1. Given active saturation, a frozen boundary, an unratified Draft Harness Model and
   versioned nodes, the command selects exactly one dependency-ready question.
2. Every node declares stable identity/version, applicability, question, rationale,
   evidence requirements, dependencies, options, recommendation policy, authority,
   affected paths, invalidation edges and completion rule.
3. Locked nodes remain visible with typed missing prerequisites and cannot be issued.
4. Recommendation cites exact active evidence and Draft Model state, separates fact
   from inference, lists viable alternatives/trade-offs/consequences and states that
   human ratification has not occurred.
5. Unsupported affected paths, missing evidence, non-human decision authority,
   malformed options, premature nodes or recommendation drift fail closed under HG-001.
6. No package contains an answer, final value, approval or Harness IR mutation.
7. At most one question is active per run; a second active package is rejected.
8. Identical inputs produce byte-identical graph/package/receipt; changed inputs
   produce new immutable identities.
9. Duplicate commands replay safely; conflicting payloads fail closed.
10. Atomic failure leaves no package, receipt, event, command or observation intent.
11. Invalidation clears active state while preserving historical canonical bytes.
12. Required observations, architecture boundaries and predecessor behavior pass.
