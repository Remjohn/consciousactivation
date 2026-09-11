// TS-APP-UI-003 - ExceptionQueue tests
// AC-011: Exception resolve only offers allowed decisions

import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { ExceptionQueue } from "../ExceptionQueue";

// Mock exception packages
const mockPackages = [
  {
    package_id: "exc-001",
    summary: "Video render failed",
    responsible_product: "video-processor",
    evidence_refs: ["ref-001", "ref-002"],
    allowed_decisions: ["REJECT"], // Only REJECT allowed, not REQUEST_REVISION
  },
  {
    package_id: "exc-002",
    summary: "Text too long",
    responsible_product: "text-analyzer",
    evidence_refs: ["ref-003"],
    allowed_decisions: ["REQUEST_REVISION", "REJECT"], // Both allowed
  },
];

describe("ExceptionQueue", () => {
  let resolveMutationMock: any;

  beforeEach(() => {
    resolveMutationMock = {
      mutate: vi.fn(),
      isPending: false,
      error: null,
      data: null,
    };
  });

  it("should only show Reject button when allowed_decisions is ['REJECT'] (AC-011)", () => {
    const packages = [mockPackages[0]]; // Only REJECT allowed

    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={packages}
        resolveMutation={resolveMutationMock}
      />
    );

    // Should have Reject button
    expect(screen.getByText("Reject")).toBeInTheDocument();

    // Should NOT have Request Revision button
    expect(screen.queryByText("Request Revision")).not.toBeInTheDocument();
  });

  it("should show both buttons when both decisions allowed (AC-011)", () => {
    const packages = [mockPackages[1]]; // Both allowed

    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={packages}
        resolveMutation={resolveMutationMock}
      />
    );

    expect(screen.getByText("Request Revision")).toBeInTheDocument();
    expect(screen.getByText("Reject")).toBeInTheDocument();
  });

  it("should call resolve mutation with REJECT decision", () => {
    const packages = [mockPackages[0]];

    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={packages}
        resolveMutation={resolveMutationMock}
      />
    );

    const rejectButton = screen.getByText("Reject");
    fireEvent.click(rejectButton);

    expect(resolveMutationMock.mutate).toHaveBeenCalledWith({
      packageId: "exc-001",
      decision: "REJECT",
    });
  });

  it("should show 'No open exceptions' when packages is empty", () => {
    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={[]}
        resolveMutation={resolveMutationMock}
      />
    );

    expect(screen.getByText("No open exceptions")).toBeInTheDocument();
  });

  it("should display evidence refs as monospace chips", () => {
    const packages = [mockPackages[0]];

    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={packages}
        resolveMutation={resolveMutationMock}
      />
    );

    expect(screen.getByText("ref-001")).toBeInTheDocument();
    expect(screen.getByText("ref-002")).toBeInTheDocument();
  });

  it("should show exception count badge", () => {
    render(
      <ExceptionQueue
        campaignId="campaign-123"
        packages={mockPackages}
        resolveMutation={resolveMutationMock}
      />
    );

    // Should show badge with count "2"
    expect(screen.getByText("2")).toBeInTheDocument();
  });
});
