# Workspace + Guest Operating Context Program Package

Governed by Phase 3 Mandate M25 and TS-CAE-TEN-001.
Authority Lanes: COMMANDER, HUNTER, ANALYST.
Operating Model: One-Workspace / One-Active-Guest.
Subordinate Dimensions: Persona/Brand Context derived with cryptographic SHA-256 evidence lineage.
Typed Operations:
- cae.workspace.configure@1.0.0
- cae.guest.register@1.0.0
- cae.guest.bind_evidence@1.0.0
- cae.guest.activate_context@1.0.0
- cae.guest.repair_context@1.0.0
Mutation Boundary: CAE PostgreSQL state only via typed operations.
Filesystem contents are composition metadata, not canonical state.
