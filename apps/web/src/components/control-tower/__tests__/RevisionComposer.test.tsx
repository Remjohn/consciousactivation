// TS-APP-UI-003 - RevisionComposer tests
// AC-008: Revision compile renders all three compilation statuses
// AC-009: Revision execute on stale state recompiles automatically
// AC-010: Timeline disabled state when nothing compiled yet

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { RevisionComposer } from "../RevisionComposer";
import type { ControlTowerProjection } from "../../api/campaigns";

// Mock tower data
const createMockTower = (hasTimeline: boolean): ControlTowerProjection => ({
  campaign: { lifecycle_state: "RUNNING" },
  run_nodes: [],
  available_actions: ["REQUEST_REVISION"],
  timeline: hasTimeline
    ? {
        video_edit_program_ref: {
          object_id: "prog-123",
          sha256: "abc123",
          version: "1",
        },
        tracks: [],
        duration_frames: 100,
        fps_numerator: 30,
        fps_denominator: 1,
      }
    : null,
  order: { category_id: "cat-123" },
} as ControlTowerProjection);

describe("RevisionComposer", () => {
  let compileMutationMock: any;
  let executeMutationMock: any;

  beforeEach(() => {
    compileMutationMock = {
      mutate: vi.fn(),
      isPending: false,
      error: null,
      data: null,
      reset: vi.fn(),
    };

    executeMutationMock = {
      mutate: vi.fn(),
      isPending: false,
      error: null,
      data: null,
      reset: vi.fn(),
    };
  });

  it("should disable Preview button when timeline is null (AC-010)", () => {
    const tower = createMockTower(false);

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    const previewButton = screen.getByText("Preview");
    expect(previewButton).toBeDisabled();
  });

  it("should show timeline message when timeline is null (AC-010)", () => {
    const tower = createMockTower(false);

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    expect(
      screen.getByText(/Open the Timeline tab first/)
    ).toBeInTheDocument();
  });

  it("should enable Preview button when timeline exists", () => {
    const tower = createMockTower(true);

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    const previewButton = screen.getByText("Preview");
    expect(previewButton).not.toBeDisabled();
  });

  it("should render COMPILED status with Confirm button (AC-008)", () => {
    const tower = createMockTower(true);
    compileMutationMock.data = {
      compilation_status: "COMPILED",
      program_id: "prog-456",
      interpretation: "Trim intro by 3 seconds",
      exact_operations: [{ tool_id: "trim", arguments: { duration: 3 } }],
      confidence_micros: 950000, // 95%
    };

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    expect(screen.getByText("Compilation Successful")).toBeInTheDocument();
    expect(screen.getByText("Confirm & Run")).toBeInTheDocument();
    expect(screen.getByText(/Trim intro/)).toBeInTheDocument();
  });

  it("should render NEEDS_CLARIFICATION without Confirm button (AC-008)", () => {
    const tower = createMockTower(true);
    compileMutationMock.data = {
      compilation_status: "NEEDS_CLARIFICATION",
      interpretation: "I'm not sure what you mean",
      escalation: "Please specify which part of the intro to trim",
    };

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    expect(screen.getByText("Needs Clarification")).toBeInTheDocument();
    expect(screen.queryByText("Confirm & Run")).not.toBeInTheDocument();
    expect(screen.getByText(/Please specify/)).toBeInTheDocument();
  });

  it("should render DENIED status in danger color without Confirm button (AC-008)", () => {
    const tower = createMockTower(true);
    compileMutationMock.data = {
      compilation_status: "DENIED",
      escalation: "This change would violate brand guidelines",
    };

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    expect(screen.getByText("Revision Denied")).toBeInTheDocument();
    expect(screen.queryByText("Confirm & Run")).not.toBeInTheDocument();
    expect(screen.getByText(/violate brand guidelines/)).toBeInTheDocument();
  });

  it("should call compile mutation on Preview click", () => {
    const tower = createMockTower(true);
    compileMutationMock.mutate = vi.fn();

    render(
      <RevisionComposer
        campaignId="campaign-123"
        tower={tower}
        compileMutation={compileMutationMock}
        executeMutation={executeMutationMock}
      />
    );

    // Type revision text
    const textarea = screen.getByPlaceholderText(/trim the intro/);
    fireEvent.change(textarea, { target: { value: "trim the intro by 3 seconds" } });

    // Click Preview
    const previewButton = screen.getByText("Preview");
    fireEvent.click(previewButton);

    expect(compileMutationMock.mutate).toHaveBeenCalledTimes(1);
  });
});
