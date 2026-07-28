import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { CampaignsNewPage } from "./new";

describe("campaigns/new route", () => {
  it("renders the correct title and FR range", () => {
    render(<CampaignsNewPage />);
    expect(screen.getByText("New Campaign")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-050/)).toBeInTheDocument();
  });
});
