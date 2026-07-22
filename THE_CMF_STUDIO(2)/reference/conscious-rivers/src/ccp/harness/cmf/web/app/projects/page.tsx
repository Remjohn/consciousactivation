'use client';

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';

// ─── Types ───

interface Project {
  project_id: string;
  title: string;
  client: string | null;
  folder_id: string | null;
  folder_path: string;
  tags: string[];
  arc_type: string;
  beat_count: number;
  total_duration_sec: number;
  thumbnail_url: string | null;
  status: string;
  pipeline_id: string | null;
  manifest_id: string | null;
  pipeline_state: string;
  review_progress: { total_beats: number; approved: number; pending: number; regenerating: number };
  total_cost_usd: number;
  total_regenerations: number;
  has_active_editor_session: boolean;
  asset_counts: { source: number; keyframes: number; clips: number; renders: number; audio: number };
  created_at: string;
  updated_at: string;
  archived_at: string | null;
}

interface Folder {
  folder_id: string;
  name: string;
  parent_folder_id: string | null;
  color: string;
  sort_order: number;
  project_count: number;
  children: Folder[];
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

// ─── Status helpers ───

const STATUS_BADGE: Record<string, { label: string; color: string; bg: string }> = {
  DRAFT: { label: 'Draft', color: '#6b7280', bg: '#f3f4f6' },
  GENERATING: { label: 'Generating', color: '#d97706', bg: '#fef3c7' },
  REVIEW: { label: 'Review', color: '#2563eb', bg: '#dbeafe' },
  APPROVED: { label: 'Approved', color: '#16a34a', bg: '#dcfce7' },
  PUBLISHED: { label: 'Published', color: '#7c3aed', bg: '#ede9fe' },
  ARCHIVED: { label: 'Archived', color: '#374151', bg: '#e5e7eb' },
  FAILED: { label: 'Failed', color: '#dc2626', bg: '#fee2e2' },
};

const ARC_ICONS: Record<string, string> = {
  witness: '👁️', hero: '⚔️', origin: '🌱', fall: '🔻', rebirth: '🔄', quest: '🗺️',
};

function formatRelative(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60_000);
  if (mins < 1) return 'just now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

// ═══════════════════════════════════════════
// Folder Sidebar
// ═══════════════════════════════════════════

function FolderTree({
  folders,
  selectedFolderId,
  onSelect,
  totalCount,
  onCreateFolder,
  onDeleteFolder,
  onRenameFolder,
}: {
  folders: Folder[];
  selectedFolderId: string | null;
  onSelect: (id: string | null) => void;
  totalCount: number;
  onCreateFolder: (parentId: string | null) => void;
  onDeleteFolder: (id: string) => void;
  onRenameFolder: (id: string, name: string) => void;
}) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [contextMenu, setContextMenu] = useState<{ id: string; x: number; y: number } | null>(null);

  const toggle = (id: string) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleContext = (e: React.MouseEvent, folderId: string) => {
    e.preventDefault();
    setContextMenu({ id: folderId, x: e.clientX, y: e.clientY });
  };

  useEffect(() => {
    const close = () => setContextMenu(null);
    document.addEventListener('click', close);
    return () => document.removeEventListener('click', close);
  }, []);

  const renderFolder = (f: Folder, depth: number) => (
    <div key={f.folder_id}>
      <div
        className={`flex items-center gap-1 px-2 py-1 text-sm cursor-pointer rounded hover:bg-gray-100 ${
          selectedFolderId === f.folder_id ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
        }`}
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
        onClick={() => onSelect(f.folder_id)}
        onContextMenu={e => handleContext(e, f.folder_id)}
      >
        {f.children.length > 0 && (
          <button onClick={e => { e.stopPropagation(); toggle(f.folder_id); }} className="text-xs w-4">
            {expanded.has(f.folder_id) ? '▼' : '▶'}
          </button>
        )}
        <span style={{ color: f.color }}>📁</span>
        <span className="truncate flex-1">{f.name}</span>
        <span className="text-xs text-gray-400">{f.project_count}</span>
      </div>
      {expanded.has(f.folder_id) && f.children.map(c => renderFolder(c, depth + 1))}
    </div>
  );

