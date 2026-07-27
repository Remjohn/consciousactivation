# Production-Grade AI Video Editing Engine for an Interview-First Personal Branding Platform

## What the engine should compile

A production-grade interview-first video engine should not behave like a prompt-in, video-out black box. It should compile structured editorial context into a deterministic render program. That recommendation is consistent with both interview-editing research and current controllable video-generation research: **ChunkyEdit** explicitly inserts an intermediate “thematically coherent chunk” layer between transcript and edit, **L-Storyboard** converts shots into a structured language representation for editing tasks, and newer cinematic generation systems such as **STAGE** and **DrawVideo** rely on storyboard- or sketch-anchored intermediate representations because long-form control over composition, layout, and motion breaks down when a single freeform prompt is asked to specify everything at once. citeturn17search3turn10search1turn10search4turn5search16turn10search22

The right core abstraction is therefore a **VideoEditProgram** that is compiled from your structured inputs: `BrandContext`, `InterviewBrief`, `InterviewAssetContract`, `TranscriptBeatMap`, `ExpressionMoments`, `VoiceVisualDNA`, `PrimitiveEvaluations`, `Doctrines`, `AssetPackageSpec`, `SceneTemplates`, and `FormatTargets`. On the render side, Remotion already supports server-side rendering with JSON `inputProps`, timeline primitives, and frame-range rendering, while OpenTimelineIO gives you a standard way to represent clips, timing, tracks, transitions, markers, and metadata without embedding media directly into the timeline file. citeturn25view0turn25view1turn12view0turn12view1

I would compile **two outputs** from the same source context. The first is a **domain-native render contract** for your Python harness and render workers. The second is an **OTIO audit/interchange artifact** for inspection, downstream export, diffing, and operator review. OTIO is particularly useful here because its objects all support namespaced metadata, which is exactly where you can carry interview doctrine, primitive scores, beat IDs, source transcript anchors, brand version IDs, and approval receipts without forcing those concepts into a generic NLE schema. citeturn12view0turn12view1

A minimal internal contract should look like this:

```json
{
  "program_id": "vidprog_001",
  "brand_context_version": "bcv_2026_06_24_a",
  "interview_asset_contract_id": "iac_014",
  "format": "cinematic_story_commentary",
  "target": {
    "aspect_ratio": "9:16",
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "duration_sec": 58
  },
  "transcript_clock": {
    "source_audio_id": "audio_master_002",
    "beats": ["beat_001", "beat_002", "beat_003"]
  },
  "timeline": {
    "scenes": ["scene_001", "scene_002", "scene_003"],
    "tracks": ["video_base", "cutouts", "text", "fx", "music", "voice"]
  },
  "brand": {
    "visual_dna_id": "visual_dna_v7",
    "voice_dna_id": "voice_dna_v3",
    "primitive_profile_id": "primitive_set_v5"
  },
  "providers": {
    "renderer": "remotion",
    "transcription": "openai_whisper_or_whisperx",
    "masking": "sam3",
    "image_gen": ["gpt-image-2", "flux-2", "qwen-image-layered"],
    "post_audio": "ffmpeg"
  },
  "approval": {
    "status": "draft",
    "required_gates": ["primitive_eval", "subtitle_layout_eval", "operator_review"]
  }
}
```

I would map that contract into OTIO with one video stack, one audio stack, markers for transcript beats and operator notes, and metadata namespaces such as `ccp.brand`, `ccp.interview`, `ccp.primitive_eval`, `ccp.source_provenance`, and `ccp.approval`. Because OTIO references media externally rather than embedding it, all actual media paths, image assets, alpha cutouts, and synthesized plates remain versioned assets in object storage while the OTIO document remains a clean editorial manifest. citeturn12view0turn12view1

The engine should also be **transcript-clocked**, not only timeline-clocked. OpenAI’s transcription API can return word- and segment-level timestamps in structured JSON, and WhisperX exists precisely to refine timestamps through forced alignment while pyannote provides speaker diarization. That makes it possible to derive beat-level timing from actual spoken language, rather than only from heuristic scene durations. citeturn21view2turn3search1turn3search2

