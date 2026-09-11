# Instructions for Workspace + Guest Operating Context Program

1. Ensure caller holds authenticated TenantContext with matching workspace_id.
2. Initialize Program aggregate under COMMANDER authority.
3. Configure Workspace isolation boundaries and operational metadata.
4. Register exactly ONE active Guest participant for the session under HUNTER authority.
5. Ingest and bind source evidence items under ANALYST authority.
6. Derive subordinate Persona/Brand context with full cryptographic SHA-256 lineage back to bound source evidence.
7. Activate the single Guest operating context under COMMANDER authority.
8. If scope violations or evidence corruptions occur, route to REPAIRING and recover via repair_context.
