

**CONSCIOUS COACHING PLATFORM**

**JIT Skill Compiler Architecture**

*Implementation Plan for the CCSB V2*

CCSB · Dependency Registry · Adapter Registry · Module Library · Fingerprint Archive · Mood State Integration · Anti-Draft Intelligence

Version 1.0  ·  March 2026  ·  CCP Engineering Division

**01\. System Overview — What We Are Building and Why**

The JIT Skill Compiler is the operational engine that transforms approved Design Brief Templates into production-ready, psychologically calibrated SKILL.md files at the moment of need. It is not a content generator. It is not a prompt library. It is a compilation system — analogous to how a code compiler takes source code with defined libraries and produces an optimized executable. The source code is the Archetype Design Brief. The libraries are the Module Registry, Adapter Registry, and Dependency Registry. The executable is the compiled SKILL.md. And critically, every compiled skill carries a unique fingerprint ID that links it to every output it ever produces.

The system comprises seven interconnected components that must be understood as a single organism, not seven separate tools. They fail together if any one is missing and they compound each other's value when all are present.

| Component | Role | Failure if Missing |
| :---- | :---- | :---- |
| Dependency Registry v4.0 | The canonical data layer — all inputs a skill can ever consume | Skills reference ghost variables, hallucinate inputs |
| Adapter Registry v2.0 | The transformation layer — how universal modules mutate per domain | Modules copy-pasted without adaptation, intelligence collapses |
| Design Brief Template Library | The specification layer — archetype-invariant container logic | Each skill authored from scratch, quality variance compounds |
| Design Brief Builder Engine | The Phase 1 compiler — produces validated briefs from templates | Incomplete briefs reach assembler, silent failures mid-assembly |
| JIT Skill Assembler v2.0 | The Phase 2 compiler — assembles skills from briefs \+ modules | Single point of failure, no recovery, pipeline collapses |
| Module Library (Containers) | The intelligence layer — ecological adaptations per archetype | Generic reasoning, no domain specificity, output mediocrity |
| Fingerprint Archive | The memory layer — tracks every compiled skill and its outputs | No reproduction, no learning, no quality compounding |

*⬡  SteerEval (Xu et al., 2025): LLM behavioral control degrades from 2.76 at L1 intent to 0.07 at L3 implementation. Pre-solved modules are the only reliable fix at L3.*

*⬡  Evolving PSN (Shi et al., 2025): Systems without maturity-gated update controls exhibit oscillatory behavior — converged modules regress when modified by downstream failures.*

*⬡  SkillNet (Liang et al., 2026): Formalizing skills as composable assets improves agent performance by 40% and reduces execution steps by 30% vs. monolithic authoring.*

**02\. Dependency Registry v4.0 — The Complete Data Layer**

The Dependency Registry v3.0 contains 38 components across 4 categories. The JIT Compiler architecture requires 8 new registrations — 5 engine outputs and 3 protocol additions — to support the Psychological Routing System, Client Intelligence Layer, and Archetype Classification functions that were architecturally specified but never formally registered. Until these are registered, the psychological routing variables in every Design Brief Template exist as inline values with no formal DEP ID, which creates the same ghost variable risk the v3.0 registry was built to eliminate.

**New Registrations — Category 1: Engine Outputs & Raw Data Assets**

| Proposed DEP ID | Name | File | Tier | Required By | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| DEP-ENG-016 | Psychological Routing Brief | psych\_routing\_brief.json | Tier 1 | All CCF script skills | PROPOSED |
| DEP-ENG-017 | Audience Maturity Profile | audience\_maturity.json | Tier 1 | Batch Composer, Assembler | PROPOSED |
| DEP-ENG-018 | Mood Context Map | mood\_context\_map.json | Tier 2 | Smart Mix, Batch Engine | PROPOSED |
| DEP-ENG-019 | Session Transcript Intelligence | transcript\_intel.json | Tier 2 | Context Premise Output 3 | PROPOSED |
| DEP-ENG-020 | Fingerprint Archive Index | fingerprint\_archive.json | Tier 3 | All compiled skills | PROPOSED |

**New Registrations — Category 2: Component Library**

| Proposed DEP ID | Name | File | Tier | Required By | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| DEP-LIB-008 | Archetype Classification Library | archetype\_psych\_map.yaml | Tier 0 | Orchestrator routing | PROPOSED |
| DEP-LIB-009 | Compiled Skill Template Registry | skill\_template\_registry.yaml | Tier 0 | Design Brief Builder | PROPOSED |

**New Registrations — Category 3: Protocols & Quality Gates**

| Proposed DEP ID | Name | Enforced By | Required By | Status |
| :---- | :---- | :---- | :---- | :---- |
| DEP-PROTO-011 | Semantic Affinity Guard Protocol | Batch Compiler, Assembler | All Escape Mode scripts | PROPOSED |
| DEP-PROTO-012 | Fingerprint Scoring Protocol | Archive Engine | All compiled skills | PROPOSED |
| DEP-PROTO-013 | Anti-Draft Calibration Protocol | Contrastive Anchor Adapter | All generation skills | PROPOSED |

**Updated Topological Sort — Tier 0 Additions**

Two new Tier 0 constants must be added to the build order. These are static libraries with zero upstream dependencies that must exist before any skill compilation begins:

* DEP-LIB-008 Archetype Classification Library — the 8-variable psychological mapping for all archetypes in framework\_archetype\_mapping.yaml

* DEP-LIB-009 Compiled Skill Template Registry — the index of all Archetype Design Brief Templates with their maturity status and last-compiled fingerprint

* DEP-PROTO-011 through 013 — all three new protocols join the existing DEP-PROTO-\* entries in Tier 0

