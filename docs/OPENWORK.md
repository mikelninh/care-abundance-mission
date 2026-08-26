# OpenWork — Work is funded → you can start

## North star

> Anyone who wants to contribute should be able to contribute — and live well from it.

OpenWork turns unmet public and social needs into **fully funded, fairly paid, skill-building employment**.

The user-facing promise is deliberately simple:

`Need → Fund → Qualify → Contract → Work → Verify → Pay → Employ`

A worker should never need to understand whether the money comes from a Jobcenter subsidy, Berlin co-funding, ESF+, a foundation, a public procurement contract, a company, or several compatible sources. OpenWork handles that complexity behind the scenes.

## Hard product rules

### 1. No green mission without guaranteed pay

A mission can only become `GREEN / STARTABLE` when **100% of the fully loaded employment cost is covered** by binding evidence.

Accepted funding evidence for V1:

- final public grant/subsidy approval;
- signed public/private purchase order or service contract;
- irrevocably reserved employer budget;
- cash already deposited into a ring-fenced payroll account/escrow-like reserve;
- approved bridge facility for reimbursement-based funding.

A verbal promise, submitted grant application, forecast donation, or non-binding expression of interest is never sufficient.

### 2. OpenWork Fair Floor

**€20 gross/hour or the applicable higher collective/tariff wage — whichever is higher.**

This is an OpenWork product standard, not a statement of current German law. Germany's statutory minimum wage is lower. The funding engine must therefore explicitly fund any gap between a subsidy basis and the OpenWork wage.

At 40 hours/week, €20/hour corresponds to about €3,466.67 gross/month and €41,600 gross/year. Net pay is personal and must never be guaranteed by OpenWork because it depends on tax class, insurance, family circumstances and other factors.

### 3. Employment, not gig-work by default

The default delivery model is a real employment relationship:

- employment contract;
- payroll;
- social insurance according to the applicable employment model;
- paid leave and sick-pay rights according to law/contract;
- employer liability and workplace safety;
- transparent working time.

OpenWork should not use task slicing to disguise permanent employment or create pseudo-self-employment.

### 4. Tasks must graduate into jobs

OpenWork tracks recurring demand. A `JOB_TRANSITION_REVIEW` is triggered when either threshold is reached:

- **120 paid hours**, or
- **12 weeks of recurring need**.

The organisation must then choose one of:

1. create a regular part-time role;
2. create a regular full-time role;
3. document a genuine time-limited project reason;
4. close the need because the work is actually finished.

The existing worker gets first consideration for the resulting role where legally and practically possible.

## Fast qualification: Learn → Prove → Do

OpenWork distinguishes **regulated work** from **open-skill work**.

### Regulated work

Medicine, licensed electrical work, regulated care activities and other legally protected work require the legally necessary professional qualification. OpenWork never substitutes a platform badge for a statutory credential.

### Open-skill work

For work where no statutory credential is required, OpenWork uses a practical Skill Passport rather than arbitrary degree filters.

A typical qualification should take 10–45 minutes:

1. **Learn** — a short, accessible micro-module explaining the task, safety, boundaries and examples.
2. **Check** — 3–8 scenario questions focused on real decisions, not trivia.
3. **Prove** — one simulated or supervised sample task.
4. **Unlock** — the relevant Skill Passport badge becomes active.
5. **Start** — first real work is supervised/lightly reviewed until the quality threshold is reached.

Rules:

- productive work must be paid;
- unpaid sample work must not create usable production value for the organisation;
- failed checks lead to another learning path, not permanent rejection;
- language and accessibility variants should be available;
- the passport records demonstrated skills, not prestige credentials.

Examples:

- Digital Helper: account safety, browser basics, explaining without taking over, escalation.
- Document Assistant: classification, privacy, naming rules, quality checks.
- Accessibility Scout: checklist, photo evidence, geotag rules, respectful interaction.
- Community Translator: scope limits, confidentiality, escalation when professional interpreting is required.

## Funding Guarantee Engine

The funding engine operates at **mission level**, not as a vague list of grants.

For every mission it computes:

`FULLY_LOADED_COST = wages + employer payroll costs + paid training + supervision + equipment + insurance/admin + contingency`

V1 uses a conservative configurable employer-cost and contingency buffer. Before real payroll, the exact amount must be replaced by a payroll-provider/employer calculation.

Each funding source has:

- target group eligibility;
- employer eligibility;
- eligible cost categories;
- subsidy basis;
- maximum amount/duration;
- application status;
- approval evidence;
- payment timing (advance vs reimbursement);
- combination/double-funding constraints;
- expiry/review date.

The engine then creates a funding stack.

Example for a €20/hour worker:

- §16i wage subsidy covers the legally eligible subsidy basis where the person and employer qualify;
- Berlin complementary funding may cover eligible gaps for qualifying common-good employers;
- employer/municipality/foundation covers any remaining OpenWork wage premium, supervision, equipment or non-eligible cost;
- a bridge reserve covers cash-flow lag where grants reimburse after payroll.

**Important:** §16e/§16i are discretionary and require Jobcenter approval before the employment contract. Therefore OpenWork marks them `PENDING`, not `GUARANTEED`, until approval exists.

## Mission funding states

### RED — unfunded
Problem exists, but less than 100% of fully loaded cost has binding coverage.

