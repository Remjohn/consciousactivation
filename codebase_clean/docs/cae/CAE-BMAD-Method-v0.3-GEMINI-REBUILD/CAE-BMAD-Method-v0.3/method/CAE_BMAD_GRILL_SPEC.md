# CAE-BMAD Grill-Me Protocol & Signal Distillation Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Method Governance  
**Lineage:** RSCS (Recursive Signal Compression Systems), `docs/methodology/Grill-me.md`, `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md`

---

## 1. Purpose & Epistemic Mental Model

The **CAE-BMAD Grill-Me Protocol** is an interactive, relentless alignment and decision crucible. Its purpose is not merely to ask preferences, but to **walk down each branch of the architectural design tree, resolving dependencies between decisions one-by-one**.

To eliminate the **Genericity Trap** and **Density Decay Curve** inherent to large language models, all grilling in CAE-BMAD is strictly governed by the **4 Laws of Signal Distillation**.

---

## 2. The 3 Invariant Operational Rules

1. **Strict Single-Question Discipline:**
   - Ask questions **ONE AT A TIME**. Never batch multiple questions into a survey or compound questionnaire.
2. **Codebase-First Precheck (Zero-Waste Questioning):**
   - If a question can be answered by exploring repository code, schemas, tests, or documentation, the agent **MUST explore the codebase INSTEAD of asking the operator**.
   - Questions directed to the operator are reserved strictly for constitutional, architectural, or irreversible trade-offs.
3. **Substantive Recommendation Floor (Density Rule):**
   - For every question asked, the agent **MUST provide a recommended answer**.
   - The recommended answer **MUST be substantive: 320–360 words minimum**.
   - Any recommendation under 320 words or capable of being copy-pasted into an unrelated project is classified as an unhandled **`DENSITY_DECAY` failure** and must be rejected.

---

## 3. The 4 Laws of Signal Distillation (RSCS Engine)

All recommended answers generated during a Grill session must comply with the 4 Laws derived from Recursive Signal Compression Systems:

### Law 1 — Saturation Before Compression
- **Axiom:** *A system cannot distill signal it has not sufficiently absorbed.*
- Every recommendation must be grounded in first-party project data (codebase lines, service boundaries, database entities, research library sources, constitutions).
- Never recommend from an abstract vacuum. The ceiling of output density equals the ceiling of input density.

### Law 2 — Meaning Emerges Through Collision
- **Axiom:** *Signal emerges where incompatible representations interact.*
- Pure facts in isolation are low-signal. Meaning is generated at boundaries of contradiction, tension, and trade-off.
- Every recommendation **MUST explicitly identify at least one structural collision** between constraints using one of the **3 Collision Primitives ($T/V/R$)**:
  1. **Prediction Violation ($V$ - Surprise):** Surfaces an unexamined assumption that is violated by empirical codebase or research reality.
  2. **Costly Exposure ($T$ - Credibility):** Identifies the genuine technical, architectural, or operational cost/risk of a path.
  3. **Latent Pattern Articulation ($R$ - Recognition):** Articulates a latent structural regularity already present in the codebase that has not yet been formalized.

### Law 3 — Compression Increases Signal Density
- **Axiom:** *Value $\propto$ Irreducible Signal Density Under Constraint.*
- Merge signals across collision types into dense, irreducible representations.
- A valid recommendation must exhibit:
  - **Irreducibility:** Cannot be decomposed or simplified without losing vital meaning.
  - **Emergence:** Contains insight not present in any single isolated file or source.
  - **Specificity:** Grounded in concrete project files, types, and numbers, not generic analogies.

### Law 4 — Evaluation Governs Reality Contact (The 4 Anti-Genericity Gates)
Every recommended answer must survive the 4-check anti-genericity gate before presentation:
- **CHECK 1:** *Could a generic LLM produce this recommendation without the specific project context?* $\implies$ **YES = REJECT.**
- **CHECK 2:** *Could a different project or generic SaaS produce the exact same recommendation?* $\implies$ **YES = REJECT.**
- **CHECK 3:** *Does the recommendation require first-order project code/data to verify?* $\implies$ **NO = REJECT.**
- **CHECK 4:** *Does the recommendation encode a collision the operator will recognize but has never articulated?* $\implies$ **NO = Flag for density improvement.**

---

## 4. Decision Lifecycle & Handshake

```text
[ Trigger: Architectural Fork / Gate Decision ]
                 ↓
[ Codebase Precheck: Can code/tests answer this? ]
     ├─ YES ──→ Resolve autonomously via AST forensics & log
     └─ NO  ──→ Proceed to Grill Question
                 ↓
[ Formulate Question (Exactly 1) ]
                 ↓
[ Synthesize RSCS Recommendation (Min 320 Words, 4 Laws, T/V/R Collision) ]
                 ↓
[ 4-Check Anti-Genericity Gate ]
     ├─ FAIL ──→ Regenerate (Density Decay Rejection)
     └─ PASS ──→ Present to Operator in Grill Modal / Prompt
                 ↓
[ Operator Response: Ratify / Modify / Reject ]
                 ↓
[ Formal Log in docs/cae-bmad/00_governance/OPERATOR_GATE_DECISIONS.json ]
```
