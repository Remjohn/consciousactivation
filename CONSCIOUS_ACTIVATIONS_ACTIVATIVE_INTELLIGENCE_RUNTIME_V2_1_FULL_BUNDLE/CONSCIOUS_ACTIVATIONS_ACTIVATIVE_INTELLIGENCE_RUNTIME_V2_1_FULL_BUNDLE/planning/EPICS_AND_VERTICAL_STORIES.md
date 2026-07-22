# Activative Intelligence Runtime V2.1 — Value-Based Epics and CBAR-Hardened Vertical Stories

**Version:** `2.1.0-draft`  
**Status:** `DRAFT_FOR_HUMAN_RATIFICATION`  
**Epics:** 15  
**Stories:** 60  
**Primary FR coverage:** 120/120

These Epics are organized by user and product value rather than technical layers. Every Story owns exactly two Functional Requirements and includes primary, denial, recovery, CBAR, and downstream-proof acceptance.

## AIR-EP-01 — Know What the System May Believe

**Value:** Every semantic claim enters the system with an explicit activation domain, epistemic state, version, owner, and lifecycle consequence.

**Entry state:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.

**Terminal state:** A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt.

**Product boundaries:** Activative Intelligence Runtime, Program Control

**Primary features:** F01

### AIR-ST-01.01 — Establish activation-domain and truth-state authority

**Story:** As an Activative Intelligence operator, I want to establish activation-domain and truth-state authority, so that Every semantic claim enters the system with an explicit activation domain, epistemic state, version, owner, and lifecycle consequence.

**Primary FRs:** `AIR-FR-001`, `AIR-FR-002`

**Entry:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.

**Terminal:** A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt.

**Primary acceptance**

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the operator completes establish activation-domain and truth-state authority
- **Then** Every activative program and semantic object shall declare exactly one primary activation domain—source, relationship, audience, campaign, or derivative—and may reference other domains only through typed handoffs and Every material field shall declare whether it is planned, observed, inferred, operator-confirmed, rejected, or superseded instead of inheriting one undifferentiated object status
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or a planned, inferred, rejected, or superseded field is presented without its exact epistemic state
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-008` Attack Problem Not Person: Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. conflicts with the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **UX failure scenario:** a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every activative program and semantic object shall declare exactly one primary activation domain—source, relationship, audience, campaign, or derivative—and may reference other domains only through typed handoffs and Every material field shall declare whether it is planned, observed, inferred, operator-confirmed, rejected, or superseded instead of inheriting one undifferentiated object status, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-01.02 expects exact outputs from this Story. If the mandate is absent, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile)

### AIR-ST-01.02 — Version semantic decisions without rewriting history

**Story:** As an Activative Intelligence operator, I want to version semantic decisions without rewriting history, so that Every semantic claim enters the system with an explicit activation domain, epistemic state, version, owner, and lifecycle consequence.

**Primary FRs:** `AIR-FR-003`, `AIR-FR-004`

**Entry:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.

**Terminal:** A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt.

**Primary acceptance**

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the operator completes version semantic decisions without rewriting history
- **Then** Semantic changes shall create immutable successor versions with explicit supersession and invalidation edges; prior versions remain replayable and The Runtime shall reject any transition that treats a Brief, hypothesis, intended role, or planned tag as evidence that a human expression or audience reaction occurred
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or a planned, inferred, rejected, or superseded field is presented without its exact epistemic state
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-003` Intent Governs Style: Subordinate all stylistic choices to the specific communication intent of the artifact. conflicts with the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **UX failure scenario:** a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Semantic changes shall create immutable successor versions with explicit supersession and invalidation edges; prior versions remain replayable and The Runtime shall reject any transition that treats a Brief, hypothesis, intended role, or planned tag as evidence that a human expression or audience reaction occurred, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-01.03 expects exact outputs from this Story. If the mandate is absent, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile)

### AIR-ST-01.03 — Prove lifecycle and epistemology claims

**Story:** As an Activative Intelligence operator, I want to prove lifecycle and epistemology claims, so that Every semantic claim enters the system with an explicit activation domain, epistemic state, version, owner, and lifecycle consequence.

**Primary FRs:** `AIR-FR-005`, `AIR-FR-006`

**Entry:** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.

**Terminal:** A versioned semantic object exists with one domain, field-level epistemic states, lineage, lifecycle status, and a non-compensable evaluation receipt.

**Primary acceptance**

- **Given** A source, relationship, audience, or campaign request introduces a semantic claim or a change to an existing claim.
- **When** the operator completes prove lifecycle and epistemology claims
- **Then** Every handoff between source, relationship, audience, campaign, and derivative activation shall preserve the originating objects, transformations, and authority boundaries and Independent evaluation shall verify domain fit, epistemic correctness, lifecycle legality, and claim ceiling before a semantic object becomes eligible downstream
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to collapse one object-level status across fields so implementation becomes simpler.
- **UX failure scenario:** a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every handoff between source, relationship, audience, campaign, and derivative activation shall preserve the originating objects, transformations, and authority boundaries and Independent evaluation shall verify domain fit, epistemic correctness, lifecycle legality, and claim ceiling before a semantic object becomes eligible downstream, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-02.01 expects exact outputs from this Story. If the mandate is absent, a planned assertion is presented downstream as observed human truth, corrupting every later activation and evaluation claim
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-001` (Activative Intelligence Lifecycle Constitution V2), `SRC-AHP-001` (AHP PRD V1.2 primitive/archetype-centered combined PRD), `SRC-DOCTRINE-001` (Current Conscious Activations writing and doctrine profile)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-02 — Surface the Real Identity Pressure and Edge

**Value:** The Runtime forms a source-backed broad signal and Edge Product from real identity, audience, interviewer, and relationship context without mutating human-owned identity truth.

**Entry state:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.

**Terminal state:** The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation.

**Product boundaries:** Activative Intelligence Runtime, Human profile authority, Interview Expression

**Primary features:** F02

### AIR-ST-02.01 — Assemble identity, audience, interviewer, and relationship context

**Story:** As an Activative Intelligence operator, I want to assemble identity, audience, interviewer, and relationship context, so that The Runtime forms a source-backed broad signal and Edge Product from real identity, audience, interviewer, and relationship context without mutating human-owned identity truth.

**Primary FRs:** `AIR-FR-007`, `AIR-FR-008`

**Entry:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.

**Terminal:** The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation.

**Primary acceptance**

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the operator completes assemble identity, audience, interviewer, and relationship context
- **Then** The Runtime shall resolve exact Identity DNA, Brand Context Version, Brand Genesis Session, Voice DNA, and Visual DNA references required by the current activation objective and The Runtime shall represent the audience situation, self-perception, pressure, desired movement, probable defenses, and relationship stage as a versioned Context Premise
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative or the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **UX failure scenario:** the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall resolve exact Identity DNA, Brand Context Version, Brand Genesis Session, Voice DNA, and Visual DNA references required by the current activation objective and The Runtime shall represent the audience situation, self-perception, pressure, desired movement, probable defenses, and relationship stage as a versioned Context Premise, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-02.02 expects exact outputs from this Story. If the mandate is absent, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### AIR-ST-02.02 — Compile Matrix broad signal and survived Edge Product

**Story:** As an Activative Intelligence operator, I want to compile Matrix broad signal and survived Edge Product, so that The Runtime forms a source-backed broad signal and Edge Product from real identity, audience, interviewer, and relationship context without mutating human-owned identity truth.

**Primary FRs:** `AIR-FR-009`, `AIR-FR-010`

**Entry:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.

**Terminal:** The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation.

**Primary acceptance**

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the operator completes compile matrix broad signal and survived edge product
- **Then** Source activation shall include the interviewer’s real resonance, lived stake, curiosity, and current relationship context when those conditions materially affect the guest response and The Matrix compiler shall intersect guest truth, audience reality, interviewer or relationship resonance, and current objective to produce a broad signal before edge candidates are ranked
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-008` Attack Problem Not Person: Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. conflicts with the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **UX failure scenario:** the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Source activation shall include the interviewer’s real resonance, lived stake, curiosity, and current relationship context when those conditions materially affect the guest response and The Matrix compiler shall intersect guest truth, audience reality, interviewer or relationship resonance, and current objective to produce a broad signal before edge candidates are ranked, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-02.03 expects exact outputs from this Story. If the mandate is absent, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### AIR-ST-02.03 — Propose Identity DNA candidate observations without mutation

**Story:** As an Activative Intelligence operator, I want to propose Identity DNA candidate observations without mutation, so that The Runtime forms a source-backed broad signal and Edge Product from real identity, audience, interviewer, and relationship context without mutating human-owned identity truth.

**Primary FRs:** `AIR-FR-011`, `AIR-FR-012`

**Entry:** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.

**Terminal:** The Runtime emits a source-backed broad signal, candidate pressures, survived edges, and identity observations with exact epistemic state and no direct Identity DNA mutation.

**Primary acceptance**

- **Given** An operator selects a guest, coach, audience, interviewer, relationship stage, or source objective.
- **When** the operator completes propose identity dna candidate observations without mutation
- **Then** The Runtime shall form an Edge Product only from edges that survive source evidence, identity fit, counteractivation analysis, and the relevant planned or observed state and The Runtime may emit evidence-linked Identity DNA candidate observations from repeated or strong expression, but canonical Identity DNA changes require a separate operator resolution
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-015` The What Is / What Could Be Contrast Engine: Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. conflicts with the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival.
- **UX failure scenario:** the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall form an Edge Product only from edges that survive source evidence, identity fit, counteractivation analysis, and the relevant planned or observed state and The Runtime may emit evidence-linked Identity DNA candidate observations from repeated or strong expression, but canonical Identity DNA changes require a separate operator resolution, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-03.01 expects exact outputs from this Story. If the mandate is absent, the interview pressure misses the guest’s actual identity layer and produces polished but non-revealing answers
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-03 — Compare Activation Paths Before Convergence

**Value:** Operators and downstream programs compare meaningfully different activation strategies before one direction becomes the planned program.

**Entry state:** A broad signal, objective, and eligible source context are available.

**Terminal state:** A selected activation hypothesis is promoted into a planned program, while rejected and repaired candidates remain evidence.

**Product boundaries:** Activative Intelligence Runtime, Independent evaluation

**Primary features:** F03

### AIR-ST-03.01 — Generate meaningfully different activation hypotheses

**Story:** As an Activative Intelligence operator, I want to generate meaningfully different activation hypotheses, so that Operators and downstream programs compare meaningfully different activation strategies before one direction becomes the planned program.

**Primary FRs:** `AIR-FR-013`, `AIR-FR-014`

**Entry:** A broad signal, objective, and eligible source context are available.

**Terminal:** A selected activation hypothesis is promoted into a planned program, while rejected and repaired candidates remain evidence.

**Primary acceptance**

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the operator completes generate meaningfully different activation hypotheses
- **Then** The Runtime shall generate multiple eligible activation hypotheses that differ in psychological role, tension, direction, pressure path, primitive coalition, or relationship move rather than merely surface wording and Source fidelity, epistemic legality, identity fit, domain fit, operator constraints, and fatal primitive conflicts shall remove ineligible hypotheses before comparative scoring
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to accept the first fluent hypothesis and skip comparative search.
- **UX failure scenario:** the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall generate multiple eligible activation hypotheses that differ in psychological role, tension, direction, pressure path, primitive coalition, or relationship move rather than merely surface wording and Source fidelity, epistemic legality, identity fit, domain fit, operator constraints, and fatal primitive conflicts shall remove ineligible hypotheses before comparative scoring, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-03.02 expects exact outputs from this Story. If the mandate is absent, the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-002` (Integrated Activative Intelligence V2 Product Requirements), `SRC-AHP-PORTFOLIO-001` (AHP adaptive candidate search feature), `SRC-CBAR-001` (CBAR Epic and Story Hardening Skill), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-03.02 — Compare candidates under non-compensable gates

**Story:** As an Activative Intelligence operator, I want to compare candidates under non-compensable gates, so that Operators and downstream programs compare meaningfully different activation strategies before one direction becomes the planned program.

**Primary FRs:** `AIR-FR-015`, `AIR-FR-016`

**Entry:** A broad signal, objective, and eligible source context are available.

**Terminal:** A selected activation hypothesis is promoted into a planned program, while rejected and repaired candidates remain evidence.

**Primary acceptance**

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the operator completes compare candidates under non-compensable gates
- **Then** Eligible hypotheses shall be compared against the current source, audience, relationship stage, desired state transition, counteractivation risk, freshness, and downstream derivative potential and The portfolio shall retain rejected, superseded, and repaired candidates with exact reasons, responsible layers, and possible future applicability
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the responsible layer is unknown or the proposed repair would regenerate valid upstream work
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-015` The What Is / What Could Be Contrast Engine: Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. conflicts with the shortcut to accept the first fluent hypothesis and skip comparative search.
- **UX failure scenario:** the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Eligible hypotheses shall be compared against the current source, audience, relationship stage, desired state transition, counteractivation risk, freshness, and downstream derivative potential and The portfolio shall retain rejected, superseded, and repaired candidates with exact reasons, responsible layers, and possible future applicability, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-03.03 expects exact outputs from this Story. If the mandate is absent, the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-002` (Integrated Activative Intelligence V2 Product Requirements), `SRC-AHP-PORTFOLIO-001` (AHP adaptive candidate search feature), `SRC-CBAR-001` (CBAR Epic and Story Hardening Skill), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-03.03 — Converge while preserving rejections and stopping evidence

**Story:** As an Activative Intelligence operator, I want to converge while preserving rejections and stopping evidence, so that Operators and downstream programs compare meaningfully different activation strategies before one direction becomes the planned program.

**Primary FRs:** `AIR-FR-017`, `AIR-FR-018`

**Entry:** A broad signal, objective, and eligible source context are available.

**Terminal:** A selected activation hypothesis is promoted into a planned program, while rejected and repaired candidates remain evidence.

**Primary acceptance**

- **Given** A broad signal, objective, and eligible source context are available.
- **When** the operator completes converge while preserving rejections and stopping evidence
- **Then** Search shall stop on a decisive eligible winner, shared defect, exhausted diversity, budget boundary, or operator-owned ambiguity rather than arbitrary iteration count and Promotion shall create a new Planned Activative Intelligence object that references the complete portfolio and evaluation receipt without erasing alternatives
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or a planned, inferred, rejected, or superseded field is presented without its exact epistemic state
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-HUM-021` Irony Inversion: Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. conflicts with the shortcut to accept the first fluent hypothesis and skip comparative search.
- **UX failure scenario:** the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Search shall stop on a decisive eligible winner, shared defect, exhausted diversity, budget boundary, or operator-owned ambiguity rather than arbitrary iteration count and Promotion shall create a new Planned Activative Intelligence object that references the complete portfolio and evaluation receipt without erasing alternatives, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-04.01 expects exact outputs from this Story. If the mandate is absent, the system converges on a cliché direction and loses alternative roles, tensions, and edges that could have activated more strongly
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-AI2-002` (Integrated Activative Intelligence V2 Product Requirements), `SRC-AHP-PORTFOLIO-001` (AHP adaptive candidate search feature), `SRC-CBAR-001` (CBAR Epic and Story Hardening Skill), `SRC-MOE-001` (Matrix of Edging)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-04 — Build Evidence-Bound Primitive Recipes