A base beat object should therefore be first-class:

```json
{
  "beat_id": "beat_014",
  "speaker": "guest",
  "start_ms": 18420,
  "end_ms": 22520,
  "text": "That was the moment I realized I was performing certainty instead of living it.",
  "expression_tags": ["vulnerability", "authority", "reflection"],
  "story_role": "turning_point",
  "emotion_curve": 0.84,
  "visual_candidates": ["guest_closeup", "memory_insert", "quote_hold"],
  "subtitle_weight": "high",
  "reaction_windows": [
    {"start_ms": 20340, "end_ms": 20980, "kind": "pause"}
  ]
}
```

That one decision—treating beats and scenes as compilable data—makes the rest of the engine possible.

## Cinematic Story Commentary

This format should be built like a short documentary scene system, not like an animated caption preset. The visual grammar revolves around **full-screen guest closeups, restrained camera motion, memory-object inserts, atmospheric background plates, archival or still-image cutaways, quote overlays, and cinematic negative space**. For subtitle behavior, the most relevant industry constraint is not “center subtitles at the bottom no matter what,” but “place subtitles where they avoid the lower-third action, faces, mouths, and on-screen text.” Netflix’s style guidance explicitly requires center-justified subtitles at top or bottom, with repositioning to avoid overlap with on-screen text, mouths, faces, and important action. citeturn27view0turn27view1

In practice, that means the **default composition** for a vulnerable or reflective beat is usually a guest closeup occupying roughly 65–85% of the frame height, with either headroom or lateral negative space reserved for emotional subtitles or a brief quote overlay. If the beat contains a memory image, physical object, place reference, or archival noun phrase, the engine should route that beat to a cutaway plate or insert card rather than force everything through talking-head footage. That recommendation is reinforced by transcript-based talking-head editing research: once you start changing speech content or bridging gaps over visible mouth movement, audio-visual mismatch becomes the central failure mode. citeturn17search5turn17search7

The canonical scene types for this format should be:

- **Guest intimacy closeup**
- **Guest medium with negative-space quote**
- **Memory-object insert**
- **Atmospheric plate with voiceover**
- **Archival still montage**
- **Hold-frame emotional pause**
- **Transition dissolve or soft cut aligned to beat boundary**

A format-specific scene contract can look like this:

```json
{
  "scene_id": "scene_csc_002",
  "format": "cinematic_story_commentary",
  "beat_span": ["beat_014", "beat_015"],
  "duration_ms": 6200,
  "scene_template": "guest_closeup_with_memory_insert",
  "composition": {
    "framing": "closeup",
    "subject_anchor": {"x": 0.46, "y": 0.42},
    "headroom_pct": 0.10,
    "negative_space_zone": "lower_left",
    "camera_motion": {
      "type": "push_in",
      "start_scale": 1.00,
      "end_scale": 1.06,
      "easing": "easeInOutSine"
    },
    "subtitle_zone": {
      "preferred": "lower_left_safe",
      "fallback": "upper_center_safe"
    }
  },
  "layers": [
    {"id": "bg_plate", "type": "video", "track": "video_base"},
    {"id": "guest_main", "type": "video", "track": "video_base"},
    {"id": "memory_insert", "type": "image_or_video", "track": "insert"},
    {"id": "quote_overlay", "type": "text", "track": "text"},
    {"id": "subtitles", "type": "caption", "track": "text"},
    {"id": "grain_vignette", "type": "fx", "track": "fx"}
  ],
  "source_provenance": {
    "guest_main": "xes_001:00:18.420-00:22.520",
    "memory_insert": "asset://memory_object/clock_01.png"
  }
}
```

The **layer stack** should be stable across most scenes: base plate, primary subject, optional insert or archival layer, quote overlay, subtitle layer, then mild texture/look effects. The subtitle layer should never be treated as a last-second burn-in after visual design; it needs to be composition-aware because the whole point of documentary framing is that emotional subtitling and negative space are planned together. Netflix’s guideline to avoid clashes with mouths and important lower-third action is especially relevant here because the guest’s face is frequently large in frame. citeturn27view1

