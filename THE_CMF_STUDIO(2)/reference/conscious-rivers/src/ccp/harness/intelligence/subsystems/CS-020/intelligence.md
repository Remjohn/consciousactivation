# CS-020 - Parallax Scaler

CS-020 exists because mobile screens can support embodied depth cues, but desktop-strength parallax values often feel artificial when transferred directly to small displays.

The subsystem reads platform, depth values, motion profile, and scene role. It succeeds when parallax quietly enhances layered realism. It fails when depth becomes conspicuous and breaks trust.

CS-020 is a classic calibration subsystem: it keeps measurable effects inside biologically plausible bounds.

## Current CMF Thresholds

- mobile parallax scale coefficient: 0.6
- desktop maximum baseline: 1.0
- mobile depth should not exceed 0.7 of desktop-intended feel unless stylized

## Good Example

Layered depth adds subtle realism on Shorts export without calling attention to itself.

## Failure Example

The phone render looks like exaggerated video-game depth because desktop settings were copied directly.