# Failure and Rollback Plan

All validation occurs before atomic commit. Injected failure leaves zero decision
artifacts, event, command, receipt, memory or outbox intent. Rollback is an immutable
reopen/invalidation artifact; it clears active decision state and invalidates affected
descendants while retaining exact historical bytes. Re-entry requires a new command
and immutable amendment version.
