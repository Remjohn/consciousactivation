# Registries and Format Adapters

## 1. Supporting registries

The existing five CCP registries remain authoritative for meaning, packaging, memes, reactions, and rendering. This bundle adds supporting registries:

### Expression Ingredient Registry
Defines semantic ingredient roles, source classes, compatibility, and default quality dimensions.

### Sequence Pattern Registry
Defines viewer-state and information-release grammars.

### Acquisition Instrument Registry
Defines question and follow-up instruments used to procure ingredient roles.

### Format Sequence Adapter Registry
Maps abstract sequence beats to format-specific spatial and temporal behavior.

### Sequence Eval Gate Registry
Defines hard and soft gates for procurement, sequence compilation, package ordering, and doctrine compliance.

---

## 2. Registry contract

Every registry item must include:

```text
id
version
status
description
required inputs
compatible archetypes
compatible formats
rules
anti-patterns
evaluation hooks
examples
```

Registry IDs are immutable. New behavior creates a new version.

---

## 3. Format adapter principle

The sequence pattern is semantic. The format adapter makes it temporal or spatial.

Example:

```text
Pattern: MYTH_MECHANISM_REPLACEMENT

Short video:
myth line → anomaly clip → mechanism diagram → replacement rule

Carousel:
cover → myth → why it persists → anomaly → mechanism → replacement → action

Single image:
myth headline → contradictory visual → one-line replacement model

Reaction format:
proof object → prediction → guest verdict → mechanism → audience question
```

No format adapter may remove a required payoff without producing a failed closure gate.
