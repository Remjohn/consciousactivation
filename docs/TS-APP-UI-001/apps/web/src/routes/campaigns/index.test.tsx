import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { CampaignsIndexPage } from "./index";

describe("campaigns/index route", () => {
  it("renders the correct title and FR range", () => {
    render(<CampaignsIndexPage />);
    expect(screen.getByText("Campaigns")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-050/)).toBeInTheDocument();
  });
});
