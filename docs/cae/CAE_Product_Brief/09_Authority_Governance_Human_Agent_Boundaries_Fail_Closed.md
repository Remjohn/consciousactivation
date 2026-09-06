# 9. Authority, Governance, Human-Agent Boundaries & Fail-Closed Behavior

CAE requires governance because its most consequential operations are not simply informational. The engine can change campaign state, select or transform evidence, prepare public artifacts, and move a production toward release. A system with those capabilities cannot rely on the informal assumption that “the model knows what is allowed.” Authority must be represented explicitly, carried through execution, and checked at the point of action.

The primary constitutional boundary is **Agents Recommend; Humans Authorize**. Agents can research, rank, summarize, detect collisions, extract evidence, compose proposals, identify alternatives, and perform constrained transformations. They may not silently turn their recommendation into an irreversible human decision. The Operator remains the conduit through which consequential product decisions are accepted, rejected, repaired, or released.

The current runtime makes this boundary concrete. The Program Operator Runtime defines typed actions including DISCOVER, RUN, INSPECT, PAUSE, RESUME, APPROVE, REJECT, REPAIR, SHIP, and EXPORT_AUDIT. It also defines four authority lanes—Hunter, Analyst, Composer, and Commander—and typed rejection dispositions that route failed candidates back to the appropriate stage, request more source, or archive them. This is a much stronger pattern than a free-form agent system because the system knows not only what an agent wants to do but which authority lane is allowed to perform the action.

Authority must be **singular at the execution level**. The App, chat interfaces, future Slack or Telegram adapters, and other interaction surfaces are not separate sources of truth. They are means through which a human expresses an intent to the same governed runtime. Campaign state, execution state, routing decisions, approvals, rejections, repairs, receipts, and lineage must be authoritative in the core runtime. A channel may submit a command or correction; it cannot create a second campaign reality.

This matters for human-agent boundaries because natural language is inherently ambiguous. A human may say, “This isn't right—find something more emotional.” That should not bypass typed governance. CAE can interpret the statement into a structured proposal: perhaps a semantic constraint, a retrieval preference, a role change, or a request for another evidence candidate. The runtime then validates the proposed operation against the current authority state. The system should not interpret every conversational sentence as an executable command.

The same distinction applies to model selection. An Operator should ordinarily not be forced to manually choose an LLM for each task. Routing should allocate intelligence inside a governed policy. If a human has a specific reason to override a model choice, that override should itself be a typed, auditable action subject to the same certification and output-contract rules. Otherwise the product becomes a model picker rather than an intelligent execution system.

The core execution object also needs integrity. CAE's canonical AgentInvocation contract defines a single governed execution object containing Agent identity, execution state, compiled package, context capsule, model policy, skills, tools, capabilities, output contract, and prompt. The object is immutable and hash-addressed. Authorized tools and forbidden actions travel deterministically with the invocation. Model resolution is bounded by the Agent's declared model policy and authority lane. Execution produces an AgentInvocationReceipt linking package, capsule, invocation, and response digests.

This is the technical expression of a deeper principle: **authority should travel with the work**. It is not enough to check permissions at the user interface. If an invocation can be copied, modified, or detached from the constraints under which it was approved, the system has a bypass. CAE therefore validates invocation integrity, rejects unauthorized tools, blocks unauthorized model selection, and validates outputs against declared contracts.

Fail-closed behavior follows from the same logic. When required evidence is missing, provenance is incomplete, an authority state is ineligible, an output contract is violated, a tool was not declared, a model is unauthorized, or a production execution lacks a real authorized inference engine, the system should not invent a plausible substitute. It should stop, escalate, or produce an explicit failure state. A governed refusal is often more useful than an apparently successful but invalid result.

The live code provides several examples. The AgentInvocation runtime raises an unauthorized-model error when a requested model is outside the Agent policy. It rejects unauthorized tool calls when a tool is not declared in the compiled invocation. It refuses production execution when no live ModelReasoningEngine or authorized inference provider is available rather than falling back to a deterministic mock. The Pipeline retrieval engine rejects projections whose authority or lifecycle state is ineligible and explicitly treats incomplete interview provenance as a validation failure.

The Operator Runtime adds a complementary state-safety mechanism through optimistic locking. Execution mutations use `state_version` and `state_hash` controls to reduce stale-UI mutation risk. That matters because governance is not only about who is allowed to click “approve.” It is also about whether the object being approved is still the object the Operator inspected. If the execution has changed since the approval view was loaded, the action should fail or require reinspection rather than silently apply to a newer state.

Governance also requires separation of concerns. Discovery, analysis, composition, and authorization should remain distinct even when the same underlying model can technically perform all four. A model that finds a candidate should not automatically declare it approved. A composer should not silently alter evidence to satisfy a requested format. A Commander should not infer missing evidence merely because production is behind schedule. The roles exist precisely to prevent these forms of responsibility leakage.

Rejection is consequently a productive operation rather than an error message. A rejected candidate should preserve its identity and history. The Operator may route the rejection back to the Hunter, Analyst, Composer, request additional source, or archive it. A natural-language injection can add intent to the next attempt, but the original proposal remains immutable history. This creates a governed correction loop:

**proposal → human decision → structured correction → constrained regeneration → validation → next proposal.**

That loop is valuable for both production quality and learning, but learning must remain subordinate to governance. A model that becomes very good at predicting Operator preferences does not gain authority to approve its own output.

Fail-closed behavior should also be applied to quotas and delivery pressure. If a monthly package declares 32 artifacts but the interview yields evidence for only 24 legitimate artifacts, the system must not fabricate eight more simply because the business plan says 32. The correct runtime outcome is a yield exception, a follow-up requirement, or an accepted lower-yield state with an explicit explanation. Operational pressure must never become a hidden permission to weaken the constitution.

The governance architecture therefore has three levels. **Policy** defines what is permitted. **Runtime state** determines what is currently eligible. **Human authority** resolves consequential choices when the system reaches a decision boundary. Agents operate inside that system; they do not replace it.

This produces a useful CAE invariant:

> **The model can increase the intelligence of an action, but it cannot increase its authority.**

That invariant should survive model upgrades, routing changes, new channels, and future automation. A more capable model may make better recommendations. A cheaper model may execute a safe classification. A multimodal model may find a stronger media candidate. None of those improvements change who can authorize release.

CAE therefore becomes trustworthy not because it assumes models will always behave correctly, but because incorrect or unauthorized behavior has limited paths through which it can become consequential. The system measures the boundary, records the decision, preserves the lineage, and fails closed when the conditions for legitimate execution are absent.

That is the governance layer that allows CAE to become more autonomous in capability without becoming autonomous in authority.
