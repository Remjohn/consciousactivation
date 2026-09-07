/**
 * CAE Programs + Artifacts + Chat Operator Application Route.
 * Governed by Phase 1 Mandate M46 (18_PHASE1_PROGRAMS_ARTIFACTS_CHAT_OPERATOR_CONTRACT.md).
 * CA-M058: workspaceId sourced from WorkspaceContext (not hardcoded).
 */

import { createFileRoute } from "@tanstack/react-router";
import { ProgramOperatorConsole } from "../../components/operator/ProgramOperatorConsole";
import { useWorkspace } from "../../context/WorkspaceContext";

function OperatorRoute() {
  const { activeWorkspaceId } = useWorkspace();
  return <ProgramOperatorConsole workspaceId={activeWorkspaceId ?? ""} />;
}

export const Route = createFileRoute("/operator/")({
  component: OperatorRoute,
});