**Value:** The Runtime grounds activation in exact Meaning-Plane and Experience-Plane primitives rather than generic creative advice. The Runtime compiles primitive coalitions that function as the true recipe builders for activation, scripts, composition, and evaluation.

**Entry state:** A selected activation hypothesis and current stage require a concrete behavioral recipe.

**Terminal state:** A validated coalition, signature, Edge Product, misuse profile, and recipe eligibility package are available for archetype and script compilation.

**Product boundaries:** Activative Intelligence Runtime, Independent evaluation, Primitive coalition authority, Primitive registry authority

**Primary features:** F04, F05

### AIR-ST-04.01 — Query the real primitive registries

**Story:** As an Activative Intelligence operator, I want to query the real primitive registries, so that The Runtime grounds activation in exact Meaning-Plane and Experience-Plane primitives rather than generic creative advice.

**Primary FRs:** `AIR-FR-019`, `AIR-FR-020`

**Entry:** A selected activation hypothesis and current stage require a concrete behavioral recipe.

**Terminal:** Every required behavior is bound to exact primitive versions, stage-local applications, suppression rules, and evidence.

**Primary acceptance**

- **Given** A selected activation hypothesis and current stage require a concrete behavioral recipe.
- **When** the operator completes query the real primitive registries
- **Then** Every primitive query and binding shall declare whether the primitive creates meaning or shapes the participant experience, and cross-plane relationships shall be explicit and The Runtime shall resolve primitive identifiers, versions, family, source registry, applicability, misuse risks, and supersession state before coalition compilation
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-BUS-001` Perception and Guidance Stack: Design visuals, text hierarchy, and action cues as one integrated system that controls where the eye goes and what the hand does next. conflicts with the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts.
- **UX failure scenario:** the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every primitive query and binding shall declare whether the primitive creates meaning or shapes the participant experience, and cross-plane relationships shall be explicit and The Runtime shall resolve primitive identifiers, versions, family, source registry, applicability, misuse risks, and supersession state before coalition compilation, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-04.02 expects exact outputs from this Story. If the mandate is absent, the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-04.02 — Bind exact primitives to the current activation state

**Story:** As an Activative Intelligence operator, I want to bind exact primitives to the current activation state, so that The Runtime grounds activation in exact Meaning-Plane and Experience-Plane primitives rather than generic creative advice.

**Primary FRs:** `AIR-FR-021`, `AIR-FR-022`

**Entry:** A selected activation hypothesis and current stage require a concrete behavioral recipe.

**Terminal:** Every required behavior is bound to exact primitive versions, stage-local applications, suppression rules, and evidence.

**Primary acceptance**

- **Given** A selected activation hypothesis and current stage require a concrete behavioral recipe.
- **When** the operator completes bind exact primitives to the current activation state
- **Then** A Primitive Binding shall connect one primitive to a target object, stage, role, tension, intended effect, execution surface, evidence, and allowed adaptation and Bindings shall expose primitives that reinforce, suppress, contradict, or become fatal with one another under the current objective
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-BUS-006` Hierarchy as Attention Routing: Assign distinct, uncompetitive visual weights to different semantic roles in the content, ensuring the viewer's eye is routed exactly where it needs to go, in the exact order it needs to go there. conflicts with the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts.
- **UX failure scenario:** the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A Primitive Binding shall connect one primitive to a target object, stage, role, tension, intended effect, execution surface, evidence, and allowed adaptation and Bindings shall expose primitives that reinforce, suppress, contradict, or become fatal with one another under the current objective, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-04.03 expects exact outputs from this Story. If the mandate is absent, the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-04.03 — Prove stage-appropriate primitive coverage and conflicts

**Story:** As an Activative Intelligence operator, I want to prove stage-appropriate primitive coverage and conflicts, so that The Runtime grounds activation in exact Meaning-Plane and Experience-Plane primitives rather than generic creative advice.

**Primary FRs:** `AIR-FR-023`, `AIR-FR-024`

**Entry:** A selected activation hypothesis and current stage require a concrete behavioral recipe.

**Terminal:** Every required behavior is bound to exact primitive versions, stage-local applications, suppression rules, and evidence.

**Primary acceptance**

- **Given** A selected activation hypothesis and current stage require a concrete behavioral recipe.
- **When** the operator completes prove stage-appropriate primitive coverage and conflicts
- **Then** The Runtime shall verify that source activation, script formation, composition, experience, and evaluation stages receive the primitive coverage required by the current archetype and category and Every accepted binding shall record registry identity, selected version, applicability rationale, source evidence, exclusions, and downstream consumers
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts.
- **UX failure scenario:** the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall verify that source activation, script formation, composition, experience, and evaluation stages receive the primitive coverage required by the current archetype and category and Every accepted binding shall record registry identity, selected version, applicability rationale, source evidence, exclusions, and downstream consumers, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-05.01 expects exact outputs from this Story. If the mandate is absent, the selected primitive behaves differently from the assumed name and injects an incompatible core move into the program
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-05.01 — Compile a complete Primitive Coalition Contract

**Story:** As an Activative Intelligence operator, I want to compile a complete Primitive Coalition Contract, so that The Runtime compiles primitive coalitions that function as the true recipe builders for activation, scripts, composition, and evaluation.

**Primary FRs:** `AIR-FR-025`, `AIR-FR-026`

**Entry:** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.

**Terminal:** A validated coalition, signature, Edge Product, misuse profile, and recipe eligibility package are available for archetype and script compilation.

**Primary acceptance**

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the operator completes compile a complete primitive coalition contract
- **Then** A Primitive Coalition Contract shall classify every bound primitive by functional role and state why the coalition requires or excludes it and The Runtime shall derive a versioned Coalition Signature that identifies the coalition’s distinctive activation geometry across source, script, composition, and experience
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-002` Tension-and-Release Narrative Engine: Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. conflicts with the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **UX failure scenario:** the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A Primitive Coalition Contract shall classify every bound primitive by functional role and state why the coalition requires or excludes it and The Runtime shall derive a versioned Coalition Signature that identifies the coalition’s distinctive activation geometry across source, script, composition, and experience, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-05.02 expects exact outputs from this Story. If the mandate is absent, the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging), `SRC-AHP-F29-001` (AHP F29 primitive-first coalition composition and evaluation)

### AIR-ST-05.02 — Resolve Coalition Signature and Edge Product

**Story:** As an Activative Intelligence operator, I want to resolve Coalition Signature and Edge Product, so that The Runtime compiles primitive coalitions that function as the true recipe builders for activation, scripts, composition, and evaluation.

**Primary FRs:** `AIR-FR-027`, `AIR-FR-028`

**Entry:** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.

**Terminal:** A validated coalition, signature, Edge Product, misuse profile, and recipe eligibility package are available for archetype and script compilation.

**Primary acceptance**

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the operator completes resolve coalition signature and edge product
- **Then** The Runtime shall test fatal conflicts, overload, misuse modes, anti-patterns, and role collapse before the coalition becomes eligible and The coalition shall emit an Edge Product that states the distinctive pressure, role, tension, and usable creative consequence produced by the survived combination
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-009` The McKee Inciting Incident Engine: Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. conflicts with the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **UX failure scenario:** the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall test fatal conflicts, overload, misuse modes, anti-patterns, and role collapse before the coalition becomes eligible and The coalition shall emit an Edge Product that states the distinctive pressure, role, tension, and usable creative consequence produced by the survived combination, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-05.03 expects exact outputs from this Story. If the mandate is absent, the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging), `SRC-AHP-F29-001` (AHP F29 primitive-first coalition composition and evaluation)

### AIR-ST-05.03 — Promote evidence into Steering Recipes and Primitive Evaluation Receipts

**Story:** As an Activative Intelligence operator, I want to promote evidence into Steering Recipes and Primitive Evaluation Receipts, so that The Runtime compiles primitive coalitions that function as the true recipe builders for activation, scripts, composition, and evaluation.

**Primary FRs:** `AIR-FR-029`, `AIR-FR-030`

**Entry:** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.

**Terminal:** A validated coalition, signature, Edge Product, misuse profile, and recipe eligibility package are available for archetype and script compilation.

**Primary acceptance**

- **Given** Eligible Primitive Bindings exist for a selected hypothesis or derivative program.
- **When** the operator completes promote evidence into steering recipes and primitive evaluation receipts
- **Then** A Steering Recipe candidate shall reference the coalition, applicability envelope, intervention, preserved properties, evidence, failures, and rollback rather than free-floating taste instructions and Independent evaluation shall report primitive presence, function, interactions, misuse, coalition integrity, Edge Product fidelity, and failure attribution
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-015` The What Is / What Could Be Contrast Engine: Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. conflicts with the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation.
- **UX failure scenario:** the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A Steering Recipe candidate shall reference the coalition, applicability envelope, intervention, preserved properties, evidence, failures, and rollback rather than free-floating taste instructions and Independent evaluation shall report primitive presence, function, interactions, misuse, coalition integrity, Edge Product fidelity, and failure attribution, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-06.01 expects exact outputs from this Story. If the mandate is absent, the coalition contains individually useful primitives that fight each other, flatten the Edge Product, or create a misuse mode
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-PRIM-001` (Meaning Primitive Registry specification), `SRC-PRIM-002` (Experience Primitive Registry specification), `SRC-PRIM-003` (CMF full primitive YAML snapshot), `SRC-MOE-001` (Matrix of Edging), `SRC-AHP-F29-001` (AHP F29 primitive-first coalition composition and evaluation)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-05 — Give the Viewer a Psychological Role Inside a Tension

**Value:** Every content or relationship program gives the participant a specific psychological role inside a source-backed tension and organizes that activation through an eligible archetype coalition.

**Entry state:** A validated Edge Product and current activation domain are available.

**Terminal state:** The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry.

**Product boundaries:** Activative Intelligence Runtime, Archetype registry authority, Human creative authority

**Primary features:** F06

### AIR-ST-06.01 — Route the Edge Product into a supported archetype

**Story:** As an Activative Intelligence operator, I want to route the Edge Product into a supported archetype, so that Every content or relationship program gives the participant a specific psychological role inside a source-backed tension and organizes that activation through an eligible archetype coalition.

**Primary FRs:** `AIR-FR-031`, `AIR-FR-032`

**Entry:** A validated Edge Product and current activation domain are available.

**Terminal:** The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry.

**Primary acceptance**

- **Given** A validated Edge Product and current activation domain are available.
- **When** the operator completes route the edge product into a supported archetype
- **Then** The Runtime shall select or propose a Core Content Archetype only when its interaction geometry fits the Edge Product, source evidence, audience state, and intended movement and Each derivative shall declare its content archetype, asset derivative route, category, and route scope instead of inheriting a generic content type
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **UX failure scenario:** the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall select or propose a Core Content Archetype only when its interaction geometry fits the Edge Product, source evidence, audience state, and intended movement and Each derivative shall declare its content archetype, asset derivative route, category, and route scope instead of inheriting a generic content type, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-06.02 expects exact outputs from this Story. If the mandate is absent, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition)

### AIR-ST-06.02 — Define the psychological role inside the tension

**Story:** As an Activative Intelligence operator, I want to define the psychological role inside the tension, so that Every content or relationship program gives the participant a specific psychological role inside a source-backed tension and organizes that activation through an eligible archetype coalition.

**Primary FRs:** `AIR-FR-033`, `AIR-FR-034`

**Entry:** A validated Edge Product and current activation domain are available.

**Terminal:** The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry.

**Primary acceptance**

- **Given** A validated Edge Product and current activation domain are available.
- **When** the operator completes define the psychological role inside the tension
- **Then** Every audience- or relationship-facing program shall name the role the person is invited to inhabit, the tension that makes the role meaningful, and the action or recognition the role enables and When more than one archetype is used, the Runtime shall declare primary, supporting, transition, and excluded archetypes and prevent geometry conflict or centroid blending
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension or a proposed Primitive is unresolved to its exact YAML, conflicts with another binding, or has an unaddressed misuse mode
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-002` Tension-and-Release Narrative Engine: Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. conflicts with the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **UX failure scenario:** the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every audience- or relationship-facing program shall name the role the person is invited to inhabit, the tension that makes the role meaningful, and the action or recognition the role enables and When more than one archetype is used, the Runtime shall declare primary, supporting, transition, and excluded archetypes and prevent geometry conflict or centroid blending, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-06.03 expects exact outputs from this Story. If the mandate is absent, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- exact Primitive YAML hashes, bindings, compatibility decisions, misuse risks, Coalition Signature, and Primitive Evaluation Receipt

**Sources:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition)

### AIR-ST-06.03 — Lock archetype coalition geometry and route evidence

**Story:** As an Activative Intelligence operator, I want to lock archetype coalition geometry and route evidence, so that Every content or relationship program gives the participant a specific psychological role inside a source-backed tension and organizes that activation through an eligible archetype coalition.

**Primary FRs:** `AIR-FR-035`, `AIR-FR-036`

**Entry:** A validated Edge Product and current activation domain are available.

**Terminal:** The program has an eligible archetype coalition, explicit viewer or participant role, tension, SDA/SFL route, and operator-reviewable geometry.

**Primary acceptance**

- **Given** A validated Edge Product and current activation domain are available.
- **When** the operator completes lock archetype coalition geometry and route evidence
- **Then** The archetype program shall resolve the applicable Story Design Archetype and Story Function Layer references required to preserve narrative function and derivative routing and The accepted route shall record Edge Product fit, role/tension contract, coalition structure, alternatives rejected, source lineage, and approval state
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-HUM-021` Irony Inversion: Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. conflicts with the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension.
- **UX failure scenario:** the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The archetype program shall resolve the applicable Story Design Archetype and Story Function Layer references required to preserve narrative function and derivative routing and The accepted route shall record Edge Product fit, role/tension contract, coalition structure, alternatives rejected, source lineage, and approval state, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-07.01 expects exact outputs from this Story. If the mandate is absent, the viewer receives information but no role, tension, or participation position, so the asset remains descriptive rather than activative
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

