# Realism Proof V2 — reusable income evidence + rights-safe agent eval

## Goal

Turn the targeted DigitalService / Agora work samples from UI demos into reproducible architecture proofs with current German rule slices, synthetic case coverage, explicit limits and safety metrics.

## Why these four systems

Priority is based on reach and vulnerability, not on pretending the population units are directly comparable:

- **Grundsicherung / SGB II** — largest directly means-tested population in this set. BA reported about 5.176m regelleistungsberechtigte people in 2.825m Bedarfsgemeinschaften in March 2026.
- **Kinderzuschlag** — 1.45m children benefited in 2025; high leverage for child poverty and working-poor families.
- **Wohngeld** — 1.21678m pure Wohngeld households at 31 Dec 2024.
- **Arbeitslosengeld I** — about 1.104m recipients in March 2026; especially valuable as the transition layer after job loss and before/alongside means-tested support.

## Life-event orchestration: income loss

The citizen-facing product should not require a person to know which programme they need before the state can help. `engine/life_event_router.py` therefore starts with one life event — **income loss** — and reuses one verified evidence packet to prepare four coordinated routes:

1. **ALG I first**: standard precheck for unemployment registration, ability to work 15+ hours and the standard 12 insured months within the prior 30 months; the existing 60/67% amount slice is reused.
2. **KiZ in parallel where children are present**: reuse the statutory minimum-income gate; full family/need/assets checks remain explicit missing work.
3. **Wohngeld in parallel**: reuse the income projection; rent, household and remaining WoGG facts remain explicit.
4. **Grundsicherung as safety net**: keep the means-tested fallback visible where ALG I is absent or insufficient; never infer final need from income alone.

The router does not choose a legal entitlement. Its product job is to answer:
- what can already be checked from verified facts;
- which services are plausible next routes;
- which exact facts are still missing;
- which facts can be reused instead of recollected.

Official transition context:
- https://www.arbeitsagentur.de/arbeitslos-arbeit-finden/arbeitslosengeld/finanzielle-hilfen/arbeitslosengeld-anspruch-hoehe-dauer
- https://www.arbeitsagentur.de/grundsicherung/finanziell-absichern/uebergang-grundsicherung
- https://www.arbeitsagentur.de/grundsicherung/finanziell-absichern/bedarfe

## Implemented rule slices

### Grundsicherungsgeld / SGB II

Implemented:
- standard §11b SGB II earned-income allowance bands: base EUR 100; 20% from 100–520; 30% from 520–1,000; 10% from 1,000–1,200, extended to 1,500 where a minor child is present;
- a countable-income projection over current net earned income plus selected other income;
- child benefit is represented as countable income in the SGB II slice;
- fail-closed on missing/unverified required evidence.

Not implemented:
- full need calculation, assets, housing reasonableness, all exemptions/special cases, sanctions or a final legal entitlement.

Sources:
- https://www.gesetze-im-internet.de/sgb_2/__11b.html
- https://www.arbeitsagentur.de/grundsicherung/finanziell-absichern/einkommen-ergaenzen
- https://www.arbeitsagentur.de/grundsicherung/unterstuetzung-fuer-familien

### Kinderzuschlag

Implemented:
- minimum-income gate: EUR 600 gross for single parents, EUR 900 for couples;
- ALG I / other qualifying income can contribute to the minimum-income gate;
- Wohngeld, Kindergeld and KiZ itself are excluded from that gate;
- fail-closed evidence requirements.

Not implemented:
- child/parent income taper, housing/need test, assets and final KiZ amount.

Sources:
- https://www.arbeitsagentur.de/familie-und-kinder/kinderzuschlag-verstehen/kinderzuschlag-anspruch-hoehe-dauer
- BA DA-KiZ, status 20 Feb 2026.

### Wohngeld

Implemented:
- reusable projected monthly income basis;
- selected current income types including ALG I;
- §16 WoGG deductions of 10% each for income tax, health/care insurance and pension contributions;
- explicit exclusion of Kindergeld and Kinderzuschlag from the income projection.

Not implemented:
- complete §14 catalogue, all Werbungskosten/Freibeträge, household exclusions, rent caps, heating/climate components or the final §19 Wohngeld amount.

Sources:
- https://www.gesetze-im-internet.de/wogg/__14.html
- https://www.gesetze-im-internet.de/wogg/__16.html
- BMWSB Wohngeld FAQ / calculator documentation.

### Arbeitslosengeld I

Implemented:
- standard 12-in-30-month insurance precheck plus registration / availability flags for the life-event router;
- official 60% / 67% replacement-rate layer applied to supplied daily Leistungsentgelt;
- 67% where a qualifying child is present, 60% otherwise.

Not implemented:
- short qualifying-period/special-case adjudication;
- full upstream Bemessungsentgelt/Leistungsentgelt tax calculation, eligibility period or duration.

Source:
- https://www.arbeitsagentur.de/arbeitslos-arbeit-finden/arbeitslosengeld/finanzielle-hilfen/arbeitslosengeld-anspruch-hoehe-dauer

## Reproducible eval

`python proof/realism_eval.py`

Current deterministic fixture:
- 48 synthetic households;
- 4 service projections each = 192 projections;
- 48 income-loss life-event plans, each preserving all four routes;
- shared canonical evidence packet;
- deliberately unverified evidence in a subset to prove fail-closed behaviour;
- 100 adversarial public-agent actions.

The hosted GitHub Actions run is the source of truth for the current numbers. Metrics are **fixture/eval metrics, not population impact claims**. The action-policy accuracy is against a deterministic labelled policy set, not general LLM safety.

## Next realism gate

1. independent domain review of each rule slice;
2. expand to 100–250 edge-case households with gold expectations;
3. add real administrative form/data schemas or anonymised case shapes;
4. measure evidence reuse against actual two-service journeys;
5. only then make time/cost savings claims.
