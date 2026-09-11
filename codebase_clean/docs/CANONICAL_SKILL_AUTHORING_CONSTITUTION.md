# Canonical Skill Authoring & Authority Lane Governance Constitution

**Version:** 1.0.0  
**Status:** CONSTITUTIONAL_DRAFT_FOR_HUMAN_RATIFICATION  
**Governing PRD Features:** F06 (FR-031–FR-036), F09 (Canonical Skill Ecology), F15 (FR-085–FR-090)  
**Constitutional Authority:** Activative Intelligence Constitution V1.1, Builder PRD V1.2  
**Scope:** All Canonical Skills across Content Semantic Intelligence and Visual Asset Editor domains  

---

## 1. Constitutional Preamble

This document establishes the governing principles, structural requirements, and authoring protocols for every Canonical Skill within the Conscious Activations system. It serves three purposes: it defines **why** the four Authority Lanes exist as epistemic necessities rather than organizational conveniences; it specifies **how** Skills must be authored, packaged, adapted, and composed within those lanes; and it declares **what** constitutional laws protect the system from the specific failure modes that arise when cognitive responsibilities are collapsed, duplicated, or left ungoverned.

A Canonical Skill is a stable, versioned, independently routable capability specification. It is not an agent. It does not route itself, own a planning loop, or autonomously decide which other Skill to invoke. An agent, harness controller, or workflow orchestrator observes the current program state, selects the needed Skills, loads them, executes them, validates their receipts, and decides what happens next. The Skill itself is a passive transformation: given governed inputs, produce a contract-valid output.

This separation is not an implementation detail. It is a constitutional law. Collapsing a Skill into an autonomous agent destroys the receipt chain, removes adversarial evaluation, and eliminates the authority boundaries that protect source truth from locally attractive but globally invalid compositions.

---

## 2. First-Principles Foundations

### 2.1 The Epistemic Separation of Powers

The architecture of four Authority Lanes—Hunter, Analyst, Composer, Commander—is not borrowed from organizational metaphor. It is derived from the epistemic observation that **search, evaluation, synthesis, and authorization are fundamentally different cognitive operations** that produce systematically worse outcomes when performed by the same reasoning process in a single pass.

When a single model prompt is asked to find source material, judge its quality, compose a narrative arc, and approve its own composition, four well-documented failure modes emerge:

**Selection bias.** Once the model identifies an emotionally resonant candidate quote, it becomes progressively more likely to justify that quote rather than challenge it. The search function contaminates the evaluation function because the same context window holds both the discovery excitement and the critical judgment. Research in cognitive science identifies this as the **anchoring effect**: early candidates disproportionately influence subsequent reasoning even when later evidence contradicts them.

**Source-recall suppression.** A Composer optimizes for coherence. A Hunter optimizes for discovery. Asking one process to do both encourages the Composer to search only for material that supports the first plausible arc, suppressing recall of contradictory, complementary, or superior alternatives. This is a direct application of **satisficing theory**: systems under cognitive load stop searching once a "good enough" candidate appears, even when the search space contains decisively better material.

**Adversarial-evaluation collapse.** An Analyst must be able to declare that an emotionally powerful quote is wrong for this format, insufficiently evidenced, redundant, overexposed, or narratively premature. When the same process that discovered the quote also evaluates it, the evaluation degrades into self-confirmation. This mirrors the well-established principle in formal verification that **a system cannot be its own oracle**.

**Authorization-boundary dissolution.** The Commander exists to protect the harness from locally attractive but globally invalid compositions. A narrative arc that is emotionally compelling for one beat may violate archetype invariants, source-fidelity requirements, wrong-reading locks, or closure contracts. Without an independent authorization authority, the system conflates "this feels right" with "this is permitted." In control theory, this is the distinction between the **plant** (which produces output) and the **controller** (which enforces constraints on that output).

These four failure modes are not speculative. They are the predictable consequences of violating the **separation of concerns** principle applied to cognitive operations rather than software modules. The lanes exist because the failure modes exist.

