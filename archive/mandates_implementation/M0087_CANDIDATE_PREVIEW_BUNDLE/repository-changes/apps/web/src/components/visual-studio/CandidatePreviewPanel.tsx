import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  decideCandidate,
  getCandidateSession,
  navigateCandidateSession,
  promoteCandidate,
  type CandidatePreviewProjection,
} from "../../api/candidatePreview";

const OPERATOR = {
  actor_id: "operator-web-001",
  actor_type: "human" as const,
  product_id: "conscious-activations-web",
  workflow_role: "operator" as const,
};

function MiniBadge({ children, good = false, warn = false }: { children: React.ReactNode; good?: boolean; warn?: boolean }) {
  const tone = good ? "border-ca-state-ready text-ca-state-ready" : warn ? "border-ca-gold-500 text-ca-gold-500" : "border-ca-border text-ca-text-secondary";
  return <span className={`rounded-full border px-2 py-0.5 text-[10px] uppercase tracking-wider ${tone}`}>{children}</span>;
}

function Meta({ label, value }: { label: string; value: React.ReactNode }) {
  return <div><div className="text-[10px] uppercase tracking-wider text-ca-text-secondary">{label}</div><div className="mt-1 break-all text-xs text-ca-text-primary">{value}</div></div>;
}

export function CandidatePreviewPanel({ initialSessionId = "" }: { initialSessionId?: string }) {
  const qc = useQueryClient();
  const [sessionId, setSessionId] = useState(initialSessionId);
  const [sessionDraft, setSessionDraft] = useState(initialSessionId);
  const [rejectNote, setRejectNote] = useState("");
  const touchStart = useRef<number | null>(null);

  useEffect(() => setSessionId(initialSessionId), [initialSessionId]);

  const query = useQuery({
    queryKey: ["candidate-preview", sessionId],
    queryFn: () => getCandidateSession(sessionId),
    enabled: Boolean(sessionId),
    retry: false,
  });

  const refresh = () => qc.invalidateQueries({ queryKey: ["candidate-preview", sessionId] });
  const navigate = useMutation({
    mutationFn: (direction: "NEXT" | "PREVIOUS") => {
      const p = query.data?.session;
      if (!p) throw new Error("Candidate session is unavailable.");
      return navigateCandidateSession(sessionId, { direction, expected_version: p.version });
    },
    onSuccess: (data) => qc.setQueryData(["candidate-preview", sessionId], data),
  });
  const decide = useMutation({
    mutationFn: (decision: "ACCEPT" | "AUTO_ACCEPT" | "REJECT") => {
      const p = query.data?.session;
      const candidate = query.data?.current_candidate;
      if (!p || !candidate) throw new Error("Candidate session is unavailable.");
      return decideCandidate(sessionId, {
        candidate_id: candidate.candidate_id,
        decision,
        expected_version: p.version,
        operator_actor: decision === "AUTO_ACCEPT" ? undefined : OPERATOR,
        rationale: decision === "REJECT" ? rejectNote : undefined,
      });
    },
    onSuccess: (data) => { setRejectNote(""); qc.setQueryData(["candidate-preview", sessionId], data); },
  });
  const promote = useMutation({
    mutationFn: () => {
      const p = query.data?.session;
      if (!p) throw new Error("Candidate session is unavailable.");
      return promoteCandidate(sessionId, { expected_version: p.version, operator_actor: OPERATOR });
    },
    onSuccess: refresh,
  });

  const p = query.data as CandidatePreviewProjection | undefined;
  const current = p?.current_candidate;
  const candidates = p?.portfolio?.candidates ?? [];

  const handleTouchStart = (event: React.TouchEvent) => { touchStart.current = event.changedTouches[0]?.clientX ?? null; };
  const handleTouchEnd = (event: React.TouchEvent) => {
    if (touchStart.current == null) return;
    const end = event.changedTouches[0]?.clientX ?? touchStart.current;
    const delta = end - touchStart.current;
    touchStart.current = null;
    if (Math.abs(delta) < 48) return;
    navigate.mutate(delta < 0 ? "NEXT" : "PREVIOUS");
  };

  return <section className="rounded-xl border border-ca-border bg-ca-surface p-4" aria-label="Candidate preview and selection">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <div><div className="text-xs uppercase tracking-[0.22em] text-ca-gold-500">Asset Research</div><h3 className="mt-1 font-medium">Candidate preview & promotion</h3></div>
      <div className="flex gap-2"><MiniBadge>{p?.session?.status ?? "NO SESSION"}</MiniBadge><MiniBadge warn>Retrieval-owned candidates</MiniBadge></div>
    </div>

    <div className="mt-4 flex flex-wrap gap-2">
      <input value={sessionDraft} onChange={(e) => setSessionDraft(e.target.value)} onKeyDown={(e) => e.key === "Enter" && setSessionId(sessionDraft.trim())} placeholder="Candidate session ID" className="min-w-[260px] flex-1 rounded border border-ca-border bg-black/10 px-3 py-2 text-xs text-ca-text-primary" aria-label="Candidate session ID" />
      <button onClick={() => setSessionId(sessionDraft.trim())} className="rounded border border-ca-border px-3 py-2 text-xs hover:border-ca-gold-500">Open session</button>
    </div>

    {!sessionId && <div className="mt-4 rounded-lg border border-dashed border-ca-border p-5 text-xs text-ca-text-secondary">No candidate session is attached to this campaign yet. The authoritative retrieval path must create and bind the candidate session; no mock candidates are synthesized here.</div>}
    {sessionId && query.isLoading && <div className="mt-4 text-xs text-ca-text-secondary">Loading candidate session…</div>}
    {sessionId && query.isError && <div className="mt-4 rounded-lg border border-ca-danger/40 bg-ca-danger/10 p-4 text-xs text-ca-danger">Candidate session could not be loaded. The preview remains fail-closed.</div>}

    {current && p && <>
      <div className="mt-4 grid gap-4 lg:grid-cols-[minmax(0,1fr)_300px]">
        <div
          className="overflow-hidden rounded-lg border border-ca-border bg-black/30"
          onTouchStart={handleTouchStart}
          onTouchEnd={handleTouchEnd}
          tabIndex={0}
          onKeyDown={(e) => { if (e.key === "ArrowLeft") navigate.mutate("PREVIOUS"); if (e.key === "ArrowRight") navigate.mutate("NEXT"); }}
          aria-label="Playable candidate preview; swipe or use arrow keys to inspect adjacent candidates"
        >
          {current.preview_uri && String(current.media_type).startsWith("VIDEO") ? <video className="aspect-video w-full bg-black object-contain" controls preload="metadata" src={current.preview_uri} /> : <div className="aspect-video grid place-items-center p-6 text-center text-xs text-ca-text-secondary">No playable media URI was supplied by retrieval. No replacement preview is synthesized.</div>}
          <div className="flex items-center justify-between border-t border-ca-border px-3 py-2 text-xs"><span>{current.candidate_id}</span><span>Candidate {p.session.current_index + 1} / {candidates.length}</span></div>
        </div>

        <div className="space-y-4">
          <Meta label="Source" value={`${current.source_ref.object_id} · v${current.source_ref.version}`} />
          <Meta label="Source SHA-256" value={current.source_ref.sha256} />
          <Meta label="Interval" value={`${current.source_range_ms[0]}–${current.source_range_ms[1]} ms`} />
          <Meta label="Rights" value={<MiniBadge good={current.rights_state === "CLEARED"}>{current.rights_state}</MiniBadge>} />
          <Meta label="Confidence / fit / quality" value={`${current.confidence_bps} / ${current.semantic_fit_bps} / ${current.quality_bps} bps`} />
          <Meta label="Eligibility" value={<MiniBadge good={current.eligible}>{current.eligible ? "eligible" : "blocked"}</MiniBadge>} />
          <Meta label="Provenance" value={`${current.provenance.scene_id ?? "MISSING scene"} · ${current.provenance.source_version}`} />
          <p className="rounded border border-ca-border bg-black/10 p-3 text-xs text-ca-text-secondary">{current.transcript_context || "No transcript context supplied."}</p>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <button disabled={navigate.isPending} onClick={() => navigate.mutate("PREVIOUS")} className="rounded border border-ca-border px-3 py-2 text-xs hover:border-ca-gold-500 disabled:opacity-40">← Previous</button>
        <button disabled={navigate.isPending} onClick={() => navigate.mutate("NEXT")} className="rounded border border-ca-border px-3 py-2 text-xs hover:border-ca-gold-500 disabled:opacity-40">Next →</button>
        <button disabled={decide.isPending} onClick={() => decide.mutate("ACCEPT")} className="rounded border border-ca-state-ready px-3 py-2 text-xs text-ca-state-ready disabled:opacity-40">Accept</button>
        <button disabled={decide.isPending} onClick={() => decide.mutate("AUTO_ACCEPT")} className="rounded border border-ca-gold-500 px-3 py-2 text-xs text-ca-gold-500 disabled:opacity-40">Auto-accept (gated)</button>
        <input value={rejectNote} onChange={(e) => setRejectNote(e.target.value)} placeholder="Rejection rationale" className="min-w-[210px] flex-1 rounded border border-ca-border bg-black/10 px-3 py-2 text-xs" aria-label="Rejection rationale" />
        <button disabled={decide.isPending || rejectNote.trim().length < 5} onClick={() => decide.mutate("REJECT")} className="rounded border border-ca-danger px-3 py-2 text-xs text-ca-danger disabled:opacity-40">Reject</button>
        <button disabled={!p.session.selected_candidate_id || promote.isPending} onClick={() => promote.mutate()} className="rounded bg-ca-gold-500 px-3 py-2 text-xs font-medium text-white disabled:opacity-40">Promote to canonical VAE/Storyboard state</button>
      </div>

      <div className="mt-3 flex items-center justify-between text-[10px] text-ca-text-secondary">
        <span>Swipe left/right or use ←/→ · rejected candidates remain in session lineage · promotion is operator-gated</span>
        <span>{p.session.last_receipt_ref ? `Receipt: ${p.session.last_receipt_ref.object_id}` : "No decision receipt yet"}</span>
      </div>
    </>}
  </section>;
}
