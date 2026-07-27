from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
PLANNING = ROOT / "docs" / "planning"
INVENTORY = PLANNING / "PLANNING_REQUIREMENTS_INVENTORY.csv"
EPIC_SOURCE = PLANNING / "EPIC_INVENTORY.yaml"
EPIC_COVERAGE = PLANNING / "EPIC_REQUIREMENT_COVERAGE.csv"
EPIC_CONFIRMATION = PLANNING / "EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml"

STORY_INVENTORY = PLANNING / "STORY_INVENTORY.yaml"
STORY_COVERAGE = PLANNING / "STORY_REQUIREMENT_COVERAGE.csv"
STORY_DEPENDENCIES = PLANNING / "STORY_DEPENDENCY_GRAPH.csv"
STORY_PROPOSAL = PLANNING / "STORY_DESIGN_PROPOSAL.md"
STORY_GROUPED = PLANNING / "STORY_INVENTORY_BY_EPIC.md"
STORY_BLOCKED = PLANNING / "STORY_BLOCKED_CONDITIONAL_REGISTER.yaml"
STORY_RELEASE_1 = PLANNING / "RELEASE_1_STORY_SUBSET.yaml"
STORY_CROSS_REPOSITORY = PLANNING / "STORY_CROSS_REPOSITORY_DEPENDENCIES.yaml"


EPIC_CONTRACTS_AND_SCHEMAS = {
    "EP-01": {
        "contracts": ["RunLifecycle", "EvidenceWorkspace", "ConstitutionalReadinessReceipt"],
        "schemas": ["docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ConstitutionalReadinessReceipt"],
    },
    "EP-02": {
        "contracts": ["SyntaxObservation", "DraftHarnessModel", "SharedActivativeCore", "ConversationalActivationExpression"],
        "schemas": ["docs/contracts/schemas/shared-activative-core.schema.json", "docs/contracts/schemas/conversational-expression.schema.json"],
    },
    "EP-03": {
        "contracts": ["GenesisDecisionReceipt", "HarnessIR", "SharedActivativeCore", "ActivativeIntelligencePack"],
        "schemas": ["docs/contracts/schemas/shared-activative-core.schema.json"],
    },
    "EP-04": {
        "contracts": ["CapabilityOwnership", "PhaseContract", "ContextContract", "HandoffContract", "ReferenceContract"],
        "schemas": [],
    },
    "EP-05": {
        "contracts": ["SkillPackage", "SkillRecipe", "PhaseCapsule"],
        "schemas": [],
    },
    "EP-06": {
        "contracts": ["SharedActivativeCore", "ActivativeIntelligencePack", "ConversationalActivationExpression", "ActivativeCall", "ReactionReceipt", "ExpressionMoment", "IdentityDNAAmendmentProposal"],
        "schemas": ["docs/contracts/schemas/shared-activative-core.schema.json", "docs/contracts/schemas/conversational-expression.schema.json"],
    },
    "EP-07": {
        "contracts": ["TargetProfile", "VisualSemanticAndNarrativeHandoff", "TVRouteRequest", "DelegationHandoff", "AssetDemandSemanticLineage"],
        "schemas": ["docs/contracts/schemas/visual-semantic-handoff.schema.json"],
    },
    "EP-08": {
        "contracts": ["EvaluationCase", "ConstitutionalEvaluationReceipt", "ConstitutionalReadinessReceipt", "RepairReceipt"],
        "schemas": ["docs/contracts/schemas/constitutional-evaluation.schema.json", "docs/contracts/schemas/conversational-expression.schema.json"],
    },
    "EP-09": {
        "contracts": ["WorkflowIR", "WorkflowNodeContract", "CheckpointReceipt", "PromotionReceipt"],
        "schemas": [],
    },
    "EP-10": {
        "contracts": ["ControlTowerConstitutionalProjection", "GovernedCommand", "ProjectionReceipt"],
        "schemas": ["docs/contracts/schemas/constitutional-evaluation.schema.json#/$defs/ControlTowerConstitutionalProjection"],
    },
    "EP-11": {
        "contracts": ["DevelopmentCapsule", "StoryCompletionReceipt", "ImplementationDeltaProposal"],
        "schemas": ["docs/contracts/schemas/constitutional-evaluation.schema.json"],
    },
    "EP-12": {
        "contracts": ["MigrationReceipt", "CertificationMatrix", "ConstitutionalReadinessReceipt", "DelegationHandoff"],
        "schemas": ["docs/contracts/schemas/constitutional-evaluation.schema.json", "docs/contracts/schemas/visual-semantic-handoff.schema.json"],
    },
}


CROSS_REPOSITORY_BOUNDARIES = {
    "XDEP-001": "Builder consumes pinned program authority; it does not mutate program-control truth from Story implementation.",
    "XDEP-002": "Builder may compile and contract-test the VAE target profile and handoff; VAE owns production editor behavior.",
    "XDEP-003": "Delegation owns shared contracts and runtime; Builder consumes a pinned snapshot and emits a compatible handoff only.",
    "XDEP-004": "Builder supplies structural Interview Expression and ReelCast profiles only; the future product owns its PRD and live behavior.",
    "XDEP-005": "The Operator Manual consumes stable behavior later; documentation cannot substitute for Builder acceptance evidence.",
    "XDEP-006": "Builder preserves Activative Intelligence Pack lineage; the Activation Compiler owns upstream semantic truth.",
}


EPIC_DEFAULTS = {
    "EP-01": {
        "boundary": "Run governance and configured evidence workspace; downstream design and execution remain outside this increment.",
        "test": "Target-profile lifecycle and evidence public-seam scenarios with fail-closed fixtures.",
        "compatibility": "Preserve shared lifecycle semantics while versioning target-specific source and state contracts.",
    },
    "EP-02": {
        "boundary": "Evidence understanding and atomic-boundary decision support; no runtime production or semantic invention.",
        "test": "Golden specimen, conversational transcript, ambiguity, and wrong-boundary fixtures at parser and ratification seams.",
        "compatibility": "Preserve Visual Syntax First for development and keep category-specific parse schemas versioned.",
    },
    "EP-03": {
        "boundary": "Genesis authority and canonical Harness IR compilation; no downstream product execution.",
        "test": "Decision-graph, receipt replay, canonical serialization, migration, and cross-artifact consistency seams.",
        "compatibility": "Use explicit IR schema migrations and preserve frozen authority, hashes, and Activative lineage.",
    },
    "EP-04": {
        "boundary": "Capability, module, phase, context, reference, and handoff architecture; no hidden orchestration implementation.",
        "test": "Ownership, graph integrity, handoff mutation, impact-analysis, and context-budget contract seams.",
        "compatibility": "Version graph and handoff contracts; reject silent downstream rewriting or required-context truncation.",
    },
    "EP-05": {
        "boundary": "Canonical skill ecology and phase-local capsule compilation; production workflow ownership stays outside skills.",
        "test": "Capability-gap, no-guidance control, package validation, binding resolution, and deterministic capsule seams.",
        "compatibility": "Pin skill, recipe, binding, evaluator, and source versions; preserve portable skill package contracts.",
    },
    "EP-06": {
        "boundary": "Five-category and conversational profile contract compilation; live Interview and ReelCast execution remain external.",
        "test": "Category/profile schema, rich-to-sparse lineage, sequencing, Reaction Receipt, Expression Moment, and HG-015 seams.",
        "compatibility": "Preserve all five category IDs, four conversational profile IDs, Activation First runtime law, and Visual Syntax First development law.",
    },
    "EP-07": {
        "boundary": "Three Builder target compilers and frozen cross-product handoffs; VAE and Delegation runtimes remain external.",
        "test": "Target-profile separation, artifact-set completeness, lineage round-trip, compatibility, and external-port contract seams.",
        "compatibility": "Version all three target profiles and require lossless migrations without universal-profile flattening.",
    },
    "EP-08": {
        "boundary": "Independent behavioral evaluation, selective repair, and authorization receipts; thresholds remain human-governed.",
        "test": "Protected benchmark, fresh-context, mutation, wrong-reading, repair, regression, and readiness decision seams.",
        "compatibility": "Pin benchmark, evaluator, threshold, artifact, repair, and receipt versions; never inherit certification silently.",
    },
    "EP-09": {
        "boundary": "Builder workflow routing and execution control plane; no monolithic skill-owned or external product workflow.",
        "test": "Manual-shadow parity, node contract, isolation, retry, resume, fault-injection, promotion, and rollback seams.",
        "compatibility": "Version workflow profiles and adapters; require migration and rollback evidence before promotion.",
    },
    "EP-10": {
        "boundary": "Approved evidence-derived Control Tower projections and commands; the UI never becomes authoritative state.",
        "test": "Projection, route, graph, command, accessibility, stale-state, redaction, budget, and telemetry UX seams.",
        "compatibility": "Preserve approved routes and command contracts; version projections without redesigning Control Tower authority.",
    },
    "EP-11": {
        "boundary": "Development Capsule and implementation handoff planning; no implementation execution in this increment.",
        "test": "Capsule completeness, traceability, contract example, fixture, dependency-order, and feedback-ingestion seams.",
        "compatibility": "Hash-bind every capsule to authority and contract versions; govern all later implementation-discovered deltas.",
    },
    "EP-12": {
        "boundary": "Brownfield migration and bounded Release 1 proof; no general certification from the Format 02 reference path.",
        "test": "Dual-compilation, regression, migration receipt, compatibility alias, reference-path, and certification-scope seams.",
        "compatibility": "Retain or deprecate V2.1 behavior only through evidence and receipts; keep unproven categories and targets uncertified.",
    },
}


