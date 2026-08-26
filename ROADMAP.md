# CARE / Germany Abundance Mission — Build Roadmap

## Mission invariants

**Promise != delivery. Verified receipt = delivery.**

**Likely money != guaranteed pay.**

**A known eligible child must not remain below the protected family floor because the family failed to navigate bureaucracy.**

# Highest priority — two guarantees

## A. Family Guarantee

`Child known → Household resolved → Floor → Gap → Auto pay → Receipt → Correct`

## B. OpenWork

`Need → Fund → Qualify → Contract → Work → Verify → Pay → Employ`

Together:

`Family safe → Useful work → More income → Skills → Regular job → Guarantee tapers smoothly`

---

# 0–72 hours — deterministic proof

### Family Guarantee

- dual floor: max(2026 legal/housing minimum, latest official poverty threshold);
- protected €259 child base in strong CARE mode;
- 35% V0 work keep rate;
- no-clawback-below-floor rule;
- household UI;
- fiscal microsimulation scaffold;
- synthetic household tests;
- income-shock E2E simulator;
- source ledger separating current law from policy proposals.

### OpenWork

- RED/YELLOW/GREEN funding engine;
- binding coverage + payroll liquidity invariant;
- €20+/hour product floor;
- Skill Passport;
- job-transition gate;
- funding registry and Funding Watch;
- worker/funder UI and E2E simulation.

**Ship:** one draft PR containing both guarantee layers. No claim of live public entitlement, live payroll or national fiscal affordability.

---

# Week 1 — Family Guarantee shadow pilot package

Choose one partner category: benefits-advice organisation, family centre, municipality or research/public-interest partner.

Prepare:

1. data-minimised household intake;
2. `CURRENT LAW` calculation trace;
3. `CARE GUARANTEE` calculation trace;
4. automated comparison receipt;
5. missed-entitlement detection;
6. poverty-gap measurement;
7. work-incentive curve;
8. correction/appeal UX;
9. privacy/legal review plan.

Use 50–100 synthetic cases first, then only consented/authorised real cases.

**Ship:** shadow pilot that moves no money but can show exactly where current delivery leaves gaps or bureaucracy.

---

# Week 1 — three real OpenWork needs

Initial mission families:

1. digital support for older Berliners;
2. accessibility/city-data mapping;
3. admin/digitisation support for public-interest organisations.

For each:

- real need owner;
- units/hours/quality definition;
- legal task boundary;
- 10–45 minute training/check where appropriate;
- exact employer/payroll cost at €20+/hour;
- at least three candidate funding routes;
- evidence required to make funding BINDING.

**Ship:** three real YELLOW missions, not fake GREEN jobs.

---

# Week 2 — guarantee infrastructure

## Family Guarantee pilot funding

Before enrolling anyone into a cash top-up pilot:

- define cohort and pilot duration;
- stress maximum liability under job-loss/income-shock cases;
- ring-fence full pilot liability + contingency;
- identify legally suitable paying entity;
- establish bank/payment reconciliation;
- establish no-enrolment rule when reserve would be breached.

A pilot family must not depend on hoped-for donations after enrolment.

## OpenWork payroll guarantee

- employer/payroll partner;
- exact fully loaded employment cost;
- payroll reserve / bridge liquidity;
- commissioner/funder commitment templates;
- double-funding review;
- worker contract/privacy/employment review.

**Ship:** infrastructure able to make one family pilot cohort cash-safe and one OpenWork mission genuinely GREEN.

---

# Week 3–4 — first real transactions

## Family Guarantee top-up pilot

Existing statutory benefits continue through official channels. The pilot pays only the verified incremental CARE gap.

Require:

- signed participant/pilot terms;
- verified household inputs;
- ring-fenced cash;
- deterministic calculation;
- payment receipt;
- incident/retry path;
- correction path;
- measurement of poverty gap before/after.

**Ship:** first real CARE top-up with payment receipt — without pretending federal law has changed.

## OpenWork first GREEN mission

Require:

