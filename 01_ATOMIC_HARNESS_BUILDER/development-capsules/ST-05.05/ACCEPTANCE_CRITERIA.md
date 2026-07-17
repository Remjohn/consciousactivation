# Acceptance Criteria

- Given an exact capsule and authorized actor, when pin/verify/activate/dispose runs, then every transition emits an immutable deterministic receipt.
- Given a disposed or invalidated capsule, when active reuse is attempted, then it fails closed while historical reproduction remains available.
- Given an empty or mismatched capsule/package hash, when any operation runs, then it fails closed without silent upgrade.
- Given identical command and payload, when repeated, then the original receipt returns; a conflicting payload fails closed.
- Given injected failure, when a transition runs, then prior state is preserved and no command or receipt commits.
- Given lifecycle success or rejection, when observed, then typed evidence identifies story, operation, actor, artifact, outcome, and failure context.
