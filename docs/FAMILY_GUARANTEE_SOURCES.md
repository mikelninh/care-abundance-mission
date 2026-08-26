# Family Guarantee source notes — verified 2026-08-26

This file keeps current-law/public-data facts separate from CARE policy choices.

## VERIFIED — current public facts

### Kindergeld 2026

- €259 per child per month from 1 January 2026.
- Existing recipients did not need to reapply for the 2026 increase.
- Source: Bundesagentur für Arbeit, `Kindergeld steigt 2026`.
- https://www.arbeitsagentur.de/news/kindergeld-steigt-2026

### Kindergeld in Grundsicherung

- The Bundesagentur states that Kindergeld counts as income when calculating Grundsicherungsgeld.
- For children under 25 living in the parental household, Kindergeld is generally attributed to the child as income insofar as needed to cover the child's need.
- Source: Bundesagentur für Arbeit, family support / SGB-II knowledge base.
- https://www.arbeitsagentur.de/grundsicherung/unterstuetzung-fuer-familien
- https://www.arbeitsagentur.de/wissensdatenbank-sgbii/5-verhaltnis-zu-anderen-leistungen

### Grundsicherung 2026 rule needs

2026 amounts remain unchanged from 2025:

- single adult: €563;
- adult partners: €506 each;
- age 14–17: €471;
- age 6–13: €390;
- age 0–5: €357.

Common single-parent extra-need examples include 36% for one child under seven or two/three children under 16, with other percentages depending on number/age.

Source: BMAS, `Leistungen und Bedarfe in der Grundsicherung für Arbeitsuchende`, 1 July 2026.
https://www.bmas.de/DE/Arbeit/Grundsicherung-fuer-Arbeitsuchende/Leistungen-und-Bedarfe-in-der-Grundsicherung-fuer-Arbeitsuchende/leistungen-und-bedarfe-in-der-grundsicherung-fuer-arbeitsuchende.html

### Kinderzuschlag

- Up to €297/month per child under the published rules.
- It remains application-based in 2026.
- Minimum gross-income thresholds published by the Familienportal: €900 for couples, €600 for single parents.
- Sources:
  - https://familienportal.de/familienportal/familienleistungen/kinderzuschlag
  - https://familienportal.de/familienportal/familienleistungen/kinderzuschlag/wer-kann-kinderzuschlag-bekommen--136754

### Latest official poverty-risk threshold

Destatis EU-SILC 2025 first results, published 3 February 2026:

- population poverty-risk rate: 16.1%;
- threshold for one adult: €1,446 net/month;
- threshold for two adults + two children under 14: €3,036 net/month.

EU definition: below 60% of median equivalised disposable income.

Source:
https://www.destatis.de/DE/Presse/Pressemitteilungen/2026/02/PD26_039_63.html

### Child poverty / single parents

- Destatis reported 15.2% of under-18s at risk of poverty for 2024, about 2.2 million children and young people.
- Latest Destatis household-type table (2025 survey) reports 28.9% poverty risk for single-parent households and 12.0% for couples with children.
- Sources:
  - https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/11/PD25_N065_63.html
  - https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Einkommen-Konsum-Lebensbedingungen/Lebensbedingungen-Armutsgefaehrdung/Tabellen/armutsgef-typ-2-zvgl.html

### Social-state reform direction

The 2026 Sozialstaatskommission recommends a simpler unified benefit system and digital/once-only administration. BMAS says implementation work is underway and explicitly describes combining Grundsicherung, Wohngeld and Kinderzuschlag in a unified system.

Sources:
- https://www.bmas.de/DE/Soziales/Modernisierung-des-Sozialstaats/Umsetzung-der-Sozialstaatsreform/umsetzung-der-sozialstaatsreform.html
- https://www.bmas.de/DE/Service/Presse/Pressemitteilungen/2026/baerbel-bas-nimmt-ergebnisse-der-sozialstaatskommission-entgegen.html

### Automatic Kindergeld

The Bundestag approved staged antragsloses Kindergeld in July 2026. The first stage is intended from March 2027 for subsequent children where the Familienkasse can reuse existing data; a later stage is intended for first children.

Sources:
- https://www.bundestag.de/dokumente/textarchiv/2026/kw21-de-kindergeld-1174720
- https://www.bundesregierung.de/breg-de/aktuelles/kindergeld-ohne-antrag-2412916

---

## CARE POLICY / PRODUCT RULES — NOT CURRENT LAW

The following are deliberate design choices and must never be presented as current entitlements:

1. **Protected child base:** €259 Kindergeld per child sits above the Family Guarantee base floor instead of reducing it.
2. **Dual floor:** base floor is `max(current legal minimum, latest official anti-poverty threshold)`.
3. **Work keep rate:** at least 35% of additional net earned income remains additional disposable income while the top-up is active.
4. **Automatic top-up:** the state calculates and pays the gap without requiring the family to choose the correct programme/application.
5. **No good-faith clawback below the protected target.**
6. **One-screen family status** and once-only data workflow.

## NOT YET VERIFIED / REQUIRED BEFORE A GOVERNMENT CLAIM

- national annual fiscal cost of the protected-child mode;
- exact distribution of incremental cost across federal/Länder/municipal budgets;
- administrative savings from programme consolidation;
- exact legal changes required across EStG/BKGG/SGB II/SGB XII/WoGG/other laws;
- production data-access architecture and lawful bases for each register connection;
- final earnings taper that optimises poverty reduction, work incentives and fiscal cost.

These require representative household microsimulation, legal review and institutional implementation design.