**Sources:** `SRC-ARCH-001` (CCP Archetype System Migration Proposition), `SRC-ARCH-002` (CMF archetype prompt evidence snapshot), `SRC-SDA-001` (CMF SDA registry snapshot), `SRC-SFL-001` (CMF SFL registry snapshot), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-06 — Ground the Guest Voice and Visual World Without Centroid Drift

**Value:** The Runtime preserves the guest’s living expression and brand organism while distilling it into category-native scripts and visual programs without centroid collapse.

**Entry state:** A source-backed expression, coalition, and archetype route require translation into a script or visual program.

**Terminal state:** The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence.

**Product boundaries:** Activative Intelligence Runtime, Brand profile authority, Human creative authority

**Primary features:** F07

### AIR-ST-07.01 — Lock active Brand Context, Voice DNA, and Visual DNA

**Story:** As an Activative Intelligence operator, I want to lock active Brand Context, Voice DNA, and Visual DNA, so that The Runtime preserves the guest’s living expression and brand organism while distilling it into category-native scripts and visual programs without centroid collapse.

**Primary FRs:** `AIR-FR-037`, `AIR-FR-038`

**Entry:** A source-backed expression, coalition, and archetype route require translation into a script or visual program.

**Terminal:** The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence.

**Primary acceptance**

- **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
- **When** the operator completes lock active brand context, voice dna, and visual dna
- **Then** Every brand-bearing source, script, or visual program shall reference the active Brand Context Version and its originating Brand Genesis Session and Writers and composers shall use Voice DNA to preserve cadence, vocabulary, stance, rhetorical movement, and credible emotional range while retaining transformation lineage
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative or the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VOC-009` Sensory Scene Anchoring: Use vivid sensory cues to build the theater of the mind for the listener. conflicts with the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence.
- **UX failure scenario:** the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every brand-bearing source, script, or visual program shall reference the active Brand Context Version and its originating Brand Genesis Session and Writers and composers shall use Voice DNA to preserve cadence, vocabulary, stance, rhetorical movement, and credible emotional range while retaining transformation lineage, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-07.02 expects exact outputs from this Story. If the mandate is absent, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid)

### AIR-ST-07.02 — Distill source signal through RSCS layers

**Story:** As an Activative Intelligence operator, I want to distill source signal through RSCS layers, so that The Runtime preserves the guest’s living expression and brand organism while distilling it into category-native scripts and visual programs without centroid collapse.

**Primary FRs:** `AIR-FR-039`, `AIR-FR-040`

**Entry:** A source-backed expression, coalition, and archetype route require translation into a script or visual program.

**Terminal:** The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence.

**Primary acceptance**

- **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
- **When** the operator completes distill source signal through rscs layers
- **Then** Visual programs shall bind Visual DNA tokens, recurring operators, exclusions, reference families, and composition tendencies without allowing Visual DNA to override the current role and tension and Every transformed script or semantic program shall record the sequence of signal extraction, compression, simplification, and re-expression used to preserve the Edge Product
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-003` Intent Governs Style: Subordinate all stylistic choices to the specific communication intent of the artifact. conflicts with the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence.
- **UX failure scenario:** the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Visual programs shall bind Visual DNA tokens, recurring operators, exclusions, reference families, and composition tendencies without allowing Visual DNA to override the current role and tension and Every transformed script or semantic program shall record the sequence of signal extraction, compression, simplification, and re-expression used to preserve the Edge Product, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-07.03 expects exact outputs from this Story. If the mandate is absent, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid)

### AIR-ST-07.03 — Generate controlled variation while protecting Negative Space and Edge Integrity

**Story:** As an Activative Intelligence operator, I want to generate controlled variation while protecting Negative Space and Edge Integrity, so that The Runtime preserves the guest’s living expression and brand organism while distilling it into category-native scripts and visual programs without centroid collapse.

**Primary FRs:** `AIR-FR-041`, `AIR-FR-042`

**Entry:** A source-backed expression, coalition, and archetype route require translation into a script or visual program.

**Terminal:** The translated program has active brand references, a traceable distillation path, controlled variation, Voice/Visual DNA conformance, and anti-centroid evidence.

**Primary acceptance**

- **Given** A source-backed expression, coalition, and archetype route require translation into a script or visual program.
- **When** the operator completes generate controlled variation while protecting negative space and edge integrity
- **Then** Variation shall occur within declared combinatorial dimensions and preserve source fidelity, coalition function, archetype geometry, and brand identity rather than producing unconstrained alternatives and Independent evaluation shall verify that negative space performs its intended attention or participation function and that the result has not converged toward a generic centroid
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-021` Punctum, Air, and Felt Truth: During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. conflicts with the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence.
- **UX failure scenario:** the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Variation shall occur within declared combinatorial dimensions and preserve source fidelity, coalition function, archetype geometry, and brand identity rather than producing unconstrained alternatives and Independent evaluation shall verify that negative space performs its intended attention or participation function and that the result has not converged toward a generic centroid, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-08.01 expects exact outputs from this Story. If the mandate is absent, the output sounds and looks like a generic high-performing content centroid rather than the guest’s credible world
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-RSCS-001` (RSCS Recursive Signal Compression Systems), `SRC-CCV-001` (CCV Combinatorial Controlled Variation), `SRC-AHP-F30-001` (AHP F30 Brand Genesis Voice/Visual DNA and anti-centroid)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-07 — Prepare an Adaptive Source-Activation Session

**Value:** An interview is planned around the human expression and derivative asset the system intends to make possible, not around an isolated list of questions.

**Entry state:** A selected source-activation hypothesis and interview objective exist.

**Terminal state:** A validated Planned AIP and one or more Interview Asset Contracts are armed for live execution with explicit states, anchors, branches, dose, and landing rules.

**Product boundaries:** Activative Intelligence Runtime, Human interview authority, Interview Expression

**Primary features:** F08

### AIR-ST-08.01 — Compile the Planned Activative Intelligence Pack

**Story:** As an Activative Intelligence operator, I want to compile the Planned Activative Intelligence Pack, so that An interview is planned around the human expression and derivative asset the system intends to make possible, not around an isolated list of questions.

**Primary FRs:** `AIR-FR-043`, `AIR-FR-044`

**Entry:** A selected source-activation hypothesis and interview objective exist.

**Terminal:** A validated Planned AIP and one or more Interview Asset Contracts are armed for live execution with explicit states, anchors, branches, dose, and landing rules.

**Primary acceptance**

- **Given** A selected source-activation hypothesis and interview objective exist.
- **When** the operator completes compile the planned activative intelligence pack
- **Then** The Runtime shall compile the selected hypothesis, broad signal, intended state transitions, roles, pressures, directions, coalition, archetype hypotheses, evidence expectations, and limitations into a versioned Planned AIP and Every intended interview asset shall have a contract that defines the desired expression, source premise, edge pressure, anchors, question program, branches, landing, and route hypotheses
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-009` The McKee Inciting Incident Engine: Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. conflicts with the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract.
- **UX failure scenario:** the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall compile the selected hypothesis, broad signal, intended state transitions, roles, pressures, directions, coalition, archetype hypotheses, evidence expectations, and limitations into a versioned Planned AIP and Every intended interview asset shall have a contract that defines the desired expression, source premise, edge pressure, anchors, question program, branches, landing, and route hypotheses, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-08.02 expects exact outputs from this Story. If the mandate is absent, the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-CONTRACT-001` (AI2 Interview Asset Contract)

### AIR-ST-08.02 — Create complete Interview Asset Contracts

**Story:** As an Activative Intelligence operator, I want to create complete Interview Asset Contracts, so that An interview is planned around the human expression and derivative asset the system intends to make possible, not around an isolated list of questions.

**Primary FRs:** `AIR-FR-045`, `AIR-FR-046`

**Entry:** A selected source-activation hypothesis and interview objective exist.

**Terminal:** A validated Planned AIP and one or more Interview Asset Contracts are armed for live execution with explicit states, anchors, branches, dose, and landing rules.

**Primary acceptance**

- **Given** A selected source-activation hypothesis and interview objective exist.
- **When** the operator completes create complete interview asset contracts
- **Then** The contract shall name the expression state expected at entry, the target state, observable transition signals, and conditions that make the target inappropriate and The contract shall specify the opening anchor that exposes the premise and the depth anchor that moves from a competent answer toward lived expression
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-002` Tension-and-Release Narrative Engine: Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. conflicts with the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract.
- **UX failure scenario:** the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The contract shall name the expression state expected at entry, the target state, observable transition signals, and conditions that make the target inappropriate and The contract shall specify the opening anchor that exposes the premise and the depth anchor that moves from a competent answer toward lived expression, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-08.03 expects exact outputs from this Story. If the mandate is absent, the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-CONTRACT-001` (AI2 Interview Asset Contract)

### AIR-ST-08.03 — Validate adaptive branches, dose, landing, and route hypotheses

**Story:** As an Activative Intelligence operator, I want to validate adaptive branches, dose, landing, and route hypotheses, so that An interview is planned around the human expression and derivative asset the system intends to make possible, not around an isolated list of questions.

**Primary FRs:** `AIR-FR-047`, `AIR-FR-048`

**Entry:** A selected source-activation hypothesis and interview objective exist.

**Terminal:** A validated Planned AIP and one or more Interview Asset Contracts are armed for live execution with explicit states, anchors, branches, dose, and landing rules.

**Primary acceptance**

- **Given** A selected source-activation hypothesis and interview objective exist.
- **When** the operator completes validate adaptive branches, dose, landing, and route hypotheses
- **Then** The contract shall include bounded follow-ups for anchor hit, partial hit, defense, topic escape, contradiction, overload, and relational reset and The contract shall state what counts as a landed answer, when to stop, which asset routes become eligible, and which planned routes must remain unconfirmed until observed evidence exists
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-008` Attack Problem Not Person: Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. conflicts with the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract.
- **UX failure scenario:** the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The contract shall include bounded follow-ups for anchor hit, partial hit, defense, topic escape, contradiction, overload, and relational reset and The contract shall state what counts as a landed answer, when to stop, which asset routes become eligible, and which planned routes must remain unconfirmed until observed evidence exists, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-09.01 expects exact outputs from this Story. If the mandate is absent, the interviewer has no state-aware branch when the guest partially lands, resists, or reveals an unexpected edge
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-CONTRACT-001` (AI2 Interview Asset Contract)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-08 — Conduct and Observe Live Source Activation

**Value:** The live interview adapts to the guest’s actual state instead of following a static script while preserving human interviewer authority. Human reaction, non-reaction, and wrong reaction become typed multimodal evidence rather than a vague interpretation attached after the session.

**Entry state:** An armed Interview Asset Contract enters a live or simulated source-activation session.

**Terminal state:** A Reaction Receipt classifies the outcome, binds evidence spans, records uncertainty and planned–observed deltas, and becomes eligible for Expression Moment resolution.

**Product boundaries:** Activative Intelligence Runtime, Human interviewer, Independent reaction evaluator, Interview Expression

**Primary features:** F09, F10

### AIR-ST-09.01 — Maintain an evidence-bearing live state

**Story:** As an Activative Intelligence operator, I want to maintain an evidence-bearing live state, so that The live interview adapts to the guest’s actual state instead of following a static script while preserving human interviewer authority.

**Primary FRs:** `AIR-FR-049`, `AIR-FR-050`

**Entry:** An armed Interview Asset Contract enters a live or simulated source-activation session.

**Terminal:** Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction.

**Primary acceptance**

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the operator completes maintain an evidence-bearing live state
- **Then** The Runtime shall update current expression state, target distance, anchor status, observed signals, pressure history, relationship condition, and available next actions after each meaningful event and The live state shall preserve the interviewer’s genuine reaction, curiosity, recognition, uncertainty, or stake when it changes the next useful call
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-008` Attack Problem Not Person: Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. conflicts with the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **UX failure scenario:** pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall update current expression state, target distance, anchor status, observed signals, pressure history, relationship condition, and available next actions after each meaningful event and The live state shall preserve the interviewer’s genuine reaction, curiosity, recognition, uncertainty, or stake when it changes the next useful call, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-09.02 expects exact outputs from this Story. If the mandate is absent, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines)

### AIR-ST-09.02 — Propose bounded next Activative Calls and pressure dose

**Story:** As an Activative Intelligence operator, I want to propose bounded next Activative Calls and pressure dose, so that The live interview adapts to the guest’s actual state instead of following a static script while preserving human interviewer authority.

**Primary FRs:** `AIR-FR-051`, `AIR-FR-052`

**Entry:** An armed Interview Asset Contract enters a live or simulated source-activation session.

**Terminal:** Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction.

**Primary acceptance**

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the operator completes propose bounded next activative calls and pressure dose
- **Then** The Runtime shall propose a bounded next call linked to the active Interview Asset Contract, observed state, expected transition, and stopping law and Each call shall declare its pressure dose, expected gain, overload risk, and available relief or affinity-reset path
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **UX failure scenario:** pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall propose a bounded next call linked to the active Interview Asset Contract, observed state, expected transition, and stopping law and Each call shall declare its pressure dose, expected gain, overload risk, and available relief or affinity-reset path, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-09.03 expects exact outputs from this Story. If the mandate is absent, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines)

### AIR-ST-09.03 — Land, reset, or stop without forcing the intended premise

**Story:** As an Activative Intelligence operator, I want to land, reset, or stop without forcing the intended premise, so that The live interview adapts to the guest’s actual state instead of following a static script while preserving human interviewer authority.

**Primary FRs:** `AIR-FR-053`, `AIR-FR-054`

**Entry:** An armed Interview Asset Contract enters a live or simulated source-activation session.

**Terminal:** Each call and state transition is recorded; the session lands, resets, or stops with a truthful explanation and no fabricated reaction.

**Primary acceptance**

- **Given** An armed Interview Asset Contract enters a live or simulated source-activation session.
- **When** the operator completes land, reset, or stop without forcing the intended premise
- **Then** The Runtime shall identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, or performative agreement and adjust the policy accordingly and The Runtime shall make the available transition explicit and shall not continue merely to exhaust a prepared question list
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-009` The McKee Inciting Incident Engine: Begin the narrative at the specific moment the status quo is disrupted, forcing the protagonist into action to restore balance. conflicts with the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer.
- **UX failure scenario:** pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall identify probable denial, reactance, shame shutdown, projection, tribal defense, topic escape, or performative agreement and adjust the policy accordingly and The Runtime shall make the available transition explicit and shall not continue merely to exhaust a prepared question list, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-10.01 expects exact outputs from this Story. If the mandate is absent, pressure becomes performative or coercive, the guest closes, and the prepared path destroys the expression opportunity
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing), `SRC-MOE-001` (Matrix of Edging), `SRC-AI2-LIVE-001` (AI2 lifecycle state machines)

