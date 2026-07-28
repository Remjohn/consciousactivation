import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { createElement, type ReactNode } from "react";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useHarnessEligibility } from "./useHarnessEligibility";

function wrapper({ children }: { children: ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return createElement(QueryClientProvider, { client: queryClient }, children);
}

describe("useHarnessEligibility", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("(a) fires when a sourceCategory is present on an activative-mode harness", async () => {
    (fetch as ReturnType<typeof vi.fn>).mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        definition_id: "def-1",
        harness_category: "carousels",
        source_category: "carousels",
        status: "ELIGIBLE",
        reason: null,
      }),
    });
    const { result } = renderHook(() => useHarnessEligibility("def-1", "carousels", "activative"), {
      wrapper,
    });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(fetch).toHaveBeenCalledTimes(1);
    expect((fetch as ReturnType<typeof vi.fn>).mock.calls[0][0]).toContain(
      "/api/harnesses/def-1/eligibility?source_category=carousels",
    );
  });

  it("(b) does not fire when a sourceCategory is present on a generic-mode harness", async () => {
    const { result } = renderHook(() => useHarnessEligibility("def-1", "carousels", "generic"), {
      wrapper,
    });
    expect(result.current.isPending).toBe(true);
    expect(result.current.fetchStatus).toBe("idle");
    expect(fetch).not.toHaveBeenCalled();
  });

  it("(c) does not fire when no sourceCategory is present at all", async () => {
    const { result } = renderHook(() => useHarnessEligibility("def-1", undefined, "activative"), {
      wrapper,
    });
    expect(result.current.isPending).toBe(true);
    expect(result.current.fetchStatus).toBe("idle");
    expect(fetch).not.toHaveBeenCalled();
  });
});
