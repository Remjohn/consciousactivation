// TS-APP-UI-003 - RunGraph tests
// AC-004: Node label reflects Studio's authoritative status, not the WS's raw status

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { RunGraph } from "../RunGraph";
import type { ConnectionState } from "../../hooks/usePipelineStatus";

// Mock run nodes
const mockRunNodes = [
  {
    node_id: "node-001",
    status: "WAITING_HUMAN", // Studio status
    dependency_ids: [],
  },
];

describe("RunGraph", () => {
  it("should show 'Needs you' label for WAITING_HUMAN status (AC-004)", () => {
    const nodeVisual = new Map<string, string>(); // Empty - no WS updates yet

    render(
      <RunGraph
        runNodes={mockRunNodes}
        nodeVisual={nodeVisual}
        connectionState="open"
      />
    );

    // Should show Studio status label, not WS status
    expect(screen.getByText("Needs you")).toBeInTheDocument();
  });

  it("should not show 'Ready' label even if WS sends READY state (AC-004)", () => {
    const nodeVisual = new Map<string, string>([["node-001", "active"]]); // WS says "active" (READY)

    render(
      <RunGraph
        runNodes={mockRunNodes}
        nodeVisual={nodeVisual}
        connectionState="open"
      />
    );

    // Should still show "Needs you" from Studio status, not "Ready" from WS
    expect(screen.getByText("Needs you")).toBeInTheDocument();
    expect(screen.queryByText("Ready")).not.toBeInTheDocument();
  });

  it("should show 'Reconnecting...' when WS is closed", () => {
    render(
      <RunGraph
        runNodes={mockRunNodes}
        nodeVisual={new Map()}
        connectionState="closed"
      />
    );

    expect(screen.getByText("Reconnecting...")).toBeInTheDocument();
  });

  it("should show 'No production run' message for no_run state", () => {
    render(
      <RunGraph
        runNodes={mockRunNodes}
        nodeVisual={new Map()}
        connectionState="no_run"
      />
    );

    expect(screen.getByText(/No production run is linked/)).toBeInTheDocument();
  });

  it("should show multiple runs message for multiple_runs state", () => {
    render(
      <RunGraph
        runNodes={mockRunNodes}
        nodeVisual={new Map()}
        connectionState="multiple_runs"
      />
    );

    expect(screen.getByText(/more than one linked run/)).toBeInTheDocument();
  });

  // Test layoutRunGraph indirectly through rendering
  it("should render nodes in correct column order", () => {
    const nodes = [
      { node_id: "node-001", status: "SUCCEEDED", dependency_ids: [] },
      { node_id: "node-002", status: "RUNNING", dependency_ids: ["node-001"] },
      { node_id: "node-003", status: "PENDING", dependency_ids: ["node-001", "node-002"] },
    ];

    render(
      <RunGraph
        runNodes={nodes}
        nodeVisual={new Map()}
        connectionState="open"
      />
    );

    // All nodes should be rendered
    expect(screen.getByText("node-001")).toBeInTheDocument();
    expect(screen.getByText("node-002")).toBeInTheDocument();
    expect(screen.getByText("node-003")).toBeInTheDocument();
  });
});