### 2.2 Source Sovereignty and Semantic Authorship

The CMF system operates under a non-negotiable doctrine: the speaker is the semantic sovereign. For interview-led content, eighty to one hundred percent of the semantic payload must originate in authenticated speaker expression. CRAL (Conscious Research Alchemy Lab)—governed by the Sovereign CRAL Research Engine (SCRE V1.0)—operates via its 7 Moment Executors ($M_1$–$M_7$), 41 Trigger Category Research Analysts, infrastructure-level SearXNG category routing (`cultural_now`, `institutional_prosecution`, etc.), and Epistemic Friction Swarm conflict resolution. CRAL intelligence may validate, contextualize, sharpen prediction gaps, find external proof, and strengthen audience recognition. It must never fabricate the speaker's lived experience, mechanism, emotional turn, result, or conclusion.

This principle constrains every Skill in every lane. A Hunter Skill cannot invent source material. An Analyst Skill cannot substitute model-generated evidence for speaker-expressed evidence. A Composer Skill cannot fabricate narrative coherence that the source does not support. A Commander Skill cannot authorize a composition that claims meaning the speaker never expressed.

Source sovereignty is not a preference. It is the architectural invariant that distinguishes this system from generic content generation. Every Skill's input contract, output contract, and evaluation rubric must be traceable to this principle.

### 2.3 Invariant Composition and the Archetype–Harness Covenant

The system recognizes two independent constitutional authorities:

**Archetype truth.** The archetype declares: "For this narrative to remain this narrative, these structural relations must survive." An Achievement Story requires Stakes → Mechanism → Turn → Result → Implication in that causal order, with a single transferable mechanism and a falsifiable result. These are structural invariants that no harness may violate.

**Harness truth.** The harness declares: "For this content product to remain this content product, meaning must be expressed through these exact perceptual, temporal, spatial, and operational affordances." A Cinematic Story supports temporal breathing, lived scenes, A-roll continuity, and sonic restraint. A Minimal Coach Object Lesson supports one concept, one meaning object, and compressed explanation.

Neither authority may override the other. Instead, a governed **Archetype–Harness Realization Covenant** determines whether the two constitutions can coexist without semantic loss. The covenant produces an explicit compatibility status—NATIVE, SUPPORTED, CONDITIONAL, LOSSY, or UNSUPPORTED—evaluated across invariant preservation, temporal capacity, sequence affordance, semantic-visual fidelity, source density, proof capacity, emotional bandwidth, closure fidelity, CRAL dependence, and adaptation loss.

Every Skill operates within the boundaries established by the active covenant. A Hunter Skill for Format 01 Cinematic Story seeks lived scenes and memory objects. A Hunter Skill for Format 03 Proof Commentary seeks claims, proof regions, and contradictions. The same archetype (Achievement Story) generates fundamentally different hunting strategies depending on which harness must realize it. This is why Skills require harness-specific adapters rather than universal implementations.

---

## 3. The Four Authority Lanes

### 3.1 The Hunter Lane — High-Recall Signal Extraction

The Hunter lane maximizes useful recall from authenticated source material. Its cognitive function corresponds to **divergent retrieval**: casting the widest defensible net over the available evidence to surface candidates that might serve the current content program.

A Hunter Skill does not judge narrative coherence, evaluate archetype fit, or compose temporal sequences. It finds material and classifies it. Its output is a typed `HunterCandidateManifest` containing source candidates, narrative cluster candidates, beat candidates, proof candidates, visual affordance candidates, rejected candidates with rejection reasons, and missing evidence declarations.

The Hunter lane may activate multiple flat, independently routable Skills during a single pass. A typical execution might include a deterministic Source Segmenter, a Content-Archetype Signal Hunter, a Harness Affordance Hunter, a conditional Proof/Evidence Hunter, and a conditional Source Provenance Hunter. These Skills compose flatly—the orchestrator invokes each one independently and collects their typed outputs. No Hunter Skill invokes another Hunter Skill.

