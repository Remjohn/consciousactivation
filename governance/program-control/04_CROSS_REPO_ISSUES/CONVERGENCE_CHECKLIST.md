# Cross-Repository Convergence Gate

Run against Delegation `1.1.0-rc.4` only after both consumers pin its exact local immutable bytes. RC1, RC2 and RC3 are historical rejection evidence, not current dependencies.

Current state: RC4 consumer pins and bounded validation pass; a fresh read-only convergence audit is the next permitted action. This checklist grants no implementation or production authorization.

- [ ] Shared field names and meanings match.
- [ ] Field-level authority ownership matches.
- [ ] Required/optional status matches.
- [ ] Contract and compatibility versions are pinned.
- [ ] Wrong-reading locks are preserved and enforced.
- [ ] Activative semantic lineage survives end to end.
- [ ] Reaction Receipt and Expression Moment references survive end to end.
- [ ] Supersession and invalidation semantics match.
- [ ] Production acceptance and consumption acknowledgement remain distinct.
- [ ] No local schema fork exists.
- [ ] Format 02 fixtures pass across all three repositories.
