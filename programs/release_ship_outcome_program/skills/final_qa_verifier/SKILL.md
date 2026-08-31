---
name: final_qa_verifier
description: "Passive flat skill for independent Dual-Axis QA verification (Semantic QA + Render QA) and verbatim evidence quote validation."
version: 1.0.0
authority_lane: ANALYST
---

# Final QA Verifier Skill

## Overview
This skill performs independent verification of Dual-Axis QA results before release authorization.

## Execution Rules
1. Inspect Semantic QA: confirm speaker authenticity, narrative role, and evidence support.
2. Inspect Render QA: confirm media validity, duration, audio-video synchronization, and container integrity.
3. Validate verbatim SHA-256 match on evidence quote text.
4. Verify non-empty lexicographical wrong-reading locks.
5. Fail closed if candidate is marked synthetic (`is_synthetic=True`).
