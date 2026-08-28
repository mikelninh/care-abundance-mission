# CARE × OpenProof — authoritative Midnight Proof Receipt consumption

CARE now has two deliberately separate proof paths:

1. `care-local-witness-v0` — integration/leakage test backend;
2. `proof.midnight_receipt` — fail-closed verifier for the authoritative minimum receipt produced by the real OpenProof Compact contract.

## Critical provenance rule

A JSON document does not become authoritative because it contains:

```json
{"source": {"kind": "midnight-indexer"}}
```

The CARE adapter that **actually performed the indexer read** must set the in-process `trusted_indexer_read=True` flag. That flag is not taken from the user payload.

Therefore:

```text
pasted matching receipt
    → MATCHED_UNTRUSTED_SOURCE

CARE-owned indexer read + exact matching receipt
    → VERIFIED_AUTHORITATIVE
```

## Exact fields CARE binds

The family verifier can bind:

- proof type;
- purpose code;
- policy version;
- policy-authorised provider ID;
- exact request binding;
- auxiliary binding (`0` for family);
- verifier challenge hash;
- one-time nullifier.

It also requires source metadata for network, contract address, transaction ID and block height.

## Privacy guard

Family Proof Receipts are rejected if they carry raw/private-looking fields such as income, rent, address, applicant identity, child count, IBAN or arbitrary disclosures.

The receipt remains evidence that a contract predicate passed. It is **not an official entitlement or payment decision**.

## Next production adapter

The remaining integration is transport, not semantics:

```text
CARE request
  → generate challenge + request binding
  → OpenProof prover
  → Midnight transaction
  → CARE-owned indexer query
  → build receipt envelope
  → verify_midnight_family_receipt(..., trusted_indexer_read=True)
  → precheck/routing signal
  → official authority remains authoritative
```

This keeps OpenProof useful without giving the chain, the model or CARE authority they do not have.
