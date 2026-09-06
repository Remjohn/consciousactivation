# 13. Observability, Production Telemetry, Learning Data & Post-Training

In CAE, observability is not merely an engineering concern. It is part of the product because the product's value depends on a causal chain that must remain explainable after execution: what evidence entered the system, what intelligence acted on it, what decision was proposed, what the Operator changed, what artifact was released, and what happened afterward. A system that can generate output but cannot reconstruct why that output exists cannot reliably improve the transformation it is selling.

Traditional application telemetry answers operational questions: did the request finish, how many tokens were consumed, how long did the API call take, and did the service return an error? CAE needs those measurements, but they are insufficient. The meaningful unit is the **governed production transformation**. Observability should therefore connect model execution to semantic decisions, human decisions, artifacts, and outcomes without breaking provenance or exposing unnecessary data.

The canonical telemetry chain should be:

**evidence → task → model invocation → candidate decision → validation → human correction or approval → artifact → release state → outcome → learning record.**

Each stage should be addressable through stable identifiers. The AgentInvocation architecture already points toward this pattern by carrying a compiled package, context capsule, model policy, skills, tools, capabilities, output contract, and prompt inside an immutable governed execution object, with a receipt linking package, capsule, invocation, and response digests. The runtime also records inference-oriented metrics such as token counts, latency, provider class, and execution state. These structures provide the basis for a causal telemetry layer rather than a collection of unrelated logs.

CAE should record at least six classes of telemetry. **Execution telemetry** captures model/provider, version, latency, token usage, retries, errors, tool usage, and fallback. **Semantic telemetry** captures selected evidence, candidate scores, extraction outcomes, contradiction findings, and validation results. **Governance telemetry** captures authority lane, permitted actions, rejection reason, approval state, and any fail-closed event. **Human telemetry** captures Operator acceptance, rejection, repair, override, and correction categories. **Artifact telemetry** captures composition lane, provenance coverage, render result, and release status. **Outcome telemetry** captures downstream performance, yield, time-to-package, and other business or activation measurements.

The purpose is not to store everything forever. CAE should practice **learning-data minimization with traceability**. Raw prompts and outputs may be necessary for certain forensic or evaluation workflows, but the product should distinguish operational retention from training retention. Sensitive or unnecessary material should not automatically become training data simply because it passed through the system. Learning datasets should use explicit inclusion rules, retention policies, provenance, consent/rights checks where applicable, and reproducible dataset versions.

Human correction is particularly valuable because it contains high-quality supervision. An Operator's action can reveal that a model selected the wrong quote, missed the stronger collision, inferred unsupported emotion, violated a format contract, or simply used an inferior candidate. These are not all the same failure type. CAE should classify them so the resulting data can support different improvements. Some corrections belong in routing evaluation, some in semantic benchmark cases, some in policy examples, and some in interface design.

This leads to three major learning datasets. **CAE-Semantic** can hold evidence extraction, ranking, relationship reconstruction, semantic editing, and canonicalization examples. **CAE-Policy** can hold authorized versus unauthorized transformations, provenance failures, composition-lane violations, governance refusals, and authority-boundary cases. **CAE-Interview** can hold successful and unsuccessful questions, follow-ups, gap-detection examples, and elicitation sequences. These datasets should remain distinct because optimizing one behavior should not silently weaken another.

Post-training then becomes a practical economic lever rather than a prestige exercise. A general-purpose model is expensive because it must maintain broad capability. CAE can potentially teach smaller or mid-sized models the product-specific behaviors that recur across thousands of transformations: output structures, evidence alignment patterns, ranking conventions, repair heuristics, and task-specific style controls. The objective is not to create a magical “CAE model” that replaces the entire stack. It is to reduce how often CAE needs expensive general intelligence.

The economic flywheel is straightforward:

**Production → telemetry → evaluation → human correction → curated data → post-training or routing improvement → lower correction cost / better reliability → more accepted production.**

The flywheel only works if the learning loop is protected from feedback contamination. A model's own output must not become ground truth merely because it was successful once. Acceptance by an Operator is stronger evidence than raw model confidence. Outcome success is useful but also insufficient on its own; a high-performing artifact created with invalid authorship would still violate the product contract. Training labels should therefore preserve the distinction among source evidence, model proposal, human authorization, and market outcome.

Observability should also make failures first-class objects. A fail-closed event is not simply an application exception to be hidden in logs. It is evidence that a declared precondition was absent. The system should preserve the stage, failed contract, authority state, relevant evidence references, and next permitted disposition where possible. That allows engineering teams to see whether the product is failing because models are weak, source material is insufficient, contracts are too strict, or the Operator is repeatedly encountering the same workflow gap.

The Product Brief should also define a **causal debugging standard**. When a released artifact is later found to be weak, the investigation should be able to move backward through its lineage to the relevant evidence, production requirement, model invocation, validation result, and approval. Conversely, when an artifact performs exceptionally well, CAE should be able to study the upstream evidence and transformation pattern without pretending that performance proves causal truth. This distinction is crucial for responsible learning.

Post-training should be gated by certification. A newly trained model enters the same evaluation system as an external candidate. It must pass CSEB or the applicable task suite, satisfy governance requirements, and demonstrate acceptable operational and economic behavior before routing policy can assign it production work. This makes the learning loop recursive without making it self-authorizing.

The strongest principle in this section is therefore:

> **Model learning improves capability. Contracts retain authority.**

A fine-tuned model cannot become the constitution. A model that learns a persuasive shortcut cannot bypass provenance. A model that predicts Operator preferences cannot approve its own output. A model that becomes cheaper cannot be routed into a high-risk task until its task-specific certification is established.

CAE's observability layer should ultimately make the product measurable at the level that matters: not “how many calls did we make?” but **how much governed transformation did each unit of intelligence purchase?** That supports both engineering optimization and commercial economics. It lets CAE compare models, workflows, and Operators by accepted artifact yield, correction burden, latency, and downstream activation rather than vanity metrics.

In this architecture, telemetry is the memory substrate for the production system. It records not only what the machine did but how humans corrected it and what the market subsequently did with the result. That is what turns CAE from a static automation product into a system capable of evidence-backed evolution.
