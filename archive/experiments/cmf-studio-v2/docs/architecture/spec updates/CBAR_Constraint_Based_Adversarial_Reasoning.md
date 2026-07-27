# Constraint-Based Adversarial Reasoning (CBAR)
## A Formal Framework for LLM Self-Correction Through Structural Conflict Resolution

**Author:** CMF Architecture Team
**Date:** 2026-03-21
**Version:** 1.0
**Status:** Reference Document — Applicable to all CMF and CCP workflow pipelines

---

## Abstract

This paper formalizes Constraint-Based Adversarial Reasoning (CBAR), a prompt engineering methodology that replaces policy instructions with structured logical puzzles to force large language models into deterministic self-correction. The core insight is that LLMs fail at policy adherence because policies ask models to deviate from their statistical priors — a fundamentally unstable request under repeated invocation. CBAR eliminates this instability by reformulating quality enforcement as constraint satisfaction problems: the model cannot produce output without first resolving mutually exclusive architectural tensions. This paper derives CBAR from first principles, defines its formal anatomy, explains why it succeeds where policy fails, identifies its applicability boundaries, and provides integration patterns for production agentic systems.

---

## 1. The Policy Failure Theorem

Every LLM operates as a conditional probability estimator. Given a prompt *P*, the model produces the token sequence *T* that maximizes *P(T|P)*. A policy instruction — "do not produce generic output" — asks the model to suppress high-probability token sequences in favor of lower-probability alternatives. This works reliably for approximately 1-3 invocations before the model mean-reverts toward its training distribution.

**Mean-reversion is not a bug. It is the mathematical consequence of how autoregressive generation works.** Each successive token is sampled from a distribution conditioned on prior tokens. The further a generation deviates from the model's prior distribution, the stronger the statistical pull back toward the centroid. Policy instructions create a momentary offset; repeated invocation collapses that offset.

This produces a characteristic failure pattern we call the **Policy Decay Curve:**

- **Invocation 1-2:** Model successfully suppresses the target behavior. Output quality matches specification.
- **Invocation 3-5:** Model begins producing hybrid output — partially compliant, partially generic. The suppressed pattern "leaks" through paraphrased equivalents.
- **Invocation 6+:** Model fully mean-reverts. The policy instruction is still present in the prompt but has lost its statistical force against the model's prior. Output is indistinguishable from an unpolicied generation.

This curve has been observed empirically across the CCP architecture (33-point stress test), the CMF visual engine (E-Roll pipeline), and the CMF video automation pipeline (9-spec FR-VID batch). **Any system relying on policy instructions for quality enforcement will exhibit this decay at production scale.**

---

## 2. The Zebra Puzzle Insight

