# Phase 1 — Agent / Skill / Operation Ownership Graph

**Mandate ID:** `M05`  
**Status:** `RATIFIED_INVENTORY_AND_CONTRACTS_BASELINE`  
**Governing Authority:** `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`, `docs/PRD/CURRENT.md` (v0.3.0), `00_CONTROL/05_PROGRAM_PACKAGE_AND_AGENT_CONVENTION.md`  
**Repository Revision:** `2a769677edbece460c0c968ecb325e138003b5f0`  
**Execution Date:** `2026-08-31`  

---

## 1. Constitutional Ownership Principles

1. **Separation of Cognitive Powers**:
   - Every reasoning capability belongs to **exactly one** of the four Authority Lanes (`HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`) or is declared `NOT_APPLICABLE_BY_RULE` (for deterministic infrastructure, storage, or transport).
   - A single agent reasoning loop may never search, critique, compose, and authorize within the same context window.
2. **Passive, Flat Canonical Skills**:
   - Skills are passive transformations (`InputContract` $\to$ `OutputContract`).
   - A Skill may never invoke another Skill (zero Skill nesting). Orchestrators load and execute flat skill arrays JIT.
3. **Deterministic Mutation Boundary**:
   - LLMs, Agents, and Skills produce candidate objects and manifests. State mutations, database transactions, and receipt emissions occur **only** through typed CAE operations (`packages/ca_runtime`, `services/pipeline`, SQL schema `cae`).
4. **Substrate Separation**:
   - Runtime engines (Pi substrate) execute workflows; Eve composition definitions guide packaging. Canonical state remains in CAE databases and verified receipt ledgers.

---

## 2. Complete Lifecycle Capability Ownership Graph

### 2.1 Workspace & Client Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `WS-001` | Workspace Creation & Tenancy Boundary Setup | `NOT_APPLICABLE_BY_RULE` | `WorkspaceAdminTeam` | `workspace-core-init` | `workspace_core.create_workspace()` | `WorkspaceRecord` / `RECEIPT_WORKSPACE_CREATED` |
| `WS-002` | Operator Access Grant & Role Assignment | `COMMANDER` | `WorkspaceCommanderAgent` | `rbac-policy-evaluator` | `workspace_core.grant_operator_access()` | `OperatorAccessGrant` / `RECEIPT_OPERATOR_ACCESS` |
| `WS-003` | RLS Policy & Tenancy Context Binding | `NOT_APPLICABLE_BY_RULE` | `WorkspaceAdminTeam` | `tenant-context-binder` | `workspace_core.set_tenant_context()` | `TenantContextSession` / `RECEIPT_RLS_ENFORCED` |

---

### 2.2 Guest Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `GST-001` | Guest Genesis & Identity Profile Setup | `HUNTER` | `GuestIntakeTeam::Hunter` | `guest-profile-intake` | `guest_core.register_guest()` | `GuestProfile` / `RECEIPT_GUEST_CREATED` |
| `GST-002` | Voice DNA & Authentic Stance Extraction | `ANALYST` | `GuestAnalysisTeam::Analyst` | `voice-dna-analyzer` | `guest_core.record_voice_dna()` | `VoiceDNASpec` / `RECEIPT_VOICE_DNA_RECORDED` |
| `GST-003` | Visual DNA & Brand Expression Boundary | `ANALYST` | `GuestAnalysisTeam::Analyst` | `visual-dna-analyzer` | `guest_core.record_visual_dna()` | `VisualDNASpec` / `RECEIPT_VISUAL_DNA_RECORDED` |
| `GST-004` | Guest Context & Evidence Archive Binding | `COMMANDER` | `GuestCommanderAgent` | `guest-evidence-linker` | `guest_core.link_evidence()` | `GuestIdentityLink` / `RECEIPT_GUEST_LINKED` |

---

