const fps = 30;
const durationFrames = 1800;

function range(start, end) {
  return {
    start_frame: start,
    end_frame: end,
    start_ms: Math.round((start / fps) * 1000),
    end_ms: Math.round((end / fps) * 1000),
  };
}

function segment(segmentId, laneId, segmentType, label, start, end, extras = {}) {
  return {
    segment_id: segmentId,
    lane_id: laneId,
    segment_type: segmentType,
    label,
    time_range: range(start, end),
    source_refs: extras.source_refs || [],
    primitive_refs: extras.primitive_refs || [],
    receipt_refs: extras.receipt_refs || [],
    blocker_codes: extras.blocker_codes || [],
    locked: Boolean(extras.locked),
    note: extras.note || "",
  };
}

function lane(laneId, displayName, laneKind, editable, segments, extras = {}) {
  return {
    lane_id: laneId,
    display_name: displayName,
    lane_kind: laneKind,
    editable,
    edit_policy_ref: extras.edit_policy_ref || null,
    segments,
  };
}

const commonScope = {
  workbench_id: "wb-2026-06-clntah-001",
  program_id: "vpr-clntah-rrc-002",
  brand_workspace_id: "CE-CLNTAH",
  guest_id: "CLNTAH",
  guest_name: "Claude Ntahuga",
  asset_code: "CE-CLNTAH-S01-MAE-SV-RRC-002-V02",
  fps,
  duration_frames: durationFrames,
  duration_ms: 60000,
  object_version: "vpr-002.17",
  proxy_render_ref: "proxy://cmf/clntah/rrc-002/v02.mp4",
  renderer_props_manifest_ref: "rpm://cmf/clntah/rrc-002/v02",
  renderer_props_hash: "rp_42c8e9_timeline_locked",
  beat_map_ref: "beatmap://cmf/clntah/source-01",
  otio_manifest_ref: "otio://cmf/clntah/rrc-002/v02",
  playback_proxy_status: "ready",
  contract_gate_status: "valid",
  built_at: "2026-06-26T12:00:00Z",
};

const scenes = [
  segment("seg-sc-001", "scene", "scene", "Hook: silence lands", 0, 330, { locked: true }),
  segment("seg-sc-002", "scene", "scene", "Context: why it hurts", 330, 810, { locked: true }),
  segment("seg-sc-003", "scene", "scene", "Reaction: the room absorbs it", 810, 1260, { locked: true }),
  segment("seg-sc-004", "scene", "scene", "Question: what do you call it?", 1260, 1800, { locked: true }),
];

const baseSource = [
  segment("seg-src-001", "source", "source_clip", "Interview A cam", 0, 870, {
    source_refs: ["source://clntah/interview-a-cam"],
    primitive_refs: ["prim.source_truth.specificity", "prim.human_dignity.non_extract", "prim.voice_dna.restraint"],
    receipt_refs: ["00000000-0000-0000-0000-000000001901"],
    locked: true,
  }),
  segment("seg-src-002", "source", "source_clip", "Interview B cam", 870, 1800, {
    source_refs: ["source://clntah/interview-b-cam"],
    primitive_refs: ["prim.source_truth.specificity", "prim.emotional_truth.pause", "prim.delivery_shape.witness"],
    receipt_refs: ["00000000-0000-0000-0000-000000001902"],
    locked: true,
  }),
];

