---
title: TS-DLG-01 Contract Registry and Common Envelope
product: CMF Content Harness Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: stage2_draft_for_review
created: 2026-07-14
---

# TS-DLG-01 Contract Registry and Common Envelope

## 1. Identity and requirement coverage

- Primary features: F01, F03
- Owned FRs: FR-001 through FR-008 and FR-017 through FR-024
- Owned NFRs: NFR-CONTRACT-001, NFR-CONTRACT-002, NFR-PERF-004, NFR-GOV-001
- Decisions: D001, D003
- Resolves: ADR-DLG-001, ADR-DLG-002, ADR-DLG-003 for canonical payload/hash rules, ADR-DLG-006, ADR-DLG-007, ADR-DLG-015
- Journeys: UJ-01, UJ-02, UJ-03, UJ-10, UJ-13, UJ-14
- Supporting specs: TS-DLG-02 authority/signatures, TS-DLG-03 lifecycle/idempotency, TS-DLG-04 compatibility, TS-DLG-09 conformance

## 2. Sources read

The normative inputs are `prd/05-features/F01-protocol-boundary.md`, `prd/05-features/F03-contract-family.md`, `governance/PROTOCOL_CONSTITUTION.yaml`, `governance/MESSAGE_TYPE_REGISTRY.yaml`, `governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`, `governance/COMPATIBILITY_POLICY.yaml`, `contracts/PROTOCOL_VERSION_POLICY.md`, all 25 schemas/examples, the Stage 1 ownership register, baseline manifest, coverage matrix, delta ADR register and `CROSS_REPO_ISSUES.md`. Upstream product packages remain unavailable under XRI-001 and XRI-002.

## 2A. Cross-cutting protocol obligations

| Concern | Normative obligation in this specification |
|---|---|
| Service and library boundaries | Only the modules and ports named here are owned; Content Harness meaning, VAE production and the existing Control Tower remain external owners. |
| Canonical schemas and field-level authority | Public payloads are closed, versioned and registry-owned; every value path has one owner and every state-changing principal/action is validated before effect. |
| Lifecycle, correlation and causation | TS-DLG-03 transition rules apply; every message keeps the exact correlation and names its direct accepted cause unless it is the initial command. |
| Idempotency versus replay | Legitimate identical command delivery returns the prior receipt; nonce/message/key reuse with different bytes, scope or invalid state is rejected as replay/conflict. |
| Compatibility, adapters and migrations | TS-DLG-04 negotiation is pinned before admission; adapters/migrations are deterministic, lossless for mandatory meaning and cannot transfer authority. |
| Event routing and audit chain | Accepted/rejected actions are receipted; accepted messages route only after atomic message/state/audit/outbox commit. |
| Cancellation and race precedence | TS-DLG-03/05 committed-sequence rules apply; accepted cancellation or supersession blocks later stale promotion for its scope. |
| Supersession and selective invalidation | Old facts remain immutable; owner-authored changed paths and VAE evidence determine conservative reuse and exact invalidation. |
| Result acknowledgement | VAE production acceptance remains separate from Content Harness/composition-runtime downstream acknowledgement under TS-DLG-06. |
| Invalidation, revocation and replacement | Post-completion authorization changes use new notices and impact analysis; no completed result or historical use is overwritten. |
| Failure, persistence and transactions | Failures use the canonical taxonomy; state-changing acceptance fails closed unless durable protocol records and audit commit atomically. |
| Observability and SLOs | TS-DLG-08 source-linked projections, bounded metrics, incident rules and SLO definitions apply to all behavior specified here. |
| Threat model and test architecture | The threat and test sections below include negative, adversarial, recovery and Given/When/Then evidence for this spec's owned behavior. |

## 3. Problem, solution and scope

The local package has 25 valid draft schemas but lacks canonical schema IDs, closed nested definitions, uniform resource identity and a single generated registry. The solution is a transport-neutral contract package whose registry is generated from canonical schema metadata and whose common envelope points to immutable canonical payloads.

The observable boundary accepts a byte sequence plus transport metadata and returns either a receipted rejection or a persisted/routed canonical message. It performs no semantic interpretation, creative ranking, production planning or visual evaluation.

## 4. Architecture and product integration

