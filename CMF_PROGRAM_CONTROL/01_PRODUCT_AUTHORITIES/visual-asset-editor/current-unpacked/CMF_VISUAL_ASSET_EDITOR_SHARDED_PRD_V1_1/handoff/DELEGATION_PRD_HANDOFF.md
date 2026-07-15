# Delegation PRD Handoff

## Product to plan next

**Content Harness ↔ Visual Asset Editor Delegation Contract**

The products are independently versioned. Their shared ABI therefore needs its own PRD rather than being finalized inside either product.

## Inputs

- this Visual Asset Editor PRD;
- the validated Atomic Harness Builder PRD and architecture;
- representative Format 02 Content Harness demand fixtures;
- the contract examples in [`../contracts/examples/`](../contracts/examples/);
- V2.1 delegation doctrine.

## Questions the Delegation PRD must resolve

1. Canonical shared product promise and users.
2. Exact field ownership across demand, submission, event, conflict, geometry, evaluation, repair, budget and result contracts.
3. Contract versioning and compatibility negotiation.
4. Idempotency, amendment, supersession, cancellation and retry semantics.
5. Terminal states and error taxonomy.
6. Event ordering, delivery guarantees and replay.
7. Caller authentication and authorization.
8. Object storage, URI, hash, access and retention behavior.
9. Backpressure and budget negotiation.
10. Human exception and degraded-result authority.
11. Content Harness consumption and final composition validation.
12. Conformance tests, fixtures, migration and rollback.

## Frozen boundary

The Delegation PRD may define the interface. It may not merge the two products, transfer Content Harness semantic authority to the editor, or expose provider-specific ComfyUI details as public contract requirements.