### AIR-ST-10.01 — Capture multimodal reaction evidence

**Story:** As an Activative Interview operator, I want to capture multimodal reaction evidence, so that Human reaction, non-reaction, and wrong reaction become typed multimodal evidence rather than a vague interpretation attached after the session.

**Primary FRs:** `AIR-FR-055`, `AIR-FR-056`

**Entry:** A live source-activation call or source segment produces observable human behavior.

**Terminal:** A Reaction Receipt classifies the outcome, binds evidence spans, records uncertainty and planned–observed deltas, and becomes eligible for Expression Moment resolution.

**Primary acceptance**

- **Given** A live source-activation call or source segment produces observable human behavior.
- **When** the operator completes capture multimodal reaction evidence
- **Then** The system shall align transcript, word timing, silence, audio events, facial and body keyframes, gaze, posture, self-correction, contradiction, and reaction-tail observations where available and Reaction outcomes shall include anchor hit, partial hit, unexpected edge, state transition, flat answer, defensive reaction, topic escape, silence, contradiction, landing reached, and activation null
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence.
- **UX failure scenario:** a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The system shall align transcript, word timing, silence, audio events, facial and body keyframes, gaze, posture, self-correction, contradiction, and reaction-tail observations where available and Reaction outcomes shall include anchor hit, partial hit, unexpected edge, state transition, flat answer, defensive reaction, topic escape, silence, contradiction, landing reached, and activation null, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-10.02 expects exact outputs from this Story. If the mandate is absent, a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-REACTION-001` (AI2 Reaction Observation and Receipt contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### AIR-ST-10.02 — Classify reactions, non-reactions, and counteractivation

**Story:** As an Activative Interview operator, I want to classify reactions, non-reactions, and counteractivation, so that Human reaction, non-reaction, and wrong reaction become typed multimodal evidence rather than a vague interpretation attached after the session.

**Primary FRs:** `AIR-FR-057`, `AIR-FR-058`

**Entry:** A live source-activation call or source segment produces observable human behavior.

**Terminal:** A Reaction Receipt classifies the outcome, binds evidence spans, records uncertainty and planned–observed deltas, and becomes eligible for Expression Moment resolution.

**Primary acceptance**

- **Given** A live source-activation call or source segment produces observable human behavior.
- **When** the operator completes classify reactions, non-reactions, and counteractivation
- **Then** When the intended pressure produces no meaningful transition, the system shall record activation null or partial activation rather than manufacture an Anchor Hit and A Reaction Receipt shall bind the triggering call, source spans, observation evidence, outcome, confidence, counteractivation, and evaluator identity
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence.
- **UX failure scenario:** a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must When the intended pressure produces no meaningful transition, the system shall record activation null or partial activation rather than manufacture an Anchor Hit and A Reaction Receipt shall bind the triggering call, source spans, observation evidence, outcome, confidence, counteractivation, and evaluator identity, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-10.03 expects exact outputs from this Story. If the mandate is absent, a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-REACTION-001` (AI2 Reaction Observation and Receipt contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### AIR-ST-10.03 — Issue Reaction Receipts and planned–observed deltas

**Story:** As an Activative Interview operator, I want to issue Reaction Receipts and planned–observed deltas, so that Human reaction, non-reaction, and wrong reaction become typed multimodal evidence rather than a vague interpretation attached after the session.

**Primary FRs:** `AIR-FR-059`, `AIR-FR-060`

**Entry:** A live source-activation call or source segment produces observable human behavior.

**Terminal:** A Reaction Receipt classifies the outcome, binds evidence spans, records uncertainty and planned–observed deltas, and becomes eligible for Expression Moment resolution.

**Primary acceptance**

- **Given** A live source-activation call or source segment produces observable human behavior.
- **When** the operator completes issue reaction receipts and planned–observed deltas
- **Then** The Runtime shall compare expected state, role, edge, and asset route with what actually emerged and preserve both the match and the mismatch and An evaluator separate from the call proposer shall test evidence sufficiency, outcome fit, alternative interpretations, and the maximum supported claim
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-021` Punctum, Air, and Felt Truth: During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. conflicts with the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence.
- **UX failure scenario:** a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall compare expected state, role, edge, and asset route with what actually emerged and preserve both the match and the mismatch and An evaluator separate from the call proposer shall test evidence sufficiency, outcome fit, alternative interpretations, and the maximum supported claim, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-11.01 expects exact outputs from this Story. If the mandate is absent, a flat or defensive answer is misclassified as an Anchor Hit and promoted as source evidence
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-REACTION-001` (AI2 Reaction Observation and Receipt contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-09 — Resolve a Trusted Source-Expression Root

**Value:** The system resolves complete, source-backed expression moments and compiles what actually emerged into an Observed Activative Intelligence Pack. Brief-led interviews and imported interviews become equally usable derivative roots without inventing absent planning history.

**Entry state:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.

**Terminal state:** A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives.

**Product boundaries:** Activative Intelligence Runtime, Activative Intelligence Runtime consumer, Human expression authority, Interview Expression, Operator source authority

**Primary features:** F11, F12

### AIR-ST-11.01 — Discover and bound complete Expression Moments

**Story:** As an Activative Interview operator, I want to discover and bound complete Expression Moments, so that The system resolves complete, source-backed expression moments and compiles what actually emerged into an Observed Activative Intelligence Pack.

**Primary FRs:** `AIR-FR-061`, `AIR-FR-062`

**Entry:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.

**Terminal:** Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not.

**Primary acceptance**

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the operator completes discover and bound complete expression moments
- **Then** The system shall use transcript, Reaction Receipts, audio events, keyframes, planned context, observed tags, and source continuity to propose moment candidates and Candidate boundaries shall include the minimum source context needed to prevent quote collapse, preserve the cause of the expression, and retain the relevant reaction tail
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VOC-009` Sensory Scene Anchoring: Use vivid sensory cues to build the theater of the mind for the listener. conflicts with the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **UX failure scenario:** a line becomes quotable only because its qualifying premise and emotional tail were removed The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The system shall use transcript, Reaction Receipts, audio events, keyframes, planned context, observed tags, and source continuity to propose moment candidates and Candidate boundaries shall include the minimum source context needed to prevent quote collapse, preserve the cause of the expression, and retain the relevant reaction tail, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-11.02 expects exact outputs from this Story. If the mandate is absent, a line becomes quotable only because its qualifying premise and emotional tail were removed
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing)

### AIR-ST-11.02 — Resolve moment lifecycle and routeability

**Story:** As an Activative Interview operator, I want to resolve moment lifecycle and routeability, so that The system resolves complete, source-backed expression moments and compiles what actually emerged into an Observed Activative Intelligence Pack.

**Primary FRs:** `AIR-FR-063`, `AIR-FR-064`

**Entry:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.

**Terminal:** Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not.

**Primary acceptance**

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the operator completes resolve moment lifecycle and routeability
- **Then** The resolver shall evaluate completeness, specificity, identity signal, pressure survival, emotional or cognitive turn, audiovisual usability, and eligible derivative routes and Candidates shall move through proposed, observed, borderline, approved, rejected, superseded, and revoked states with immutable decisions and evidence
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-021` Punctum, Air, and Felt Truth: During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. conflicts with the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **UX failure scenario:** a line becomes quotable only because its qualifying premise and emotional tail were removed The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The resolver shall evaluate completeness, specificity, identity signal, pressure survival, emotional or cognitive turn, audiovisual usability, and eligible derivative routes and Candidates shall move through proposed, observed, borderline, approved, rejected, superseded, and revoked states with immutable decisions and evidence, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-11.03 expects exact outputs from this Story. If the mandate is absent, a line becomes quotable only because its qualifying premise and emotional tail were removed
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing)

### AIR-ST-11.03 — Compile the Observed Activative Intelligence Pack

**Story:** As an Activative Interview operator, I want to compile the Observed Activative Intelligence Pack, so that The system resolves complete, source-backed expression moments and compiles what actually emerged into an Observed Activative Intelligence Pack.

**Primary FRs:** `AIR-FR-065`, `AIR-FR-066`

**Entry:** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.

**Terminal:** Approved, rejected, or borderline Expression Moments and an Observed AIP truthfully summarize what emerged and what did not.

**Primary acceptance**

- **Given** Reaction Receipts, transcript, source media, keyframes, tags, and session context are available.
- **When** the operator completes compile the observed activative intelligence pack
- **Then** The Runtime shall compile actual roles, directions, pressures, urges, edges, primitive and archetype evidence, reactions, limitations, and planned–observed deltas from approved source evidence and The Observed AIP shall reference exact source packages and moments and shall not grant the derivative producer authority to reinterpret the guest’s meaning
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** a planned, inferred, rejected, or superseded field is presented without its exact epistemic state or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-002` Tension-and-Release Narrative Engine: Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. conflicts with the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail.
- **UX failure scenario:** a line becomes quotable only because its qualifying premise and emotional tail were removed The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall compile actual roles, directions, pressures, urges, edges, primitive and archetype evidence, reactions, limitations, and planned–observed deltas from approved source evidence and The Observed AIP shall reference exact source packages and moments and shall not grant the derivative producer authority to reinterpret the guest’s meaning, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-12.01 expects exact outputs from this Story. If the mandate is absent, a line becomes quotable only because its qualifying premise and emotional tail were removed
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-EXPRESSION-001` (AI2 Expression Moment contract), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-INT-002` (CCP V9.1 Expression Capture and Archetype Routing)

### AIR-ST-12.01 — Admit Brief-led and imported interview sources

**Story:** As an Activative Interview operator, I want to admit Brief-led and imported interview sources, so that Brief-led interviews and imported interviews become equally usable derivative roots without inventing absent planning history.

**Primary FRs:** `AIR-FR-067`, `AIR-FR-068`

**Entry:** An Activative Interview session completes or an operator imports an existing interview and transcript.

**Terminal:** A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives.

**Primary acceptance**

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the operator completes admit brief-led and imported interview sources
- **Then** A completed Activative Interview shall produce a source package that references its Brief, Planned AIP, Interview Asset Contracts, calls, observations, Reaction Receipts, and observed evidence and An imported interview shall become a first-class source package while explicitly declaring which planned activation, anchor, Matrix, or session objects are absent
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VOC-009` Sensory Scene Anchoring: Use vivid sensory cues to build the theater of the mind for the listener. conflicts with the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **UX failure scenario:** derivatives cite invented planning history or drift across source-package versions The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A completed Activative Interview shall produce a source package that references its Brief, Planned AIP, Interview Asset Contracts, calls, observations, Reaction Receipts, and observed evidence and An imported interview shall become a first-class source package while explicitly declaring which planned activation, anchor, Matrix, or session objects are absent, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-12.02 expects exact outputs from this Story. If the mandate is absent, derivatives cite invented planning history or drift across source-package versions
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine)

### AIR-ST-12.02 — Assemble the exact media, transcript, tag, reaction, and keyframe spine

**Story:** As an Activative Interview operator, I want to assemble the exact media, transcript, tag, reaction, and keyframe spine, so that Brief-led interviews and imported interviews become equally usable derivative roots without inventing absent planning history.

**Primary FRs:** `AIR-FR-069`, `AIR-FR-070`

**Entry:** An Activative Interview session completes or an operator imports an existing interview and transcript.

**Terminal:** A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives.

**Primary acceptance**

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the operator completes assemble the exact media, transcript, tag, reaction, and keyframe spine
- **Then** The source package shall hash and version original video/audio, transcript words and phrases, speaker map, time alignment, audio events, shot map, keyframes, and visual references and Every planned, observed, inferred, operator-confirmed, rejected, and superseded tag shall retain its source, timestamp or span, author, and lifecycle state
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or a planned, inferred, rejected, or superseded field is presented without its exact epistemic state
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-003` Intent Governs Style: Subordinate all stylistic choices to the specific communication intent of the artifact. conflicts with the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **UX failure scenario:** derivatives cite invented planning history or drift across source-package versions The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The source package shall hash and version original video/audio, transcript words and phrases, speaker map, time alignment, audio events, shot map, keyframes, and visual references and Every planned, observed, inferred, operator-confirmed, rejected, and superseded tag shall retain its source, timestamp or span, author, and lifecycle state, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-12.03 expects exact outputs from this Story. If the mandate is absent, derivatives cite invented planning history or drift across source-package versions
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine)

### AIR-ST-12.03 — Version and publish the canonical source package under operator authority

**Story:** As an Activative Interview operator, I want to version and publish the canonical source package under operator authority, so that Brief-led interviews and imported interviews become equally usable derivative roots without inventing absent planning history.

**Primary FRs:** `AIR-FR-071`, `AIR-FR-072`

**Entry:** An Activative Interview session completes or an operator imports an existing interview and transcript.

**Terminal:** A versioned canonical package is validated and available for source-led shorts, Carousels, SuperVisuals, animation scenes, and future source-backed derivatives.

**Primary acceptance**

- **Given** An Activative Interview session completes or an operator imports an existing interview and transcript.
- **When** the operator completes version and publish the canonical source package under operator authority
- **Then** Corrections to transcripts, speaker maps, tags, moments, or references shall create successor package versions and invalidate only dependent derivative programs and The package shall record the operator-provided source authority and intended route scope as provenance and execution context without introducing a separate creative-policy authority
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical.
- **UX failure scenario:** derivatives cite invented planning history or drift across source-package versions The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Corrections to transcripts, speaker maps, tags, moments, or references shall create successor package versions and invalidate only dependent derivative programs and The package shall record the operator-provided source authority and intended route scope as provenance and execution context without introducing a separate creative-policy authority, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-13.01 expects exact outputs from this Story. If the mandate is absent, derivatives cite invented planning history or drift across source-package versions
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD), `SRC-AI2-SOURCE-001` (AI2 Canonical Interview Source Package contract), `SRC-INT-001` (CCP V9 Interview-First Expression Engine)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-10 — Orchestrate a Fresh Campaign Across Audience Roles

**Value:** A content batch distributes psychological roles, tensions, directions, archetypes, and primitive coalitions coherently without exhausting one formula or confusing audience response with source reaction.

**Entry state:** A canonical source package and approved derivative opportunities exist.

**Terminal state:** A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision.

**Product boundaries:** Activative Intelligence Runtime, Atomic Harness Pipeline consumer, Publishing observation adapters

**Primary features:** F13

### AIR-ST-13.01 — Compile a coordinated Campaign Activation Program

**Story:** As an Activative Intelligence operator, I want to compile a coordinated Campaign Activation Program, so that A content batch distributes psychological roles, tensions, directions, archetypes, and primitive coalitions coherently without exhausting one formula or confusing audience response with source reaction.

**Primary FRs:** `AIR-FR-073`, `AIR-FR-074`

**Entry:** A canonical source package and approved derivative opportunities exist.

**Terminal:** A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision.

**Primary acceptance**

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the operator completes compile a coordinated campaign activation program
- **Then** The Runtime shall sequence source-backed derivative programs with audience segment, role, tension, direction, edge, archetype, primitive signature, format, and intended relationship movement and The campaign shall apply minimum diversity and repetition limits so repeated accusation, regret, inversion, or one archetype formula cannot dominate by local score alone
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit or the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-002` Tension-and-Release Narrative Engine: Hold attention by alternating pressure and relief, forcing the audience to wait for the resolution of a stated problem. conflicts with the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **UX failure scenario:** the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall sequence source-backed derivative programs with audience segment, role, tension, direction, edge, archetype, primitive signature, format, and intended relationship movement and The campaign shall apply minimum diversity and repetition limits so repeated accusation, regret, inversion, or one archetype formula cannot dominate by local score alone, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-13.02 expects exact outputs from this Story. If the mandate is absent, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

