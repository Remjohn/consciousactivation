# CS-022 - AV Sync Enforcer

CS-022 exists to keep audiovisual events inside a biologically plausible synchrony window. When a hit, caption, gesture accent, or proof card lands out of sync, the brain has to decide whether the sound and picture belong together. That adds friction and weakens recall.

The subsystem reads audio and visual onset times and scores the offset by event class. It succeeds when the event is perceived as a single bound occurrence. It fails when the offset is large enough to split the event into separate processing tasks.

CS-022 is execution-critical because timing falsehood can survive visual polish and still make the piece feel subtly wrong.

## Current CMF Thresholds

- preferred sync window: -20 ms to +100 ms
- speech-linked events should bias closer to the center of the allowed range
- out-of-window events require retime before commit

## Good Example

A proof card lands with the spoken keyword and the sound accent is perceived as one event.

## Failure Example

The visual lands late, so the viewer first hears the word and then separately sees the support graphic.