Implementation may use the minimum sufficient intelligence. Deterministic transcript slicing, embedding-based search, local classifiers, and targeted DSPy extraction handle structured retrieval. Semantic model calls are reserved for ambiguous classifications—determining whether a specific utterance functions as a memory object, an aftermath evidence, an identity transition, or a closure callback.

The Hunter lane's constitutional obligation is **recall without premature judgment**. It must surface candidates that the Analyst may later reject. Suppressing a candidate because it seems unlikely to survive analysis is a constitutional violation—it removes the Analyst's authority to make that determination.

### 3.2 The Analyst Lane — Adversarial Criticism and Rubric Evaluation

The Analyst lane separates signal from attractive noise. Its cognitive function corresponds to **convergent evaluation**: systematically testing each candidate against source fidelity, archetype coverage, harness fit, primitive compatibility, redundancy, and wrong-reading risk.

An Analyst Skill does not discover new material, compose narrative arcs, or authorize final programs. It enriches candidates with scored evaluations and produces a `ClusterAnalysisManifest` containing enrichment records, evaluation receipts, collision reports, and gap analyses.

The Analyst lane's distinctive contribution is **adversarial independence**. It must be able to declare that an emotionally powerful source span is wrong for this format, insufficiently evidenced to carry the claimed meaning, redundant with a higher-fidelity candidate, or likely to produce a wrong reading in the target audience. This adversarial capacity is destroyed when analysis is performed by the same reasoning context that discovered the candidate.

Possible activated Skills include: Narrative Cluster Enricher, Archetype Phase Coverage Analyst, Source Fidelity Analyst, Harness Fit Analyst, Primitive Fit Analyst, Redundancy Analyst, and Wrong-Reading Analyst. Each produces independently auditable evaluation receipts.

The Analyst lane's constitutional obligation is **honest evaluation without composition pressure**. It must score candidates based on evidence, not on how well they would serve a narrative the Composer has not yet proposed.

### 3.3 The Composer Lane — Synthesizing Coherent Programs

The Composer lane creates emergent narrative coherence from analyzed material. Its cognitive function corresponds to **creative synthesis**: organizing enriched, scored candidates into one or more candidate narrative programs, beat cluster programs, content arcs, viewer-state sequences, and sequence strategy plans.

A Composer Skill does not search for new material, re-evaluate source fidelity, or authorize its own output. It proposes candidate programs and submits them downstream for authorization.

The Composer lane is where archetype invariants become temporal structure. An Achievement Story Composer arranges material into Stakes → Mechanism → Turn → Result → Implication. A Proof Commentary Composer creates an evidence-inspection arc. A Blind Ranking Composer creates prediction and reveal logic. Each harness dialect further constrains how the archetype's structural DNA is realized in the production language.

Possible activated Skills include: Narrative Cluster Composer, Beat Cluster Composer, Content Arc Composer, Viewer-State Sequence Composer, and Sequence Strategy Composer. The Composer lane may produce multiple candidate programs ranked by different optimization criteria (source coverage, emotional density, archetype fidelity, production feasibility).

The Composer lane's constitutional obligation is **coherence from evidence, not invention**. Every element of the composed program must trace to an analyzed, scored source candidate. The Composer may arrange, compress, and sequence, but it may not fabricate meaning that the source does not contain.

### 3.4 The Commander Lane — Executive Authority and Gatekeeping

The Commander lane authorizes, rejects, or reroutes candidate programs. Its cognitive function corresponds to **executive control**: testing proposed compositions against the full constitutional stack—source fidelity, archetype invariants, harness constitution, primitive coalition integrity, wrong-reading locks, closure contracts, and production eligibility.

A Commander Skill does not search, analyze, or compose. It renders verdicts.

The Commander may return one of seven typed dispositions:

