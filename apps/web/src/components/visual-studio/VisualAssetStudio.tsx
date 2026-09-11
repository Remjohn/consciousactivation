import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { compileVisualProposal, compileVisualTransformProposal, getVisualStudio, recordVisualFeedback, type VisualFeedbackDecision, type VisualTransformType } from "../../api/visualStudio";

const OPERATOR = { actor_id: "operator-web-001", actor_type: "human" as const, product_id: "conscious-activations-web", workflow_role: "operator" as const };

function Badge({ children, tone = "neutral" }: { children: React.ReactNode; tone?: "good" | "warn" | "bad" | "neutral" }) {
  const classes = tone === "good" ? "border-ca-state-ready text-ca-state-ready" : tone === "bad" ? "border-ca-danger text-ca-danger" : tone === "warn" ? "border-ca-gold-500 text-ca-gold-500" : "border-ca-border text-ca-text-secondary";
  return <span className={`rounded-full border px-2 py-0.5 text-[10px] uppercase tracking-wider ${classes}`}>{children}</span>;
}

function Field({ label, value }: { label: string; value: React.ReactNode }) {
  return <div><div className="text-[10px] uppercase tracking-wider text-ca-text-secondary">{label}</div><div className="mt-1 break-all text-xs text-ca-text-primary">{value}</div></div>;
}