const laneGroups = {
  "SV-CSC": [
    lane("scene", "Scene boundaries", "scene", false, scenes),
    lane("source", "Full-screen guest closeups", "video", false, baseSource),
    lane("memory", "Memory-object inserts", "asset", true, [
      segment("seg-mem-001", "memory", "generated_insert", "Courtyard gate", 210, 430, {
        primitive_refs: ["prim.memory_object.anchor", "prim.cinematic_restraint.negative_space", "prim.source_truth.specificity"],
      }),
      segment("seg-mem-002", "memory", "generated_insert", "Old notebook closeup", 980, 1200, {
        primitive_refs: ["prim.memory_object.anchor", "prim.visual_dna.material", "prim.meaning_transform.witness"],
      }),
    ]),
    lane("caption", "Emotional subtitle lane", "caption", true, [
      segment("seg-cap-001", "caption", "caption", "I entered as a friend...", 80, 360, {
        primitive_refs: ["prim.voice_dna.restraint", "prim.delivery_shape.witness", "prim.emotional_truth.specific"],
      }),
      segment("seg-cap-002", "caption", "caption", "and left as a suspect.", 390, 650, {
        primitive_refs: ["prim.voice_dna.restraint", "prim.delivery_shape.witness", "prim.emotional_truth.specific"],
      }),
    ]),
    lane("camera", "Slow push and negative space", "video", true, [
      segment("seg-cam-001", "camera", "annotation", "Slow push in", 0, 720, {
        primitive_refs: ["prim.cinematic_restraint.pacing", "prim.delivery_shape.quiet_gravity", "prim.visual_dna.negative_space"],
      }),
    ]),
  ],
  "SV-EDU": [
    lane("scene", "Scene boundaries", "scene", false, scenes),
    lane("paper", "Paper texture and boards", "asset", true, [
      segment("seg-paper-001", "paper", "papercut", "Textured paper background", 0, 1800, {
        primitive_refs: ["prim.material_expression.paper_texture", "prim.teaching_clarity.grounding", "prim.visual_dna.handmade"],
      }),
    ]),
    lane("avatar", "2D avatar performance", "animation", true, [
      segment("seg-ava-001", "avatar", "avatar", "Curious eyebrow pose", 130, 420, {
        primitive_refs: ["prim.delivery_shape.teacher_presence", "prim.character_rig.expression", "prim.dignity.warm_authority"],
      }),
      segment("seg-ava-002", "avatar", "avatar", "Open-hand correction", 710, 1080, {
        primitive_refs: ["prim.delivery_shape.teacher_presence", "prim.character_rig.hand_pose", "prim.metaphor_discipline.clear"],
      }),
    ]),
    lane("diagram", "Concept diagram objects", "asset", true, [
      segment("seg-dia-001", "diagram", "generated_insert", "River vs shore diagram", 260, 760, {
        primitive_refs: ["prim.concept_clarity.contrast", "prim.metaphor_discipline.river", "prim.teaching_rhythm.sequence"],
      }),
      segment("seg-dia-002", "diagram", "generated_insert", "Identity bridge card", 960, 1380, {
        primitive_refs: ["prim.concept_clarity.bridge", "prim.metaphor_discipline.boundary", "prim.source_truth.guest_language"],
      }),
    ]),
    lane("rough", "Rough notation and arrows", "animation", true, [
      segment("seg-rgh-001", "rough", "annotation", "Underline: not nostalgia", 820, 980, {
        primitive_refs: ["prim.rough_notation.emphasis", "prim.teaching_clarity.disambiguation", "prim.format_material_expression.hand_drawn"],
      }),
    ]),
  ],
  "SV-FRB": [
    lane("scene", "Scene boundaries", "scene", false, scenes),
    lane("source", "Guest proof footage", "video", false, baseSource),
    lane("claim", "Contradiction cards", "ui", true, [
      segment("seg-claim-001", "claim", "reaction_ui", "Silence protects you", 60, 420, {
        primitive_refs: ["prim.provocation_fit.tension", "prim.context_premise.recognition", "prim.commentability.choice"],
      }),
      segment("seg-claim-002", "claim", "reaction_ui", "Silence betrays you", 450, 840, {
        primitive_refs: ["prim.provocation_fit.tension", "prim.context_premise.recognition", "prim.commentability.choice"],
      }),
    ]),
    lane("punch", "Punch-ins and proof inserts", "video", true, [
      segment("seg-punch-001", "punch", "generated_insert", "Proof receipt flash", 690, 780, {
        primitive_refs: ["prim.source_truth.receipt", "prim.frame_breaker.evidence", "prim.delivery_shape.punch"],
      }),
      segment("seg-punch-002", "punch", "annotation", "Fast push-in", 1210, 1300, {
        primitive_refs: ["prim.delivery_shape.punch", "prim.provocation_fit.escalation", "prim.visual_dna.motion"],
      }),
    ]),
  ],
  "SV-RRC": [
    lane("scene", "Scene boundaries", "scene", false, scenes),
    lane("source", "Interview source clips", "video", false, baseSource),
    lane("reaction_ui", "Upper reaction UI", "ui", true, [
      segment("seg-ui-001", "reaction_ui", "reaction_ui", "Poll: survival or betrayal", 90, 760, {
        primitive_refs: ["prim.context_premise.recognition", "prim.commentability.poll", "prim.human_proof.reaction_prompt"],
      }),
      segment("seg-ui-002", "reaction_ui", "reaction_ui", "Comment card reveal", 1110, 1560, {
        primitive_refs: ["prim.context_premise.recognition", "prim.commentability.comment", "prim.delivery_shape.participation"],
      }),
    ]),
    lane("subjects", "Lower human cutouts", "subject", true, [
      segment("seg-sub-001", "subjects", "subject_cutout", "Guest upper body", 0, 1800, {
        primitive_refs: ["prim.human_proof.face", "prim.dignity.non_extract", "prim.voice_dna.presence"],
      }),
      segment("seg-sub-002", "subjects", "subject_cutout", "Interviewer reaction", 780, 1180, {
        primitive_refs: ["prim.human_proof.interaction", "prim.reaction_timing.pause", "prim.delivery_shape.witness"],
      }),
    ]),
    lane("caption", "Quote and subtitle cards", "caption", true, [
      segment("seg-cap-003", "caption", "caption", "The silence was not empty.", 340, 620, {
        primitive_refs: ["prim.source_truth.exact_phrase", "prim.emotional_truth.pause", "prim.delivery_shape.witness"],
      }),
      segment("seg-cap-004", "caption", "caption", "It was a room full of calculations.", 850, 1160, {
        primitive_refs: ["prim.source_truth.exact_phrase", "prim.emotional_truth.pause", "prim.delivery_shape.witness"],
        blocker_codes: ["BLK-SOURCE-QUOTE-ALIGNMENT"],
      }),
    ]),
  ],
};

