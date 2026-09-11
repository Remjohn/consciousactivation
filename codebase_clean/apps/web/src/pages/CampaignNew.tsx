import { useState, useRef } from "react";
import { useNavigate } from "@tanstack/react-router";
import { useCreateCampaign } from "../hooks/useCreateCampaign";
import { ExistingSourcePanel } from "../components/campaign-new/ExistingSourcePanel";
import { ImportInterviewPanel } from "../components/campaign-new/ImportInterviewPanel";
import { HarnessPicker } from "../components/campaign-new/HarnessPicker";
import { OutputTargetsEditor } from "../components/campaign-new/OutputTargetsEditor";
import { AutonomyModeSelector } from "../components/campaign-new/AutonomyModeSelector";
import { LaunchReview } from "../components/campaign-new/LaunchReview";
import { requireAtLeastOneOutputTarget } from "../lib/campaignFormValidation";
import type { CampaignCreateRequest, HarnessSummary, OutputTarget, AutonomyMode } from "../api/types";

type WizardStep = 1 | 2;

export default function CampaignNew() {
  const navigate = useNavigate();
  const [step, setStep] = useState<WizardStep>(1);
  const [sourcePackageId, setSourcePackageId] = useState<string | null>(null);
  const [selectedHarness, setSelectedHarness] = useState<HarnessSummary | null>(null);
  const [outputTargets, setOutputTargets] = useState<OutputTarget[]>([]);
  const [objective, setObjective] = useState("");
  const [initialSeed, setInitialSeed] = useState("");
  const [tasteDirection, setTasteDirection] = useState<string[]>([]);
  const [budgetUnits, setBudgetUnits] = useState(1);
  const [autonomyMode, setAutonomyMode] = useState<AutonomyMode>("REVIEW_BEFORE_SHIP");
  const [formatProfileId, setFormatProfileId] = useState("");
  const [operatorId, setOperatorId] = useState("");
  const [workspaceId, setWorkspaceId] = useState("");
  const [projectId, setProjectId] = useState("");

  const idempotencyKeyRef = useRef(crypto.randomUUID());
  const createMutation = useCreateCampaign();

  function resetIdempotencyKey() {
    idempotencyKeyRef.current = crypto.randomUUID();
  }

  function handleSourceReady(packageId: string) {
    setSourcePackageId(packageId);
    setStep(2);
    resetIdempotencyKey();
  }

  function handleHarnessSelect(harness: HarnessSummary) {
    setSelectedHarness(harness);
  }

  async function handleLaunch() {
    if (!sourcePackageId || !selectedHarness) return;

    const validationError = requireAtLeastOneOutputTarget(outputTargets.length);
    if (validationError) {
      alert(validationError.message);
      return;
    }

    try {
      const result = await createMutation.mutateAsync({
        idempotency_key: idempotencyKeyRef.current,
        workspace_id: workspaceId,
        project_id: projectId,
        source_package_id: sourcePackageId,
        harness_definition_id: selectedHarness.definition_id,
        category_id: selectedHarness.category_id ?? "",
        format_profile_id: formatProfileId,
        objective,
        initial_seed: initialSeed,
        taste_direction: tasteDirection,
        output_targets: outputTargets,
        budget_units: budgetUnits,
        deadline_utc: null,
        autonomy_mode: autonomyMode,
        operator_id: operatorId,
      });

      if (result.state?.campaign_id) {
        await navigate({ to: "/campaigns/$campaignId", params: { campaignId: result.state.campaign_id } });
      }
    } catch {
      // Error is handled by the mutation
    }
  }

  return (
    <div className="min-h-screen bg-canvas p-8">
      {/* Step indicator */}
      <div className="flex gap-4 mb-8">
        <button
          type="button"
          onClick={() => step === 2 && sourcePackageId && setStep(1)}
          className={`rounded-full px-4 py-2 text-sm font-medium ${
            step === 1 ? "bg-gold text-gold-on" : "border border-border-subtle text-ink-muted"
          }`}
          data-testid="step-1-indicator"
        >
          Step 1: Source
        </button>
        <button
          type="button"
          disabled={!sourcePackageId}
          onClick={() => sourcePackageId && setStep(2)}
          className={`rounded-full px-4 py-2 text-sm font-medium ${
            step === 2 ? "bg-gold text-gold-on" : "border border-border-subtle text-ink-muted disabled:opacity-40"
          }`}
          data-testid="step-2-indicator"
        >
          Step 2: Configure & Launch
        </button>
      </div>

      {step === 1 && (
        <div className="grid grid-cols-2 gap-6">
          <ExistingSourcePanel onReady={handleSourceReady} />
          <ImportInterviewPanel onReady={handleSourceReady} />
        </div>
      )}

      {step === 2 && (
        <div className="space-y-6">
          <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6">
            <h3 className="text-ink-primary text-lg font-semibold mb-4">Select Harness</h3>
            <HarnessPicker onSelect={handleHarnessSelect} selectedId={selectedHarness?.definition_id} />
          </div>

          {selectedHarness && (
            <>
              <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6">
                <h3 className="text-ink-primary text-lg font-semibold mb-4">Output Targets</h3>
                <OutputTargetsEditor targets={outputTargets} onChange={setOutputTargets} />
              </div>

              <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6">
                <h3 className="text-ink-primary text-lg font-semibold mb-4">Autonomy Mode</h3>
                <AutonomyModeSelector value={autonomyMode} onChange={setAutonomyMode} />
              </div>

              <div className="rounded-[var(--radius-card)] border border-border-subtle bg-surface p-6">
                <h3 className="text-ink-primary text-lg font-semibold mb-4">Details</h3>
                <textarea
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                  placeholder="Objective"
                  className="w-full rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
                  rows={3}
                  data-testid="objective-input"
                />
                <textarea
                  value={initialSeed}
                  onChange={(e) => setInitialSeed(e.target.value)}
                  placeholder="Initial Seed"
                  className="mt-3 w-full rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
                  rows={3}
                  data-testid="initial-seed-input"
                />
                <input
                  type="number"
                  value={budgetUnits}
                  onChange={(e) => setBudgetUnits(Math.max(1, parseInt(e.target.value) || 1))}
                  min={1}
                  placeholder="Budget Units"
                  className="mt-3 w-full rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
                  data-testid="budget-input"
                />
                <input
                  type="text"
                  value={formatProfileId}
                  onChange={(e) => setFormatProfileId(e.target.value)}
                  placeholder="Format Profile ID (optional)"
                  className="mt-3 w-full rounded border border-border-subtle bg-surface-raised px-3 py-2 text-sm text-ink-primary placeholder:text-ink-faint"
                  data-testid="format-profile-input"
                />
              </div>

              <LaunchReview
                request={{
                  idempotency_key: idempotencyKeyRef.current,
                  workspace_id: workspaceId,
                  project_id: projectId,
                  source_package_id: sourcePackageId ?? "",
                  harness_definition_id: selectedHarness.definition_id,
                  category_id: selectedHarness.category_id ?? "",
                  format_profile_id: formatProfileId,
                  objective,
                  initial_seed: initialSeed,
                  taste_direction: tasteDirection,
                  output_targets: outputTargets,
                  budget_units: budgetUnits,
                  deadline_utc: null,
                  autonomy_mode: autonomyMode,
                  operator_id: operatorId,
                }}
                harness={selectedHarness}
                onLaunch={handleLaunch}
                isPending={createMutation.isPending}
                error={createMutation.error ? { error_code: createMutation.error.error_code ?? "UNKNOWN", message: createMutation.error.message } : null}
              />
            </>
          )}
        </div>
      )}
    </div>
  );
}
