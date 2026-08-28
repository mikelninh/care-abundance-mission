# CARE × OpenProof — Family Eligibility Proof MVP

## Goal

Let a family prove that named precheck conditions are satisfied **without sending the receiving workflow the family's raw income, rent, bank details, names or full household record**.

This is deliberately a routing/precheck proof. It does **not** calculate a binding entitlement and it does **not** replace an authority decision.

## Golden synthetic journey

```text
private household evidence
        ↓
local/OpenProof prover
        ↓
resident_country = true
minimum_children = true
income_under_demo_ceiling = true
credential_current = true
        ↓
claims commitment + predicate results
        ↓
CARE verifier
        ↓
continue official check / NEEDS_REVIEW
```

The public proof contains no raw household values by default.

## Current implementation

`proof/openproof_family.py` provides:

- versioned proof purpose and policy ID;
- SHA-256 commitment over the private witness + nonce;
- four explicit predicates;
- zero raw disclosures;
- a fail-closed verifier;
- an immutable authority boundary: `precheck_only_official_decision_remains_official`.

`tests/test_openproof_family.py` checks:

- a positive synthetic household;
- non-disclosure of name, IBAN, rent and raw income;
- income failure -> `NEEDS_REVIEW`;
- purpose mismatch -> reject;
- policy mismatch -> reject.

## Security truth

The current `care-local-witness-v0` backend is **not zero knowledge**. It is an integration/leakage-test backend that evaluates the private witness locally and publishes only the predicate projection.

The production path is:

1. receive official/EUDI/issuer-bound credentials;
2. keep raw credentials local/private;
3. verify issuer binding inside a Midnight Compact circuit;
4. evaluate the versioned CARE predicates in-circuit;
5. disclose only the proof result / necessary selective fields;
6. let the official service make the official decision.

## Why this matters

CARE's existing design says **facts once, coordinated official checks, missing facts stay missing**. OpenProof adds a stronger privacy rule:

> **Facts once. Proofs reused. Minimum disclosure.**

A household should not need to hand every participating service its entire financial and family dossier simply to establish one narrow condition.

## Next Midnight gates

- replace `care-local-witness-v0` with a Midnight-generated proof;
- bind the private household witness to a trusted credential issuer;
- bind each proof to purpose + policy version + expiry + nonce/nullifier;
- prove raw claim values are absent from ledger/indexer-visible state;
- test credential revocation and policy-version rollover;
- shadow-test with benefits advisers before any live authority workflow.