function commonLanes(format) {
  const formatLanes = laneGroups[format];
  const supportLanes = [
    lane("audio", "Dialogue waveform proxy", "audio", true, [
      segment("seg-aud-001", "audio", "audio", "Guest audio", 0, 1800, {
        primitive_refs: ["prim.source_truth.audio", "prim.delivery_shape.pause", "prim.voice_dna.cadence"],
      }),
    ]),
    lane("music", "Music and SFX", "audio", true, [
      segment("seg-mus-001", "music", "music", "Low ambient bed", 0, 1440, {
        primitive_refs: ["prim.sonic_prestige.restraint", "prim.cinematic_restraint.pacing", "prim.emotional_truth.support"],
      }),
      segment("seg-sfx-001", "music", "sfx", "Soft hit on question", 1290, 1330, {
        primitive_refs: ["prim.sonic_prestige.soft_hit", "prim.delivery_shape.punctuation", "prim.commentability.turn"],
      }),
    ]),
    lane("eval", "Eval and blocker markers", "eval", false, [
      segment("seg-eval-001", "eval", "eval_marker", "Primitive coverage pass", 0, 760, {
        primitive_refs: ["prim.source_truth.specificity", "prim.human_dignity.non_extract", "prim.delivery_shape.witness"],
      }),
      segment("seg-eval-002", "eval", "eval_marker", "Source quote alignment blocker", 850, 1160, {
        primitive_refs: ["prim.source_truth.exact_phrase"],
        blocker_codes: ["BLK-SOURCE-QUOTE-ALIGNMENT"],
      }),
    ]),
    lane("approval", "Approval and OTIO markers", "approval", false, [
      segment("seg-app-001", "approval", "approval_marker", "OTIO 100% coverage", 0, 1800, {
        primitive_refs: ["prim.verifiable_artifact.otio", "prim.receipt_chain.coverage", "prim.operator_approval.trace"],
      }),
    ]),
  ];

  const diagnostic = Array.from({ length: 30 - formatLanes.length - supportLanes.length }, (_, index) => {
    const laneIndex = index + 1;
    return lane(`diag-${laneIndex}`, `Diagnostic lane ${laneIndex}`, "eval", false, [
      segment(`seg-diag-${laneIndex}`, `diag-${laneIndex}`, "annotation", `Receipt probe ${laneIndex}`, 120 + index * 22, 220 + index * 22, {
        primitive_refs: ["prim.receipt_chain.coverage", "prim.telemetry.surface", "prim.operator_review.trace"],
      }),
    ]);
  });

  return [...formatLanes, ...supportLanes, ...diagnostic];
}

