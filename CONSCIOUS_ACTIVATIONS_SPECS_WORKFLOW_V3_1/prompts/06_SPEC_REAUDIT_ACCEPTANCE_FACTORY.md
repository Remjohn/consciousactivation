# PROMPT 06 — Independent Re-Audit and Accepted-Spec Factory

**Integrator:** GPT-5.6 Sol Extra High  
**Re-auditors:** GPT-5.6 Sol High  
**Parallel:** Yes per spec. Final cross-spec convergence and hash locking are sequential under one Extra High integrator.

Execute the V2.1 Tech Spec Re-Audit and Acceptance Factory.

Do not implement code. Do not let original writers or revisers perform controlling re-audits.

## Required gate

Prompt 05 passes; revised specs have revision receipts/finding matrices. Candidate-pass specs from Prompt 04 also enter this stage.

## Per-spec work

Each re-auditor:

- processes exactly one spec;
- uses `CA_TECH_SPEC_REAUDIT_ACCEPT_SKILL.md`;
- audits the complete current spec, not only revisions;
- verifies all original findings and detects new defects;
- returns `ACCEPTED_FOR_BUILD`, `REVISION_REQUIRED`, `ARCHITECT_DECISION_REQUIRED`, or `REAUDIT_BLOCKED`;
- for accepted specs emits re-audit report and acceptance receipt.

## Integrator work

1. Run a cross-spec reference-slice trace from imported interview to replay.
2. Verify shared objects have one producer/owner and compatible consumers.
3. Reject acceptance where implementation would require invention.
4. Hash-lock accepted specs.
5. Publish accepted spec registry/hash lock, convergence report, status matrix, and completion receipt.

Any failed spec loops back to Prompt 05. Stop when the active implementation set is accepted and hash-locked.