For **camera and framing rules**, I would keep motion extremely conservative. Slow push-ins, gentle hold-and-breathe, and rare reframes are acceptable. Fast scale jitter, whip pans, or UI-like motion are usually compositionally wrong for this format. If the engine must switch from closeup to insert, the transition should be beat-driven: noun phrase emergence, emotional pause, or memory reference. Remotion’s `TransitionSeries` is sufficient for most deterministic sequence-to-sequence transitions, while HTML-in-canvas-based transitions should remain optional because client-side HTML-in-canvas is still experimental and limited to supported element/style subsets. citeturn15search0turn15search2turn25view2

For **text and subtitle rules**, I would use one or two lines maximum in the documentary layer unless you are intentionally doing a quote card. That is also aligned with Netflix’s general subtitle guidance, which caps subtitles at two lines and emphasizes readable segmentation and placement. For documentary and unscripted material, Netflix also specifically recommends including first-use speaker identifiers where needed and preserving on-screen identifiers when relevant, which maps well to nameplate/introduction scenes in personal-brand interviews. citeturn27view0turn27view1

For **timing**, subtitles should be beat-derived, but visual scene boundaries should usually lag the transcript by a few frames rather than cutting exactly on every sentence edge. A useful rule is: scene start on beat emphasis; quote overlay in at phrase apex; memory insert after noun phrase or pause; dissolve out on emotional comedown. Where a semantic bridge is synthetic or off-camera, cover it with insert footage or background plates rather than visible mouth footage, since transcript-based talking-head editing literature shows that the audio-visual seam is the hard part. citeturn17search5turn17search7

The **provider split** for this format should be straightforward. Remotion should own final timeline composition, exact frame timing, and server-side rendering. Use `OffthreadVideo` or the newer `@remotion/media` video component when frame-perfect extraction matters; Remotion explicitly documents `OffthreadVideo` as exact-frame extraction outside the browser using FFmpeg, and its video-tag comparison page marks `OffthreadVideo` and `@remotion/media` as frame-perfect alternatives to plain HTML5 video. GPT Image 2 or FLUX should supply atmospheric plates, archival-style stills, and memory-object variants; FLUX’s current documentation emphasizes production-grade generation and editing with strong composition control and multi-reference editing, while GPT Image 2 is positioned for high-quality generation and editing with image inputs. Qwen-Image-Layered is useful when a generated insert must be decomposed into independent RGBA layers for parallax or object-isolated motion. citeturn24view1turn24view2turn22view0turn21view0turn20view0

The **eval gates** should score at least: subtitle-face collision risk, negative-space preservation, source fidelity, transition coherence, face crop safety, emotional beat alignment, archival insert relevance, and primitive compliance. An operator should approve any scene where generated plates, archival stand-ins, or synthetic bridge coverage materially affect meaning.

## Educational and Explainer

This format should not pretend to be cinematic. It should be unapologetically **constructed**. The right visual language is **paper-cut and layered 2D composition**: textured paper backgrounds, cutout avatars, diagram nodes, timeline strips, labels, arrows, rough annotation, teaching panels, metaphor objects, and motion paths that correspond to transcript concepts rather than merely decorating them. Programmatic animation tools support this well: Motion Canvas is built around scenes, tweens, transitions, and an orthographic camera, while Manim is designed for precise explanatory animations with programmable object control. citeturn23view0turn23view1turn23view2turn23view3turn7search2turn7search5

The key composition principle here is **concept-to-object mapping**. Every transcript concept should either become a visual object, a label, a relation, a sequence, or a transformation. If the guest says, “Most people think X causes Y, but actually Z mediates it,” the scene should literally show X, Y, Z, the false arrow being crossed out, and the correct relationship being animated. This is the format where geometry must be far more deterministic than it is in story commentary.

A scene template for explainers should therefore look like this:

