# Failure taxonomy

| Code | Condition | Required behavior |
| --- | --- | --- |
| `MISSING_REQUIRED_CONTEXT` | A mandatory context item is absent | Stop before semantic compilation |
| `INVALID_IMMUTABLE_REFERENCE` | A reference lacks identity, version, or hash | Reject the input |
| `AUTHORITY_CONFLICT` | Subordinate instruction contradicts governing authority | Fail closed and identify the conflict |
| `HUMAN_TRUTH_INVENTION` | Output asserts unsupplied human truth or reaction | Reject the output |
| `IDENTITY_DNA_MUTATION` | Output changes or proposes a hidden identity mutation | Reject the output |
| `WRONG_READING_LOCK_MISSING` | No lock governs an applicable semantic branch | Reject the output |
| `APPLICABILITY_UNJUSTIFIED` | Applicability status lacks a reason | Reject the output |
| `LINEAGE_INCOMPLETE` | An output field lacks exact source lineage | Reject the output |
| `EXTERNAL_EXECUTION_REQUESTED` | Input asks the skill to run another product | Reject the request |
| `UNSUPPORTED_READINESS_CLAIM` | Output claims production or certification authority | Reject the output |
