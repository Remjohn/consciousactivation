# Asset Intelligence V1 Implementation Order

## Milestone A — Contracts + registries

Add:

```text
src/ccp_studio/contracts/asset_intelligence.py
registries/canonical/asset_intelligence/*
```

Tests:

```text
asset record requires brand_id
asset version requires hash
unknown rights cannot direct-use
```

## Milestone B — Repository + service

Add:

```text
src/ccp_studio/repositories/asset_intelligence.py
src/ccp_studio/services/asset_intelligence_service.py
```

Tests:

```text
asset ingestion
fingerprinting
rights attachment
retrieval gates
reference board gaps
```

## Milestone C — Adapters

Add:

```text
src/ccp_studio/services/asset_intelligence_adapters.py
```

Tests:

```text
micro-semiotic anchor adapter
visual candidate adapter
provider output adapter
```

## Milestone D — Shared skills

Add:

```text
registries/canonical/skills/shared/asset_intelligence/*
```

Tests:

```text
skill manifests exist
skill registry is complete
```

## Milestone E — SuperVisual integration

Update SuperVisualBuilderService to call AssetIntelligenceService for:

```text
retrieve_candidates
build_reference_board
record_usage
```

Keep fake providers until stable.
