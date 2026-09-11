import { LIFECYCLE_TOKENS } from "../../lib/statusTokens";
import type { CampaignLifecycleState } from "../../api/types";

const ICON_SVG: Record<string, JSX.Element> = {
  "circle-dashed": (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <circle cx={12} cy={12} r={10} strokeDasharray="4 4" />
    </svg>
  ),
  rocket: (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M4.5 16.5L3 21l4.5-1.5M8.5 8.5L21 3l-5.5 12.5M8.5 8.5L12 12" />
    </svg>
  ),
  loader: (
    <svg className="h-3 w-3 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
    </svg>
  ),
  pause: (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <rect x={6} y={4} width={4} height={16} /><rect x={14} y={4} width={4} height={16} />
    </svg>
  ),
  flag: (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" /><line x1={4} y1={22} x2={4} y2={15} />
    </svg>
  ),
  check: (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <polyline points="20 6 9 17 4 12" />
    </svg>
  ),
  "check-check": (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <polyline points="20 6 9 17 4 12" /><polyline points="16 6 5 17" />
    </svg>
  ),
  x: (
    <svg className="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
      <line x1={18} y1={6} x2={6} y2={18} /><line x1={6} y1={6} x2={18} y2={18} />
    </svg>
  ),
};

export function LifecycleBadge({ state }: { state: CampaignLifecycleState }) {
  const token = LIFECYCLE_TOKENS[state];
  const icon = ICON_SVG[token.icon];

  if (token.filled) {
    return (
      <span
        className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold tracking-wide uppercase bg-${token.color} text-canvas`}
      >
        {icon}
        {state.replace(/_/g, " ")}
      </span>
    );
  }

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-semibold tracking-wide uppercase border-${token.color} text-${token.color}`}
    >
      {icon}
      {state.replace(/_/g, " ")}
    </span>
  );
}
