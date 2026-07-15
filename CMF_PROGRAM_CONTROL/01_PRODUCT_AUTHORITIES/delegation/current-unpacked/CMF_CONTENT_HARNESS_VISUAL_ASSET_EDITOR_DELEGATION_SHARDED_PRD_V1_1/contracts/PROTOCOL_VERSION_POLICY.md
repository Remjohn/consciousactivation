---
title: Protocol Versioning and Deprecation
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Protocol Versioning and Deprecation

## Version classes

- **Patch** — non-semantic corrections; no authority or lifecycle change.
- **Minor** — backward-compatible optional fields, messages, codes or features.
- **Major** — changes to mandatory authority, lifecycle, acceptance, invalidation, hard-gate or identifier semantics.

## Contract status

```text
active
→ discouraged
→ deprecated
→ read_only_support
→ retired
```

An accepted delegation pins its negotiated profile and remains governed by it for the complete lifecycle.

## Migration

Migrations produce new immutable artifacts, preserve originals, declare every transformation and prove semantic and authority equivalence. Lossy adapters are prohibited for mandatory fields.
