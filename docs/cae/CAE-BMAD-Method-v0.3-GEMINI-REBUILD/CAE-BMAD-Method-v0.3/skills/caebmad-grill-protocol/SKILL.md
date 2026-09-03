---
name: caebmad-grill-protocol
description: Executes the interactive Grill-Me Protocol governed by the 4 Laws of Signal Distillation (RSCS), enforcing single-question discipline, codebase prechecks, collision primitives, and 320-word substantive recommendations.
version: 0.3.0-rebuild
agent: cae-method-orchestrator
---

# Skill: caebmad-grill-protocol

## 1. Purpose & Invocation
The `caebmad-grill-protocol` skill enables `cae-method-orchestrator`, `cae-adversarial-reviewer`, or any specialized analyst agent to interview the human operator relentlessly about architectural plans, resolving dependencies between decisions one-by-one without succumbing to the Genericity Trap or Density Decay.

## 2. Invocation Preconditions
1. An architectural fork, constitutional ambiguity, or unratified operator gate requires human judgment.
2. The codebase precheck has been performed and verified that repository/documentation inspection cannot resolve the question.
3. Schema `schemas/grill_session.schema.json` loaded.

## 3. Mandatory Execution Logic

### Step 1: Execute Codebase Precheck
Before prompting the operator, search the repository (`services/`, `packages/`, `schemas/`, `docs/`). If existing code or tests dictate the answer, adopt it, document it in `DECISION_LEDGER.md`, and **DO NOT interrupt the operator**.

### Step 2: Formulate Single Question
If operator judgment is genuinely required, articulate **EXACTLY ONE** focused question. Never ask compound, multi-part, or batched questions.

### Step 3: Author RSCS Substantive Recommendation
Construct the recommended answer complying strictly with the **4 Laws of Signal Distillation**:
- **Law 1 (Saturation):** Cite concrete paths (`packages/ca_runtime/`, `services/world-intelligence/`), classes, and research IDs (`SRC-xxx`).
- **Law 2 (Collision):** Declare which of the 3 Collision Primitives is active:
  - `PREDICTION_VIOLATION` (Surprise)
  - `COSTLY_EXPOSURE` (Credibility / Risk)
  - `LATENT_PATTERN_ARTICULATION` (Recognition)
- **Law 3 (Compression):** Ensure high epistemic density, irreducible concepts, and emergent insights.
- **Law 4 (Evaluation):** Run the 4-check anti-genericity evaluation. If it could fit a generic SaaS app, **REJECT AND REWRITE**.
- **Density Floor:** Enforce a strict minimum of **320 to 360 words** for the recommendation.

### Step 4: Record Decision
Once the operator responds, log the ratified outcome into:
- `docs/cae-bmad/00_governance/OPERATOR_GATE_DECISIONS.json` & `.md`
- `docs/cae-bmad/00_governance/DECISION_LEDGER.md`

## 4. Output Contract
- Formatted Grill Question modal or terminal prompt following `templates/grill_question.md`
- JSON record conforming to `schemas/grill_session.schema.json`