- binding commissioner commitment;
- subsidy approval if used;
- €20 premium gap funded where necessary;
- training/supervision/admin funded;
- payroll liquidity reserved;
- qualification ready;
- measurable output ready.

**Ship:** first real `PAY GUARANTEED` Berlin mission.

---

# Month 2 — closed-loop pilot

Run households/workers through both systems where suitable:

`family floor → work match → skill check → contract → paid work → more net income → top-up taper → quality evidence → payroll → transition review`

Measure:

- time from risk detection to calculated protection;
- time from confirmed underpayment to payment;
- poverty gap closed;
- missed current-law entitlements;
- household admin minutes/documents;
- earnings-to-disposable-income slope;
- OpenWork time-to-contract;
- qualification completion;
- gross wage / on-time payroll;
- conversion toward regular jobs;
- participant and organisation experience.

**Ship:** CARE Guarantees outcome report with receipts and failures.

---

# Month 2–3 — national Family Guarantee microsimulation

Do not make a national budget claim before this step.

Acquire/use an appropriate representative household microdata source and model:

`current law disposable income`
`→ existing public support by programme`
`→ CARE protected target`
`→ incremental top-up`
`→ household weights`
`→ national gross incremental cost`

Report separately:

- incremental cash cost;
- distribution by income/household type;
- number of children lifted above floor;
- effects of 20/35/50% work keep rates;
- effects of protecting/not protecting Kindergeld;
- administrative savings (not netted into primary cost);
- behavioural scenarios with uncertainty.

**Ship:** reproducible fiscal and distributional model suitable for expert challenge.

---

# Month 3–6 — OpenWork 100 + Family Guarantee cohort

### OpenWork 100

- 100 people into fairly paid work/missions;
- €20/hour gross product floor or higher tariff;
- every mission GREEN before start;
- recurring work reaches transition review.

### Family Guarantee

- expanded consented shadow cohort;
- top-up pilot only within fully reserved liability;
- payment/correction reliability tracked;
- publish poverty gaps and take-up failures found.

### Combined

Test whether households can increase paid work without a benefits cliff.

**Ship:** Berlin institutional pilot proposal with independent review of law, privacy, finance and labour design.

---

# 6–18 months — institutional integration

## Family Guarantee

- align with emerging unified social-benefit system;
- once-only/register architecture;
- automatic Kindergeld integration;
- deterministic entitlement API;
- payment/reconciliation service;
- human exception/appeal service;
- privacy/security/audit model;
- statutory drafting for automatic top-up duty, protected target and work taper.

## OpenWork

- standard workflows with Jobcenters/funders;
- employer/payroll network;
- regulated Pay Guarantee Fund/finance partner;
- identity/work-authorisation;
- portable Skill Passport;
- production funding registry and deadline monitoring.

---

# 2–5 years — national guarantees

1. **Family Guarantee in law:** eligible family protection is an individual statutory entitlement, not a capped discretionary grant.
2. Unified social-benefit calculation/payment layer.
3. National OpenWork mission/funding interoperability standard.
4. Portable evidence-based Skill Passport.
5. Practical pathway toward a fair-work guarantee for able/willing people.
6. Public outcome ledger: poverty gap, payment reliability, work progression, fiscal cost and household abundance.

---

# Long-term scoreboard

The state should be able to answer continuously:

1. How many children are projected below the protected floor?
2. How many remain below it after the state has the information required to act?
3. How much money is missing and why?
4. Did the payment land on time?
5. Did any recovery or administrative change push a good-faith family below the floor?
6. Does every additional euro earned raise household disposable income?
7. What useful work is not being done?
8. Is funding/payroll guaranteed before a worker starts?
9. Did recurring work become a regular job?
10. What is the gross public cost, separately from speculative future savings?
11. Are ordinary households becoming materially more secure and abundant?

Targets:

- **children left below the protected floor after verified eligibility: 0**;
- **GREEN OpenWork missions with unfunded payroll: 0**;
- **income cliffs created by the guarantee formula: 0**.