**Sources:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### AIR-ST-13.02 — Protect role, direction, archetype, and structure freshness

**Story:** As an Activative Intelligence operator, I want to protect role, direction, archetype, and structure freshness, so that A content batch distributes psychological roles, tensions, directions, archetypes, and primitive coalitions coherently without exhausting one formula or confusing audience response with source reaction.

**Primary FRs:** `AIR-FR-075`, `AIR-FR-076`

**Entry:** A canonical source package and approved derivative opportunities exist.

**Terminal:** A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision.

**Primary acceptance**

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the operator completes protect role, direction, archetype, and structure freshness
- **Then** The system shall track prior structures, Primitive coalitions, roles, tensions, visual operators, archetypes, and audience exposure that affect present activation strength and Publishing observations shall produce Audience Reaction Receipts tied to exact asset versions, audience context, platform, exposure window, and measurement limits
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-HUM-021` Irony Inversion: Express the polar opposite of the Subtext with total conviction, never breaking voice, and let the audience resolve the contradiction to discover the hidden truth. conflicts with the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **UX failure scenario:** the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The system shall track prior structures, Primitive coalitions, roles, tensions, visual operators, archetypes, and audience exposure that affect present activation strength and Publishing observations shall produce Audience Reaction Receipts tied to exact asset versions, audience context, platform, exposure window, and measurement limits, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-13.03 expects exact outputs from this Story. If the mandate is absent, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### AIR-ST-13.03 — Capture audience response and revise the campaign additively

**Story:** As an Activative Intelligence operator, I want to capture audience response and revise the campaign additively, so that A content batch distributes psychological roles, tensions, directions, archetypes, and primitive coalitions coherently without exhausting one formula or confusing audience response with source reaction.

**Primary FRs:** `AIR-FR-077`, `AIR-FR-078`

**Entry:** A canonical source package and approved derivative opportunities exist.

**Terminal:** A versioned campaign program sequences eligible assets, enforces diversity and freshness, captures audience response separately, and supports additive revision.

**Primary acceptance**

- **Given** A canonical source package and approved derivative opportunities exist.
- **When** the operator completes capture audience response and revise the campaign additively
- **Then** The Runtime shall identify defensive repetition, habituation, formula visibility, role overload, edge overuse, and relief deficits across the campaign and Campaign revisions shall supersede only affected asset plans or sequencing decisions while preserving published history, source lineage, and prior performance evidence
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit or the proposed campaign repeats an exhausted role, structure, Primitive signature, or archetype beyond its current freshness limit
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-TRS-003` Reflective Social Proof (The Status Share): Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. conflicts with the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls.
- **UX failure scenario:** the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall identify defensive repetition, habituation, formula visibility, role overload, edge overuse, and relief deficits across the campaign and Campaign revisions shall supersede only affected asset plans or sequencing decisions while preserving published history, source lineage, and prior performance evidence, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-14.01 expects exact outputs from this Story. If the mandate is absent, the campaign repeatedly activates the same defense or formula until the audience sees the template instead of the truth
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-CAMPAIGN-001` (AI2 Campaign Activation Program contract), `SRC-AHP-F23-001` (AHP F23 source-backed batch and archetype routing), `SRC-CCV-001` (CCV Combinatorial Controlled Variation)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-11 — Advance Relationships Through Bounded Activative Calls

**Value:** Public interaction, replies, micro-commitments, interviews, asset delivery, and offers form an evidence-bearing relationship progression rather than disconnected outreach steps.

**Entry state:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.

**Terminal state:** The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust.

**Product boundaries:** Activative Intelligence Runtime, Interview Expression, Relationship operator

**Primary features:** F14

### AIR-ST-14.01 — Represent the current relationship state and hypotheses

**Story:** As an Activative Intelligence operator, I want to represent the current relationship state and hypotheses, so that Public interaction, replies, micro-commitments, interviews, asset delivery, and offers form an evidence-bearing relationship progression rather than disconnected outreach steps.

**Primary FRs:** `AIR-FR-079`, `AIR-FR-080`

**Entry:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.

**Terminal:** The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust.

**Primary acceptance**

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the operator completes represent the current relationship state and hypotheses
- **Then** The Runtime shall represent current relationship stage, prior interactions, expressed recognition, unresolved tension, commitments, delivered value, and evidence limits and The Runtime shall compare recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset hypotheses appropriate to the current stage
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence or the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-BUS-007` Social Media as Relationship: Treat every piece of content not as an end in itself, but as a touchpoint designed to advance a relationship, build trust, or invite further connection. conflicts with the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **UX failure scenario:** a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall represent current relationship stage, prior interactions, expressed recognition, unresolved tension, commitments, delivered value, and evidence limits and The Runtime shall compare recognition, mirroring, direct close, micro-commitment, invitation, interview, asset delivery, and reset hypotheses appropriate to the current stage, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-14.02 expects exact outputs from this Story. If the mandate is absent, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-14.02 — Select the smallest useful commitment

**Story:** As an Activative Intelligence operator, I want to select the smallest useful commitment, so that Public interaction, replies, micro-commitments, interviews, asset delivery, and offers form an evidence-bearing relationship progression rather than disconnected outreach steps.

**Primary FRs:** `AIR-FR-081`, `AIR-FR-082`

**Entry:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.

**Terminal:** The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust.

**Primary acceptance**

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the operator completes select the smallest useful commitment
- **Then** The selected move shall ask for the minimum action that creates meaningful evidence or makes the next state possible without pretending greater trust exists and Public comment, reply or DM, micro-commitment, Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer shall be separate states and receipts
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-PER-003` Cumulative Investment: Immediately after delivering a variable reward (like a high Delivery Score), prompt the user to make a small, permanent investment in the platform (e.g., 'Save this vocal take to your Master Archive' or 'Pin this stance to your public profile'). conflicts with the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **UX failure scenario:** a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The selected move shall ask for the minimum action that creates meaningful evidence or makes the next state possible without pretending greater trust exists and Public comment, reply or DM, micro-commitment, Interview Brief, Complete Expression Session, Asset Package, delivery, and next offer shall be separate states and receipts, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-14.03 expects exact outputs from this Story. If the mandate is absent, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging)

### AIR-ST-14.03 — Progress through ReelCast and asset delivery with scoped learning

**Story:** As an Activative Intelligence operator, I want to progress through ReelCast and asset delivery with scoped learning, so that Public interaction, replies, micro-commitments, interviews, asset delivery, and offers form an evidence-bearing relationship progression rather than disconnected outreach steps.

**Primary FRs:** `AIR-FR-083`, `AIR-FR-084`

**Entry:** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.

**Terminal:** The relationship state, smallest commitment, call, response, ReelCast or asset-delivery transition, and scoped learning are recorded without fabricating trust.

**Primary acceptance**

- **Given** A public interaction, direct response, existing relationship, or campaign touchpoint creates a possible next move.
- **When** the operator completes progress through reelcast and asset delivery with scoped learning
- **Then** A delivered source-backed asset shall update relationship state only from the actual delivery, response, use, and operator interpretation rather than from planned value and Relationship learnings shall carry person, audience, stage, platform, interaction type, and applicability limits before they influence future calls
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy or the requested relationship move is inconsistent with the current relationship stage or observed readiness evidence
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-PRG-002` Discover -> On-board -> Immerse -> Master -> Replay: Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. conflicts with the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage.
- **UX failure scenario:** a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A delivered source-backed asset shall update relationship state only from the actual delivery, response, use, and operator interpretation rather than from planned value and Relationship learnings shall carry person, audience, stage, platform, interaction type, and applicability limits before they influence future calls, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-15.01 expects exact outputs from this Story. If the mandate is absent, a premature relationship ask breaks trust or an unnecessarily weak ask wastes demonstrated readiness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-AI2-REL-001` (AI2 relationship activation models), `SRC-INT-001` (CCP V9 Interview-First Expression Engine), `SRC-MOE-001` (Matrix of Edging)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-12 — Compile Final Scripts and Reusable Animation Scenes

**Value:** Every derivative begins from an approved source-backed semantic production package, and every eligible script yields reusable 2D animation scene compositions even when a complete animation short is not immediately rendered.

**Entry state:** An approved Expression Moment, source package, campaign role, and derivative objective exist.

**Terminal state:** A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning.

**Product boundaries:** Activative Intelligence Runtime, Atomic Harness Pipeline consumer, Human script authority

**Primary features:** F15

### AIR-ST-15.01 — Compile a category-specific Derivative Activation Program

**Story:** As an Activative Intelligence operator, I want to compile a category-specific Derivative Activation Program, so that Every derivative begins from an approved source-backed semantic production package, and every eligible script yields reusable 2D animation scene compositions even when a complete animation short is not immediately rendered.

**Primary FRs:** `AIR-FR-085`, `AIR-FR-086`

**Entry:** An approved Expression Moment, source package, campaign role, and derivative objective exist.

**Terminal:** A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning.

**Primary acceptance**

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the operator completes compile a category-specific derivative activation program
- **Then** Each short, Carousel, SuperVisual, animation scene, or relationship asset shall declare source ingredients, viewer role, tension, Edge Product, primitive coalition, archetype coalition, Voice/Visual DNA, and transfer requirements and Writers and Composers shall receive only approved source ingredients, relevant Voice DNA, coalition and archetype context, route rules, and transformation constraints
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VOC-009` Sensory Scene Anchoring: Use vivid sensory cues to build the theater of the mind for the listener. conflicts with the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **UX failure scenario:** copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Each short, Carousel, SuperVisual, animation scene, or relationship asset shall declare source ingredients, viewer role, tension, Edge Product, primitive coalition, archetype coalition, Voice/Visual DNA, and transfer requirements and Writers and Composers shall receive only approved source ingredients, relevant Voice DNA, coalition and archetype context, route rules, and transformation constraints, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-15.02 expects exact outputs from this Story. If the mandate is absent, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition)

### AIR-ST-15.02 — Write and approve the archetype-coalition Final Script

**Story:** As an Activative Intelligence operator, I want to write and approve the archetype-coalition Final Script, so that Every derivative begins from an approved source-backed semantic production package, and every eligible script yields reusable 2D animation scene compositions even when a complete animation short is not immediately rendered.

**Primary FRs:** `AIR-FR-087`, `AIR-FR-088`

**Entry:** An approved Expression Moment, source package, campaign role, and derivative objective exist.

**Terminal:** A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning.

**Primary acceptance**

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the operator completes write and approve the archetype-coalition final script
- **Then** Every verbatim quote, condensation, adaptation, connective line, or rewrite shall identify its source spans, transformation class, authoring program, and approval state and No composition may begin until the complete archetype-coalition Final Script has been reviewed and approved or explicitly superseded by the operator
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative or the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-003` Intent Governs Style: Subordinate all stylistic choices to the specific communication intent of the artifact. conflicts with the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **UX failure scenario:** copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every verbatim quote, condensation, adaptation, connective line, or rewrite shall identify its source spans, transformation class, authoring program, and approval state and No composition may begin until the complete archetype-coalition Final Script has been reviewed and approved or explicitly superseded by the operator, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-15.03 expects exact outputs from this Story. If the mandate is absent, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

**Sources:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition)

### AIR-ST-15.03 — Compose mandatory reusable 2D animation scene packages and hand off production

**Story:** As an Activative Intelligence operator, I want to compose mandatory reusable 2D animation scene packages and hand off production, so that Every derivative begins from an approved source-backed semantic production package, and every eligible script yields reusable 2D animation scene compositions even when a complete animation short is not immediately rendered.

**Primary FRs:** `AIR-FR-089`, `AIR-FR-090`

**Entry:** An approved Expression Moment, source package, campaign role, and derivative objective exist.

**Terminal:** A Final Script and semantic production package are approved; reusable animation scenes are composed; category-specific Harnesses can proceed without reinterpreting meaning.

**Primary acceptance**

- **Given** An approved Expression Moment, source package, campaign role, and derivative objective exist.
- **When** the operator completes compose mandatory reusable 2d animation scene packages and hand off production
- **Then** The system shall create composition-ready scene programs, visual references, character or symbolic roles, timing, BBOX intent, and asset demands that can serve as B-roll, slide elements, or complete animation scenes and The approved Final Script, coalition, archetype program, animation scene package, source lineage, transfer contract, and evaluation requirements shall be packaged for Builder/Harness/Pipeline consumption
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the active Brand Context, Voice DNA, Visual DNA, or Final Script version does not match the one authorized for the derivative or the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PRS-015` The What Is / What Could Be Contrast Engine: Continuously oscillate between validating the audience's current reality and revealing a superior future state, creating an irresistible structural tension. conflicts with the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval.
- **UX failure scenario:** copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The system shall create composition-ready scene programs, visual references, character or symbolic roles, timing, BBOX intent, and asset demands that can serve as B-roll, slide elements, or complete animation scenes and The approved Final Script, coalition, archetype program, animation scene package, source lineage, transfer contract, and evaluation requirements shall be packaged for Builder/Harness/Pipeline consumption, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-16.01 expects exact outputs from this Story. If the mandate is absent, copy, visuals, and animation are built from different semantic programs and cannot form one coherent category-native embodiment
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AHP-F25-001` (AHP F25 source-grounded static and animation derivatives), `SRC-AHP-F28-001` (AHP F28 psychological role and archetype coalition), `SRC-BRAND-001` (CCP CMF Brand Genesis and Micro-Semiotic Pipeline V3), `SRC-ARCH-001` (CCP Archetype System Migration Proposition)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-13 — Preserve Activation Through Every Transformation and Composition

**Value:** The human state and source charge that made the expression valuable survive clipping, rewriting, archetype routing, composition, animation, and platform adaptation. The Runtime translates approved semantic activation into a visual program grounded in research, real-life reference, composition function, primitive contracts, and category-native handoffs before editing begins.

**Entry state:** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.

**Terminal state:** A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics.

**Product boundaries:** Activative Intelligence Runtime, Atomic Harness Builder/Pipeline consumers, Derivative product owners, Independent transfer evaluator, Visual Asset Editor

**Primary features:** F16, F17

### AIR-ST-16.01 — Identify the original source charge and must-survive properties

**Story:** As an Activative Intelligence operator, I want to identify the original source charge and must-survive properties, so that The human state and source charge that made the expression valuable survive clipping, rewriting, archetype routing, composition, animation, and platform adaptation.

**Primary FRs:** `AIR-FR-091`, `AIR-FR-092`

**Entry:** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.

**Terminal:** Every material handoff is evaluated against source fidelity and transfer fidelity; failures are attributed and repairable without rewriting valid upstream truth.

**Primary acceptance**

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the operator completes identify the original source charge and must-survive properties
- **Then** The Runtime shall state the original activation source, participant role, tension, Edge Product, expression evidence, must-survive properties, permitted transformations, and destructive wrong readings and The contract shall distinguish semantic premise, identity stance, emotional or cognitive turn, rhythm, reaction tail, visual cue, and participation role that materially carry the source charge
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the derivative preserves surface wording but drops the source pressure, role, tension, coalition, or Edge Product or the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-001` Matching Principle: Detect the active conversation layer (practical, emotional, or social) and match it before attempting to redirect or advise. conflicts with the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **UX failure scenario:** the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall state the original activation source, participant role, tension, Edge Product, expression evidence, must-survive properties, permitted transformations, and destructive wrong readings and The contract shall distinguish semantic premise, identity stance, emotional or cognitive turn, rhythm, reaction tail, visual cue, and participation role that materially carry the source charge, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-16.02 expects exact outputs from this Story. If the mandate is absent, the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision

