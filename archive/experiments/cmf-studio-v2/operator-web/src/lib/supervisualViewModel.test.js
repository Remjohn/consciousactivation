import { describe, expect, it } from "vitest";
import { buildSuperVisualViewModel } from "./supervisualViewModel";

describe("buildSuperVisualViewModel", () => {
  it("builds status rail and actions from snapshot", () => {
    const viewModel = buildSuperVisualViewModel({
      projectDetail: {
        project: { title: "Runtime Project", status: "active" },
        current_variant: { variant_label: "A", status: "composition_options_ready" },
      },
      snapshot: {
        status: "composition_options_ready",
        step: "composition_hypotheses",
        available_actions: ["composition.lock"],
        blockers: [],
        display_payload: {},
      },
      events: [],
    });

    expect(viewModel.projectTitle).toBe("Runtime Project");
    expect(viewModel.status).toBe("composition_options_ready");
    expect(viewModel.availableActions).toEqual(["composition.lock"]);
    expect(viewModel.statusRail.some((item) => item.state === "active")).toBe(true);
  });
});