  return (
    <div className="w-60 border-r border-gray-200 bg-gray-50 flex flex-col h-full">
      <div className="p-3 border-b border-gray-200 flex items-center justify-between">
        <span className="font-semibold text-sm text-gray-800">Folders</span>
        <button onClick={() => onCreateFolder(null)} className="text-xs text-blue-600 hover:underline">+ New</button>
      </div>
      <div className="flex-1 overflow-y-auto py-1">
        <div
          className={`flex items-center gap-2 px-3 py-1.5 text-sm cursor-pointer rounded mx-1 hover:bg-gray-100 ${
            selectedFolderId === null ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700'
          }`}
          onClick={() => onSelect(null)}
        >
          <span>🏠</span>
          <span className="flex-1">All Projects</span>
          <span className="text-xs text-gray-400">{totalCount}</span>
        </div>
        {folders.map(f => renderFolder(f, 1))}
      </div>

      {/* Context Menu */}
      {contextMenu && (
        <div
          className="fixed bg-white border border-gray-200 rounded shadow-lg py-1 z-50"
          style={{ left: contextMenu.x, top: contextMenu.y }}
        >
          <button className="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100" onClick={() => {
            const name = prompt('New folder name:');
            if (name) onRenameFolder(contextMenu.id, name);
            setContextMenu(null);
          }}>Rename</button>
          <button className="block w-full text-left px-3 py-1 text-sm hover:bg-gray-100" onClick={() => {
            onCreateFolder(contextMenu.id);
            setContextMenu(null);
          }}>Create Subfolder</button>
          <button className="block w-full text-left px-3 py-1 text-sm text-red-600 hover:bg-red-50" onClick={() => {
            if (confirm('Delete this folder? Projects inside will be moved to the parent folder.')) {
              onDeleteFolder(contextMenu.id);
            }
            setContextMenu(null);
          }}>Delete</button>
        </div>
      )}
    </div>
  );
}

// ═══════════════════════════════════════════
// Project Card (Grid)
// ═══════════════════════════════════════════

