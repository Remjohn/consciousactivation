# CS-005 - Safe Zone Enforcer

CS-005 exists because mobile viewers do not scan the entire frame uniformly. The upper-central zone receives disproportionate attention, while the bottom area is often degraded by platform UI, thumbs, and low perceptual priority. In CMF, that makes placement an execution rule rather than a final-export nicety.

The subsystem reads bounding boxes for faces, captions, and overlays, plus the platform exclusion zones. It succeeds when critical information lives in the viable viewing region. It fails when important semantic content is pushed into UI-heavy or low-attention areas.

CS-005 is an execution-critical quality subsystem because even correct storytelling can become unreadable if the interface geometry is ignored.

## Current CMF Thresholds

- preferred face band: 15% to 25% from top
- preferred caption band: 30% to 60% from top
- bottom 20%: blocked for critical semantic content
- far-right 15%: avoid for essential content

## Good Example

The face sits high in frame, captions clear the platform chrome, and the CTA remains visible in the active zone.

## Failure Example

The key caption and CTA sit behind UI overlays near the bottom of the frame.