- **AUTHORIZE** — The candidate program satisfies all constitutional requirements.
- **REJECT** — The candidate program has a fatal constitutional violation.
- **RETURN_TO_HUNTER** — Insufficient source material; the Hunter lane must search again.
- **RETURN_TO_ANALYST** — Analysis is incomplete or contradictory; the Analyst must re-evaluate.
- **RETURN_TO_COMPOSER** — The composition has structural problems but the material is adequate.
- **REQUEST_MORE_SOURCE** — The available source evidence cannot support this content program.
- **ESCALATE_TO_HUMAN** — The decision exceeds automated authority (high blast radius, structural ambiguity, or human policy escalation).

This recursive routing was one of the strongest architectural ideas in the original Format 01 POC and must survive in all future implementations. The Commander does not merely choose the highest-scoring arc. It protects the entire constitutional hierarchy.

The Commander lane's constitutional obligation is **protection without creation**. It must never improve a composition by silently rewriting it. If a composition requires changes, it returns it to the appropriate upstream lane with explicit instructions.

---

## 4. Dual-Domain Specialization

### 4.1 Content Semantic Intelligence Workcell

The Content Semantic Intelligence Workcell operates on textual and narrative material: interview transcripts, expression moments, narrative arc structures, beat clusters, and viewer-state sequences. Its four lanes (Hunter, Analyst, Composer, Commander) process **meaning** derived from authenticated speaker expression.

Every content harness owns a local instance of this workcell. The workcell's lane Skills are selected JIT based on the active content program's archetype, harness dialect, and primitive coalition. A Format 01 Cinematic Story workcell activates different Hunter Skills than a Format 04 Blind Ranking workcell, even when processing the same source transcript. This is because each harness has a different ontology of what counts as valuable material.

The workcell produces an **Authorized Narrative Program** containing the locked content arc, beat cluster program, viewer-state sequence, and sequence strategy plan. This program is the semantic handoff to the visual production layer. No visual composition may begin until this program is authorized.

### 4.2 Visual Asset Editor (VAE) Production Workcell

The Visual Asset Editor operates on visual material: real-life image references, asset vault items, subject masks, safe zones, spatial composition geometry, and production-ready deliverables. Its authority lanes process **visual realization** of meaning that has already been authorized upstream.

The VAE workcell inherits the same four-lane architecture but with domain-specific responsibilities:

- **Asset Research Hunter** — Finds existing vault assets, real-world photographic references, proof surface images, documentary environments, and identity references. Searches are compiled from the semantic obligation, visual recognition target, contextual clues, and cultural symbols declared in the upstream `VisualAssetDemandContract`. The Hunter does not invent search terms from shallow object labels.

- **Asset Lineage Analyst** — Validates source lineage and asset classification to maintain clean lineage records across production executions.

- **Activative Visual Analyst** — Tests semantic fit (does this image carry the authorized meaning?), composition feasibility (can it support the required crop, BBOX intent, text safe zones, gaze routing, negative space?), identity fidelity, and human believability. Real-world imperfection, documentary texture, and culturally specific details are quality dimensions, not defects.

- **Asset Strategy Composer** — Chooses the production route: REUSE_APPROVED, DIRECT_LICENSED_USE, CROP_AND_GRADE, CUTOUT_AND_MASK, EDIT_REAL_ASSET, COMPOSITE_REAL_ASSETS, GENERATE_GROUNDED_DERIVATIVE, CREATE_DETERMINISTIC_VECTOR, or RETURN_UNRESOLVED. The priority hierarchy places existing approved assets first and generation last. Generation always inherits structure from real-life references; it never invents the visual world from nothing.

- **Asset Commander** — Authorizes, rejects, or requests contract amendments. The Asset Commander cannot change the narrative arc, archetype invariants, beat order, viewer-state sequence, semantic obligation, sequence operator, composition role, BBOX purpose, source claim, intended identity, or final meaning. When a requirement is infeasible, it returns a typed contract amendment request to the Content Harness Commander. It does not silently solve infeasibility by changing the meaning.

### 4.3 The Delegation Bridge

The Content Harness and the VAE are separate atomic systems connected by a receipt-driven delegation protocol, not by shared code imports or direct agent calls.

