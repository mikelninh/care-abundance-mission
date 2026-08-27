# Benefit Bridge 🌉

**A WebMCP proof for public benefits: one trustworthy capability surface for people and their AI agents.**

Benefit Bridge turns a small household snapshot into source-linked benefit orientation, an evidence checklist, safe next actions and a replayable rule trace. The visual UI and the agent tools call the same deterministic evaluator.

> **Boundary:** this is a challenge prototype, not a statutory calculator, benefits decision or legal advice. It deliberately refuses to invent exact values where the official calculation is more complex.

## Why WebMCP

Most government websites are technically readable by agents but not *agent-ready*. An agent has to scrape text, infer which form controls matter and guess whether clicking a button is safe.

Benefit Bridge exposes explicit browser tools instead:

- `check_eligibility`
- `calculate_support`
- `list_missing_evidence`
- `explain_result`
- `prepare_next_steps`
- `replay_case`

All six are registered with the current `document.modelContext.registerTool(definition, { signal })` API and are read-only. There is no autonomous application submission.

## What is real in this proof

The current policy pack pins a few official 2026 anchors:

- **Kindergeld:** €259 per eligible child / month from January 2026.
- **Kinderzuschlag:** up to €297 per child / month.
- **KiZ preliminary income floor:** €600 gross for single parents and €900 for couples.

The prototype **does not** claim to reproduce the complete KiZ or Wohngeld statutory calculations. KiZ is clearly labelled as a maximum potential amount; Wohngeld is routed to an official check.

Official sources are linked in every result.

## Architecture

```text
person ── visual form ───────────────┐
                                     │
agent ── WebMCP tools ───────────────┼── POST /api/evaluate
                                     │          │
                                     │          ▼
                                     └── deterministic policy engine
                                                │
                          sources + uncertainty + trace + boundary
```

The design rule is simple: **a tool wraps the same capability the website already uses.** There is no hidden “agent-only” rules path.

## Run locally

Requires Node 20+.

```bash
npm run dev
# open http://localhost:8888
```

Then run:

```bash
npm test
npm run check
```

The page includes a small WebMCP testing shim only when `document.modelContext` is unavailable. That means ordinary browsers can use the built-in agent simulator, while WebMCP-capable Chromium uses the native API.

For native WebMCP testing in current Chromium, enable the WebMCP testing flag / origin-trial environment described by Chrome's WebMCP documentation.

## Deploy to Netlify

```bash
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

`netlify.toml` already configures the static site, Functions directory and `/api/evaluate` redirect.

## Safety / trust properties

- deterministic server-side evaluator for pinned rules
- explicit distinction between known amount, maximum potential and not-calculated values
- official source link per benefit
- stable trace ID for the same household input
- human-readable decision trace
- all WebMCP tools marked read-only
- no application submission, signing or legal-entitlement claim
- input validation on the server, not only in tool descriptions

## Demo case

Single parent · 2 children (7, 12) · €2,000 gross income · €1,100 warm rent · Berlin.

Expected orientation:

- **€518/month known Kindergeld anchor** (2 × €259)
- **up to €594/month KiZ worth checking** (2 × €297 maximum; *not* an entitlement amount)
- Wohngeld flagged for an official calculation instead of guessed

## Next proof upgrades

1. signed/versioned policy packs with machine-readable source snapshots
2. official-calculator adapters instead of duplicated complex statutory formulas
3. Netlify Blobs for privacy-safe session trace persistence
4. eval suite covering contradictory inputs, stale policy versions and prompt/tool misuse
5. EUDI/eID selective-disclosure path for “prove once, reuse safely” evidence

---

Built by Michael Ninh for the 2026 WebMCP Challenge.
