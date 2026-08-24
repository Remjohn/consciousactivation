# Phase 5 Data Model — Conceptual to Physical

## Canonical entities / definitions
- interview_definition
- question_grammar_definition
- evidence_policy
- authentication_policy

## Dynamic state
- interview_state
- question_state
- evidence_candidate_state
- authentication_state

## Immutable evidence
- interview_session
- interview_turn
- guest_response
- source_media
- transcript_segment
- evidence_span

## Derived artifacts
- interview_brief
- interview_plan
- evidence_assessment
- authenticated_evidence
- semantic_evidence_packet
- anti_leading_assessment
- anti_centroid_patrol_result
- interview_receipt

## Recommended PostgreSQL model

```text
interview_sessions
interview_turns
questions
question_grammar_defs
responses
response_spans
evidence_candidates
authentication_decisions
semantic_evidence_packets
anti_leading_assessments
anti_centroid_patrol_results
interview_receipts
```

## JSONB usage
Use JSONB for evolving fields such as:

- extraction_details
- linguistic_markers
- candidate_interpretations
- question_context_snapshot
- patrol_details
- model-specific evaluator payloads

Do not store the canonical identity of an evidence object only in JSONB.

## Vector usage
Use embeddings for retrieval of:

- similar Guest statements,
- prior evidence spans,
- related stories,
- previous questions that successfully elicited comparable evidence,
- semantic neighborhoods for research and interview planning.

Vector similarity is retrieval evidence, not canonical truth.

## Event model

```text
InterviewStarted
QuestionIssued
ResponseCaptured
EvidenceSpanCreated
EvidenceAssessed
AuthenticationDecided
QuestionReplanned
AntiLeadingChecked
AntiCentroidPatrolled
SemanticEvidencePacketEmitted
InterviewCompleted
```

## Immutability law
Raw response and source media are append-only. Corrections occur through new derived records or correction events; historical source is never rewritten.