| GHOST VARIABLE RULE *Every field in every Design Brief Template that references a data source MUST have a formal DEP ID. If no DEP ID exists, the field cannot be marked CRITICAL — it must be marked PROPOSED and the registration must be completed before the template reaches TESTED maturity.* |
| :---- |

**03\. Adapter Registry v2.0 — Three New Psychological Adapters**

The current Adapter Registry contains 5 adapters that govern execution structure and reasoning depth. None of them know anything about psychological state, mood routing, arousal calibration, or semantic affinity risk. This is the gap that makes the current system psychologically blind — it can produce structurally excellent skills that serve the wrong psychological mode to the wrong audience state and damage the relationship it was designed to build.

Three new adapters are required. They join the existing 5 as Tier 2 (Deep Reasoning Injection) conditional adapters — invoked only for CCF script-generating skills, not for CMF, CBCS, or V2WS skills where psychological routing is not the primary concern.

**Adapter 6: Psychological Routing Adapter (psych-routing-adapter)**

| Property | Value |
| :---- | :---- |
| Adapter ID | psych-routing-adapter |
| Execution Tier | Deep/Premium |
| Mandatory For | ALL CCF script-generating skills |
| Inputs | Approved Design Brief field\_3\_context \+ DEP-ENG-016 Psychological Routing Brief |
| Output | Adapted psychological pre-generation constraint block |

Adaptation Targets:

* Mood State Calibration — translates mood\_state \+ arousal\_direction \+ valence\_delivery into specific sentence rhythm rules, empathy marker requirements, and energy escalation patterns. Processing Mode: rhythm lengthens, TMT function activates. Escape Mode: semantic affinity guard activates, vehicle-first construction mandated. Discovery Mode: cognitive reward must precede emotional payload. Status Mode: comparison mechanism governs close.

* Regulatory Frame Hook Engineering — translates regulatory\_frame into hook construction rule. Promotion: hook leads with what becomes possible. Prevention: hook leads with what is at risk. Derived from Lee & Aaker (2004) finding that regulatory fit mismatches produce friction regardless of content quality.

* SDT Need Alignment — maps sdt\_need\_primary to the dominant psychological register of the piece. Relatedness (Processing): neural coupling language. Competence (Discovery): mastery signal. Autonomy (Status): identity expression. Relief (Escape): deactivation and release.

*⬡  Regulatory Focus Theory (Higgins, 1997): Regulatory fit between message framing and audience motivational orientation produces a 'feeling right' phenomenon — misattributed to content quality. Fit amplifies perceived quality by up to 26% in interaction time (Cesario, Grant & Higgins, 2004).*

*⬡  Self-Determination Theory (Deci & Ryan, 1985): Consistent need satisfaction (Autonomy, Competence, Relatedness) builds genuine intrinsic motivation toward the content source — converting casual followers into advocates over time.*

**Adapter 7: Payload Masking Adapter (payload-masking-adapter)**

| Property | Value |
| :---- | :---- |
| Adapter ID | payload-masking-adapter |
| Execution Tier | Deep/Premium |
| Mandatory For | All CCF script skills with mood\_state ≠ Processing |
| Inputs | mood\_state \+ archetype\_id from Design Brief |
| Output | Trojan Horse construction instruction for Emilio generation agent |

The Payload Masking Adapter operationalizes Zillmann's Excitation Transfer mechanism. Residual arousal from an initial high-affect stimulus (humor, surprise, entertainment) is misattributed to the emotional response triggered by the subsequent L3 payload — amplifying the perceived impact of the truth. The adapter generates the specific masking instruction for each archetype × mood combination:

* Escape Mode: L3 payload arrives as vehicle resolution subtext. Vehicle must function as standalone entertainment. Truth is the punchline, not the lesson. Semantic Affinity Guard activates automatically.

* Discovery Mode: L3 payload embedded in the resolution of a genuinely surprising counter-intuitive entry point. Audience receives cognitive reward (competence satisfaction) before emotional payload.

* Status Mode: L3 truth encoded in the comparison mechanism — what the winner understood, what the tier list reveals. Never stated as explicit lesson. Comparison type (upward assimilation, downward, worldview validation) governs close.

* Processing Mode: No masking. Payload IS the content. Direct engagement with the L3 truth is the point. TMT Worldview Construction function may activate for loyal cohort.

*⬡  Mood Management Theory (Zillmann, 1988): Non-conscious affective homeostasis governs content selection. High semantic affinity between content and active stress domain is actively counterproductive for mood repair — the system must detect and block this combination.*

*⬡  Excitation Transfer (Zillmann, 1971): Residual physiological arousal from one stimulus amplifies the emotional response to a subsequent stimulus. Humor as primer for deep payload is not a stylistic choice — it is a neurological amplification mechanism.*

**Adapter 8: Audience Maturity Adapter (audience-maturity-adapter)**

| Property | Value |
| :---- | :---- |
| Adapter ID | audience-maturity-adapter |
| Execution Tier | Standard |
| Mandatory For | All CCF script skills |
| Inputs | audience\_cohort from Design Brief \+ DEP-ENG-017 Audience Maturity Profile |
| Output | Depth permission level \+ batch allocation modifier |

The Audience Maturity Adapter translates cohort classification into a depth permission level that governs how much psychological weight the skill can carry in its Implication phase and whether TMT Worldview Construction function is permitted:

| Cohort | Depth Permission | Processing Allocation | TMT Function | Broaden-and-Build Status |
| :---- | :---- | :---- | :---- | :---- |
| New (0-4wk) | Surface | 10% | insight\_delivery only | Not yet seeded — build positive affect first |
| Developing (4-16wk) | Mid | 25% | insight\_delivery | Active — cognitive scope broadening in progress |
| Loyal (16wk+) | Full | 50% | worldview\_construction permitted | Mature — advocate behavior possible |

