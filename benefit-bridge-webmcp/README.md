# Benefit Bridge 🌉

**The public-benefits website an AI agent can use without inventing authority.**

Benefit Bridge is a WebMCP challenge proof for agent-native public services. V0.2 adds a **Benefit Passport**: a reusable household snapshot that keeps self-attested claims, documentary evidence, derived benefit signals and authority decisions visibly separate.

## V0.2 — Benefit Passport

```text
household claims
      ↓
deterministic benefit signals
      ↓
Benefit Passport
  ├─ self-attested claims
  ├─ evidence categories
  ├─ cross-service reuse matrix
  └─ downstream-rights graph
      ↓
agent prepares next service
      ↓
human reviews / supplies evidence / applies
```

The model can inspect and prepare. **Authority still lives outside the model.**

## Berlin demo

Single parent · children 7 + 12 · €2,000 gross/month · €1,100 warm rent:

- **€518/month known Kindergeld anchor** — 2 × €259
- **up to €594/month KiZ worth checking** — explicitly a maximum, not an entitlement
- **Wohngeld → official check** — no guessed statutory amount
- **Bildung & Teilhabe → conditional downstream right** if KiZ/Wohngeld is actually awarded; 2026 school-supplies anchor: **€195/year**

## What the Benefit Passport proves

- typed values stay labelled **self-attested** rather than magically becoming verified evidence
- recurring evidence categories are mapped once and reused across KiZ / Wohngeld / Bildung & Teilhabe preparation
- a human can mark evidence as *prepared* locally; that still does **not** mean verified
- local passport saving requires an explicit human click
- V0.2 stores no passport data server-side
- downstream rights are represented as a graph without confusing “possible” with “awarded”

## WebMCP surface — 9 read-only tools

1. `check_eligibility`
2. `calculate_support`
3. `list_missing_evidence`
4. `explain_result`
5. `prepare_next_steps`
6. `replay_case`
7. `derive_benefit_passport`
8. `get_passport_status`
9. `plan_application`

Every tool is currently **read-only**. There is no autonomous submit/sign/apply tool.

## Shared capability

The human UI and WebMCP tools use the same `/api/evaluate` capability and deterministic policy engine.

```text
person → visual UI ─┐
                    ├→ evaluator → trace → passport → preparation plan
agent  → WebMCP ────┘
```

## Grounded 2026 anchors

- Bundesagentur für Arbeit: Kindergeld **€259 / eligible child / month** in 2026
- Bundesagentur für Arbeit: KiZ **up to €297 / child / month**; final amount requires the official calculation
- KiZ-Lotse asks for child, income and rent information among its checks
- Berlin Wohngeld guidance lists recurring evidence categories including income evidence, rental documents and recent rent-payment proof
- BMAS: KiZ or Wohngeld can unlock Bildung & Teilhabe; **€195 personal school supplies in calendar year 2026**

Official source URLs are embedded directly in `lib/benefits.mjs` and returned to the UI/agent.

## Run locally

```bash
npm run dev
# http://localhost:8888
```

## Verify

```bash
npm run check
```

Current deterministic suite: **9 tests** plus a smoke case.

The suite checks, among other things:

- Berlin anchor maths
- KiZ preliminary floor behaviour
- stable trace + passport IDs
- claims/evidence separation
- conditional downstream rights
- evidence-reuse service planning
- explicit unsupported-service failure

### Verification boundary

Engine, API shape, JavaScript syntax and deterministic tests are runnable in this repository. In the build environment used for this iteration, automated Chromium was blocked from opening the local dev origin by administrator policy, so a browser E2E pass is **not** claimed here. The UI includes an in-page agent simulator for manual review.

## Privacy boundary

V0.2 uses browser-local storage only after the user explicitly clicks **Save to this browser**. A production identity/evidence layer would need authentication, encryption, selective disclosure, retention controls, explicit consent and an authority-compatible trust model before any real personal documents should be stored.

## Why this matters

Public services often ask the same household for the same facts and evidence repeatedly. Benefit Bridge explores a safer agent-native alternative:

> **collect once → preserve provenance → reuse with consent → prepare automatically → authorise explicitly**

Built as a public-interest WebMCP proof by Michael Ninh in Berlin.
