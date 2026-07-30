// TS-APP-UI-003 - CampaignDetail page
// Main Control Tower page with tabs and full layout

import { useState } from "react";
import { CampaignHeader } from "../components/control-tower/CampaignHeader";
import { RunProgressGauge } from "../components/control-tower/RunProgressGauge";
import { ActionRail } from "../components/control-tower/ActionRail";
import { ControlTower } from "../components/control-tower/ControlTower";
import { RunGraph } from "../components/control-tower/RunGraph";
import { Timeline } from "../components/control-tower/Timeline";
import { ExceptionQueue } from "../components/control-tower/ExceptionQueue";
import { RevisionComposer } from "../components/control-tower/RevisionComposer";
import { useControlTower } from "../hooks/useControlTower";
import { usePipelineStatus } from "../hooks/usePipelineStatus";
import { useRevisionCompose, useRevisionExecute } from "../hooks/useRevision";
import { useExceptionResolve } from "../hooks/useExceptions";
import { useQueryClient } from "@tanstack/react-query";
import type { ActionContext } from "../lib/actionRegistry";

type TabId = "overview" | "run-graph" | "timeline" | "exceptions" | "revise";

const TABS: { id: TabId; label: string }[] = [
  { id: "overview", label: "Overview" },
  { id: "run-graph", label: "Run Graph" },
  { id: "timeline", label: "Timeline" },
  { id: "exceptions", label: "Exceptions" },
  { id: "revise", label: "Revise" },
];

export function CampaignDetail({ campaignId }: { campaignId: string }) {
  const queryClient = useQueryClient();

  // Tab state
  const [activeTab, setActiveTab] = useState<TabId>("overview");

  // Action context for ActionRail
  const actionContext: ActionContext = {
    setTab: (tab: string) => setActiveTab(tab as TabId),
  };

  // Invalidate handler for WS
  const handleDirty = () => {
    queryClient.invalidateQueries({ queryKey: ["campaign", campaignId] });
  };

  // Fetch tower data
  const towerQuery = useControlTower(campaignId);
  const { connectionState, nodeVisual } = usePipelineStatus(campaignId, { onDirty: handleDirty });

  // Revision mutations
  const compileMutation = useRevisionCompose(campaignId);
  const executeMutation = useRevisionExecute(campaignId);

  // Exception mutation
  const resolveMutation = useExceptionResolve(campaignId);

  // Loading state
  if (towerQuery.isLoading) {
    return (
      <div className="control-tower-page p-8">
        <div className="animate-pulse space-y-4">
          <div className="h-12 w-1/3 rounded bg-ca-surface" />
          <div className="h-64 rounded bg-ca-surface" />
          <div className="h-64 rounded bg-ca-surface" />
        </div>
      </div>
    );
  }

  // Error state
  if (towerQuery.isError) {
    return (
      <div className="control-tower-page p-8">
        <div className="rounded-lg bg-ca-danger/10 p-6 text-center">
          <h2 className="mb-2 text-xl font-semibold text-ca-danger">
            Failed to load campaign
          </h2>
          <p className="text-ca-text-secondary">
            This campaign doesn't exist or you don't have access to it
          </p>
          <button
            onClick={() => window.history.back()}
            className="mt-4 rounded bg-ca-gold-500 px-4 py-2 text-sm font-medium text-white hover:bg-ca-gold-600"
          >
            Back to Campaign List
          </button>
        </div>
      </div>
    );
  }

  const tower = towerQuery.data as any;

  return (
    <div className="control-tower-page p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <CampaignHeader tower={tower} campaignId={campaignId} />

        {/* Hero Section */}
        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
          <RunProgressGauge runNodes={tower.run_nodes ?? []} />
          <div className="lg:col-span-2">
            <ActionRail tower={tower} actionContext={actionContext} />
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mt-6 border-b border-ca-border">
          <nav className="flex gap-4">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`border-b-2 px-4 py-2 text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? "border-ca-gold-500 text-ca-gold-500"
                    : "border-transparent text-ca-text-secondary hover:text-ca-text-primary"
                }`}
              >
                {tab.label}
                {/* Show exception count badge */}
                {tab.id === "exceptions" &&
                  tower.exception_packages?.length > 0 && (
                    <span className="ml-2 rounded-full bg-ca-danger px-2 py-0.5 text-xs text-white">
                      {tower.exception_packages.length}
                    </span>
                  )}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="mt-6">
          {activeTab === "overview" && <ControlTower tower={tower} />}
          {activeTab === "run-graph" && (
            <RunGraph
              runNodes={tower.run_nodes ?? []}
              nodeVisual={nodeVisual}
              connectionState={connectionState}
            />
          )}
          {activeTab === "timeline" && (
            <Timeline campaignId={campaignId} timeline={tower.timeline ?? null} />
          )}
          {activeTab === "exceptions" && (
            <ExceptionQueue
              campaignId={campaignId}
              packages={tower.exception_packages ?? []}
              resolveMutation={resolveMutation}
            />
          )}
          {activeTab === "revise" && (
            <RevisionComposer
              campaignId={campaignId}
              tower={tower}
              compileMutation={compileMutation}
              executeMutation={executeMutation}
            />
          )}
        </div>
      </div>
    </div>
  );
}
