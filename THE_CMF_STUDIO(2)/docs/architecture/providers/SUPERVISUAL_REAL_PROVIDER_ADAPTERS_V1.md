# SuperVisual Real Provider Adapters V1

SuperVisual Real Provider Adapters V1 is the runtime layer that converts typed provider blueprints into provider-specific requests, downloads outputs into owned storage, normalizes receipts, and registers outputs for Asset Intelligence.

The correct flow is:

```text
SuperVisual
→ Visual Preproduction Packet
→ Asset Intelligence Reference Board
→ Style Route Decision
→ Route Production Spec
→ Provider Job Blueprint
→ Provider Adapter
→ Provider Job Receipt
→ Asset Intelligence Variant
→ Deterministic Skia Final Render
→ Eval Receipt
→ Operator Approval
```

Hard laws:

```text
No provider call from freeform chat.
No provider call without ProviderJobBlueprint.
No provider call without brand_context_version_id.
No provider call without idempotency_key.
No paid/live provider call without operator approval or trusted auto-approval policy.
No provider output is treated as the final SuperVisual.
Every provider output is downloaded, hashed, and stored.
Final SuperVisual render remains deterministic.
```
