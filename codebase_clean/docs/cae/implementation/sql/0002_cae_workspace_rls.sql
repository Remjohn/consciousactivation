-- CAE WP-02a staging security scaffold. This migration enables RLS on every
-- CAE table. Direct application writes remain server-only; authenticated users
-- receive only workspace-scoped read grants where a policy is defined.

CREATE OR REPLACE FUNCTION cae.current_auth_subject()
RETURNS text
LANGUAGE sql
STABLE
AS $$
  SELECT NULLIF(current_setting('request.jwt.claim.sub', true), '');
$$;

CREATE OR REPLACE FUNCTION cae.has_workspace_access(target_workspace_id text)
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path = cae, pg_temp
AS $$
  SELECT EXISTS (
    SELECT 1
    FROM cae.actor
    WHERE workspace_id = target_workspace_id
      AND external_subject = cae.current_auth_subject()
  );
$$;

REVOKE ALL ON FUNCTION cae.current_auth_subject() FROM PUBLIC;
REVOKE ALL ON FUNCTION cae.has_workspace_access(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION cae.has_workspace_access(text) TO authenticated;

ALTER TABLE cae.schema_migrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.workspace ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.project ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.actor ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.media_asset ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.source_package ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_session ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.interview_turn ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.evidence_item ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.evidence_span ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.evidence_authentication ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.semantic_assessment ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.assessment_evidence_link ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.semantic_operation ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.command ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.state_aggregate ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.state_transition_contract ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.state_transition ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.event ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.receipt ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_import_run ENABLE ROW LEVEL SECURITY;
ALTER TABLE cae.legacy_import_record ENABLE ROW LEVEL SECURITY;

GRANT USAGE ON SCHEMA cae TO authenticated;
GRANT SELECT ON cae.workspace, cae.project, cae.actor, cae.media_asset,
  cae.source_package, cae.interview_session, cae.interview_turn,
  cae.evidence_item, cae.evidence_span, cae.evidence_authentication,
  cae.semantic_assessment, cae.assessment_evidence_link, cae.state_aggregate,
  cae.command, cae.state_transition, cae.event, cae.receipt TO authenticated;

CREATE POLICY workspace_read ON cae.workspace
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY project_read ON cae.project
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY actor_read ON cae.actor
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY media_asset_read ON cae.media_asset
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY source_package_read ON cae.source_package
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY interview_session_read ON cae.interview_session
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY interview_turn_read ON cae.interview_turn
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.interview_session session
      WHERE session.session_id = interview_turn.session_id
        AND cae.has_workspace_access(session.workspace_id)
    )
  );
CREATE POLICY evidence_item_read ON cae.evidence_item
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY evidence_span_read ON cae.evidence_span
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.evidence_item item
      WHERE item.evidence_id = evidence_span.evidence_id
        AND cae.has_workspace_access(item.workspace_id)
    )
  );
CREATE POLICY evidence_authentication_read ON cae.evidence_authentication
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.evidence_item item
      WHERE item.evidence_id = evidence_authentication.evidence_id
        AND cae.has_workspace_access(item.workspace_id)
    )
  );
CREATE POLICY semantic_assessment_read ON cae.semantic_assessment
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY assessment_evidence_link_read ON cae.assessment_evidence_link
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.semantic_assessment assessment
      WHERE assessment.assessment_id = assessment_evidence_link.assessment_id
        AND assessment.revision = assessment_evidence_link.assessment_revision
        AND cae.has_workspace_access(assessment.workspace_id)
    )
  );
CREATE POLICY state_aggregate_read ON cae.state_aggregate
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY command_read ON cae.command
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY state_transition_read ON cae.state_transition
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.state_aggregate aggregate
      WHERE aggregate.aggregate_id = state_transition.aggregate_id
        AND cae.has_workspace_access(aggregate.workspace_id)
    )
  );
CREATE POLICY event_read ON cae.event
  FOR SELECT TO authenticated
  USING (cae.has_workspace_access(workspace_id));
CREATE POLICY receipt_read ON cae.receipt
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM cae.command command
      WHERE command.command_id = receipt.command_id
        AND cae.has_workspace_access(command.workspace_id)
    )
  );
