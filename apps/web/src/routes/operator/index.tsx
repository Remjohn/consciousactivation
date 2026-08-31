/**
 * CAE Programs + Artifacts + Chat Operator Application Route.
 * Governed by Phase 1 Mandate M46 (18_PHASE1_PROGRAMS_ARTIFACTS_CHAT_OPERATOR_CONTRACT.md).
 */

import { createFileRoute } from "@tanstack/react-router";
import { ProgramOperatorConsole } from "../../components/operator/ProgramOperatorConsole";

export const Route = createFileRoute("/operator/")({
  component: () => <ProgramOperatorConsole workspaceId="ws-default" />,
});