### YELLOW — funding in progress
Likely sources identified or applications submitted, but at least one necessary source is not binding yet.

### GREEN — pay guaranteed
100%+ of fully loaded cost is covered by binding evidence and liquidity exists for payroll timing.

Only GREEN missions are shown in the worker marketplace as startable.

## Liquidity: how we guarantee salary even when grants reimburse later

A grant can be approved and still pay too slowly for payroll. OpenWork therefore separates **funding certainty** from **cash timing**.

V1 guarantee account:

1. employer/project signs funding stack;
2. OpenWork calculates the next payroll obligations;
3. cash or a committed credit/bridge facility covering that period is reserved;
4. payroll is released from the guaranteed pool;
5. later reimbursements refill the pool.

Longer term this can become an `OpenWork Pay Guarantee Fund` funded by a mix of philanthropy, public guarantees, employer deposits and a bank/impact-finance credit facility.

The worker never carries reimbursement risk.

## Upside above the €20 floor

The floor is not a ceiling. OpenWork should support visible progression:

- Skill Level 1 — €20+/h
- Skill Level 2 — €22+/h
- Specialist — €25+/h
- Lead / trainer — €28+/h
- regulated/tariff roles — applicable higher wage

Additional upside mechanisms:

- responsibility premium;
- scarce-skill premium;
- shift/undesirable-hours premium;
- trainer/mentor premium;
- outcome bonus only on top of guaranteed wage, never replacing it;
- regular-job conversion with negotiated salary bands.

## Worker UX

### Screen 1

**I want to work.**

Choose what sounds like you:

`Help people` `Organise` `Computer` `Outdoors` `Languages` `Children` `Care support` `Hands-on`

Choose availability:

`Now` `10h/week` `20h/week` `30h/week` `Full-time`

### Screen 2

OpenWork shows at most three best matches, all GREEN:

> **Digital helper for older Berliners**
> €20–24/h · 20h/week · Berlin
> ✓ Pay guaranteed
> ✓ 18-minute qualification
> ✓ employment contract
> ✓ path to regular role
>
> `QUALIFY & START`

The worker does not see the funding stack unless they choose “How is this funded?”.

## Organisation UX

### Screen 1

**What needs to get done?**

Organisation writes one sentence, for example:

> “300 older residents need help setting up digital government accounts.”

OpenWork converts it to:

- units of work;
- estimated hours;
- skill profile;
- training module;
- output/evidence definition;
- fully loaded budget;
- likely funding routes.

### Screen 2

Organisation sees:

> Need: 600 hours
> Fair wage: €20/h
> Fully loaded budget: €17,400 (illustrative model)
> Funding secured: €12,800
> Gap: €4,600
>
> `FIND THE GAP`

The system searches compatible sources and produces the exact next action, owner and evidence needed.

### Screen 3

When coverage reaches 100%:

> 🟢 **READY TO HIRE**
> Payroll liquidity reserved.
> Qualification module ready.
> Worker matching can start.

## Funder UX

Funders do not fund “a platform”. They can fund concrete outcome bundles:

> €50,000 funds 2,000 hours of digital support
> target: 400 residents helped
> wage floor: €20/h
> 100% employment contracts
> outcome evidence: verified service receipts
> transition target: 20% into regular roles

Every euro receives an auditable path:

`Funder → mission budget → payroll → worker → verified result`

## First OpenWork 100 pilot

Goal: **100 people into fair paid work in Berlin, with funding guaranteed before start.**

First mission families:

1. digital assistance for older people;
2. document/data support for nonprofits and public-interest organisations;
3. accessibility mapping and checks;
4. city/climate data collection;
5. language/community navigation within clear non-regulated boundaries;
6. school/community learning support where permitted;
7. administrative relief for social and care organisations;
8. digitisation support for associations and small public-interest organisations.

We prioritise missions that are:

- socially valuable;
- low or moderate entry barrier;
- trainable quickly;
- objectively verifiable;
- safe to delegate;
- capable of becoming recurring employment.

## First funding routes to operationalise

1. §16i SGB II — eligible long-term benefit recipients; up to five years; Jobcenter approval required.
2. §16e SGB II — eligible long-term benefit recipients; two-year employment commitment; Jobcenter approval required.
3. Berlin complementary §16i funding for eligible common-good employers.
4. Berlin Social Enterprises / related employment programmes.
5. ESF+ Berlin project instruments in employment, skills and social inclusion.
6. district/Land/public-company procurement for measurable services.
7. foundations such as LOTTO-Stiftung Berlin for eligible public-benefit projects.
8. inclusion funding such as Aktion Mensch for eligible organisations/target groups.
9. companies purchasing mission outcomes or co-financing a public-interest mission.
10. philanthropy/impact capital for the Pay Guarantee Fund and bridge liquidity.

## What OpenWork does not claim yet

- We cannot promise a universal legal right to a €20/hour job today.
- We cannot treat a submitted subsidy application as guaranteed money.
- We cannot assume different grants may be stacked without checking their specific double-funding rules.
- We cannot guarantee a person's net pay.
- We cannot use OpenWork badges as substitutes for regulated professional qualifications.

What we **can** guarantee as a platform rule is narrower and powerful:

> **If a mission is GREEN, the contractual gross wage at or above the OpenWork Fair Floor is fully funded and payroll liquidity is reserved before the person starts.**

That is the V1 promise.
