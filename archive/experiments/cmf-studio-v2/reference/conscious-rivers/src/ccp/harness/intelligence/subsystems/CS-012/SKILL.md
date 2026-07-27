# CS-012 Skill

## Purpose

Apply the CTA Fusion Timer so the behavioral ask remains fused to the ending rather than separated by dead air that the feed will overwrite.

## Use This Skill When

- designing the VISION beat and CTA timing
- reviewing whether an outro or pause weakens post-viewing action
- validating end-state edits during regeneration

## Required Inputs

- end-state timestamp
- CTA timestamp
- gap duration
- audio continuity across the ending

## Decision Procedure

1. Measure the gap between the end-state and the CTA.
2. Confirm they occupy the same action window.
3. Reject decorative outro spacing that separates feeling from action.
4. Return a fusion verdict and timing correction if needed.

## Runtime Guidance

- The CTA is part of the ending, not an attachment after it.
- Do not insert branding tail or empty fade between emotional resolution and action.
- Use this subsystem whenever the final beat is being re-cut.