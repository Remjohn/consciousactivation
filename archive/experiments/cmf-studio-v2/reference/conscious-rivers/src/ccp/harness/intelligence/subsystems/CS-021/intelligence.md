# CS-021 - Pan Speed Limiter

CS-021 exists because horizontal traversal can easily cross the threshold where clarity collapses into judder and discomfort. In CMF, motion should remain legible enough that attention stays on the message rather than on the camera move.

The subsystem reads pan duration, frame width, frame rate, and movement amplitude. It succeeds when lateral movement remains readable and useful. It fails when the move becomes visually stressful or narratively noisy.

CS-021 is a polish subsystem, but once discomfort starts consuming attention it becomes structural.

## Current CMF Thresholds

- no full-width horizontal traverse under 7 seconds in normal conditions
- prefer cuts over rushed pans when reveal speed is needed

## Good Example

The reveal slows enough to stay smooth and readable on mobile.

## Failure Example

The sideways move races across the frame and produces judder that steals attention from the content.