**Sources:** `SRC-AI2-TRANSFER-001` (AI2 Activation Transfer Contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### AIR-ST-16.02 — Declare permitted transformations and exact lineage

**Story:** As an Activative Intelligence operator, I want to declare permitted transformations and exact lineage, so that The human state and source charge that made the expression valuable survive clipping, rewriting, archetype routing, composition, animation, and platform adaptation.

**Primary FRs:** `AIR-FR-093`, `AIR-FR-094`

**Entry:** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.

**Terminal:** Every material handoff is evaluated against source fidelity and transfer fidelity; failures are attributed and repairable without rewriting valid upstream truth.

**Primary acceptance**

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the operator completes declare permitted transformations and exact lineage
- **Then** The contract shall explicitly allow or forbid condensation, reordering, rewriting, voice substitution, visual abstraction, animation, crop, timing, and platform adaptation by derivative type and Source-to-moment, moment-to-script, script-to-composition, composition-to-render, and render-to-platform handoffs shall emit transfer evidence and failure attribution
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the derivative preserves surface wording but drops the source pressure, role, tension, coalition, or Edge Product
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-003` Intent Governs Style: Subordinate all stylistic choices to the specific communication intent of the artifact. conflicts with the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **UX failure scenario:** the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The contract shall explicitly allow or forbid condensation, reordering, rewriting, voice substitution, visual abstraction, animation, crop, timing, and platform adaptation by derivative type and Source-to-moment, moment-to-script, script-to-composition, composition-to-render, and render-to-platform handoffs shall emit transfer evidence and failure attribution, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-16.03 expects exact outputs from this Story. If the mandate is absent, the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AI2-TRANSFER-001` (AI2 Activation Transfer Contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### AIR-ST-16.03 — Measure transfer fidelity and repair the responsible handoff

**Story:** As an Activative Intelligence operator, I want to measure transfer fidelity and repair the responsible handoff, so that The human state and source charge that made the expression valuable survive clipping, rewriting, archetype routing, composition, animation, and platform adaptation.

**Primary FRs:** `AIR-FR-095`, `AIR-FR-096`

**Entry:** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.

**Terminal:** Every material handoff is evaluated against source fidelity and transfer fidelity; failures are attributed and repairable without rewriting valid upstream truth.

**Primary acceptance**

- **Given** An Observed AIP and approved Derivative Activation Program require transformation into a category-native embodiment.
- **When** the operator completes measure transfer fidelity and repair the responsible handoff
- **Then** Every derivative assertion, scene, caption, quote, visual proof, voiceover, and animation element shall be traceable to source spans or clearly labeled original connective material and A derivative shall fail when it preserves surface content but changes the intended psychological role, neutralizes the tension, erases the Edge Product, or converges toward generic centroid expression
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the supplied source reference is missing, stale, points to another version, or omits the evidence span needed to support the claim or the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-021` Punctum, Air, and Felt Truth: During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. conflicts with the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product.
- **UX failure scenario:** the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every derivative assertion, scene, caption, quote, visual proof, voiceover, and animation element shall be traceable to source spans or clearly labeled original connective material and A derivative shall fail when it preserves surface content but changes the intended psychological role, neutralizes the tension, erases the Edge Product, or converges toward generic centroid expression, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-17.01 expects exact outputs from this Story. If the mandate is absent, the derivative remains factually connected to the source but loses the charge that gave the viewer a role inside the original tension
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- source spans, word/phrase timing, speakers, audio/visual observations, planned–observed delta, and expression decision
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AI2-TRANSFER-001` (AI2 Activation Transfer Contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-SOURCE-FIRST-001` (AHP V1.1 Source-First Interview PRD)

### AIR-ST-17.01 — Compile visual activation candidates from research and reference

**Story:** As an Activative Intelligence operator, I want to compile visual activation candidates from research and reference, so that The Runtime translates approved semantic activation into a visual program grounded in research, real-life reference, composition function, primitive contracts, and category-native handoffs before editing begins.

**Primary FRs:** `AIR-FR-097`, `AIR-FR-098`

**Entry:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.

**Terminal:** A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics.

**Primary acceptance**

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the operator completes compile visual activation candidates from research and reference
- **Then** The Runtime shall propose visual metaphors, evidence structures, real-life scenes, graphic relations, and composition strategies tied to the viewer role, tension, coalition, archetype, Voice/Visual DNA, and transfer contract and Visual candidates shall cite specimens, real environments, human references, object behavior, or documented visual systems before generated assets are requested where such reference is applicable
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry or composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-001` Composition as Eye-Path Engineering: Structure visual elements within the frame to force a specific sequence of eye movement. conflicts with the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **UX failure scenario:** editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall propose visual metaphors, evidence structures, real-life scenes, graphic relations, and composition strategies tied to the viewer role, tension, coalition, archetype, Voice/Visual DNA, and transfer contract and Visual candidates shall cite specimens, real environments, human references, object behavior, or documented visual systems before generated assets are requested where such reference is applicable, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-17.02 expects exact outputs from this Story. If the mandate is absent, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2)

### AIR-ST-17.02 — Define composition intent and feature contracts before editing

**Story:** As an Activative Intelligence operator, I want to define composition intent and feature contracts before editing, so that The Runtime translates approved semantic activation into a visual program grounded in research, real-life reference, composition function, primitive contracts, and category-native handoffs before editing begins.

**Primary FRs:** `AIR-FR-099`, `AIR-FR-100`

**Entry:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.

**Terminal:** A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics.

**Primary acceptance**

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the operator completes define composition intent and feature contracts before editing
- **Then** The Runtime shall define hierarchy, reading path, subject relationships, BBOX function, negative space, sequence role, and intended viewer state before timeline or canvas operations are authorized and Required gaze, hands, facial expression, props, evidence, text, scale, depth, motion, sonic cues, and wrong-reading locks shall be represented as independently testable Feature Contracts
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry or composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-024` Space as Psychological Relationship: Before finalizing a visual, define the psychological relationship between the subject and the room/landscape. If the character feels trapped, compose the shot to make the walls literally close in on them. If the character feels lost, place them in a vast, empty space that visually overwhelms their scale. Force the environment to express the internal state of the subject. conflicts with the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **UX failure scenario:** editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The Runtime shall define hierarchy, reading path, subject relationships, BBOX function, negative space, sequence role, and intended viewer state before timeline or canvas operations are authorized and Required gaze, hands, facial expression, props, evidence, text, scale, depth, motion, sonic cues, and wrong-reading locks shall be represented as independently testable Feature Contracts, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-17.03 expects exact outputs from this Story. If the mandate is absent, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2)

### AIR-ST-17.03 — Handoff to Pipeline/VAE and reparse the rendered result

**Story:** As an Activative Intelligence operator, I want to handoff to Pipeline/VAE and reparse the rendered result, so that The Runtime translates approved semantic activation into a visual program grounded in research, real-life reference, composition function, primitive contracts, and category-native handoffs before editing begins.

**Primary FRs:** `AIR-FR-101`, `AIR-FR-102`

**Entry:** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.

**Terminal:** A visual activation handoff declares composition function, BBOX intent, negative space, evidence, feature contracts, asset demands, and evaluation criteria without prescribing unapproved provider tactics.

**Primary acceptance**

- **Given** An approved Final Script, Derivative Activation Program, and Activation Transfer Contract require visual embodiment.
- **When** the operator completes handoff to pipeline/vae and reparse the rendered result
- **Then** The handoff shall include semantic authority, visual narrative, composition intent, asset requirements, allowed variation, source references, and evaluation profile for AHP or VAE consumption and The completed composition shall be reparsed into observed hierarchy, BBOX relationships, gaze, reading order, timing, and role/tension evidence for comparison with intent
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry or composition begins without the approved Final Script, real-life reference package, negative-space plan, or category-native geometry
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-021` Punctum, Air, and Felt Truth: During visual review or generation, aggressively protect and prioritize images that contain 'friction'—a messy desk, a genuinely exhausted look, an un-styled strand of hair, or a micro-expression— choosing the image that feels 'lived in' over the image that is technically flawless. conflicts with the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved.
- **UX failure scenario:** editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The handoff shall include semantic authority, visual narrative, composition intent, asset requirements, allowed variation, source references, and evaluation profile for AHP or VAE consumption and The completed composition shall be reparsed into observed hierarchy, BBOX relationships, gaze, reading order, timing, and role/tension evidence for comparison with intent, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-18.01 expects exact outputs from this Story. If the mandate is absent, editing polish hides a weak composition, collapsed negative space, centroid placement, or missing real-life reference
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- Activation Transfer Contract, source-fidelity trace, composition program, render or preview evidence, and independent reparse

**Sources:** `SRC-AI2-VISUAL-001` (AI2 visual narrative schema), `SRC-AHP-F09-001` (AHP F09 Composition IR and static runtime), `SRC-AHP-F15-001` (AHP F15 VAE Delegation and GNM boundary), `SRC-VISUAL-DOCTRINE-001` (CCP Creative Pipeline Architecture V2)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-14 — Learn and Repair Without Global Creative Drift

**Value:** Every meaningful operator correction becomes attributable, structured programming material without silently becoming universal doctrine or changing live model weights. The system identifies which semantic or execution layer failed, invalidates only dependent descendants, and gives each bounded role the smallest complete context required to repair or decide.

**Entry state:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.

**Terminal state:** The failure is attributed, descendants are invalidated, a bounded repair or human escalation occurs, and replay proves the correction without unrelated regeneration.

**Product boundaries:** Activative Intelligence Runtime, Atomic Harness Pipeline consumer, Conscious Activations Studio, Human creative authority, Independent evaluators

**Primary features:** F18, F19

### AIR-ST-18.01 — Capture every meaningful HumanResolutionEpisode

**Story:** As a Conscious Content Operator, I want to capture every meaningful HumanResolutionEpisode, so that Every meaningful operator correction becomes attributable, structured programming material without silently becoming universal doctrine or changing live model weights.

**Primary FRs:** `AIR-FR-103`, `AIR-FR-104`

**Entry:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.

**Terminal:** The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback.

**Primary acceptance**

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the operator completes capture every meaningful humanresolutionepisode
- **Then** Approvals, rejections, candidate selections, revisions, direct manipulations, tool overrides, taste explanations, and publication decisions shall emit immutable HumanResolutionEpisodes and The episode shall identify whether the issue originated in source understanding, Activative Intelligence, primitive binding, archetype routing, script, retrieval, model, composition, tool, runtime, evaluator, or operator policy
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to turn one operator correction into a global default or live weight update.
- **UX failure scenario:** local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Approvals, rejections, candidate selections, revisions, direct manipulations, tool overrides, taste explanations, and publication decisions shall emit immutable HumanResolutionEpisodes and The episode shall identify whether the issue originated in source understanding, Activative Intelligence, primitive binding, archetype routing, script, retrieval, model, composition, tool, runtime, evaluator, or operator policy, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-18.02 expects exact outputs from this Story. If the mandate is absent, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler)

### AIR-ST-18.02 — Attribute the decision and index programming material

**Story:** As a Conscious Content Operator, I want to attribute the decision and index programming material, so that Every meaningful operator correction becomes attributable, structured programming material without silently becoming universal doctrine or changing live model weights.

**Primary FRs:** `AIR-FR-105`, `AIR-FR-106`

**Entry:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.

**Terminal:** The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback.

**Primary acceptance**

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the operator completes attribute the decision and index programming material
- **Then** Accepted, rejected, repaired, and contradictory episodes shall become retrievable records and candidate SFT, preference, repair, hard-negative, or evaluator examples with exact lineage and Production use may append evidence and indexes but shall not update live weights, canonical Skills, Primitive registries, archetype authority, or doctrine without a release process
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the input is stale, contradictory, unresolved, or cannot support the claimed state transition or the observation evidence is incomplete, the guest state contradicts the prepared path, or the proposed call exceeds the declared pressure policy
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-PSY-008` Attack Problem Not Person: Separate the human identity from the behavioral issue to preserve the alliance while delivering correction. conflicts with the shortcut to turn one operator correction into a global default or live weight update.
- **UX failure scenario:** local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Accepted, rejected, repaired, and contradictory episodes shall become retrievable records and candidate SFT, preference, repair, hard-negative, or evaluator examples with exact lineage and Production use may append evidence and indexes but shall not update live weights, canonical Skills, Primitive registries, archetype authority, or doctrine without a release process, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-18.03 expects exact outputs from this Story. If the mandate is absent, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler)

### AIR-ST-18.03 — Promote scoped recipes, model data, and Identity DNA observations through evidence

**Story:** As a Conscious Content Operator, I want to promote scoped recipes, model data, and Identity DNA observations through evidence, so that Every meaningful operator correction becomes attributable, structured programming material without silently becoming universal doctrine or changing live model weights.

**Primary FRs:** `AIR-FR-107`, `AIR-FR-108`

**Entry:** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.

**Terminal:** The resolution is immutable, attributed, indexed for retrieval and dataset construction, and eligible for scoped promotion or rollback.

**Primary acceptance**

- **Given** An operator approves, rejects, compares, revises, directly manipulates, explains, or publishes a semantic or production result.
- **When** the operator completes promote scoped recipes, model data, and identity dna observations through evidence
- **Then** Promotion shall require repeated evidence, control comparisons, regression cases, scope, lifecycle, rollback, and human authority and Identity observations may be accepted, rejected, narrowed, or superseded through a separate profile-resolution event linked to source evidence and HumanResolutionEpisodes
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-TRS-003` Reflective Social Proof (The Status Share): Design the output artifact (video, image, or link preview) to function primarily as a high-status credential for the sender, completely bypassing the social friction of traditional 'refer-a-friend' mechanics. conflicts with the shortcut to turn one operator correction into a global default or live weight update.
- **UX failure scenario:** local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Promotion shall require repeated evidence, control comparisons, regression cases, scope, lifecycle, rollback, and human authority and Identity observations may be accepted, rejected, narrowed, or superseded through a separate profile-resolution event linked to source evidence and HumanResolutionEpisodes, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-19.01 expects exact outputs from this Story. If the mandate is absent, local taste feedback mutates unrelated clients, formats, or archetypes and compounds creative sameness
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-AI2-HRE-001` (AI2 Human Resolution Episode contract), `SRC-STUDIO-AMENDMENT-001` (Conscious Activations Studio Architecture Amendment V2.1), `SRC-AHP-F26-001` (AHP F26 Human Resolution and Revision Compiler)

### AIR-ST-19.01 — Locate the failed layer and its exact descendants

**Story:** As an Activative Intelligence operator, I want to locate the failed layer and its exact descendants, so that The system identifies which semantic or execution layer failed, invalidates only dependent descendants, and gives each bounded role the smallest complete context required to repair or decide.

**Primary FRs:** `AIR-FR-109`, `AIR-FR-110`

**Entry:** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.

**Terminal:** The failure is attributed, descendants are invalidated, a bounded repair or human escalation occurs, and replay proves the correction without unrelated regeneration.

**Primary acceptance**

- **Given** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.
- **When** the operator completes locate the failed layer and its exact descendants
- **Then** The system shall distinguish source, epistemic state, Matrix, hypothesis, primitive, archetype, brand/DNA, script, transfer, retrieval, model, composition, tool, runtime, evaluator, and operator-resolution failures and The Runtime shall traverse typed dependencies and invalidate only objects whose validity depends on the failed or superseded object
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the responsible layer is unknown or the proposed repair would regenerate valid upstream work or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-FBK-001` RIM Feedback Discipline: Architect the feedback loops so that the moment the user completes an action, the system immediately returns a score or visual response that explicitly explains *why* the action mattered to the user's specific progression. conflicts with the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only.
- **UX failure scenario:** repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must The system shall distinguish source, epistemic state, Matrix, hypothesis, primitive, archetype, brand/DNA, script, transfer, retrieval, model, composition, tool, runtime, evaluator, and operator-resolution failures and The Runtime shall traverse typed dependencies and invalidate only objects whose validity depends on the failed or superseded object, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-19.02 expects exact outputs from this Story. If the mandate is absent, repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-REPAIR-001` (AI2 failure attribution and repair contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-AHP-F03-001` (AHP F03 bounded role taxonomy)

### AIR-ST-19.02 — Compile and execute a bounded local repair

**Story:** As an Activative Intelligence operator, I want to compile and execute a bounded local repair, so that The system identifies which semantic or execution layer failed, invalidates only dependent descendants, and gives each bounded role the smallest complete context required to repair or decide.

**Primary FRs:** `AIR-FR-111`, `AIR-FR-112`

**Entry:** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.

**Terminal:** The failure is attributed, descendants are invalidated, a bounded repair or human escalation occurs, and replay proves the correction without unrelated regeneration.

**Primary acceptance**

- **Given** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.
- **When** the operator completes compile and execute a bounded local repair
- **Then** A Repair Program shall state the target object, permitted changes, preserved valid properties, required evidence, evaluator, stopping law, and escalation path and The system shall declare each role’s purpose, actor, inputs, outputs, authority, and handoff rather than treating role labels as hidden personas or autonomous product owners
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the responsible layer is unknown or the proposed repair would regenerate valid upstream work or the candidate archetype communicates a topic but does not position the audience inside the approved role and tension
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-BUS-006` Hierarchy as Attention Routing: Assign distinct, uncompetitive visual weights to different semantic roles in the content, ensuring the viewer's eye is routed exactly where it needs to go, in the exact order it needs to go there. conflicts with the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only.
- **UX failure scenario:** repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must A Repair Program shall state the target object, permitted changes, preserved valid properties, required evidence, evaluator, stopping law, and escalation path and The system shall declare each role’s purpose, actor, inputs, outputs, authority, and handoff rather than treating role labels as hidden personas or autonomous product owners, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-19.03 expects exact outputs from this Story. If the mandate is absent, repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

**Sources:** `SRC-AI2-REPAIR-001` (AI2 failure attribution and repair contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-AHP-F03-001` (AHP F03 bounded role taxonomy)

### AIR-ST-19.03 — Provide role-specific JIT context and replay evidence

**Story:** As an Activative Intelligence operator, I want to provide role-specific JIT context and replay evidence, so that The system identifies which semantic or execution layer failed, invalidates only dependent descendants, and gives each bounded role the smallest complete context required to repair or decide.

**Primary FRs:** `AIR-FR-113`, `AIR-FR-114`

**Entry:** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.

**Terminal:** The failure is attributed, descendants are invalidated, a bounded repair or human escalation occurs, and replay proves the correction without unrelated regeneration.

**Primary acceptance**

- **Given** A semantic, reaction, transfer, composition, evaluation, or production result fails or becomes contradicted by new evidence.
- **When** the operator completes provide role-specific jit context and replay evidence
- **Then** Hunters receive discovery context, Analysts receive evidence and contradictions, Composers receive approved ingredients and contracts, and Commanders receive candidates, receipts, gates, and stopping laws and The system shall reproduce the relevant object versions, context capsules, candidates, decisions, repairs, and evaluation results without synthesizing missing human authority
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the candidate archetype communicates a topic but does not position the audience inside the approved role and tension or the responsible layer is unknown or the proposed repair would regenerate valid upstream work
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-VSG-001` Composition as Eye-Path Engineering: Structure visual elements within the frame to force a specific sequence of eye movement. conflicts with the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only.
- **UX failure scenario:** repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Hunters receive discovery context, Analysts receive evidence and contradictions, Composers receive approved ingredients and contracts, and Commanders receive candidates, receipts, gates, and stopping laws and The system shall reproduce the relevant object versions, context capsules, candidates, decisions, repairs, and evaluation results without synthesizing missing human authority, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-20.01 expects exact outputs from this Story. If the mandate is absent, repair regenerates valid upstream work, destroys source lineage, and makes the actual defect impossible to learn from
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- psychological role, tension, archetype coalition, Guest Voice DNA lineage, Final Script approval, and rejection alternatives

**Sources:** `SRC-AI2-REPAIR-001` (AI2 failure attribution and repair contract), `SRC-AHP-F16-001` (AHP F16 evaluation and selective repair), `SRC-AHP-F03-001` (AHP F03 bounded role taxonomy)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## AIR-EP-15 — Deploy Specialized Intelligence and Integrate the Product System

**Value:** The Runtime uses the smallest reliable specialized model or deterministic program for each bounded capability while preserving semantic sovereignty, independent evaluation, and cross-product contracts.

**Entry state:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.

**Terminal state:** An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible.

**Product boundaries:** Activative Intelligence Runtime, Cross-product owners, Model Program engineers, Program Control

**Primary features:** F20

### AIR-ST-20.01 — Register Programmed Models and model-specific harnesses

**Story:** As an Activative Intelligence operator, I want to register Programmed Models and model-specific harnesses, so that The Runtime uses the smallest reliable specialized model or deterministic program for each bounded capability while preserving semantic sovereignty, independent evaluation, and cross-product contracts.

**Primary FRs:** `AIR-FR-115`, `AIR-FR-116`

**Entry:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.

**Terminal:** An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible.

**Primary acceptance**

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the operator completes register programmed models and model-specific harnesses
- **Then** Every learned implementation shall pin base model, tokenizer, adapter or checkpoint, runtime, training lineage, supported inputs, applicability envelope, limitations, and exact hashes and The system shall diagnose instruction, knowledge, retrieval, tool, context, and planning failures and improve context, tools, checks, or orchestration before assuming a larger model is required
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary or the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `PRM-BUS-001` Perception and Guidance Stack: Design visuals, text hierarchy, and action cues as one integrated system that controls where the eye goes and what the hand does next. conflicts with the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **UX failure scenario:** a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Every learned implementation shall pin base model, tokenizer, adapter or checkpoint, runtime, training lineage, supported inputs, applicability envelope, limitations, and exact hashes and The system shall diagnose instruction, knowledge, retrieval, tool, context, and planning failures and improve context, tools, checks, or orchestration before assuming a larger model is required, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-20.02 expects exact outputs from this Story. If the mandate is absent, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models)

### AIR-ST-20.02 — Evaluate claims independently and integrate products through typed handoffs

**Story:** As an Activative Intelligence operator, I want to evaluate claims independently and integrate products through typed handoffs, so that The Runtime uses the smallest reliable specialized model or deterministic program for each bounded capability while preserving semantic sovereignty, independent evaluation, and cross-product contracts.

**Primary FRs:** `AIR-FR-117`, `AIR-FR-118`

**Entry:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.

**Terminal:** An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible.

**Primary acceptance**

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the operator completes evaluate claims independently and integrate products through typed handoffs
- **Then** Deterministic gates shall run first; semantic, Primitive, archetype, transfer, visual, and relationship judgments shall use independent calibrated evaluators and human labels where required and Program Control, Interview Expression, Builder, AHP, VAE, Delegation, and Studio shall exchange exact objects and receipts without duplicating semantic or execution ownership
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary or the implementation is outside its capability envelope, approves itself, or crosses the declared product boundary
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-PRG-002` Discover -> On-board -> Immerse -> Master -> Replay: Architect the platform as a state-changing progression system where the available features, required skill level, and visible metrics unlock sequentially based on the user's maturity phase. conflicts with the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **UX failure scenario:** a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Deterministic gates shall run first; semantic, Primitive, archetype, transfer, visual, and relationship judgments shall use independent calibrated evaluators and human labels where required and Program Control, Interview Expression, Builder, AHP, VAE, Delegation, and Studio shall exchange exact objects and receipts without duplicating semantic or execution ownership, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** AIR-ST-20.03 expects exact outputs from this Story. If the mandate is absent, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity

**Sources:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models)