ACTION_INFINITIVES = {
    "applies": "apply", "binds": "bind", "checkpoints": "checkpoint", "classifies": "classify",
    "compares": "compare", "compiles": "compile", "derives": "derive", "dual-compiles": "dual-compile",
    "encounters": "encounter", "evaluates": "evaluate", "exposes": "expose", "groups": "group",
    "indexes": "index", "ingests": "ingest", "inspects": "inspect", "inventories": "inventory",
    "loads": "load", "maps": "map", "measures": "measure", "monitors": "monitor", "moves": "move",
    "navigates": "navigate", "normalizes": "normalize", "opens": "open", "operates": "operate",
    "parses": "parse", "preflights,": "preflight,", "promotes": "promote", "publishes": "publish",
    "queries": "query", "ratifies": "ratify", "records": "record", "registers": "register",
    "resolves": "resolve", "reviews": "review", "routes": "route", "runs": "run", "selects": "select",
    "separates": "separate", "tests": "test", "traces": "trace", "uses": "use",
    "validates": "validate", "verifies": "verify", "writes": "write",
}


def as_infinitive(action: str) -> str:
    first, separator, remainder = action.partition(" ")
    return f"{ACTION_INFINITIVES.get(first, first)}{separator}{remainder}"


def story(
    story_id: str,
    epic_id: str,
    title: str,
    actor: str,
    action: str,
    value: str,
    failure: str,
) -> dict[str, str]:
    return {
        "id": story_id,
        "epic_id": epic_id,
        "title": title,
        "actor": actor,
        "action": action,
        "intent": as_infinitive(action),
        "value": value,
        "failure": failure,
    }