function ProjectCard({
  project,
  onOpen,
  onArchive,
  onDuplicate,
  onTitleChange,
}: {
  project: Project;
  onOpen: () => void;
  onArchive: () => void;
  onDuplicate: () => void;
  onTitleChange: (title: string) => void;
}) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(project.title);
  const badgeInfo = STATUS_BADGE[project.status] || STATUS_BADGE.DRAFT;
  const progress = project.review_progress;
  const approvalPct = progress.total_beats > 0 ? (progress.approved / progress.total_beats) * 100 : 0;
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (editing && inputRef.current) inputRef.current.focus();
  }, [editing]);

  return (
    <div className="group bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow relative">
      {/* Thumbnail */}
      <div className="h-36 bg-gray-100 relative flex items-center justify-center">
        {project.thumbnail_url ? (
          <img src={project.thumbnail_url} alt={project.title} className="w-full h-full object-cover" />
        ) : (
          <span className="text-4xl">{ARC_ICONS[project.arc_type] || '🎬'}</span>
        )}
        {project.has_active_editor_session && (
          <span className="absolute top-2 right-2 w-3 h-3 rounded-full bg-green-400 border-2 border-white" title="Active editor session" />
        )}
        {/* Hover quick actions */}
        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
          <button onClick={onOpen} className="bg-white text-gray-800 px-3 py-1.5 rounded text-xs font-medium hover:bg-gray-100">
            Open Editor
          </button>
          <button onClick={() => window.location.href = `/projects/${project.project_id}/assets`}
            className="bg-white text-gray-800 px-3 py-1.5 rounded text-xs font-medium hover:bg-gray-100">
            Assets
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-3">
        {/* Title */}
        {editing ? (
          <input
            ref={inputRef}
            className="w-full text-sm font-semibold border-b border-blue-400 outline-none bg-transparent"
            value={title}
            onChange={e => setTitle(e.target.value)}
            onBlur={() => { setEditing(false); if (title !== project.title) onTitleChange(title); }}
            onKeyDown={e => { if (e.key === 'Enter') { setEditing(false); if (title !== project.title) onTitleChange(title); } }}
          />
        ) : (
          <h3 className="text-sm font-semibold text-gray-900 truncate cursor-pointer" onDoubleClick={() => setEditing(true)} title="Double-click to rename">
            {project.title}
          </h3>
        )}

        {/* Status + progress */}
        <div className="flex items-center gap-2 mt-1.5">
          <span className="text-xs px-1.5 py-0.5 rounded" style={{ color: badgeInfo.color, backgroundColor: badgeInfo.bg }}>
            {badgeInfo.label}
          </span>
          {progress.total_beats > 0 && (
            <div className="flex-1 flex items-center gap-1">
              <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full transition-all" style={{ width: `${approvalPct}%` }} />
              </div>
              <span className="text-xs text-gray-500">{progress.approved}/{progress.total_beats}</span>
            </div>
          )}
        </div>

        {/* Metadata */}
        <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
          <span>{ARC_ICONS[project.arc_type] || '🎬'} {project.arc_type || '—'}</span>
          <span>·</span>
          <span>{project.beat_count} beats</span>
          <span>·</span>
          <span>${project.total_cost_usd.toFixed(2)}</span>
          <span>·</span>
          <span>{formatRelative(project.updated_at)}</span>
        </div>

        {/* Tags */}
        {project.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {project.tags.slice(0, 4).map(tag => (
              <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{tag}</span>
            ))}
            {project.tags.length > 4 && <span className="text-xs text-gray-400">+{project.tags.length - 4}</span>}
          </div>
        )}
      </div>

      {/* Actions dropdown (hover) */}
      <div className="absolute top-2 left-2 opacity-0 group-hover:opacity-100 transition-opacity">
        <div className="bg-white rounded shadow text-xs">
          <button onClick={onDuplicate} className="block px-2 py-1 hover:bg-gray-100 w-full text-left">Duplicate</button>
          <button onClick={onArchive} className="block px-2 py-1 hover:bg-gray-100 w-full text-left text-red-600">
            {project.status === 'ARCHIVED' ? 'Restore' : 'Archive'}
          </button>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Project Row (List view)
// ═══════════════════════════════════════════

function ProjectRow({
  project,
  onOpen,
  selected,
  onToggleSelect,
}: {
  project: Project;
  onOpen: () => void;
  selected: boolean;
  onToggleSelect: () => void;
}) {
  const badgeInfo = STATUS_BADGE[project.status] || STATUS_BADGE.DRAFT;
  const progress = project.review_progress;
  const approvalPct = progress.total_beats > 0 ? (progress.approved / progress.total_beats) * 100 : 0;

  return (
    <tr className="hover:bg-gray-50 cursor-pointer" onClick={onOpen}>
      <td className="px-3 py-2" onClick={e => e.stopPropagation()}>
        <input type="checkbox" checked={selected} onChange={onToggleSelect} />
      </td>
      <td className="px-3 py-2">
        <div className="w-10 h-10 rounded bg-gray-100 flex items-center justify-center overflow-hidden">
          {project.thumbnail_url
            ? <img src={project.thumbnail_url} className="w-full h-full object-cover" />
            : <span>{ARC_ICONS[project.arc_type] || '🎬'}</span>
          }
        </div>
      </td>
      <td className="px-3 py-2 text-sm font-medium text-gray-900">{project.title}</td>
      <td className="px-3 py-2">
        <span className="text-xs px-1.5 py-0.5 rounded" style={{ color: badgeInfo.color, backgroundColor: badgeInfo.bg }}>
          {badgeInfo.label}
        </span>
      </td>
      <td className="px-3 py-2">
        <div className="flex items-center gap-1">
          <div className="w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden">
            <div className="h-full bg-green-500 rounded-full" style={{ width: `${approvalPct}%` }} />
          </div>
          <span className="text-xs text-gray-500">{progress.approved}/{progress.total_beats}</span>
        </div>
      </td>
      <td className="px-3 py-2 text-xs text-gray-500">{project.arc_type || '—'}</td>
      <td className="px-3 py-2 text-xs text-gray-500">${project.total_cost_usd.toFixed(2)}</td>
      <td className="px-3 py-2 text-xs text-gray-500">{formatRelative(project.updated_at)}</td>
    </tr>
  );
}