### AIR-ST-20.03 — Promote evidence-backed capability claims and bounded release states

**Story:** As an Activative Intelligence operator, I want to promote evidence-backed capability claims and bounded release states, so that The Runtime uses the smallest reliable specialized model or deterministic program for each bounded capability while preserving semantic sovereignty, independent evaluation, and cross-product contracts.

**Primary FRs:** `AIR-FR-119`, `AIR-FR-120`

**Entry:** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.

**Terminal:** An implementation is registered, evaluated, shadowed, promoted within evidence, integrated through typed handoffs, monitored, and reversible.

**Primary acceptance**

- **Given** A bounded semantic or operational responsibility has a stable contract, dataset opportunity, benchmark, and fallback.
- **When** the operator completes promote evidence-backed capability claims and bounded release states
- **Then** Claims shall move through proposed, experimental, validated, shadow, limited-production, production, deprecated, retired, and revoked states with rollback and focused regression and The product shall emit exact Stories, Tech Specs, source dispositions, target paths, tests, evidence gaps, and authority gates; planning completeness shall not imply production readiness or certification
- **And** every produced object carries exact version, source, epistemic state, product owner, evaluator, and descendant relationships.

**Adversarial denial**

- **Given** one episode is treated as universal doctrine or a live model update without an applicability envelope and release evidence or the input is stale, contradictory, unresolved, or cannot support the claimed state transition
- **When** the same Story operation is requested
- **Then** the system emits a typed blocker before any object becomes downstream-eligible
- **And** it does not manufacture a source fact, Primitive meaning, human decision, or product authority to make the request pass.

**Recovery / supersession**

- **Given** a previously accepted upstream object is superseded or contradicted
- **When** dependency analysis runs
- **Then** only dependent descendants are invalidated and the accepted historical path remains replayable
- **And** the Story can be rerun with the successor version without rewriting unrelated evidence.

**CBAR hardening**

- **Tension:** `EXP-TRG-005` First Major Win-State: Gate all social and expansion triggers behind a mathematically proven, hard-won success state, completely suppressing them during onboarding or failure. conflicts with the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation.
- **UX failure scenario:** a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient The user or operator would act on a false or flattened result, causing trust erosion, identity misrecognition, formula fatigue, or avoidable rework depending on the feature.
- **Resolution demand:** The product law and exact Primitive contract take precedence. The implementation must Claims shall move through proposed, experimental, validated, shadow, limited-production, production, deprecated, retired, and revoked states with rollback and focused regression and The product shall emit exact Stories, Tech Specs, source dispositions, target paths, tests, evidence gaps, and authority gates; planning completeness shall not imply production readiness or certification, and must expose a blocker instead of using the shortcut.
- **Downstream proof:** cross-product implementation and release handoff expects exact outputs from this Story. If the mandate is absent, a specialist performs outside evidence, approves itself, or crosses product boundaries while appearing efficient
- **Verdict:** `REWRITE INCORPORATED` — the hardened acceptance above is canonical for this draft.

**Required evidence**

- exact input object IDs, versions, hashes, and source references
- the active contract, product owner, actor identity, and lifecycle transition
- positive and adversarial validation results with immutable receipt identity
- model/harness version, dataset and evaluation lineage, applicability envelope, baseline comparison, shadow result, fallback, and rollback

**Sources:** `SRC-AI2-MODEL-001` (AI2 reference implementation models), `SRC-AHP-MODEL-001` (AHP Programmed Model and learned claims feature), `SRC-HARNESS-RESEARCH-001` (Better Harnesses, Smaller Models research paper), `SRC-RECENT-001` (Efficient Skill Grounding via Code Refactoring with Small Language Models)