STORIES = [
    story("ST-01.01", "EP-01", "Start and Resume One Target-Profiled Builder Run", "Harness Architect", "selects exactly one compilation target and starts or resumes its governed lifecycle", "the run has stable identity, explicit authority, replay-safe state, and target-specific required work", "Reject missing or multiple targets, invalid transitions, unauthorized waivers, and any resume that replays a human decision."),
    story("ST-01.02", "EP-01", "Lock a Safe Target-Specific Evidence Workspace", "Harness Architect", "validates a real target boundary and creates an immutable target-specific source lock", "source material is portable, safe to inspect, and protected from mutation", "Block invalid paths, unsafe archives, missing consent policy, unreadable authority, and any attempted source mutation."),
    story("ST-01.03", "EP-01", "Index Every Evidence Specimen with Provenance", "Evidence steward", "indexes every target specimen and its relationships under immutable evidence identity", "later decisions can query complete evidence and distinguish observation, status, and provenance", "Fail when specimens are unaccounted for, identities collide, provenance is missing, or corpus processing loses knowledge status."),
    story("ST-01.04", "EP-01", "Decide Evidence Saturation Without Inventing Claims", "Harness Architect", "evaluates the target saturation contract and classifies gaps or authority conflicts", "the run proceeds, pauses, or blocks through an evidence-backed typed outcome", "Block critical claims without evidence and prohibit readiness or semantic invention from incomplete sources."),

    story("ST-02.01", "EP-02", "Normalize Evidence into Typed Syntax Observations", "Constitutional reviewer", "normalizes and deduplicates visual or conversational specimens into typed syntax observations", "reviewers can compare reliable geometry, components, turns, and evidence identities", "Reject unsupported parser outputs, duplicate inflation, provider-only claims, and observation fields contaminated by hypotheses."),
    story("ST-02.02", "EP-02", "Build Spatial, Temporal, and Reading-Order Graphs", "Constitutional reviewer", "parses spatial relationships, hierarchy, reading order, composition variables, and temporal syntax", "the candidate grammar is grounded in substrate-specific relationships rather than vague meaning", "Fail on dangling graph targets, impossible geometry, missing time states, or category-inappropriate parse fields."),
    story("ST-02.03", "EP-02", "Induce Grammar Only After Syntax Evidence", "Harness Architect", "separates observations from WHY hypotheses and induces cross-specimen, sequence, and Activative hypotheses", "Visual Syntax First governs development discovery while unsupported meaning stays visibly provisional", "Reject meaning-first inference, unsupported knowledge promotion, and category grammar that erases conversational or temporal evidence."),
    story("ST-02.04", "EP-02", "Compare Candidate Atomic Product Boundaries", "Harness Architect", "compares merge, split, variant, and family boundaries with typed risk and recommendations", "human authority can see the consequence of each candidate before choosing the atomic product", "Block a recommendation that lacks evidence, hides alternatives, or uses an uncalibrated protected-boundary claim as certainty."),
    story("ST-02.05", "EP-02", "Ratify and Freeze the Draft Harness Boundary", "Product authority", "ratifies one atomic boundary and freezes a transparent Draft Harness Model for Genesis", "downstream constitutional decisions start from an explicit, reviewable, and stable product boundary", "Reject unratified promotion, freeze with unresolved critical boundary contradiction, and any later silent boundary rewrite."),

    story("ST-03.01", "EP-03", "Ask Only Dependency-Ready Constitutional Questions", "Harness Architect", "opens only dependency-ready Genesis decisions and presents one evidence-backed recommendation per turn", "human attention is spent on the next consequential question with complete rationale", "Block unsupported constitutional decisions, premature questions, or recommendations that omit relevant evidence and alternatives."),
    story("ST-03.02", "EP-03", "Record Human Authority and Resume Genesis Safely", "Product authority", "records the human answer separately from the final decision, updates state transactionally, and resumes without replay", "human authority remains explicit, auditable, and recoverable across sessions", "Reject agent substitution for required human authority, partial decision commits, contradictory cascade locks, and replayed approvals."),
    story("ST-03.03", "EP-03", "Maintain One Provenance-Rich Canonical Harness IR", "Compiler maintainer", "writes ratified values and frozen references into one versioned canonical Harness IR", "all downstream artifacts share one source of truth with explicit schema evolution and Activative lineage", "Fail on missing provenance, incompatible schema changes, local semantic copies, or divergence between Harness IR and Workflow IR ownership."),
    story("ST-03.04", "EP-03", "Compile Human and Machine Artifacts Deterministically", "Compiler maintainer", "compiles sharded specifications, OpenSpec views, and machine artifacts from the same IR", "maintainers receive reproducible, hash-bound outputs without duplicated authority", "Reject manual drift, nondeterministic serialization, incomplete artifact sets, unresolved references, and non-idempotent recompilation."),
    story("ST-03.05", "EP-03", "Enforce Constitutional Precedence Across Compiled Artifacts", "Constitutional reviewer", "validates cross-artifact completeness and constitutional precedence before release", "lower-authority artifacts cannot override Constitution V1.1 or lose semantic lineage", "Block any conflict, missing constitutional applicability, or artifact set that passes syntax while violating higher authority."),

    story("ST-04.01", "EP-04", "Assign Explicit Ownership to Every Required Capability", "Harness Architect", "inventories capabilities and assigns code, agent, human, external, or hybrid ownership using reliability and cost evidence", "the design has accountable owners and no capability disappears between product intent and execution", "Reject unowned capabilities, unjustified agent ownership, universal-skill defaults, and hybrids without explicit handoff responsibility."),
    story("ST-04.02", "EP-04", "Compile Responsibility-Centered Modules with Test Seams", "Architecture maintainer", "groups capabilities into responsibility-centered modules with declared public test seams", "each module can change and be tested without recreating horizontal technical layers", "Block mixed-authority modules, hidden side effects, missing seams, and modules defined only as database, API, UI, router, or agent layers."),
    story("ST-04.03", "EP-04", "Order Work Through an Executable Phase Graph", "Harness Architect", "compiles sequential and dependency-independent phase relationships", "the harness exposes what may run now, later, or safely in parallel", "Reject cycles, undeclared dependencies, default parallelism, and phase edges that bypass required human or validation gates."),
    story("ST-04.04", "EP-04", "Protect Typed Phase and Context Handoffs", "Architecture maintainer", "compiles phase-specific contexts and versioned handoffs with ownership and mutation limits", "downstream work receives complete inputs without silently rewriting upstream truth", "Block contract contradictions, missing authority, silent rewrites, dangling dependencies, and invalidation that reruns unaffected state."),
    story("ST-04.05", "EP-04", "Compile Minimum Complete Context Without Silent Truncation", "Context architect", "selects references, SPR, progressive-disclosure pointers, and context budgets by functional necessity", "each phase receives the minimum complete context plus a complete manifest", "Block missing required pointers, conversation-history substitution, silent truncation, unbounded loading, and budgets that hide omitted authority."),

    story("ST-05.01", "EP-05", "Operate a Versioned Canonical Skill Registry", "Skill maintainer", "registers canonical skills by authority lane, maturity, plasticity, and evaluated identity", "the team can distinguish stable reusable behavior from local adaptation and experimental capability", "Reject duplicate capability claims, maturity without receipts, stale evaluator pins, and skill sediment hidden as active behavior."),
    story("ST-05.02", "EP-05", "Prove a Skill Is Needed Before Designing It", "Harness Architect", "runs the capability-gap test and prefers reuse, adaptation, or adapter composition", "new skill work begins only where behavior evidence shows a real gap", "Reject skill creation when the control has no target failure, ownership belongs in code or workflow, or an existing capability is adequate."),
    story("ST-05.03", "EP-05", "Package Portable Skills with Behavioral Anchors", "Skill maintainer", "compiles tested leading words, progressive disclosure, evaluation links, and no-op detection into a portable package", "skill behavior is attributable, maintainable, and reusable across compatible harnesses", "Block packages without behavioral lift, evaluator assets, authority boundaries, or evidence that redundant instructions were removed."),
    story("ST-05.04", "EP-05", "Assemble a Deterministic Phase-Local JIT Capsule", "Capsule compiler maintainer", "resolves recipes, bindings, precedence, degradation rules, and minimum complete context into one capsule", "an agent receives exactly the evaluated authority and context needed for the current phase", "Block unresolved bindings, untested required skills, authority conflicts, forbidden degradation, and confusion between canonical skills and runtime capsules."),
    story("ST-05.05", "EP-05", "Pin and Dispose of Capsules Reproducibly", "Capsule compiler maintainer", "binds exact versions and hashes, executes within bounded stochastic policy, and treats capsules as ephemeral", "a phase can be replayed without accumulating hidden conversational state or stale capsule sediment", "Reject unpinned inputs, persistent phase-local context, nondeterministic assembly, and reuse outside the declared capsule scope."),

    story("ST-06.01", "EP-06", "Bind Every Harness to One of Five Canonical Categories", "Category steward", "compiles the Shared Activative Core through one governed category and versioned category constitution", "all five categories remain distinct while preserving shared meaning and atomic creative ownership", "Block unsupported categories, flattened category IDs, missing conversational category support, absent wrong-reading locks, and semantic stacks that fail HG-015."),
    story("ST-06.02", "EP-06", "Compile Category-Local Format and Performance Profiles", "Category steward", "maps edited-video formats and Format 02 character-performance registries into their owning category profiles", "each format inherits the correct substrate grammar rather than acting as a cosmetic theme", "Reject cross-category registry reuse, missing character-performance state, and format mappings that claim certification they have not earned."),
    story("ST-06.03", "EP-06", "Compile Category-Native Syntax and Activative Sequencing", "Category steward", "loads category-specific syntax, temporal, conversational, and sequence parsers and compiles adapted Activative Sequencing Intelligence", "shared Activative meaning becomes category-native form without losing frozen rich-object lineage", "Reject generic parser output, sparse tokens without rich references, Activation First violations, and development parsing that invents runtime semantics."),
    story("ST-06.04", "EP-06", "Own Category Runtime, Evaluation, Repair, and Migration Rules", "Category steward", "compiles category-owned runtime, evaluator, repair, atomic ownership, and profile migration contracts", "each category can evolve without silently changing another category or inheriting certification", "Block incompatible profile migration, cross-category repair, missing evaluator ownership, and atomic creative ownership transfer."),
    story("ST-06.05", "EP-06", "Compile the Conversational Expression Feedback Chain", "Conversational category steward", "compiles Activative Calls into Reaction Receipts, Expression Moments, post-expression recompilation, and final Content Type Contract handoffs", "Public Comment, Reply or DM, ReelCast, and Interview profiles are first-class structural outputs while live execution stays external", "Block missing consent authority, scripted guest landings, Reaction Receipt or Expression Moment provenance loss, premature Identity DNA merge, and local Interview product invention."),

    story("ST-07.01", "EP-07", "Register Three Distinct Compilation Targets", "Cross-product architect", "registers versioned Atomic Content Harness, Visual Asset Editor, and Content Asset Delegation Contract profiles", "one control plane can select the correct product outcome without flattening ownership or evidence needs", "Reject unknown targets, multiple targets, universal-profile assumptions, and target records without required extensions or prohibitions."),
    story("ST-07.02", "EP-07", "Compile a Target-Specific Atomic Content Harness", "Harness Architect", "applies content-harness source, IR, Genesis, and category extensions to compile one atomic harness profile", "content-harness output preserves Activative ownership and its category-native contracts", "Block missing category binding, borrowed VAE authority, incomplete source profile, or Genesis decisions copied from another target."),
    story("ST-07.03", "EP-07", "Compile VAE and Delegation Handoffs Without Implementing Them", "Cross-product architect", "compiles VAE and Delegation target profiles plus visual-semantic, Composition Asset Pack, T or V route, and Asset Demand handoffs", "external products receive frozen, typed meaning while Builder stays within compile-validate-handoff ownership", "Block semantic mutation, local external-runtime behavior, incompatible Delegation fields, missing lineage, and unstubbed Release 1 production dependencies."),
    story("ST-07.04", "EP-07", "Validate Target Artifacts, Gates, and Compatibility", "Cross-product reviewer", "compiles target artifact sets and applies target-specific evaluation, authorization, non-flattening, and compatibility checks", "each target can be reviewed and migrated independently with explicit certification scope", "Reject missing artifacts, cross-target field leakage, lossy migrations, unpinned external contracts, and certification inherited from another target."),

    story("ST-08.01", "EP-08", "Measure Behavior Against Controls in Fresh Contexts", "Independent evaluator", "evaluates every skill-system layer with no-guidance controls, repeated fresh-context trials, and adversarial cases", "claimed behavioral improvements are attributable rather than prompt-history artifacts", "Reject non-independent evaluation, missing controls, reused generator context, insufficient repetitions, and cases without protected expected behavior."),
    story("ST-08.02", "EP-08", "Promote Maturity Only Through Protected Receipts", "Evaluation steward", "verifies artifact identity and stores staged benchmark, corpus, and maturity receipts", "only the exact evaluated version can advance toward release", "Block benchmark leakage, artifact hash mismatch, unprotected release cases, missing source authority, and maturity promotion without complete receipts."),
    story("ST-08.03", "EP-08", "Score Independent Dimensions and Controlled Mutations", "Independent evaluator", "runs controlled mutations, category-appropriate scorecards, stability analysis, and downstream result ingestion", "quality dimensions remain visible and non-compensable rather than collapsing into one flattering score", "Reject leaked cases, category-inappropriate rubrics, hidden minimum failures, unstable repeated results, and downstream evidence without identity."),
    story("ST-08.04", "EP-08", "Diagnose Root Cause Before Selecting Repair", "Repair reviewer", "classifies failure and compiles a repair and invalidation graph from root-cause evidence", "repair targets the responsible layer and preserves unaffected upstream truth", "Reject repair-by-symptom, cross-layer mutation, missing failure evidence, and invalidation scopes broader than the demonstrated cause."),
    story("ST-08.05", "EP-08", "Repair Selectively and Rerun Only Affected Regressions", "Repair operator", "applies bounded repair, preserves unaffected state, reruns targeted regressions, and escalates repeated constitutional failures", "the system can improve without restarting validated work or hiding recurring defects", "Block repairs that skip regression, change protected upstream state, exceed retry limits, or suppress escalation after repeated failure."),
    story("ST-08.06", "EP-08", "Issue Evidence-Backed Readiness and Authorization Receipts", "Product authority", "evaluates hard gates and issues full, prototype-only, or blocked authorization with immutable receipts", "implementation teams know exactly what is authorized and why", "Reject false readiness from document completeness, anti-goal violations, missing thresholds, unresolved blockers, and authority outcomes without evidence."),
    story("ST-08.07", "EP-08", "Reject Wrong Readings and Evaluate Conversational Expression", "Conversational evaluation steward", "tests dominant wrong-reading locks and the constitutional conversational dimensions across protected cases", "role clarity, pattern interruption, prediction, payoff, affinity, anticipation, residue, anti-cliche, no-text survival, and rejection remain independently governed", "Block conversational certification while HD-007 thresholds or HD-006 evidence governance remain open, or when one dimension compensates for a hard failure."),

    story("ST-09.01", "EP-09", "Compile an Actor-Explicit Builder Workflow", "Workflow architect", "compiles approved product graphs into versioned Workflow IR nodes, conditions, actors, and profiles", "every request has reproducible routing and explicit responsibility", "Reject missing actors, ambiguous node ownership, graph cycles, undeclared handoffs, and workflow definitions not derived from approved product graphs."),
    story("ST-09.02", "EP-09", "Route Through a Manual Shadow Before Automation", "Builder operator", "routes a request through the selected profile and proves manual-shadow parity before agent automation", "automation begins from observed expert behavior and evaluated phase-local capsules", "Block unmatched profiles, missing manual shadow evidence, agent execution outside evaluated capsules, and deterministic work delegated to an agent."),
    story("ST-09.03", "EP-09", "Validate Node Outputs and Contain Failure Feedback", "Workflow operator", "validates each node and returns structured failure context only to the responsible node under bounded control flow", "failures stay local, diagnosable, and unable to leak invalid output downstream", "Reject unvalidated release, unbounded retries, broad conversational feedback, repair without root cause, and output emitted after a circuit breaker opens."),
    story("ST-09.04", "EP-09", "Checkpoint, Isolate, and Resume Work Safely", "Workflow operator", "checkpoints idempotently, isolates tasks and secrets, grants least privilege, and parallelizes only independent work", "the workflow can resume after failure without duplicating side effects or widening access", "Block unsafe sandbox access, duplicate replay, shared secret leakage, dependency-unsafe parallelism, and recovery that corrupts protected state."),
    story("ST-09.05", "EP-09", "Race Candidates and Route Compute Under Human Authority", "Workflow operator", "uses quality-gated candidate races, risk-aware model routing, independent evaluators, and authority-placed human gates", "compute is spent proportionally while consequential decisions stay human-governed", "Reject winner selection before evaluation, generator-context evaluators, risk-blind model routing, or automation that removes required human gates."),
    story("ST-09.06", "EP-09", "Observe Queues and Prove Workflow Recovery", "Workflow maintainer", "exposes queues and node telemetry and runs end-to-end plus fault-injection recovery tests", "operators can see cost, latency, quality, interventions, and recovery behavior at public seams", "Block hidden budget overflow, missing telemetry, untested failure modes, private-seam-only tests, and recovery claims without fault evidence."),
    story("ST-09.07", "EP-09", "Promote, Migrate, Roll Back, and Hotfix Workflow Profiles", "Release maintainer", "promotes versioned profiles through CI, migration, rollback, incident, and hotfix gates", "workflow changes remain reversible and operationally governed", "Reject promotion without end-to-end and fault tests, incompatible migration, absent rollback, unsigned profile authority, and hotfixes that bypass receipts."),
    story("ST-09.08", "EP-09", "Measure Workflow Outcomes and Reject Monolithic Orchestration", "Workflow maintainer", "measures cost, latency, quality, and intervention while detecting production workflows hidden inside skills or sessions", "the workflow remains an explicit, testable factory rather than an opaque agent prompt", "Block monolithic skill-owned production workflows, hidden state, unbounded self-correction, missing public adapters, and architecture that cannot be replayed."),

    story("ST-10.01", "EP-10", "Open a Trustworthy Run Index and Overview", "Harness Architect", "opens the stable Control Tower shell and selects a run from operational tables into a complete overview", "the current target, category, stage, status, and next governed action are immediately understandable", "Show explicit empty or unavailable state rather than optimistic status when no run or projection exists."),
    story("ST-10.02", "EP-10", "Explore Phase, Context, and Dependency Graphs", "Harness Architect", "navigates phase, context, ownership, and dependency graphs with addressable selections", "the architect can trace what is ready, blocked, upstream, or affected without losing context", "Reject dangling graph navigation, hidden dependency states, inaccessible keyboard traversal, and graph views that invent authority."),
    story("ST-10.03", "EP-10", "Inspect Evidence and Syntax Behind Decisions", "Constitutional reviewer", "opens evidence specimens, source locks, knowledge status, syntax observations, and hypotheses from the run", "every critical claim can be inspected at its originating evidence and parse seam", "Redact unauthorized evidence, show missing or stale projections honestly, and prohibit the UI from upgrading hypotheses into facts."),
    story("ST-10.04", "EP-10", "Review Genesis Decisions and Human Authority", "Product authority", "reviews dependency state, recommendations, answers, final decisions, and receipts and invokes only available human actions", "constitutional authority remains understandable and resumable from the Control Tower", "Block actions without server-described authority, hide no contradiction, and show a conflict instead of overwriting concurrent decisions."),
    story("ST-10.05", "EP-10", "Trace Skills, Recipes, and Runtime Capsules", "Skill maintainer", "inspects canonical skills, local adaptations, recipes, binding versions, evaluators, and capsule manifests", "the maintainer can explain which behavior and context entered a phase", "Show missing evaluator or hash as blocked, distinguish canonical skills from capsules, and never expose secrets or hidden prompt history."),
    story("ST-10.06", "EP-10", "Inspect Ownership, Modules, and Contracts", "Architecture maintainer", "traces capabilities through owners, modules, phases, contracts, and cross-product boundaries", "responsibility and permitted mutation remain clear before change or handoff", "Reject views that merge product ownership, hide contract versions, or allow UI-side edits to authoritative architecture."),
    story("ST-10.07", "EP-10", "Judge Evaluations, Repairs, and Authorization Trajectory", "Independent reviewer", "compares benchmark receipts, hard gates, failures, repair history, and authorization outcomes", "the reviewer can see why readiness advanced, regressed, or remains blocked", "Never render missing thresholds as a pass, never hide failed dimensions, and distinguish prototype-only from production authorization."),
    story("ST-10.08", "EP-10", "Monitor Workflow, Incidents, Cost, and Context", "Builder operator", "monitors workflow queues, nodes, incidents, retries, latency, model usage, and context budgets", "operational pressure and intervention needs are visible before they become silent failure", "Show partial telemetry and disconnection explicitly, flag budget overflow, and prevent hidden retries or parallel work."),
    story("ST-10.09", "EP-10", "Execute Governed Commands and Export Receipts", "Authorized operator", "preflights, confirms, submits, resolves, and exports through server-described typed commands", "human actions remain least-privilege, conflict-aware, and auditable", "Reject unauthorized commands, require confirmation where declared, preserve conflicts, and export only governed redacted evidence with receipts."),
    story("ST-10.10", "EP-10", "Use a Stable, Accessible, Evidence-Backed Shell", "Any authorized Control Tower user", "operates the approved shell through progressive disclosure, keyboard access, honest uncertainty, and responsive continuity", "the Control Tower remains usable without becoming a second source of truth", "Fail accessibility or authority checks rather than hiding controls, fabricating status, or losing addressable context."),
    story("ST-10.11", "EP-10", "Preserve Workspace Context Across Inspectors and Layouts", "Control Tower user", "moves among tables, inspectors, dialogs, notices, and compact layouts while preserving selection and context", "dense operational review stays coherent across screen sizes and interaction modes", "Reject context-destructive navigation, inaccessible dialogs, missing status notices, and compact layouts that hide required authority."),
    story("ST-10.12", "EP-10", "Represent Loading, Empty, Stale, and Disconnected State Honestly", "Control Tower user", "encounters loading, empty, stale, or disconnected projections", "the interface communicates evidence age and availability without optimistic authority", "Never substitute cached success for disconnected truth, hide stale timestamps, or enable commands against unavailable authoritative state."),
    story("ST-10.13", "EP-10", "Contain Partial, Redacted, Failed, and Invalidated Projections", "Control Tower user", "encounters partial, unauthorized, failed, or invalidated data and follows its recovery path", "the interface preserves security and truth while exposing what can be retried or inspected", "Do not leak redacted content, collapse partial state into success, suppress query failure, or retain invalidated projections as current."),
    story("ST-10.14", "EP-10", "Operate Large Collections Within Interaction Budgets", "Control Tower user", "queries and navigates large evidence, event, and run collections under declared budgets", "the interface remains responsive and measurable at Release 1 scale", "Reject unbounded queries, hidden pagination loss, interaction-budget violations, and missing UX telemetry for degraded operations."),

    story("ST-11.01", "EP-11", "Generate a Versioned Traceable Development Capsule", "Implementation lead", "compiles requirements, architecture, contracts, justified scaffolding, examples, fixtures, and acceptance evidence into one capsule", "an implementation team receives complete authority without inventing missing product decisions", "Block incomplete traceability, unjustified scaffolding, missing test fixtures, unresolved contract versions, and capsules without immutable hashes."),
    story("ST-11.02", "EP-11", "Plan Dependency-Ordered Vertical Implementation Increments", "Implementation lead", "derives one working vertical-slice plan and dependency-ordered Stories from the accepted capsule", "implementation can deliver user-observable value without horizontal layer sequencing or future-story dependencies", "Reject stories that exceed one fresh context, depend on future work, omit acceptance evidence, or authorize implementation while readiness is FAIL."),
    story("ST-11.03", "EP-11", "Govern Implementation Deltas and Certification Feedback", "Harness Architect", "ingests implementation discoveries, evaluation results, and certification feedback as typed amendment proposals", "validated authority can evolve without silent drift between planning and implementation", "Block direct mutation of frozen authority, untraceable feedback, incompatible capsule changes, and acceptance of downstream results without artifact identity."),

    story("ST-12.01", "EP-12", "Inventory and Map Proven V2.1 Behavior", "Brownfield maintainer", "inventories repository-local V2.1 capabilities and maps each concept into retain, adapt, replace, or defer evidence", "migration starts from proven assets rather than a greenfield rewrite", "Block migration claims without accessible authoritative artifacts, evidence, owner, or an explicit no-local-baseline disposition."),
    story("ST-12.02", "EP-12", "Dual-Compile and Migrate Through Regression Receipts", "Brownfield maintainer", "dual-compiles eligible targets, applies incremental migration, runs regressions, and emits compatibility and deprecation receipts", "retained behavior changes only through evidence-backed, reversible increments", "Reject lossy aliases, untested deprecation, missing rollback, silent schema drift, and migration that regresses a protected baseline."),
    story("ST-12.03", "EP-12", "Prove the Complete Builder Spine Through Format 02", "Release reviewer", "runs one complete Format 02 reference path from evidence through implementation handoff, evaluation, repair, and certification evidence", "Release 1 demonstrates a coherent vertical product outcome instead of disconnected infrastructure", "Block the reference proof when any required stage, target stub, hard gate, evaluator, or receipt is missing; do not implement in this planning step."),
    story("ST-12.04", "EP-12", "Publish Bounded Certification Claims Across Categories and Targets", "Product authority", "publishes a certification matrix for five categories, four conversational profiles, and three targets", "proven Release 1 scope is explicit while unproven transfer outcomes remain uncertified", "Reject general Builder readiness from one harness, inherited Interview or ReelCast certification, and production claims while any required decision or blocker remains open."),
]


