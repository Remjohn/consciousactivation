import { canonicalSha256, deterministicId, tokenize, uniqueSorted } from "./canonical.js";
import type { ArtifactRef, ImmutableRef } from "./generated/contracts.js";
import type {
  ChangeRequestProgram,
  ExactChange,
  HumanResolutionEpisode,
  ProgrammingMaterialDispositions,
  ProgrammingMaterialRecord,
  ResolutionScope,
} from "./domain.js";
import { AppendOnlyJsonLedger } from "./store.js";
import { StudioValidationError, validateActor, validateImmutableRef } from "./validators.js";

export interface HumanResolutionInput {
  readonly workspace_id: string;
  readonly project_id: string;
  readonly campaign_id: string;
  readonly run_ref: ImmutableRef;
  readonly harness_ref: ImmutableRef;
  readonly category_id: string;
  readonly format_profile_id: string | "NOT_APPLICABLE";
  readonly resolution_kind: HumanResolutionEpisode["resolution_kind"];
  readonly state_before_ref: ImmutableRef;
  readonly state_after_ref: ImmutableRef;
  readonly artifact_before_refs: ReadonlyArray<ArtifactRef>;
  readonly request_text: string | null;
  readonly program: ChangeRequestProgram | null;
  readonly selected_or_rejected_candidate_refs: ReadonlyArray<ImmutableRef>;
  readonly exact_changes: ReadonlyArray<ExactChange>;
  readonly runtime_and_model_refs: ReadonlyArray<ImmutableRef>;
  readonly retrieved_context_ref: ImmutableRef | null;
  readonly wrong_reading_locks: ReadonlyArray<string>;
  readonly result_refs: ReadonlyArray<ImmutableRef>;
  readonly evaluation_refs: ReadonlyArray<ImmutableRef>;
  readonly accepted: boolean;
  readonly human_authority_actor: HumanResolutionEpisode["human_authority_actor"];
  readonly scope: ResolutionScope;
  readonly recorded_at_utc: string;
}

function dispositions(input: HumanResolutionInput): ProgrammingMaterialDispositions {
  return {
    retrieval_memory: "AUTOMATIC",
    hard_negative: input.accepted ? "NOT_APPLICABLE" : "CANDIDATE",
    supervised_example: "CANDIDATE",
    preference_pair: input.resolution_kind === "candidate_selection" || input.resolution_kind === "rejection" ? "CANDIDATE" : "NOT_APPLICABLE",
    repair_trajectory: input.program && input.program.exact_operations.length > 0 ? "CANDIDATE" : "NOT_APPLICABLE",
    programmed_model_training: "CANDIDATE",
    steering_recipe_evidence: "CANDIDATE",
  };
}

export function createHumanResolutionEpisode(input: HumanResolutionInput): HumanResolutionEpisode {
  validateImmutableRef(input.run_ref, "run_ref");
  validateImmutableRef(input.harness_ref, "harness_ref");
  validateImmutableRef(input.state_before_ref, "state_before_ref");
  validateImmutableRef(input.state_after_ref, "state_after_ref");
  validateActor(input.human_authority_actor);
  if (!input.workspace_id || !input.project_id || !input.campaign_id || !input.category_id) throw new StudioValidationError("RESOLUTION_SCOPE_REQUIRED", "workspace, project, campaign and category are required");
  const programRef: ImmutableRef | null = input.program
    ? { object_id: input.program.program_id, version: "1.0.0", sha256: input.program.program_sha256 }
    : null;
  const body = {
    workspace_id: input.workspace_id,
    project_id: input.project_id,
    campaign_id: input.campaign_id,
    run_ref: input.run_ref,
    harness_ref: input.harness_ref,
    category_id: input.category_id,
    format_profile_id: input.format_profile_id,
    resolution_kind: input.resolution_kind,
    state_before_ref: input.state_before_ref,
    state_after_ref: input.state_after_ref,
    artifact_before_refs: input.artifact_before_refs,
    request_text: input.request_text,
    request_structured_ref: programRef,
    selected_or_rejected_candidate_refs: input.selected_or_rejected_candidate_refs,
    exact_changes: input.exact_changes,
    tool_program_ref: programRef,
    exact_tool_calls: input.program?.exact_operations ?? [],
    runtime_and_model_refs: input.runtime_and_model_refs,
    retrieved_context_ref: input.retrieved_context_ref,
    declared_invariants: input.program?.declared_invariants ?? [],
    required_transformations: input.program?.required_transformations ?? [],
    creative_degrees_of_freedom: input.program?.creative_degrees_of_freedom ?? [],
    wrong_reading_locks: uniqueSorted(input.wrong_reading_locks),
    result_refs: input.result_refs,
    evaluation_refs: input.evaluation_refs,
    accepted: input.accepted,
    human_authority_actor: input.human_authority_actor,
    scope: input.scope,
    programming_material_dispositions: dispositions(input),
    recorded_at_utc: input.recorded_at_utc,
  } as const;
  const episodeId = deterministicId("human-resolution", body);
  const withoutHash = { episode_id: episodeId, ...body };
  return { ...withoutHash, episode_sha256: canonicalSha256(withoutHash) };
}

