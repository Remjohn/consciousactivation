# Phase 5 Brownfield Integration Map

## Existing systems to inventory first

- Trigger-First Engine / interview ingress
- Context Premise extraction
- Emotional DNA extraction
- Voice DNA
- Negative Space
- Telegram elicitation path
- AFFiNE knowledge/memory layer
- transcript intelligence
- LIWC-based authenticity scoring if already present
- existing question-generation skills
- existing anti-draft / contrastive systems
- existing receipt or lineage tables

## Reuse rule
If an existing component already performs a function correctly, Phase 5 should wrap/adapt it to the canonical object model rather than build a competing subsystem.

## Expected brownfield deltas

### Missing canonicalization
Existing raw outputs may need to be mapped into InterviewQuestion, GuestResponse, EvidenceSpan, and AuthenticatedEvidence.

### Missing state/history
Current implementations may overwrite or flatten session context. Add append-only events and versioned state snapshots where needed.

### Missing lineage
Every derived insight must link back to the original response and question.

### Missing error taxonomy
Replace generic retry behavior with typed Phase 5 errors.

### Missing operator transparency
Expose tables/views for session inspection, evidence promotion, contradictions, and patrol results.
