# CARE — Domain Language

Use these terms consistently across rules, journeys, tests and agents.

## Core concepts

- **Evidence Item** — one source-linked fact/value with source, as-of date and verification state.
- **Evidence Packet** — the validated reusable set of Evidence Items admitted once and reused across public-service routes.
- **Projection** — a deterministic calculation slice under one explicit rule version. It is narrower than entitlement.
- **Route** — a recommended next official check produced from the available verified evidence.
- **Life Event** — a change such as income loss that can trigger several coordinated routes from one Evidence Packet.
- **Precheck** — a bounded deterministic gate that identifies whether a full official check should continue and what is still missing.
- **Guarantee** — a CARE policy/product promise with explicit funding/delivery conditions. A proposed CARE Guarantee is not current law unless explicitly stated.
- **Delivery Receipt** — evidence that promised value actually reached the intended destination.
- **Authority Decision** — the binding decision of the legally competent institution. CARE projections and routes never silently become one.
- **Shadow Pilot** — comparison against real/anonymised cases without automated authority action or payment.

## Evidence states

Keep these separate:

- **missing** — the fact is not present;
- **unverified** — a value exists but is not accepted as verified evidence;
- **verified** — the evidence source/provenance state satisfies the current packet contract;
- **invalid** — structurally impossible or contract-breaking evidence; fail closed before routing.

Missing is never converted to zero.

## Route states

`NEEDS_DATA`, `CHECK_NOW`, `CHECK_PARALLEL`, `STANDARD_GATE_NOT_MET`, `MINIMUM_GATE_NOT_MET`, `NOT_APPLICABLE`, and `SAFETY_NET_CHECK` are routing/precheck states. None means approved.

## Invariants

1. Missing is not zero.
2. Unverified is not verified.
3. Projection is not entitlement.
4. Route is not approval.
5. Authority Decision remains external to CARE unless a future authorised adapter explicitly represents it.
6. Delivery claim requires a Delivery Receipt.
7. Reused evidence is validated once at the Evidence Packet seam.
8. Proposed policy must be labelled separately from current law.

## Architecture vocabulary

Use **module**, **interface**, **implementation**, **seam**, **adapter**, **depth**, **leverage** and **locality** when discussing codebase design.
