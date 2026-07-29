// TS-APP-UI-003 - RunProgressGauge component
// Hero radial gauge showing run progress (SUCCEEDED / total nodes)

import { useMemo } from "react";

interface RunProgressGaugeProps {
  runNodes: Array<{ status: string }>;
}

export function RunProgressGauge({ runNodes }: RunProgressGaugeProps) {
  const { succeededCount, totalCount, percentage, displayText } = useMemo(() => {
    const total = runNodes.length;
    const succeeded = runNodes.filter((n) => n.status === "SUCCEEDED").length;
    const pct = total > 0 ? Math.round((succeeded / total) * 100) : null;

    return {
      succeededCount: succeeded,
      totalCount: total,
      percentage: pct,
      displayText: pct !== null ? `${pct}%` : "—",
    };
  }, [runNodes]);

  // SVG circle calculations
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = percentage !== null
    ? circumference - (percentage / 100) * circumference
    : circumference; // Full circle for "no data"

  return (
    <div className="control-tower-card flex items-center gap-6">
      {/* Radial gauge */}
      <div className="relative h-32 w-32">
        <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
          {/* Background circle */}
          <circle
            cx="60"
            cy="60"
            r={radius}
            fill="none"
            stroke="var(--ca-idle)"
            strokeWidth="8"
          />
          {/* Progress circle */}
          {percentage !== null && (
            <circle
              cx="60"
              cy="60"
              r={radius}
              fill="none"
              stroke="var(--ca-gold-500)"
              strokeWidth="8"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className="transition-all duration-500"
            />
          )}
        </svg>
        {/* Centered percentage */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-3xl font-bold text-ca-text-primary">
            {displayText}
          </span>
        </div>
      </div>

      {/* Stats text */}
      <div>
        <h2 className="text-xl font-semibold text-ca-text-primary">Run Progress</h2>
        {totalCount > 0 ? (
          <p className="mt-1 text-sm text-ca-text-secondary">
            {succeededCount} / {totalCount} nodes succeeded
          </p>
        ) : (
          <p className="mt-1 text-sm text-ca-text-tertiary">
            No production nodes yet
          </p>
        )}
        {runNodes.some((n) => n.status === "RUNNING") && (
          <p className="text-sm text-ca-gold-500">
            {runNodes.filter((n) => n.status === "RUNNING").length} running
          </p>
        )}
        {runNodes.some((n) => n.status === "BLOCKED") && (
          <p className="text-sm text-ca-waiting">
            {runNodes.filter((n) => n.status === "BLOCKED").length} blocked
          </p>
        )}
      </div>
    </div>
  );
}
