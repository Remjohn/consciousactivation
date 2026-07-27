# Failure and Rollback Plan

All validation failures occur before commit. Injected transaction failure leaves zero
partial graph/package/receipt/event/command/outbox state. Non-destructive rollback
invalidates only the active question package and retains immutable history. A changed
definition, model, evidence or dependency completion set creates a new identity; no
prior package, boundary, model or evidence artifact is mutated.
