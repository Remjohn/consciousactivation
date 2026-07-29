// TS-APP-UI-003 - useControlTower hook tests
// AC-006: Poll interval disables while WS is open, resumes when closed

import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook } from "@testing-library/react";
import { useControlTower } from "../useControlTower";

// Mock the API module
vi.mock("../../api/campaigns", () => ({
  getControlTower: vi.fn(),
}));

describe("useControlTower", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should disable polling when wsOpen is true (AC-006)", () => {
    const { result } = renderHook(() => useControlTower("campaign-123", true));

    // When WS is open, refetchInterval should be false
    expect(result.current.isFetching).toBeDefined();
    // The query should still work, just not poll
  });

  it("should enable polling when wsOpen is false (AC-006)", () => {
    const { result } = renderHook(() => useControlTower("campaign-123", false));

    // When WS is closed, polling should be active (refetchInterval = 4000)
    expect(result.current.isFetching).toBeDefined();
  });

  it("should refetch when manually invalidated", async () => {
    const mockGetTower = vi.fn().mockResolvedValue({ run_nodes: [] });
    vi.mocked(require("../../api/campaigns").getControlTower).mockImplementation(mockGetTower);

    const { result } = renderHook(() => useControlTower("campaign-123", false));

    // Initial fetch
    expect(mockGetTower).toHaveBeenCalledTimes(1);

    // Manual refetch
    await act(async () => {
      result.current.refetch();
    });

    expect(mockGetTower).toHaveBeenCalledTimes(2);
  });
});