*⬡  Broaden-and-Build Theory (Fredrickson, 1998): Positive emotions literally expand cognitive scope. New audiences need consistent Escape/Discovery content to build the neurological capacity for Processing Mode depth. Forcing depth too early lands in a narrowed, defensive state.*

*⬡  Terror Management Theory (Greenberg et al., 1986): worldview\_construction function produces advocate behavior — the audience defends the coach's framework as their own. This is only possible after sustained engagement has built worldview investment.*

**04\. Design Brief Builder Engine — Phase 1 Compiler**

The Design Brief Builder Engine is the Phase 1 system that produces validated, compilation-ready Design Briefs from Archetype Templates. It is not the same as the CCSB Phase 1 Orchestrator — that agent handled general skill creation. The Builder Engine is specifically designed for JIT compiled script skills, where the template provides the invariant Block A and the Builder's job is to correctly populate Block B and validate the complete brief through Block C before handing to the Assembler.

**Builder Engine Architecture**

The Builder operates as a 5-step process with two hard gates:

| INPUT: Archetype ID \+ Runtime Parameters STEP 1 — TEMPLATE LOAD   Load Archetype Design Brief Template from DEP-LIB-009   Verify template maturity ≥ tested   Load Block A (invariants) — read-only STEP 2 — RUNTIME PARAMETER INJECTION   Populate Block B fields from runtime context:     coach\_id → resolve DEP-LIB-001, DEP-ENG-002, DEP-ENG-003, DEP-ENG-004     mood\_state → from DEP-ENG-016 Psychological Routing Brief     audience\_cohort → from DEP-ENG-017 Audience Maturity Profile     output\_format → from batch strategy     regulatory\_frame → from DEP-ENG-016     semantic\_affinity\_risk → from DEP-PROTO-011 Guard output GATE 1 — DEP RESOLUTION CHECK   All CRITICAL tier DEP IDs must resolve in registry   FAIL → return structured rejection, do not proceed STEP 3 — PSYCHOLOGICAL ROUTING BRIEF GENERATION   If DEP-ENG-016 not yet populated for this batch:     Run Psychological Routing Brief Generator     Inputs: DEP-ENG-006 (L3 pain domain), DEP-ENG-018 (Mood Context Map)     Output: psych\_routing\_brief.json for this specific batch slot STEP 4 — SEMANTIC AFFINITY PRE-CHECK   Cross-reference content domain vs active L3 pain domain   IF semantic\_affinity\_risk \= high AND mood\_state \= Escape → BLOCK   Return: affinity\_mode\_conflict \+ reclassification instruction GATE 2 — BLOCK C VALIDATION   Run all compilation validation rules   TTT hardcoding check (reject if present)   TMT/cohort mismatch check (downgrade if needed)   All required Block B fields populated   FAIL → structured rejection with specific failed checks STEP 5 — BRIEF FINALIZATION   Assign Compilation Request ID (see Section 7\)   Write validated brief to queue   Return: compilation\_request\_id \+ brief\_path |
| :---- |

**The Psychological Routing Brief Generator**

This is the sub-process within Step 3 that produces DEP-ENG-016 for each batch slot. It runs the following logic against the available intelligence tier:

| Intelligence Tier | Routing Brief Source | Confidence Level | Guard Behavior |
| :---- | :---- | :---- | :---- |
| Tier 1 — Research Only | Probabilistic inference from L1/L2/L3 Context Premise | \~60% | Guard runs on inferred pain domain |
| Tier 2 — Transcript Intelligence | LIWC-22 extraction from session transcripts | \~85% | Guard runs on empirically confirmed pain domain |
| Tier 3 — Full CBCS+Session+Journal | Live psychometric state vector per cohort | \~100% | Guard runs on real-time confirmed pain domain |

*⬡  Uses & Gratifications Theory (Katz, Blumler & Gurevitch, 1973): Instrumental vs. ritualistic media use patterns vary by time-of-day, platform, and audience segment. Tier 1 routing inference uses these population-level patterns as probabilistic priors.*

*⬡  LIWC-22 (Pennebaker et al., 2022): Linguistic Inquiry and Word Count analysis produces validated psychometric state vectors from natural language. First-person singular frequency, hedging shifts, and negative emotion markers are empirically validated indicators of regulatory orientation and arousal state.*

**05\. JIT Skill Assembler v2.0 — Resilient Phase 2 Compiler**

The current CCBS Skill Assembler has four structural vulnerabilities: single point of execution (one adapter failure halts everything), blind repair (one retry pass with no diagnosis logic), no fallback for unregistered adapters, and no pre-flight gate. The v2.0 assembler addresses all four through a tiered isolation architecture with diagnostic repair and deployment quarantine.

**The Four-Tier Execution Model**

