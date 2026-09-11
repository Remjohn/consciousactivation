# CAE WP-09 — First Vertical Runtime Slice

**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Work package:** WP-09 — one real existing evidence-source path into CAE
**Environment:** Interview Expression repository-integrated fixture (`E2`) plus
private Supabase Storage and PostgreSQL staging (`E3`).

## Objective and boundary

Bridge one existing Interview Expression `canonical_interview_source_package`
to the bounded CAE evidence-to-AIR slice. The bridge establishes the exact
meaning of CAE `VERIFIED` for this path: an immutable legacy package payload
matches its stored package hash, its admitted source file is available at the
governed local-media locator, and the source bytes/size match the admitted
media asset before those exact bytes are copied into private Supabase Storage.

The bridge is CAE-side and read-only with respect to Interview Expression. It
does not change the Interview SQLite schema, source package, local-media file,
API route, legacy state authority, or runtime cutover. It makes no semantic,
human-truth, taste, derivative-publication, or production claim.

## Brownfield adapter

The existing path is:

```text
API local-media layout: CA_MEDIA_ROOT/interviews/{workspace}/{project}/{file}
  + Interview Expression canonical source package in interview.db
  -> WP-09 read-only verification adapter
  -> private cae-media object copy
  -> typed CAE source registration
  -> existing CAE evidence.capture operation
```

`InterviewExpressionSourceBridge` accepts only a current legacy object whose:

- object type is `canonical_interview_source_package`;
- canonical package payload reproduces its recorded SHA-256;
- source kind is `INTERVIEW_EXPRESSION`;
- source lifecycle is `ADMITTED` or `COMPONENTS_IN_PROGRESS`;
- operator source-authority fields are present (they are preserved as source
  evidence, not interpreted as a new permission authority);
- media set contains exactly one complete admitted asset; and
- `workspace://{workspace}/{project}/{file}` resolves under the existing
  `CA_MEDIA_ROOT/interviews/` layout without traversal.

It hashes local bytes and compares both digest and byte count before copying.
It then calls only `cae.bridge.register-interview-source@1.0.0`. Migration
`0009_cae_interview_source_bridge_operation.sql` adds that operation and
`STC-BRIDGE-000` (`source_package: CREATED -> VERIFIED`). The operation writes
the CAE media/source package, state transition, event, envelope receipt,
execution receipt, and immutable upstream-reference payload atomically.

The Storage object key is deterministic from the legacy immutable reference and
media digest. On a retry, an existing object is re-read and re-hashed; HTTP
400/409 alone is never treated as proof of the correct object.

## What was proven

`scripts/cae/verify_wp09_interview_source_bridge.py` created a disposable
Interview Expression SQLite source through its actual `SourcePackageService`,
using the same local-media layout as the API. The real CAE bridge then:

1. verified legacy package identity and media bytes;
2. copied the exact bytes to private Supabase Storage;
3. registered a CAE `INTERVIEW_EXPRESSION` source package and `VERIFIED` media
   asset via the new typed operation;
4. replayed the bridge idempotently, yielding the original receipt;
5. fed the CAE source into the existing `capture_evidence` operation; and
6. force-rolled back all PostgreSQL fixture rows, deleted the temporary Storage
   object, and left the legacy package's hash/revision unchanged.

The following adversarial checks passed:

| Test | Shortcut prevented | Result |
|---|---|---|
| package-payload tamper | reuse recorded legacy hash after changing package contents | rejected before CAE transition |
| local-media tamper | reuse admitted logical URI/hash after bytes changed | rejected before CAE transition |
| replay duplication | create two CAE verified sources from one request | original receipt replayed |
| unusable `VERIFIED` state | mark source verified but fail the existing capture path | typed capture accepted |

The governed metadata is in
`docs/cae/evaluations/INTERVIEW_SOURCE_BRIDGE_WP09_EVALUATION_SUITE.yaml`.

## What remains explicitly unproven

- No operator’s existing Interview Expression SQLite data was read, copied, or
  migrated. The source was a disposable repository-integrated fixture.
- No API route or service invokes the bridge; it is a callable CAE adapter.
- The existing local media store remains an upstream source location, not CAE
  durable authority. CAE becomes authoritative only for the isolated copied
  object and CAE transition slice.
- The legacy `source_authority` declaration is structurally required but not a
  complete rights, consent, publication, or production authorization system.
- No transcript/component reconciliation, semantic assessment truth, SDA/SFL
  resolution, human review, taste, anti-centroid quality, or E4 outcome exists.

## Rollback and recovery

The CAE database transaction rolls back if typed registration fails. If a
newly copied Storage object was created before that failure, the adapter deletes
it best-effort; a pre-existing verified matching object is retained. The
bridge never deletes or mutates local Interview Expression bytes or SQLite
records. Disabling the adapter removes the new path without affecting legacy
runtime behavior; existing CAE receipts remain immutable diagnostic history.

## Exact operator decision

**Promote WP-09 and authorize WP-10 regression/promotion/operator acceptance
for the bounded vertical slice, without treating the staging bridge as a
repository-wide SQLite cutover or a claim that PostgreSQL/Supabase now owns all
existing CAE operational state?**
