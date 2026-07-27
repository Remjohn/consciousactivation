# ST-01.02 Failure and Rollback Evidence

Verdict: `PASS`

## Atomic runtime rollback demonstration

The deterministic in-memory adapter was instructed to fail the next atomic
evidence-workspace commit. The command had already completed read-only
diagnostics and constructed candidate events and a Source Lock, but none became
authoritative:

| State | Run events | Source Locks | Command record |
|---|---:|---:|---:|
| Before injected failure | 2 | 0 | absent |
| After `AtomicCommitFailed` | 2 | 0 | absent |
| After retry | 5 | 1 | present |

The retry committed exactly once. The failure code was `AtomicCommitFailed`;
both failure observations retained typed context. This proves that events, the
Source Lock, and the idempotency receipt share one atomic visibility boundary
in the bounded development/test adapter.

## Source immutability and cleanup

- The governed target candidate retained SHA-256
  `82f86a94e1183ee3d475277734b03eb5f2ab3d2bb7afe0520b8828105917337b`
  and unchanged modification metadata before and after successful inspection.
- Directory and ZIP tests compare pre/post entry sets and hashes.
- ZIP inputs are streamed and hashed in place; no extraction path exists.
- Every runtime-created directory and ZIP is owned by a `TemporaryDirectory`
  context and was disposed after success and exception paths.
- Typed diagnostic failures leave the original two run-creation events, zero
  Source Locks, and zero command records.

## Governed code rollback procedure

A code rollback must be separately authorized. It must remove only the three
new ST-01.02 source modules and seven ST-01.02 test files, restore the seven
modified existing implementation/test files to the `previous_sha256` values in
`FILE_CHANGE_MANIFEST.yaml`, and remove only this Story's completion directory.
Original ST-01.01 and supplemental completion evidence must remain untouched.

The capsule-amendment authorization is historical governance evidence and must
not be silently erased. Any rollback must issue its own receipt and reconcile
the capsule authorization state explicitly.
