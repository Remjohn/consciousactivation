# Phase 5 Receipt Architecture

## InterviewReceipt

```yaml
receipt_id: IR-{SESSION_ID}-{VERSION}
activation_event_id: ...
interview_session_id: ...
question_count: 0
turns: []
question_grammars: []
evidence_spans: []
authentication_decisions: []
antileading_findings: []
anticentroid_findings: []
semantic_evidence_packet_ids: []
state_transitions: []
errors: []
operator_interventions: []
started_at: ...
completed_at: ...
```

## Receipt law
Receipts record what the runtime did. They do not become substitutes for evidence.

## Reproducibility requirement
Given the same canonical definitions, relevant state snapshots, activation event, source responses, and versioned planner/validator policies, an auditor must be able to explain why a particular question was asked and why a particular evidence object was emitted.
