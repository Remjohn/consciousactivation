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
- The envelope stays at protocol `1.0`; Visual Asset Demand advances to message
  `1.1` under replacement package candidate `1.1.0-rc.2`; RC1 is retained as
  consumer-rejected evidence.
- `source_provenance.source_kind` is the sole governed source discriminator.
  `interview_expression` requires non-empty Reaction Receipt and Expression
  Moment reference collections.
- Constitutional references use the exact resource identity tuple: resource
  ID, version, payload hash, and canonical reference.

## Validation

Run:

```bash
python scripts/validate_package.py
```

The validator checks YAML parsing, JSON Schema validity, example conformance, IDs, traceability, links, manifest hashes and ZIP integrity.

## Important boundary

These schemas do not grant creative or production authority. Field ownership is governed by `governance/AUTHORITY_MATRIX.yaml`.