### 2.3 Audience Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `AUD-001` | Audience World & Tension Profiling | `HUNTER` | `AudienceTeam::Hunter` | `audience-tension-hunter` | `relational_intelligence.create_audience_profile()` | `AudienceProfile` / `RECEIPT_AUDIENCE_PROFILED` |
| `AUD-002` | Cognitive Island & Resistance Mapping | `ANALYST` | `AudienceTeam::Analyst` | `cognitive-island-mapper` | `relational_intelligence.map_cognitive_islands()` | `CognitiveIslandMap` / `RECEIPT_ISLANDS_MAPPED` |
| `AUD-003` | Temporal Viewer-State Evolution & Resonance | `COMPOSER` | `AudienceTeam::Composer` | `viewer-state-composer` | `relational_intelligence.evolve_viewer_state()` | `ViewerStateSequence` / `RECEIPT_VIEWER_STATE_EVOLVED` |

---

### 2.4 Research & Knowledge Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `RES-001` | Multi-Source Signal Acquisition & Fanout | `HUNTER` | `ResearchTeam::Hunter` | `searxng-signal-hunter` | `world_intelligence.acquire_signals()` | `ResearchSignalManifest` / `RECEIPT_SIGNAL_ACQUIRED` |
| `RES-002` | Source Verification & Syndication Anti-Inflation | `ANALYST` | `ResearchTeam::Analyst` | `source-anti-inflation-analyst` | `world_intelligence.verify_sources()` | `VerifiedSourceBatch` / `RECEIPT_SOURCES_VERIFIED` |
| `RES-003` | Epistemic Friction & Contradiction Extraction | `ANALYST` | `ResearchTeam::Analyst` | `epistemic-friction-analyst` | `world_intelligence.extract_frictions()` | `FrictionRegister` / `RECEIPT_FRICTIONS_EXTRACTED` |
| `RES-004` | Knowledge Canonicalization & Entity Binding | `COMPOSER` | `ResearchTeam::Composer` | `knowledge-graph-builder` | `world_intelligence.canonicalize_entities()` | `CuratedKnowledgePack` / `RECEIPT_KNOWLEDGE_PACKED` |

---

### 2.5 Activation & Collision Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `COL-001` | Tension Collision & Analogy Discovery | `HUNTER` | `CollisionTeam::Hunter` | `collision-hypothesis-hunter` | `collision_intelligence.discover_collisions()` | `CollisionCandidateManifest` / `RECEIPT_COLLISIONS_HUNTED` |
| `COL-002` | Falsification & Vector-Truth Fallacy Testing | `ANALYST` | `CollisionTeam::Analyst` | `collision-falsification-analyst` | `collision_intelligence.falsify_hypotheses()` | `CollisionEvaluationReport` / `RECEIPT_HYPOTHESIS_FALSIFIED` |
| `COL-003` | Hypothesis Portfolio Synthesis & Structuring | `COMPOSER` | `CollisionTeam::Composer` | `hypothesis-portfolio-composer` | `collision_intelligence.compose_portfolio()` | `CollisionHypothesisPortfolio` / `RECEIPT_PORTFOLIO_COMPOSED` |
| `COL-004` | Collision Hypothesis Authorization Gate | `COMMANDER` | `CollisionCommanderAgent` | `collision-gatekeeper` | `collision_intelligence.authorize_hypothesis()` | `AuthorizedHypothesisBatch` / `RECEIPT_HYPOTHESIS_AUTHORIZED` |

---

