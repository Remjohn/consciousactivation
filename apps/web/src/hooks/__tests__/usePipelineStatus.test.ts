// TS-APP-UI-003 - usePipelineStatus hook tests
// AC-005: WS close code 4404 stops reconnection
// AC-007: run_state_changed triggers tower refetch

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { usePipelineStatus } from "../usePipelineStatus";

// Mock WebSocket
class MockWebSocket {
  static instances: MockWebSocket[] = [];
  onopen: ((evt: Event) => void) | null = null;
  onmessage: ((evt: MessageEvent) => void) | null = null;
  onclose: ((evt: CloseEvent) => void) | null = null;
  onerror: ((evt: Event) => void) | null = null;

  constructor(url: string) {
    MockWebSocket.instances.push(this);
  }

  close() {
    // Mock close
  }

  send(data: string) {
    // Mock send
  }

  // Helper to simulate events
  simulateOpen() {
    this.onopen?.(new Event("open"));
  }

  simulateMessage(data: unknown) {
    this.onmessage?.(new MessageEvent("message", { data: JSON.stringify(data) }));
  }

  simulateClose(code: number) {
    this.onclose?.(new CloseEvent("close", { code }));
  }
}

global.WebSocket = MockWebSocket as unknown as typeof WebSocket;

describe("usePipelineStatus", () => {
  beforeEach(() => {
    MockWebSocket.instances = [];
    vi.clearAllMocks();
  });

  afterEach(() => {
    MockWebSocket.instances = [];
  });

  it("should set connectionState to 'no_run' on close code 4404 (AC-005)", async () => {
    const onDirtyMock = vi.fn();

    const { result } = renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    // Wait for effect
    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateOpen();
      ws.simulateClose(4404);
    });

    expect(result.current.connectionState).toBe("no_run");
  });

  it("should not reconnect after 4404 close (AC-005)", async () => {
    const onDirtyMock = vi.fn();

    renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];
    act(() => {
      ws.simulateClose(4404);
    });

    // Should not create new WebSocket instance
    expect(MockWebSocket.instances).toHaveLength(1);
  });

  it("should set connectionState to 'multiple_runs' on close code 4409 (AC-005)", async () => {
    const onDirtyMock = vi.fn();

    const { result } = renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateClose(4409);
    });

    expect(result.current.connectionState).toBe("multiple_runs");
  });

  it("should call onDirty on run_state_changed message (AC-007)", async () => {
    const onDirtyMock = vi.fn();

    renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateMessage({
        type: "run_state_changed",
        run: { run_id: "run-123", state: "RUNNING" },
      });
    });

    expect(onDirtyMock).toHaveBeenCalledTimes(1);
  });

  it("should call onDirty on run_terminal message (AC-007)", async () => {
    const onDirtyMock = vi.fn();

    renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateMessage({
        type: "run_terminal",
        run: { run_id: "run-123", state: "SUCCEEDED" },
      });
    });

    expect(onDirtyMock).toHaveBeenCalledTimes(1);
  });

  it("should not call onDirty on node_state_changed message (AC-007)", async () => {
    const onDirtyMock = vi.fn();

    renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateMessage({
        type: "node_state_changed",
        node: { node_id: "node-001", state: "RUNNING" },
      });
    });

    expect(onDirtyMock).not.toHaveBeenCalled();
  });

  it("should update nodeVisual on snapshot message", async () => {
    const onDirtyMock = vi.fn();

    const { result } = renderHook(() =>
      usePipelineStatus("campaign-123", { onDirty: onDirtyMock })
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const ws = MockWebSocket.instances[0];

    act(() => {
      ws.simulateMessage({
        type: "snapshot",
        run: {
          nodes: [
            { node_id: "node-001", state: "RUNNING" },
            { node_id: "node-002", state: "SUCCEEDED" },
          ],
        },
      });
    });

    expect(result.current.nodeVisual.size).toBe(2);
    expect(result.current.nodeVisual.get("node-001")).toBe("active");
    expect(result.current.nodeVisual.get("node-002")).toBe("done");
  });
});