// ═══════════════════════════════════════════
// Create Project Modal
// ═══════════════════════════════════════════

function CreateProjectModal({
  folders,
  defaultFolderId,
  onClose,
  onCreate,
}: {
  folders: Folder[];
  defaultFolderId: string | null;
  onClose: () => void;
  onCreate: (data: { title: string; client?: string; folder_id?: string; tags?: string[] }) => void;
}) {
  const [title, setTitle] = useState('');
  const [client, setClient] = useState('');
  const [folderId, setFolderId] = useState(defaultFolderId || '');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState<string[]>([]);

  const flatFolders = useMemo(() => {
    const out: { id: string; label: string }[] = [];
    const walk = (list: Folder[], depth: number) => {
      for (const f of list) {
        out.push({ id: f.folder_id, label: '  '.repeat(depth) + f.name });
        walk(f.children, depth + 1);
      }
    };
    walk(folders, 0);
    return out;
  }, [folders]);

  const addTag = () => {
    const t = tagInput.trim();
    if (t && !tags.includes(t)) setTags([...tags, t]);
    setTagInput('');
  };

  const submit = () => {
    if (!title.trim()) return;
    onCreate({
      title: title.trim(),
      client: client.trim() || undefined,
      folder_id: folderId || undefined,
      tags: tags.length > 0 ? tags : undefined,
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white rounded-lg w-[480px] max-h-[80vh] overflow-y-auto shadow-xl" onClick={e => e.stopPropagation()}>
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold">New Project</h2>
        </div>
        <div className="px-6 py-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
            <input className="w-full border rounded px-3 py-2 text-sm" value={title} onChange={e => setTitle(e.target.value)}
              placeholder="My Video Project" autoFocus />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Client</label>
            <input className="w-full border rounded px-3 py-2 text-sm" value={client} onChange={e => setClient(e.target.value)}
              placeholder="Client name (optional)" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Folder</label>
            <select className="w-full border rounded px-3 py-2 text-sm" value={folderId} onChange={e => setFolderId(e.target.value)}>
              <option value="">Root (no folder)</option>
              {flatFolders.map(f => <option key={f.id} value={f.id}>{f.label}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
            <div className="flex gap-2">
              <input className="flex-1 border rounded px-3 py-2 text-sm" value={tagInput}
                onChange={e => setTagInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addTag(); } }}
                placeholder="Type tag and press Enter" />
              <button onClick={addTag} className="px-3 py-2 bg-gray-100 rounded text-sm hover:bg-gray-200">Add</button>
            </div>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-2">
                {tags.map(t => (
                  <span key={t} className="flex items-center gap-1 bg-blue-50 text-blue-700 text-xs px-2 py-1 rounded">
                    {t}
                    <button onClick={() => setTags(tags.filter(x => x !== t))} className="text-blue-400 hover:text-blue-700">×</button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="px-6 py-3 border-t border-gray-200 flex justify-end gap-2">
          <button onClick={onClose} className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded">Cancel</button>
          <button onClick={submit} disabled={!title.trim()}
            className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
            Create Project
          </button>
        </div>
      </div>
    </div>
  );
}

// ═══════════════════════════════════════════
// Main Page
// ═══════════════════════════════════════════

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [folders, setFolders] = useState<Folder[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [selectedFolder, setSelectedFolder] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [sortBy, setSortBy] = useState('updated_at');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Selection (for bulk ops)
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());

  // Modals
  const [showCreate, setShowCreate] = useState(false);

  // ── Fetch data ──

  const fetchProjects = useCallback(async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (selectedFolder) params.set('folder_id', selectedFolder);
      if (search) params.set('q', search);
      if (statusFilter) params.set('status', statusFilter);
      params.set('sort_by', sortBy);
      params.set('sort_dir', 'desc');
      params.set('per_page', '100');

      const data = await apiFetch<{ projects: Project[]; total: number }>(`/api/projects?${params}`);
      setProjects(data.projects);
      setTotalCount(data.total);
      setError(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [selectedFolder, search, statusFilter, sortBy]);

  const fetchFolders = useCallback(async () => {
    try {
      const data = await apiFetch<{ folders: Folder[] }>('/api/folders');
      setFolders(data.folders);
    } catch { /* folders are non-critical */ }
  }, []);

  useEffect(() => {
    fetchProjects();
    fetchFolders();
  }, [fetchProjects, fetchFolders]);

  // Ctrl+K search shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('project-search')?.focus();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  // ── Handlers ──

  const handleCreate = async (data: { title: string; client?: string; folder_id?: string; tags?: string[] }) => {
    await apiFetch('/api/projects', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    fetchProjects();
    fetchFolders();
  };

  const handleArchive = async (pid: string) => {
    const project = projects.find(p => p.project_id === pid);
    if (!project) return;
    if (project.status === 'ARCHIVED') {
      await apiFetch(`/api/projects/${encodeURIComponent(pid)}/restore`, { method: 'POST' });
    } else {
      await apiFetch(`/api/projects/${encodeURIComponent(pid)}/archive`, { method: 'POST' });
    }
    fetchProjects();
  };

  const handleDuplicate = async (pid: string) => {
    await apiFetch(`/api/projects/${encodeURIComponent(pid)}/duplicate`, {
      method: 'POST',
      body: JSON.stringify({}),
    });
    fetchProjects();
  };

  const handleTitleChange = async (pid: string, title: string) => {
    await apiFetch(`/api/projects/${encodeURIComponent(pid)}`, {
      method: 'PATCH',
      body: JSON.stringify({ title }),
    });
    fetchProjects();
  };

  const handleCreateFolder = async (parentId: string | null) => {
    const name = prompt('Folder name:');
    if (!name) return;
    await apiFetch('/api/folders', {
      method: 'POST',
      body: JSON.stringify({ name, parent_folder_id: parentId }),
    });
    fetchFolders();
  };

  const handleDeleteFolder = async (fid: string) => {
    await apiFetch(`/api/folders/${encodeURIComponent(fid)}`, { method: 'DELETE' });
    if (selectedFolder === fid) setSelectedFolder(null);
    fetchFolders();
    fetchProjects();
  };

  const handleRenameFolder = async (fid: string, name: string) => {
    await apiFetch(`/api/folders/${encodeURIComponent(fid)}`, {
      method: 'PATCH',
      body: JSON.stringify({ name }),
    });
    fetchFolders();
  };

  const toggleSelect = (pid: string) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(pid)) next.delete(pid);
      else next.add(pid);
      return next;
    });
  };

  const handleBulkArchive = async () => {
    for (const pid of selectedIds) {
      await apiFetch(`/api/projects/${encodeURIComponent(pid)}/archive`, { method: 'POST' });
    }
    setSelectedIds(new Set());
    fetchProjects();
  };

  // ── Render ──

  return (
    <div className="flex h-screen bg-white">
      {/* Folder sidebar */}
      <FolderTree
        folders={folders}
        selectedFolderId={selectedFolder}
        onSelect={setSelectedFolder}
        totalCount={totalCount}
        onCreateFolder={handleCreateFolder}
        onDeleteFolder={handleDeleteFolder}
        onRenameFolder={handleRenameFolder}
      />

      {/* Main area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="border-b border-gray-200 px-4 py-3 flex items-center gap-3">
          <input
            id="project-search"
            type="text"
            placeholder="Search projects… (Ctrl+K)"
            className="flex-1 max-w-sm border rounded px-3 py-1.5 text-sm"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <select className="border rounded px-2 py-1.5 text-sm" value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
            <option value="">All statuses</option>
            {Object.keys(STATUS_BADGE).map(s => <option key={s} value={s}>{STATUS_BADGE[s].label}</option>)}
          </select>
          <select className="border rounded px-2 py-1.5 text-sm" value={sortBy} onChange={e => setSortBy(e.target.value)}>
            <option value="updated_at">Last Modified</option>
            <option value="created_at">Created</option>
            <option value="title">Title</option>
            <option value="status">Status</option>
            <option value="total_cost_usd">Cost</option>
          </select>
          <div className="flex border rounded">
            <button className={`px-2 py-1 text-sm ${viewMode === 'grid' ? 'bg-gray-100' : ''}`} onClick={() => setViewMode('grid')}>▦</button>
            <button className={`px-2 py-1 text-sm ${viewMode === 'list' ? 'bg-gray-100' : ''}`} onClick={() => setViewMode('list')}>☰</button>
          </div>
          <button onClick={() => setShowCreate(true)} className="px-4 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
            + New Project
          </button>
        </div>

        {/* Bulk actions bar */}
        {selectedIds.size > 0 && (
          <div className="bg-blue-50 px-4 py-2 flex items-center gap-3 border-b border-blue-200">
            <span className="text-sm text-blue-700">{selectedIds.size} selected</span>
            <button onClick={handleBulkArchive} className="text-xs text-red-600 hover:underline">Archive selected</button>
            <button onClick={() => setSelectedIds(new Set())} className="text-xs text-gray-500 hover:underline">Clear</button>
          </div>
        )}

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading && <div className="text-center text-gray-400 py-8">Loading projects…</div>}
          {error && <div className="text-center text-red-500 py-8">Error: {error}</div>}

          {!loading && projects.length === 0 && (
            <div className="text-center py-16">
              <div className="text-4xl mb-4">🎬</div>
              <h2 className="text-lg font-semibold text-gray-700">No projects yet</h2>
              <p className="text-gray-500 mt-1">Create your first video project to get started.</p>
              <button onClick={() => setShowCreate(true)} className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                + Create First Project
              </button>
            </div>
          )}

          {!loading && projects.length > 0 && viewMode === 'grid' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
              {projects.map(p => (
                <ProjectCard
                  key={p.project_id}
                  project={p}
                  onOpen={() => window.location.href = `/editor/${p.manifest_id || p.project_id}`}
                  onArchive={() => handleArchive(p.project_id)}
                  onDuplicate={() => handleDuplicate(p.project_id)}
                  onTitleChange={title => handleTitleChange(p.project_id, title)}
                />
              ))}
            </div>
          )}

          {!loading && projects.length > 0 && viewMode === 'list' && (
            <table className="w-full">
              <thead>
                <tr className="text-xs text-gray-500 border-b">
                  <th className="px-3 py-2 w-8" />
                  <th className="px-3 py-2 w-12" />
                  <th className="px-3 py-2 text-left">Title</th>
                  <th className="px-3 py-2 text-left">Status</th>
                  <th className="px-3 py-2 text-left">Progress</th>
                  <th className="px-3 py-2 text-left">Arc</th>
                  <th className="px-3 py-2 text-left">Cost</th>
                  <th className="px-3 py-2 text-left">Modified</th>
                </tr>
              </thead>
              <tbody>
                {projects.map(p => (
                  <ProjectRow
                    key={p.project_id}
                    project={p}
                    onOpen={() => window.location.href = `/editor/${p.manifest_id || p.project_id}`}
                    selected={selectedIds.has(p.project_id)}
                    onToggleSelect={() => toggleSelect(p.project_id)}
                  />
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Create modal */}
      {showCreate && (
        <CreateProjectModal
          folders={folders}
          defaultFolderId={selectedFolder}
          onClose={() => setShowCreate(false)}
          onCreate={handleCreate}
        />
      )}
    </div>
  );
}
