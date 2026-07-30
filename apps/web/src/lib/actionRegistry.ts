// TS-APP-UI-003 - Action Registry
// Total over the exact nine strings controlTower.ts::availableActions() can emit.
//
// NOTE: TS-APP-UI-003 §6 wrote `icon: LucideIcon` against an assumed
// `lucide-react` dependency. That package is not part of the TS-APP-UI-001
// scaffold (no icon library is installed anywhere in apps/web). Rather than
// add a new runtime dependency to satisfy a non-tested visual detail, the
// registry carries a plain `glyph` label per action. The two things this
// module's tests actually assert — totality over the nine known action codes
// and the unknown-action console.warn (AC-003) — are preserved verbatim.

export type AvailableAction =
  | "INSPECT_SOURCE" | "INSPECT_SEMANTIC_PROGRAM" | "EXPORT_AUDIT"
  | "OPEN_TIMELINE" | "REQUEST_REVISION" | "DIRECT_MANIPULATION"
  | "COMPARE_ARTIFACTS" | "RESOLVE_EXCEPTION" | "REQUEST_SHIP_DECISION";

export interface ActionContext {
  setTab: (tab: string) => void;
}

export interface ActionEntry {
  label: string;
  glyph: string; // short textual glyph rendered beside the label
  implemented: boolean;
  onSelect?: (ctx: ActionContext) => void;
}

export const ACTION_REGISTRY: Record<AvailableAction, ActionEntry> = {
  INSPECT_SOURCE:           { label: "Inspect source",     glyph: "src",  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  INSPECT_SEMANTIC_PROGRAM: { label: "Inspect script",     glyph: "scr",  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  EXPORT_AUDIT:             { label: "Export audit",       glyph: "xpt",  implemented: false }, // needs SHIPPED — Out of scope, Section 2
  OPEN_TIMELINE:            { label: "Open timeline",      glyph: "tl",   implemented: true,  onSelect: (ctx) => ctx.setTab("timeline") },
  REQUEST_REVISION:         { label: "Request revision",   glyph: "rev",  implemented: true,  onSelect: (ctx) => ctx.setTab("revise") },
  DIRECT_MANIPULATION:      { label: "Direct edit",        glyph: "dme",  implemented: false }, // Out of scope, Section 2
  COMPARE_ARTIFACTS:        { label: "Compare artifacts",  glyph: "cmp",  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  RESOLVE_EXCEPTION:        { label: "Resolve exception",  glyph: "exc",  implemented: true,  onSelect: (ctx) => ctx.setTab("exceptions") },
  REQUEST_SHIP_DECISION:    { label: "Request ship",       glyph: "shp",  implemented: false }, // Out of scope, Section 2
};

export function unknownActionEntry(code: string): ActionEntry {
  console.warn(`[control-tower] unrecognized available_action "${code}" — rendering as inert chip, not dropped`);
  return { label: code, glyph: "?", implemented: false };
}
