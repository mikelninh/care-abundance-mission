# CARE Family Guarantee — no child below the floor

> **The state already knows a child exists. The family should not have to discover, combine and repeatedly apply for the money required to keep that child out of poverty.**

This document separates **current 2026 law** from the **CARE policy/product proposal**.

## The problem today

Germany has multiple family and minimum-income systems with different owners and rules: Kindergeld, Grundsicherungsgeld, Kinderzuschlag, Wohngeld, Unterhaltsvorschuss, Bildung und Teilhabe and tax allowances.

In 2026 Kindergeld is €259/month per child. In Grundsicherung it is treated as income when the Jobcenter calculates the remaining need. That makes administrative sense inside a top-up system, but it means a low-income child does not necessarily receive €259 *on top* of the minimum-income floor.

At the same time, the latest official Destatis data show material child-poverty risk and especially high risk for single-parent households.

The government is already moving toward simpler administration: from July 2026 Bürgergeld is called Grundsicherungsgeld; the Sozialstaatskommission recommends combining core tax-funded benefits; and antragsloses Kindergeld is scheduled to begin in stages from 2027.

CARE goes one step further: **make anti-poverty protection itself automatic.**

---

# The guarantee

## Citizen-facing promise

> **If a child lives in your household, the state continuously checks whether your family is financially safe. If verified household resources fall below the protected floor, the difference is paid automatically.**

No benefit maze. No knowing which office owns which euro.

The family sees one status:

- `PROTECTED` — projected resources stay above the floor;
- `TOP-UP ACTIVE` — an automatic payment is filling the gap;
- `DATA NEEDED` — only the one missing fact that materially changes the calculation;
- `URGENT` — payment or housing risk requires human handling now.

## Five hard invariants

1. **No child below the floor.** The calculated disposable household resources after the guarantee may not be below the protected target.
2. **Kindergeld is a protected child base in the strong policy mode.** It does not replace the Family Guarantee top-up.
3. **Work always pays.** Additional earned income may reduce the top-up, but never 1:1; V0 keeps at least 35% of each additional net earned euro while top-up is active.
4. **No good-faith clawback into poverty.** Recovery from future payments may only use income above the protected target.
5. **The state owns the bureaucracy.** Existing register/payroll/tax/housing data are reused under lawful once-only data sharing; the family supplies only genuinely missing information.

---

# What exactly is the floor?

One number is not robust enough. CARE uses the stronger of two independently grounded tests.

## Floor A — legal minimum

2026 rule needs plus relevant special needs plus verified eligible housing/heating cost.

For V0 the deterministic engine includes:

- adult single: €563/month;
- adult partner: €506/month;
- child 0–5: €357/month;
- child 6–13: €390/month;
- child 14–17: €471/month;
- common single-parent extra-need percentages;
- housing/heating as an explicit household input;
- an override for additional needs.

This is a guardrail, not yet a replacement for the complete statutory entitlement engine.

## Floor B — anti-poverty floor

The latest official Destatis poverty-risk threshold is 60% of median equivalised disposable income. The published EU-SILC 2025 threshold is €1,446/month for one adult. CARE applies the modified OECD equivalence weights used for household comparison:

- first adult: 1.0;
- additional adult: 0.5;
- child under 14: 0.3;
- child 14+: 0.5.

Example: two adults + two children under 14 gives about €3,036/month, matching the latest official published household threshold after rounding.

## CARE base floor

`base_family_floor = MAX(legal_minimum, anti_poverty_floor)`

This matters in expensive housing markets: a generic relative-income threshold must not override a higher verified legal/housing minimum.

## Strong protected-child mode

`protected_target = base_family_floor + €259 × number_of_children`

This deliberately treats universal Kindergeld as a child-development base rather than as money that merely substitutes for the anti-poverty top-up.

That is a **policy proposal**, not current German law. National fiscal cost must be microsimulated before making a budget claim.

---

# Work must produce upside

A simple poverty top-up can create a 100% marginal withdrawal rate: earn €1 more, lose €1 support. CARE refuses that design.

V0 uses:

`countable_earned_income = net_earned_income × 65%`

So, while the top-up is active:

`€100 additional net earnings → at least €35 additional disposable household income`

The 35% keep rate is configurable. The non-negotiable rule is monotonicity:

> **More earned income must never reduce disposable household income.**

OpenWork then sits naturally underneath the Family Guarantee:

`Family Security → Learn → Fair Paid Work → More Net Income → Skill Growth → Regular Job`

The guarantee is a safety floor, not a ceiling.

---

# Zero-application workflow

## 1. Child event

Birth/residence data creates or updates the household entitlement record.

The citizen does **not** start with a benefit application.

## 2. Once-only household facts

The state resolves, where legally available and consent/authority permits:

- household members;
- child ages;
- current payroll/employment income;
- existing social transfers;
- tax status where relevant;
- verified rent/housing/heating data;
- custody/shared-care status;
- special legally relevant needs.