The Content Harness emits an `ActivativeVisualAssetProgram` containing every asset obligation for the authorized composition—one `VisualAssetDemandContract` per required asset or asset family. Each demand contract specifies why the asset exists, which narrative beat it serves, what meaning it carries, where it will be placed, what the viewer must notice, which source material authorizes it, which visual references are acceptable, and which representations are forbidden.

The VAE resolves the program and returns a `ResolvedActivativeVisualAssetProgram` containing reference evidence packs, production asset packs, geometry analysis packs, lineage receipts, evaluation receipts, and any contract amendment requests. The Content Harness then performs image-conditioned spatial composition using the actual subject masks, safe zones, and gaze vectors from the resolved assets—geometry that could not have been known before the real image existed.

---

## 5. Canonical Skill Package Structure and JIT Assembly

### 5.1 The Portable Skill Package

Every Canonical Skill is packaged as a self-contained, versioned directory:

```
skill-packages/<skill_name>/<version>/
    SKILL.md              — Procedure, completion criteria, authority boundaries
    manifest.json         — Metadata: authority_lane, maturity, dependencies, cost
    contracts/
        input.schema.json   — Required input contract (JSON Schema)
        output.schema.json  — Required output contract (JSON Schema)
    eval/
        rubric.json         — Evaluation rubric and scoring criteria
        golden_samples/     — Reference inputs/outputs for regression testing
    adapters/
        archetype/          — Archetype-specific ecological adaptations
        harness/            — Harness-specific dialect adaptations
```

The `SKILL.md` file contains the procedure that an agent or model executes. It declares: what the Skill does, what inputs it requires, what outputs it produces, what invariants it must preserve, what it is forbidden from doing, and how it handles missing or degraded inputs. It is written in natural language because its consumer is a language model, but its contracts are machine-validated JSON schemas.

The `manifest.json` declares the Skill's identity, authority lane assignment, maturity status (DRAFT, TESTED, STABLE), dependency graph, estimated token cost, model-call policy, and certification state. A Skill at DRAFT maturity may be used in YOLO Draft and Skill Lab contexts. Only TESTED or STABLE Skills may enter production execution.

### 5.2 Flat Composition and Anti-Nesting Laws

Skills compose flatly. The orchestrator invokes Skills independently and collects their typed outputs. No Skill invokes another Skill. This is not merely a style preference—it is derived from empirical evidence that hierarchical Skill nesting produces cascading errors, more difficult debugging, and measurably lower task success rates compared with flat composition.

The correct topology is:

```
Harness Workcell Orchestrator
    ├── invokes Quote Authenticator Skill
    ├── invokes Achievement Story Hunter Skill
    ├── invokes Harness Affordance Hunter Skill
    └── collects all typed outputs
```

The orchestration logic is hierarchical. The Skills remain flat. This distinction is constitutional.

### 5.3 JIT Capsule Assembly

At runtime, the JIT assembler creates a `PhaseLocalJITCapsule` for each workflow node by binding:

- The selected Canonical Skill (identified by `skill_id` and `skill_version`)
- The skill package hash (integrity verification)
- The required context requirements (classified as REQUIRED, CONDITIONAL_REQUIRED, OPTIONAL, FORBIDDEN, or NOT_APPLICABLE)
- The input and output contract references
- The acceptance test references
- The wrong-reading locks inherited from the harness constitution
- The semantic lineage references tracing back to source evidence
- The evaluation status and production eligibility flags

The capsule is assembled from governed inputs. It cannot be assembled when required context is missing, when the skill package hash does not match, when forbidden context is present, or when the evaluation status prohibits production execution. These are hard integrity gates, not soft preferences.

### 5.4 Ecological Adaptation Without Mutation

A Canonical Skill carries universal cognitive DNA—the core reasoning pattern that remains stable across all contexts. An Achievement Story Hunter always seeks stakes, mechanisms, turns, results, and implications. A Source Fidelity Analyst always verifies that claimed meaning traces to authenticated speaker expression.

