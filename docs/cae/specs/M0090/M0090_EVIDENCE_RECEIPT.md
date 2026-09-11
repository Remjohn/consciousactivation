# CAE-M0090 Evidence Receipt — SAM3 TrackingSession

Status: implemented and verified.

## Authority and integration

- The operator-controlled TrackingSession flow is implemented at packages/ca_runtime/src/ca_runtime/tracking_session.py.
- The SAM3 adapter is bounded at engines/intelligence/vision/sam3/adapter.py and records source identity, prompt provenance, confidence, discontinuity evidence, and governed geometry.
- TrackSegment and TrackRevision are immutable revision records; latest-revision and operator-transition guards are fail-closed.
- Accepted geometry projects into existing storyboard/BBOX/OpenChatCut representations without creating a second semantic authority.
- Native SAM3 runtime availability is not claimed; the adapter remains an explicit integration boundary.

## Verification

| Check | Result |
|---|---:|
| Focused M0090 suite: tests/cae/test_m0090_sam3_tracking_session.py | PASS (10/10) |
| Combined M0085–M0091 CAE regression selected for this integration | PASS (88/88) |
| Python compile check for M0090 and M0091 sources/tests | PASS |
| Existing Studio regression: services/studio/tests/*.test.mjs | PASS (20/20) |
| Full apps/web TypeScript check | BLOCKED by unrelated pre-existing repository errors; no M0091-specific errors observed |

The supplied M0090 bundle did not contain a literal COMPONENT_CONTRACT.yaml. Its AGENT_HANDOFF.md, upstream mapping, existing CAE composition/storyboard authorities, and current repository tests were used as the controlling integration inputs.