```json
{
  "scene_id": "scene_edu_004",
  "format": "educational_explainer",
  "beat_span": ["beat_031", "beat_032"],
  "duration_ms": 7800,
  "scene_template": "paper_cut_causal_reframe",
  "composition": {
    "layout_mode": "three_panel_teaching_board",
    "background": {
      "texture": "paper_fibers_offwhite",
      "depth_layers": 3
    },
    "avatar_slot": {
      "enabled": true,
      "placement": "bottom_right",
      "scale": 0.42
    },
    "diagram_zone": {
      "x": 0.08,
      "y": 0.16,
      "w": 0.72,
      "h": 0.56
    },
    "annotation_slots": ["underline", "arrow", "circle"]
  },
  "layers": [
    {"id": "paper_bg", "type": "paper_texture", "track": "background"},
    {"id": "avatar_cutout", "type": "rgba_cutout", "track": "subject"},
    {"id": "diagram_nodes", "type": "vector_group", "track": "diagram"},
    {"id": "labels", "type": "text_group", "track": "labels"},
    {"id": "rough_annotations", "type": "vector_fx", "track": "fx"},
    {"id": "subtitles", "type": "caption", "track": "text"}
  ],
  "motion_plan": [
    {"target": "node_x", "action": "enter_pop", "at_ms": 200},
    {"target": "wrong_arrow", "action": "draw_then_strike", "at_ms": 1200},
    {"target": "correct_arrow", "action": "path_draw", "at_ms": 2100},
    {"target": "label_z", "action": "slide_in", "at_ms": 2600},
    {"target": "avatar_cutout", "action": "head_nod", "at_ms": 3400}
  ]
}
```

The **layer stack** is typically: paper background, shadowed depth planes, cutout avatar or host figure, diagram primitives, text labels, rough-annotation layer, subtitles, then optional grain/noise. Qwen-Image-Layered is unusually valuable in this format because it can decompose an image into multiple RGBA layers and preserve editability for resize/reposition/recolor operations. That makes it a strong candidate for generating or decomposing metaphor objects, layered teaching plates, or editable paper-cut scenes before deterministic composition takes over. citeturn20view0

I would divide **generation responsibility** sharply. Any scene that is basically geometry—arrows, timelines, nodes, labels, ranking ladders, comparison tables—should be **fully deterministic**, rendered by Remotion plus Skia/canvas primitives or emitted as alpha assets from Motion Canvas or Manim. Any scene that needs a stylized metaphor object, textured paper prop, or collage element can use GPT Image 2 or FLUX upstream. FLUX’s current model family emphasizes image editing and multi-reference control, which is useful when you must hold character identity or brand object language across many explainers; GPT Image 2 is strong when you need promptable edits to existing assets or tightly guided image generation. citeturn22view0turn21view0turn21view1

**Motion Canvas** is particularly suited to this educational layer when the scene is motion-first: it offers scene-based TypeScript animation, tween generators, orthographic camera controls, and built-in transitions. It also exports either image sequences or video via an FFmpeg exporter. **Manim** is the stronger choice when the visuals are math-like, diagrammatic, symbol-dense, or require extremely precise object choreography. In both cases, I would treat them as **sub-scene generators** that emit alpha plates or image sequences, then composite those outputs inside a master Remotion timeline. That keeps one final render spine while letting each specialist engine do what it does best. citeturn23view0turn23view1turn23view2turn23view3turn7search2turn7search5

For **text and subtitle rules**, I would keep subtitles secondary whenever the educational objects already externalize the concept. The label system should do most of the teaching. Subtitles can be reduced, raised, or simplified when the diagram itself carries the semantics, but they still need collision-aware placement and readable segmentation. Netflix’s reading-speed guidance—17 cps for adult English templates, with strong segmentation rules—provides a good upper bound for educational scenes where viewers are also reading labels and looking at diagrams. citeturn27view1

The **timing model** should be transcript-concept-driven, not phrase-by-phrase karaoke. A useful rule is one major visual action per concept turn. If a beat introduces three relationships, the motion plan should stage those relationships sequentially rather than animate everything in parallel. Motion Canvas’ tween model is helpful here because its timing model is explicitly value-progress over a set number of seconds, which maps cleanly to beat windows. citeturn23view3

