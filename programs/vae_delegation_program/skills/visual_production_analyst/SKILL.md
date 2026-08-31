---
name: "visual_production_analyst"
version: "1.0.0"
description: "Evaluates VAE generation outputs against render/technical criteria, negative-space locks, and independent semantic narrative requirements."
lanes:
  - "ANALYST"
---

# Visual Production Analyst Skill

## Role & Purpose
Evaluates materialized visual candidates against technical and semantic quality criteria before forwarding results to the Pipeline acknowledgement boundary.

## Evaluation Protocol
1. **Technical Hard Gates**:
   - Verify bounding box geometry, aspect ratio, and resolution compliance.
   - Verify negative-space locks and alpha matte boundary sharpness.
   - Validate that forbidden elements specified in wrong-reading locks are absent.
2. **Dual-Axis Semantic QA**:
   - Independently evaluate narrative fit, somatic impact, and anti-centroid integrity.
   - Fail closed if semantic requirements are violated, even if technical render criteria pass.
3. **Provider-Neutral Result Envelope**:
   - Package findings into canonical `AssetResult` envelope.
   - Explicitly ensure `consumption_authorized` is NOT declared in the VAE result.
