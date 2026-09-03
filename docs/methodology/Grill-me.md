Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. 

For each question, provide your **recommended answer**.

### The Grill-Me Protocol
1. Ask the questions ONE AT A TIME. Never batch multiple questions.
2. If a question can be answered by exploring the codebase, explore the codebase INSTEAD of asking the user.
3. Your recommended answer MUST be substantive (320-360 words minimum).

### The 4 Laws of Signal Distillation
All recommended answers MUST strictly follow the 4 Laws of Signal Distillation (from `docs/methodology/RSCS_Recursive_Signal_Compression_Systems.md`):

*   **Law 1 — Saturation Before Compression:** Ground every recommendation in first-party project data (codebase, briefs, specs, registries). Never recommend from vacuum. The ceiling of output density equals the ceiling of input density.
*   **Law 2 — Meaning Emerges Through Collision:** Surface structural collisions — contradictions, tensions, asymmetries, shadows, anomalies, and unarticulated regularities — within the project context. Every recommendation must identify at least one collision between existing constraints. The 3 Collision Primitives (T/V/R): Prediction Violation (surprise), Costly Exposure (credibility), Latent Pattern Articulation (recognition).
*   **Law 3 — Compression Increases Signal Density:** Merge signals across collision types into dense, irreducible representations. A recommended answer must exhibit: Irreducibility (cannot be decomposed without losing meaning), Emergence (contains insight not present in any single source), and Specificity (grounded in concrete project data, not abstract generalization).
*   **Law 4 — Evaluation Governs Reality Contact:** Every recommendation must survive the 4-check anti-genericity gate:
    *   *CHECK 1:* Could a generic system produce this without the project context? YES = REJECT.
    *   *CHECK 2:* Could a different project produce the same recommendation? YES = REJECT.
    *   *CHECK 3:* Does the recommendation require first-order project data to verify? NO = REJECT.
    *   *CHECK 4:* Does the recommendation encode a collision the user will recognize but has never articulated? NO = flag for density improvement.

**FAILURE MODE:** A recommended answer under 320 words or one that could be copy-pasted into a different project without modification is a DENSITY DECAY failure and MUST be regenerated.
