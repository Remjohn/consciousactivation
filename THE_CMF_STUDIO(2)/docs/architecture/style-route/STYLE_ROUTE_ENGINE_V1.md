# Style Route / CAC / GMG / Paper-Cut Engine V1

Style Route V1 is the shared system that selects, validates, compiles, and evaluates a visual production route for a beat, asset, layer, scene, slide, or SuperVisual.

It sits after Visual Preproduction and Asset Intelligence and before Provider Orchestration and Composition.

Hard laws:

```text
One provider job gets one primary style route.
A composition may contain multiple route-pure layers.
No provider job may average CAC + GMG + Paper-Cut in one prompt.
CAC requires real-life/source reference.
Paper-Cut Artifact requires source object or artifact reference.
Documentary Proof requires proof/document/evidence source.
GMG Expert 03 requires a photo cutout object.
GMG Expert 04 requires document/evidence/archive input.
GMG Expert 06 forbids gold, photo realism, paper texture, and random objects.
Style Route compiles ProviderJobBlueprints but does not execute providers.
```
