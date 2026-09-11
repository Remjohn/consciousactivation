import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { ResearchPanel } from "../../components/interview-composer/ResearchPanel";
import { BriefPanel } from "../../components/interview-composer/BriefPanel";
import { PipelineStatusNotice } from "../../components/interview-composer/PipelineStatusNotice";
import { useCreateComposerSession } from "../../hooks/useCreateComposerSession";
import type { ComposeSessionInput } from "../../api/interviewComposer";
import { Card } from "../../components/ui/Card";
import { Button } from "../../components/ui/Button";

type Step = "research" | "brief" | "session";

export function InterviewsComposePage() {
  const [step, setStep] = useState<Step>("research");
  const [researchPackageId, setResearchPackageId] = useState<string | null>(null);
  const [briefId, setBriefId] = useState<string | null>(null);
  const [operatorId, setOperatorId] = useState("");
  const [authorityScope, setAuthorityScope] = useState("");
  const [assertionId, setAssertionId] = useState("");
  const [recordingDate, setRecordingDate] = useState("");
  const sessionMutation = useCreateComposerSession();

  async function handleSessionCreate() {
    if (!briefId) return;
    const input: ComposeSessionInput = {
      brief_id: briefId,
      recording_date: recordingDate || null,
      operator_id: operatorId,
      authority_scope: authorityScope,
      assertion_id: assertionId,
    };
    await sessionMutation.mutateAsync(input);
    setStep("session");
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6 p-6" data-testid="interviews-compose-page">
      <h1 className="text-2xl font-bold text-foreground">Interview Composer</h1>

      <PipelineStatusNotice />

      <div className="flex items-center gap-2" data-testid="compose-stepper">
        <StepBadge label="Research" active={step === "research"} done={!!researchPackageId} />
        <span className="text-muted-foreground">→</span>
        <StepBadge label="Brief" active={step === "brief"} done={!!briefId} />
        <span className="text-muted-foreground">→</span>
        <StepBadge label="Session" active={step === "session"} done={false} />
      </div>

      {step === "research" && (
        <Card data-testid="research-panel-card">
          <ResearchPanel
            onReady={(id) => {
              setResearchPackageId(id);
              setStep("brief");
            }}
          />
        </Card>
      )}

      {step === "brief" && researchPackageId && (
        <Card data-testid="brief-panel-card">
          <BriefPanel
            researchPackageId={researchPackageId}
            onReady={(id) => {
              setBriefId(id);
              setStep("session");
            }}
          />
        </Card>
      )}

      {step === "session" && briefId && (
        <Card data-testid="session-panel-card">
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-foreground">Create Session</h2>
            <p className="text-sm text-muted-foreground">Research Package: {researchPackageId}</p>
            <p className="text-sm text-muted-foreground">Brief: {briefId}</p>
            <input
              type="text" value={operatorId} onChange={(e) => setOperatorId(e.target.value)}
              placeholder="Operator ID" required
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              data-testid="session-operator-id-input"
            />
            <input
              type="text" value={authorityScope} onChange={(e) => setAuthorityScope(e.target.value)}
              placeholder="Authority Scope" required
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              data-testid="session-authority-scope-input"
            />
            <input
              type="text" value={assertionId} onChange={(e) => setAssertionId(e.target.value)}
              placeholder="Assertion ID" required
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              data-testid="session-assertion-id-input"
            />
            <input
              type="text" value={recordingDate} onChange={(e) => setRecordingDate(e.target.value)}
              placeholder="Recording date (optional)"
              className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              data-testid="session-recording-date-input"
            />
            {sessionMutation.error && (
              <p className="text-sm text-red-600" data-testid="session-error">{sessionMutation.error.message}</p>
            )}
            {sessionMutation.data && (
              <p className="text-sm text-green-600" data-testid="session-success">
                Session created: {sessionMutation.data.session_id}
              </p>
            )}
            <Button onClick={handleSessionCreate} disabled={sessionMutation.isPending} data-testid="session-submit-btn">
              {sessionMutation.isPending ? "Creating..." : "Create Session"}
            </Button>
          </div>
        </Card>
      )}
    </div>
  );
}

function StepBadge({ label, active, done }: { label: string; active: boolean; done: boolean }) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-medium ${
        done ? "bg-green-100 text-green-700" : active ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
      }`}
      data-testid={`stepper-${label.toLowerCase()}`}
    >
      {done ? "✓ " : ""}{label}
    </span>
  );
}

export const Route = createFileRoute("/interviews/compose")({
  component: InterviewsComposePage,
});
