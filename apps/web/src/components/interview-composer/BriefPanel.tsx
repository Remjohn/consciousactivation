import { useState } from "react";
import { useComposeBrief } from "../../hooks/useComposeBrief";
import type { ComposeBriefInput, PlannedQuestionInput } from "../../api/interviewComposer";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";

interface BriefPanelProps {
  researchPackageId: string;
  onReady: (briefId: string) => void;
}

function PlannedQuestionRow({
  q, index, onChange, onRemove,
}: {
  q: PlannedQuestionInput;
  index: number;
  onChange: (q: PlannedQuestionInput) => void;
  onRemove: () => void;
}) {
  return (
    <div className="space-y-2 rounded border border-border p-3" data-testid={`planned-question-${index}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-muted-foreground">Question {index + 1}</span>
        <button type="button" onClick={onRemove} className="text-xs text-red-500" data-testid={`remove-question-${index}`}>Remove</button>
      </div>
      <input
        type="text" value={q.question_text} onChange={(e) => onChange({ ...q, question_text: e.target.value })}
        placeholder="Question text" required
        className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
        data-testid={`question-text-${index}`}
      />
      <input
        type="text" value={q.activation_direction} onChange={(e) => onChange({ ...q, activation_direction: e.target.value })}
        placeholder="Activation direction" required
        className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
        data-testid={`activation-direction-${index}`}
      />
      <input
        type="text" value={q.psychological_role} onChange={(e) => onChange({ ...q, psychological_role: e.target.value })}
        placeholder="Psychological role" required
        className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
        data-testid={`psychological-role-${index}`}
      />
    </div>
  );
}

export function BriefPanel({ researchPackageId, onReady }: BriefPanelProps) {
  const [guestName, setGuestName] = useState("");
  const [tensionHypothesis, setTensionHypothesis] = useState("");
  const [expressionTargets, setExpressionTargets] = useState("");
  const [brandContextRef, setBrandContextRef] = useState("");
  const [voiceDnaRef, setVoiceDnaRef] = useState("");
  const [matrixSeed, setMatrixSeed] = useState({
    psychological_role: "", tension: "", activation_direction_set: "",
    pressure_path: "", stance: "", counteractivation_strategy: "", smallest_commitment: "",
  });
  const [plannedQuestions, setPlannedQuestions] = useState<PlannedQuestionInput[]>([]);
  const [operatorId, setOperatorId] = useState("");
  const [authorityScope, setAuthorityScope] = useState("");
  const [assertionId, setAssertionId] = useState("");

  const mutation = useComposeBrief();

  function addQuestion() {
    setPlannedQuestions((prev) => [...prev, { question_text: "", activation_direction: "", psychological_role: "" }]);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const input: ComposeBriefInput = {
      research_package_id: researchPackageId,
      brand_context_ref: brandContextRef ? JSON.parse(brandContextRef) : undefined,
      voice_dna_ref: voiceDnaRef ? JSON.parse(voiceDnaRef) : undefined,
      guest_name: guestName,
      tension_hypothesis: tensionHypothesis,
      matrix_of_edging_seed: {
        psychological_role: matrixSeed.psychological_role,
        tension: matrixSeed.tension,
        activation_direction_set: matrixSeed.activation_direction_set
          .split(",").map((s) => s.trim()).filter(Boolean),
        pressure_path: matrixSeed.pressure_path,
        stance: matrixSeed.stance,
        counteractivation_strategy: matrixSeed.counteractivation_strategy,
        smallest_commitment: matrixSeed.smallest_commitment,
      },
      planned_questions: plannedQuestions.length > 0 ? plannedQuestions : [],
      expression_targets: expressionTargets
        .split("\n").map((s) => s.trim()).filter(Boolean),
      operator_id: operatorId,
      authority_scope: authorityScope,
      assertion_id: assertionId,
    };
    const result = await mutation.mutateAsync(input);
    onReady(result.brief_id);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4" data-testid="brief-form">
      <div className="flex items-center gap-2">
        <h2 className="text-lg font-semibold text-foreground">Activative Interview Brief</h2>
        <Badge tone="muted">FR-APP-011</Badge>
      </div>

      <input type="text" value={researchPackageId} disabled className="w-full rounded border border-border bg-surface-dimmed px-3 py-2 text-sm text-muted-foreground" data-testid="brief-research-package-id" />

      <input type="text" value={guestName} onChange={(e) => setGuestName(e.target.value)} placeholder="Guest name" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="guest-name-input" />
      <textarea value={tensionHypothesis} onChange={(e) => setTensionHypothesis(e.target.value)} placeholder="Tension hypothesis" required rows={3} className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="tension-hypothesis-input" />
      <textarea value={expressionTargets} onChange={(e) => setExpressionTargets(e.target.value)} placeholder="Expression targets (one per line)" required rows={3} className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="expression-targets-input" />

      <input type="text" value={brandContextRef} onChange={(e) => setBrandContextRef(e.target.value)} placeholder='Brand Context Ref (JSON: {"object_id":"...","version":"...","sha256":"..."})' className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="brand-context-ref-input" />
      <input type="text" value={voiceDnaRef} onChange={(e) => setVoiceDnaRef(e.target.value)} placeholder='Voice DNA Ref (JSON)' className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="voice-dna-ref-input" />

      <div className="space-y-2">
        <h3 className="text-sm font-medium text-foreground">Matrix of Edging Seed</h3>
        {Object.entries(matrixSeed).map(([key, val]) => (
          <textarea
            key={key} value={val} onChange={(e) => setMatrixSeed((prev) => ({ ...prev, [key]: e.target.value }))}
            placeholder={key.replace(/_/g, " ")}
            rows={2}
            className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
            data-testid={`matrix-${key.replace(/_/g, "-")}-input`}
          />
        ))}
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-medium text-foreground">Planned Questions</h3>
          <Button type="button" variant="ghost" onClick={addQuestion} data-testid="add-question-btn">+ Add Question</Button>
        </div>
        {plannedQuestions.map((q, i) => (
          <PlannedQuestionRow key={i} q={q} index={i} onChange={(u) => setPlannedQuestions((prev) => prev.map((p, j) => j === i ? u : p))} onRemove={() => setPlannedQuestions((prev) => prev.filter((_, j) => j !== i))} />
        ))}
      </div>

      <input type="text" value={operatorId} onChange={(e) => setOperatorId(e.target.value)} placeholder="Operator ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="brief-operator-id-input" />
      <input type="text" value={authorityScope} onChange={(e) => setAuthorityScope(e.target.value)} placeholder="Authority Scope" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="brief-authority-scope-input" />
      <input type="text" value={assertionId} onChange={(e) => setAssertionId(e.target.value)} placeholder="Assertion ID" required className="w-full rounded border border-border bg-surface-raised px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground" data-testid="brief-assertion-id-input" />

      {mutation.error && (
        <p className="text-sm text-red-600" data-testid="brief-error">{mutation.error.message}</p>
      )}
      {mutation.data && (
        <p className="text-sm text-green-600" data-testid="brief-success">
          Created: {mutation.data.brief_id}
        </p>
      )}

      <Button type="submit" disabled={mutation.isPending} data-testid="brief-submit-btn">
        {mutation.isPending ? "Creating..." : "Create Brief"}
      </Button>
    </form>
  );
}