# CARE — Germany Abundance Mission

**Produce more. Make essentials abundant. Give people ownership. Prove that value reached them.**

> **Promise != delivery. Verified receipt = delivery.**

# Highest priority: three guarantees

CARE now treats three failures as one delivery problem:

1. people want to contribute but useful work is not converted into funded fair employment;
2. families qualify for support but fragmented rules and delivery can still leave children in poverty;
3. income or benefit access can still fail at the exact moment a person needs food.

The mission is therefore:

> **Useful work when you can work. A protected family floor when income is not enough. And no eligible person left without adequate food because money or bureaucracy failed.**

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

> **No child below the protected financial floor.**

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
- source notes, workflows, versioned baselines and Family Safety Watch.

### Funding rule

OpenWork must secure money per mission. The national Family Guarantee must instead become a **statutory entitlement**: an eligible household cannot be told that an internal programme pot is exhausted. Before legislation, a pilot can only enroll households whose maximum pilot liability is covered by a ring-fenced cash reserve.

CARE deliberately does **not** publish a national cost yet. The strong guarantee must first be microsimulated on representative household data, separating current programme spending, incremental cost, administration savings and behavioural scenarios.

---

## Guarantee 3 — CARE Food Guarantee

> **No one goes without adequate food because money, paperwork or a delayed payment failed.**

For children the target is stronger: **daily access, seven days a week** — including evenings, weekends and school holidays.

Hard rules:

- **cash first:** Food Guarantee never replaces the Family Guarantee or wages;
- school/Kita meals alone are not enough — evenings, weekends and holidays must also be covered;
- **same-day emergency access** exists when the normal payment route fails;
- no separate poor-child queue or stigma;
- medically necessary diets/allergies and access barriers must be handled;
- home delivery or equivalent accessible route where shopping is not possible;
- nutrition quality should use evidence-based public standards such as the DGE quality standards;
- CARE only calls the guarantee GREEN when every required access channel is actually available.

V0 includes:

- [`food/index.html`](food/index.html) one-screen guarantee prototype;
- [`engine/food_guarantee.py`](engine/food_guarantee.py) deterministic access-state engine;
- [`tests/test_food_guarantee.py`](tests/test_food_guarantee.py) fail-closed tests;
- [`docs/FOOD_GUARANTEE.md`](docs/FOOD_GUARANTEE.md) operating model and pilot design.

The enforceable claim is intentionally narrower than "nobody will ever feel hunger":

> **No eligible person is left without access to adequate food because they lack money, cannot navigate bureaucracy, or the normal payment system failed.**

---

# One closed loop

`Food secure + Family safe`
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
| **Family Guarantee** | Is every known child in a household above the protected financial floor, and did the top-up land? |
| **Food Guarantee** | Can every eligible person actually access adequate food today, including children outside school hours? |
| **CARE** | What does this person deserve, and did they actually receive it? |
| **Abundance Engine** | How can Germany produce dramatically more real value? |
| **Policy Proof** | What does a proposal mean for a household in euros, duration and funding? |
| **Growth Corridors** | Where can Germany create additional wealth through international cooperation? |

Expanded chain:

`Protect → Feed → Enable → Fund Useful Work → Pay → Deliver → Verify → Grow`

## Run proofs

```bash
python -m pytest -q tests/test_openwork.py
python -m pytest -q tests/test_family_guarantee.py tests/test_family_fiscal_model.py
python -m pytest -q tests/test_food_guarantee.py
python openwork/simulate.py
python family/simulate.py
```

## Next real-world proofs

1. **Family Guarantee shadow pilot:** one benefits-advice/municipal partner, current-law vs CARE calculations, no money moved initially.
2. **Food Guarantee pilot:** map 7-day child food coverage, add same-day emergency route and prove zero uncovered days caused by money/admin failure.
3. **Family Guarantee top-up pilot:** ring-fenced incremental fund for a defined cohort; measure poverty gap closed and payment reliability.
4. **OpenWork first GREEN mission:** real need + employer/payroll + binding funding + liquidity + worker + paid result.
5. Join the loops: prove a participating household can remain food-secure and above the protected floor while moving into paid work without an income cliff.
6. Microsimulate national Family Guarantee and Food Guarantee fiscal cost before making affordability claims.

See [`ROADMAP.md`](ROADMAP.md).

**Bake more cake. Give everyone a stake in the bakery. Make sure every child can eat. Show the receipts.**
