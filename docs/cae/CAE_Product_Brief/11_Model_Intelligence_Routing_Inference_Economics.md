# 11. Model Intelligence, Routing & Inference Economics

CAE should be model-agnostic but intelligence-contract-driven. The product should never define its identity as “an application powered by Model X.” Models change, vendors change, context limits change, inference pricing changes, and hardware economics change. What must remain stable is the task contract: what intelligence a particular CAE operation requires, what evidence boundary it must respect, what output contract it must satisfy, what reliability is acceptable, and what cost envelope makes the operation economically viable.

This changes the fundamental model-selection question. CAE is not trying to discover the globally “smartest” model. It is trying to answer:

> **Which certified intelligence is sufficient for this transformation, at the lowest acceptable cost and operational risk?**

That is the purpose of the model-intelligence layer. It sits between the declarative task and the governed Agent invocation system, allocating the appropriate amount and type of intelligence without changing the underlying authority rules.

CAE tasks have different intelligence requirements. Interview Brief construction needs knowledge integration, retrieval, context management, and uncertainty handling. Interview Question generation needs gap detection, reasoning, audience understanding, and narrative awareness. Transcript extraction requires high evidence fidelity and long-context semantic reasoning. Quote selection is a ranking problem constrained by exact source evidence. Narrative reconstruction requires synthesis while preserving relationships and provenance. Editing requires faithfulness and instruction following. Rendering is primarily tool and execution competence. Governance validation requires strong instruction adherence, refusal behavior, and sensitivity to policy boundaries.

The routing philosophy should therefore be:

**task classification → intelligence lane → policy constraints → certified candidate models → cost/latency comparison → execution → validation → fallback or escalation.**

The router identifies what kind of transformation is required. It does not invent a policy for what is allowed. Policy determines which models are eligible for that lane. The Agent determines which models are authorized for its invocation. The selected model executes inside the same compiled context, tools, capabilities, output contract, and authority boundary that would apply regardless of model choice.

A small routing model or deterministic classifier may become an important component of this architecture. Its economic role is not to perform the expensive transformation. Its role is to make a low-cost prediction about which transformation lane is required.  A compact local encoder can potentially perform high-volume classification or triage cheaply, while richer models handle semantic synthesis, long-context reconstruction, or difficult multimodal work.

But the router must remain subordinate to governance. Its output is a recommendation to policy, not permission. This is why the product principle should be:

> **Routing is policy-controlled classification, not model improvisation.**

The AgentInvocation runtime already expresses a version of this boundary. Its contract states that Agent model resolution is strictly bounded by the Agent's model policy and authority lane. The compiled invocation includes model policy, skills, tools, capabilities, output contract, and prompt, and its integrity is checked before execution. An unauthorized model produces a typed failure rather than silently substituting another provider. citeturn178167view0

The economics become meaningful when routing is connected to observable execution data. For each invocation, CAE can capture model or provider identity, model version, latency, token usage, output-contract result, validation outcome, retries, fallback, and ultimately human correction and artifact outcome. The runtime already records inference metrics such as prompt tokens, completion tokens, total tokens, latency, provider class, and production execution state. It also explicitly prohibits deterministic mock fallback during production execution when no authorized live inference engine is available. citeturn178167view1

This supports a richer economic metric than raw token price. A model that costs 20% more but reduces Operator correction by 50% may be cheaper at the system level. A model that is inexpensive but produces frequent provenance failures can become expensive through retries and human review. CAE therefore needs to reason about **cost per accepted transformation**, not cost per API call.

A useful economic north star is **Cost Per Accepted Activation Package (CPAAP)**. This metric can combine intelligence spend, retries, operator review burden, rendering or media-retrieval overhead, and other production costs against the number of packages that reach an accepted state. It is to establish the correct optimization target. CAE is economically successful when it can produce high-quality, human-authorized activation at lower total system cost, not merely when it uses cheap models.

Routing should also be risk-aware. Some tasks can tolerate a weak model because errors are easy to detect and cheap to recover. Other tasks are high consequence because a mistake can alter authorship, provenance, rights status, or public meaning. The router should therefore consider task risk alongside capability. A deterministic parser may be preferred for exact phrase extraction even when an LLM could do it. A higher-capability model may be required for a complex contradiction analysis. A governance-sensitive operation may be forced through a certified model class or an explicit validation stage.

The system should support **graceful escalation**. A low-cost model can attempt a task inside a safe contract. If the validation layer finds that the result is incomplete, ambiguous, or below the required confidence threshold, CAE can escalate to a more capable certified model or a human gate. This is more efficient than routing every task to the most expensive model from the beginning. The critical requirement is that escalation remains deterministic enough to observe and reproduce.

Importantly, “confidence” must not become an opaque model feeling. A routing decision should be represented with observable information: selected lane, candidate set, routing uncertainty, selected model, fallback behavior, validation result, and eventual outcome. The Operator should see which intelligence was used and why, supporting troubleshooting, cost management, and later certification.

Inference economics also benefit from architectural locality. Transcript processing can be segmented into deterministic extraction first, followed by global semantic reasoning only where needed. Retrieval can use exact search before semantic ranking. Asset lookup can filter ineligible sources before applying expensive dense or multimodal ranking. Small models can handle high-volume classification. 

The model layer must remain replaceable. CAE can maintain a control baseline for historical comparison without making a particular vendor constitutionally permanent. Candidate models can enter through a certification process that measures them against CAE-specific tasks. A provider migration should therefore change a versioned implementation or policy artifact, not the identity of the product itself.

Learning completes the economic loop. Production telemetry can reveal that a model is cheap but causes excessive semantic corrections, that another model is expensive but nearly eliminates review, or that a small router misclassifies a certain class of requests. Those observations can inform benchmark updates, routing-policy changes, model selection, and post-training. But learning cannot rewrite governance. A model that improves economically still has to satisfy the same evidence, authority, and composition contracts.

The CAE model architecture can therefore be summarized as:

**Model capability → task fit → routing → governed execution → validation → human acceptance → economic measurement → learning.**

This is what makes model intelligence a product capability rather than an implementation detail. The engine is not valuable because it has access to many models. It is valuable because it can allocate intelligence deliberately while preserving the human authority and evidence discipline established elsewhere in the system.

In the long term, the highest-value outcome is a compounding intelligence allocation advantage. CAE observes which models are effective at which transformations, which errors matter, which corrections recur, which retrieval strategies resolve fastest, and which outputs actually become accepted activation. The result can be a progressively better map from task to intelligence, with lower average inference cost and higher reliability.

The governing rule remains simple:

> **Use the least expensive certified intelligence that can satisfy the task contract, and escalate when the evidence, risk, validation result, or authority boundary requires more.**

That rule prevents CAE from becoming a model showcase. It turns intelligence into an economic resource governed by the same constitutional architecture as every other part of the product.
