/**
 * Workspace Management Console Route.
 * Governed by SPEC-TWC-UI-001, FR-APP-001..003, MC-CAE-WS-001, and TS-APP-API-004 §5.
 */

import { createFileRoute } from "@tanstack/react-router";
import { WorkspaceConsole } from "../../components/workspace/WorkspaceConsole";

export const Route = createFileRoute("/workspace/")({
  component: WorkspaceConsole,
});
