import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ResearchPackageInspector } from "./ResearchPackageInspector";
import type { GuestResearchPackageResponse } from "../../api/types";

describe("ResearchPackageInspector", () => {
  const mockPackage: GuestResearchPackageResponse = {
    research_package_id: "pkg-123456",
    revision: 1,
    guest_name: "Audrey Hepburn",
    source_urls: ["https://example.com/bio"],
    uploaded_documents: [
      {
        asset_id: "ast-001",
        original_filename: "bio.pdf",
        bytes: 102400,
        media_type: "application/pdf",
        sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        context_class: "IDENTITY_DNA",
      },
      {
        asset_id: "ast-002",
        original_filename: "recording.mp4",
        bytes: 104857600,
        media_type: "video/mp4",
        sha256: "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
        context_class: "INTERVIEW_RECORDING",
      },
      {
        asset_id: "ast-003",
        original_filename: "transcript.vtt",
        bytes: 2048,
        media_type: "text/vtt",
        sha256: "aabbccddeeff00112233445566778899aabbccddeeff00112233445566778899",
        context_class: "CAPTION_TRACK",
        caption_for: "recording.mp4",
      },
    ],
    idempotent_replay: false,
  };

  it("renders package metadata and grouped asset library", () => {
    render(
      <ResearchPackageInspector
        pkg={mockPackage}
        workspaceId="ws-dev"
        onProceedToBrief={vi.fn()}
      />
    );

    expect(screen.getByTestId("inspector-package-id")).toHaveTextContent("pkg-123456");
    expect(screen.getByTestId("inspector-guest-name")).toHaveTextContent("Audrey Hepburn");

    // Group sections
    expect(screen.getByTestId("inspector-group-IDENTITY_DNA")).toBeInTheDocument();
    expect(screen.getByTestId("inspector-group-INTERVIEW_RECORDING")).toBeInTheDocument();
    expect(screen.getByTestId("inspector-group-CAPTION_TRACK")).toBeInTheDocument();
    expect(screen.getByTestId("inspector-group-EVIDENCE_SOURCE")).toBeInTheDocument();

    // Check filenames and hashes
    expect(screen.getByText("bio.pdf")).toBeInTheDocument();
    expect(screen.getByText("recording.mp4")).toBeInTheDocument();
    expect(screen.getByText("transcript.vtt")).toBeInTheDocument();
    expect(screen.getByText("Captions: recording.mp4")).toBeInTheDocument();
  });

  it("filters displayed groups by context class filter chip", () => {
    render(
      <ResearchPackageInspector
        pkg={mockPackage}
        workspaceId="ws-dev"
        onProceedToBrief={vi.fn()}
      />
    );

    const identityFilter = screen.getByTestId("inspector-filter-IDENTITY_DNA");
    fireEvent.click(identityFilter);

    expect(screen.getByTestId("inspector-group-IDENTITY_DNA")).toBeInTheDocument();
    expect(screen.queryByTestId("inspector-group-INTERVIEW_RECORDING")).not.toBeInTheDocument();
  });

  it("calls onProceedToBrief when proceed button clicked", () => {
    const handleProceed = vi.fn();
    render(
      <ResearchPackageInspector
        pkg={mockPackage}
        workspaceId="ws-dev"
        onProceedToBrief={handleProceed}
      />
    );

    const proceedBtn = screen.getByTestId("proceed-to-brief-btn");
    fireEvent.click(proceedBtn);

    expect(handleProceed).toHaveBeenCalledTimes(1);
  });
});
