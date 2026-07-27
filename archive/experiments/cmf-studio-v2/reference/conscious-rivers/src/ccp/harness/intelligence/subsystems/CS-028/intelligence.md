# CS-028 - Element Counter

CS-028 exists because mobile visual working memory is narrow. In CMF, piling face, text, icons, product imagery, and decorative markers into one frame can quickly push the viewer from fluency into split attention.

The subsystem reads frame-level element count, semantic weights, and redundancy. It succeeds when the composition stays within a mobile-viable capacity. It fails when too many meaningful items compete at once.

CS-028 is a simple but necessary overload control, especially in automated pipelines that keep adding helpful overlays until the frame collapses.

## Current CMF Thresholds

- maximum simultaneous meaningful elements: 3
- supportive contextual element allowed only if it does not become a fourth competing task

## Good Example

The frame contains face, keyword text, and one support icon, all clearly prioritized.

## Failure Example

Face, subtitle, icon, product, emoji, and lower-third all demand attention simultaneously.