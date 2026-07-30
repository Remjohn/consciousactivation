// TS-APP-UI-003 - actionRegistry.ts tests
// AC-003: Unrecognized available action is never dropped

import { describe, it, expect, vi, beforeEach } from "vitest";
import { ACTION_REGISTRY, unknownActionEntry, type AvailableAction } from "../actionRegistry";

describe("actionRegistry", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should have entries for all known actions", () => {
    const knownActions: AvailableAction[] = [
      "INSPECT_SOURCE", "INSPECT_SEMANTIC_PROGRAM", "EXPORT_AUDIT",
      "OPEN_TIMELINE", "REQUEST_REVISION", "DIRECT_MANIPULATION",
      "COMPARE_ARTIFACTS", "RESOLVE_EXCEPTION", "REQUEST_SHIP_DECISION"
    ];

    knownActions.forEach((action) => {
      expect(ACTION_REGISTRY[action]).toBeDefined();
      expect(ACTION_REGISTRY[action].label).toBeTruthy();
      expect(ACTION_REGISTRY[action].glyph).toBeTruthy();
    });
  });

  it("should mark EXPORT_AUDIT as not implemented", () => {
    expect(ACTION_REGISTRY.EXPORT_AUDIT.implemented).toBe(false);
  });

  it("should mark DIRECT_MANIPULATION as not implemented", () => {
    expect(ACTION_REGISTRY.DIRECT_MANIPULATION.implemented).toBe(false);
  });

  it("should mark REQUEST_SHIP_DECISION as not implemented", () => {
    expect(ACTION_REGISTRY.REQUEST_SHIP_DECISION.implemented).toBe(false);
  });

  it("should have onSelect handlers for implemented actions", () => {
    expect(ACTION_REGISTRY.INSPECT_SOURCE.onSelect).toBeDefined();
    expect(ACTION_REGISTRY.OPEN_TIMELINE.onSelect).toBeDefined();
    expect(ACTION_REGISTRY.REQUEST_REVISION.onSelect).toBeDefined();
  });
});

describe("unknownActionEntry", () => {
  it("should return an entry with the raw code as label", () => {
    const entry = unknownActionEntry("FUTURE_ACTION");
    expect(entry.label).toBe("FUTURE_ACTION");
  });

  it("should mark unknown actions as not implemented", () => {
    const entry = unknownActionEntry("FUTURE_ACTION");
    expect(entry.implemented).toBe(false);
  });

  it("should call console.warn with the action code (AC-003)", () => {
    const consoleSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    unknownActionEntry("FUTURE_ACTION");
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining("FUTURE_ACTION")
    );
    consoleSpy.mockRestore();
  });

  it("should use a fallback glyph for unknown actions", () => {
    const entry = unknownActionEntry("FUTURE_ACTION");
    expect(entry.glyph).toBeDefined();
  });
});
