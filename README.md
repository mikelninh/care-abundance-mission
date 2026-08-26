# CARE — Germany Abundance Mission

**Produce more. Make essentials abundant. Give people ownership. Prove that value reached them.**

> **Promise != delivery. Verified receipt = delivery.**

# Highest priority: guarantees + action

CARE treats four failures as one systems problem:

1. people want to contribute but useful work is not converted into funded fair employment;
2. families qualify for support but fragmented rules and delivery can still leave children in poverty;
3. a monthly income floor alone does not guarantee that food is accessible today;
4. people who want to help face fragmented organisations, links and unclear next steps.

The mission is therefore:

> **Protect the floor. Feed people today. Make useful work pay. Make helping simple. Prove what arrived.**

---

## Public action layer — CARE Club Berlin

> **Heute helfen. Heute Hilfe finden.**

[`club/index.html`](club/index.html) is the first public action router. It has only three front doors:

1. **Ich brauche Hilfe** → verified existing Berlin routes;
2. **Ich kann helfen** → direct donation, volunteering, food-rescue and company routes;
3. **Ich will mitbauen** → the guarantee architecture and open-source project.

V0 deliberately stores no sensitive family data. Existing Berliner Tafel / foodsharing activity is shown as existing infrastructure, **never as CARE impact**. CARE direct impact starts at zero and only increments from verified delivery receipts.

Public 24-hour activation board: **Issue #3 — CARE Berlin #001**.

See [`docs/CARE_CLUB_BERLIN.md`](docs/CARE_CLUB_BERLIN.md) and [`data/berlin_action_routes.json`](data/berlin_action_routes.json).

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

Family Guarantee V0 includes interactive household UI, deterministic engine, weighted fiscal microsimulation scaffold, 720 synthetic household stress combinations, income-shock/work/recovery E2E simulation, source registry and Family Safety Watch.

### Funding rule

OpenWork must secure money per mission. The national Family Guarantee must instead become a **statutory entitlement**: an eligible household cannot be told that an internal programme pot is exhausted. Before legislation, a pilot can only enroll households whose maximum pilot liability is covered by a ring-fenced cash reserve.

CARE deliberately does **not** publish a national cost yet. The strong guarantee must first be microsimulated on representative household data, separating current programme spending, incremental cost, administration savings and behavioural scenarios.

---

## Guarantee 3 — CARE Food Guarantee

> **No one should lack adequate food because money, paperwork or a normal payment route failed. Children need 7-day coverage.**

`Cash floor → Daytime meals → Home coverage → Same-day emergency → Delivery → Receipt`

Hard rules:

- cash first; food benefits never replace wages or Family Guarantee;
- school/Kita meals alone are not a 7-day guarantee;
- child coverage includes evenings, weekends and holidays;
- same-day emergency food access exists when normal payment fails;
- accessibility, medically necessary diets and allergies are supported;
- no separate poor-child queue;
- public claim is fail-closed: CARE only calls food access guaranteed when all required routes are actually available.

See [`docs/FOOD_GUARANTEE.md`](docs/FOOD_GUARANTEE.md), [`engine/food_guarantee.py`](engine/food_guarantee.py), [`tests/test_food_guarantee.py`](tests/test_food_guarantee.py) and [`food/index.html`](food/index.html).

---

# One closed loop

`Food access safe`
`→ Family financial floor safe`
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
| **CARE Club Berlin** | Can someone find help, help, or join the build in two clicks today? |
| **OpenWork** | What useful work needs doing, who can do it, and is fair pay guaranteed before start? |
| **Family Guarantee** | Is every known child in a household above the protected floor, and did the top-up land? |
| **Food Guarantee** | Does every eligible person have adequate food access despite money/admin failure? |
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
python -m pytest -q tests/test_care_club_router.py
python openwork/simulate.py
python family/simulate.py
```

Hosted GitHub Actions Run #26 passed on the CARE Club action-router build.

## Next real-world proofs

1. **CARE Berlin #001:** one real action + five activated people + one frontline conversation + one anonymous system gap.
2. **Family Guarantee shadow pilot:** one benefits-advice/municipal partner, current-law vs CARE calculations, no money moved initially.
3. **Food/Family top-up pilot:** ring-fenced incremental fund for a defined cohort; measure food-access gap and poverty gap closed.
4. **OpenWork first GREEN mission:** real need + employer/payroll + binding funding + liquidity + worker + paid result.
5. Join the loops: prove a participating household can stay food-secure and above the floor while moving into paid work without an income cliff.
6. Microsimulate national Family/Food Guarantee fiscal cost before making any affordability claim.

See [`ROADMAP.md`](ROADMAP.md).

**Bake more cake. Give everyone a stake in the bakery. Make sure every child can eat. Show the receipts.**
