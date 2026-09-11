# No-Primitive-Before-Audits Law

The Question Intelligence program has one hard dependency that must not be violated:

> **Primitive codification is downstream of source auditing.**

The following are prohibited before all assigned book audits are complete and accepted:

- writing new `PRM-QST-*` YAML primitives;
- editing existing Question Primitive definitions to incorporate book claims;
- promoting a candidate mechanism into the canonical registry;
- modifying the runtime Interview Harness to depend on an unaudited Question Primitive;
- treating book-derived question techniques as established architecture merely because they sound plausible.

Earlier `PRM-QST-*` files, if present, must be marked `QUARANTINED_HYPOTHESIS` and excluded from the canonical registry and runtime resolver.

The taxonomy is intentionally open. Existing dimensions are not sacred. A book may reveal a new dimension that the current taxonomy cannot represent. In that event, the audit records:

1. the observed mechanism;
2. the source evidence supporting it;
3. the collision with the current taxonomy;
4. the proposed new dimension or distinction;
5. why the distinction is operationally useful in CAE;
6. what later cross-book evidence would be needed to promote it.