### 2.6 Interview Intelligence Family (Mandates M01–M11)

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `INT-001` | Dynamic Question Frontier Exploration | `HUNTER` | `InterviewTeam::FrontierHunter` | `adaptive-question-frontier` | `interview_intelligence.frontier_service.explore_frontier()` | `QuestionFrontierManifest` / `RECEIPT_FRONTIER_EXPLORED` |
| `INT-002` | Contextual Transcript Resolution & Token Lock | `ANALYST` | `InterviewTeam::ResolutionAnalyst` | `question-resolution-engine` | `interview_intelligence.resolution_engine.resolve_turn()` | `ResolvedTurnRecord` / `RECEIPT_TURN_RESOLVED` |
| `INT-003` | Semantic Acquisition & Lived Experience Mapping | `ANALYST` | `InterviewTeam::AcquisitionAnalyst` | `semantic-acquisition-observer` | `interview_intelligence.semantic_acquisition.observe()` | `SemanticObservationBatch` / `RECEIPT_SEMANTIC_ACQUIRED` |
| `INT-004` | Composition Compatibility & Harness Pre-Check | `ANALYST` | `InterviewTeam::CompatibilityAnalyst` | `composition-compatibility-checker` | `interview_intelligence.composition_compatibility.check()` | `CompatibilityReport` / `RECEIPT_COMPATIBILITY_CHECKED` |
| `INT-005` | Interview Brief & Research Package Assembly | `COMPOSER` | `InterviewTeam::BriefComposer` | `interview-brief-composer` | `interview_composer.brief_compiler.compile_brief()` | `InterviewBrief` / `RECEIPT_BRIEF_COMPILED` |
| `INT-006` | Live Operator Question Studio Control | `COMMANDER` | `InterviewCommanderAgent` | `operator-studio-controller` | `interview_intelligence.candidate_menu.rank_menu()` | `CandidateMenuManifest` / `RECEIPT_MENU_RENDERED` |

---

### 2.7 Evidence Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `EVD-001` | Lossless Thought-Bounded Segmentation | `HUNTER` | `EvidenceTeam::SegmenterHunter` | `semantic-transcript-segmenter` | `segmentation_intelligence.segment_transcript()` | `TranscriptSegmentationResult` / `RECEIPT_TRANSCRIPT_SEGMENTED` |
| `EVD-002` | Multi-Dimensional Semantic Attribution | `ANALYST` | `EvidenceTeam::AttributionAnalyst` | `semantic-attribution-analyzer` | `attribution_intelligence.attribute_segment()` | `AttributedEvidenceBatch` / `RECEIPT_EVIDENCE_ATTRIBUTED` |
| `EVD-003` | Cryptographic Provenance & Monotonicity Gate | `COMMANDER` | `EvidenceCommanderAgent` | `lossless-provenance-verifier` | `segmentation_intelligence.verify_lossless()` | `EvidenceVerificationReceipt` / `RECEIPT_EVIDENCE_AUTHENTICATED` |

---

### 2.8 Editorial Intelligence Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `EDT-001` | Content Candidate Formation & Hook Discovery | `HUNTER` | `EditorialTeam::CandidateHunter` | `content-candidate-former` | `candidate_intelligence.form_candidates()` | `ContentCandidateManifest` / `RECEIPT_CANDIDATES_FORMED` |
| `EDT-002` | Multi-Axis Adversarial Candidate Scoring | `ANALYST` | `EditorialTeam::ScoringAnalyst` | `multi-axis-scoring-rubric` | `scoring_intelligence.score_candidates()` | `ScoredCandidateBatch` / `RECEIPT_CANDIDATES_SCORED` |
| `EDT-003` | Editorial Storyboard & Narrative Sequencing | `COMPOSER` | `EditorialTeam::StoryboardComposer` | `editorial-storyboard-composer` | `production_program.compile_storyboard()` | `EditorialStoryboard` / `RECEIPT_STORYBOARD_COMPILED` |
| `EDT-004` | Semantic Program & Activation Payload Lock | `COMPOSER` | `EditorialTeam::SemanticComposer` | `semantic-program-composer` | `production_program.compile_program()` | `SemanticProgram` / `RECEIPT_PROGRAM_COMPILED` |
| `EDT-005` | Operator Editorial Selection & Gatekeeping | `COMMANDER` | `EditorialCommanderAgent` | `operator-editorial-gate` | `operator_intelligence.record_decision()` | `OperatorEditorialDecision` / `RECEIPT_EDITORIAL_AUTHORIZED` |

