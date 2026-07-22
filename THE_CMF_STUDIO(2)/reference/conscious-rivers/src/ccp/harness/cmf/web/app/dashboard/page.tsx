'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ─── Types ───

interface PipelineRow {
  pipeline_id: string;
  project_id: string;
  project_title: string;
  current_state: string;
  progress: { total_beats: number; approved: number; pending: number; regenerating: number };
  cost_usd: number;
  started_at: string;
  duration_in_state_sec: number;
}

interface DashboardStats {
  active_pipelines: number;
  awaiting_review: number;
  approved_today: number;
  failed: number;
  total_cost_today_usd: number;
  queue_depth: number;
  concurrent_used: number;
  concurrent_limit: number;
}

interface ThroughputDay {
  date: string;
  completed: number;
  failed: number;
  total_cost_usd: number;
  avg_completion_sec: number;
}

// ─── API helpers ───

const API_BASE = process.env.NEXT_PUBLIC_PROJECT_API_URL || 'http://localhost:8000';

async function apiFetch<T>(path: string): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('cmf_token') || 'dev-token' : 'dev-token';
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return res.json();
}

// ─── Pipeline state helpers ───

const PIPELINE_STATES = [
  'PENDING', 'GENERATING_T2I', 'PROCESSING_AUDIO', 'AUDIO_COMPLETE',
  'QUALITY_GATE', 'GENERATING_I2V', 'FINGERPRINTING', 'ASSEMBLING_MANIFEST',
  'GENERATING_CAPTIONS', 'RENDERING_PREVIEW', 'READY_FOR_REVIEW',
  'REGENERATING', 'RENDERING_FINAL', 'APPROVED', 'PUBLISHED', 'FAILED',
];

const STATE_COLORS: Record<string, string> = {
  PENDING: '#9ca3af',
  GENERATING_T2I: '#f59e0b',
  PROCESSING_AUDIO: '#f59e0b',
  AUDIO_COMPLETE: '#f59e0b',
  QUALITY_GATE: '#8b5cf6',
  GENERATING_I2V: '#f59e0b',
  FINGERPRINTING: '#6366f1',
  ASSEMBLING_MANIFEST: '#6366f1',
  GENERATING_CAPTIONS: '#6366f1',
  RENDERING_PREVIEW: '#3b82f6',
  READY_FOR_REVIEW: '#2563eb',
  REGENERATING: '#d97706',
  RENDERING_FINAL: '#3b82f6',
  APPROVED: '#16a34a',
  PUBLISHED: '#7c3aed',
  FAILED: '#dc2626',
};

function StateBadge({ state }: { state: string }) {
  const color = STATE_COLORS[state] || '#6b7280';
  return (
    <span className="text-xs px-2 py-0.5 rounded font-medium" style={{ color, backgroundColor: `${color}20` }}>
      {state.replace(/_/g, ' ')}
    </span>
  );
}

function StateProgressDots({ currentState }: { currentState: string }) {
  const idx = PIPELINE_STATES.indexOf(currentState);
  return (
    <div className="flex gap-0.5 items-center">
      {PIPELINE_STATES.map((s, i) => (
        <div
          key={s}
          className="w-2 h-2 rounded-full"
          title={s}
          style={{
            backgroundColor:
              i < idx ? '#16a34a' :
              i === idx ? (STATE_COLORS[s] || '#6b7280') :
              '#e5e7eb',
          }}
        />
      ))}
    </div>
  );
}

// ═══════════════════════════════════════════
// Summary Card
// ═══════════════════════════════════════════

function SummaryCard({
  label,
  value,
  subtext,
  color,
  onClick,
}: {
  label: string;
  value: number | string;
  subtext?: string;
  color?: string;
  onClick?: () => void;
}) {
  return (
    <div
      className={`bg-white border border-gray-200 rounded-lg p-4 ${onClick ? 'cursor-pointer hover:shadow-md' : ''}`}
      onClick={onClick}
    >
      <div className="text-xs text-gray-500 uppercase tracking-wide">{label}</div>
      <div className="text-2xl font-bold mt-1" style={{ color: color || '#111827' }}>{value}</div>
      {subtext && <div className="text-xs text-gray-400 mt-0.5">{subtext}</div>}
    </div>
  );
}

