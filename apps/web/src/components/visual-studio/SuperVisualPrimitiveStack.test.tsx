import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { SuperVisualPrimitiveStack } from "./SuperVisualPrimitiveStack";

describe("SuperVisualPrimitiveStack", () => {
  it("exposes the four distinct primitive responsibilities without implying canonical mutation", () => {
    render(
      <SuperVisualPrimitiveStack
        layers={[{ layer_id: "layer:1", bbox: { x: 0, y: 0, width: 100, height: 100 }, text: "claim", annotations: [] }]}
        rendererKind="SKIA_STATIC_RENDERER"
      />,
    );

    expect(screen.getByTestId("primitive-BBOX")).toHaveTextContent("authoritative spatial bounds");
    expect(screen.getByTestId("primitive-PRETEXT")).toHaveTextContent("measurement and deterministic text wrapping");
    expect(screen.getByTestId("primitive-SKIA")).toHaveTextContent("display-list/raster substrate");
    expect(screen.getByTestId("primitive-ROUGH_NOTATION")).toHaveTextContent("NOT_PRESENT");
    expect(screen.getByText(/operator approval is required/i)).toBeInTheDocument();
  });

  it("does not imply a geometry primitive is present when no authoritative bbox exists", () => {
    render(
      <SuperVisualPrimitiveStack
        layers={[{ layer_id: "layer:1", source_ref: { object_id: "source:1" }, text: "claim", annotations: [] }]}
        rendererKind="SKIA_STATIC_RENDERER"
      />,
    );
    expect(screen.getByTestId("primitive-BBOX")).toHaveTextContent("NOT_PRESENT");
  });
});