The target library boundary is:

```text
Transport adapter -> Envelope decoder -> Registry lookup -> Payload resolver
                  -> Canonical/hash checks -> authority/compatibility/lifecycle pipeline
                  -> transactional message/audit persistence -> outbox route
```

Required modules are `contract-registry`, `canonical-codec`, `envelope-validator`, `resource-reference`, `inbound-port`, `outbound-port` and generated bindings. These are protocol modules, not replacements for Content Harness, VAE or Control Tower owners.

Content Harness integration emits demands and owner-authorized commands through an inbound port. VAE integration consumes accepted commands and emits production facts through the same public ABI. Control Tower consumes projection events defined by TS-DLG-08; it does not read transport-specific payloads directly.

## 5. Canonical registry and version policy

Each public payload schema shall declare:

- `$id`: `https://contracts.cmf.dev/delegation/<message_type>/<major>.<minor>/schema.json`
- `x-cmf-message-type`, `x-cmf-message-version`, producer principal types, consumer principal types, authority scopes, lifecycle effects, idempotency class and compatibility status
- `additionalProperties: false` at every public object boundary
- an optional `extensions` object only where registered extension namespaces are allowed

Wire `protocol_version` and `message_version` use `MAJOR.MINOR`. Package releases use SemVer `MAJOR.MINOR.PATCH`. Patch releases may correct descriptions, examples or generators without changing accepted wire instances. A required field, authority change, lifecycle change or changed acceptance meaning requires a major version. Backward-compatible optional fields require a minor version and a declared feature token.

The checked-in machine registry is generated from schema metadata. Generation fails on duplicate IDs, missing owners, unknown principals, missing examples, unregistered lifecycle effects, unresolved schema references or a schema hash mismatch. Hand-edited parallel registries are prohibited.

Unknown message types and unsupported required feature tokens are rejected with `UNSUPPORTED_CONTRACT_VERSION` or the applicable compatibility failure. Unknown optional extension namespaces are preserved byte-for-byte but never influence authority, lifecycle, quality gates, budget or acceptance.

## 6. Common envelope and canonical resources

The target envelope retains the current fields and tightens them as follows:

| Field | Rule and owner |
|---|---|
| `protocol_version`, `message_type`, `message_version` | Protocol-defined values selected from the negotiated profile |
| `message_id` | Sender-generated UUIDv7 encoded as `MSG-<uuid>`; globally unique |
| `correlation_id` | Content Harness creates `DEL-<uuid>` for a new delegation; immutable thereafter |
| `causation_id` | Required for every message except the initial submission; equals the direct accepted causing message ID |
| `sender`, `recipient` | Registered principal identity and release version; sender-authored and authority-validated |
| `authority` | Claimed action and field scopes; sender-authored, protocol-validated |
| `occurred_at` | Sender event time in RFC 3339 UTC; not an ordering authority |
| `idempotency_key` | Required for state-changing commands; semantics defined by TS-DLG-03 |
| `payload_ref` | Immutable absolute URI resolved through an authorized resolver |
| `payload_hash` | `sha256:<64 lowercase hex>` over RFC 8785 canonical JSON payload bytes |
| `integrity` | Signature and replay fields defined by TS-DLG-02 and TS-DLG-03 |

YAML remains an authoring format only. Wire, hashing, signing and stored canonical payloads use UTF-8 JSON. Numbers that cannot be represented without ambiguity in interoperable JSON are prohibited. Timestamps are normalized to UTC with explicit `Z`; object key order has no semantic effect.

### Exact demand identity

All references to a Visual Asset Demand use one closed object:

```json
{
  "request_id": "VAD-...",
  "version": 1,
  "payload_hash": "sha256:...",
  "canonical_ref": "cmf-contract://visual-asset-demand/VAD-.../1"
}
```

This `DemandIdentityRef` replaces bare `demand_ref`, `accepted_demand_ref`, `previous_demand` and `new_demand` strings in the next major schemas. A receiver must resolve the reference, verify the hash and compare all four fields. Aliases and latest-version lookups are forbidden in state-changing paths.

### Extension policy

An extension key is a reverse-DNS namespace mapped to an immutable JSON value. A registry entry declares its owner, schema URI, version, mandatory/optional status and compatible consumers. Extensions may not shadow canonical fields. Any extension that changes required meaning must be promoted to a canonical field or negotiated required feature.

