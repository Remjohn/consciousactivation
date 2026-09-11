// TS-APP-UI-003 - RunProgressGauge tests
// AC-001: Control Tower renders a running campaign's full projection
// AC-013: Run progress gauge matches node counts exactly, including zero-node edge case

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { RunProgressGauge } from "../RunProgressGauge";

describe("RunProgressGauge", () => {
  it("should show 67% when 2 out of 3 nodes succeeded (AC-001)", () => {
    const runNodes = [
      { status: "SUCCEEDED" },
      { status: "SUCCEEDED" },
      { status: "RUNNING" },
    ];

    render(<RunProgressGauge runNodes={runNodes} />);

    expect(screen.getByText("67%")).toBeInTheDocument();
    expect(screen.getByText("2 / 3 nodes succeeded")).toBeInTheDocument();
  });

  it("should show '—' when no nodes exist (AC-013)", () => {
    render(<RunProgressGauge runNodes={[]} />);

    expect(screen.getByText("—")).toBeInTheDocument();
    expect(screen.getByText("No production nodes yet")).toBeInTheDocument();
  });

  it("should not show NaN% for empty nodes", () => {
    render(<RunProgressGauge runNodes={[]} />);

    expect(screen.queryByText("NaN%")).not.toBeInTheDocument();
  });

  it("should show running node count", () => {
    const runNodes = [
      { status: "SUCCEEDED" },
      { status: "RUNNING" },
      { status: "RUNNING" },
    ];

    render(<RunProgressGauge runNodes={runNodes} />);

    expect(screen.getByText("2 running")).toBeInTheDocument();
  });

  it("should show blocked node count", () => {
    const runNodes = [
      { status: "SUCCEEDED" },
      { status: "BLOCKED" },
    ];

    render(<RunProgressGauge runNodes={runNodes} />);

    expect(screen.getByText("1 blocked")).toBeInTheDocument();
  });
});
