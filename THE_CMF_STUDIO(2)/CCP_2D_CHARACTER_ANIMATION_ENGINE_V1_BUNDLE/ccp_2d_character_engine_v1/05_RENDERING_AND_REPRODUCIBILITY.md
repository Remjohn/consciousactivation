# Rendering and Reproducibility

## 1. Render modes

### Embedded runtime

Character runtime is evaluated directly inside the Remotion render.

Best for:

- simple scenes;
- lower storage overhead;
- exact character/subtitle synchronization;
- reusable character positioning.

### Precomposed RGBA plate

Motion Canvas or the character runtime renders transparent frames or ProRes 4444 before final composition.

Best for:

- complex choreography;
- debugging isolation;
- reusable character plates;
- scenes where the character engine and final compositor must be decoupled.

## 2. Motion Canvas contract

Motion Canvas consumes only:

- approved choreography cues;
- camera cues;
- scene-object cues;
- character placement;
- deterministic easing and seeds.

It cannot select acting states or change transcript meaning.

## 3. Remotion contract

Remotion receives:

- exact duration in frames;
- exact FPS and resolution;
- character render mode;
- scene template;
- subtitles;
- background plates;
- overlays;
- safe-zone profile;
- audio references;
- deterministic seeds.

## 4. FFmpeg finishing

Recommended production sequence:

```text
render video-only master
render or collect voice/music/SFX stems
normalize voice
apply music ducking
mix stems
mux audio and video
verify duration and stream metadata
create preview derivatives
hash all outputs
```

## 5. Canonical reproducibility receipt

Pin:

- program JSON hash;
- every asset hash;
- every sidecar hash;
- character runtime version;
- Motion Canvas version;
- Remotion version;
- FFmpeg build;
- fonts;
- renderer container digests;
- locale and timezone;
- FPS rational;
- audio sample rate;
- random seeds;
- color profile;
- codec settings;
- final command lines.

## 6. Golden tests

Maintain fixtures for:

- neutral rig frame;
- extreme arm bends;
- eye clipping;
- each mouth shape;
- costume switch;
- prop attach/detach;
- warp-deform export;
- paper-material rendering;
- acting-state transitions;
- one end-to-end reference asset.

CI should render selected frames and compare perceptual hashes and structured state snapshots.

## 7. Network isolation

The production renderer should run with no outbound network access. All files must already exist in content-addressed storage or the local render package.
