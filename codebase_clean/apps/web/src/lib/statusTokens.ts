import type { CampaignLifecycleState } from "../api/types";

/**
 * Lifecycle badge color/icon lookup table.
 * Maps all eight CampaignLifecycleState values onto the CA design system palette
 * (see TS-APP-UI-002 §5).
 */
export const LIFECYCLE_TOKENS: Record<
  CampaignLifecycleState,
  { color: string; icon: string; filled: boolean }
> = {
  DRAFT: { color: "state-inactive", icon: "circle-dashed", filled: false },
  LAUNCHED: { color: "gold", icon: "rocket", filled: true },
  RUNNING: { color: "state-running", icon: "loader", filled: true },
  AWAITING_REVIEW: { color: "state-awaiting", icon: "pause", filled: true },
  BLOCKED_EXCEPTION: { color: "state-blocked", icon: "flag", filled: true },
  READY_TO_SHIP: { color: "state-ready", icon: "check", filled: true },
  SHIPPED: { color: "state-shipped", icon: "check-check", filled: true },
  CANCELLED: { color: "state-inactive", icon: "x", filled: true },
};
