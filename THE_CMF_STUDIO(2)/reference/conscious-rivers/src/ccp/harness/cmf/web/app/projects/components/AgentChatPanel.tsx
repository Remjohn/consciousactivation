'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';

// ─── Types ───

interface Comment {
  comment_id: string;
  project_id: string;
  author: string;
  content: string;
  is_agent_command: boolean;
  agent_response: string | null;
  agent_job_id: string | null;
  created_at: string;
}

// ─── API helpers ───

const API_BASE = process.env.NEXT_PUBLIC_PROJECT_API_URL || 'http://localhost:8000';

async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('cmf_token') || 'dev-token' : 'dev-token';
  const res = await fetch(`${API_BASE}${path}`, {
    ...opts,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...opts.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error(body.detail || body.error || `API ${res.status}`);
  }
  return res.json();
}

// ─── Helpers ───

function formatTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// ═══════════════════════════════════════════
// Comment Bubble
// ═══════════════════════════════════════════

function CommentBubble({ comment }: { comment: Comment }) {
  const isSystem = comment.author === 'system';
  const isAgent = comment.author === 'agent';
  const isOperator = !isSystem && !isAgent;

  if (isSystem) {
    return (
      <div className="flex justify-center my-2">
        <div className="text-xs text-gray-400 bg-gray-50 px-3 py-1 rounded-full">
          {comment.content} · {formatTime(comment.created_at)}
        </div>
      </div>
    );
  }

  return (
    <div className={`flex ${isOperator ? 'justify-end' : 'justify-start'} mb-3`}>
      <div className={`max-w-[85%] ${isOperator ? 'order-2' : ''}`}>
        {/* Author label */}
        <div className={`text-xs mb-0.5 ${isOperator ? 'text-right text-gray-400' : 'text-blue-500'}`}>
          {isOperator ? 'You' : '🤖 Agent'} · {formatTime(comment.created_at)}
        </div>

        {/* Message */}
        <div className={`rounded-lg px-3 py-2 text-sm ${
          isOperator ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'
        }`}>
          {comment.content}
        </div>

        {/* Agent response (for @agent commands) */}
        {comment.is_agent_command && comment.agent_response && (
          <div className="mt-1 bg-green-50 border border-green-200 rounded-lg px-3 py-2 text-sm text-gray-800">
            <div className="text-xs text-green-600 font-medium mb-1">🤖 Agent Response</div>
            <div className="whitespace-pre-wrap">{comment.agent_response}</div>
            {comment.agent_job_id && (
              <div className="text-xs text-gray-400 mt-1">Job: {comment.agent_job_id}</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Agent Chat Panel
// ═══════════════════════════════════════════

export default function AgentChatPanel({
  projectId,
  isOpen,
  onClose,
}: {
  projectId: string;
  isOpen: boolean;
  onClose: () => void;
}) {
  const [comments, setComments] = useState<Comment[]>([]);
  const [total, setTotal] = useState(0);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // ── Fetch comments ──

  const fetchComments = useCallback(async (limit = 10, offset = 0) => {
    try {
      const data = await apiFetch<{ comments: Comment[]; total: number }>(
        `/api/projects/${encodeURIComponent(projectId)}/comments?limit=${limit}&offset=${offset}`
      );
      setComments(data.comments);
      setTotal(data.total);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    }
  }, [projectId]);

  useEffect(() => {
    if (isOpen) {
      fetchComments(10, 0);
    }
  }, [isOpen, fetchComments]);

  // Auto-scroll on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [comments]);

  // Focus input when panel opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // ── Send message ──

  const sendMessage = async () => {
    const content = input.trim();
    if (!content || sending) return;

    setSending(true);
    setInput('');

    try {
      const comment = await apiFetch<Comment>(
        `/api/projects/${encodeURIComponent(projectId)}/comments`,
        {
          method: 'POST',
          body: JSON.stringify({ content }),
        }
      );
      setComments(prev => [...prev, comment]);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  // ── Load more ──

  const loadMore = async () => {
    const offset = comments.length;
    try {
      const data = await apiFetch<{ comments: Comment[]; total: number }>(
        `/api/projects/${encodeURIComponent(projectId)}/comments?limit=10&offset=${offset}`
      );
      setComments(prev => [...data.comments, ...prev]);
      setTotal(data.total);
    } catch { /* ignore */ }
  };

  // ── Quick commands ──

  const quickCommands = [
    { label: 'Status', cmd: '@agent what\'s the status?' },
    { label: 'Cost', cmd: '@agent what\'s the cost breakdown?' },
    { label: 'Approve All', cmd: '@agent approve all' },
    { label: 'Export', cmd: '@agent export TikTok final' },
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-white border-l border-gray-200 shadow-xl z-40 flex flex-col">
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-200 flex items-center justify-between bg-gray-50">
        <div>
          <h3 className="text-sm font-semibold text-gray-800">Agent Chat</h3>
          <p className="text-xs text-gray-400">Type @agent or / for commands</p>
        </div>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg">✕</button>
      </div>

      {/* LLM offline warning */}
      {error && (
        <div className="bg-yellow-50 px-4 py-2 text-xs text-yellow-700 border-b border-yellow-200">
          Agent offline — commands queued for retry. Error: {error}
        </div>
      )}

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-3">
        {/* Load more */}
        {comments.length < total && (
          <div className="text-center mb-3">
            <button onClick={loadMore} className="text-xs text-blue-600 hover:underline">
              Load earlier messages ({total - comments.length} more)
            </button>
          </div>
        )}

        {comments.length === 0 && !error && (
          <div className="text-center py-8 text-gray-400 text-sm">
            <div className="text-3xl mb-2">💬</div>
            <p>No messages yet.</p>
            <p className="text-xs mt-1">Use @agent to interact with the Project Manager Agent.</p>
          </div>
        )}

        {comments.map(c => (
          <CommentBubble key={c.comment_id} comment={c} />
        ))}

        {sending && (
          <div className="flex justify-start mb-3">
            <div className="bg-gray-100 rounded-lg px-3 py-2 text-sm text-gray-400">
              🤖 Thinking…
            </div>
          </div>
        )}
      </div>

      {/* Quick commands */}
      <div className="px-4 py-2 border-t border-gray-100 flex gap-1 flex-wrap">
        {quickCommands.map(qc => (
          <button
            key={qc.label}
            className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded hover:bg-gray-200"
            onClick={() => { setInput(qc.cmd); inputRef.current?.focus(); }}
          >
            {qc.label}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="px-4 py-3 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            placeholder="Type a message or @agent command…"
            className="flex-1 border rounded-lg px-3 py-2 text-sm"
            value={input}
            onChange={e => {
              let val = e.target.value;
              // '/' shortcut → '@agent ' prefix
              if (val === '/') val = '@agent ';
              setInput(val);
            }}
            onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
            disabled={sending}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || sending}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
