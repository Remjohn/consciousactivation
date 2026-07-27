# Narrative Story Doctor → Format Intelligence Bridge V1

## Definition

This bridge converts Narrative Story Doctor extraction packets into `GenericExtractionPacketRef` payloads that Format Intelligence can compile into format-specific realization programs.

It is a thin adapter layer.

It does not own:
- extraction doctrine
- format doctrine
- visual preproduction
- style route decisions
- provider execution
- component-engine execution

## Flow

```text
SuperVisualExtractionPacket
CarouselExtractionPacket
VideoExtractionPacket
Format01StoryExtractionPacket
Format02ExplainerExtractionPacket
Format03ReactionExtractionPacket
Format04ConsciousReactionExtractionPacket
MemeVisualExtractionPacket
PollVisualExtractionPacket
ReactionSeedPacket
        ↓
NarrativeToFormatBridgeService
        ↓
GenericExtractionPacketRef
        ↓
FormatIntelligenceService
        ↓
FormatIntelligenceProgram
        ↓
FormatCommanderVerdict
        ↓
EngineAdapterPayload
```
