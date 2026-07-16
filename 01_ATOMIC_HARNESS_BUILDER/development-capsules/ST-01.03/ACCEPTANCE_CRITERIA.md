# Acceptance criteria

1. Given a hash-valid active Source Lock and authorized Builder code actor, when
   indexing is requested, then exactly one immutable specimen is created for every
   descriptor and no descriptor or specimen is omitted or duplicated.
2. Given an indexed specimen, when queried, then its observation, governed status,
   knowledge status and provenance are distinct typed values linked to the exact
   Source Lock, descriptor and run.
3. Given identical governed inputs in fresh contexts, when indexed, then canonical
   index bytes, index identity and receipt identity are byte-identical.
4. Given a changed descriptor, Source Lock, adapter version or classification, when
   indexed, then a new immutable index identity is produced.
5. Given a missing descriptor, identity collision, conflicting duplicate,
   missing/invalid provenance or unsupported knowledge status, when validation runs,
   then the command fails closed with no partial state.
6. Given an unauthorized, stale, superseded or invalidated run/Source Lock, when
   indexing is requested, then it is rejected before any active index is committed.
7. Given an identical repeated command, when replayed, then the original receipt is
   returned without duplicate index, event or decision state; a conflicting payload
   is rejected.
8. Given an injected commit or observation-delivery failure, when the command runs,
   then commit is all-or-nothing and a committed result is never reported as
   uncommitted; pending observations can be retried without duplicate delivery.
9. Given an upstream invalidation, when applied, then the active descendant index is
   invalidated while historical bytes and receipt remain reproducible.
10. Given 100,000 valid descriptors, when the pure index compiler runs, then all are
    covered in deterministic canonical order without external services or unbounded
    duplicate structures.
11. Given the Story public seam, when success or failure occurs, then observations
    include run, Story, artifact, authority, version, provenance, outcome and typed
    failure context, and success links to the completion receipt.
12. Given repository boundary checks, when the implementation is inspected, then it
    adds only the authorized modules, standard-library imports and no Format 02,
    conversational, VAE, Delegation-runtime, provider or production behavior.
