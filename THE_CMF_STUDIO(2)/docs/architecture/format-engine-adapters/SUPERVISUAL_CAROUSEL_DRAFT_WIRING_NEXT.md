# Next Wiring Steps

After this patch passes, wire the real engines additively.

## SuperVisual

If present:

```text
src/ccp_studio/services/supervisual_builder_service.py
```

Add:

```python
build_from_format_adapter_input(...)
```

It should delegate to:

```python
SuperVisualFormatDraftWiringService.build_from_format_adapter_input(...)
```

Then later extend from draft state into Visual Preproduction / Asset Intelligence / Style Route.

## Carousel

If present:

```text
src/ccp_studio/services/carousel_engine_service.py
```

Add:

```python
create_variant_from_format_adapter_input(...)
```

It should delegate to:

```python
CarouselFormatDraftWiringService.create_variant_from_format_adapter_input(...)
```

Then later extend from draft variant state into slide planning / visual system / render contract.

## Important

These methods must remain optional and additive. If the exact service file is absent, do not create a fake replacement in this branch.
