import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { CampaignDetailPage } from "./$campaignId";

describe("campaigns/$campaignId route", () => {
  it("renders the correct title and FR range", () => {
    render(<CampaignDetailPage />);
    expect(screen.getByText("Control Tower")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-060\.\.064/)).toBeInTheDocument();
  });
});
