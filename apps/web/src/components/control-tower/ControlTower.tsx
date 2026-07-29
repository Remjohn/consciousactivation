// TS-APP-UI-003 - ControlTower component
// Overview panel: source/script refs, knowledge, runtime health, artifacts

import { Badge } from "../ui/Badge";
import type { ControlTowerProjection } from "../../api/campaigns";

interface ControlTowerProps {
  tower: ControlTowerProjection;
}

export function ControlTower({ tower }: ControlTowerProps) {
  const { source_package_ref, final_script_ref, knowledge, runtime_health, artifacts } = tower;

  return (
    <div className="space-y-6">
      {/* Source & Script References */}
      <div className="control-tower-card">
        <div className="control-tower-card-header">
          <span>Source & Script</span>
        </div>
        <dl className="grid grid-cols-2 gap-4">
          {source_package_ref && (
            <div>
              <dt className="text-xs text-ca-text-secondary">Source Package</dt>
              <dd className="mt-1 font-mono text-sm text-ca-text-primary">
                {source_package_ref.object_id}
              </dd>
            </div>
          )}
          {final_script_ref && (
            <div>
              <dt className="text-xs text-ca-text-secondary">Final Script</dt>
              <dd className="mt-1 font-mono text-sm text-ca-text-primary">
                {final_script_ref.object_id}
              </dd>
            </div>
          )}
        </dl>
      </div>

      {/* Knowledge Counts */}
      {knowledge && (
        <div className="control-tower-card">
          <div className="control-tower-card-header">
            <span>Knowledge</span>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-ca-gold-500">
                {knowledge.activations ?? 0}
              </div>
              <div className="text-xs text-ca-text-secondary">Activations</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-ca-gold-500">
                {knowledge.interviews ?? 0}
              </div>
              <div className="text-xs text-ca-text-secondary">Interviews</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-ca-gold-500">
                {knowledge.harnesses ?? 0}
              </div>
              <div className="text-xs text-ca-text-secondary">Harnesses</div>
            </div>
          </div>
        </div>
      )}

      {/* Runtime Health */}
      {runtime_health && runtime_health.length > 0 && (
        <div className="control-tower-card">
          <div className="control-tower-card-header">
            <span>Runtime Health</span>
          </div>
          <div className="space-y-3">
            {runtime_health.map((health: any, idx: number) => (
              <div key={idx} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className={`h-2 w-2 rounded-full ${
                      health.status === "healthy" ? "bg-ca-success" : "bg-ca-danger"
                    }`}
                  />
                  <span className="text-sm text-ca-text-primary">
                    {health.component_id}
                  </span>
                </div>
                <div className="text-xs text-ca-text-secondary">
                  {health.budget_units_used} / {health.budget_units_limit} units
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Artifacts */}
      {artifacts && artifacts.length > 0 && (
        <div className="control-tower-card">
          <div className="control-tower-card-header">
            <span>Artifacts</span>
          </div>
          <div className="space-y-2">
            {artifacts.map((artifact: any, idx: number) => (
              <div
                key={idx}
                className="flex items-center justify-between rounded-lg bg-ca-surface-raised p-3"
              >
                <div className="flex items-center gap-3">
                  <Badge variant="outline">{artifact.media_type}</Badge>
                  <span className="text-sm text-ca-text-primary">
                    {(artifact.bytes / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
                {artifact.uri && (
                  <a
                    href={artifact.uri}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-ca-gold-500 hover:text-ca-gold-600"
                  >
                    Download
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