export function VisualAssetStudio({ campaignId }: { campaignId: string }) {
  const qc = useQueryClient();
  const query = useQuery({ queryKey: ["visual-studio", campaignId], queryFn: () => getVisualStudio(campaignId), refetchInterval: 4000 });
  const [selectedLayerId, setSelectedLayerId] = useState<string | null>(null);
  const [chatInput, setChatInput] = useState("");
  const [proposal, setProposal] = useState<any>(null);
  const [transformType, setTransformType] = useState<VisualTransformType>("MOVE_BBOX");
  const [transformAmount, setTransformAmount] = useState("5");
  const feedback = useMutation({
    mutationFn: (decision: VisualFeedbackDecision) => {
      const p = query.data;
      if (!p) throw new Error("Visual Studio projection is unavailable.");
      const layer = (p?.composition?.layers ?? []).find((item: any) => item.layer_id === (selectedLayerId ?? p?.selected_layer?.layer_id));
      return recordVisualFeedback(campaignId, {
        revision_ref: p.revision.revision_ref,
        target_ref: layer?.source_ref ?? null,
        decision,
        reason: decision === "NEEDS_EDIT" ? "COMPOSITION" : decision === "REJECT" ? "WRONG_READING" : null,
        note: decision === "GOOD" ? "Operator visual inspection marked the current composition good." : "Operator visual inspection requires follow-up.",
        operator_actor: OPERATOR,
        expected_state_version: p.revision.state_version,
      });
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["visual-studio", campaignId] }),
  });
  const propose = useMutation({
    mutationFn: (text: string) => {
      const p = query.data;
      if (!p) throw new Error("Visual Studio projection is unavailable.");
      const layer = (p?.composition?.layers ?? []).find((item: any) => item.layer_id === (selectedLayerId ?? p?.selected_layer?.layer_id));
      if (!layer) throw new Error("Select a canonical composition layer before proposing a visual edit.");
      return compileVisualProposal(campaignId, { target_ref: layer.source_ref ?? p.source.source_ref, target_node_id: layer.layer_id, natural_language_request: text, operator_actor: OPERATOR, expected_state_version: p.revision.state_version });
    },
    onSuccess: setProposal,
  });
  const transform = useMutation({
    mutationFn: () => {
      const p = query.data;
      if (!p) throw new Error("Visual Studio projection is unavailable.");
      const layer = (p?.composition?.layers ?? []).find((item: any) => item.layer_id === (selectedLayerId ?? p?.selected_layer?.layer_id));
      if (!layer?.source_ref) throw new Error("Select a canonical layer with source lineage before proposing a transform.");
      const amount = Number(transformAmount);
      if (!Number.isFinite(amount)) throw new Error("Transform amount must be numeric.");
      const argumentsByType: Record<VisualTransformType, Record<string, string | number | boolean>> = {
        MOVE_BBOX: { axis: "x", delta_micros: Math.round(amount * 10000), mode: "NORMALIZED_MICROS" },
        RESIZE_BBOX: { scale_delta_micros: Math.round(amount * 10000), anchor: "CENTER" },
        TRIM_SEGMENT: { edge: "END", delta_ms: Math.round(-amount), preserve_word_boundary: true, preserve_expression_tail: true },
      };
      return compileVisualTransformProposal(campaignId, { target_ref: layer.source_ref, target_node_id: layer.layer_id, manipulation_type: transformType, arguments: argumentsByType[transformType], operator_actor: OPERATOR, expected_state_version: p.revision.state_version });
    },
    onSuccess: setProposal,
  });

  const layers: any[] = query.data?.composition?.layers ?? [];
  const selected = useMemo(() => layers.find((item) => item.layer_id === (selectedLayerId ?? query.data?.selected_layer?.layer_id)) ?? layers[0] ?? null, [layers, selectedLayerId, query.data]);
  if (query.isLoading) return <div className="rounded-xl border border-ca-border bg-ca-surface p-6 text-sm text-ca-text-secondary">Loading canonical Visual Asset Studio projection…</div>;
  if (query.isError || !query.data) return <div className="rounded-xl border border-ca-danger/40 bg-ca-danger/10 p-6 text-sm text-ca-danger">Visual Asset Studio could not establish a canonical projection. No replacement or generated preview is shown.</div>;
  const p = query.data!;
  const preview = p.preview?.artifact_ref;
  const timeline = p.composition?.timeline;
  const canvasW = timeline?.width ?? 1920; const canvasH = timeline?.height ?? 1080;

  return <div className="space-y-5" data-testid="visual-asset-studio">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div><div className="text-xs uppercase tracking-[0.22em] text-ca-gold-500">Evidence-First Visual Asset Studio</div><h2 className="mt-1 text-xl font-semibold">Inspect → transform → compose → validate</h2></div>
      <div className="flex gap-2"><Badge tone="good">Canonical state</Badge><Badge tone={p.preview?.available ? "good" : "warn"}>{p.preview?.available ? "Artifact preview" : "Preview unavailable"}</Badge></div>
    </div>

    <div className="grid gap-4 xl:grid-cols-[280px_minmax(0,1fr)_320px]">
      <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Source and evidence">
        <div className="mb-4 flex items-center justify-between"><h3 className="font-medium">Source / evidence</h3><Badge>{p.source?.evidence_status}</Badge></div>
        {preview?.uri && String(preview.media_type ?? "").startsWith("video") ? <video className="mb-4 aspect-video w-full rounded-lg bg-black object-contain" controls src={preview.uri} /> : <div className="mb-4 rounded-lg border border-dashed border-ca-border bg-black/20 p-5 text-xs text-ca-text-secondary">No playable artifact is currently linked. Preview is not substituted with a mock.</div>}
        <div className="space-y-4">
          <Field label="Source identity" value={p.source?.source_ref ? `${p.source.source_ref.object_id} · v${p.source.source_ref.version}` : "MISSING"} />
          <Field label="Source SHA-256" value={p.source?.source_ref?.sha256 ?? "MISSING"} />
          <Field label="Selected range" value={selected?.source_range_ms?.[0] != null ? `${selected.source_range_ms[0]}–${selected.source_range_ms[1]} ms` : "Not recorded"} />
          <Field label="Lineage" value={<Badge tone={p.validation?.source_lineage === "PASS" ? "good" : "bad"}>{p.validation?.source_lineage}</Badge>} />
          <Field label="Source quality" value={<Badge tone="warn">{p.validation?.source_quality}</Badge>} />
        </div>
      </section>

      <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Composition canvas">
        <div className="mb-4 flex items-center justify-between"><h3 className="font-medium">Composition canvas</h3><span className="text-xs text-ca-text-secondary">{canvasW}×{canvasH}</span></div>
        <div className="relative mx-auto aspect-video max-w-4xl overflow-hidden rounded-lg border border-ca-border bg-[radial-gradient(circle_at_30%_20%,rgba(232,185,35,.15),transparent_30%),#0b0b0e]" data-testid="composition-canvas">
          {layers.map((layer, index) => { const active = layer.layer_id === selected?.layer_id; return <button key={layer.layer_id} onClick={() => setSelectedLayerId(layer.layer_id)} className={`absolute rounded-md border p-3 text-left text-xs transition ${active ? "border-ca-gold-500 bg-ca-gold-500/10" : "border-white/10 bg-white/5 hover:border-white/20"}`} style={{ left: `${8 + (index % 3) * 30}%`, top: `${10 + Math.floor(index / 3) * 28}%`, width: "25%" }} aria-label={`Layer ${layer.layer_id}`}><div className="font-medium">{layer.role || layer.kind}</div><div className="mt-1 text-[10px] text-ca-text-secondary">{layer.layer_id}</div></button>; })}
          {!layers.length && <div className="absolute inset-0 grid place-items-center text-xs text-ca-text-secondary">No canonical composition layers are available.</div>}
          <div className="absolute bottom-2 left-2 rounded border border-white/10 bg-black/50 px-2 py-1 text-[10px] text-ca-text-secondary">Canonical projection · not rendered-proof semantics</div>
        </div>
        <div className="mt-4 grid grid-cols-4 gap-2 text-[10px] text-ca-text-secondary"><div>RETRIEVE</div><div>TRANSFORM</div><div>COMPOSE</div><div>GENERATE</div></div>
      </section>

      <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Layer inspector">
        <h3 className="mb-4 font-medium">Layer inspector</h3>
        {selected ? <div className="space-y-4"><Field label="Layer" value={selected.layer_id} /><Field label="Role" value={selected.role} /><Field label="Kind" value={selected.kind} /><Field label="Editable operations" value={selected.editable_operations?.join(", ") || "None"} />
          <div><div className="mb-2 text-[10px] uppercase tracking-wider text-ca-text-secondary">Validation</div><div className="space-y-2"><div className="flex justify-between"><span className="text-xs">Lineage</span><Badge tone={p.validation.source_lineage === "PASS" ? "good" : "bad"}>{p.validation.source_lineage}</Badge></div><div className="flex justify-between"><span className="text-xs">Geometry</span><Badge tone="warn">{p.validation.geometry}</Badge></div><div className="flex justify-between"><span className="text-xs">Semantic correctness</span><Badge tone="warn">{p.validation.semantic_correctness}</Badge></div></div></div>
          <div><div className="mb-2 text-[10px] uppercase tracking-wider text-ca-text-secondary">Keyframes</div><div className="rounded border border-ca-border p-3 text-xs text-ca-text-secondary">{p.validation.keyframes}</div>{(p.keyframe_inspection?.selected_layer_keyframes ?? []).length > 0 && <div className="mt-2 space-y-1">{p.keyframe_inspection.selected_layer_keyframes.map((kf: any, i: number) => <div key={i} className="flex justify-between"><span>{kf.time_ms ?? kf.time ?? "—"}</span><span>{JSON.stringify(kf)}</span></div>)}</div>}</div>
          <div><div className="mb-2 text-[10px] uppercase tracking-wider text-ca-text-secondary">Transform controls</div><div className="grid grid-cols-[1fr_90px] gap-2"><select value={transformType} onChange={(e) => setTransformType(e.target.value as VisualTransformType)} className="rounded border border-ca-border bg-black/20 p-2 text-xs"><option value="MOVE_BBOX">Move X (%)</option><option value="RESIZE_BBOX">Resize (%)</option><option value="TRIM_SEGMENT">Trim end (ms)</option></select><input value={transformAmount} onChange={(e) => setTransformAmount(e.target.value)} inputMode="decimal" className="rounded border border-ca-border bg-black/20 p-2 text-xs" aria-label="Transform amount" /></div><button className="mt-2 w-full rounded bg-ca-gold-500 px-3 py-2 text-xs font-medium text-black disabled:opacity-50" disabled={!selected?.source_ref || transform.isPending} onClick={() => transform.mutate()}>Prepare deterministic transform</button>{transform.isError && <div className="mt-2 text-xs text-ca-danger">{transform.error instanceof Error ? transform.error.message : "Transform proposal failed."}</div>}</div>
        </div> : <div className="text-sm text-ca-text-secondary">Select a canonical layer to inspect.</div>}
      </section>
    </div>

    <div className="grid gap-4 lg:grid-cols-[1fr_1fr]">
      <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Visual chat">
        <div className="mb-3 flex items-center justify-between"><h3 className="font-medium">Visual Chat</h3><Badge>Typed proposals only</Badge></div>
        <textarea value={chatInput} onChange={(e) => setChatInput(e.target.value)} rows={3} className="w-full rounded-lg border border-ca-border bg-black/20 p-3 text-sm outline-none focus:border-ca-gold-500" placeholder="Ask for a bounded visual change; Chat does not mutate canonical state directly." />
        <div className="mt-3 flex flex-wrap gap-2"><button className="rounded border border-ca-border px-3 py-2 text-xs" disabled={!chatInput.trim() || !selected || propose.isPending} onClick={() => propose.mutate(chatInput)}>Propose</button><button className="rounded border border-ca-border px-3 py-2 text-xs" onClick={() => setChatInput("Regenerate the selected layer from its linked source evidence")}>REGENERATE</button><button className="rounded border border-ca-border px-3 py-2 text-xs" disabled={!proposal} onClick={() => setProposal(null)}>Clear</button></div>
        {proposal && <div className="mt-4 rounded-lg border border-ca-gold-500/30 bg-ca-gold-500/5 p-3"><div className="flex items-center justify-between"><span className="text-xs font-medium">Compiled proposal</span><Badge tone={proposal.compilation_status === "COMPILED" ? "good" : "warn"}>{proposal.compilation_status}</Badge></div><p className="mt-2 text-sm">{proposal.interpretation}</p><div className="mt-3 space-y-2 text-xs text-ca-text-secondary">{(proposal.exact_operations ?? []).map((op: any) => <div key={op.operation_id}>{op.tool_id} · {op.expected_effect}</div>)}</div>{proposal.compilation_status === "COMPILED" && <div className="mt-3"><button className="rounded bg-ca-gold-500 px-3 py-2 text-xs font-medium text-black" onClick={() => setChatInput("Confirm compiled proposal for operator review")}>COMPILE</button></div>}</div>}
        {propose.isError && <div className="mt-3 text-xs text-ca-danger">{propose.error instanceof Error ? propose.error.message : "Proposal compilation failed."}</div>}
      </section>
      <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Operator feedback">
        <div className="mb-3 flex items-center justify-between"><h3 className="font-medium">Operator inspection</h3><span className="text-xs text-ca-text-secondary">state v{p.revision.state_version}</span></div>
        <p className="mb-4 text-xs leading-5 text-ca-text-secondary">Feedback is persisted immutably against the current canonical revision. It does not promote, ship, or silently mutate production state.</p>
        <div className="grid grid-cols-3 gap-2"><button className="rounded border border-ca-state-ready/40 px-3 py-2 text-xs" onClick={() => feedback.mutate("GOOD")}>GOOD</button><button className="rounded border border-ca-gold-500/40 px-3 py-2 text-xs" onClick={() => feedback.mutate("NEEDS_EDIT")}>NEEDS_EDIT</button><button className="rounded border border-ca-danger/40 px-3 py-2 text-xs" onClick={() => feedback.mutate("REJECT")}>REJECT</button></div>
        {feedback.isSuccess && <div className="mt-3 text-xs text-ca-state-ready">Feedback receipt persisted: {feedback.data.feedback_ref.object_id}</div>}
        {feedback.isError && <div className="mt-3 text-xs text-ca-danger">{feedback.error instanceof Error ? feedback.error.message : "Feedback persistence failed."}</div>}
        <div className="mt-5 rounded-lg border border-ca-border p-3"><div className="text-[10px] uppercase tracking-wider text-ca-text-secondary">Governed release path</div><div className="mt-2 text-xs text-ca-text-secondary">Visual Asset Studio → canonical revision → validation → operator approval → downstream compile. No Visual Chat bypass is exposed here.</div></div>
      </section>
    </div>
  </div>;
}
