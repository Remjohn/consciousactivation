# Implementation Scope

Implement one deterministic local domain model and one application command that:

1. loads the current run, Source Lock and active Evidence Index;
2. validates their exact identity, current status, authority and lineage;
3. validates the capsule-governed category-neutral Saturation Contract;
4. derives role/specimen/traceability coverage and typed gaps or conflicts without
   producing any new semantic claim;
5. issues exactly one allowed saturation result and downstream consequence;
6. atomically attaches the immutable evaluation, receipt, event, command record and
   observation outbox entry;
7. supports payload-safe replay, query, invalidation and historical reproduction.

The synthetic complete case may issue `PASS`. Recoverable missing or sparse evidence
must issue the corresponding blocked/insufficient result. Contradictory authority
must issue `BLOCKED_CONTRADICTORY_AUTHORITY`. `PASS_WITH_LIMITATIONS` requires an
explicit human waiver and cannot be produced by the code-only synthetic command.

No lifecycle transition beyond the current Builder-owned run attachment is required;
later atomicity and Genesis remain separate Stories.
