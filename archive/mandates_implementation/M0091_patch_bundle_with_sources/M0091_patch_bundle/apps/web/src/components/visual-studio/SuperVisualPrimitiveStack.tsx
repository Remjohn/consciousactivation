import type { ReactNode } from "react";

export type PrimitiveRole = "BBOX" | "PRETEXT" | "SKIA" | "ROUGH_NOTATION";

const primitiveDescriptors: Array<{ role: PrimitiveRole; owner: string; responsibility: string }> = [
  { role: "BBOX", owner: "Geometry", responsibility: "authoritative spatial bounds and collision checks" },
  { role: "PRETEXT", owner: "Text fit", responsibility: "measurement and deterministic text wrapping" },
  { role: "SKIA", owner: "Rendering", responsibility: "display-list/raster substrate; not semantic authority" },
  { role: "ROUGH_NOTATION", owner: "Annotation", responsibility: "typed visual annotations; proposal-only until promoted" },
];

function Status({ value }: { value: string }) {
  const tone = value === "READY" || value === "PRESENT" ? "text-ca-state-ready" : value === "BLOCKED" ? "text-ca-danger" : "text-ca-text-secondary";
  return <span className={`text-[10px] uppercase tracking-wider ${tone}`}>{value}</span>;
}

export function SuperVisualPrimitiveStack({
  layers,
  rendererKind,
  children,
}: {
  layers: any[];
  rendererKind?: string;
  children?: ReactNode;
}) {
  return (
    <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="SuperVisual primitive stack" data-testid="supervisual-primitive-stack">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          <h3 className="font-medium">SuperVisual primitive stack</h3>
          <p className="mt-1 text-[11px] text-ca-text-secondary">Distinct primitive roles over the canonical composition surface.</p>
        </div>
        <Status value={layers.length ? "READY" : "NO_CANONICAL_LAYERS"} />
      </div>
      <div className="grid gap-2 md:grid-cols-2">
        {primitiveDescriptors.map((item) => {
          const present = item.role === "BBOX" ? layers.some((layer) => layer.bbox || layer.geometry) : item.role === "PRETEXT" ? layers.some((layer) => layer.text || layer.text_measurement) : item.role === "ROUGH_NOTATION" ? layers.some((layer) => (layer.annotations ?? []).length) : Boolean(rendererKind);
          return (
            <div key={item.role} className="rounded-lg border border-ca-border/80 p-3" data-testid={`primitive-${item.role}`}>
              <div className="flex items-center justify-between gap-3">
                <span className="text-xs font-semibold">{item.role}</span>
                <Status value={present ? "PRESENT" : "NOT_PRESENT"} />
              </div>
              <div className="mt-1 text-[10px] uppercase tracking-wider text-ca-text-secondary">{item.owner}</div>
              <div className="mt-2 text-xs leading-5 text-ca-text-secondary">{item.responsibility}</div>
            </div>
          );
        })}
      </div>
      {children}
      <div className="mt-4 rounded-lg border border-ca-border/80 p-3 text-[10px] leading-5 text-ca-text-secondary">
        <div><span className="font-medium text-ca-text-primary">Authority:</span> CAE canonical semantic/state/provenance contracts.</div>
        <div><span className="font-medium text-ca-text-primary">Editing:</span> geometry, text fit, rendering, and annotation remain distinct responsibilities.</div>
        <div><span className="font-medium text-ca-text-primary">Promotion:</span> operator approval is required; this surface does not silently mutate canonical state.</div>
      </div>
    </section>
  );
}
