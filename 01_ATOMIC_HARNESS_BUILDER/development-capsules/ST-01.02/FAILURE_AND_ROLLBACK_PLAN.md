# Failure, Rollback, and Cleanup Plan

All source acquisition and validation occurs before the atomic repository
commit. A typed failure must leave the run stream, lock store, command records,
and source tree unchanged.

Required typed failures include missing/escaped path, profile/hash/authority
mismatch, unsupported kind/media, required-role gap, unsafe archive/member,
symlink, executable, resource-limit overflow, source mutation during read,
stale stream version, idempotency payload mismatch, and authority denial.

The development/test adapter must commit the run events and Source Lock as one
operation. Injected commit failure must prove neither becomes visible. A retry
with the same command identity after a successful commit returns the original
receipt without new events.

Rollback is additive and non-destructive: remove only the three new source
modules and ST-01.02 tests, restore the exact previous hashes of the six allowed
modified files, and remove only ST-01.02 completion evidence. No migration,
external compensation, source rewrite, or original/supplemental receipt change
is permitted.

Runtime-created temp directories/ZIPs must be disposed after every test,
including exceptions. The completion receipt must include pre/post source
hashes, an injected-failure atomicity result, and exact previous/current hashes
for every modified existing file.
