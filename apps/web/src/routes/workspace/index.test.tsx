import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { WorkspaceIndexPage } from "./index";

describe("workspace/index route", () => {
  it("renders the correct title and FR range", () => {
    render(<WorkspaceIndexPage />);
    expect(screen.getByText("Workspace")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-001\.\.003/)).toBeInTheDocument();
  });
});
