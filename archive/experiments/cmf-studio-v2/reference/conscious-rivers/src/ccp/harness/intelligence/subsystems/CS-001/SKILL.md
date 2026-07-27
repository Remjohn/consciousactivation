# CS-001 Skill

## Purpose

Apply the First Frame Imprint subsystem during HOOK selection and regeneration review so the first 400 ms contain a single dominant focal anchor instead of scroll-inducing clutter.

## Use This Skill When

- selecting or regenerating a HOOK scene
- reviewing the first frame of any mobile-first export
- validating whether opening captions, logos, or overlays are competing with the focal element

## Required Inputs

- first-frame still or manifest frame data
- focal-element count
- saliency or contrast estimate
- vertical placement of the dominant element
- initial CLS estimate

## Decision Procedure

1. Confirm the frame contains exactly one dominant focal element.
2. Confirm the focal element is placed in the upper-central working zone.
3. Confirm initial CLS is less than or equal to 2.
4. Confirm no competing text stack or decorative clutter is present.
5. Return `PASS`, `REVISE`, or `BLOCK` with the violated threshold names.

## Runtime Guidance

- Prefer a face or one striking object over branded atmosphere.
- Treat logos, multiple text blocks, and split focal points as survival risks.
- If CS-001 fails, fix the first frame before tuning later beats.

## Escalate Or Block When

- focal count is not exactly one
- the dominant element lands outside the safe zone
- opening CLS exceeds the threshold
- the frame asks the viewer to search before they can lock