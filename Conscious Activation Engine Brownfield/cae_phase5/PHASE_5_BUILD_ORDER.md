# Phase 5 Build Order

## Stage 1 — Brownfield audit
Inventory the existing interview/Telegram/AFFiNE ingress, interview brief generation, Context Premise extraction, Emotional DNA extraction, transcript processing, authenticity scoring, question grammars, and any current response/evidence schemas.

## Stage 2 — Human-first evidence ontology
Define the boundaries between Interview, Question, Prompt, Response, Transcript, EvidenceSpan, AuthenticatedEvidence, Interpretation, Hypothesis, and SemanticEvidencePacket.

## Stage 3 — Interview constitutional model
Define the legal status of the interview as an evidence-acquisition procedure. Establish which actions are allowed before, during, and after a Guest response.

## Stage 4 — Question grammar system
Formalize object-specific question types: broad provocation, reflective follow-up, specificity probe, mechanism probe, contradiction probe, example probe, counterexample probe, consequence probe, meaning probe, and closure/transition question. Each grammar must preserve Guest agency.

## Stage 5 — Interview brief compiler
Compile Phase 4 activation information plus relevant Guest/Audience context into a small, auditable InterviewBrief without inserting unsupported conclusions.

## Stage 6 — Sequential interview planner
Build the stepwise planner that selects the next question from the current evidence state, rather than generating the entire conversation as a fixed script.

## Stage 7 — Response capture and immutable evidence
Capture verbatim response data, timestamps, speaker attribution, confidence, source channel, and provenance. Preserve original media/transcript where available.

## Stage 8 — Authentication pipeline
Separate raw response capture from evidence promotion. Determine whether a statement is explicit, inferred, ambiguous, contradicted, context-bound, repeated, or unresolved.

## Stage 9 — Evidence distillation
Extract spans, claims, examples, beliefs, experiences, mechanisms, tensions, and emotional/semantic markers without erasing the original wording.

## Stage 10 — Anti-leading and anti-centroid review
Detect leading questions, presuppositions, confirmation-seeking, premature paraphrase, sanitization, over-smoothing, and genericization of Guest language.

## Stage 11 — Dynamic replanning
Allow the next-question planner to react to surprises, contradictions, new evidence, silence, refusal, or newly surfaced high-value material.

## Stage 12 — Receipt and lineage wiring
Record activation-event lineage → question → response → evidence spans → authentication decision → derived packet.

## Stage 13 — Technical convergence
Produce PostgreSQL/JSONB models, Pydantic models, authorized SQL functions/views, planner programs, event schemas, validators, and error taxonomy.

## Exit gate

A downstream agent must be able to distinguish, without reading hidden conversational memory:

- what Phase 4 believed,
- what the Guest actually said,
- what evidence was extracted,
- what was inferred from that evidence,
- what remains unresolved,
- and why the next phase is authorized to use each object.
