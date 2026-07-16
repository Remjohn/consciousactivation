# Governing technical specifications

## TS-02 - Configured Evidence Workspace

`docs/tech-specs/specs/TS-02-CONFIGURED-EVIDENCE-WORKSPACE.md` owns deterministic
indexing, stable specimen identity, source provenance, query seams, corpus-scale
processing, resume and source-lock invalidation. This Story implements only the
indexing and query increment. It does not implement saturation, authority-conflict
resolution, multimodal inference or a real-profile corpus.

The implementation owner is `evidence_workspace_owner`. The component boundary is
the Builder domain model, indexing command service, repository port and current
in-memory development/test adapter. Data contracts are `Specimen`,
`EvidenceProvenance`, `EvidenceIndex`, `EvidenceIndexReceipt` and typed queries.
Failures are typed and atomic. Tests cover exact coverage, identity collisions,
provenance/knowledge status, authority, scale, determinism, replay and invalidation.

Compatibility is additive: existing Source Locks and the synthetic compilation path
remain valid without an evidence-index reference; evidence-derived paths may require
an active index in later Stories.
