# Autonomous VLM Quality Loop

## Core loop

```text
candidate
→ deterministic technical validation
→ asset-level VLM evaluation
→ composition render
→ composition-level VLM evaluation
→ syntax/recurrence/continuity evaluation
→ temporal evaluation when applicable
→ accept or typed repair
```

## Independence

The production model may provide structured metadata, but cannot be the only acceptance authority. The evaluator receives the authoritative demand and only the context needed for its evaluation role.

## Failure contract

Every quality failure must state:

- failure code and severity;
- evidence BBOX or time range;
- responsible layer;
- preserved properties;
- permitted and prohibited changes;
- invalidated nodes;
- expected correction evidence;
- calibrated confidence.

## Three rounds

1. local/deterministic or parameter correction;
2. strengthened/substituted conditioning;
3. approved fallback workflow or resolution route.

After round three, the system emits a Human Exception or Capability Gap. Infrastructure retries are tracked separately.

## Evaluator certification

Evaluator profiles require protected labeled data, including:

- accepted and rejected assets;
- borderline cases;
- wrong action and wrong-reading cases;
- composition failures;
- identity and continuity drift;
- beneficial and fatiguing recurrence;
- temporal artifacts;
- correct and incorrect repair-owner labels.

A newer VLM does not replace a certified evaluator without shadow and regression evidence.