FR_RANGES = [
    (1, 8, "ST-01.01"), (9, 13, "ST-01.02"), (14, 15, "ST-01.03"), (16, 18, "ST-01.04"),
    (19, 23, "ST-02.01"), (24, 27, "ST-02.02"), (28, 31, "ST-02.03"), (32, 35, "ST-02.04"), (36, 40, "ST-02.05"),
    (41, 44, "ST-03.01"), (45, 50, "ST-03.02"), (51, 53, "ST-03.03"), (54, 58, "ST-03.04"), (59, 59, "ST-03.05"),
    (60, 63, "ST-04.01"), (64, 65, "ST-04.02"), (66, 67, "ST-04.03"), (68, 71, "ST-04.04"), (72, 80, "ST-04.05"),
    (81, 83, "ST-05.01"), (84, 86, "ST-05.02"), (87, 90, "ST-05.03"), (91, 99, "ST-05.04"), (100, 102, "ST-05.05"),
    (103, 106, "ST-08.01"), (107, 110, "ST-08.02"), (111, 116, "ST-08.03"),
    (117, 117, "ST-10.01"), (118, 118, "ST-10.02"), (119, 119, "ST-10.03"), (120, 120, "ST-10.04"),
    (121, 121, "ST-10.05"), (122, 122, "ST-10.06"), (123, 123, "ST-10.07"), (124, 124, "ST-10.08"),
    (125, 125, "ST-10.09"), (126, 126, "ST-10.13"),
    (127, 129, "ST-08.04"), (130, 132, "ST-08.05"), (133, 136, "ST-08.06"),
    (137, 141, "ST-06.01"), (142, 144, "ST-06.02"), (145, 147, "ST-06.03"), (148, 150, "ST-06.04"),
    (151, 155, "ST-11.01"), (156, 157, "ST-11.02"), (158, 159, "ST-11.03"),
    (160, 161, "ST-12.01"), (162, 166, "ST-12.02"), (167, 167, "ST-12.03"), (168, 169, "ST-12.04"),
    (170, 170, "ST-07.01"), (171, 171, "ST-07.02"), (172, 173, "ST-07.03"), (174, 176, "ST-07.02"), (177, 180, "ST-07.04"),
    (181, 185, "ST-09.01"), (186, 189, "ST-09.02"), (190, 193, "ST-09.03"), (194, 197, "ST-09.04"),
    (198, 201, "ST-09.05"), (202, 205, "ST-09.06"), (206, 208, "ST-09.07"), (209, 210, "ST-09.08"),
]


