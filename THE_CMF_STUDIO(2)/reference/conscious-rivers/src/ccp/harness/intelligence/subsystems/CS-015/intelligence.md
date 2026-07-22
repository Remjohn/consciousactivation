# CS-015 - Shot Duration Enforcer

CS-015 exists because narrative inference requires a perceptual floor. In CMF, shots that are meant to carry emotional or semantic meaning must stay on screen long enough to be processed, especially when prior context has not already prepared the interpretation.

The subsystem reads shot duration, prior context stability, shot role, and semantic load. It succeeds when the duration matches the interpretive burden. It fails when a meaningful shot is present only long enough to be noticed but not understood.

CS-015 helps stop the common error of using micro-cuts as a default style instead of as a deliberate tool.

## Current CMF Thresholds

- minimum inference duration after stable context: 750 ms
- contextless minimum duration: 2000 ms
- micro-cuts allowed mainly in simple HOOK rhythm

## Good Example

The reaction insert is extended enough that the emotional shift becomes inferable.

## Failure Example

An explanatory or emotional shot flashes so briefly that the audience registers the image but not the meaning.