| INPUT: Validated Design Brief (from Builder Engine) \+ Compilation Request ID TIER 0 — PRE-FLIGHT (zero generation, zero tokens)   Run Block C validation rules from brief   Verify all CRITICAL DEP IDs resolve   Check DEP-ENG-016 exists and is populated   Check DEP-ENG-003 status ≠ empty   Check DEP-ENG-006 L3 layer ≥ 10% threshold   Check DEP-ENG-010 has ≥1 archetype-tagged passage   FAIL → REJECTED status, return diagnostic JSON, do not proceed TIER 1 — MANDATORY ADAPTERS (parallel execution)   irevc-adapter   negative-space-loader-adapter  ← Load DEP-ENG-004 FIRST   pre-generation-constraints-adapter   graceful-degradation-adapter   psych-routing-adapter          ← NEW: always for CCF script skills   audience-maturity-adapter      ← NEW: always for CCF script skills   FAIL any mandatory → HALT with specific adapter diagnostic   Do not proceed to Tier 2 TIER 2 — CONDITIONAL ADAPTERS (parallel, isolated)   Each adapter runs independently   distillation-funnel-adapter    (if in modules field)   contrastive-anchor-adapter     (if in modules field)   deliberation-adapter           (if in modules field)   voice-separation-adapter       (if in modules field)   payload-masking-adapter        (if mood\_state ≠ Processing)   semiotic-filter-adapter        (if in modules field)   mcda-adapter                   (if in modules field)   Unregistered modules → MANUAL\_ADAPTATION\_REQUIRED flag   Individual failures → flag \+ proceed with others TIER 3 — SECTION ASSEMBLY (section-by-section, isolated)   Each of 10 SKILL.md sections assembled independently   Section failure → \[MANUAL\_COMPLETION\_REQUIRED: reason\] placeholder   Assembly always completes — never halts mid-document POST-ASSEMBLY — VALIDATION \+ DIAGNOSTIC REPAIR   Run 6 structural checks \+ 5 psychological checks (NEW)   Failure → diagnostic repair (REGENERATE | ESCALATE | RERUN)   Maximum 1 targeted repair per failing section OUTPUT: SKILL.md \+ assembly\_report.json \+ deployment\_status   COMPLETE → deployable   PARTIAL\_AUTO → deployable with logged gaps   PARTIAL\_MANUAL → quarantined, human completion required   REJECTED → never started, returned to Builder Engine |
| :---- |

**New Post-Assembly Validation Checks (Psychological Layer)**

Five new checks join the existing six structural checks. These are the quality gates that ensure the psychological routing architecture was correctly compiled into the skill:

| Check ID | Name | Pass Condition | Fail Action |
| :---- | :---- | :---- | :---- |
| PC-01 | Mood State Calibration Injection | psych-routing-adapter output present in Reasoning Architecture section | RERUN psych-routing-adapter |
| PC-02 | Payload Masking Instruction | Masking instruction present for non-Processing Mode | RERUN payload-masking-adapter |
| PC-03 | Semantic Affinity Guard | Guard rule present in Negative Space section | REGENERATE Negative Space section |
| PC-04 | Regulatory Frame Hook Rule | Hook engineering rule present in Pre-Generation Constraints | REGENERATE Constraints section |
| PC-05 | TMT/Cohort Alignment | tmt\_function matches audience\_cohort permission level | ESCALATE\_TO\_MANUAL — requires human review |

**Diagnostic Repair Protocol**

The current assembler's 'maximum 1 repair pass' is blind — it retries without knowing why the check failed. The v2.0 diagnostic repair protocol classifies every failure before acting:

| Failure Type | Root Cause | Repair Action | Max Passes |
| :---- | :---- | :---- | :---- |
| Generation quality failure | Output produced but below threshold (too few items, wrong format) | REGENERATE\_SECTION with explicit gap in instruction | 1 |
| Missing input failure | A CRITICAL input was absent or empty | ESCALATE\_TO\_MANUAL — cannot synthesize critical inputs | 0 — immediate escalation |
| Adapter output integration failure | Adapter produced output but assembly mapping failed | RERUN\_ADAPTER with diagnostic context | 1 |
| Ontological boundary violation | SKILL.md contains routing logic or agent language | REGENERATE\_SECTION with explicit prohibition | 1 |

**Deployment Quarantine Rule**

| RULE: No compiled skill may enter the active pipeline without its assembly\_report.json being read by the Orchestrator. If assembly\_status \= PARTIAL\_MANUAL or REJECTED, the skill is QUARANTINED. It cannot be invoked until all MANUAL\_COMPLETION\_REQUIRED sections are resolved and the report is updated to COMPLETE or PARTIAL\_AUTO. The Orchestrator reads the report, not just the skill. |
| :---- |

*⬡  Evolving PSN (Shi et al., 2025): Online refactoring (coupled with real execution failures) achieves 84.6% success rate vs. 68.75% for offline batch rewrites. The quarantine system enforces online refinement — skills only deploy after real validation, not theoretical correctness.*

**06\. Module Library — Container Intelligence for Every Archetype**

The Module Library for Containers is the highest-leverage investment in the entire JIT Compiler system. It encodes the structural intelligence of each content archetype — the institutional knowledge that currently lives only in experienced authors' heads — into formally specified, ecologically adaptable modules. A better module improves every compiled skill that references it. The improvement is automatic, not something that requires updating 22 individual skills.

Each Archetype Module in the library contains three components, following the CCSB Module Architecture specification: Core DNA (the universal structural procedure), Adaptation Protocol (how to mutate it per compilation context), and Reference Example (a production mutation showing the correct output for a known archetype × coach × mood combination).

**The Container Module Taxonomy — All Archetype Families**

| Family | Archetypes | Core DNA | Primary Structural Law |
| :---- | :---- | :---- | :---- |
| Storytelling | Achievement, Transformation, Inspiration, Relief, Surprise | 5-phase narrative arc | Stakes ceiling \= emotional ceiling of Turn phase |
| Listicle | Shocking, Funny Relatable, Nostalgia, Fear-Anxiety, Curiosity, Hope | Hook → Item sequence → Payload close | First item must earn the list. Last item must earn the read. |
| Case Study | Surprising, Inspirational, Relatable, FOMO, Social Proof | Evidence → Mechanism → Implication | Result must be falsifiable. Mechanism must be transferable. |
| Comparison | Shocking, Funny, Surprising, Outrageous, Nostalgia | Delta definition → Contrast execution → Resolution | Delta must be structural, not superficial. Resolution must resolve the tension. |
| Myth & Scam | Indignation, Curiosity, Empowering, Fear-Anxiety | Belief established → Evidence contradicts → New frame installed | The myth must be real and widely held. Debunk with mechanism not opinion. |
| Tier List | Authority, Controversial, Relatable, Nostalgia, Red Flag | Ranking logic → Criteria → Verdicts | Criteria must be stated before verdicts. Hidden criteria \= credibility loss. |
| Core Formats | Dopamine Cliff, Relief Peak, Persuasive Tweet | Arc-specific: aspiration→reality / pain→solution / single truth | Transition point is the structural hinge. It cannot be telegraphed. |

