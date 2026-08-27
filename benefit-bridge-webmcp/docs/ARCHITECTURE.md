# Benefit Bridge architecture — v0.2

## Principle

**Claims are not evidence. Evidence is not an authority decision.**

Benefit Bridge keeps those three layers separate all the way through the system.

## Data flow

```text
Household form / WebMCP household input
                 │
                 ▼
       normalize + validate
                 │
                 ▼
     deterministic policy pack
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
   benefit    trace    Benefit Passport
   signals             ├─ claims
                       ├─ evidence map
                       ├─ reuse matrix
                       └─ downstream graph
                 │
                 ▼
         preparation plans
                 │
                 ▼
       explicit human action
```

## Trust layers

### 1. Claim
A value the person supplied, for example `monthlyGrossIncome = 2000`.

Status in V0.2: `self_attested`.

### 2. Evidence
A document or trusted source that could support a claim, for example a payslip, rental agreement or decision notice.

V0.2 stores **no documents**. The UI only tracks whether a person has marked an evidence category as prepared.

### 3. Derived signal
A deterministic result from the pinned demo policy pack, for example:

- 2 eligible children × €259 Kindergeld anchor
- KiZ preliminary check worth pursuing
- Wohngeld should be checked officially

### 4. Authority decision
The actual decision from Familienkasse, Wohngeldstelle, municipality, etc.

Benefit Bridge never fabricates this layer.

## Rights graph

```text
Kindergeld ──→ KiZ signal ─────────┐
                                   ├──→ Bildung & Teilhabe (if actually awarded)
Wohngeld official check ───────────┘
```

The graph deliberately represents the edge as conditional until a real KiZ/Wohngeld award exists.

## Evidence reuse

V0.2 maps reusable evidence categories across services:

| Evidence category | KiZ | Wohngeld | Bildung & Teilhabe |
| --- | :---: | :---: | :---: |
| child / household | ✓ | ✓ | ✓ |
| income evidence | ✓ | ✓ |  |
| housing evidence | ✓ | ✓ |  |
| recent rent-payment proof |  | ✓ |  |
| KiZ / Wohngeld award notice |  |  | ✓ |

This is a **preparation model**, not a universal statutory checklist. Individual cases can require more evidence.

## WebMCP contract

The page registers nine read-only tools through `document.modelContext.registerTool(...)`.

The three v0.2 passport tools are:

- `derive_benefit_passport` — derive claims/evidence/reuse from a household
- `get_passport_status` — inspect the latest passport plus human-marked local preparation state
- `plan_application` — produce a KiZ/Wohngeld/BuT evidence preparation plan

No registered tool can submit, sign, or create a legal application.

## Storage

V0.2:

- server: **stateless**
- passport save: **browser localStorage, explicit human click only**
- evidence documents: **not stored**

Future Netlify-native option: encrypted pseudonymous state in Netlify Blobs or structured state in Netlify Database, only after adding a real authentication/consent model. Netlify Blobs is suitable as a simple key/value store, but storage technology alone is not a trust model.

## Evaluation

Deterministic tests focus on boundaries and regression behaviour rather than “AI intelligence”:

- amount anchors
- policy gates
- stable trace/passport IDs
- claim/evidence separation
- downstream conditionality
- evidence reuse planning
- unsupported-service failures

The goal is for every discovered failure to become a repeatable test.