The **eval gates** for explainers should be different from cinematic commentary: label collision, diagram legibility, object permanence, concept-mapping accuracy, annotation restraint, reading-speed overload, and brand palette compliance. Human approval is especially important when a generated metaphor object could accidentally introduce misleading symbolism.

## Living Commentary Reactions

This format should feel **present, human, and credible**, not overproduced. The right composition is a vertical interview-proof setup with **upper-body cutouts, reaction closeups, eye-line-aware split frames, emotional pause emphasis, quote cards, and subtle room atmosphere**. It is still an interview format, so the engine should treat the human face as the primary source of integrity.

The base composition should usually use one of three shells:

- **Single-commentary frame**: guest or interviewer upper-body cutout over room plate
- **Dual-reaction split**: guest and interviewer or guest and quoted clip
- **Quote interruption card**: a textual or graphic hold that absorbs an emotional pause

Because the framing is human-first, subtitle placement is more fragile than in a diagram scene. Netflix’s subtitle guidance to avoid mouths, faces, and lower-third action matters here even more than in cinematic commentary, especially in vertical crop compositions where faces and hands often occupy the middle and lower portions of frame. citeturn27view1

A canonical scene contract should look like this:

```json
{
  "scene_id": "scene_lcr_003",
  "format": "living_commentary_reactions",
  "beat_span": ["beat_041", "beat_042"],
  "duration_ms": 5400,
  "scene_template": "dual_reaction_vertical_split",
  "composition": {
    "frame_shell": "top_bottom_split",
    "primary_subject": "guest",
    "secondary_subject": "interviewer",
    "eyeline_mode": "matched_inward",
    "pause_emphasis": true,
    "subtitle_zone": {
      "preferred": "center_raised",
      "fallback": "top_center"
    }
  },
  "layers": [
    {"id": "atmosphere_bg", "type": "image_or_video", "track": "background"},
    {"id": "guest_cutout", "type": "video_cutout", "track": "subject_a"},
    {"id": "interviewer_cutout", "type": "video_cutout", "track": "subject_b"},
    {"id": "quote_card", "type": "text_card", "track": "text"},
    {"id": "subtitles", "type": "caption", "track": "text"},
    {"id": "room_fx", "type": "light_fx", "track": "fx"}
  ],
  "reaction_timing": {
    "lead_ms": 120,
    "pause_hold_ms": 380,
    "micro_zoom_on_pause": true
  }
}
```

The critical design variable in this format is **reaction timing from transcript beats**. Reactions should be scheduled not only on speech segments but on **pauses, repetitions, emotional hesitations, disbelief markers, laughter edges, and unfinished clauses**. That is why word/segment timestamps plus speaker diarization are so important. OpenAI’s transcription API can deliver word-level timestamps for edits, while WhisperX and pyannote can refine alignment and speaker identity when you need stronger beat maps for reactions. citeturn21view2turn3search1turn3search2

For the **visual layer stack**, background removal is unavoidable, but I would not treat all masking tools as equal. **SAM 3** is the high-control choice because it is a promptable segmentation model for images and videos that can detect, segment, and track objects from text or visual prompts and handle open-vocabulary concepts across images and videos. That makes it better for tracked subject cutouts, hands, chairs, microphones, props, and multi-frame consistency. **rembg** or similar ONNX-based background-removal tools are useful as a fast fallback for simple stills or low-risk single-subject extractions, but they are not the right backbone for complex tracked human compositions. citeturn19view1turn2search2

For **camera and framing rules**, I would keep crops to upper body or chest-up by default, preserve natural eye line, and only use split frames when both eyes still read naturally toward the center or toward the quoted material. If eye lines fight, the composition feels synthetic immediately. Micro punch-ins are acceptable on emotional landing or reaction pause, but not as constant motion. If a reaction beat needs emphasis, a better move is often a short freeze-hold, subtitle raise, or quote card intercut.

For **text**, quote cards should be sparse and should appear mainly when the reaction beat is semantically dense or deserves a reflective hold. Subtitles should usually be condensed to one or two lines, raised when necessary, and never allowed to hide the face or the lower-frame hands. If the lower third is already busy with hands or quote cards, route subtitles to upper safe zone.

