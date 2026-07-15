# False-Positive and False-Negative Reporting Contract

Classification: `non_production_readiness_proof`

Every calibration candidate must report confusion counts and reviewed case IDs overall and by profile slice. Required slices include accepted, borderline, wrong visible action, identity drift, composition failure, technical defect, recurrence, wrong-reading lock, Feature Contract, no-text and repairability.

For each dimension and non-compensable gate, report `true_positive`, `true_negative`, `false_positive`, `false_negative`, `abstain`, and `not_applicable`; include evaluator/program pins, corpus digest, case-list digest, annotation version, uncertainty policy and reviewer/arbitration references.

A false negative means the evaluator allowed a labeled failure. Critical false negatives for lineage, wrong-reading locks, identity, Feature Contracts, activation direction, viewer role or applicable no-text survival are reported individually and remain release blockers. False positives are reviewed for unnecessary repair cost, representational skew and recurring slice bias. No error ceiling is set by this proof package.
