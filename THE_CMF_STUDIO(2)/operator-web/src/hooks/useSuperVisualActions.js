import { useCallback, useState } from "react";
import {
  approveSuperVisualVariant,
  createSuperVisualCompositionHypotheses,
  createSuperVisualProviderBlueprints,
  createSuperVisualRenderContract,
  evaluateSuperVisualVariant,
  exportSuperVisualVariant,
  lockSuperVisualComposition,
  materializeSuperVisual,
  renderSuperVisualVariant,
  runSuperVisualStep,
  startSuperVisualBuildRun,
  submitSuperVisualRevision,
} from "../api/supervisualRuntime";
import { normalizeApiError } from "../lib/apiClient";
import { normalizeRuntimeAction } from "../lib/supervisualViewModel";

export function useSuperVisualActions({ variantId, onAfterAction } = {}) {
  const [activeAction, setActiveAction] = useState(null);
  const [error, setError] = useState(null);
  const [buildRunId, setBuildRunId] = useState(null);

  const after = useCallback(async (result) => {
    if (result?.build_run?.supervisual_build_run_id) {
      setBuildRunId(result.build_run.supervisual_build_run_id);
    } else if (result?.supervisual_build_run_id) {
      setBuildRunId(result.supervisual_build_run_id);
    }
    if (onAfterAction) await onAfterAction(result);
    return result;
  }, [onAfterAction]);

  const runAction = useCallback(async (action, payload = {}) => {
    const resolvedAction = normalizeRuntimeAction(action);
    if (!variantId && resolvedAction !== "noop") return null;
    setActiveAction(resolvedAction);
    setError(null);
    try {
      let result;
      switch (resolvedAction) {
        case "build.start":
          result = await startSuperVisualBuildRun(variantId, payload);
          break;
        case "composition.hypotheses":
          result = await createSuperVisualCompositionHypotheses(variantId, payload);
          break;
        case "composition.lock":
          result = await lockSuperVisualComposition(variantId, payload);
          break;
        case "provider_blueprints.compile":
          result = await createSuperVisualProviderBlueprints(variantId, payload);
          break;
        case "materialize.run":
          result = await materializeSuperVisual(variantId, payload);
          break;
        case "render_contract.compile":
          result = await createSuperVisualRenderContract(variantId, payload);
          break;
        case "render.run":
          result = await renderSuperVisualVariant(variantId, payload);
          break;
        case "eval.run":
          result = await evaluateSuperVisualVariant(variantId, payload);
          break;
        case "variant.approve":
          result = await approveSuperVisualVariant(variantId, payload);
          break;
        case "variant.export":
          result = await exportSuperVisualVariant(variantId, payload);
          break;
        case "revision.apply":
          result = await submitSuperVisualRevision(variantId, payload);
          break;
        default: {
          const runId = payload.build_run_id || buildRunId;
          if (!runId) {
            const started = await startSuperVisualBuildRun(variantId, { requested_steps: [resolvedAction] });
            const startedRunId =
              started?.build_run?.supervisual_build_run_id ||
              started?.supervisual_build_run_id;
            setBuildRunId(startedRunId);
            result = await runSuperVisualStep(startedRunId, resolvedAction, payload);
          } else {
            result = await runSuperVisualStep(runId, resolvedAction, payload);
          }
        }
      }
      return await after(result);
    } catch (err) {
      setError(normalizeApiError(err));
      throw err;
    } finally {
      setActiveAction(null);
    }
  }, [after, buildRunId, variantId]);

  const submitRevision = useCallback((feedback, payload = {}) => {
    return runAction("revision.apply", {
      ...payload,
      feedback,
      operator_feedback: feedback,
    });
  }, [runAction]);

  return {
    activeAction,
    error,
    buildRunId,
    setBuildRunId,
    runAction,
    submitRevision,
  };
}