## 7. Field-level authority and principal permissions

Schema shape and compatibility metadata are owned by this repository. Payload values retain the field authority in `CONTRACT_OWNERSHIP_REGISTER.yaml`. The registry compiler requires exactly one `value_owner` or one deterministic owner-selection rule for every field.

The boundary service may create message/audit IDs, validation results and lifecycle projections. It may not create demand meaning, VAE production facts, acknowledgement decisions or owner-authored amendments. Content Harness and VAE principals may use only message types registered for their principal type. Transport service identities are delivery actors, never payload authorities.

## 8. Lifecycle, routing and cross-cutting behavior

- Initial submission creates a correlation and proposes `DRAFT -> SUBMITTED`; lifecycle acceptance is specified by TS-DLG-03.
- Transport arrival order never determines lifecycle order. Accepted transactional sequence does.
- Every accepted message is persisted once and routed through an outbox keyed by `message_id`.
- Every rejected message produces a rejection receipt without lifecycle mutation.
- Cancellation, supersession, amendments, results and post-completion notices use the same envelope; their domain precedence is defined in TS-DLG-05 and TS-DLG-06.
- Idempotent duplicate delivery returns the prior receipt. A different message reusing a key or ID is a conflict or replay, never a silent overwrite.
- Compatibility is negotiated before admission and pinned for the correlation under TS-DLG-04.
- Adapters run before payload acceptance, emit a new immutable representation and never rewrite the signed source.

Routing ports expose `accept(envelope_bytes, transport_context) -> receipt` and an ordered stream of accepted canonical messages. Transport context may supply delivery attempt and channel identity but cannot supply authority-bearing payload values. HTTP, queue, stream, local and fixture adapters must pass the same contract suite.

## 9. Validation and transaction rules

The full validation order is defined by TS-DLG-03. Contract-specific rules are:

1. Enforce byte and depth limits before parsing.
2. Decode strict UTF-8 JSON; reject duplicate object keys and non-finite numbers.
3. Validate envelope shape and select an exact registry entry.
4. Resolve the payload using recipient-scoped credentials.
5. Verify canonical payload hash before schema validation.
6. Validate against the exact schema ID/hash pinned by the registry.
7. Reject unknown canonical fields and unsupported mandatory extensions.

Message persistence, lifecycle mutation, audit receipt and outbox enqueue form one atomic transaction. Payload/resource storage may be external, but acceptance records its immutable URI, hash, availability lease and retention class. If audit persistence or outbox insertion fails, acceptance fails closed.

## 10. Failure, retry, invalidation and recovery

Malformed JSON, unknown schema, invalid reference, hash mismatch and unsupported version map to the contract/compatibility taxonomy. These failures do not consume VAE quality rounds. A corrected payload is a new message ID; a transport retry of identical bytes keeps the same ID and idempotency key.

Registry rollback selects the prior signed package for new correlations only. Existing correlations retain their pinned registry snapshot. A bad optional schema release may be deprecated; accepted historical messages remain resolvable by schema hash.

Supersession never edits the prior payload. Invalidation records affected references while retaining original bytes and hashes. Result acknowledgement and post-completion notices remain separate messages.

## 11. Security and threat model

Threats include parser differentials, hash confusion, schema substitution, malicious reference redirects, oversized payloads, extension smuggling, principal spoofing and transport bypass. Mitigations are strict parsing, RFC 8785 canonicalization, exact schema hash pinning, allowlisted URI schemes/hosts, recipient-scoped fetch credentials, size/depth limits, signatures, authority validation and identical transport conformance.

Secrets, media binaries and private reasoning traces are forbidden in public messages. References must not embed credentials. Resolvers log resource identity and result, not secret query parameters or payload content.

## 12. Observability and SLOs

Emit counters and latency histograms for decode, registry lookup, resource resolution, hash verification, schema validation, acceptance and rejection by stable reason code. Record `message_id`, correlation, schema ID/hash, principal IDs and receipt ID; never use free-form payloads as labels.

