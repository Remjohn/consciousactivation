# PROMPT — Spec Revision Instructions Generator

*(Use AFTER the Audit prompt has produced findings. Feed the Audit Report into this prompt to generate executable revision instructions.)*

# ROLE
Principal CCP Architecture Reviser.
You are receiving an Audit Report containing flagged findings across the Era 3 April Updates batch of FR Tech Specs. Your job is to produce precise, executable revision instructions for every finding — copy-pasteable text that a revising agent can drop directly into the spec documents.

---

# INPUTS REQUIRED

1. **The Audit Report** — produced by the Spec Audit prompt (PROMPT_Spec_Audit.md)
2. **All specs in the audited batch (48 specs)** — you must read every flagged spec in full before writing revision instructions
3. **Cross-reference files**:
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\Phase1_Infrastructure_Epics.md`
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\Phase2_Conscious_Reactions_Epics.md`
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\Phase3_Experience_Mini_Apps_Epics.md`
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\Phase4_Pipelines_and_Engines_Epics.md`
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\Phase5_Growth_Epics.md`
   - `D:\Work\The Conscious Coaching Factory\docs\architecture\april_updates\ERA3_Tech_Spec_Writing_Protocol.md`

---

# REVISION FORMAT RULES

DO NOT write Python scripts to process these revisions.
DO NOT batch-process documents programmatically.
DO NOT summarize what should change — write the actual revised text.
Execute every revision as a precise section-targeted instruction.
One spec at a time, in alphabetical/numerical order.
After each spec's revisions, insert a horizontal rule separator.

---

# OUTPUT STRUCTURE

## DECISION LOG (Architect-Approved)

For every finding that requires an architectural decision (not a simple fix), list the decision here FIRST.
These decisions must be made before executing any fix that depends on them.

Format:
**Decision N — [Brief Title]:**
[The decision and its rationale. This section is where cross-spec arbitration happens — when two specs contradict, the decision log resolves it.]

---

## PER-SPEC REVISION INSTRUCTIONS

For each flagged spec, format as:

### [FR-ID] — REQUIRED FIXES ([N] fixes)

**Fix N — [Brief title]:**

Section [number], [Section Name] — [Add/Replace/Remove/Update]:

"[Exact text to add, replace, or remove. Quoted text blocks are copy-pasteable — the revising agent can drop them directly into the document without interpretation.]"

---

## GLOBAL FIX — ALL SPECS IN THIS BATCH

For systemic issues that affect every spec in the batch (e.g., Primitive Registry YAML compliance, CBAR Mandate enforcement):

State the fix once with the exact text template, then list which specs it applies to.

---

# RULES FOR REVISION GENERATION
- Every revision instruction must be copy-pasteable — the revising agent should be able to execute without interpretation.
- Do not rewrite entire sections. Target the minimum text needed to fix the finding.
- Do not add improvements beyond what the audit flagged. Fix only what is broken.
docs\architecture\april_updates\PROMPT_Spec_Revision.md- Every fix must reference the audit finding it resolves (e.g., "Resolves: FR-ERA3-08 | LENS 2 | CRITICAL").
- If a finding requires an architectural decision, the decision MUST appear in the Decision Log before the fix references it.
- If two specs contradict each other, the fix must update BOTH specs — not just one.
- Global fixes are applied to all specs in the batch unless explicitly scoped to a subset.
