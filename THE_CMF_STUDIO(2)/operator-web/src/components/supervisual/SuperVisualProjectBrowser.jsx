export function SuperVisualProjectBrowser({
  projects,
  selectedProjectId,
  onSelectProject,
  onCreateProject,
  loading,
}) {
  return (
    <aside className="sv-project-browser">
      <div className="sv-panel-header">
        <div>
          <p className="sv-eyebrow">SuperVisual</p>
          <h2>Projects</h2>
        </div>
        <button className="sv-button sv-button-small" onClick={onCreateProject}>
          New
        </button>
      </div>

      {loading ? (
        <div className="sv-skeleton">Loading projects…</div>
      ) : projects?.length ? (
        <div className="sv-project-list">
          {projects.map((project) => {
            const id = project.supervisual_project_id || project.id;
            return (
              <button
                key={id}
                className={`sv-project-card ${id === selectedProjectId ? "is-active" : ""}`}
                onClick={() => onSelectProject(id)}
              >
                <strong>{project.title || "Untitled SuperVisual"}</strong>
                <span>{project.status || "draft"}</span>
                <small>{project.updated_at || project.created_at || ""}</small>
              </button>
            );
          })}
        </div>
      ) : (
        <div className="sv-empty">
          <strong>No SuperVisual projects yet.</strong>
          <span>Create the first runtime-backed project.</span>
          <button className="sv-button" onClick={onCreateProject}>Create project</button>
        </div>
      )}
    </aside>
  );
}
