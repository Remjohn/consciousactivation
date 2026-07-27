# Template Model

A template preview is built from:

```text
TemplateSlotMap
TemplateSamplePayload
TemplatePreviewRequest
TemplatePreviewResult
```

Every preview must preserve:

```text
template_id
template_format
frame_profile
slot labels
sample payload
visual SVG
thumbnail URI
provider/render execution flags set to false
```
