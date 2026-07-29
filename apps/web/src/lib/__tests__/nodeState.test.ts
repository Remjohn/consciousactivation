// TS-APP-UI-003 - nodeState.ts tests
// AC coverage: correctness of WS_STATE_TO_COARSE mapping (feeds AC-004)

import { describe, it, expect } from "vitest";
import { coarseFromWsState, STUDIO_STATUS_TOKEN, type StudioNodeStatus, type CoarseNodeState } from "../nodeState";

describe("coarseFromWsState", () => {
  it("should map BLOCKED to idle", () => {
    expect(coarseFromWsState("BLOCKED")).toBe("idle");
  });

  it("should map READY to active", () => {
    expect(coarseFromWsState("READY")).toBe("active");
  });

  it("should map DISPATCHED to active", () => {
    expect(coarseFromWsState("DISPATCHED")).toBe("active");
  });

  it("should map RUNNING to active", () => {
    expect(coarseFromWsState("RUNNING")).toBe("active");
  });

  it("should map SUCCEEDED to done", () => {
    expect(coarseFromWsState("SUCCEEDED")).toBe("done");
  });

  it("should map FAILED to failed", () => {
    expect(coarseFromWsState("FAILED")).toBe("failed");
  });

  it("should map QUARANTINED to failed", () => {
    expect(coarseFromWsState("QUARANTINED")).toBe("failed");
  });

  it("should map CANCELLED to stopped", () => {
    expect(coarseFromWsState("CANCELLED")).toBe("stopped");
  });

  it("should map INVALIDATED to stopped", () => {
    expect(coarseFromWsState("INVALIDATED")).toBe("stopped");
  });

  it("should return idle for unknown states (future-proofing)", () => {
    expect(coarseFromWsState("UNKNOWN_FUTURE_STATE")).toBe("idle");
  });
});

describe("STUDIO_STATUS_TOKEN", () => {
  it("should have entries for all StudioNodeStatus values", () => {
    const statuses: StudioNodeStatus[] = [
      "PENDING", "READY", "RUNNING", "WAITING_HUMAN",
      "SUCCEEDED", "FAILED", "CANCELLED", "INVALIDATED"
    ];

    statuses.forEach((status) => {
      expect(STUDIO_STATUS_TOKEN[status]).toBeDefined();
      expect(STUDIO_STATUS_TOKEN[status].color).toBeTruthy();
      expect(STUDIO_STATUS_TOKEN[status].label).toBeTruthy();
    });
  });

  it("should map WAITING_HUMAN to 'Needs you'", () => {
    expect(STUDIO_STATUS_TOKEN.WAITING_HUMAN.label).toBe("Needs you");
  });

  it("should use ca-waiting color for WAITING_HUMAN", () => {
    expect(STUDIO_STATUS_TOKEN.WAITING_HUMAN.color).toBe("var(--ca-waiting)");
  });
});