---

### 2.9 Production & Visual Syntax Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `PRD-001` | Visual Syntax & Spatial Layout Observation | `HUNTER` | `ProductionTeam::VisualHunter` | `stage1-visual-syntax-skill` | `builder.skills.jit_capsule.observe_syntax()` | `Stage1SyntaxReport` / `RECEIPT_SYNTAX_OBSERVED` |
| `PRD-002` | Composition IR & Layout Specification Compile | `COMPOSER` | `ProductionTeam::CompositionComposer` | `visual_syntax_composition_compiler` | `builder.skills.jit_capsule.compile_spec()` | `CompositionIR` / `RECEIPT_COMPOSITION_SPEC_COMPILED` |
| `PRD-003` | Visual Asset Demand Protocol Compilation | `COMPOSER` | `ProductionTeam::DemandComposer` | `delegation-demand-compiler` | `cmf_pipeline.delegation.compile_demand()` | `VisualAssetDemandContract` / `RECEIPT_DEMAND_COMPILED` |
| `PRD-004` | Visual Asset Result & Safe Zone Validation | `ANALYST` | `ProductionTeam::ResultAnalyst` | `delegation-result-validator` | `cmf_pipeline.delegation.validate_result()` | `ValidatedAssetResult` / `RECEIPT_ASSET_VALIDATED` |
| `PRD-005` | Video Edit Program & Timeline Projection | `COMPOSER` | `ProductionTeam::TimelineComposer` | `timeline-projection-engine` | `services/studio/dist/rpc.js::projectVideoEditProgram` | `VideoEditProgram` / `RECEIPT_TIMELINE_PROJECTED` |
| `PRD-006` | Production Gate Authorization & Seal | `COMMANDER` | `ProductionCommanderAgent` | `production-seal-evaluator` | `pipeline.deterministic_scheduler.authorize_run()` | `ProductionReleaseSeal` / `RECEIPT_PRODUCTION_AUTHORIZED` |

---

### 2.10 Release & Ship Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `REL-001` | Audit Export Manifest & Lineage Build | `ANALYST` | `ReleaseTeam::AuditAnalyst` | `audit-export-builder` | `services/studio/dist/rpc.js::buildAuditExportManifest` | `AuditExportManifest` / `RECEIPT_AUDIT_BUILT` |
| `REL-002` | Release & Ship Evaluation Gate | `COMMANDER` | `ReleaseCommanderAgent` | `ship-gate-evaluator` | `services/studio/dist/rpc.js::evaluateShipRequest` | `ShipVerdict` / `RECEIPT_SHIP_EVALUATED` |
| `REL-003` | Destination Publishing & Channel Handshake | `NOT_APPLICABLE_BY_RULE` | `PublishingTransportTeam` | `channel-publish-adapter` | `pipeline.publish_artifact()` | `PublishingReceipt` / `RECEIPT_PUBLISHED` |

---

### 2.11 Learning & Evolution Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `LRN-001` | Real-World Outcome Ingestion & Metric Capture | `HUNTER` | `LearningTeam::MetricHunter` | `outcome-metric-ingester` | `outcome_intelligence.record_metrics()` | `OutcomeObservationBatch` / `RECEIPT_METRICS_INGESTED` |
| `LRN-002` | Prediction Gap & Resonance Failure Analysis | `ANALYST` | `LearningTeam::ResonanceAnalyst` | `prediction-gap-analyst` | `outcome_intelligence.analyze_prediction_gaps()` | `ResonanceAnalysisReport` / `RECEIPT_GAPS_ANALYZED` |
| `LRN-003` | Harness & Rubric Parameter Adaptation Proposal | `COMPOSER` | `LearningTeam::EvolutionComposer` | `rubric-adaptation-composer` | `outcome_intelligence.propose_tuning()` | `RubricTuningProposal` / `RECEIPT_TUNING_PROPOSED` |
| `LRN-004` | Learning Promotion & Model Claim Verification | `COMMANDER` | `LearningCommanderAgent` | `programmed-model-verifier` | `programmed_model_engine.register_claim()` | `ProgrammedModelClaim` / `RECEIPT_CLAIM_VERIFIED` |

