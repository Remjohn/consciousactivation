# PROMPT 04 — Independent Per-Spec Audit Factory

**Controller/arbitrator:** GPT-5.6 Sol Extra High  
**Auditors:** GPT-5.6 Sol High  
**Parallel:** Yes. Every spec can be audited concurrently by an independent agent on disjoint audit paths.

Execute the Independent V2.1 Tech Spec Audit Factory.

Do not revise specs. Do not implement code. Do not issue Development Capsules. A writer cannot audit its own spec.

## Required gate

Prompt 03 passes; each target has writing and files-read receipts and state `WRITTEN_PENDING_AUDIT`.

## Per-spec audit

Each child agent:

- audits exactly one spec;
- uses `CA_TECH_SPEC_AUDIT_SKILL.md`;
- reads controlling authority/FRs/Stories/upstream/downstream/current and predecessor source;
- runs all six audit lenses and drift blacklist;
- changes no spec bytes;
- emits audit YAML/MD/files-read receipt;
- returns `ACCEPTED_FOR_BUILD_CANDIDATE`, `REVISION_REQUIRED`, `ARCHITECT_DECISION_REQUIRED`, or `AUDIT_BLOCKED`.

## Controller work

- ensure auditor independence;
- aggregate findings;
- identify cross-spec conflicts;
- assign architecture decisions to Extra High arbitration without changing specs;
- update quality registry;
- create audit status matrix, findings registry, architecture-decision queue, and completion receipt.

Stop after audit publication. Specs requiring changes proceed to Prompt 05. Candidate passes still require Prompt 06.