**What Each Container Module Must Contain**

Every Container Module in the library is a SKILL.md in its own right — stored in \`intelligence/modules/containers/{archetype-id}/MODULE.md\`. It contains:

* Core DNA block — the universal structural procedure, expressed as named phases with their structural laws. Archetype-invariant. Never modified after reaching STABLE maturity.

* Ecological Adaptation Protocol — explicit instructions for how each of the 4 Distillation Funnel laws mutates in this archetype's domain. What does Compression mean for a Tier List vs. an Achievement Story? This must be defined explicitly per Directive 8\.

* Contrastive Anchor Calibration — the precise archetypal failure mode for this archetype. What does generic AI output look like for a Surprise Story vs. a Fear-Anxiety Listicle? The negative baseline must be domain-specific.

* Mood State Interaction Matrix — how each of the 4 mood states changes the execution of this specific archetype. A Shocking Listicle in Escape Mode vs. Processing Mode requires fundamentally different construction. This matrix is the archetype's psychological routing intelligence.

* Payload Masking Default — the default Trojan Horse construction instruction for this archetype per mood state. Achievement Story in Discovery Mode always opens with a counter-intuitive historical fact about success. This is the archetype's compiled masking default.

* Reference Production Example — one fully assembled Block A \+ Block B Design Brief showing a complete compilation for a known archetype × mood × coach combination. This is the 'shot' that anchors the Assembler's L3 execution quality.

**The Mood State Interaction Matrix — Core Design Principle**

Every Container Module must encode how all four mood states change the archetype's execution. This is the most important new addition to the Module Library — it is what makes the JIT Compiler psychologically calibrated rather than structurally competent. The matrix for Achievement Story:

| Mood State | Hook Engineering | Arc Modification | Payload Delivery | Semantic Affinity Risk |
| :---- | :---- | :---- | :---- | :---- |
| Processing | Stakes-first, direct L3 entry | Full 5-phase arc, TMT function may activate | Implication \= direct existential parallel | HIGH — appropriate for this mode |
| Escape | Vehicle-first (humor/absurdity), Stakes buried | Arc compressed into vehicle resolution | Truth arrives as punchline in phase 5 | HIGH — GUARD ACTIVATES, domain swap required |
| Discovery | Counter-intuitive fact opens (mechanism as surprise) | Stakes revealed through fact resolution | Implication \= competence reward \+ L3 parallel | LOW — entry domain is semantically distant |
| Status | Achievement framed as comparison signal | Mechanism \= what winners know that others don't | Implication \= identity marker, not lesson | MEDIUM — flag if active stress \= achievement pressure |

*⬡  Social Comparison Theory (Festinger, 1954): Upward assimilation (Status Mode inspiration) requires explicit pathway framing or it flips to contrast and produces envy. The Mood State Interaction Matrix for Status Mode must always specify whether the comparison mechanism is upward assimilation, downward, or worldview validation — and construct accordingly.*

**07\. Fingerprint Archive — Skill ID System and Performance Memory**

Every compiled skill needs a unique, trackable, human-readable ID that links it to: (1) the archetype template it was compiled from, (2) the coach and psychological context it was compiled for, (3) every content output it ever produced, and (4) every performance signal those outputs generated. Without this linkage, the system cannot learn. It produces skills, observes outputs, and has no mechanism to connect a viral piece of content back to the specific compiled skill that produced it.

**The Skill Fingerprint ID Schema**

| SKILL-{ARCH\_ID}-{COACH\_ID}-{MOOD}-{REG\_FRAME}-{COHORT}-{YYYYMMDD}-{SEQ} Components:   ARCH\_ID      \= Archetype identifier (STORY01, LIST02, CASE03, etc.)   COACH\_ID     \= Coach short ID (3-4 chars from coach\_soul.json)   MOOD         \= P (Processing) | E (Escape) | D (Discovery) | S (Status)   REG\_FRAME    \= PRO (promotion) | PRV (prevention)   COHORT       \= N (new) | DEV (developing) | L (loyal)   YYYYMMDD     \= Compilation date   SEQ          \= Sequential number for same-day compilations Examples:   SKILL-STORY01-EMI-P-PRV-L-20260315-001     Achievement Story / Coach Emilio / Processing / Prevention / Loyal / March 15   SKILL-LIST02-ANA-E-PRO-N-20260315-001     Shocking Listicle / Coach Ana / Escape / Promotion / New / March 15   SKILL-CLIFF07-MAR-D-PRO-DEV-20260315-001     Dopamine Cliff / Coach Maria / Discovery / Promotion / Developing / March 15 |
| :---- |

**The Fingerprint Archive Structure**

Every compiled skill's fingerprint is registered in DEP-ENG-020 (fingerprint\_archive.json) with the following schema:

| {   'skill\_id': 'SKILL-STORY01-EMI-P-PRV-L-20260315-001',   'archetype\_template\_id': 'ARCH-STORY-01',   'archetype\_template\_version': '1.1',   'compilation\_date': '2026-03-15',   'maturity': 'draft',   'assembly\_status': 'COMPLETE',   'context': {     'coach\_id': 'EMI',     'mood\_state': 'Processing',     'regulatory\_frame': 'prevention',     'audience\_cohort': 'loyal',     'tmt\_function': 'worldview\_construction',     'sdt\_need\_primary': 'relatedness'   },   'dep\_snapshot': {     'DEP-ENG-003': 'hash\_of\_emotional\_dna\_used',     'DEP-ENG-006': 'hash\_of\_context\_premise\_used',     'DEP-ENG-016': 'hash\_of\_psych\_routing\_brief\_used'   },   'outputs': \[\],   'performance\_scores': {},   'promoted\_to\_stable': false } |
| :---- |

**Output Linkage — Connecting Skill to Content Performance**

When a compiled skill produces a content output, the output is registered against the skill fingerprint:

| 'outputs': \[   {     'output\_id': 'OUT-STORY01-EMI-20260316-001',     'content\_title': 'The day I got promoted was the loneliest day of my career',     'platform': 'instagram',     'published\_date': '2026-03-16',     'performance': {       'saves': 2847,       'shares': 1203,       'comments': 892,       'reach': 147000,       'engagement\_rate': 0.034,       'viral\_quartet\_score': 4.2     },     'audience\_signals': {       'dm\_vulnerability\_ratio': 0.18,       'comment\_depth\_score': 3.4,       'save\_to\_share\_ratio': 2.37     }   } \] |
| :---- |

**Promotion Protocol — From Draft to Stable**

A compiled skill advances through maturity tiers based on production evidence, following Evolving PSN's empirically validated thresholds:

| Maturity Tier | Promotion Requirement | Behavioral Impact | Modification Rule |
| :---- | :---- | :---- | :---- |
| Draft | Newly compiled — no production history | High plasticity, free iteration | Accept breaking changes |
| Tested | 3+ production outputs without assembly failure | Medium plasticity | Changes require written justification |
| Stable | 10+ outputs across diverse inputs, ≥1 high-performer (saves \>2x category average) | Low plasticity — locked | Only structural augmentation, full regression review required |
| Reference | Stable \+ promoted to Module Library as canonical production example | Immutable except by Architecture Review | Changes require new version with old preserved |

A skill that reaches Reference tier contributes its complete Block A \+ Block B compilation back to the Archetype Design Brief Template as an updated Reference Example — closing the learning loop. The next compilation using the same archetype × mood × coach combination starts from a known working baseline rather than first principles.

*⬡  SkillNet (Liang et al., 2026): Formalizing skills as evolving, composable assets with performance tracking enables 40% agent performance improvement. The improvement mechanism is the feedback loop — skills that worked inform the next generation of skills that will work.*

*⬡  Agent Skills benchmark (Li et al., 2025): Curated agent skills boost LLM performance by \+16.2 percentage points on average. Self-generated skills without curation offer zero gain. The Fingerprint Archive is the curation mechanism.*

**08\. Anti-Draft Intelligence — Contrastive Prompting as the Last Defence**

The compiled skill is the last intervention point before content generation. Everything before it — Emotional DNA extraction, Trigger-First activation, Context Premise, Psychological Routing — can be architecturally perfect. If the skill itself doesn't contain a precisely calibrated negative baseline, the generation agent (Emilio) will produce the statistical centroid of everything in its training data that matches the skill's positive instructions. That centroid is always mediocre. It passes every surface check and fails every depth test.

Contrastive prompting with Anti-Drafting is not a nice-to-have quality layer. It is the immune system of the generation process. Ling et al. (2023) established the Law of the Negative Anchor: providing explicitly generated invalid examples forces the LLM away from mean reversion. The skill must not just say what good looks like — it must generate what bad looks like, explain exactly why it fails, and then instruct Emilio to maximize semantic distance from that baseline.

**The Three-Level Anti-Draft Architecture**

Anti-drafting operates at three levels in every compiled skill. Each level catches a different failure mode:

**Level 1 — Archetype-Level Anti-Draft (from Container Module, Block A)**

This is the generic AI failure mode for this specific archetype. It is pre-written in the Container Module and arrives in every compiled skill that uses this archetype unchanged. It answers: what does a mediocre version of this archetype look like?

| ACHIEVEMENT STORY — ARCHETYPE-LEVEL ANTI-DRAFT *Generic AI Achievement Story: 'I worked incredibly hard and never gave up. After months of struggle, I finally achieved my goal. The lesson I learned is that persistence pays off. You can do this too if you believe in yourself.' WHY THIS FAILS: Mechanism is non-transferable (persistence/belief), result is impressionistic, implication is generic inspiration. This is the statistical centroid. The generation must be maximally distant from it.* |
| :---- |

**Level 2 — Psychological Mode Anti-Draft (from Payload Masking Adapter, Block B)**

This is the failure mode specific to the compiled mood state × archetype combination. It answers: what does a bad Escape Mode Achievement Story look like? This cannot be pre-written in the template — it requires the compilation context to be meaningful.

| ACHIEVEMENT STORY × ESCAPE MODE — MODE-LEVEL ANTI-DRAFT *Mode failure: An Achievement Story in Escape Mode that announces its payload. 'I used to hustle myself into the ground. I learned that rest is actually productive. Here's what changed for me...' WHY THIS FAILS: The topic (hustle culture, achievement anxiety) has HIGH semantic affinity to the audience's primary stress domain. The payload is stated not earned. The vehicle (story) adds more emotional weight rather than releasing it. The audience came to escape this exact conversation.* |
| :---- |

**Level 3 — Coach-Specific Anti-Draft (from Voice Separation Adapter, Block B)**

This is the failure mode for this specific coach's voice. It answers: what does Emilio produce when it has the right structure but falls back to the coach's worst patterns? This is extracted from DEP-ENG-004 Negative Space Object and the coach's authenticated baseline. It is the most precise anti-draft and the one most likely to catch the subtle failures that survive Levels 1 and 2\.

| COACH-SPECIFIC ANTI-DRAFT EXAMPLE *Coach Emilio's voice drift pattern: When uncertain, defaults to numbered list structure ('3 things I learned...'). Produces hedged implication closes ('maybe this isn't for everyone, but...'). Imports professional vocabulary when authentic language would be blunter. These are the exact patterns DEP-ENG-004 encodes as forbidden — the anti-draft makes them visible so the generation actively repels them.* |
| :---- |

**The Contrastive Instruction Architecture**

Once all three anti-draft levels are assembled, the compiled skill contains a structured contrastive block that Emilio reads before generating any output. The block has four components:

* NEGATIVE DEMONSTRATION — The actual bad output text. Not described. Written. 3-5 sentences of exactly what the generation must not produce. Making the failure mode concrete activates semantic repulsion rather than abstract avoidance.

* FAILURE DIAGNOSIS — One sentence per failure mode identifying the exact constraint violation. Why does each element of the bad output fail? The diagnosis trains Emilio's evaluation of its own draft.

* SEMANTIC DISTANCE INSTRUCTION — The explicit calculation of distance required. 'Your output must not share vocabulary, structural pattern, or emotional register with the negative demonstration above. Maximum distance from the statistical mean is the target, not merely exceeding it.'

* FORBIDDEN VOCABULARY LIST — From DEP-ENG-004 plus the mode-specific additions. Words, phrases, and structural patterns that are specifically banned for this compilation. Not general rules — exact strings.

**Draft → Anti-Draft → Synthesis Loop**

The contrastive architecture integrates with the Deliberation Adapter to create a three-pass generation quality loop for every compiled script skill:

| PASS 1 — DRAFT GENERATION   Emilio generates initial script following all positive constraints   Chain-of-Draft reasoning: each logical step ≤5 words before full generation   Output: draft\_v1.md PASS 2 — ANTI-DRAFT EVALUATION (Critic Subagent)   Spawn Critic Subagent with anti-draft block as primary context   Critic evaluates draft\_v1 against all three anti-draft levels:     Level 1: Is any element of the Archetype Anti-Draft present?     Level 2: Is the mode failure pattern present?     Level 3: Are any coach-specific drift patterns present?   Critic also runs structural gates from field\_11\_structural\_success\_criteria   Output: critic\_report.json with specific flagged elements PASS 3 — SYNTHESIS   IF Critic flags ≥2 violations → full regeneration with critic report as constraint   IF Critic flags 1 violation → targeted revision of flagged element only   IF Critic flags 0 violations → confirm draft, proceed to Voice Distiller   Log: deliberation\_override: true/false   Output: final\_script.md \+ deliberation\_log.json |
| :---- |

*⬡  Contrastive Chain-of-Thought Prompting (Ling et al., 2023): Positive-only examples allow the model to satisfy surface patterns while violating deep constraints. Pairing every example with a contrastive negative closes this gap. The failure mode must be as specifically generated as the target mode.*

*⬡  SkillFactory Self-Distillation (Deng et al., 2025): Cognitive behaviors reliably transfer between LLM instances when explicitly tagged with structural markers. The Draft→Critic→Synthesis loop must use explicit headers (\#\#\# DRAFT PHASE, \#\#\# CRITIC PHASE, \#\#\# SYNTHESIS PHASE) — not flowing prose. Structure forces the cognitive behavior; prose allows it to be skipped.*

**09\. Mood State Architecture Integration — End-to-End Wiring**

The Psychological Routing & Mood State Architecture has been fully theorized and academically grounded across 7 papers. The gap is operational wiring — which system reads what, when, in what order, and what happens when the routing produces a conflict. This section maps the complete end-to-end flow from audience state detection through to compiled skill deployment.

**The Five-Stage Routing Flow**

| STAGE 1 — MOOD CONTEXT DETECTION   Source: DEP-ENG-018 Mood Context Map   Inputs: DEP-ENG-006 (L3 pain domain) \+ DEP-ENG-019 (transcript intel if available)   Output: Probability distribution across 4 mood states for this batch window   Intelligence Tier 1: probabilistic from contextual signals   Intelligence Tier 2+: empirical from LIWC-22 transcript analysis STAGE 2 — AUDIENCE MATURITY CLASSIFICATION   Source: DEP-ENG-017 Audience Maturity Profile   Input: Engagement depth signals (saves, DMs, comment vulnerability, replay)   Output: Cohort classification (new/developing/loyal) \+ batch allocation percentages   Note: Behavioral signals override calendar-time thresholds STAGE 3 — PSYCHOLOGICAL ROUTING BRIEF GENERATION   Source: DEP-ENG-016 (produced by Design Brief Builder Engine Step 3\)   Inputs: Stage 1 output \+ Stage 2 output \+ DEP-ENG-006 L3 data   Output: psych\_routing\_brief.json per batch slot   Fields: mood\_state, arousal\_direction, valence\_delivery, regulatory\_frame,            sdt\_need\_primary, semantic\_affinity\_risk, tmt\_function, audience\_cohort STAGE 4 — SEMANTIC AFFINITY GUARD   Protocol: DEP-PROTO-011   Inputs: psych\_routing\_brief.json \+ DEP-ENG-006 active L3 pain domain   Logic: IF semantic\_affinity\_risk \= HIGH AND mood\_state \= Escape → BLOCK           IF semantic\_affinity\_risk \= HIGH AND mood\_state \= Processing → PERMIT           IF semantic\_affinity\_risk \= MEDIUM AND mood\_state \= Escape → FLAG   Output: Guard decision \+ reclassification instruction if blocked STAGE 5 — COMPILATION TRIGGER   DEP-ENG-016 (validated, Guard-cleared) → Design Brief Builder Engine   Builder injects psych\_routing\_brief into Block B field\_3\_context   Block C validation includes Stage 4 Guard decision   Validated brief → JIT Skill Assembler v2.0   Assembled skill contains fully wired psychological intelligence |
| :---- |

**Batch Composition Engine Integration**

The Mood State Architecture governs not just individual skills but the composition of the full batch. The Smart Mix Synthesis Protocol (DEP-PROTO-006) must be updated to read from DEP-ENG-017 and DEP-ENG-018 before assembling batch allocations:

| Cohort | Processing | Escape | Discovery | Status | Sequencing Rule |
| :---- | :---- | :---- | :---- | :---- | :---- |
| New | 10% | 40% | 30% | 20% | Escape before Discovery (Broaden-and-Build priming) |
| Developing | 25% | 35% | 20% | 20% | Escape/Discovery can precede Processing (upward spiral active) |
| Loyal | 50% | 20% | 15% | 15% | Processing-forward, Escape as tension release only |

**The Upward Spiral as Platform Strategy**

The Audience Maturity Lifecycle is not passive observation — it is an active training protocol that the batch composition engine must be designed to execute. Fredrickson and Joiner (2002) established that positive emotions and broadened thinking are mutually reinforcing over time. Each Escape/Discovery Mode piece that lands successfully builds the cognitive capacity to receive the next Processing Mode piece. The batch composition engine, when correctly calibrated, is systematically training the audience toward greater depth over time — not just serving them where they are.

This has a specific implication for compiled skill deployment: the Fingerprint Archive should track not just individual skill performance but cohort-level progression signals. If a coach's developing cohort is showing loyalty-cohort behavioral signals (save rates, DM depth, comment vulnerability) earlier than the 16-week threshold, the Audience Maturity Adapter should advance their classification immediately — not wait for calendar time to expire.

*⬡  Broaden-and-Build Theory (Fredrickson & Joiner, 2002): The upward spiral is documented empirically — each iteration of broadened thinking increases likelihood of positive emotion, which further broadens thinking. Applied to content: the batch composition engine is a neurological training system for audience cognitive capacity, not just a content distribution schedule.*

*⬡  Terror Management Theory (Burke, Martens & Faucher, 2010): When worldview investment activates (loyal cohort, Processing Mode, worldview\_construction function), the audience begins defending the coach's framework as their own worldview. This behavioral state produces advocacy, churn resistance, and referral behavior that no algorithm optimization can replicate.*

**10\. Implementation Sequence — What to Build, In What Order, and Why**

The seven components of the JIT Compiler are interdependent. The build sequence must honor the dependency graph: nothing that references a component can be built before that component exists. The sequence below is the correct topological order, with the scientific rationale for each step.

| Step | Build Target | Unblocks | Estimated Effort | Why This Order |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Dependency Registry v4.0 — add 8 new DEP IDs | Everything. All templates reference DEP IDs. | ½ day | Ghost variable prevention. No template can reach TESTED without valid DEP IDs. |
| 2 | Adapter Registry v2.0 — add 3 psychological adapters | Assembler v2.0, all CCF compiled skills | 1 day | Adapters must exist before Assembler can invoke them. Adapter before consumer. |
| 3 | DEP-PROTO-011 Semantic Affinity Guard — define protocol | Builder Engine Stage 4, all Escape Mode skills | ½ day | Guard must exist before any Escape Mode brief can pass Block C validation. |
| 4 | DEP-LIB-008 Archetype Classification Library — populate 8-variable YAML for all 22+ archetypes | Orchestrator routing, all Design Brief Templates | 2 days | This is the routing database. Templates reference it. Must pre-exist templates. |
| 5 | Container Module Library — Block A for all archetype families (7 families, 30+ archetypes) | Design Brief Templates, Assembler Section Assembly | 3-4 days | Highest leverage investment. Module quality compounds across all compiled skills. |
| 6 | Design Brief Template Library — full templates for all archetypes using completed modules | Design Brief Builder Engine | 2 days | Templates consume modules. Modules must exist first. |
| 7 | Design Brief Builder Engine — 5-step Phase 1 compiler with psychological routing brief generator | JIT Assembler v2.0 | 2 days | Builder produces the validated briefs the Assembler consumes. |
| 8 | JIT Skill Assembler v2.0 — 4-tier resilient compiler with diagnostic repair | All compiled skill production | 2 days | Assembler consumes validated briefs \+ adapters. Both must pre-exist. |
| 9 | Fingerprint Archive Engine — ID schema \+ DEP-ENG-020 \+ scoring protocol | Performance learning loop | 1 day | Archive can be built in parallel with steps 7-8 but must be active before first production compilation. |
| 10 | First production compilations (pilot: 2 archetypes × 2 coaches × 4 mood states \= 16 skills) | Full pipeline validation | Ongoing | Online validation. Skills compiled, deployed, performance tracked, maturity promoted. |

**The Critical Path**

Steps 1 → 2 → 3 → 4 are the critical path. None of the creative work (modules, templates, builder, assembler) can reach production quality until the four foundational registries are complete and correct. This is the most common failure mode in agentic system builds: architects begin writing skills before the data layer is clean, producing technically impressive work that references variables that don't formally exist.

**What Changes in the PRD as a Result**

The PRD v2.0 update requires three additional imperatives beyond the seven documented in the CCP Evolution Architecture Report v2.0:

* Imperative 8: The CCF pipeline must be updated to include the 5-stage Mood Routing Flow as a mandatory pre-generation stage. No batch slot may receive a compilation trigger without a validated DEP-ENG-016 Psychological Routing Brief.

* Imperative 9: The Smart Mix Synthesis Protocol (DEP-PROTO-006) must be updated to read from DEP-ENG-017 Audience Maturity Profile and enforce cohort-specific batch allocation percentages before assembling the final batch.

* Imperative 10: The Dependency Registry, Adapter Registry, and Fingerprint Archive are declared living documents — they must be updated before any new skill type is introduced into the pipeline. The ghost variable failure mode is structurally prevented by requiring DEP ID registration as a prerequisite to template authoring.

**END OF DOCUMENT**

*CCP Engineering Division  ·  JIT Skill Compiler Architecture v1.0  ·  March 2026*