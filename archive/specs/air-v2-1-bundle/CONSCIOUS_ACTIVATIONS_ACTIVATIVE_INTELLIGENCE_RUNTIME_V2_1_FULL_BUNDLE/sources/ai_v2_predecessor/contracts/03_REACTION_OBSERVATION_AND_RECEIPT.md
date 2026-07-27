# Reaction Observation and Receipt Contracts

## ReactionObservation

Stores one concrete source-linked signal:

- modality;
- timestamp or span;
- observed value;
- source ref;
- confidence in observation;
- optional inferred interpretations.

## ReactionReceipt

Resolves the effect of one Activative Call:

- contract and call refs;
- pre-state;
- observations;
- outcome;
- post-state;
- anchor status;
- interpretation state;
- operator resolution;
- next-action recommendation.

Null reaction is a valid outcome.
