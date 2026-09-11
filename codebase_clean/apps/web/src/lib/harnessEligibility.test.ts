import { describe, it, expect } from "vitest";
import { computeEligibilityPreview } from "./harnessEligibility";

describe("computeEligibilityPreview", () => {
  it("returns null when no sourceCategory is supplied, regardless of mode", () => {
    expect(computeEligibilityPreview({ mode: "generic", category_id: null }, undefined)).toBeNull();
    expect(
      computeEligibilityPreview({ mode: "activative", category_id: "carousels" }, undefined),
    ).toBeNull();
  });

  it("returns NOT_APPLICABLE for a generic-mode harness when a match would exist", () => {
    expect(computeEligibilityPreview({ mode: "generic", category_id: null }, "carousels")).toBe(
      "NOT_APPLICABLE",
    );
  });

  it("returns NOT_APPLICABLE for a generic-mode harness when no match would exist", () => {
    expect(
      computeEligibilityPreview({ mode: "generic", category_id: null }, "supervisuals"),
    ).toBe("NOT_APPLICABLE");
  });

  it("returns ELIGIBLE for an activative-mode harness whose category_id matches sourceCategory", () => {
    expect(
      computeEligibilityPreview({ mode: "activative", category_id: "carousels" }, "carousels"),
    ).toBe("ELIGIBLE");
  });

  it("returns INELIGIBLE for an activative-mode harness whose category_id does not match sourceCategory", () => {
    expect(
      computeEligibilityPreview({ mode: "activative", category_id: "carousels" }, "supervisuals"),
    ).toBe("INELIGIBLE");
  });

  it("returns INELIGIBLE for an activative-mode harness when sourceCategory is not a canonical id", () => {
    expect(
      computeEligibilityPreview({ mode: "activative", category_id: "carousels" }, "not_a_real_category"),
    ).toBe("INELIGIBLE");
  });

  it("returns INELIGIBLE for an activative-mode harness with a null category_id (malformed data)", () => {
    expect(
      computeEligibilityPreview({ mode: "activative", category_id: null }, "carousels"),
    ).toBe("INELIGIBLE");
  });
});
