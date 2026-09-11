---
title: Delegation Contract Family
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---

# Delegation Contract Family

This directory contains **PRD-level schemas and representative fixtures** for the canonical Content Harness ↔ Visual Asset Editor boundary.

## Authority

- Shared contract ownership is established by this Delegation PRD.
- Exact implementation schemas are finalized during Architecture and contract-family validation.
- Public messages use the common Delegation Envelope and a single-purpose immutable payload.
- Large media and canonical payloads are referenced by URI and hash.
- Every message type is registered in `governance/MESSAGE_TYPE_REGISTRY.yaml`.

## Validation

Run:

```bash
python scripts/validate_package.py
```

The validator checks YAML parsing, JSON Schema validity, example conformance, IDs, traceability, links, manifest hashes and ZIP integrity.

## Important boundary

These schemas do not grant creative or production authority. Field ownership is governed by `governance/AUTHORITY_MATRIX.yaml`.