Targets inherited from the PRD are p99 valid receipt at or below 1000 ms, p99 duplicate resolution at or below 750 ms and 100% audit-receipt coverage. Resource-fetch time is reported separately. ADR-DLG-019 must benchmark realistic Format 02 payloads before targets are frozen.

## 13. Compatibility, adapters and migration

Registry packages declare active, discouraged, deprecated, read-only and retired versions. A consumer may accept multiple versions while emitting one preferred version. Required semantic fields cannot be dropped. A deterministic adapter produces a separately hashed target payload plus transformation receipt. Immutable migration follows TS-DLG-04. Rollback never converts stored messages in place.

## 14. Test architecture

- Schema tests compile every schema and validate positive and negative fixtures.
- Registry tests prove one-to-one schema/example/owner coverage and stable generation.
- Canonicalization vectors prove identical hashes across supported languages.
- Property tests vary key order, Unicode, numeric forms, unknown fields and extension namespaces.
- Contract tests run all transport adapters against identical accept/reject vectors.
- Security tests cover duplicate keys, reference redirects, hash substitution, parser bombs and schema downgrade.
- Integration tests verify atomic message/receipt/outbox behavior and pinned-registry recovery.

## 15. Given/When/Then acceptance criteria

1. Given a registered signed message and matching immutable payload, when any supported transport submits it, then every adapter yields the same canonical message and receipt.
2. Given a payload whose bytes differ from its declared hash, when accepted, then `PAYLOAD_HASH_MISMATCH` is receipted and no state/outbox record is created.
3. Given an unsupported required extension, when compatibility is checked, then the verdict is `INCOMPATIBLE` and the field is not ignored.
4. Given two JSON payloads differing only in object key order, when canonicalized, then their hashes match.
5. Given a bare demand string in a next-major message, when validated, then schema validation fails in favor of `DemandIdentityRef`.
6. Given a direct product-to-product invocation that bypasses the inbound port, when conformance is run, then the adapter is non-conformant and no protocol receipt can be produced.
7. Given an accepted historical message after registry rollback, when audited, then its exact schema remains resolvable by ID and hash.

## 16. Implementation tasks

1. Close all 84 open public object paths and define governed extensions.
2. Add canonical `$id` and metadata to every schema and generate the registry.
3. Define `DemandIdentityRef`, resource-reference and extension schemas.
4. Implement canonical JSON/hash test vectors before validators.
5. Define language-neutral inbound/outbound port interfaces and transport fixtures.
6. Generate target-language types and validators from the canonical package.
7. Add registry signing/publication hooks for Stage 3 without publishing yet.
8. Resolve upstream schema diffs under XRI-001 before contract freeze.

## 17. Explicit non-goals

- Content generation, semantic rewriting or composition decisions
- VAE Visual Production Plans, model/workflow selection, evaluation or asset generation
- A new Control Tower or mutable shared delegation record
- Transport-specific authority exceptions
- Stage 3 publication or Stage 5 runtime implementation in this stage

## 18. Readiness and blockers

Specification verdict: `CONCERNS`. The normative target is defined, but contract freeze requires the upstream schema diff, closure of all public object paths, normalized principals and executable canonicalization vectors. This spec does not authorize implementation.

## 19. V1.1 constitutional alignment amendment

The envelope protocol remains `1.0`; `visual-asset-demand` alone advances to
message version `1.1` in replacement package `1.1.0-rc.2`. Registry entries and schema IDs
must therefore resolve message version independently from envelope protocol
version. The demand schema is closed and requires the canonical Activative
lineage, Activation Contract, Visual Semantic Pack, Visual Narrative Program,
Feature Contracts, somatic T/V route, and non-empty wrong-reading locks.
Every referenced upstream object uses the exact resource ID, version, payload
hash, and canonical-reference tuple. The full demand remains the hash and
signature unit. Traceability: `CONST-LINEAGE-001`, `CONST-REACTION-001`,
`CONST-VERSION-001`.

## 20. RC2 consumer-conformance correction

The closed demand adds mandatory `source_provenance.source_kind` using the
governed enum. The schema conditionally requires non-empty Reaction Receipt and
Expression Moment references for `interview_expression`; supplied collections
are non-empty for every source kind. Registry, fixture, and manifest paths are
relative to the release root. RC1 remains immutable and consumer-rejected.
