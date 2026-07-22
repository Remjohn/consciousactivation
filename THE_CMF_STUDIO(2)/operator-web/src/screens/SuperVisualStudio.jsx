import { useEffect, useMemo, useState } from "react";
import {
  SuperVisualActionBar,
  SuperVisualCanvasPreview,
  SuperVisualCommandBar,
  SuperVisualCompositionPanel,
  SuperVisualCreateProjectModal,
  SuperVisualEventsTimeline,
  SuperVisualInspector,
  SuperVisualProjectBrowser,
  SuperVisualStatusRail,
} from "../components/supervisual";
import { buildSuperVisualViewModel } from "../lib/supervisualViewModel";
import { useSuperVisualActions } from "../hooks/useSuperVisualActions";
import { useSuperVisualEvents } from "../hooks/useSuperVisualEvents";
import { useSuperVisualProject } from "../hooks/useSuperVisualProject";
import { useSuperVisualProjects } from "../hooks/useSuperVisualProjects";
import { useSuperVisualSnapshot } from "../hooks/useSuperVisualSnapshot";
import "../styles/supervisual.css";

function getProjectId(project) {
  return project?.supervisual_project_id || project?.id || null;
}

function getVariantId(projectDetail) {
  return (
    projectDetail?.current_variant?.supervisual_variant_id ||
    projectDetail?.current_variant?.id ||
    projectDetail?.current_variant_id ||
    projectDetail?.project?.current_variant_id ||
    null
  );
}

export function SuperVisualStudio() {
  const {
    projects,
    loading: projectsLoading,
    error: projectsError,
    refresh: refreshProjects,
    createProject,
  } = useSuperVisualProjects();

  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    if (!selectedProjectId && projects?.length) {
      setSelectedProjectId(getProjectId(projects[0]));
    }
  }, [projects, selectedProjectId]);

  const {
    projectDetail,
    loading: projectLoading,
    error: projectError,
    refresh: refreshProject,
  } = useSuperVisualProject(selectedProjectId);

  const variantId = getVariantId(projectDetail);

  const {
    snapshot,
    loading: snapshotLoading,
    error: snapshotError,
    refresh: refreshSnapshot,
  } = useSuperVisualSnapshot(variantId);

  const {
    events,
    loading: eventsLoading,
    error: eventsError,
    refresh: refreshEvents,
  } = useSuperVisualEvents(variantId, {
    poll: Boolean(variantId && snapshot?.status && !["approved", "exported", "archived"].includes(snapshot.status)),
    intervalMs: 5000,
  });

  const refreshAll = async () => {
    await Promise.allSettled([
      refreshProjects(),
      selectedProjectId ? refreshProject() : Promise.resolve(),
      variantId ? refreshSnapshot() : Promise.resolve(),
      variantId ? refreshEvents() : Promise.resolve(),
    ]);
  };

  const {
    activeAction,
    error: actionError,
    runAction,
    submitRevision,
  } = useSuperVisualActions({
    variantId,
    onAfterAction: refreshAll,
  });

  const viewModel = useMemo(
    () => buildSuperVisualViewModel({ projectDetail, snapshot, events }),
    [projectDetail, snapshot, events]
  );

  async function handleCreateProject(payload) {
    setCreating(true);
    try {
      const result = await createProject(payload);
      const project = result?.project || result;
      const id = getProjectId(project);
      if (id) setSelectedProjectId(id);
      setCreateOpen(false);
    } finally {
      setCreating(false);
    }
  }

  const combinedError =
    projectsError ||
    projectError ||
    snapshotError ||
    eventsError ||
    actionError;

  return (
    <div className="sv-studio-runtime">
      <SuperVisualProjectBrowser
        projects={projects}
        selectedProjectId={selectedProjectId}
        onSelectProject={setSelectedProjectId}
        onCreateProject={() => setCreateOpen(true)}
        loading={projectsLoading}
      />

      <main className="sv-main">
        <header className="sv-hero">
          <div>
            <p className="sv-eyebrow">Runtime-backed cockpit</p>
            <h1>{viewModel.projectTitle}</h1>
            <p>
              {viewModel.variantLabel} / {viewModel.status.replaceAll("_", " ")}
            </p>
          </div>
          <SuperVisualActionBar
            actions={viewModel.availableActions}
            status={viewModel.status}
            activeAction={activeAction}
            onRunAction={(action) => runAction(action)}
          />
        </header>

        {combinedError ? (
          <div className="sv-error-banner">
            <strong>Runtime error</strong>
            <span>{combinedError.message}</span>
          </div>
        ) : null}

        {!selectedProjectId && !projectsLoading ? (
          <section className="sv-empty sv-empty-main">
            <h2>No project selected</h2>
            <p>Create a SuperVisual project to start using the backend runtime.</p>
            <button className="sv-button sv-button-primary" onClick={() => setCreateOpen(true)}>
              Create project
            </button>
          </section>
        ) : (
          <>
            <SuperVisualStatusRail items={viewModel.statusRail} />

            <div className="sv-workbench">
              <section className="sv-center-stack">
                {projectLoading || snapshotLoading ? (
                  <div className="sv-skeleton sv-large">Loading runtime snapshot...</div>
                ) : (
                  <>
                    <SuperVisualCanvasPreview
                      previewRef={viewModel.previewRef}
                      status={viewModel.status}
                      displayPayload={viewModel.displayPayload}
                    />

                    <SuperVisualCompositionPanel
                      displayPayload={viewModel.displayPayload}
                      canLock={viewModel.availableActions.includes("composition.lock")}
                      active={Boolean(activeAction)}
                      onLockComposition={(payload) => runAction("composition.lock", payload)}
                    />

                    <SuperVisualCommandBar
                      disabled={!variantId || Boolean(activeAction)}
                      onSubmitRevision={submitRevision}
                    />
                  </>
                )}
              </section>

              <SuperVisualInspector viewModel={viewModel} onRefresh={refreshAll} />
            </div>

            <SuperVisualEventsTimeline
              events={viewModel.events}
              loading={eventsLoading}
              onRefresh={refreshEvents}
            />
          </>
        )}
      </main>

      <SuperVisualCreateProjectModal
        open={createOpen}
        creating={creating}
        onClose={() => setCreateOpen(false)}
        onCreate={handleCreateProject}
      />
    </div>
  );
}

export default SuperVisualStudio;
