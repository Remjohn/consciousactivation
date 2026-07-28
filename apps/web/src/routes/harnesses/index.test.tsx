import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { HarnessesIndexPage } from "./index";

describe("harnesses/index route", () => {
  it("renders the correct title and FR range", () => {
    render(<HarnessesIndexPage />);
    expect(screen.getByText("Harness Library")).toBeInTheDocument();
    expect(screen.getByText(/FR-APP-040\.\.041/)).toBeInTheDocument();
  });
});
