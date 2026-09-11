import { Badge } from "../ui/Badge";
import type { HarnessMode } from "../../api/types";

export function ModeBadge({ mode }: { readonly mode: HarnessMode }) {
  return (
    <Badge tone={mode === "activative" ? "accent" : "muted"}>
      {mode === "activative" ? "Activative" : "Generic"}
    </Badge>
  );
}
