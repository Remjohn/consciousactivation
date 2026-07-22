# CS-027 - Temporal Binding

CS-027 exists to fuse spoken meaning and visual support into a single encoded event. Temporal contiguity is powerful because it lowers integration cost and strengthens memory. When the graphic arrives inside the binding window, the viewer experiences one coherent event. When it arrives late, the brain must reopen the phrase and connect it manually.

The subsystem reads phonetic onset, waveform cues, and the first frame of the supporting visual. It succeeds when the visual lands inside the CMF binding window, ideally very near the keyword onset. It fails when the overlay is late enough that the word and image become separate memory tasks.

This subsystem is stricter than general sync checking. Its purpose is not just polish. It is to improve recall and comprehension in coaching and proof-driven scenes.

## Current CMF Thresholds

- preferred binding window: -20 ms to +160 ms relative to phonetic onset
- visual-leading is slightly safer than audio-leading
- late-arrival risk becomes severe beyond roughly 300 ms

## Good Example

A keyword framework card appears exactly as the coach starts saying the core term.

## Failure Example

The overlay lands after the coach has already finished the keyword, forcing the viewer to reconnect meaning manually.