The **provider model** is: Remotion for final composition and timing, SAM 3 for masks and tracked cutouts, GPT Image/FLUX for room atmosphere or background extensions when needed, FFmpeg for final encode and audio mixing, and optionally Qwen-Image-Layered only if a generated background or quote plate needs layer-separated depth motion. The operator should always review mask edges, hair handling, eyeline plausibility, and reaction latency before publish.

The **eval gates** should score: mask bleed, eyeline plausibility, subject scale balance, subtitle collision, reaction latency coherence, emotional authenticity, and primitive compliance. This format especially needs human review because the line between “editorial shaping” and “cheap reaction content” is thin.

## Conscious Reactions Editing

This format is intentionally more synthetic and higher energy, but it still has to be compositionally disciplined. The right architecture is a **two-zone vertical shell**: the **upper frame** carries UI-like editorial argument—polls, rankings, tier lists, debate cards, comments, this-vs-that panels, score states, meme cues—while the **lower frame** carries the human reaction layer with background removal, clean silhouette, and strong eye focus. The goal is not chaos; it is **structured velocity**.

This format maps especially well to platform-native vertical conventions. Remotion’s own Recorder documentation explicitly distinguishes platform conventions such as 1:1 muted-with-captions for some social surfaces, 16:9 for YouTube, and 9:16 for TikTok/Reels/Shorts, with a specific note that bottom safe space is required for short-form vertical and that word-by-word captions are a common expectation. citeturn8search10

A canonical scene contract should have much more UI state than the prior formats:

```json
{
  "scene_id": "scene_cre_007",
  "format": "conscious_reactions_editing",
  "beat_span": ["beat_057", "beat_058", "beat_059"],
  "duration_ms": 4600,
  "scene_template": "upper_ui_lower_human_reaction",
  "composition": {
    "shell": "two_zone_vertical",
    "upper_zone_pct": 0.54,
    "lower_zone_pct": 0.46,
    "human_anchor": {"x": 0.50, "y": 0.79},
    "safe_space_bottom_pct": 0.12,
    "ui_density": "high",
    "reaction_density": "medium"
  },
  "layers": [
    {"id": "ui_bg", "type": "solid_or_pattern", "track": "ui_bg"},
    {"id": "poll_card", "type": "card", "track": "ui"},
    {"id": "ranking_bar", "type": "data_ui", "track": "ui"},
    {"id": "comment_chip", "type": "comment_bubble", "track": "ui"},
    {"id": "score_state", "type": "animated_badge", "track": "ui"},
    {"id": "human_cutout", "type": "video_cutout", "track": "human"},
    {"id": "human_shadow", "type": "shadow_fx", "track": "human_fx"},
    {"id": "caption_words", "type": "kinetic_caption", "track": "text"}
  ],
  "interaction_timing": [
    {"at_ms": 0, "action": "poll_card_in"},
    {"at_ms": 520, "action": "rank_flip"},
    {"at_ms": 980, "action": "comment_pop"},
    {"at_ms": 1420, "action": "punch_in_human"},
    {"at_ms": 1960, "action": "score_badge_change"},
    {"at_ms": 2520, "action": "this_vs_that_swap"}
  ]
}
```

The **upper-frame compositions** should be treated almost like editorial HUD modules. They need to be template-based, not fully generative, because the grammar is repeatable: card header, evidence slot, score badge, pointer arrow, divider, result state. Motion is usually quick but discrete—enter, swap, rank-change, highlight, confirm—rather than continuous float. Remotion’s `TransitionSeries`, custom timings, and deterministic frame-based sequencing are well suited to this because they let you define exact durations and overlay behavior around cut points. Motion Canvas can also be useful when the upper UI needs scene-to-scene custom transition logic or camera-like panel choreography. citeturn15search0turn15search10turn23view2

