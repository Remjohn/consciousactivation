# Phase 2 — Runtime Event / Trace Contract

Required causal trace:

PROGRAM_REQUESTED
→ AUTHORIZED
→ STATE_ENTERED
→ AGENT_STARTED
→ SKILL_LOADED
→ TOOL_REQUESTED
→ TOOL_ALLOWED/BLOCKED
→ OPERATION_STARTED
→ EFFECT_PENDING
→ EFFECT_SETTLED/UNCERTAIN
→ ARTIFACT_CHANGED
→ RECEIPT_COMMITTED
→ TRANSFER_CHECKED
→ TRANSFERRED / REPAIRED / BLOCKED
→ COMPLETED

Every event/trace must carry stable run/program/operation IDs, Workspace, lane, agent/subagent, Skill hash/version,
tool/capability ID, hook result, artifact/receipt IDs and replay/recovery status where relevant.
Do not log secret values or sensitive content merely for telemetry.