### Epic evidence claim

The Epic is complete only when every Story passes its controlling Tech Spec, exact Primitive sources resolve, cross-product handoffs pass, and the terminal user/product value is demonstrated without inferring production readiness from planning or synthetic evidence.

## Constraint Resolution Manifest

The following mandates are appended to the V2.1 planning program. Each is traceable to one Story and one exact Primitive source.

1. **AIR-EP-01-M01 — PRM-PSY-008 Rule:** Establish activation-domain and truth-state authority must preserve Attack Problem Not Person's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. Downstream lock: `AIR-ST-01.02`.
2. **AIR-EP-01-M02 — PRM-VSG-003 Rule:** Version semantic decisions without rewriting history must preserve Intent Governs Style's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. Downstream lock: `AIR-ST-01.03`.
3. **AIR-EP-01-M03 — EXP-FBK-001 Rule:** Prove lifecycle and epistemology claims must preserve RIM Feedback Discipline's core move while denying the shortcut to collapse one object-level status across fields so implementation becomes simpler. Downstream lock: `AIR-ST-02.01`.
4. **AIR-EP-02-M01 — PRM-PSY-001 Rule:** Assemble identity, audience, interviewer, and relationship context must preserve Matching Principle's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. Downstream lock: `AIR-ST-02.02`.
5. **AIR-EP-02-M02 — PRM-PSY-008 Rule:** Compile Matrix broad signal and survived Edge Product must preserve Attack Problem Not Person's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. Downstream lock: `AIR-ST-02.03`.
6. **AIR-EP-02-M03 — PRM-PRS-015 Rule:** Propose Identity DNA candidate observations without mutation must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to use topic similarity as a substitute for identity, resonance, and Matrix survival. Downstream lock: `AIR-ST-03.01`.
7. **AIR-EP-03-M01 — PRM-PSY-001 Rule:** Generate meaningfully different activation hypotheses must preserve Matching Principle's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. Downstream lock: `AIR-ST-03.02`.
8. **AIR-EP-03-M02 — PRM-PRS-015 Rule:** Compare candidates under non-compensable gates must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. Downstream lock: `AIR-ST-03.03`.
9. **AIR-EP-03-M03 — PRM-HUM-021 Rule:** Converge while preserving rejections and stopping evidence must preserve Irony Inversion's core move while denying the shortcut to accept the first fluent hypothesis and skip comparative search. Downstream lock: `AIR-ST-04.01`.
10. **AIR-EP-04-M01 — PRM-BUS-001 Rule:** Query the real primitive registries must preserve Perception and Guidance Stack's core move while denying the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts. Downstream lock: `AIR-ST-04.02`.
11. **AIR-EP-04-M02 — PRM-BUS-006 Rule:** Bind exact primitives to the current activation state must preserve Hierarchy as Attention Routing's core move while denying the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts. Downstream lock: `AIR-ST-04.03`.
12. **AIR-EP-04-M03 — PRM-PSY-001 Rule:** Prove stage-appropriate primitive coverage and conflicts must preserve Matching Principle's core move while denying the shortcut to select primitives by name similarity without loading their core move, misuse modes, or conflicts. Downstream lock: `AIR-ST-05.01`.
13. **AIR-EP-04-M04 — PRM-PRS-002 Rule:** Compile a complete Primitive Coalition Contract must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. Downstream lock: `AIR-ST-05.02`.
14. **AIR-EP-04-M05 — PRM-PRS-009 Rule:** Resolve Coalition Signature and Edge Product must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. Downstream lock: `AIR-ST-05.03`.
15. **AIR-EP-04-M06 — PRM-PRS-015 Rule:** Promote evidence into Steering Recipes and Primitive Evaluation Receipts must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to treat a list of primitives as a coalition without binding, signature, edge, or misuse evaluation. Downstream lock: `AIR-ST-06.01`.
16. **AIR-EP-05-M01 — PRM-PSY-001 Rule:** Route the Edge Product into a supported archetype must preserve Matching Principle's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. Downstream lock: `AIR-ST-06.02`.
17. **AIR-EP-05-M02 — PRM-PRS-002 Rule:** Define the psychological role inside the tension must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. Downstream lock: `AIR-ST-06.03`.
18. **AIR-EP-05-M03 — PRM-HUM-021 Rule:** Lock archetype coalition geometry and route evidence must preserve Irony Inversion's core move while denying the shortcut to select an archetype because it is familiar or fashionable rather than because it gives the viewer the intended role inside the tension. Downstream lock: `AIR-ST-07.01`.
19. **AIR-EP-06-M01 — PRM-VOC-009 Rule:** Lock active Brand Context, Voice DNA, and Visual DNA must preserve Sensory Scene Anchoring's core move while denying the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence. Downstream lock: `AIR-ST-07.02`.
20. **AIR-EP-06-M02 — PRM-VSG-003 Rule:** Distill source signal through RSCS layers must preserve Intent Governs Style's core move while denying the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence. Downstream lock: `AIR-ST-07.03`.
21. **AIR-EP-06-M03 — PRM-VSG-021 Rule:** Generate controlled variation while protecting Negative Space and Edge Integrity must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to imitate surface style while omitting Brand Genesis, Voice DNA, Visual DNA, and distillation evidence. Downstream lock: `AIR-ST-08.01`.
22. **AIR-EP-07-M01 — PRM-PRS-009 Rule:** Compile the Planned Activative Intelligence Pack must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract. Downstream lock: `AIR-ST-08.02`.
23. **AIR-EP-07-M02 — PRM-PRS-002 Rule:** Create complete Interview Asset Contracts must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract. Downstream lock: `AIR-ST-08.03`.
24. **AIR-EP-07-M03 — PRM-PSY-008 Rule:** Validate adaptive branches, dose, landing, and route hypotheses must preserve Attack Problem Not Person's core move while denying the shortcut to generate a question list instead of a complete adaptive Interview Asset Contract. Downstream lock: `AIR-ST-09.01`.
25. **AIR-EP-08-M01 — PRM-PSY-008 Rule:** Maintain an evidence-bearing live state must preserve Attack Problem Not Person's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. Downstream lock: `AIR-ST-09.02`.
26. **AIR-EP-08-M02 — EXP-FBK-001 Rule:** Propose bounded next Activative Calls and pressure dose must preserve RIM Feedback Discipline's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. Downstream lock: `AIR-ST-09.03`.
27. **AIR-EP-08-M03 — PRM-PRS-009 Rule:** Land, reset, or stop without forcing the intended premise must preserve The McKee Inciting Incident Engine's core move while denying the shortcut to continue the prepared interview script despite live defense, overload, or a landed answer. Downstream lock: `AIR-ST-10.01`.
28. **AIR-EP-08-M04 — EXP-FBK-001 Rule:** Capture multimodal reaction evidence must preserve RIM Feedback Discipline's core move while denying the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence. Downstream lock: `AIR-ST-10.02`.
29. **AIR-EP-08-M05 — PRM-PSY-001 Rule:** Classify reactions, non-reactions, and counteractivation must preserve Matching Principle's core move while denying the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence. Downstream lock: `AIR-ST-10.03`.
30. **AIR-EP-08-M06 — PRM-VSG-021 Rule:** Issue Reaction Receipts and planned–observed deltas must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to infer reaction from transcript wording while ignoring null, visual, sonic, and reaction-tail evidence. Downstream lock: `AIR-ST-11.01`.
31. **AIR-EP-09-M01 — PRM-VOC-009 Rule:** Discover and bound complete Expression Moments must preserve Sensory Scene Anchoring's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. Downstream lock: `AIR-ST-11.02`.
32. **AIR-EP-09-M02 — PRM-VSG-021 Rule:** Resolve moment lifecycle and routeability must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. Downstream lock: `AIR-ST-11.03`.
33. **AIR-EP-09-M03 — PRM-PRS-002 Rule:** Compile the Observed Activative Intelligence Pack must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to extract the shortest quotable phrase and omit the premise or reaction tail. Downstream lock: `AIR-ST-12.01`.
34. **AIR-EP-09-M04 — PRM-VOC-009 Rule:** Admit Brief-led and imported interview sources must preserve Sensory Scene Anchoring's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. Downstream lock: `AIR-ST-12.02`.
35. **AIR-EP-09-M05 — PRM-VSG-003 Rule:** Assemble the exact media, transcript, tag, reaction, and keyframe spine must preserve Intent Governs Style's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. Downstream lock: `AIR-ST-12.03`.
36. **AIR-EP-09-M06 — EXP-FBK-001 Rule:** Version and publish the canonical source package under operator authority must preserve RIM Feedback Discipline's core move while denying the shortcut to fabricate missing Brief-led history for an imported interview so both admission paths look identical. Downstream lock: `AIR-ST-13.01`.
37. **AIR-EP-10-M01 — PRM-PRS-002 Rule:** Compile a coordinated Campaign Activation Program must preserve Tension-and-Release Narrative Engine's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. Downstream lock: `AIR-ST-13.02`.
38. **AIR-EP-10-M02 — PRM-HUM-021 Rule:** Protect role, direction, archetype, and structure freshness must preserve Irony Inversion's core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. Downstream lock: `AIR-ST-13.03`.
39. **AIR-EP-10-M03 — EXP-TRS-003 Rule:** Capture audience response and revise the campaign additively must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to rank every asset locally and publish repeated high-scoring formulas without campaign freshness controls. Downstream lock: `AIR-ST-14.01`.
40. **AIR-EP-11-M01 — PRM-BUS-007 Rule:** Represent the current relationship state and hypotheses must preserve Social Media as Relationship's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. Downstream lock: `AIR-ST-14.02`.
41. **AIR-EP-11-M02 — EXP-PER-003 Rule:** Select the smallest useful commitment must preserve Cumulative Investment's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. Downstream lock: `AIR-ST-14.03`.
42. **AIR-EP-11-M03 — EXP-PRG-002 Rule:** Progress through ReelCast and asset delivery with scoped learning must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to treat a relationship move as a generic conversion funnel and ignore the current relationship stage. Downstream lock: `AIR-ST-15.01`.
43. **AIR-EP-12-M01 — PRM-VOC-009 Rule:** Compile a category-specific Derivative Activation Program must preserve Sensory Scene Anchoring's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. Downstream lock: `AIR-ST-15.02`.
44. **AIR-EP-12-M02 — PRM-VSG-003 Rule:** Write and approve the archetype-coalition Final Script must preserve Intent Governs Style's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. Downstream lock: `AIR-ST-15.03`.
45. **AIR-EP-12-M03 — PRM-PRS-015 Rule:** Compose mandatory reusable 2D animation scene packages and hand off production must preserve The What Is / What Could Be Contrast Engine's core move while denying the shortcut to begin composition from raw quotes or generic copy before archetype-coalition Final Script approval. Downstream lock: `AIR-ST-16.01`.
46. **AIR-EP-13-M01 — PRM-PSY-001 Rule:** Identify the original source charge and must-survive properties must preserve Matching Principle's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. Downstream lock: `AIR-ST-16.02`.
47. **AIR-EP-13-M02 — PRM-VSG-003 Rule:** Declare permitted transformations and exact lineage must preserve Intent Governs Style's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. Downstream lock: `AIR-ST-16.03`.
48. **AIR-EP-13-M03 — PRM-VSG-021 Rule:** Measure transfer fidelity and repair the responsible handoff must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to preserve literal wording while losing the psychological role, tension, Primitive coalition, or Edge Product. Downstream lock: `AIR-ST-17.01`.
49. **AIR-EP-13-M04 — PRM-VSG-001 Rule:** Compile visual activation candidates from research and reference must preserve Composition as Eye-Path Engineering's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. Downstream lock: `AIR-ST-17.02`.
50. **AIR-EP-13-M05 — PRM-VSG-024 Rule:** Define composition intent and feature contracts before editing must preserve Space as Psychological Relationship's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. Downstream lock: `AIR-ST-17.03`.
51. **AIR-EP-13-M06 — PRM-VSG-021 Rule:** Handoff to Pipeline/VAE and reparse the rendered result must preserve Punctum, Air, and Felt Truth's core move while denying the shortcut to start editing or generation before composition intent, negative space, and real-life reference research are resolved. Downstream lock: `AIR-ST-18.01`.
52. **AIR-EP-14-M01 — EXP-FBK-001 Rule:** Capture every meaningful HumanResolutionEpisode must preserve RIM Feedback Discipline's core move while denying the shortcut to turn one operator correction into a global default or live weight update. Downstream lock: `AIR-ST-18.02`.
53. **AIR-EP-14-M02 — PRM-PSY-008 Rule:** Attribute the decision and index programming material must preserve Attack Problem Not Person's core move while denying the shortcut to turn one operator correction into a global default or live weight update. Downstream lock: `AIR-ST-18.03`.
54. **AIR-EP-14-M03 — EXP-TRS-003 Rule:** Promote scoped recipes, model data, and Identity DNA observations through evidence must preserve Reflective Social Proof (The Status Share)'s core move while denying the shortcut to turn one operator correction into a global default or live weight update. Downstream lock: `AIR-ST-19.01`.
55. **AIR-EP-14-M04 — EXP-FBK-001 Rule:** Locate the failed layer and its exact descendants must preserve RIM Feedback Discipline's core move while denying the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only. Downstream lock: `AIR-ST-19.02`.
56. **AIR-EP-14-M05 — PRM-BUS-006 Rule:** Compile and execute a bounded local repair must preserve Hierarchy as Attention Routing's core move while denying the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only. Downstream lock: `AIR-ST-19.03`.
57. **AIR-EP-14-M06 — PRM-VSG-001 Rule:** Provide role-specific JIT context and replay evidence must preserve Composition as Eye-Path Engineering's core move while denying the shortcut to rewrite the full prompt or program instead of attributing the failed layer and invalidating descendants only. Downstream lock: `AIR-ST-20.01`.
58. **AIR-EP-15-M01 — PRM-BUS-001 Rule:** Register Programmed Models and model-specific harnesses must preserve Perception and Guidance Stack's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. Downstream lock: `AIR-ST-20.02`.
59. **AIR-EP-15-M02 — EXP-PRG-002 Rule:** Evaluate claims independently and integrate products through typed handoffs must preserve Discover -> On-board -> Immerse -> Master -> Replay's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. Downstream lock: `AIR-ST-20.03`.
60. **AIR-EP-15-M03 — EXP-TRG-005 Rule:** Promote evidence-backed capability claims and bounded release states must preserve First Major Win-State's core move while denying the shortcut to use a larger or fine-tuned model as authority before stabilizing the harness, retrieval, tools, contracts, and independent evaluation. Downstream lock: `cross-product implementation and release handoff`.
