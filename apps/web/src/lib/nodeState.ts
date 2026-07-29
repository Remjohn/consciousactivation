// TS-APP-UI-003 - Node State Normalization
// Source gap notice 1 resolution: Two separate vocabularies for node status

// Authoritative — sourced only from GET .../tower. Matches RunNodeProjectionModel.status exactly.
export type StudioNodeStatus =
  | "PENDING" | "READY" | "RUNNING" | "WAITING_HUMAN"
  | "SUCCEEDED" | "FAILED" | "CANCELLED" | "INVALIDATED";

// Coarse — sourced only from the WS stream (TS-APP-API-005's raw NodeState). Visual/pulse only.
export type CoarseNodeState = "idle" | "active" | "done" | "failed" | "stopped";

const WS_STATE_TO_COARSE: Record<string, CoarseNodeState> = {
  BLOCKED: "idle",
  READY: "active",
  DISPATCHED: "active",
  RUNNING: "active",
  SUCCEEDED: "done",
  FAILED: "failed",
  QUARANTINED: "failed",   // late/unconsumable result — same failed color family,
                            // distinct tooltip ("late result, not a content failure")
  CANCELLED: "stopped",
  INVALIDATED: "stopped",
};

export function coarseFromWsState(state: string): CoarseNodeState {
  return WS_STATE_TO_COARSE[state] ?? "idle"; // unknown future state: render inert, never crash
}

export const STUDIO_STATUS_TOKEN: Record<StudioNodeStatus, { color: string; label: string }> = {
  PENDING:       { color: "var(--ca-idle)",    label: "Pending" },
  READY:         { color: "var(--ca-gold-500)",label: "Ready" },
  RUNNING:       { color: "var(--ca-gold-500)",label: "Running" },
  WAITING_HUMAN: { color: "var(--ca-waiting)", label: "Needs you" },
  SUCCEEDED:     { color: "var(--ca-success)", label: "Succeeded" },
  FAILED:        { color: "var(--ca-danger)",  label: "Failed" },
  CANCELLED:     { color: "var(--ca-idle)",    label: "Cancelled" },
  INVALIDATED:   { color: "var(--ca-idle)",    label: "Invalidated" },
};

// Lifecycle state badge colors (separate from node status)
export const LIFECYCLE_STATUS_TOKEN: Record<string, { color: string; label: string }> = {
  DRAFT:           { color: "var(--ca-idle)",      label: "Draft" },
  READY_TO_SHIP:   { color: "var(--ca-success)",   label: "Ready to Ship" },
  RUNNING:         { color: "var(--ca-gold-500)",   label: "Running" },
  PAUSED:          { color: "var(--ca-waiting)",    label: "Paused" },
  SHIPPED:         { color: "var(--ca-success)",    label: "Shipped" },
  ARCHIVED:        { color: "var(--ca-text-tertiary)", label: "Archived" },
};