But the same cognitive DNA must be **ecologically adapted** to each archetype and harness without mutating the canonical procedure. This adaptation is achieved through external adapter files, not through forking the Skill:

- **Archetype Adapter** — Tells the Skill what matters for the selected archetype. An Achievement Story Hunter adapter specifies the five-phase arc structure, CRAL intelligence mappings, and structural invariants.
- **Harness Adapter** — Tells the Skill what material the harness can actually express. A Format 01 adapter specifies lived scenes, memory objects, aftermath evidence, and A-roll continuity. A Format 02 adapter specifies one teachable mechanism, one meaning object, and sparse explanation.
- **Primitive Appreciation Adapter** — Tells the Skill how primitives manifest and fail inside this specific harness. Active Prediction in Format 04 operates through rank withholding and commitment mechanics. Active Prediction in Format 01 operates through emotional inference and aftermath evidence. Same primitive, different realization.
- **Evaluation Adapter** — Maps the Skill's output into harness-specific CBAR (Constraint-Based Adversarial Review), MCDA (Multi-Criteria Decision Analysis), source fidelity, sequence integrity, visual coherence, and runtime evaluation gates.

The canonical `SKILL.md` procedure remains immutable across all adaptations. Adapters are versioned, governed, and separately testable. This satisfies FR-032: "A Harness may reference a governed local adaptation without mutating the Canonical Skill."

---

## 6. Cognitive Architecture Validation

### 6.1 OODA Loop Correspondence

The four authority lanes map precisely to Colonel John Boyd's **OODA loop** (Observe–Orient–Decide–Act), the foundational model for adversarial decision-making under uncertainty:

- **Hunter → Observe.** Scan the environment (source material) for signals. Maximize the observation aperture without premature filtering.
- **Analyst → Orient.** Contextualize observations against mental models (archetype schemas, harness affordances, primitive rubrics). Identify what each signal means relative to the current program.
- **Commander → Decide.** Select the authorized course of action from the oriented possibilities. Apply constitutional constraints. Determine whether to proceed, retreat, or escalate.
- **Composer → Act.** Produce the coherent output program that realizes the authorized decision in the production language.

Boyd's critical insight was that the **Orient** phase is the most important and the most vulnerable to corruption. When orientation is collapsed into observation (Hunter doing Analyst work) or into action (Composer doing Commander work), the loop degenerates into reflexive pattern-matching rather than deliberate reasoning. The four-lane architecture preserves orientation as an independent, adversarial function.

### 6.2 Dual-Process Theory (System 1 / System 2)

Kahneman's dual-process framework validates the lane architecture from a different angle:

- **System 1 (fast, associative, high-recall)** corresponds to Hunter operations: pattern matching, retrieval, classification, and surface-level signal detection.
- **System 2 (slow, deliberate, effortful)** corresponds to Analyst and Commander operations: rubric-based evaluation, invariant checking, wrong-reading detection, and authorization decisions.
- **Creative synthesis** (Composer) operates at the boundary between systems, drawing on both associative creativity and deliberate structural reasoning.

Collapsing System 1 and System 2 into a single prompt produces the characteristic errors of each system's failure mode: System 1 anchoring biases contaminate System 2 evaluations, while System 2 cognitive load suppresses System 1 recall breadth. The lane separation preserves each system's strengths while protecting against its characteristic weaknesses.

### 6.3 Active Inference and Predictive Processing

The system's ultimate purpose—activating viewer psychological participation through content—aligns with **active inference** theory from computational neuroscience. Content activates when it creates a prediction error in the viewer's mental model that the viewer is motivated to resolve. The four lanes serve this purpose precisely:

- The **Hunter** identifies source material that carries genuine prediction-gap potential.
- The **Analyst** verifies that the gap is real (not manufactured) and that the source evidence can sustain it.
- The **Composer** sequences the material to maximize the viewer's predictive engagement while preserving truthful resolution.
- The **Commander** ensures that the prediction gap is resolved honestly—no misleading withholding, no fabricated payoff, no wrong reading.

