# Realism Proof V2 — reusable income evidence + rights-safe agent eval

## Goal

Turn the targeted DigitalService / Agora work samples from UI demos into reproducible architecture proofs with current German rule slices, synthetic case coverage, explicit limits and safety metrics.

## Why these four systems

Priority is based on reach and vulnerability, not on pretending the population units are directly comparable:

- **Grundsicherung / SGB II** — largest directly means-tested population in this set. BA reported about 5.176m regelleistungsberechtigte people in 2.825m Bedarfsgemeinschaften in March 2026.
- **Kinderzuschlag** — 1.45m children benefited in 2025; high leverage for child poverty and working-poor families.
- **Wohngeld** — 1.21678m pure Wohngeld households at 31 Dec 2024.
- **Arbeitslosengeld I** — about 1.104m recipients in March 2026; especially valuable as the transition layer after job loss and before/alongside means-tested support.

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
- official 60% / 67% replacement-rate layer applied to supplied daily Leistungsentgelt;
- 67% where a qualifying child is present, 60% otherwise.

Not implemented:
- full upstream Bemessungsentgelt/Leistungsentgelt tax calculation, eligibility period or duration.

Source:
- https://www.arbeitsagentur.de/arbeitslos-arbeit-finden/arbeitslosengeld/finanzielle-hilfen/arbeitslosengeld-anspruch-hoehe-dauer

## Reproducible eval

`python proof/realism_eval.py`

Current deterministic fixture:
- 48 synthetic households;
- 4 service projections each = 192 projections;
- shared canonical evidence packet;
- deliberately unverified evidence in a subset to prove fail-closed behaviour;
- 100 adversarial public-agent actions.

Local pre-push result:

```text
households=48
services=4
projections=192
shared_evidence_reuse_rate=34.8%
fail_closed_projections=15
nonmissing_projections_with_used-fields=177/177
agent_adversarial_cases=100
agent_policy_accuracy=100.0%
unsafe_executions=0
unconfirmed_external_actions=0
missing_action_receipts=0
safe_assistance_blocked=0
```

These metrics are **fixture/eval metrics, not population impact claims**. The 100% action-policy accuracy reflects a deterministic labelled policy set, not general LLM safety.

## Next realism gate

1. independent domain review of each rule slice;
2. expand to 100–250 edge-case households with gold expectations;
3. add real administrative form/data schemas or anonymised case shapes;
4. measure evidence reuse against actual two-service journeys;
5. only then make time/cost savings claims.
