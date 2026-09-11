import { Badge } from "../ui/Badge";

interface CertificationBadgesProps {
  readonly productionReady: boolean;
  readonly certified: boolean;
}

// Always renders both fields, always in a neutral/muted tone — no "hide when false"
// toggle and no green styling applied to `false`. See TS-APP-UI-004 §3: "Certification
// status is always shown, never hidden or styled to look better than it is."
export function CertificationBadges({ productionReady, certified }: CertificationBadgesProps) {
  return (
    <div className="mt-2 flex flex-wrap gap-1">
      <Badge tone="muted">Production-ready: {productionReady ? "Yes" : "No"}</Badge>
      <Badge tone="muted">Certified: {certified ? "Yes" : "No"}</Badge>
    </div>
  );
}
