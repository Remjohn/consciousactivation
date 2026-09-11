# Video Edit Production Program — Standard Operating Instructions

## Lifecycle Stages
1. **Admission (`COMMANDER`)**: Validate incoming `SemanticProgram` and ensure no synthetic markers exist.
2. **Source Media Registration (`HUNTER`)**: Register source media files via `SourceMediaService`, extract verbatim timings, and verify quote hashes.
3. **EDL Compilation (`COMPOSER`)**: Compile word boundary EDL ensuring boundary classes (`WORD_BOUNDARY`, `SILENCE_BOUNDARY`) and tail protection.
4. **Program Compilation (`COMPOSER`)**: Compile `VideoEditProgram` ensuring `PRIMARY_A_ROLL_SPINE` and wrong-reading locks.
5. **Binding Compilation (`COMPOSER`)**: Compile Remotion and HyperFrames export bindings.
6. **Physical Render Pass (`COMPOSER`)**: Execute `FFmpegSourceLedRenderer` to produce `.mp4` and `.srt` artifacts.
7. **Dual-Axis QA (`ANALYST`)**: Execute `RenderedVideoEvaluator` (ffprobe streams + cut frame extraction) alongside Semantic QA checks.
8. **Release Authorization (`COMMANDER`)**: Sign cryptographic `VideoReleaseReceipt` with operator rationale.
