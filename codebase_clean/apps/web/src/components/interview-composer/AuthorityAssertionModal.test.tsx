import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AuthorityAssertionModal } from "./AuthorityAssertionModal";

describe("AuthorityAssertionModal", () => {
  it("does not render when isOpen is false", () => {
    render(
      <AuthorityAssertionModal
        isOpen={false}
        onConfirm={vi.fn()}
        onCancel={vi.fn()}
      />
    );
    expect(screen.queryByTestId("authority-modal")).not.toBeInTheDocument();
  });

  it("renders when isOpen is true and submits valid authority attestation", () => {
    const handleConfirm = vi.fn();
    const handleCancel = vi.fn();

    render(
      <AuthorityAssertionModal
        isOpen={true}
        initialData={{
          operatorId: "op-audrey",
          authorityScope: "EDITORIAL_PRODUCER",
          assertionId: "assert-001",
        }}
        onConfirm={handleConfirm}
        onCancel={handleCancel}
      />
    );

    expect(screen.getByTestId("authority-modal")).toBeInTheDocument();
    expect(screen.getByTestId("operator-id-input")).toHaveValue("op-audrey");

    fireEvent.click(screen.getByTestId("authority-confirm-btn"));

    expect(handleConfirm).toHaveBeenCalledWith({
      operatorId: "op-audrey",
      authorityScope: "EDITORIAL_PRODUCER",
      assertionId: "assert-001",
    });
  });

  it("shows error if operatorId is cleared and submitted", () => {
    const handleConfirm = vi.fn();

    render(
      <AuthorityAssertionModal
        isOpen={true}
        initialData={{ operatorId: "op-dev" }}
        onConfirm={handleConfirm}
        onCancel={vi.fn()}
      />
    );

    const input = screen.getByTestId("operator-id-input");
    fireEvent.change(input, { target: { value: "" } });
    fireEvent.click(screen.getByTestId("authority-confirm-btn"));

    expect(handleConfirm).not.toHaveBeenCalled();
    expect(screen.getByTestId("authority-error")).toHaveTextContent("Operator ID is required");
  });
});
