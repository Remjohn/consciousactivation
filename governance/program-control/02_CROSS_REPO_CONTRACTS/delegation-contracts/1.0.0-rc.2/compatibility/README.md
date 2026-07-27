# CMF Delegation Compatibility

This package records deterministic compatibility rules for the Stage 3
release candidate. Automatic adaptation is allowed only when it is lossless
and supplied with immutable source context. The legacy mixed-owner submission
receipt requires an explicit evidence-backed migration and cannot be adapted
automatically.

Consumers must pin a published, signed release manifest. They must not copy or
fork these schemas into product repositories.

