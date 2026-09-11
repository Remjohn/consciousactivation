import { Link } from "@tanstack/react-router";

export function EmptyCampaignState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-[var(--radius-card)] border border-border-subtle bg-surface p-12 text-center">
      <svg
        className="mb-4 h-12 w-12 text-ink-faint"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth={1.5}
      >
        <rect x={3} y={3} width={18} height={18} rx={2} />
        <path d="M9 12h6M12 9v6" />
      </svg>
      <h3 className="text-ink-primary text-lg font-semibold">No campaigns yet</h3>
      <p className="mt-1 text-ink-muted text-sm">Create your first campaign to get started.</p>
      <Link
        to="/campaigns/new"
        className="mt-6 inline-flex rounded-full bg-gold px-5 py-2.5 font-semibold text-gold-on"
      >
        + Create your first campaign
      </Link>
    </div>
  );
}
