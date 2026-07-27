# Security and authority boundaries

Deterministic Builder code owns parsing, validation, canonicalization, hashing, compatibility checks, impact analysis, atomic commit and receipt issuance. The ST-04.03 Phase Graph and its upstream lineage are immutable inputs. Field owners remain the only authorities for authoritative values; consumers may validate and derive new subordinate artifacts but may not rewrite upstream truth.

The repository-local synthetic input declares contract shape only and cannot override constitutional precedence, human ratification, Source Lock, frozen boundary, Harness IR or predecessor authority. Missing or stale authority fails closed. `NOT_APPLICABLE` remains explicit where present.

BF-AM-005 removes BD-014 only from this Builder-internal mode. Delegation and VAE contracts remain externally owned; no external handoff, runtime call or local schema fork is allowed. The fixture is synthetic, repository-owned, non-production, non-certified and Builder Core validation only.