export class HumanResolutionLedger {
  private readonly ledger: AppendOnlyJsonLedger<HumanResolutionEpisode>;

  constructor(filePath: string) {
    this.ledger = new AppendOnlyJsonLedger<HumanResolutionEpisode>(filePath);
  }

  append(episode: HumanResolutionEpisode): void {
    const withoutHash = { ...episode } as Record<string, unknown>;
    delete withoutHash.episode_sha256;
    if (canonicalSha256(withoutHash) !== episode.episode_sha256) throw new StudioValidationError("EPISODE_HASH_MISMATCH", "HumanResolutionEpisode hash mismatch");
    const existing = this.ledger.readAll().find((entry) => entry.record.episode_id === episode.episode_id);
    if (existing) {
      if (existing.record.episode_sha256 !== episode.episode_sha256) throw new StudioValidationError("EPISODE_ID_COLLISION", "episode ID exists with different bytes");
      return;
    }
    this.ledger.append(episode);
  }

  all(): ReadonlyArray<HumanResolutionEpisode> {
    return this.ledger.readAll().map((entry) => entry.record);
  }

  ledgerSha256(): string | null {
    return this.ledger.fileSha256();
  }
}

function recordFromEpisode(episode: HumanResolutionEpisode): ProgrammingMaterialRecord {
  const text = [
    episode.request_text ?? "",
    episode.category_id,
    episode.resolution_kind,
    ...episode.exact_tool_calls.map((call) => `${call.tool_id} ${call.expected_effect}`),
    ...episode.declared_invariants,
    ...episode.required_transformations,
    ...episode.wrong_reading_locks,
  ].join(" ");
  const episodeRef: ImmutableRef = { object_id: episode.episode_id, version: "1.0.0", sha256: episode.episode_sha256 };
  const body = {
    episode_ref: episodeRef,
    retrieval_tokens: tokenize(text),
    category_id: episode.category_id,
    harness_ref: episode.harness_ref,
    scope: episode.scope,
    accepted: episode.accepted,
    dispositions: episode.programming_material_dispositions,
  } as const;
  return { record_id: deterministicId("programming-material", body), ...body };
}

export class ProgrammingMaterialIndex {
  private readonly records = new Map<string, ProgrammingMaterialRecord>();

  addEpisode(episode: HumanResolutionEpisode): ProgrammingMaterialRecord {
    const record = recordFromEpisode(episode);
    this.records.set(record.record_id, record);
    return record;
  }

  query(query: string, filters: { readonly category_id?: string; readonly accepted?: boolean } = {}): ReadonlyArray<ProgrammingMaterialRecord> {
    const queryTokens = new Set(tokenize(query));
    return [...this.records.values()]
      .filter((record) => filters.category_id === undefined || record.category_id === filters.category_id)
      .filter((record) => filters.accepted === undefined || record.accepted === filters.accepted)
      .map((record) => ({ record, score: record.retrieval_tokens.reduce((score, token) => score + (queryTokens.has(token) ? 1 : 0), 0) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.record.record_id.localeCompare(b.record.record_id))
      .map((item) => item.record);
  }

  all(): ReadonlyArray<ProgrammingMaterialRecord> {
    return [...this.records.values()].sort((a, b) => a.record_id.localeCompare(b.record_id));
  }
}