---

### 2.12 Operator Control Family

| Capability ID | Description | Authority Lane | Agent / Team | Canonical Skill Package | Deterministic Operation / Hook | Artifact & Receipt |
|---|---|---|---|---|---|---|
| `OPR-001` | Control Tower System State Projection | `ANALYST` | `OperatorControlTeam::Analyst` | `control-tower-projector` | `services/studio/dist/rpc.js::buildControlTowerProjection` | `ControlTowerProjection` / `RECEIPT_STATE_PROJECTED` |
| `OPR-002` | Natural Language Revision Compilation | `COMPOSER` | `OperatorControlTeam::Composer` | `revision-compiler` | `services/studio/dist/rpc.js::compileNaturalLanguageRevision` | `RevisionInstructionSet` / `RECEIPT_REVISION_COMPILED` |
| `OPR-003` | Human Resolution Episode & Dispute Logging | `COMMANDER` | `OperatorCommanderAgent` | `human-resolution-logger` | `services/studio/dist/rpc.js::createHumanResolutionEpisode` | `HumanResolutionLedger` / `RECEIPT_DISPUTE_LOGGED` |

---

## 3. Unexecuted Intelligence Register

The following reasoning capabilities are defined in specifications or present as synthetic/reference algorithms, but lack live runtime execution wiring or production model bindings in the current repository:

| Unexecuted Capability ID | Capability Name | Stated Scope / Spec | Current Implementation Reality | Required Runtime Convergence Action |
|---|---|---|---|---|
| `UNEX-01` | **Dense / Embedding Vector Retrieval** | PRD F04 (Dense Retrieval) | Only lexical/regex retrieval exists in `pipeline/retrieval_engine.py`. Zero embedding models or vector DBs wired in runtime. | Bind governed embedding provider to PostgreSQL `pgvector` or runtime vector store under tenant isolation. |
| `UNEX-02` | **Automated Audio-to-Transcript (ASR)** | Interview Expression Protocol | Only pre-aligned JSON and SRT ingestion exist (`test_pre_aligned_json_ingestion`). Whisper/ASR is not wired. | Implement audio chunking, ASR provider adapter, and monotonic word-alignment validator. |
| `UNEX-03` | **Real SAM3 / ComfyUI / GNM Image Generation** | VAE PRD F15 / TS-VAE-BOUND-001 | VAE emits `GRAPH_COMPILED_NOT_EXECUTED`. `ComfyUIHttpAdapter` is unwired. Reference providers emit synthetic masks. | Mount `/api/vae`, wire Pipeline `VisualDelegationService`, and connect authorized ComfyUI runtime endpoint. |
| `UNEX-04` | **Dynamic Prompt Steering & Negotiation** | `ProgrammedModelRegistry` TS-RET-001 | Schema and registration engine exist (`programmed_model_program.schema.json`), but live LLM steering loop is mock/deterministic. | Connect live DSPy/model inference runner obeying `allowed_tool_ids` and `forbidden_action_ids`. |

---

## 4. Invariant Verification & Compliance Proof

1. **No Skill Nesting**: Every Canonical Skill package listed in Section 2 is flat. No Skill specifies a child Skill in its manifest or imports another Skill package.
2. **Authority Lane Purity**: Every capability is assigned to exactly one of `HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`, or `NOT_APPLICABLE_BY_RULE`. No mixed-lane agent loops exist.
3. **Deterministic State Invariant**: All mutations terminate on typed Python/SQL operations with explicit preconditions, postconditions, and cryptographic receipts.
