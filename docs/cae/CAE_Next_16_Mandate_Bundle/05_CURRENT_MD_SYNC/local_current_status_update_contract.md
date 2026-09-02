# Local Current-State Update Contract

When M49–M64 changes a local service/package, update that component's existing `CURRENT.md` or `CURRENT_PROJECT_STATUS.md` in the same execution session.

Required fields:
- mandate ID;
- current verified behavior;
- exact changed paths;
- commands/tests;
- runtime evidence;
- blockers;
- next owner;
- exact commit SHA;
- link/reference to canonical PRD current-state entry.

Do not create a competing authority file simply because a directory lacks one today. If no local current-state file exists and the mandate genuinely needs one, record that as an explicit deliverable and justify its authority boundary.
