# M0085 upstream/reference record

Evidence class: REGISTRY_SOURCE / DOCUMENT

Repository consulted: https://github.com/Remjohn/consciousactivation
Current remote reference observed during audit: `1238dda04cc89e16ed7ac96ac79417c7c321f8a8`

Exact upstream source paths inspected for adopted behavior/reference:
- `services/studio/src/domain.ts`
- `services/studio/src/revision.ts`
- `services/studio/src/timeline.ts`

Adoption decision: no third-party/external repository code was copied into CAE. The Studio package in this mandate is a narrow CAE-native reconstruction/repair of the bridge contract and currently referenced frontend/backend symbol surface, constrained by the repository's own constitutional and product documents.

License record: no root `LICENSE` file was found at the consulted current upstream path during the audit; therefore no external license was asserted and no external source code was adopted.

Compatibility note: the Python `StudioBridge` in the archive consumes the JSON response field `result`; M0085 preserves that live bridge contract rather than changing it to the prose-only `data` spelling appearing in one secondary spec description.
