# Implementation Scope

Accept one answer from an authorized human for the active question package; preserve
the raw answer separately from the normalized final decision; create a deterministic
immutable IR decision amendment; persist a complete decision receipt and resumable
memory atomically; compute ready/locked/cascade-complete state; reject replayed human
approval, contradictory locks, stale packages and unauthorized actors; allow explicit
non-destructive reopening that invalidates affected descendants.

The amendment is an input contract for later canonical Harness IR compilation. This
Story must not compile or mutate the canonical `HarnessIR` aggregate.
