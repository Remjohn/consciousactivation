# Acceptance Criteria

- Given a valid evaluated package and exact phase requirements, when assembly runs, then the result contains every mandatory and no unrelated context item.
- Given optional, forbidden, inapplicable, unknown, or missing mandatory context, when assembly runs, then it fails closed with no partial state.
- Given identical governed inputs in fresh services, when assembly repeats, then bytes, identity, and hash are equal.
- Given changed context, package, authority, or contracts, when assembly runs, then a new immutable identity results or invalid input is rejected.
- Given duplicate commands, when payloads match, then the original result is returned; conflicting payloads fail closed.
- Production eligibility and certification remain false.
