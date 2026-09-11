# M0095 Final Assembly Graph and Collision Audit

## Assembly graph

```text
M0079 StoryboardSession/Revision + operator feedback
  -> M0080 format programs (Presentation / Carousel / Video)
    -> M0092 Final-Hit validation + MotionPlan/Keyframe compilation
      -> M0093 downstream Presentation/Carousel runtime projections

M0086–M0089 Asset Research / Visual Chat / Feedback / Candidate Preview
  -> M0091 SuperVisual bounded editor projection
    -> M0095 optional downstream SuperVisual launch slot

M0090 SAM3 TrackingSession
  -> governed tracking/geometry capability
    -> M0095 optional downstream SAM3 launch slot

M0065/M0094 OpenChatCut adapter + human-resolution boundary
  -> native timeline handoff/inspection
    -> M0095 optional downstream OpenChatCut launch slot

Existing CAE API + existing CAE Studio UI
  -> M0095 single loopback control server + nginx gateway
     /api/ -> API, /ws/ -> API WebSocket, / -> Studio UI, /runtime/<id>/ -> enabled downstream runtime
```

## Authority ownership

| Concern | Canonical authority | M0095 treatment |
|---|---|---|
| Semantic meaning and storyboard lineage | M0079 StoryboardRevision and M0080 programs | Consumed through existing API/runtime commands; never re-authored |
| Evidence-first ordering and source provenance | M0086–M0094 governed contracts and receipts | Runtime processes are downstream capability slots only |
| Design System and motion bounds | M0092 Final-Hit validation / existing composition contracts | No new Design System or motion authority |
| Operator state, feedback, promotion | Existing CAE API, Studio bridge, human-resolution and revision paths | Orchestrator owns process lifecycle/health only |
| Native runtime behavior | OpenChatCut/M0093/M0091/M0090 adapters | Reachability observation and routing; runtimes remain replaceable |

## Collision audit

- Exact M0095 destinations were absent before integration; no existing file was overwritten.
- No M0095 destination overlaps M0085–M0094 implementation paths.
- No semantic model, retrieval system, VAE state machine, Design System registry, storyboard authority, or promotion path was duplicated.
- The only shared dependency is intentional: the orchestrator launches and health-checks existing CAE API/UI and downstream adapters through the manifest.
- The broad affected pytest run exposed test-process contamination from `tests/cae/test_m066_human_resolution.py`, which installs a test-only `api.services.campaign_projection` shim in `sys.modules`. The acceptance tests were rerun in isolated pytest processes; no production code or assertions were weakened.

## Runtime limitations

- No COMPONENT_CONTRACT.yaml or separate authority-manifest file was supplied in the M0095 bundle; `manifest.json`, AGENT_HANDOFF.md, the M0095 mandate, and the proven M0079–M0094 paths controlled integration.
- nginx is not installed in the active Windows environment, so `orchestrator.py validate` cannot execute its nginx syntax phase. The M0095 suite covers deterministic nginx rendering and health/topology behavior; no native nginx success is claimed.
- Optional external runtimes remain disabled by default and require operator-supplied commands and health URLs.
