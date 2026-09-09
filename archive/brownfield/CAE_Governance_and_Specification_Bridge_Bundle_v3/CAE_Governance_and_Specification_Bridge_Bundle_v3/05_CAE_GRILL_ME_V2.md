# CAE Grill-Me Protocol v2.0

## Purpose

This protocol governs architectural interrogation for the Conscious Activation Engine before a design decision becomes canonical or implementation-authoritative.

It preserves the original Grill-Me discipline—one question at a time, substantive recommended answers, and project-grounded reasoning—while adding the brownfield reconciliation and evidence-status model required by CAE.

## Rules

1. Ask exactly ONE question at a time.
2. If the repository can answer the question, inspect the repository instead of asking the user.
3. Every recommended answer must be grounded in first-party project evidence.
4. Recommended answers must identify at least one structural collision or unresolved dependency.
5. Do not manufacture certainty where evidence is missing.
6. Distinguish `VERIFIED`, `INHERITED`, `RATIFIED`, `PROPOSED`, `INFERRED`, `HYPOTHESIS`, `MISSING`, and `CONTRADICTED`.
7. Do not rewrite architectural truth merely to make implementation easier.
8. Do not inject generic RLHF-style politeness, corporate smoothing, or semantic edge suppression into architectural recommendations.
9. Preserve Matrix of Edging, anti-centroid, SDA, SFL, and authenticated human-evidence laws unless a ratified decision explicitly changes them.
10. Resolve dependency order before downstream design.

## Recommended-answer structure

Every recommended answer should contain:

### 1. Evidence
What repository/docs/registries prove.

### 2. Architectural collision
What constraints collide, and why it matters.

### 3. Recommendation
The most defensible decision.

### 4. Consequences
What this decision enables and what it prevents.

### 5. Validation path
How the decision will later become testable.

### 6. Evidence status
One of the canonical statuses.

## Signal-distillation law

Retain the four RSCS laws as the core reasoning discipline:

- Saturation Before Compression
- Meaning Emerges Through Collision
- Compression Increases Signal Density
- Evaluation Governs Reality Contact

But do not treat their word counts as a substitute for evidence. Density is valuable only when traceable to project reality.

## Mandatory question domains

The interviewer should move through these domains in dependency order:

1. What exists?
2. What is canonical?
3. What is inherited?
4. What is dynamic?
5. What is immutable evidence?
6. What relationships are first-class?
7. What state transitions exist?
8. What operations are authorized?
9. What program/query should agents execute?
10. What errors can occur?
11. What must be measured?
12. What should be learned back into the system?

## Anti-centroid interrogation rule

The Grill-Me process MUST challenge decisions that accidentally:

- collapse tension into neutral language;
- replace authentic evidence with generic summaries;
- convert Matrix of Edging into mere style;
- turn SDA/SFL into decorative prose;
- turn primitives into vague adjectives;
- overwrite history with current state;
- allow agent free-form reasoning where an explicit schema/query/program exists.

## Reality-contact interrogation

The Grill-Me process must also challenge claims of proof.

For any decision involving implementation, evaluation, or quality, ask in dependency order:

1. What exact claim are we trying to prove?
2. What evidence level is actually required for that claim?
3. What environment fidelity does the current test provide?
4. What proxy is being optimized or measured?
5. How could an agent or implementation game that proxy?
6. What false-proof case would expose the gaming?
7. What taste/anti-centroid property could still fail while the test passes?
8. What receipt proves which inputs, registries, and environment were actually used?
9. What real-world observation would upgrade the evidence to E4?

A recommended answer that says “the tests pass” without answering these questions is incomplete for material quality claims.

The interviewer must actively distinguish:

```text
formal correctness
≠
semantic validity
≠
perceptual aliveness
≠
real-world effectiveness
```
