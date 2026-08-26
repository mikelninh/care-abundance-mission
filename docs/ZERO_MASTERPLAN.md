# ZERO Deutschland — 365-day national guarantee

**North star:** 0 children with an unresolved income-poverty gap and 0 children missing defined material essentials because the household cannot afford them.

**Clock:** target within **365 days of a parliamentary mandate**. This is an aggressive implementation target, not a forecast of legislative timing.

## 1. The guarantee

ZERO is not a discretionary programme. The policy target is a statutory, enforceable top-up:

```text
ZERO floor for household
- verified disposable household income after taxes and existing transfers
= ZERO top-up (minimum 0)
```

The official EU-SILC poverty-risk line is 60% of median equivalised income. ZERO V1 defaults to **65%** as a safety buffer. The percentage is a policy parameter and must be explicit, versioned and auditable.

A household that is already above the floor receives no ZERO top-up. ZERO never reduces existing income.

### Operational definition of 0%

The annual EU-SILC indicator is sample-based and arrives with a lag. Government therefore needs a faster operational KPI:

> **0 identified children with an unresolved guaranteed-income gap for longer than the service standard.**

The statistical poverty rate remains an independent outcome check and must not be replaced by the operational metric.

## 2. The funding guarantee

A child entitlement must not disappear because a tax forecast misses its target.

ZERO therefore uses two layers:

1. **Dedicated progressive funding:** high-wealth taxation, inheritance-tax reform and any legislated high-income contribution.
2. **Statutory general-revenue backstop:** the federal/Länder budget automatically fills any remaining gap.

Annual appropriation rule:

```text
forecast ZERO cost
+ 20% stabilisation reserve
= required guaranteed funding

required guaranteed funding
- dedicated recurring revenue
= automatic general-revenue backstop
```

If dedicated tax revenue is higher than needed, excess revenue is not automatically spent by ZERO; it returns to the normal budget process or reserve according to law.

### Evidence-backed reference scenarios

These are reference points, not promises of 2026 receipts:

- DIW 2021 long-run modelling of high-wealth taxation / a wealth levy produced annual-equivalent figures of roughly **€13–20bn** depending on allowances. The conservative configuration with a €2m personal allowance and €5m business-asset allowance was around **€13bn/year equivalent**. This needs a fresh 2026 microsimulation before legislation.
- DIW 2026 estimates a **€2.3bn/year** additional inheritance-tax yield for a balanced reform with lifetime allowances and simplified progressive rates.
- A more far-reaching removal of business-transfer privileges with deferral/annuitisation was estimated at **€7.8bn/year** additional revenue in the long run.
- The €2.3bn and €7.8bn inheritance scenarios are **alternatives and must never be added together**.

High-income-tax reform is deliberately **€0 in the default engine** until a source-backed revenue estimate is added.

## 3. 365-day execution plan

### Days 0–14 — Freeze the contract

- Publish ZERO Guarantee Act draft.
- Freeze the operational poverty definition, 65% default buffer, appeal rights and data-minimisation rules.
- Publish open calculation specification and evidence ledger.
- Commission current-year microsimulation for gross/net fiscal cost and behavioural sensitivity.
- Define a national service standard: identification → provisional payment → final reconciliation.

**Exit gate:** every formula and legal dependency is public.

### Days 15–30 — Find every existing entitlement first

- Connect or batch-import, under legal authority, the minimum data needed from tax, family-benefit, basic-support and housing-benefit systems.
- Detect likely missing current-law entitlements.
- Notify households and caseworkers before creating a new ZERO payment.
- Launch public calculator with household-side explanation and source trace.

**Exit gate:** existing benefits are not silently ignored or double-counted.

### Days 31–60 — Payment sandbox

- Run synthetic and consenting-user payment simulations end to end.
- Produce decision trace, payment instruction, reconciliation receipt and appeal route.
- Red-team wrong household composition, stale income, duplicate children, shared custody, recent separation, income shocks and missing data.

**Exit gate:** no payment without a reproducible trace; no denial without an appeal path.

### Days 61–100 — Law + first live jurisdictions

Political target:

- pass the legal entitlement and funding backstop;
- authorise minimum-necessary data matching;
- launch live pilots in high-need municipalities / Länder;
- use safe provisional payments where data are incomplete, with human review for ambiguous cases.

**Exit gate:** real households can receive a legally valid top-up.

### Months 4–6 — Hardest places first

- Expand to high-poverty urban and rural areas.
- Measure uncovered children, median gap, time to payment, appeals, false positives/negatives and administrative effort.
- Publish aggregate municipality-level scoreboard.
- Fix failure modes weekly.

**Exit gate:** operational error and delay are below agreed safety thresholds.

### Months 7–9 — National coverage

- Roll out the same versioned rule contract nationally.
- Add automatic income-change handling and quarterly reconciliation.
- Add material-needs referrals/benefits for housing, school participation, nutrition and digital access.

**Exit gate:** every child is in coverage scope regardless of postcode.

### Months 10–12 — Close every known gap

- Resolve all remaining identified income gaps.
- Run independent audit against EU-SILC / administrative aggregates.
- Publish unresolved-case count and reason codes.
- Trigger automatic operational escalation for any case beyond the service standard.

**Target:** **0 unresolved guaranteed-income gaps**.

## 4. System architecture

```text
Authoritative data / verified household declaration
                     ↓
            Current-law CARE engine
                     ↓
       disposable income after transfers
                     ↓
             ZERO guarantee engine
                     ↓
      top-up + evidence + decision trace
                     ↓
          payment / reconciliation
                     ↓
     aggregate public accountability view
```

### Fail-closed boundaries

- No invented current-law entitlement amount.
- No unversioned poverty threshold.
- No double-counting of inheritance-tax scenarios.
- No dedicated-tax forecast can cap the legal child entitlement.
- No public dashboard contains person-level data.
- No fully automated adverse decision when material data are ambiguous.

## 5. What is built in this branch now

- `engine/zero_engine.py` — deterministic household gap and funding engine.
- `tests/test_zero_engine.py` — core invariants.
- `data/zero_evidence.json` — facts vs study scenarios vs policy assumptions.
- `data/zero_synthetic_households.json` — synthetic demo cases.
- `scripts/zero_demo.py` — reproducible batch demo.
- `zero.html` — public interactive guarantee + funding simulator.
- `.github/workflows/test.yml` — CI test gate.

## 6. What software cannot solve by itself

A production national guarantee still requires:

- legislation and appropriations;
- constitutional/tax-law review;
- refreshed microsimulation using representative microdata;
- data-sharing legal bases and DPIA/security review;
- government identity and payment integrations;
- operational owners in Bund/Länder/Kommunen;
- independent evaluation and appeals.

The prototype's job is to make those dependencies explicit and to remove the excuse that the mechanism is too vague to test.

## 7. Success scoreboard

Public, aggregate and privacy-safe:

- children with unresolved ZERO gap;
- median unresolved gap (€ / month);
- share resolved through existing entitlements vs ZERO top-up;
- median identification-to-payment time;
- benefit take-up rate where measurable;
- appeal rate and reversal rate;
- material-deprivation indicators;
- annual ZERO gross cost, dedicated funding and general-budget backstop;
- coverage reserve ratio;
- source/version freshness.

**One number stays at the top: unresolved children = 0.**
