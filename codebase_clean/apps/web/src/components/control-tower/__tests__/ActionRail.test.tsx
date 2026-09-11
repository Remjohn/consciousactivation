// TS-APP-UI-003 - ActionRail tests
// AC-002: Available actions render exactly the affordances the projection allows
// AC-003: Unrecognized available action is never dropped

import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { ActionRail } from "../ActionRail";
import { unknownActionEntry } from "../../lib/actionRegistry";

// Mock tower data
const createMockTower = (available_actions: string[]) => ({
  available_actions,
});

describe("ActionRail", () => {
  it("should render exactly 3 chips when 3 actions provided (AC-002)", () => {
    const tower = createMockTower(["INSPECT_SOURCE", "EXPORT_AUDIT", "REQUEST_SHIP_DECISION"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: vi.fn() }}
      />
    );

    // Should have exactly 3 buttons
    const buttons = screen.getAllByRole("button");
    expect(buttons).toHaveLength(3);
  });

  it("should not render 'Request revision' when not in available_actions (AC-002)", () => {
    const tower = createMockTower(["INSPECT_SOURCE", "EXPORT_AUDIT"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: vi.fn() }}
      />
    );

    expect(screen.queryByText("Request revision")).not.toBeInTheDocument();
  });

  it("should not render 'Open timeline' when not in available_actions (AC-002)", () => {
    const tower = createMockTower(["INSPECT_SOURCE"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: vi.fn() }}
      />
    );

    expect(screen.queryByText("Open timeline")).not.toBeInTheDocument();
  });

  it("should render 'Request ship' as disabled (AC-002)", () => {
    const tower = createMockTower(["REQUEST_SHIP_DECISION"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: vi.fn() }}
      />
    );

    const button = screen.getByText("Request ship");
    expect(button).toBeDisabled();
  });

  it("should render unknown action as disabled chip (AC-003)", () => {
    const consoleSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    const tower = createMockTower(["FUTURE_ACTION"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: vi.fn() }}
      />
    );

    // Should render the unknown action
    expect(screen.getByText("FUTURE_ACTION")).toBeInTheDocument();

    // Should be disabled
    const button = screen.getByText("FUTURE_ACTION");
    expect(button).toBeDisabled();

    // Should have called console.warn
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining("FUTURE_ACTION")
    );

    consoleSpy.mockRestore();
  });

  it("should call setTab when implemented action is clicked", () => {
    const setTabMock = vi.fn();
    const tower = createMockTower(["OPEN_TIMELINE"]);

    render(
      <ActionRail
        tower={tower}
        actionContext={{ setTab: setTabMock }}
      />
    );

    const button = screen.getByText("Open timeline");
    button.click();

    expect(setTabMock).toHaveBeenCalledWith("timeline");
  });
});
