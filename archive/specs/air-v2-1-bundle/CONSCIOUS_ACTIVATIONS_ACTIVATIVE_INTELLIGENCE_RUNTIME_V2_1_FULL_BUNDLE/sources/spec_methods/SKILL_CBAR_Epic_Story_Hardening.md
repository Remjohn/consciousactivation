# SKILL: CBAR Epic & Story Hardening
# Version: 1.0
# Date: 2026-05-09
# Status: Source of Truth
# Purpose: Governs the adversarial hardening of all CCP Epic and User Story documents using Constraint-Based Adversarial Reasoning

---

## ⚠️ ANTI-LAZINESS & ANTI-DRIFT PROTOCOL — READ THIS FIRST

> **THIS IS NOT OPTIONAL. THIS IS THE LAW OF THIS TASK.**
>
> Epics and Stories are the functional blueprint of the entire CCP engineering effort.
> If a story passes through this pipeline with an unresolved architectural tension,
> the downstream engineer will build technically functional code that **violates the behavioral psychology** the platform is built on.
> **One "happy-path" story is worse than no story.**

### What Counts as FAILURE (Task will be considered FAILED if any of these are true):

1. **You gave a PASS without finding a tension.** Every story has at least one tension between its technical implementation and its mapped Experience Primitive. If you found zero tensions, you did not read the primitive's `misuse_modes`, `suppression_conditions`, or `conflicts_with` fields.
2. **Your failure scenario is vague.** "The user will have a bad experience" is not a scenario. A real scenario names the specific psychological drop-off point, the specific primitive violation, and the downstream behavioral consequence (bounce, churn, buyer's remorse, cognitive overload).
3. **Your resolution hallucinated the physics away.** If you wrote "the system will do this instantly" without checking whether the underlying infrastructure (network round-trips, DB provisioning, OS permission gates, Stripe SCA flows) actually permits instant execution, you have produced a dangerous fiction.
4. **You skipped the Downstream Proof.** Every resolution must prove it does not break the next story in the cascade. If Story 1.1's resolution changes how authentication works, Story 1.2 and 1.3 must structurally inherit that change.
5. **You did not read the source documents.** You relied on the story text alone. You did not open the PRD module, the Tech Spec, or the YAML primitive file.

---

## 1. Task Definition

You are executing a **CBAR Adversarial Audit** on existing CCP Epic and User Story documents. Your job is NOT to rewrite stories from scratch. Your job is to:

1. Read each story as drafted.
2. Load the mapped Experience Primitive YAML.
3. Load the parent PRD module and/or Tech Spec for architectural context.
4. Force a 4-part CBAR tension resolution against each story.
5. Output a **CBAR Audit Manifest** with verdicts, rewrites, and a Constraint Resolution Manifest.

**Output:** One `.md` file saved to `docs/architecture/cbar_audits/CBAR_Audit_Phase{N}_{Epic_Name}.md`

---

## 2. Mandatory Pre-Audit Loading Sequence

Before analyzing any story, you MUST load and read the following files in this exact order. Do not skip or summarize. Actually read them.

### Step 1: Load the CBAR Theory (The Reasoning Engine)
- `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning.md` — Read Part I (Sections 1-6). Internalize the 4-part anatomy, the Policy Decay Curve, and the Applicability Boundaries. This is the mental model you are executing.

### Step 2: Load the Target Epic Document (The Input)
- Load the Phase Epic file being audited (e.g., `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md`)
- Read every story. Note the mapped Primitive IDs.

### Step 3: Load Every Mapped Primitive YAML (The Alphabet)
- For each Primitive ID referenced in the Epic (e.g., `EXP-FRC-002`, `EXP-FBK-001`), load the full YAML file from `primitives/experience/[family_name]/[PRIMITIVE_ID].yaml`
- Read the following fields with extreme care: `core_move`, `why_it_works`, `misuse_modes`, `suppression_conditions`, `conflicts_with`, `activation_conditions`
- These fields are the adversarial ammunition. If you don't read them, you will produce a generic, Level 1 compliance check instead of a true CBAR audit.

### Step 4: Load the Parent PRD Module (The Physics)
- Load the PRD module governing this Epic's domain (e.g., `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` for infrastructure, `PRD_04_CVE_Experience_Design.md` for experience)
- Read the architecture sections, schema sections, and implementation/stack sections
- This is where you learn the **real physics**: what the backend actually does, what latency exists, what Stripe/Telegram/React limitations apply

### Step 5: Load the Tech Spec (if it exists)
- If a matching Tech Spec exists (e.g., `docs/architecture/april_updates/FR-ERA3-08_Mini_App_Separation_Architecture_Tech_Spec.md`), load it
- The Tech Spec contains the actual API contracts, database schemas, and processing pipelines that constrain the implementation
- This is the document that prevents you from hallucinating away the physics

### Step 6: Load the ERA3 Protocol (for Protocol-Level Gaps)
- `docs/architecture/april_updates/ERA3_Epic_and_Story_Writing_Protocol.md`
- Identify if the protocol itself has structural weaknesses that allowed the stories to pass without adversarial review

---

## 3. The CBAR Audit Engine (The Cognitive Tool)

For EACH story in the target Epic, execute the following 4-part CBAR sequence. This is NOT a checklist you skim. Each part is a forced derivation step. You cannot proceed to the next part without completing the current one.

### Part 1 — The Tension (MANDATORY)

**Instruction:** Identify two specific, concrete constraints that are individually valid but cannot both be satisfied simultaneously with the story's current implementation.

**Rules:**
- One constraint MUST be from the mapped Experience Primitive YAML (`core_move`, `activation_conditions`, or `misuse_modes`)
- The other constraint MUST be from the technical architecture (PRD, Tech Spec, or known infrastructure physics)
- Abstract tensions ("quality vs. speed") are BANNED. Name the specific rule and the specific technical limitation.
- If you genuinely cannot find a tension after reading all sources: state "No tension found" and provide a 3-sentence justification citing the specific primitive fields you checked. Do NOT fabricate a tension.

### Part 2 — The UX Failure Scenario (MANDATORY)

**Instruction:** Describe the exact user behavior that will result if the story is implemented as-is without resolving the tension.

**Rules:**
- Name the specific psychological event: cognitive overload, System 2 activation, dopamine crash, identity violation, friction spike, trust erosion
- Name the specific user action: bounce, abandon, close app, delay, churn, buyer's remorse
- Name the specific primitive violation: which field of the YAML is being violated and how
- "The user will have a bad experience" is a FAILED scenario. Be surgical.

### Part 3 — The Resolution Demand (MANDATORY)

**Instruction:** Derive which constraint takes precedence. State the rule that grants that precedence. Declare the specific architectural action the story's Acceptance Criteria must enforce.

**Rules:**
- You MUST derive the answer. Do not pre-answer. Walk through the logic.
- Check: Does the PRD or Tech Spec already contain a resolution? If yes, cite it.
- Check: Does the Primitive's `why_it_works` contain the theoretical justification for precedence? If yes, cite it.
- The resolution must be implementable. "Make it faster" is not a resolution. "Inject the DPA palette via URL parameter to eliminate the network round-trip" is a resolution.

### Part 4 — The Downstream Proof (MANDATORY)

**Instruction:** Prove that your resolution does not break the next story in the cascade.

**Rules:**
- Name the downstream story by number (e.g., "Story 1.2 inherits this constraint")
- State what input the downstream story expects
- Confirm that your resolution produces that input, OR flag a secondary conflict
- If your resolution creates a new conflict with a downstream story, you MUST resolve that conflict before proceeding. This is the Cascade Lock.

---

## 4. The Constraint Resolution Manifest (Final Output)

After all stories in an Epic have been audited, produce a **Constraint Resolution Manifest** at the bottom of the audit document. This is a numbered list of canonical engineering mandates.

**Format:**
```markdown
## Constraint Resolution Manifest

Based on the adversarial simulations executed above, the following structural mandates are permanently appended to the Phase [N] execution plan. Engineering teams must treat these resolutions as canonical.

1. **The [Name] Rule:** [One-sentence mandate derived from the CBAR resolution]
2. **The [Name] Rule:** [One-sentence mandate derived from the CBAR resolution]
...
```

**Rules for the Manifest:**
- Every mandate must be traceable to a specific CBAR Question number in the document
- Every mandate must name the specific primitive it protects
- Every mandate must be implementable as a testable engineering constraint (not a vague guideline)

---

## 5. CBAR Verdicts (Per-Story Scoring)

Each story receives exactly one verdict:

| Verdict | Meaning |
|---|---|
| **PASS** | The story's current Acceptance Criteria already resolve the identified tension. No rewrite needed. |
| **PASS WITH NOTE** | The story resolves the primary tension but has a minor gap (e.g., missing edge case). Append a note, not a full rewrite. |
| **REWRITE REQUIRED** | The story's Acceptance Criteria fail to resolve the tension. A rewritten BDD block must be provided. |
| **FATAL CONFLICT** | The story's resolution conflicts with another story's resolution. Both must be rewritten as a pair. |

**Rewrite Format (when REWRITE REQUIRED):**
```markdown
**Original Acceptance Criteria:**
*   Given [original]
*   When [original]
*   Then [original]

**CBAR-Hardened Acceptance Criteria:**
*   Given [rewritten]
*   When [rewritten]
*   Then [rewritten — incorporating the resolution]
*   And [additional constraint from the resolution]
```

---

## 6. Anti-Hallucination Protocol (The Physics Check)

This is the gate that separates a Level 1 compliance check from a true CBAR audit.

Before finalizing ANY resolution, run this internal verification:

```
PHYSICS CHECK — Story [X.Y]
├── Does my resolution assume instant network responses?     → Check Tech Spec for actual latency
├── Does my resolution assume the user has permissions?      → Check if OS-level gates exist (mic, camera, location)
├── Does my resolution assume Stripe clears instantly?       → Check for SCA/3D Secure edge cases
├── Does my resolution assume the DB is provisioned?         → Check for async provisioning pipelines
├── Does my resolution assume the cache is fresh?            → Check for invalidation strategies
├── Does my resolution assume all primitives cooperate?      → Check `conflicts_with` fields in YAMLs
└── If ANY assumption is unverified: flag it. Do not proceed.
```

If you cannot verify a physics assumption because the Tech Spec doesn't exist yet, explicitly state: "UNVERIFIED ASSUMPTION: [description]. This must be resolved during Tech Spec writing."

---

## 7. Execution Protocol

### For Each Phase Epic:

1. **Load** — Follow §2 (Mandatory Pre-Audit Loading Sequence) exactly
2. **Audit** — Execute §3 (The CBAR Audit Engine) for every story in the Epic
3. **Physics Check** — Run §6 against every resolution
4. **Manifest** — Produce §4 (The Constraint Resolution Manifest)
5. **Self-Review** — Re-read all resolutions as a batch. Check for Cascade Lock violations (does Resolution A contradict Resolution B?)
6. **Declare Complete** — Only after the Cascade Lock is clean

---

## 8. Post-Audit Verification Checklist

Run this checklist BEFORE declaring the audit complete. Every box must pass.

```
STRUCTURAL CHECKS
[ ] All stories in the Epic have been audited (none skipped)
[ ] Every story has all 4 CBAR parts completed (Tension, Failure, Resolution, Proof)
[ ] Every story has a verdict (PASS / PASS WITH NOTE / REWRITE REQUIRED / FATAL CONFLICT)
[ ] The Constraint Resolution Manifest is present and numbered

SOURCE VERIFICATION
[ ] All mapped Primitive YAMLs were loaded and read (not assumed from memory)
[ ] The parent PRD module was loaded and read
[ ] The Tech Spec was loaded (or flagged as non-existent with UNVERIFIED ASSUMPTION notes)
[ ] The ERA3 Protocol was loaded for protocol-level gap analysis

ANTI-HALLUCINATION
[ ] Every resolution passed the Physics Check (§6)
[ ] No resolution assumes instant network responses without verification
[ ] No resolution assumes universal permission grants
[ ] No resolution ignores Stripe SCA or payment edge cases
[ ] No resolution assumes cache freshness without an invalidation strategy

CASCADE INTEGRITY
[ ] Every Downstream Proof (Part 4) was completed
[ ] No two resolutions in the Manifest contradict each other
[ ] If a FATAL CONFLICT was found, both affected stories have paired rewrites
```

---

## 9. Completion Receipt

After finishing a Phase audit, produce this receipt:

```
═══════════════════════════════════════════════════════
CBAR AUDIT COMPLETION RECEIPT
═══════════════════════════════════════════════════════
PHASE:                   Phase [N] — [Name]
EPIC COUNT:              [count]
STORY COUNT:             [count]
─────────────────────────────────────────────────────
VERDICTS:
  PASS:                  [count]
  PASS WITH NOTE:        [count]
  REWRITE REQUIRED:      [count]
  FATAL CONFLICT:        [count]
─────────────────────────────────────────────────────
PRIMITIVES AUDITED:      [list all IDs loaded]
PRD MODULES LOADED:      [list all modules loaded]
TECH SPECS LOADED:       [list all specs loaded, or "NONE — flagged"]
─────────────────────────────────────────────────────
UNVERIFIED ASSUMPTIONS:  [count] — [brief list]
CASCADE LOCK STATUS:     CLEAN / [N] CONFLICTS REMAIN
MANIFEST RULES:          [count] canonical mandates produced
─────────────────────────────────────────────────────
TIMESTAMP:               [ISO 8601]
═══════════════════════════════════════════════════════
```

---

## 10. Fatality Conditions

The audit is declared FATAL and must be restarted from scratch if:

- Any story was skipped without justification
- Any CBAR Part (1-4) is missing for any story
- The Constraint Resolution Manifest is absent
- More than 2 resolutions fail the Physics Check upon review
- The Cascade Lock reveals 3+ unresolved inter-story conflicts

---

## 11. Cognitive Toolbox Integration

> **This SKILL operates the CBAR Reasoning Engine as a cognitive tool.**
> The CBAR Engine is not a prompt instruction. It is a structured derivation sequence that forces the LLM out of its statistical centroid by demanding constraint satisfaction before generation.
>
> **Future DSPy Integration Note:**
> When this SKILL is migrated to a DSPy Declarative Pipeline, the 4-part CBAR sequence (§3) becomes a `dspy.Signature` with typed input/output fields. The Physics Check (§6) becomes a programmatic eval function. The Cascade Lock becomes a dependency graph validated by the DSPy `Module.forward()` method. Until that migration occurs, this SKILL operates as the human-readable specification that the DSPy pipeline will be compiled from.

---

**END OF CBAR EPIC & STORY HARDENING SKILL**
