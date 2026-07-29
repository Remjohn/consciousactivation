// TS-APP-UI-003 - ActionRail component
// Renders available_actions as affordance chips using actionRegistry.ts

import { Badge } from "../ui/Badge";
import {
  ACTION_REGISTRY,
  unknownActionEntry,
  type AvailableAction,
  type ActionContext,
} from "../../lib/actionRegistry";
import type { ControlTowerProjection } from "../../api/campaigns";

interface ActionRailProps {
  tower: ControlTowerProjection;
  actionContext: ActionContext;
}

export function ActionRail({ tower, actionContext }: ActionRailProps) {
  const actions = tower.available_actions ?? [];

  return (
    <div className="control-tower-card">
      <div className="control-tower-card-header">
        <span>Actions</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {actions.map((actionCode) => {
          const entry = isKnownAction(actionCode)
            ? ACTION_REGISTRY[actionCode]
            : unknownActionEntry(actionCode);

          return (
            <button
              key={actionCode}
              onClick={() => entry.onSelect?.(actionContext)}
              disabled={!entry.implemented}
              className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-sm font-medium transition-colors ${
                entry.implemented
                  ? "bg-ca-gold-500 text-white hover:bg-ca-gold-600"
                  : "cursor-not-allowed bg-ca-surface-raised text-ca-text-tertiary"
              }`}
              title={entry.implemented ? undefined : "Coming soon"}
            >
              <entry.icon className="h-4 w-4" />
              {entry.label}
            </button>
          );
        })}
        {actions.length === 0 && (
          <p className="text-sm text-ca-text-tertiary">No actions available</p>
        )}
      </div>
    </div>
  );
}

function isKnownAction(code: string): code is AvailableAction {
  return code in ACTION_REGISTRY;
}