The Zebra Puzzle (also known as Einstein's Riddle) is a class of constraint satisfaction problem where the solution cannot be reached by inspecting any single clue in isolation. Success requires holding multiple mutually constraining facts in working memory simultaneously and deriving the unique configuration that satisfies all of them.

The canonical example: "The Norwegian lives next to the blue house. The blue house owner drinks water. The green house is immediately to the right of the ivory house. **What must be true about the green house owner?**" The answer cannot be "guessed" or "defaulted to" — it must be *derived* through logical elimination.

CBAR applies this exact mechanic to LLM generation. Instead of telling the model what not to produce (policy), we present the model with two or more statements it holds to be true, demonstrate that they cannot both be true simultaneously, and demand that it derive which takes precedence and why. **The model cannot produce output without performing the derivation.** There is no statistical prior to fall back on because the answer is unique to the specific input configuration.

This is why CBAR is stable under repeated invocation: each invocation presents a new, input-specific constraint configuration. The model's prior distribution is irrelevant because the answer is not a probability over token sequences — it is a logical entailment from concrete premises.

---

## 3. The CBAR Question Anatomy

Every CBAR question follows a 4-part structure. Omitting any part degrades the technique from adversarial reasoning to simple questioning.

### Part 1 — The Tension

Name two specific, concrete constraints that the model holds to be individually valid but that cannot both be satisfied simultaneously with the current input configuration.

**Formal requirement:** Both constraints must be traceable to named architectural rules, data schemas, or pipeline specifications. Abstract tensions ("quality vs. speed") are not CBAR tensions — they are management tradeoffs. A CBAR tension is concrete: "Rule X demands the character's shoulders be collapsed (Brand Avatar DNA). Rule Y demands the character's chest be expanding (PRIMAL BODY TRUTH for PROOF beat). Both reference the same character's posture in the same frame."

**Why this matters:** The specificity of the tension is what prevents mean-reversion. A vague tension ("make it more authentic") offers the model an infinite solution space, and infinite solution spaces collapse to the statistical centroid. A concrete tension offers exactly one resolution path per input configuration.

### Part 2 — The Failure Scenario

Describe the exact output the system will produce if the model proceeds without resolving the tension.

**Formal requirement:** The scenario must name the downstream module or consumer that will receive the incorrect output, and the specific failure mode that consumer will exhibit. "The output will be bad" is not a scenario. "The storyboard-composer will receive warm, intimate imagery for a beat whose emotional register is TENSION, producing a tonal mismatch that requires manual replacement" is a scenario.

**Why this matters:** Part 2 activates the model's consequence-sensitivity. LLMs display measurably different reasoning behavior when they are told what breaks downstream versus when they are merely told to "be careful." The named failure scenario converts the abstract obligation into a concrete avoidance target.

### Part 3 — The Resolution Demand

Force the model to state which constraint takes precedence, cite the rule that grants that precedence, and declare the specific action it will take.

**Formal requirement:** The question must not provide the answer. It must demand that the model *derive* the answer. "Which constraint takes priority? Name the rule, cite the source, and state what you will DO" is a resolution demand. "In this case, Constraint X takes priority because..." is not — it is pre-answering, which converts the question into a policy instruction (and re-engages mean-reversion).

**Why this matters:** Part 3 is the reasoning kernel. The model must perform constrained inference to produce its answer. The answer is deterministic for a given input configuration — there is exactly one correct resolution. This determinism is why CBAR scales: 1,000 invocations with 1,000 different input configurations will produce 1,000 different but individually correct resolutions, whereas a policy instruction would produce ~3 correct resolutions followed by 997 mean-reverted outputs.

### Part 4 — The Downstream Proof

Require the model to state how its resolution affects the next consumer in the pipeline.

**Formal requirement:** The model must name the downstream module by identifier, state what input that module expects, and confirm that the resolution produces the expected input or flag that it does not.

**Why this matters:** Part 4 converts isolated questions into a constraint *network*. Each resolution creates a postcondition that becomes a precondition for the next question. The model cannot answer Question 3 without having resolved Question 1 — because Question 3's input depends on Question 1's output. This inter-question dependency is the Zebra Puzzle mechanic: the model must hold the entire resolved state in working memory, preventing any individual resolution from being "forgotten" or mean-reverted by subsequent generation.

---

## 4. The Constraint Network: From Questions to Systems

Individual CBAR questions provide local self-correction. **Constraint Networks** provide systemic self-correction by organizing questions into dependency graphs where resolutions propagate.

A Constraint Network has three structural properties:

**4.1 — Cascade Dependency.** Questions are ordered such that later questions reference earlier answers. If Question A-1 reclassifies a finding from EVIDENCE to ILLUSTRATION, Question A-6 must account for the reduced evidence count. This is not merely "reviewing previous answers" — it is structural dependency. The model's answer to A-6 is literally different depending on A-1's resolution.

**4.2 — The Cascade Lock.** The final question in every gate block requires the model to review all prior resolutions for mutual consistency. This is the Zebra Puzzle's "final confirmation" step — the moment where all individual deductions must form a coherent global state. If any pair of resolutions contradicts another pair, the model must resolve the secondary conflict before proceeding. The Cascade Lock produces a **Constraint Resolution Manifest**: a structured JSON output listing every correction, every re-classification, and every downstream impact.

**4.3 — Cross-Gate Propagation.** In production pipelines, multiple gates operate at different pipeline positions. Gate A runs before research; Gate B runs before query submission; Gate C runs before prompt generation. The Constraint Resolution Manifest from Gate A becomes an input to Gate B. This creates a multi-stage reasoning chain where the model at Gate B cannot produce correct output unless it has absorbed Gate A's resolutions. The entire pipeline becomes a single extended constraint satisfaction problem.

---

## 5. Why CBAR Succeeds Where Policy Fails — The Formal Argument

CBAR's stability under repeated invocation derives from a fundamental asymmetry between policy instructions and constraint satisfaction:

| Property | Policy Instruction | CBAR Question |
|---|---|---|
| **Answer space** | Infinite (suppress bad, entire output space is valid) | Singular (exactly one correct resolution per input) |
| **Dependency on prior** | High (model must deviate from its training distribution) | Zero (answer derived from input constraints, not prior) |
| **Scaling behavior** | Mean-reverts after ~3-5 invocations | Stable indefinitely (each invocation has a unique input) |
| **Verifiability** | Subjective (was the output "authentic enough"?) | Objective (did the resolution correctly identify precedence?) |
| **Composability** | None (policies are independent instructions) | High (resolutions form dependency graphs) |

The critical insight is **answer space cardinality.** A policy instruction like "avoid generic output" leaves the model with an astronomically large valid answer space — *anything that isn't generic.* The model navigates this space using its prior, which mean-reverts to the centroid. A CBAR question reduces the answer space to exactly one valid resolution for the given input, making the prior irrelevant.

---

## 6. Applicability Boundaries

CBAR is not universally applicable. It requires specific conditions to function:

**6.1 — Named, Traceable Rules.** Every tension must reference concrete, named architectural rules or data schemas. If the pipeline lacks formal specifications with named constraints, CBAR questions cannot be constructed. Systems with informal or implicit quality standards cannot use CBAR until those standards are formalized.

**6.2 — Deterministic Inputs.** The input configuration must be concrete enough that exactly one resolution exists. Ambiguous inputs — where reasonable people could disagree on which constraint takes priority — produce non-deterministic CBAR answers and reintroduce the policy failure mode. When ambiguity exists, the correct response is to formalize the precedence hierarchy before deploying the CBAR question.

**6.3 — Pipeline Topology.** CBAR Constraint Networks require a directed pipeline with identifiable stages and consumers. Architectures where modules interact bidirectionally or non-deterministically (general agent swarms without structured handoffs) cannot leverage the cascade dependency mechanic.

**6.4 — Gate Placement Discipline.** CBAR gates must be placed BEFORE the generation step they govern, not after. A post-generation CBAR question becomes a validation check — useful but fundamentally different. The power of CBAR is *pre-generation reasoning*: forcing the model to resolve tensions before spending tokens on generation, not after.

---

## 7. Integration Patterns for Production Workflows

### Pattern 1: Spec-Level Integration (Build Phase)

Each technical specification includes a Skill Definition section containing a named Constraint Gate with 4-8 CBAR questions. The gate runs before the skill's primary generation step. This pattern is deployed across the CCP architecture (Gates PC-01 through PC-08), the CMF E-Roll pipeline (Gates A-C), and the CMF video pipeline (Gates D-L).

### Pattern 2: Audit-Level Integration (Review Phase)

The Spec Audit prompt (5-lens review) uses CBAR principles in Lens 4 (Gate & Constraint Completeness) to verify that every gate question is implementable as an executable validation function. Questions that cannot be answered programmatically are flagged for revision.

### Pattern 3: Stress Test Integration (Architecture Phase)

The architecture stress test applies CBAR at the system level, posing N questions that span the entire pipeline. Each question names a cross-module tension that can only be resolved by understanding two or more specifications simultaneously. The resolved stress test produces an Architectural Decision Log — the canonical reference for all downstream gates.

### Pattern 4: Build Prompt Integration (Execution Phase)

The build prompt enforces CBAR at implementation time by requiring that Constraint Gate questions are implemented as executable functions, not documentation. Every gate question must have a corresponding validation function that returns True/False with a diagnostic message. This closes the loop from specification to implementation.

---

## 8. Conclusion

Constraint-Based Adversarial Reasoning reframes LLM quality enforcement from "tell the model what not to do" (policy) to "present the model with irreconcilable tensions and demand it derive the resolution" (constraint satisfaction). This reframing eliminates mean-reversion because the answer space collapses from infinite to singular for each input configuration. The technique composes through Constraint Networks — ordered question sequences where later answers depend on earlier resolutions — creating a systemic reasoning layer that forces the model to hold its entire decision state in working memory before producing output.

CBAR is not a prompt hack. It is a structural methodology for constructing self-correcting agentic systems. Its deployment requires formal specifications, deterministic inputs, directed pipelines, and disciplined gate placement. When these conditions are met, CBAR provides stable, scalable, verifiable quality enforcement that does not degrade under repeated invocation — the exact failure mode that policy instructions inevitably exhibit at production scale.

---

*This document is a living reference. As CBAR is applied to new pipeline domains, new applicability boundaries and integration patterns will be appended.*
