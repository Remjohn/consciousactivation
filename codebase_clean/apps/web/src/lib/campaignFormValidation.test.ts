import { describe, it, expect } from "vitest";
import {
  requireNonEmpty,
  requirePositiveInteger,
  requireAtLeastOneOutputTarget,
  isFormat02Deferred,
} from "./campaignFormValidation";

describe("campaignFormValidation", () => {
  describe("requireNonEmpty", () => {
    it("returns null for non-empty string", () => {
      expect(requireNonEmpty("hello", "Field")).toBeNull();
    });

    it("returns EMPTY_VALUE for empty string", () => {
      const result = requireNonEmpty("", "Field");
      expect(result?.code).toBe("EMPTY_VALUE");
      expect(result?.message).toBe("Field must not be empty");
    });

    it("returns EMPTY_VALUE for whitespace-only string", () => {
      const result = requireNonEmpty("   ", "Field");
      expect(result?.code).toBe("EMPTY_VALUE");
    });
  });

  describe("requirePositiveInteger", () => {
    it("returns null for positive integer", () => {
      expect(requirePositiveInteger(5, "Count")).toBeNull();
    });

    it("returns INVALID_INTEGER for zero", () => {
      const result = requirePositiveInteger(0, "Count");
      expect(result?.code).toBe("INVALID_INTEGER");
    });

    it("returns INVALID_INTEGER for negative number", () => {
      const result = requirePositiveInteger(-1, "Count");
      expect(result?.code).toBe("INVALID_INTEGER");
    });

    it("returns INVALID_INTEGER for float", () => {
      const result = requirePositiveInteger(1.5, "Count");
      expect(result?.code).toBe("INVALID_INTEGER");
    });
  });

  describe("requireAtLeastOneOutputTarget", () => {
    it("returns null when count >= 1", () => {
      expect(requireAtLeastOneOutputTarget(1)).toBeNull();
      expect(requireAtLeastOneOutputTarget(3)).toBeNull();
    });

    it("returns OUTPUT_TARGET_REQUIRED when count is 0", () => {
      const result = requireAtLeastOneOutputTarget(0);
      expect(result?.code).toBe("OUTPUT_TARGET_REQUIRED");
      expect(result?.message).toBe("At least one output target is required");
    });
  });

  describe("isFormat02Deferred", () => {
    it("returns true for 2d_character_animation category", () => {
      expect(isFormat02Deferred("2d_character_animation", "")).toBe(true);
    });

    it("returns true for format02_ profile ID", () => {
      expect(isFormat02Deferred("", "format02_video")).toBe(true);
    });

    it("returns false for other categories and profiles", () => {
      expect(isFormat02Deferred("short_form_edited_video", "format01_video")).toBe(false);
    });
  });
});
