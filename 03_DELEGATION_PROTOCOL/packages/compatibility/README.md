# CMF Delegation Compatibility

This package records deterministic compatibility rules for the Stage 3
release candidate. Automatic adaptation is allowed only when it is lossless
and supplied with immutable source context. The legacy mixed-owner submission
receipt requires an explicit evidence-backed migration and cannot be adapted
automatically.

Visual Asset Demand `1.0` likewise requires an immutable, owner-evidenced
migration to `1.1`. Compatibility is behavioral: every mandatory semantic
domain must carry preservation, enforcement, and evaluator evidence where
required. Parse-only support and adapters that drop, weaken, synthesize,
flatten, or reinterpret constitutional meaning are incompatible. Consumers
claiming derivative asset flows must preserve and enforce portable
parent/derivative wrong-reading-lock inheritance. Parse-only support remains
incompatible, and legacy derivative records require explicit classification
and authoritative parent evidence.

Consumers must pin a published, signed release manifest. They must not copy or
fork these schemas into product repositories.