const formatMeta = {
  "SV-CSC": {
    name: "Cinematic Story Commentary",
    role: "Make them feel the story.",
    previewHeadline: "I entered as a friend.",
    previewSubhead: "and left as a suspect.",
    sceneNote: "Documentary closeups, memory objects, slow push-ins, emotional subtitle placement.",
  },
  "SV-EDU": {
    name: "Educational / Explainer",
    role: "Make them understand the idea.",
    previewHeadline: "MYTH 1",
    previewSubhead: "Identity is not nostalgia.",
    sceneNote: "PaperCut boards, 2D avatar poses, diagrams, arrows, rough annotations.",
  },
  "SV-FRB": {
    name: "Challenger / Frame Breaker",
    role: "Make them reconsider the frame.",
    previewHeadline: "WHO IS RIGHT?",
    previewSubhead: "Silence vs survival",
    sceneNote: "Contradiction cards, proof inserts, punch-ins, comment-first framing.",
  },
  "SV-RRC": {
    name: "Reaction / Recognition Clip",
    role: "Make them trust the human moment.",
    previewHeadline: "SILENCE:",
    previewSubhead: "survival or betrayal?",
    sceneNote: "Upper reaction UI, lower guest/interviewer cutouts, emotional pause emphasis.",
  },
};

export const timelineFormatOptions = Object.keys(formatMeta).map((formatSlot) => ({
  formatSlot,
  ...formatMeta[formatSlot],
}));

export function createTimelineWorkbenchFixture(formatSlot = "SV-RRC") {
  const lanes = commonLanes(formatSlot);
  const markers = [
    {
      marker_id: "mrk-primitive-pass-001",
      marker_type: "primitive_pass",
      lane_id: "eval",
      time_range: range(0, 760),
      severity: "info",
      label: "3 primitive roles covered",
      primitive_refs: ["prim.source_truth.specificity", "prim.human_dignity.non_extract", "prim.delivery_shape.witness"],
      receipt_refs: ["00000000-0000-0000-0000-000000001905"],
    },
    {
      marker_id: "mrk-source-block-001",
      marker_type: "eval_blocker",
      lane_id: "caption",
      time_range: range(850, 1160),
      severity: "hard_blocker",
      label: "Source quote alignment required",
      primitive_refs: ["prim.source_truth.exact_phrase"],
      receipt_refs: ["00000000-0000-0000-0000-000000001906"],
      repair_command_type: "request_repair",
    },
  ];

  return {
    schema_version: "cmf.video_timeline_workbench_state.v1",
    ...commonScope,
    format_slot: formatSlot,
    format_meta: formatMeta[formatSlot],
    lanes,
    markers,
    selected_segment_id: lanes[2]?.segments[0]?.segment_id || null,
    hard_blocker_codes: formatSlot === "SV-RRC" ? ["BLK-SOURCE-QUOTE-ALIGNMENT"] : [],
    next_valid_commands: ["request_repair", "rerender_proxy", "export_otio"],
  };
}