UX_ASSIGNMENTS = {
    **{f"UXC-{number:03d}": "ST-10.10" for number in range(1, 11)},
    "UXC-101": "ST-10.01", "UXC-102": "ST-10.01", "UXC-103": "ST-10.02",
    "UXC-104": "ST-10.03", "UXC-105": "ST-10.04", "UXC-106": "ST-10.05",
    "UXC-107": "ST-10.06", "UXC-108": "ST-10.07", "UXC-109": "ST-10.07",
    "UXC-110": "ST-10.08", "UXC-111": "ST-10.08", "UXC-112": "ST-10.09",
    "UXC-113": "ST-10.07", "UXC-201": "ST-10.01", "UXC-202": "ST-10.01",
    "UXC-203": "ST-10.02", "UXC-204": "ST-10.03",
    **{f"UXC-{number:03d}": "ST-10.11" for number in range(205, 210)},
    **{f"UXC-{number:03d}": "ST-10.09" for number in range(301, 308)},
    **{f"UXC-{number:03d}": "ST-10.12" for number in range(401, 405)},
    **{f"UXC-{number:03d}": "ST-10.13" for number in range(405, 409)},
    **{f"UXC-{number:03d}": "ST-10.14" for number in range(501, 505)},
}


OTHER_BY_STORY = {
    "ST-01.01": ["ADR-001", "AG-001", "AG-002", "D001", "D006", "NFR-REL-002", "NFR-SEC-003"],
    "ST-01.02": ["ADR-007", "D005", "NFR-PORT-001", "NFR-SEC-001", "NFR-SEC-002"],
    "ST-01.03": ["NFR-SCALE-001", "NFR-TRACE-004"], "ST-01.04": ["HG-002"],
    "ST-02.01": ["ADR-008"], "ST-02.03": ["AG-006", "AG-007", "D007"], "ST-02.04": ["D008"], "ST-02.05": ["HG-003"],
    "ST-03.01": ["D009", "D010", "HG-001"], "ST-03.02": ["ADR-005", "D002"],
    "ST-03.03": ["ADR-002", "D011", "NFR-COMPAT-002", "NFR-COMPAT-003", "NFR-TRACE-001"],
    "ST-03.04": ["ADR-004", "AG-018", "NFR-MAINT-001", "NFR-REL-001", "NFR-REL-003"], "ST-03.05": ["CONST-001"],
    "ST-04.01": ["D012"], "ST-04.02": ["D015"], "ST-04.03": ["D013"],
    "ST-04.04": ["D014", "NFR-ARCH-001", "HG-004", "HG-005", "HG-007"],
    "ST-04.05": ["AG-012", "AG-013", "D016", "D020"],
    "ST-05.01": ["D021", "NFR-MAINT-002"], "ST-05.02": ["AG-008"], "ST-05.03": ["AG-010", "D017"],
    "ST-05.04": ["ADR-009", "AG-009", "D018", "D019", "HG-006"],
    "ST-06.01": ["AG-003", "AG-004", "CONST-002", "D030", "D031", "NFR-CAT-001", "NFR-CAT-002", "HG-015"],
    "ST-06.02": ["AG-005"], "ST-06.03": ["CONST-003", "CONST-006", "NFR-CAT-003"],
    "ST-06.04": ["NFR-MAINT-003"], "ST-06.05": ["CONST-004"],
    "ST-07.01": ["ADR-013", "D004"], "ST-07.03": ["ADR-018", "CONST-005"],
    "ST-08.01": ["NFR-EVAL-002", "NFR-EVAL-003"],
    "ST-08.02": ["ADR-010", "D022", "D023", "NFR-EVAL-001", "NFR-TRACE-003"],
    "ST-08.03": ["D024", "NFR-EVAL-004", "HG-008"], "ST-08.04": ["AG-014", "D026"],
    "ST-08.06": ["AG-015", "AG-022", "D027", "D033", "HG-009", "HG-010"], "ST-08.07": ["CONST-007", "CONST-008"],
    "ST-09.01": ["ADR-006", "NFR-WORKFLOW-001", "NFR-WORKFLOW-002", "NFR-WORKFLOW-003"],
    "ST-09.02": ["NFR-PORT-002"],
    "ST-09.03": ["AG-020", "NFR-WORKFLOW-004", "NFR-REL-004", "HG-012", "HG-013"],
    "ST-09.04": ["ADR-012", "AG-021", "NFR-SEC-004", "NFR-WORKFLOW-005", "NFR-WORKFLOW-006", "NFR-WORKFLOW-007", "NFR-WORKFLOW-008", "NFR-PERF-004"],
    "ST-09.05": ["AG-011", "NFR-WORKFLOW-009"],
    "ST-09.06": ["NFR-PERF-002", "NFR-PERF-003", "NFR-TEST-001", "NFR-WORKFLOW-010", "NFR-WORKFLOW-011"],
    "ST-09.07": ["ADR-016", "ADR-017", "NFR-WORKFLOW-012", "HG-014"],
    "ST-09.08": ["AG-019", "NFR-ARCH-002", "HG-011"],
    "ST-10.01": ["NFR-PERF-001"], "ST-10.09": ["NFR-OBS-004"], "ST-10.10": ["NFR-UX-001", "NFR-UX-002"],
    "ST-10.12": ["ADR-003", "ADR-011", "D025", "NFR-OBS-001", "NFR-OBS-002", "NFR-OBS-003", "NFR-TRACE-002"],
    "ST-10.13": ["AG-016"], "ST-11.01": ["D029"],
    "ST-12.01": ["ADR-015", "NFR-COMPAT-001"], "ST-12.02": ["D028"],
    "ST-12.03": ["ADR-014", "D003"], "ST-12.04": ["AG-017", "D032"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def refs(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def unique_join(values: list[str]) -> str:
    return ";".join(dict.fromkeys(item for item in values if item))


def implementation_gate_status(gates: list[str], cross_repository_ids: list[str]) -> str:
    if any(gate.startswith("HD-") for gate in gates):
        return "BLOCKED_PENDING_HUMAN_DECISION"
    if any(gate.startswith("BD-") for gate in gates):
        return "EVIDENCE_GATED"
    if any(item != "XDEP-001" for item in cross_repository_ids):
        return "CONDITIONAL_EXTERNAL_DEPENDENCY"
    return "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED"


def release_1_role(story_id: str, epic_id: str) -> str:
    if story_id == "ST-12.03":
        return "FORMAT_02_REFERENCE_PATH_PROOF"
    if story_id == "ST-12.04":
        return "FORMAT_02_CERTIFICATION_SCOPE_AND_GENERAL_DEFERRAL"
    if story_id in {"ST-06.05", "ST-08.07"}:
        return "CONVERSATIONAL_STRUCTURAL_SUPPORT_UNCERTIFIED"
    if epic_id == "EP-07":
        return "THREE_TARGET_STRUCTURAL_SUPPORT_EXTERNAL_RUNTIME_EXCLUDED"
    if epic_id == "EP-11":
        return "IMPLEMENTATION_HANDOFF_PLANNING_ONLY"
    return "RELEASE_1_FORMAT_02_REFERENCE_SUPPORT"


def build_assignment_map() -> dict[str, str]:
    result: dict[str, str] = {}
    for start, end, story_id in FR_RANGES:
        for number in range(start, end + 1):
            inventory_id = f"FR-{number:03d}"
            if inventory_id in result:
                raise ValueError(f"duplicate FR assignment {inventory_id}")
            result[inventory_id] = story_id
    for inventory_id, story_id in UX_ASSIGNMENTS.items():
        if inventory_id in result:
            raise ValueError(f"duplicate UX assignment {inventory_id}")
        result[inventory_id] = story_id
    for story_id, inventory_ids in OTHER_BY_STORY.items():
        for inventory_id in inventory_ids:
            if inventory_id in result:
                raise ValueError(f"duplicate other assignment {inventory_id}")
            result[inventory_id] = story_id
    return result


def main() -> None:
    confirmation = yaml.safe_load(EPIC_CONFIRMATION.read_text(encoding="utf-8"))
    if confirmation.get("status") != "CONFIRMED_STEP_3_AUTHORIZED":
        raise ValueError("Epic inventory is not confirmed for Step 3")

    inventory_rows = read_csv(INVENTORY)
    inventory_by_id = {row["inventory_id"]: row for row in inventory_rows}
    epic_coverage_rows = read_csv(EPIC_COVERAGE)
    epic_coverage_by_id = {row["inventory_id"]: row for row in epic_coverage_rows}
    epic_doc = yaml.safe_load(EPIC_SOURCE.read_text(encoding="utf-8"))
    epic_by_id = {epic["id"]: epic for epic in epic_doc["epics"]}

    story_by_id = {item["id"]: item for item in STORIES}
    assignment = build_assignment_map()
    missing = sorted(set(inventory_by_id) - set(assignment))
    extra = sorted(set(assignment) - set(inventory_by_id))
    if missing or extra:
        raise ValueError(f"Story assignments differ missing={missing} extra={extra}")

    stories_by_epic: dict[str, list[dict[str, str]]] = defaultdict(list)
    for item in STORIES:
        stories_by_epic[item["epic_id"]].append(item)
    last_story_by_epic = {epic_id: items[-1]["id"] for epic_id, items in stories_by_epic.items()}

    primary_ids_by_story: dict[str, list[str]] = defaultdict(list)
    for inventory_id, story_id in assignment.items():
        primary_ids_by_story[story_id].append(inventory_id)

    generated_stories = []
    dependency_rows = []
    previous_story_by_epic: dict[str, str] = {}
    global_order_by_story = {item["id"]: index for index, item in enumerate(STORIES, start=1)}

    for item in STORIES:
        story_id = item["id"]
        epic_id = item["epic_id"]
        epic = epic_by_id[epic_id]
        if epic_id in previous_story_by_epic:
            dependencies = [previous_story_by_epic[epic_id]]
            dependency_reason = "previous vertical increment in the same Epic"
        else:
            dependencies = [last_story_by_epic[dep] for dep in epic["dependencies"]]
            dependency_reason = "terminal increments of prerequisite Epics"
        previous_story_by_epic[epic_id] = story_id

        primary_ids = sorted(primary_ids_by_story[story_id], key=lambda value: list(inventory_by_id).index(value))
        covered_rows = [inventory_by_id[inventory_id] for inventory_id in primary_ids]
        expected_epic_ids = {epic_coverage_by_id[inventory_id]["primary_epic_id"] for inventory_id in primary_ids}
        if expected_epic_ids != {epic_id}:
            raise ValueError(f"{story_id}: assigned requirements cross Epic ownership {sorted(expected_epic_ids)}")

        specs = sorted({spec for row in covered_rows for spec in refs(row["primary_specs"])})
        components = sorted({component for row in covered_rows for component in refs(row["architecture_components"])})
        verification = sorted({ref for row in covered_rows for ref in refs(row["verification_refs"])})
        owners = sorted({row["planning_owner"] for row in covered_rows})
        gates = sorted(
            {gate for row in covered_rows for gate in refs(row["active_blockers"])}
            | {gate for gate in epic["decision_and_blocker_obligations"] if gate.startswith("HD-")}
        )
        fr_ids = [inventory_id for inventory_id in primary_ids if inventory_id.startswith("FR-")]
        nfr_ids = [inventory_id for inventory_id in primary_ids if inventory_id.startswith("NFR-")]
        other_obligations = [
            inventory_id for inventory_id in primary_ids
            if inventory_id not in fr_ids and inventory_id not in nfr_ids
        ]
        cross_repository_ids = list(epic["cross_repository_dependencies"])
        gate_status = implementation_gate_status(gates, cross_repository_ids)
        contract_profile = EPIC_CONTRACTS_AND_SCHEMAS[epic_id]
        default = EPIC_DEFAULTS[epic_id]
        generated_stories.append({
            "story_id": story_id,
            "global_order": global_order_by_story[story_id],
            "epic_id": epic_id,
            "epic_title": epic["title"],
            "title": item["title"],
            "primary_outcome": item["value"],
            "narrative": {
                "as_a": item["actor"],
                "i_want": item["intent"],
                "so_that": item["value"],
            },
            "dependencies": dependencies,
            "prerequisites": {
                "story_receipts": [f"{dependency}:StoryCompletionReceipt" for dependency in dependencies],
                "decision_or_blocker_ids": gates,
                "cross_repository_dependency_ids": cross_repository_ids,
                "authority_sources": ["Builder PRD V1.2", "Activative Intelligence Constitution V1.1"],
            },
            "release_1_disposition": epic["release_1_disposition"],
            "release_1_role": release_1_role(story_id, epic_id),
            "primary_obligation_ids": primary_ids,
            "primary_obligation_count": len(primary_ids),
            "relevant_requirements": {
                "fr_ids": fr_ids,
                "nfr_ids": nfr_ids,
                "other_planning_obligation_ids": other_obligations,
            },
            "implementation_owners": owners,
            "component_boundary": default["boundary"],
            "affected_contracts_and_schemas": {
                "contract_ids_or_planned_handles": contract_profile["contracts"],
                "schema_refs": contract_profile["schemas"],
                "schema_disposition": "Documentation-time or planned contract boundary only; no production schema implementation is authorized by Step 3.",
            },
            "contracts_and_seams": {
                "primary_specs": specs,
                "architecture_components": components,
                "verification_refs": verification,
                "test_seam": default["test"],
            },
            "failure_behavior": item["failure"],
            "authority_behavior": "Only the declared human, agent, code, or external owner may perform each covered action; all listed gates remain unresolved unless separately ratified.",
            "observability": "Emit or preserve story-scoped events and receipts with run, artifact, authority, version, provenance, outcome, and failure context.",
            "observability_evidence": {
                "required_fields": ["run_id", "story_id", "artifact_identity", "authority_identity", "version", "provenance", "outcome", "failure_context"],
                "success_evidence": f"{story_id}:OutcomeVerified",
                "failure_evidence": f"{story_id}:OutcomeRejected",
                "receipt_link": f"{story_id}:StoryCompletionReceipt",
            },
            "migration_or_compatibility": default["compatibility"],
            "gate_refs": gates,
            "implementation_gate_status": gate_status,
            "cross_product_boundary": {
                "builder_scope": "compile, validate, evaluate, project, and hand off Builder-owned contracts only",
                "external_dependency_ids": cross_repository_ids,
                "prohibited_builder_implementation": [
                    "Visual Asset Editor production behavior",
                    "Delegation Protocol production behavior or shared-contract ownership",
                    "Interview Expression or ReelCast live product behavior before its own approved PRD",
                ],
            },
            "acceptance_criteria": [
                f"Given all dependency outputs for {story_id} are accepted and the covered authority is available,",
                f"When the {item['actor']} {item['action']},",
                f"Then {item['value']}",
                f"And failure behavior is explicit: {item['failure']}",
                "And only declared authority may approve or mutate governed state; unresolved gates remain blocking where applicable.",
                "And events, receipts, evidence identity, version, provenance, and failure context are observable at the declared public seam.",
                f"And compatibility behavior is enforced: {default['compatibility']}",
            ],
            "test_plan": {
                "public_seam": default["test"],
                "required_tests": [
                    {"test_id": f"{story_id}-acceptance", "kind": "vertical_acceptance", "assertion": item["value"]},
                    {"test_id": f"{story_id}-failure", "kind": "negative_contract", "assertion": item["failure"]},
                    {"test_id": f"{story_id}-authority", "kind": "authority_boundary", "assertion": "unauthorized approval or mutation fails closed"},
                    {"test_id": f"{story_id}-receipt", "kind": "observability_and_receipt", "assertion": "success and failure evidence is attributable and receipt-linked"},
                ],
            },
            "completion_receipt": {
                "receipt_type": "StoryCompletionReceipt",
                "receipt_id_template": f"{story_id}:StoryCompletionReceipt:<artifact-hash>",
                "current_status": "PLANNED_NOT_ISSUED",
                "required_evidence": ["dependency receipts", "Given/When/Then results", "required test results", "observability evidence", "gate disposition", "artifact and contract hashes"],
                "issuance_rule": "Issue only after every acceptance criterion and required test passes and every blocking or conditional dependency has an authoritative disposition.",
            },
            "fresh_context_scope": f"One independently testable {item['title']} increment covering {len(primary_ids)} primary obligations; no production implementation is authorized by this plan.",
        })
        dependency_rows.append({
            "story_id": story_id,
            "global_order": global_order_by_story[story_id],
            "epic_id": epic_id,
            "dependency_story_ids": ";".join(dependencies),
            "dependency_orders": ";".join(str(global_order_by_story[dep]) for dep in dependencies),
            "backward_only": str(all(global_order_by_story[dep] < global_order_by_story[story_id] for dep in dependencies)).lower(),
            "dependency_reason": dependency_reason,
            "prerequisite_receipt_ids": ";".join(f"{dependency}:StoryCompletionReceipt" for dependency in dependencies),
            "decision_or_blocker_ids": ";".join(gates),
            "cross_repository_dependency_ids": ";".join(cross_repository_ids),
            "implementation_gate_status": gate_status,
        })

    story_doc = {
        "schema_version": "cmf-builder-vertical-story-inventory/v2",
        "status": "PROPOSED_AWAITING_HUMAN_CONFIRMATION",
        "step": 3,
        "created_on": "2026-07-14",
        "authority": {
            "builder_prd": "1.2",
            "activative_intelligence_constitution": "1.1",
            "confirmed_epic_receipt": "docs/planning/EPIC_INVENTORY_CONFIRMATION_RECEIPT.yaml",
        },
        "planning_boundary": {
            "story_authoring_completed": True,
            "step_4_authorized": False,
            "production_implementation_authorized": False,
            "implementation_readiness": "FAIL",
            "next_gate": "human_confirmation_before_step_4_coverage_and_readiness_validation",
        },
        "story_count": len(generated_stories),
        "primary_obligation_assignments": len(assignment),
        "stories": generated_stories,
    }
    STORY_INVENTORY.write_text(yaml.safe_dump(story_doc, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
    generated_story_by_id = {item["story_id"]: item for item in generated_stories}

    coverage_columns = [
        "inventory_id", "authority_type", "title", "primary_epic_id", "primary_story_id", "story_title",
        "source_release_scope", "story_release_disposition", "story_release_1_role", "primary_specs", "active_blockers",
        "gate_refs", "story_implementation_gate_status", "completion_receipt", "assignment_basis",
    ]
    coverage_rows = []
    for inventory_row in inventory_rows:
        inventory_id = inventory_row["inventory_id"]
        story_id = assignment[inventory_id]
        story_item = story_by_id[story_id]
        generated_story = generated_story_by_id[story_id]
        epic = epic_by_id[story_item["epic_id"]]
        gates = sorted(set(refs(inventory_row["active_blockers"])) | {g for g in epic["decision_and_blocker_obligations"] if g.startswith("HD-")})
        coverage_rows.append({
            "inventory_id": inventory_id,
            "authority_type": inventory_row["authority_type"],
            "title": inventory_row["title"],
            "primary_epic_id": story_item["epic_id"],
            "primary_story_id": story_id,
            "story_title": story_item["title"],
            "source_release_scope": inventory_row["release_scope"],
            "story_release_disposition": epic["release_1_disposition"],
            "story_release_1_role": generated_story["release_1_role"],
            "primary_specs": inventory_row["primary_specs"],
            "active_blockers": inventory_row["active_blockers"],
            "gate_refs": ";".join(gates),
            "story_implementation_gate_status": generated_story["implementation_gate_status"],
            "completion_receipt": generated_story["completion_receipt"]["receipt_id_template"],
            "assignment_basis": "vertical decomposition within confirmed primary Epic responsibility",
        })
    with STORY_COVERAGE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=coverage_columns)
        writer.writeheader()
        writer.writerows(coverage_rows)

    with STORY_DEPENDENCIES.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(dependency_rows[0]))
        writer.writeheader()
        writer.writerows(dependency_rows)

    gated_story_ids = [
        item["story_id"] for item in generated_stories
        if item["implementation_gate_status"] != "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED"
    ]
    blocked_doc = {
        "schema_version": "cmf-builder-story-blocked-conditional-register/v1",
        "status": "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED",
        "implementation_readiness": "FAIL",
        "entry_count": len(gated_story_ids),
        "entries": [
            {
                "story_id": item["story_id"],
                "epic_id": item["epic_id"],
                "title": item["title"],
                "classification": item["implementation_gate_status"],
                "decision_or_blocker_ids": item["gate_refs"],
                "cross_repository_dependency_ids": item["prerequisites"]["cross_repository_dependency_ids"],
                "effect": "Planning may continue; Story implementation and completion-receipt issuance remain prohibited or conditional.",
                "resolution_authority": "Only the named human decision owner, blocker evidence owner, or external repository owner may change this state.",
            }
            for item in generated_stories if item["story_id"] in gated_story_ids
        ],
        "planning_complete_but_implementation_prohibited_story_ids": [
            item["story_id"] for item in generated_stories
            if item["implementation_gate_status"] == "PLANNING_COMPLETE_IMPLEMENTATION_PROHIBITED"
        ],
    }
    STORY_BLOCKED.write_text(yaml.safe_dump(blocked_doc, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")

    release_1_doc = {
        "schema_version": "cmf-builder-release-1-story-subset/v1",
        "status": "PLANNED_NOT_IMPLEMENTATION_AUTHORIZED",
        "certified_reference_path": "Format 02",
        "reference_path_proof_story": "ST-12.03",
        "certification_scope_story": "ST-12.04",
        "release_1_story_count": len(generated_stories),
        "release_1_story_ids": [item["story_id"] for item in generated_stories],
        "by_release_role": {
            role: [item["story_id"] for item in generated_stories if item["release_1_role"] == role]
            for role in sorted({item["release_1_role"] for item in generated_stories})
        },
        "certification_boundaries": {
            "format_02": "reference path planned; future certification requires implementation and evidence",
            "conversational_activation": "structural support only; no inherited certification",
            "interview_expression": "structural target-profile support only pending its own approved PRD",
            "reelcast_expression": "structural target-profile support only pending owning-product authority",
            "visual_asset_editor": "contract-tested external handoff only; production behavior externally owned",
            "delegation_protocol": "shared contracts and production runtime externally owned",
        },
        "implementation_authorized": False,
        "implementation_readiness": "FAIL",
    }
    STORY_RELEASE_1.write_text(yaml.safe_dump(release_1_doc, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")

    dependency_consumers = []
    for dependency in epic_doc["cross_repository_dependencies"]:
        dependency_id = dependency["id"]
        consuming_epics = [
            epic["id"] for epic in epic_doc["epics"]
            if dependency_id in epic["cross_repository_dependencies"]
        ]
        consuming_stories = [
            item["story_id"] for item in generated_stories
            if item["epic_id"] in consuming_epics
        ]
        dependency_consumers.append({
            **dependency,
            "consuming_epic_ids": consuming_epics,
            "consuming_story_ids": consuming_stories,
            "builder_boundary": CROSS_REPOSITORY_BOUNDARIES[dependency_id],
            "implementation_effect": "CONDITIONAL_OR_EVIDENCE_GATED; planning may continue but no external product behavior is implemented here.",
        })
    cross_repository_doc = {
        "schema_version": "cmf-builder-story-cross-repository-dependencies/v1",
        "status": "REGISTERED_NOT_IMPLEMENTED",
        "dependency_count": len(dependency_consumers),
        "dependencies": dependency_consumers,
        "external_product_implementation_stories": [],
        "boundary_validation": "PASS",
    }
    STORY_CROSS_REPOSITORY.write_text(
        yaml.safe_dump(cross_repository_doc, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8"
    )

    sections = []
    grouped_sections = []
    for epic in epic_doc["epics"]:
        epic_stories = [item for item in generated_stories if item["epic_id"] == epic["id"]]
        story_sections = []
        for item in epic_stories:
            narrative = item["narrative"]
            criteria = "\n".join(f"- {criterion}" for criterion in item["acceptance_criteria"])
            story_sections.append(f"""### {item['story_id']} — {item['title']}

As a **{narrative['as_a']}**, I want to **{narrative['i_want']}**, so that **{narrative['so_that']}**

- Global order: `{item['global_order']}`
- Dependencies: {', '.join(f'`{dep}`' for dep in item['dependencies']) if item['dependencies'] else 'None'}
- Primary outcome: {item['primary_outcome']}
- Primary obligations ({item['primary_obligation_count']}): {', '.join(f'`{req}`' for req in item['primary_obligation_ids'])}
- Relevant FRs: {', '.join(f'`{req}`' for req in item['relevant_requirements']['fr_ids']) if item['relevant_requirements']['fr_ids'] else 'None'}
- Relevant NFRs: {', '.join(f'`{req}`' for req in item['relevant_requirements']['nfr_ids']) if item['relevant_requirements']['nfr_ids'] else 'None'}
- Release 1 disposition: `{item['release_1_disposition']}`
- Release 1 role: `{item['release_1_role']}`
- Implementation owners: {', '.join(f'`{owner}`' for owner in item['implementation_owners'])}
- Component boundary: {item['component_boundary']}
- Affected contracts: {', '.join(f'`{contract}`' for contract in item['affected_contracts_and_schemas']['contract_ids_or_planned_handles'])}
- Affected schemas: {', '.join(f'`{schema}`' for schema in item['affected_contracts_and_schemas']['schema_refs']) if item['affected_contracts_and_schemas']['schema_refs'] else 'None; planned contract shapes remain owned by the cited technical specifications'}
- Primary specifications: {', '.join(f'`{spec}`' for spec in item['contracts_and_seams']['primary_specs'])}
- Test seam: {item['contracts_and_seams']['test_seam']}
- Gate references: {', '.join(f'`{gate}`' for gate in item['gate_refs']) if item['gate_refs'] else 'None'}
- Implementation gate status: `{item['implementation_gate_status']}`
- Failure behavior: {item['failure_behavior']}
- Observability evidence: `{item['observability_evidence']['success_evidence']}`, `{item['observability_evidence']['failure_evidence']}`
- Required tests: {', '.join(f"`{test['test_id']}`" for test in item['test_plan']['required_tests'])}
- Completion receipt: `{item['completion_receipt']['receipt_id_template']}` (`{item['completion_receipt']['current_status']}`)
- Migration or compatibility: {item['migration_or_compatibility']}
- Fresh-context scope: {item['fresh_context_scope']}

Acceptance criteria:

{criteria}
""")
        sections.append(f"""## {epic['id']} — {epic['title']}

**Epic outcome:** {epic['outcome']}

**Story count:** {len(epic_stories)}

{chr(10).join(story_sections)}
""")
        grouped_rows = [
            "| Story | Primary outcome | Prerequisite Stories | Obligations | Gate state | Release 1 role | Completion receipt |",
            "|---|---|---|---:|---|---|---|",
        ]
        for item in epic_stories:
            dependencies = ", ".join(item["dependencies"]) if item["dependencies"] else "None"
            outcome = item["primary_outcome"].replace("|", "\\|")
            grouped_rows.append(
                f"| `{item['story_id']}` {item['title']} | {outcome} | {dependencies} | {item['primary_obligation_count']} | "
                f"`{item['implementation_gate_status']}` | `{item['release_1_role']}` | `{item['completion_receipt']['receipt_id_template']}` |"
            )
        grouped_sections.append(
            f"## {epic['id']} — {epic['title']}\n\n{epic['outcome']}\n\n" + "\n".join(grouped_rows)
        )

    grouped_inventory = f"""# Builder V1.2 Story Inventory Grouped by Epic

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

- Stories: {len(generated_stories)}
- Primary obligation assignments: {len(assignment)}
- Step 4: `NOT_AUTHORIZED`
- Production implementation: `PROHIBITED_READINESS_FAIL`

{chr(10).join(grouped_sections)}
"""
    STORY_GROUPED.write_text(grouped_inventory, encoding="utf-8")

    proposal = f"""# Builder V1.2 Vertical Story Design Proposal

Status: `PROPOSED_AWAITING_HUMAN_CONFIRMATION`

Step: `3 — Vertical Story authoring`

Authority: confirmed 12-Epic Builder V1.2 design under Activative Intelligence Constitution V1.1.

- Stories: {len(generated_stories)}
- Confirmed obligations assigned to a primary Story: {len(assignment)}
- Story dependencies: backward-only by construction
- Step 4 coverage/readiness validation: not authorized
- Production implementation: prohibited while readiness is `FAIL`

Every Story is a complete, independently testable vertical increment sized for one fresh development-agent context. Stories preserve confirmed Epic ownership, use only earlier dependencies, carry unresolved human decisions and blockers, and do not implement Visual Asset Editor, Delegation Protocol, Interview Expression, or ReelCast product runtimes.

{chr(10).join(sections)}

## Step boundary

- Vertical Story proposal: `AWAITING_HUMAN_CONFIRMATION`.
- Step 4 full coverage and implementation-readiness validation: `NOT_AUTHORIZED`.
- Production implementation: `PROHIBITED_READINESS_FAIL`.
- Next action: human confirms or corrects the Story inventory before Step 4 begins.
"""
    STORY_PROPOSAL.write_text(proposal, encoding="utf-8")


if __name__ == "__main__":
    main()