The **lower human zone** should remain compositionally simple: one clean cutout, maybe one secondary reaction crop, strong shadow separation from background, and safe subtitle handling. The mistake to avoid is letting the upper UI and lower human layer compete equally for attention. In a strong composition, the upper frame carries the argument and the lower frame carries the witness.

For **subtitle rules**, I would typically use word-group or phrase-group kinetic captions in the upper-middle of the lower zone, not at the absolute bottom, because the bottom safe area on short-form platforms and the lower-body crop both create collision risk. Again, the lower safe-space note in Remotion Recorder’s platform guidance is operationally relevant here. citeturn8search10

The **provider model** is similar to living commentary but with more deterministic UI rendering. SAM 3 should still do mask work. Remotion should render the UI modules and master timeline. GPT Image or FLUX can generate reaction backplates, meme-style illustrative panels, or stylized comparison assets, but the cards, rankings, poll containers, and score states should be deterministic vector/canvas components. Qwen-Image-Layered may be useful if you want editable layered meme panels or decomposed sticker-like props. ComfyUI is best used here as a worker/orchestration environment for open-weight generation pipelines, not as the final compositor; its own documentation positions it as a node-based generation/inference engine with local and cloud APIs, custom nodes, and agent connectivity. citeturn19view1turn22view2turn21view0turn22view0turn20view0

The **eval gates** should score: upper/lower zone balance, card legibility under motion, timing density, caption collision, bottom-safe-zone compliance, human-cutout edge quality, meme/graphic relevance, and rhythm fatigue. More than any other format, this one benefits from operator approval on pacing, because a technically valid render can still feel exhausting.

## Runtime stack, determinism, evaluation, and approval

For the **primary render spine**, Remotion is the strongest center of gravity. It has server-side rendering via `@remotion/renderer`, JSON `inputProps`, timeline primitives, a documented path for building timeline-based video editors, frame-perfect video components, deterministic seeded randomness, and a clear distinction between server-side rendering and still-experimental client-side/web rendering. Its docs explicitly warn that client-side rendering cannot capture the full browser viewport and only supports a subset of elements and styles, whereas server-side rendering remains the safer production path. citeturn25view0turn25view1turn24view0turn24view1turn24view2turn24view3turn25view2

For **specialist animation sub-engines**, Motion Canvas and Manim should be used surgically rather than as the master timeline. Motion Canvas is excellent for authored 2D scenes because it is scene-based, supports tween generators, orthographic camera moves, and transition generators, and can export image sequences or finished video with an FFmpeg exporter. But its automation and headless-server story is less clearly documented than Remotion’s, and community issues still surface around headless rendering in server environments. Manim is superb for exact math-like or conceptual animation but is too specialized to be the whole editorial spine. citeturn23view0turn23view1turn23view2turn23view3turn9search9turn7search2turn7search5

For **media plumbing**, FFmpeg remains indispensable even if it is not the engine your operators interact with. Its filtergraph system gives you the final reliable layer for overlays, subtitle burn-in, concatenation, loudness normalization, mixing, sidechain ducking, and terminal encoding. Official docs cover `overlay`, `subtitles`, `amix`, `sidechaincompress`, and `loudnorm`, which are exactly the primitives you need for final finishing. citeturn26view1turn11view3turn11view2turn11view1turn11view0

For **interchange and auditing**, OTIO should be used as the editorial transport and review artifact, not as the live runtime. OTIO’s strengths are its clip/track/transition model, external media references, and metadata namespaces. That makes it perfect for a render receipt or approval package but not sufficient by itself as your branded composition engine. citeturn12view0turn12view1

For **React video editors**, the correct role is UI shell, not truth source. Remotion itself documents how to synchronize a Player with a timeline-based editor, and React video editor frameworks emphasize timeline editing, captions, transitions, and real-time preview. Those are useful capabilities for the operator surface, but they do not replace the need for a deterministic server-side render program, stable scene templates, and provider-specific media workers. citeturn24view0turn6search1turn6search2turn6search8

For **segmentation**, use **SAM 3** when the mask must track a subject or object across frames or when the prompt is semantic, and use **fast background removal** tools only as fallbacks. SAM 3’s official repo describes a unified promptable model for segmentation in images and videos, including text and visual prompts plus tracking. That is categorically different from a quick still-image matte tool like rembg. citeturn19view1turn2search2

