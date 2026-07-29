// TS-APP-UI-003 - Action Registry
// Total over the exact nine strings controlTower.ts::availableActions() can emit

import type { LucideIcon } from "lucide-react";
import {
  FileSearch, ScrollText, Download, Clapperboard,
  Wand2, MousePointerSquareDashed, Columns2, TriangleAlert,
  Rocket, HelpCircle
} from "lucide-react";

export type AvailableAction =
  | "INSPECT_SOURCE" | "INSPECT_SEMANTIC_PROGRAM" | "EXPORT_AUDIT"
  | "OPEN_TIMELINE" | "REQUEST_REVISION" | "DIRECT_MANIPULATION"
  | "COMPARE_ARTIFACTS" | "RESOLVE_EXCEPTION" | "REQUEST_SHIP_DECISION";

export interface ActionContext {
  setTab: (tab: string) => void;
}

interface ActionEntry {
  label: string;
  icon: LucideIcon;
  implemented: boolean;
  onSelect?: (ctx: ActionContext) => void;
}

export const ACTION_REGISTRY: Record<AvailableAction, ActionEntry> = {
  INSPECT_SOURCE:          { label: "Inspect source",       icon: FileSearch,  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  INSPECT_SEMANTIC_PROGRAM:{ label: "Inspect script",       icon: ScrollText,  implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  EXPORT_AUDIT:            { label: "Export audit",         icon: Download,    implemented: false }, // needs SHIPPED — see Out of scope
  OPEN_TIMELINE:           { label: "Open timeline",        icon: Clapperboard,implemented: true,  onSelect: (ctx) => ctx.setTab("timeline") },
  REQUEST_REVISION:        { label: "Request revision",     icon: Wand2,       implemented: true,  onSelect: (ctx) => ctx.setTab("revise") },
  DIRECT_MANIPULATION:     { label: "Direct edit",          icon: MousePointerSquareDashed, implemented: false }, // Out of scope, Section 2
  COMPARE_ARTIFACTS:       { label: "Compare artifacts",    icon: Columns2,    implemented: true,  onSelect: (ctx) => ctx.setTab("overview") },
  RESOLVE_EXCEPTION:       { label: "Resolve exception",    icon: TriangleAlert, implemented: true, onSelect: (ctx) => ctx.setTab("exceptions") },
  REQUEST_SHIP_DECISION:   { label: "Request ship",         icon: Rocket,      implemented: false }, // Out of scope, Section 2
};

export function unknownActionEntry(code: string): ActionEntry {
  console.warn(`[control-tower] unrecognized available_action "${code}" — rendering as inert chip, not dropped`);
  return { label: code, icon: HelpCircle, implemented: false };
}