A missing-data request asks only one question at a time and explains why it changes the amount.

## 3. Monthly nowcast

Before each payment cycle:

`family floor → resources → protected child base → work disregard → gap`

If `gap > 0`, the system creates an automatic top-up.

## 4. Income-shock trigger

Job loss, hours reduction, separation, birth or a material verified rent change triggers an immediate recalculation rather than waiting for the next annual application cycle.

Target operational standard for a future production system:

- automatic provisional recalculation from trusted event data;
- emergency human path for incomplete data;
- correction payment as soon as the gap is verified.

## 5. Payment receipt

The family sees a one-screen explanation:

> **Family protected**
>
> Base family floor: €X
> Protected child base: €Y
> Household resources counted: €Z
> Work bonus retained: €A
> Automatic top-up: €B
> Next payment: date

Every number is expandable to rule + source + data used.

## 6. Appeal/correction

One button:

`Something is wrong`

The family selects the incorrect fact, not the responsible authority.

The system routes the correction internally.

---

# No-clawback-into-poverty rule

Good-faith households should not be pushed below the guarantee because the administration used stale data or reconciled late.

V0 rule:

`maximum_recovery = MAX(0, disposable_before_recovery - protected_target)`

Fraud and intentional false declarations remain separate legal cases. The product guarantee is about protecting families acting in good faith from administrative volatility.

---

# Child services: cash is necessary, not sufficient

The cash guarantee should unlock automatic service entitlements where available:

- school/kita meals;
- school supplies;
- local transport where covered;
- participation/sports/culture support;
- childcare fee reductions/exemptions;
- learning support;
- relevant health/prevention services.

The UI should say `included` and arrange access, rather than telling parents to research another programme.

---

# Funding architecture

CARE does not invent a new euro for every existing programme. It first creates a **single delivery layer over existing public budgets**, then identifies the residual fiscal gap created by the stronger guarantee.

## Existing flows to consolidate operationally

- Kindergeld;
- Grundsicherung child/adult needs;
- Kinderzuschlag;
- Wohngeld where integrated by reform;
- relevant child participation benefits;
- other family transfers where law permits.

## New fiscal requirement

The strong policy mode creates additional cost mainly from:

- protecting Kindergeld above the family floor;
- filling the gap to the anti-poverty threshold when current legal minimum is lower;
- improved take-up because payment becomes automatic;
- a gentler earnings taper so work creates real upside.

**Do not publish a national euro cost until microsimulation on representative household microdata is complete.**

Required model:

`household microdata → current-law disposable income → CARE guarantee → incremental cost → behavioural sensitivity → distribution by household type`

The result must show gross cost, overlap with existing programmes, administration savings separately, and uncertainty.

---

# Implementation architecture

## Family Guarantee Engine

Deterministic calculation, versioned rules, no LLM deciding entitlement.

## Eligibility/Rules Graph

Maps current programmes, precedence, incompatibilities and transitions.

## Once-Only Data Broker

Purpose-limited data access, consent/legal-basis record, minimisation, audit log.

## Payment Orchestrator

Creates payment instructions only after deterministic entitlement calculation and identity/account checks.

## Evidence Ledger

For every amount:

`value → rule version → input facts → source → calculation trace → payment → reconciliation`

## Family Safety Monitor

Detects income shocks, expiring decisions, missing payments and households projected below the floor.

AI may help explain, classify documents and route exceptions. **AI does not get final authority over legal entitlement or payment amount.**

---

# Real-world rollout

## Phase 0 — proof

Use synthetic households and public 2026 rules. Prove:

- protected Kindergeld is not offset;
- floor is never breached;
- more work never reduces disposable income;
- income shocks produce the correct top-up;
- good-faith recovery never breaches the floor.

## Phase 1 — shadow calculator

With a benefits-advice/municipal partner, calculate `CURRENT LAW` and `CARE GUARANTEE` side by side without moving money.

Measure:

- missed current entitlements;
- time and documents required;
- poverty gap before/after;
- work-incentive curve;
- false-positive/false-negative eligibility flags.

## Phase 2 — top-up pilot

A legally suitable public/philanthropic pilot fund covers the **incremental CARE gap** for a defined participant group while existing statutory benefits continue through official channels.

This proves delivery without pretending a prototype can rewrite federal law.

## Phase 3 — government integration

Integrate with the emerging unified social-benefit system, once-only infrastructure and automatic Kindergeld process.

## Phase 4 — legal guarantee

Legislation encodes the protected floor, automatic calculation/payment duty, data safeguards, work taper, correction deadlines and appeal rights.

---

# Success metric

Not `applications processed`.

Not `benefits claimed`.

The north-star test is brutally simple:

> **How many children were projected below the protected floor, and how many remained below it after the state had the information required to act?**

Target: **zero.**
