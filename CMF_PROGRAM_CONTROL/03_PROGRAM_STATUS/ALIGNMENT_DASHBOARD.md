# Conscious Activations Alignment Dashboard

As of: 2026-07-15  
Current contract: `delegation-contracts@1.1.0-rc.4`  
Final convergence verdict: **CONCERNS**  
Rubric totals: **63 PASS / 1 CONCERN / 0 FAIL**  
Reconciliation mode: **bounded CRC evidence ingestion; full audit not rerun**

## Audit dashboard

| Audit domain | Status | Evidence summary |
|---|---|---|
| Preconditions | PASS | RC4 release, both consumer integrations and namespace reconciliation exist and validate. |
| Release identity and hashes | PASS | Two 164-file trees and all 163 receipt entries match. |
| Live validation | PASS | Release validator; 83/83 validator; 35/35 protocol; 16/16 Builder; 14/14 VAE. |
| Historical release classification | PASS | RC1 consumer-rejected; RC2/RC3 convergence-rejected; RC4 current. |
| Constitutional precedence | PASS | Constitution V1.1 is byte-identical and cannot be locally overridden. |
| Dedicated local precedence evidence | PASS | VAE local contract `sha256:35b5…dd0e` validates Constitution `sha256:21c2…d70b`; non-forking and non-overriding; CRC-401 resolved. |
| Product authority boundaries | PASS | No creative, semantic or production-authority mutation. |
| Source kind and provenance | PASS | Governed enum, no guessing and interview provenance enforced. |
| Semantic lineage | PASS | Fourteen lineage elements preserved without flattening. |
| Derivative locks | PASS | Portable inheritance enforced across Builder, RC4 and VAE. |
| VAE `EVALUATE` | PASS | Capability declared and enforced without certification inference. |
| Feature Contract ownership | PASS | Intent, feasibility and receipt boundaries converge. |
| Feature Contract fixture breadth | PASS | Matrix `sha256:139d…42b6` registers 40/40 governed pairs, 2 positive and 3 rejection fixtures, and zero production-certification claims; CRC-402 resolved. |
| Categories and profiles | PASS | Five categories and four conversational profiles converge. |
| Format 02 | PASS | Canonical ID plus governed alias; `contract_compatible`; not certified. |
| Lifecycle and compatibility | PASS | Acceptance, acknowledgement, fencing, migrations and no-fork rules converge. |
| XRI sole authority | PASS | Program Control is the only canonical XRI authority. |
| XRI reference completeness | PASS | Zero undefined active references. |
| XRI repository redefinitions | PASS | None found; local issues use `DLG-ISSUE-*`. |
| XRI uniqueness and history | PASS | Zero duplicates; historical aliases labeled; XRI-001/XRI-002 unchanged. |
| Repository status truth | PASS | All four status surfaces agree on release and authorization state. |
| Signing, publication and readiness | CONCERNS | RC4 remains unsigned/unpublished and product evidence gates remain open. |

## Authorization boundary

Builder Step 4, VAE Stage 5, RC4 signing/publication and production
implementation remain unauthorized.

CRC-401 and CRC-402 are resolved in `CRC_STATUS_REGISTRY.yaml`; CRC-403 remains
open. Next permitted actions are CRC-403 and operational-XRI evidence closure,
followed only by the affected readiness or certification gates.
