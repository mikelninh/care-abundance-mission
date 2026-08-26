# CARE — Germany Abundance Mission

**Produce more. Make essentials abundant. Give people ownership. Prove that value reached them.**

> **Promise != delivery. Verified receipt = delivery.**

# Highest priority: two guarantees

CARE now treats two failures as the same systems problem:

1. people want to contribute but useful work is not converted into funded fair employment;
2. families qualify for support but fragmented rules and delivery can still leave children in poverty.

The mission is therefore:

> **Useful work when you can work. A protected family floor when income is not enough. No bureaucracy should be able to push a child below it.**

---

## Guarantee 1 — OpenWork

> **Work is funded → you can start.**

`Need → Fund → Qualify → Contract → Work → Verify → Pay → Employ`

Hard rules:

- no GREEN/startable mission until 100% of fully loaded employment cost has **binding funding and payroll liquidity**;
- **€20 gross/hour OpenWork Fair Floor or higher applicable tariff** — a product standard, not a current universal legal entitlement;
- `Learn → Check → Prove → Unlock → Paid Work` for non-regulated tasks;
- regulated work still requires the legally necessary credential;
- productive sample work is paid;
- at **120 paid hours or 12 weeks recurring demand**, trigger a job-transition review;
- submitted grant applications are never guaranteed money.

OpenWork V0 includes worker/funder UI, deterministic guarantee engine, funding registry, Skill Passport logic, stakeholder workflows, end-to-end simulator, stress tests and Funding Watch specification.

---

## Guarantee 2 — CARE Family Guarantee

> **No child below the protected floor.**

`Child known → Household resolved → Floor calculated → Gap detected → Auto pay → Receipt → Correct`

### Current 2026 fact that motivates the design

Kindergeld is €259/month per child, but in Grundsicherung it is treated as income when the remaining entitlement is calculated. The CARE strong mode deliberately changes that relationship.

### Proposed CARE rules — not current law

- **protected child base:** €259 Kindergeld per child sits above the Family Guarantee base floor;
- **dual floor:** use the higher of current legal/housing minimum and latest official anti-poverty threshold;
- **automatic top-up:** state calculates the gap instead of requiring the family to choose the correct programme;
- **work always pays:** V0 keeps at least 35% of each additional net earned euro as additional disposable income while top-up remains active;
- **no good-faith clawback into poverty:** recovery may only use resources above the protected target;
- **one-screen explanation:** target, resources, top-up, payment and calculation trace;
- deterministic entitlement maths; AI may assist routing/explanation but cannot set the legal euro amount.

### Family Guarantee V0 includes

- [`family/index.html`](family/index.html) simple interactive household UI;
- [`engine/family_guarantee.py`](engine/family_guarantee.py) deterministic dual-floor/child-base/work-taper engine;
- [`engine/family_fiscal_model.py`](engine/family_fiscal_model.py) weighted fiscal microsimulation scaffold;
- [`tests/test_family_guarantee.py`](tests/test_family_guarantee.py) 720 synthetic household stress cases + invariants;
- [`tests/test_family_fiscal_model.py`](tests/test_family_fiscal_model.py) fiscal-model tests;
- [`family/simulate.py`](family/simulate.py) income-shock/work/recovery end-to-end simulation;
- [`docs/FAMILY_GUARANTEE.md`](docs/FAMILY_GUARANTEE.md) policy and operating model;
- [`docs/FAMILY_GUARANTEE_WORKFLOWS.md`](docs/FAMILY_GUARANTEE_WORKFLOWS.md) citizen/state/funding workflows;
- [`docs/FAMILY_GUARANTEE_SOURCES.md`](docs/FAMILY_GUARANTEE_SOURCES.md) verified facts vs policy choices;
- [`data/family_baselines_2026.json`](data/family_baselines_2026.json) versioned baselines;
- [`agents/family_safety_watch.md`](agents/family_safety_watch.md) family-risk monitoring specification.

### Funding rule

OpenWork must secure money per mission. The national Family Guarantee must instead become a **statutory entitlement**: an eligible household cannot be told that an internal programme pot is exhausted. Before legislation, a pilot can only enroll households whose maximum pilot liability is covered by a ring-fenced cash reserve.

CARE deliberately does **not** publish a national cost yet. The strong guarantee must first be microsimulated on representative household data, separating current programme spending, incremental cost, administration savings and behavioural scenarios.

---

# One closed loop

`Family safe`
`→ useful work available`
`→ fast practical qualification`
`→ €20+/h funded employment`
`→ more net income`
`→ Skill Passport`
`→ regular job`
`→ Family Guarantee tapers smoothly`

**Safety is the floor. Upward mobility is the direction.**

---

## CARE ecosystem

| Product | Core question |
|---|---|
| **OpenWork** | What useful work needs doing, who can do it, and is fair pay guaranteed before start? |
| **Family Guarantee** | Is every known child in a household above the protected floor, and did the top-up land? |
| **CARE** | What does this person deserve, and did they actually receive it? |
| **Abundance Engine** | How can Germany produce dramatically more real value? |
| **Policy Proof** | What does a proposal mean for a household in euros, duration and funding? |
| **Growth Corridors** | Where can Germany create additional wealth through international cooperation? |

Expanded chain:

`Protect → Enable → Fund Useful Work → Pay → Deliver → Verify → Grow`

## Run proofs

```bash
python -m pytest -q tests/test_openwork.py
python -m pytest -q tests/test_family_guarantee.py tests/test_family_fiscal_model.py
python openwork/simulate.py
python family/simulate.py
```

## Next real-world proofs

1. **Family Guarantee shadow pilot:** one benefits-advice/municipal partner, current-law vs CARE calculations, no money moved initially.
2. **Family Guarantee top-up pilot:** ring-fenced incremental fund for a defined cohort; measure poverty gap closed and payment reliability.
3. **OpenWork first GREEN mission:** real need + employer/payroll + binding funding + liquidity + worker + paid result.
4. Join both loops: prove a participating household can move into paid work without an income cliff.
5. Microsimulate national Family Guarantee fiscal cost before making any affordability claim.

See [`ROADMAP.md`](ROADMAP.md).

**Bake more cake. Give everyone a stake in the bakery. Make sure every child can eat. Show the receipts.**