// ═══════════════════════════════════════════
// Queue Lane
// ═══════════════════════════════════════════

function QueueLane({ pipelines, stats }: { pipelines: PipelineRow[]; stats: DashboardStats }) {
  const queued = pipelines.filter(p => p.current_state === 'PENDING');
  const processing = pipelines.filter(p => !['PENDING', 'APPROVED', 'PUBLISHED', 'FAILED'].includes(p.current_state));
  const completed = pipelines.filter(p => ['APPROVED', 'PUBLISHED'].includes(p.current_state));
  const failed = pipelines.filter(p => p.current_state === 'FAILED');

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-800 mb-3">Batch Queue</h3>
      <div className="flex gap-4">
        {/* Queued lane */}
        <div className="flex-1 min-w-0">
          <div className="text-xs text-gray-500 mb-1">QUEUED ({queued.length})</div>
          <div className="bg-gray-50 rounded p-2 min-h-[60px] space-y-1">
            {queued.map(p => (
              <div key={p.pipeline_id} className="bg-white border rounded px-2 py-1 text-xs truncate">
                {p.project_title}
              </div>
            ))}
            {queued.length === 0 && <div className="text-xs text-gray-300 text-center py-2">Empty</div>}
          </div>
        </div>

        <div className="text-gray-300 flex items-center">→</div>

        {/* Processing lane */}
        <div className="flex-1 min-w-0">
          <div className="text-xs text-gray-500 mb-1">PROCESSING ({processing.length}/{stats.concurrent_limit})</div>
          <div className="bg-blue-50 rounded p-2 min-h-[60px] space-y-1">
            {processing.slice(0, stats.concurrent_limit).map(p => (
              <div key={p.pipeline_id} className="bg-white border border-blue-200 rounded px-2 py-1">
                <div className="text-xs truncate">{p.project_title}</div>
                <StateProgressDots currentState={p.current_state} />
              </div>
            ))}
            {processing.length === 0 && <div className="text-xs text-gray-300 text-center py-2">Idle</div>}
          </div>
        </div>

        <div className="text-gray-300 flex items-center">→</div>

        {/* Completed lane */}
        <div className="flex-1 min-w-0">
          <div className="text-xs text-gray-500 mb-1">COMPLETED ({completed.length})</div>
          <div className="bg-green-50 rounded p-2 min-h-[60px] space-y-1">
            {completed.slice(0, 5).map(p => (
              <div key={p.pipeline_id} className="bg-white border border-green-200 rounded px-2 py-1 text-xs truncate">
                ✅ {p.project_title}
              </div>
            ))}
            {completed.length > 5 && <div className="text-xs text-gray-400 text-center">+{completed.length - 5} more</div>}
            {completed.length === 0 && <div className="text-xs text-gray-300 text-center py-2">None yet</div>}
          </div>
        </div>

        {/* Failed lane */}
        {failed.length > 0 && (
          <>
            <div className="text-gray-300 flex items-center">→</div>
            <div className="flex-1 min-w-0">
              <div className="text-xs text-red-500 mb-1">FAILED ({failed.length})</div>
              <div className="bg-red-50 rounded p-2 min-h-[60px] space-y-1">
                {failed.map(p => (
                  <div key={p.pipeline_id} className="bg-white border border-red-200 rounded px-2 py-1 text-xs truncate">
                    ❌ {p.project_title}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Throughput Chart (simple bar chart)
// ═══════════════════════════════════════════

function ThroughputChart({ daily }: { daily: ThroughputDay[] }) {
  const maxVal = Math.max(1, ...daily.map(d => d.completed + d.failed));

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-800 mb-3">Throughput (Last 30 Days)</h3>
      <div className="flex items-end gap-1 h-32">
        {daily.slice(0, 30).reverse().map(d => {
          const h = ((d.completed + d.failed) / maxVal) * 100;
          const failH = maxVal > 0 ? (d.failed / maxVal) * 100 : 0;
          return (
            <div key={d.date} className="flex-1 flex flex-col items-center justify-end" title={`${d.date}: ${d.completed} done, ${d.failed} failed, $${d.total_cost_usd.toFixed(2)}`}>
              <div className="w-full flex flex-col justify-end" style={{ height: `${h}%`, minHeight: h > 0 ? '4px' : '0' }}>
                {d.failed > 0 && <div className="bg-red-400 rounded-t" style={{ height: `${failH}%`, minHeight: '2px' }} />}
                <div className="bg-green-400 rounded-t flex-1" />
              </div>
            </div>
          );
        })}
      </div>
      <div className="flex justify-between mt-1 text-xs text-gray-400">
        <span>30d ago</span>
        <span>Today</span>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Main Dashboard Page
// ═══════════════════════════════════════════

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [pipelines, setPipelines] = useState<PipelineRow[]>([]);
  const [throughput, setThroughput] = useState<ThroughputDay[]>([]);
  const [loading, setLoading] = useState(true);
  const [stateFilter, setStateFilter] = useState('');
  const [sseStatus, setSseStatus] = useState<'connected' | 'reconnecting' | 'failed'>('reconnecting');
  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectDelayRef = useRef(1000);

  // ── Fetch data ──

  const fetchAll = useCallback(async () => {
    try {
      setLoading(true);
      const [s, p, t] = await Promise.all([
        apiFetch<DashboardStats>('/api/dashboard/stats'),
        apiFetch<{ pipelines: PipelineRow[] }>('/api/dashboard/pipelines'),
        apiFetch<{ daily: ThroughputDay[] }>('/api/dashboard/throughput?days=30'),
      ]);
      setStats(s);
      setPipelines(p.pipelines);
      setThroughput(t.daily);
    } catch {
      // Will show stale data
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  // ── SSE Connection ──

  const connectSSE = useCallback(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('cmf_token') || 'dev-token' : 'dev-token';
    const es = new EventSource(`${API_BASE}/api/dashboard/stream?authorization=Bearer+${encodeURIComponent(token)}`);
    eventSourceRef.current = es;

    es.onopen = () => {
      setSseStatus('connected');
      reconnectDelayRef.current = 1000;
    };

    es.addEventListener('pipeline_update', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setPipelines(prev => {
        const idx = prev.findIndex(p => p.pipeline_id === data.pipeline_id);
        if (idx >= 0) {
          const updated = [...prev];
          updated[idx] = { ...updated[idx], current_state: data.state, progress: data.progress, cost_usd: data.cost_usd };
          return updated;
        }
        return prev;
      });
    });

    es.addEventListener('cost_update', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setStats(prev => prev ? { ...prev, total_cost_today_usd: data.daily_cost_usd } : prev);
    });

    es.addEventListener('queue_update', (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setStats(prev =>
        prev ? { ...prev, queue_depth: data.queue_stats?.queued || 0, } : prev
      );
    });

    es.onerror = () => {
      es.close();
      setSseStatus('reconnecting');
      // Exponential backoff: 1s, 2s, 4s, ... max 30s (FR-VID-11 §4 Stage 4)
      const delay = reconnectDelayRef.current;
      reconnectDelayRef.current = Math.min(delay * 2, 30000);
      setTimeout(() => connectSSE(), delay);
    };
  }, []);

  useEffect(() => {
    connectSSE();
    return () => { eventSourceRef.current?.close(); };
  }, [connectSSE]);

  // Polling fallback if SSE fails (TD4: 5s interval)
  useEffect(() => {
    if (sseStatus !== 'connected') {
      const interval = setInterval(() => fetchAll(), 5000);
      return () => clearInterval(interval);
    }
  }, [sseStatus, fetchAll]);

  // ── Filtered pipelines ──
  const filteredPipelines = stateFilter
    ? pipelines.filter(p => p.current_state === stateFilter)
    : pipelines;

  // ── Render ──

  if (loading && !stats) {
    return <div className="flex items-center justify-center h-screen text-gray-400">Loading dashboard…</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 space-y-6">
      {/* SSE status banner */}
      {sseStatus === 'reconnecting' && (
        <div className="bg-yellow-50 border border-yellow-200 rounded px-4 py-2 text-sm text-yellow-700">
          ⚠ Reconnecting to live updates… Using polling fallback (5s).
        </div>
      )}

      {/* Section 1: Summary Cards */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <SummaryCard label="Active Pipelines" value={stats.active_pipelines} color="#2563eb" />
          <SummaryCard label="Awaiting Review" value={stats.awaiting_review} color="#d97706"
            onClick={() => setStateFilter('READY_FOR_REVIEW')} />
          <SummaryCard label="Approved Today" value={stats.approved_today} color="#16a34a" />
          <SummaryCard
            label="Failed"
            value={stats.failed}
            color={stats.failed > 0 ? '#dc2626' : '#6b7280'}
            onClick={() => setStateFilter('FAILED')}
          />
          <SummaryCard label="Cost Today" value={`$${stats.total_cost_today_usd.toFixed(2)}`} />
          <SummaryCard
            label="Queue"
            value={stats.queue_depth}
            subtext={`${stats.concurrent_used}/${stats.concurrent_limit} slots`}
          />
        </div>
      )}

      {/* Section 2: Active Pipeline Table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="px-4 py-3 border-b border-gray-200 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-800">Active Pipelines</h3>
          <div className="flex items-center gap-2">
            <select className="border rounded px-2 py-1 text-sm" value={stateFilter} onChange={e => setStateFilter(e.target.value)}>
              <option value="">All states</option>
              {PIPELINE_STATES.map(s => <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>)}
            </select>
            <button onClick={fetchAll} className="text-xs text-blue-600 hover:underline">Refresh</button>
          </div>
        </div>

        {filteredPipelines.length === 0 ? (
          <div className="text-center py-8 text-gray-400 text-sm">No active pipelines</div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="text-xs text-gray-500 border-b bg-gray-50">
                <th className="px-4 py-2 text-left">Project</th>
                <th className="px-4 py-2 text-left">State</th>
                <th className="px-4 py-2 text-left">Progress</th>
                <th className="px-4 py-2 text-left">Beats</th>
                <th className="px-4 py-2 text-left">Cost</th>
                <th className="px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredPipelines.map(p => (
                <tr key={p.pipeline_id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <div className="text-sm font-medium text-gray-900">{p.project_title}</div>
                    <div className="text-xs text-gray-400">{p.pipeline_id}</div>
                  </td>
                  <td className="px-4 py-3"><StateBadge state={p.current_state} /></td>
                  <td className="px-4 py-3"><StateProgressDots currentState={p.current_state} /></td>
                  <td className="px-4 py-3">
                    {p.progress.total_beats > 0 && (
                      <span className="text-xs text-gray-600">
                        {p.progress.approved}/{p.progress.total_beats} approved
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">${p.cost_usd.toFixed(2)}</td>
                  <td className="px-4 py-3">
                    <button
                      className="text-xs text-blue-600 hover:underline"
                      onClick={() => window.location.href = `/editor/${p.project_id}`}
                    >
                      Open Editor
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Section 3: Queue Visualization */}
      {stats && <QueueLane pipelines={pipelines} stats={stats} />}

      {/* Section 4: Throughput Chart */}
      {throughput.length > 0 && <ThroughputChart daily={throughput} />}
    </div>
  );
}