For **image assets**, split responsibilities. Use **GPT Image 2** for high-fidelity generation and edits when you want API-native generation, iterative edits, or image-in/image-out workflows. Use **FLUX** when you need strong composition control, multi-reference editing, or open-weight/self-hosted options. Use **Qwen-Image-Layered** when you need decomposition into editable RGBA layers and iterative object-isolated edits. Use **ComfyUI** as the worker and orchestration layer for open models and partner-provider workflows, not as the final authoring truth. citeturn21view0turn21view1turn22view0turn22view1turn20view0turn22view2

For **captions and transcript alignment**, I would use a hybrid stack. OpenAI’s speech-to-text API is very attractive for structured word timestamps because it can emit word- and segment-level timings directly in `verbose_json`, which is enough for many beat-mapped edits. But when you need stronger forced alignment and diarization for reaction formats or multi-speaker interviews, WhisperX plus pyannote remain highly relevant: WhisperX is explicitly built around word-level timestamps and forced alignment, and pyannote is purpose-built for speaker diarization. citeturn21view2turn3search1turn3search2

For **audio finishing**, do not let browser playback rules define the master mix. Final loudness, music weighting, and ducking should be deterministic post-process steps. FFmpeg’s `loudnorm` supports EBU R128 loudness normalization, `sidechaincompress` supports voice-driven ducking against another input, and `amix` supports controlled mixing of multiple floating-point streams. That is sufficient for a stable mastering pass on interviews, beds, stings, and boosted voice inserts. citeturn11view0turn11view1turn11view2

The core rule is this:

**What must be deterministic**
- source trims and transcript anchors  
- scene order and beat boundaries  
- all final line breaks, subtitle positions, and safe-zone decisions  
- camera/framing values after compile  
- card geometry, label positions, arrow paths, paper layers, rankings, scores  
- transition durations and easing curves  
- audio mix coefficients, ducking thresholds, loudness targets  
- brand tokens, fonts, color constants, primitive rules  
- model/version IDs, seeds, asset hashes, approval receipts  
- final render contract and OTIO export

**What can be generative**
- memory plates, archival stand-ins, metaphor objects, room backgrounds  
- layered cutout candidate assets  
- first-pass storyboard candidates  
- paper-cut props and illustrative inserts  
- synthetic bridge coverage plates when doctrine allows  
- optional alternative scene suggestions for operator review

That line is supported by both tooling reality and editing research. Modern systems can generate, edit, or decompose imagery very effectively, but controllable multi-shot and long-form work still performs best when intermediate scene structure is explicit and editor-supervised. citeturn17search3turn10search1turn5search16turn10search22

To guarantee **reproducibility**, I would store every approved render with:
- a full render contract JSON,
- an OTIO manifest,
- media hashes and source time ranges,
- provider model/version IDs,
- deterministic seeds where randomness exists,
- subtitle segmentation snapshot,
- primitive evaluation results,
- and operator approval receipts.

Remotion already supports embedded metadata at render time, deterministic random seeds, and server-side rendering APIs; those should be used as part of the audit trail, not just for rendering. citeturn25view1turn24view3

The **approval workflow** should be hard-gated:

```json
{
  "workflow": [
    "compile_edit_program",
    "render_preview_proxy",
    "run_evals",
    "flag_failures",
    "operator_review",
    "lock_contract",
    "render_final_master",
    "emit_otio_and_receipts"
  ],
  "hard_gates": [
    "source_fidelity_pass",
    "subtitle_layout_pass",
    "format_specific_composition_pass",
    "primitive_compliance_pass",
    "operator_approved"
  ]
}
```

The final engine, then, is not “an AI editor.” It is a **compiler for interview-derived video composition**. The structured context defines meaning. The format templates define visual grammar. The renderer executes a deterministic timeline. Generative providers contribute only where they add material value. And the operator remains the final authority over whether the edit is truthful, on-brand, and compositionally alive.