This is not metaphorical decoration on the architecture. It is the functional reason the system exists. The lanes protect the integrity of the viewer's predictive engagement by ensuring that each stage of the content production process is governed by the appropriate epistemic authority.

---

## 7. Constitutional Governance Summary

### 7.1 Authority Order

When rules conflict, authority follows this explicit hierarchy:

1. **Source truth** outranks everything.
2. **CMF Global Constitution** outranks local convenience.
3. **Archetype structural invariants** outrank harness realization preferences.
4. **Harness Constitution** outranks scene-template convenience.
5. **Authorized Content Program** outranks opportunistic generation.
6. **Deterministic gates** outrank model confidence.
7. **Human Commander** resolves remaining high-impact conflicts.

### 7.2 Non-Negotiable Laws

These laws apply to every Canonical Skill in every lane across both domains:

1. **Canonical Skills are not mutated by local adaptations** (FR-031, FR-032).
2. **One Skill owns one independently routable capability** — the granularity test is: "Would the orchestrator ever need to invoke this transformation independently?"
3. **Skills compose flatly** — no Skill invokes another Skill.
4. **Reasoning DNA is shared; ecological adaptation is local** — adapters are external, versioned, and separately testable.
5. **JIT selects and assembles approved Skills; JIT does not bypass maturity and certification** — production execution may assemble stable Skills dynamically but may not invent unvalidated Skills dynamically.
6. **Every lane output is a typed, auditable receipt** — no hidden chain-of-thought substitutes for inspectable evidence, candidates, scores, collisions, rejection reasons, and authorization conditions.
7. **The Commander may reroute but never rewrite** — if a composition needs changes, it returns to the appropriate upstream lane.
8. **Source sovereignty is absolute** — no Skill in any lane may fabricate meaning that the authenticated speaker did not express.

### 7.3 Skill Maturity Progression

Every Skill begins as DRAFT and progresses through evidence-backed maturity stages:

- **DRAFT** — Authored, schema-valid, and logically coherent. Usable in YOLO Draft and Skill Lab.
- **TESTED** — Executed successfully against diverse real inputs with passing evaluation receipts.
- **STABLE** — Demonstrated consistent performance across multiple archetypes, harnesses, and source conditions. Eligible for production campaigns.

Maturity cannot be self-declared. It is earned through execution evidence and evaluation receipts. A Skill that was generated successfully once does not graduate from DRAFT. Maturity progression requires diverse, independently evaluated successful executions.

---

## 8. Conclusion and Authoring Mandate

This constitution establishes that the four Authority Lanes are not organizational labels or agent personas. They are epistemic necessities derived from the failure modes of collapsed cognitive operations, validated by OODA loop theory, dual-process cognitive science, and active inference principles, and enforced through typed contracts, immutable receipt chains, and constitutional authority hierarchies.

The dual-domain architecture (Content Semantic Intelligence and Visual Asset Editor) preserves the same lane structure across fundamentally different material domains—text and images—while ensuring that the delegation bridge between them is governed by explicit demand contracts rather than shared internal state.

Every Canonical Skill authored within this system must declare its lane, its capability boundary, its input and output contracts, its constitutional obligations, its adaptation interfaces, its maturity status, and its evaluation rubric. Skills that violate flat composition, mutate canonical procedures through local adaptation, fabricate source material, or bypass maturity gates are constitutionally invalid regardless of the quality of their output.

The harness definitions—once built—become the demand contracts that drive Skill authoring. Each harness's constitution, archetype compatibility profile, sequencing grammar, and visual realization language specify exactly what each lane's Skills must find, evaluate, compose, and protect. Skills authored without a governing harness definition are generic. Skills authored against a specific harness definition are precise.

Build the harnesses first. Author the Skills around them. Populate the registry from governed packages. Assemble execution capsules JIT from approved, mature Skills. Evaluate everything. Fabricate nothing.
