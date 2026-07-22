---
type: tech_spec_assignment
spec_id: TS-INT-002
title: "Word/Speaker Alignment and Packed Phrase Transcript"
product_owner: "Interview Expression"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "INTERVIEW_EXPRESSION/docs/architecture/TS-INT-002.md"
---

# TS-INT-002 — Word/Speaker Alignment and Packed Phrase Transcript

## Controlling product requirements and Stories

**Functional Requirements:** FR-124, FR-128  
**Primary Stories:** ST-01.03, ST-02.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-EXT-017` | github://browser-use/video-use | REFERENCE | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-EXT-020` | github://UVA-Computer-Vision-Lab/OmniShotCut | REFERENCE | Shot-boundary and transition classification. |
| `SRC-EXT-023` | github://SamurAIGPT/AI-Youtube-Shorts-Generator | REFERENCE | Long-video chunking with overlap, deduplication, caching, structured JSON, and vertical crop patterns. |
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |

The writer must also read the exact current source and tests at the target product paths, the current product status, relevant contracts, and every predecessor file named by the exact source reuse crosswalk.

## Required 10-section Tech Spec structure

1. Files and authorities read.
2. Problem, solution, scope, and non-goals.
3. Architecture traceability, existing backend integration, product ownership, and governing decisions.
4. Staged implementation plan with exact paths and migration dispositions.
5. Schemas, APIs, state transitions, commands, events, and receipts.
6. Backward compatibility, fallback, rollback, invalidation, and historical replay.
7. Implementation tasks and path ownership.
8. Behavior-specific acceptance criteria, each with a failure example and Story/CBAR reference.
9. Dependencies, source authority, licenses, providers, models, workers, and external products.
10. Testing, evaluation, observability, security, performance, recovery, evidence, and release.

## Completion law

The spec is accepted only when all controlling FRs and Stories are covered, no second canonical object or product owner is introduced, exact existing code integration is named, negative and downstream failure cases are testable, and the implementation authority issues a bounded Development Capsule.
