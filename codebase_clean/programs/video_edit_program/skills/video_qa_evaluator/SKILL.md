---
name: video_qa_evaluator
description: Evaluates independent Semantic QA and Render QA for source-led video edits.
version: 1.0.0
lane: ANALYST
---

# Video QA Evaluator Skill

## Role
Passive, flat skill executed within the `ANALYST` authority lane.
Performs independent dual-axis evaluation: Semantic QA (source fidelity, quote checksums, wrong-reading locks) vs Render QA (ffprobe streams, non-zero file byte count, cut frame evidence extraction).

## Invariants
- Semantic QA and Render QA must be evaluated as distinct axes.
- Emits structured evaluation records with extracted cut evidence frames.
- No sub-skill execution.
