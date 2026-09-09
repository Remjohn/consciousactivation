# Phase 5 Reasoning Program — SQL-of-Thought-Aligned Interview Compiler

## Mission
Given a Phase 4 ActivationEvent, determine the next human question that maximizes evidence acquisition while preserving Guest agency and anti-centroid integrity.

## Program

```text
Human / Activation Intent
  ↓
Schema Linking
  ↓
Relevant Guest + Audience + Context + Activation entities
  ↓
Relevant relations and current states
  ↓
Evidence gaps / contradictions / unresolved pressure
  ↓
Question-type subproblem decomposition
  ↓
Question plan
  ↓
InterviewQuestion
  ↓
Human response
  ↓
Evidence extraction
  ↓
Authentication evaluation
  ↓
Typed result
  ↓
Replan or advance
```

## Authorized retrieval functions
- `get_activation_event_context(activation_event_id)`
- `get_guest_current_state(guest_id)`
- `get_guest_relevant_experience(guest_id, tension_ids)`
- `get_audience_relevant_state(audience_id, tension_ids)`
- `get_unresolved_evidence_gaps(interview_session_id)`
- `get_recent_response_contradictions(interview_session_id)`
- `find_question_grammar_candidates(evidence_gap_type)`
- `get_prior_successful_question_patterns(context_signature)`

## Planning law
The planner should prefer the smallest next question that resolves the highest-value uncertainty. A question must have a declared evidence target before issuance.

## Replanning triggers
- unexpected new tension
- contradiction
- emotionally significant specificity
- Guest rejection of premise
- evidence saturation
- answer repetition
- unresolved ambiguity

## Repair taxonomy
- `QUESTION_PLAN_ERROR`
- `SCHEMA_LINK_ERROR`
- `EVIDENCE_TARGET_ERROR`
- `LEADING_QUESTION_ERROR`
- `PRESUPPOSITION_ERROR`
- `DUPLICATE_QUESTION_ERROR`
- `INSUFFICIENT_SPECIFICITY_ERROR`
- `UNRESOLVED_AMBIGUITY_ERROR`
- `AUTHENTICATION_GAP_ERROR`
- `CENTROID_FLATTENING_ERROR`

The reasoning loop must never repair a weak evidence state by inventing evidence.
