import { actionLabel } from "../../lib/supervisualViewModel";

export function SuperVisualActionBar({ actions = [], status, onRunAction, activeAction }) {
  return (
    <div className="sv-action-bar">
      {actions.length ? (
        actions.map((action) => (
          <button
            key={action}
            className="sv-button"
            disabled={Boolean(activeAction)}
            onClick={() => onRunAction?.(action)}
          >
            {activeAction === action ? "Running..." : actionLabel(action)}
          </button>
        ))
      ) : (
        <button className="sv-button" disabled>
          No runtime actions for {String(status || "current state").replaceAll("_", " ")}
        </button>
      )}
    </div>
  );
}
