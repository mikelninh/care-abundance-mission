# Family Guarantee — end-to-end workflows

## 0. Funding principle

OpenWork and Family Guarantee need different guarantee mechanisms.

### OpenWork

A specific employment mission is GREEN only after mission funding + payroll liquidity are secured.

### Family Guarantee

A national anti-poverty guarantee must **not** be a grant programme with a capped pot that can be exhausted mid-year. The target end-state is a statutory individual entitlement financed through the public budget, with the payment system obligated to pay the deterministic amount when legal conditions are met.

For a pilot before legislation, the incremental CARE top-up requires a ring-fenced pilot fund with a hard participant/cost cap and cash reserve before enrolment.

---

# Citizen workflow

## Family

Sees:

1. `YOUR FAMILY IS PROTECTED`
2. guaranteed target;
3. household resources used;
4. protected child base;
5. automatic top-up;
6. next payment date;
7. one button: `Something is wrong`.

Does **not** need to know whether the backend uses Kindergeld, Grundsicherung, Wohngeld, Kinderzuschlag or another lawful route.

## Missing information

Ask only for the smallest fact that changes the result.

Bad:

> Upload all financial documents for the last six months.

Better:

> We cannot verify your current warm rent. Is it still €1,100/month? Upload or connect one current proof.

---

# State workflow

## 1. Family event service

Triggers:

- birth;
- child joins/leaves household;
- separation/custody change;
- job start/end;
- material payroll-hours change;
- verified rent/heating change;
- benefit/payment failure.

Output: `recalculate household`.

## 2. Once-only resolver

Retrieves only legally permitted facts needed for the calculation. Every data access records:

`purpose → legal basis/consent → fields → source → timestamp → retention rule`.

If a required fact cannot be fetched, create a citizen request rather than guessing.

## 3. Deterministic rules engine

Calculates two views:

- `CURRENT LAW` — statutory entitlement result;
- `CARE GUARANTEE` — policy/prototype result.

No generative model sets a benefit amount.

## 4. Payment router

### Current-law phase

Routes the person to / pre-fills official channels and tracks whether the statutory euro actually arrived.

### Pilot phase

Existing statutory payments continue normally. A ring-fenced pilot fund pays only the verified incremental CARE gap.

### National guarantee phase

Unified payment service executes the statutory Family Guarantee amount directly.

## 5. Receipt ledger

Every monthly decision stores:

`household facts → rule version → target → counted resources → top-up → payment instruction → settlement status`.

---

# Funding workflow

## National legislation target

The finance model is:

`existing child/family transfer spending`
`+ current minimum-income/housing support attributable to participant households`
`+ incremental anti-poverty top-up`
`+ gentler work-taper cost`
`- separately reported administrative savings`
`= gross public cost`

Do not net speculative labour-supply or long-term social returns against the cash budget when making the primary affordability claim. Show them separately as scenarios.

## Fiscal guarantee control

A family payment cannot be blocked because an internal programme sub-budget is exhausted. Treasury/appropriation management is a government problem, not an eligibility criterion shown to the family.

Government dashboard should therefore track:

- forecast statutory obligation;
- actual monthly obligation;
- appropriated amount;
- cash requirement;
- variance;
- household count;
- poverty gap closed;
- administrative cost.

If forecast cost rises, government adjusts appropriations. It does not silently stop protecting eligible children.

## Pilot guarantee control

Before a pilot household is enrolled:

1. calculate maximum pilot liability under conservative income-shock scenarios;
2. ring-fence enough cash for the pilot period;
3. reserve contingency;
4. cap enrolment before funds are exhausted;
5. never enrol a family on hoped-for donations.

---

# Correction / appeal workflow

## Citizen correction

One-screen facts:

- household composition;
- income;
- housing;
- custody;
- special need;
- payment account;
- `other`.

Citizen marks the wrong fact and supplies the correction once.

## Automatic safe handling

- obvious data mismatch → pause adverse change, route human review;
- missing payment → payment incident, not a new benefits application;
- government data error → recalculate and pay difference;
- good-faith overpayment → recovery only above protected floor;
- suspected fraud → separate due-process/fraud workflow; do not encode guilt in the benefit engine.

---

# Operational service levels for the target system

These are product targets, not current statutory deadlines.

- routine monthly recalculation: automatic;
- known income-shock event: same-day recalculation;
- missing critical fact: one focused request;
- family projected below floor with incomplete data: urgent human queue;
- confirmed underpayment: immediate payment instruction;
- payment failure: visible incident + retry/escalation;
- correction: traceable status, no black box.

---

# Family + OpenWork closed loop

A household should never face the false choice `poverty support OR work`.

1. Family Guarantee prevents the drop below the floor.
2. OpenWork can offer already funded €20+/hour work where suitable.
3. Skill Passport makes entry fast for non-regulated tasks.
4. Earnings taper ensures more work raises disposable income.
5. Recurring OpenWork demand converts toward regular employment.
6. Family Guarantee shrinks smoothly as income grows.
7. Family remains above the protected floor throughout transition.

North-star invariant:

> **Safety first; upward mobility second; never create a cliff between them.**
