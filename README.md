# CARE — Germany Abundance Mission

**Produce more. Make essentials abundant. Give people ownership. Prove that value reached them.**

CARE — **Civic Accountability & Resource Entitlement** — is a public-interest prototype for an abundance-oriented state: grow productive capacity, make public promises executable, and verify that money and resources actually reach people.

> **Promise != delivery. Verified receipt = delivery.**

## What this repository contains

- **CARE household engine** — deterministic, source-backed entitlement calculations.
- **Germany Abundance Mission** — evidence-led growth levers and transparent scenario maths.
- **Policy Proof** — planned household-level comparison of political proposals: who gets what, for how long, at what fiscal cost, with what funding proof.
- **Germany–Vietnam Growth Corridor** — a first international growth corridor matching complementary capabilities, trade, investment and talent.
- **Evidence ledger** — separates `VERIFIED`, `MODELLED`, and `PENDING` claims.
- **Mission agents** — specifications for evidence monitoring, opportunity discovery and mission control.

## V0 status

V0 already includes:

- official 2025 German GDP/population baselines;
- an interactive 1–5 year real-growth scenario calculator;
- an illustrative citizen growth-dividend scenario;
- evidence-backed high-leverage reform areas;
- a canonical Berlin household test case;
- a fail-closed entitlement engine skeleton;
- starter agent specifications;
- a roadmap from prototype to institutional pilot.

### What V0 deliberately refuses to fake

The canonical household is:

- single parent;
- 2 children;
- Berlin;
- €2,000 gross monthly income;
- €1,100 monthly rent.

The current-law entitlement and party-by-party household outcomes remain **PENDING** until deterministic legal rules, source/version traces and tests are implemented.

No verified rule + source + version = **no public euro claim**.

## Four connected products

| Product | Core question |
|---|---|
| **CARE** | What does this person deserve, and did they actually receive it? |
| **Abundance Engine** | How can Germany produce dramatically more real value? |
| **Policy Proof** | What does a political proposal mean for this household in euros, duration and funding? |
| **Growth Corridors** | Where can Germany create additional wealth through international cooperation? |

The end-to-end chain is:

`Produce → Distribute → Deliver → Verify`

## Run locally

Open `index.html` directly in a browser. The V0 front-end has no build step.

Run the engine tests with:

```bash
python -m pytest -q
```

## Build order

1. Implement the current-law Berlin household calculation.
2. Expand to 20–30 high-value German entitlements.
3. Add deterministic calculation traces and regression tests.
4. Add application → decision → payment → reconciliation simulation.
5. Build Policy Proof: TODAY vs proposed policy rules.
6. Add funding-proof calculations and uncertainty.
7. Build the Germany–Vietnam Growth Corridor MVP.
8. Recruit a real benefits-advice/municipal pilot and a trade-corridor pilot.
9. Replace synthetic adapters with real government/data/payment connectors where legally available.

See [`ROADMAP.md`](ROADMAP.md) and [`docs/MISSION.md`](docs/MISSION.md).

## Principle

The goal is not simply a bigger or smaller state. The goal is **greater human possibility, backed by auditable delivery**.

**Bake more cake. Give everyone a stake in the bakery. Show the receipts.**
