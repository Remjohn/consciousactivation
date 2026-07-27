# Style Route V1 Object Model

Core objects:

```text
StyleRouteDecisionRequest
StyleRoutePreconditionReport
StyleRouteDecision
StyleRouteSourcePacket
GMGVerbatimNounMap
CACProductionSpec
GMGExpertSelection
GMGProductionSpec
PaperCutArtifactSpec
PaperCutEditorialSpec
RouteProductionSpec
ProviderJobBlueprint
StyleRouteEvaluationReceipt
StyleRouteRepairInstruction
StyleRouteUsageReceipt
```

Core flow:

```text
request → precondition report → decision → source packet → route-specific spec → route production spec → provider blueprint
```

Provider blueprint is not provider execution.
