# Phase 5 Canonical Objects

## InterviewBrief
A derived planning object that compiles the Phase 4 activation opportunity, relevant Guest/Audience context, known constraints, evidence gaps, and interview objective into a bounded plan for acquiring truth.

## InterviewPlan
A dynamic execution plan controlling the current question strategy, evidence objectives, stopping conditions, and replanning rules for a session.

## InterviewQuestion
A typed human-directed inquiry with a declared semantic purpose, evidence target, question grammar, and anti-leading constraints.

## QuestionSequence
An ordered but mutable relation structure describing the intended progression from broad activation to specificity and meaning extraction.

## InterviewSession
A bounded interaction event containing ordered InterviewTurns and associated session state.

## InterviewTurn
A timestamped question/response interaction within an InterviewSession.

## GuestResponse
The Guest's source utterance or media contribution as captured, preserving the original representation before interpretation.

## EvidenceSpan
A traceable segment of a GuestResponse selected because it carries potentially useful factual, experiential, semantic, or linguistic information.

## AuthenticatedEvidence
A promoted evidence object whose provenance, context, interpretation status, and authentication decision are explicit.

## EvidenceAssessment
A structured assessment of evidence quality including explicitness, specificity, consistency, repetition, context dependency, contradiction, and confidence.

## SemanticEvidencePacket
A machine-readable bundle of authenticated evidence and carefully bounded derived interpretations made available to downstream semantic processing.

## AuthenticationDecision
A typed verdict describing whether a candidate claim is authenticated, provisionally supported, ambiguous, contradicted, or rejected as unsupported.

## AntiLeadingAssessment
A structured assessment of whether a question contaminated the response by presupposing an answer, narrowing the permitted interpretation, or embedding unsupported framing.

## AntiCentroidPatrolResult
A structured assessment of whether evidence or interpretation was flattened toward generic language, over-sanitized, or stripped of meaningful asymmetry.

## InterviewReceipt
The durable execution trace connecting activation event, question, response, evidence, authentication, patrols, and emitted packets.
