# Given/When/Then Acceptance Criteria

## AC-01 — Dependency-bound run

**Given** a PASS original ST-01.01 receipt, a PASS supplemental receipt, and a
run created under `synthetic_text_normalization_v1@1.0.0`, **when** source-lock
creation is requested, **then** the command uses that exact run/profile identity
and rejects any Format 02, category, external, conversational, or ungoverned
profile substitution without mutation.

## AC-02 — Exact portable source profile and candidate

**Given** the hash-valid `synthetic_task_definition_source_v1@1.0.0`, **when**
the workspace is resolved, **then** the exact `repo://` target candidate exists,
matches its pinned SHA-256, has complete repository authority/license/privacy
metadata, and no absolute workstation path enters the persisted descriptor.

## AC-03 — Pre-commit actionable diagnostics

**Given** a missing path, unsupported source kind/media type, absent required
role, wrong pinned hash, or incomplete authority metadata, **when** diagnostics
run, **then** a typed actionable rejection is emitted before any run event,
Source Lock, or command receipt is committed.

## AC-04 — Read-only file, directory, and ZIP handling

**Given** bounded approved synthetic file, directory, and ZIP fixtures, **when**
they are diagnosed and locked, **then** originals and containing directories are
byte/metadata unchanged, no ZIP is extracted, ordered descriptors are stable,
and a repeated run produces the same content and aggregate identities.

## AC-05 — Fail-closed path and archive safety

**Given** traversal, absolute paths, symlinks, case-fold collisions, executable
surprise, nested archives, decompression ratio overflow, file-count/depth/byte
overflow, or malformed ZIP input, **when** inspected, **then** it is rejected
with the exact typed reason, temporary data is cleaned, and state is unchanged.

## AC-06 — Complete immutable descriptor contract

**Given** accepted source bytes, **when** descriptors are created, **then** each
has stable content identity, portable provenance, relative path/member,
source kind, required role, precedence, authority, license, privacy class,
media type, byte size, available timestamp, SHA-256, and discovery origin.

## AC-07 — Content identity with preserved provenance

**Given** identical bytes at two approved relative paths, **when** locked,
**then** they share content identity while retaining distinct portable provenance
and deterministic specimen/source descriptor identities.

## AC-08 — Immutable aggregate lock and invalidation

**Given** a committed Source Lock, **when** the same command is replayed, **then**
the prior receipt and lock are returned without duplicate authoritative events;
**and when** a locked byte changes under a new command, **then** a new lock/version
and explicit invalidation relationship are produced without altering history.

## AC-09 — Authority, concurrency, receipt, and observability

**Given** human/code actors with exact grants plus agent/external actors without
commit authority, **when** commands are attempted, **then** only an authorized
actor can atomically move the run through `SOURCE_DIAGNOSTIC` to `SOURCE_LOCKED`;
unauthorized, stale-version, or command-payload-reuse attempts fail without
mutation and all outcomes emit the required trace and receipt fields.

## AC-10 — Builder Core boundary

**Given** the successful locked workspace, **when** architecture and dependency
tests run, **then** the implementation remains category-neutral, non-production,
non-certified, uses no external dependency, does not compile or execute a
Harness, and imports or invokes no Format 02, VAE, Delegation runtime,
conversational, GPU/provider, evaluator, publication, or later-Story behavior.
