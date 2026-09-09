# Phase 5 Functional Requirements Inventory

## FR-P05-01 — Interview Brief Compiler
Build validated InterviewBrief objects from Phase 4 ActivationEvent + relevant Guest/Audience state.

## FR-P05-02 — Question Grammar Registry
Define and version question grammars and their admissible purposes.

## FR-P05-03 — Sequential Interview Planner
Select the next question from current evidence state and declared objective.

## FR-P05-04 — Human Response Capture
Persist immutable source responses with channel, speaker, timestamps, and provenance.

## FR-P05-05 — Evidence Span Extraction
Create traceable spans without modifying source text.

## FR-P05-06 — Evidence Assessment
Score explicitness, specificity, consistency, repetition, and contradiction.

## FR-P05-07 — Authentication Decision Engine
Classify evidence for downstream use.

## FR-P05-08 — Dynamic Replanning
Recompute the next-question plan after meaningful new evidence.

## FR-P05-09 — Anti-Leading Patrol
Detect presupposition, contaminated framing, and answer narrowing.

## FR-P05-10 — Anti-Centroid Patrol
Detect genericization and RLHF-like flattening.

## FR-P05-11 — Semantic Evidence Packet Compiler
Emit typed downstream evidence packets with provenance.

## FR-P05-12 — Interview Receipt Service
Record full execution lineage.

## FR-P05-13 — Authorized Retrieval Functions
Expose bounded SQL functions/views for interview planning and evidence retrieval.

## FR-P05-14 — Error Taxonomy and Repair
Implement typed diagnostic correction rather than unguided retries.

## FR-P05-15 — Brownfield Adapter Layer
Map existing transcript/Context Premise/Emotional DNA machinery into Phase 5 canonical objects without duplicating working systems.

## FR-P05-16 — Human Operator Review Surface
Provide transparent table-oriented inspection of questions, responses, evidence status, and patrol findings.
