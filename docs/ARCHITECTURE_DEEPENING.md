# CARE Architecture Deepening — Verified Evidence Packet

## Problem

The income kernel, statutory projection slices and life-event router each knew parts of the reusable evidence contract. That made evidence validation a shallow cross-cutting concern: every new public-service route risked duplicating or drifting on finite/non-negative checks, boolean/integer semantics, provenance-key integrity and missing/unverified handling.

## Deep module

`engine/evidence_packet.py` is now the admission seam for reusable public-service evidence.

Small interface:

- `EvidencePacket.from_mapping(...)`
- `put(...)`
- `require(...)`
- `value(...)`
- `boolean(...)`
- `integer(...)`
- `is_verified(...)`
- `verified_keys()`

Behavior hidden behind it:

- provenance key matching;
- required source/as-of metadata;
- finite/non-negative numeric validation;
- strict boolean and integer field semantics;
- declared field ranges;
- missing vs unverified distinction;
- deterministic reusable-field enumeration.

## Before

```text
raw dict
 ├─ IncomeKernel validation
 ├─ projection _require/_bool/_amount helpers
 └─ life-event _validate/_verified/_value helpers
```

## After

```text
raw evidence
     ↓
Verified Evidence Packet
     ↓
  small fact interface
  ├─ IncomeKernel
  ├─ statutory projection slices
  └─ life-event routing
```

## Deletion test

Deleting the Evidence Packet would force each downstream rule family to reimplement evidence admission and trust-state logic. That is why the module earns its place.

## Boundary

A structurally valid/verified Evidence Packet is still not a legal entitlement. Projections remain bounded calculations and routes remain prechecks; the competent authority remains the decision maker.
