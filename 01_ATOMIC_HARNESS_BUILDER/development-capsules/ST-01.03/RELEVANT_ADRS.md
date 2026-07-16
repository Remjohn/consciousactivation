# Governing ADRs

- `ADR-003` Authoritative State and Artifact Storage: command state, immutable index,
  receipt and run attachment commit atomically in the current development/test
  adapter; the Story does not claim production PostgreSQL or object storage.
- `ADR-007` Evidence Identity and Source Profiles: Source Lock hashes and immutable
  descriptors are the only specimen inputs; observation, knowledge status and
  provenance remain explicit. Real Format 02 and conversational addenda stay
  conditional and inactive.
- `ADR-012` Sandbox and Least Privilege: the indexer receives no file-write, network,
  provider, external repository or secret capability and cannot widen authority.

All three ADRs remain accepted and unchanged. This capsule implements their bounded
Builder-owned seam and does not amend architectural authority.
