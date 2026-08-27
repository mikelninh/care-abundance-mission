# Targeted outreach — DigitalService + Agora

Prepared 2026-08-26. Keep the message short; let the proof carry the detail.

---

## 1) DigitalService — Product Manager

### Positioning

**AI Product Engineer / Product Builder for digital public services**

The application should not present CARE as a competing solution to DigitalService. It is evidence of how Michael works: start from citizen/admin burden, form a falsifiable product hypothesis, prototype the smallest useful system, make uncertainty explicit, test invariants, and define the next discovery questions.

### Targeted proof

**Income Kernel — Collect income once. Explain every projection.**

Repo demo path: `proof/digitalservice/index.html`

Code proof:
- `engine/income_kernel.py`
- `tests/test_income_kernel.py`

Public problem inspiration:
- DigitalService, "Mit einer zentralen Einkommensprüfung Kommunen entlasten", 28 May 2026
- https://digitalservice.bund.de/blog/mit-einer-zentralen-einkommenspruefung-kommunen-entlasten

Role:
- https://digitalservice.bund.de/karriere/offene-stellen/4844852101

### 30-second pitch

> Mich reizt am DigitalService nicht einfach „GovTech“, sondern genau diese Art von Problem: Bürger:innen reichen dieselben Informationen mehrfach ein, Fachlogiken unterscheiden sich, und die eigentliche Komplexität landet bei Menschen und Kommunen. Als ich eure Arbeit zur zentralen Einkommensprüfung gesehen habe, habe ich deshalb einen kleinen unabhängigen Proof gebaut: eine kanonische Evidence-Schicht, versionierte Einkommensprojektionen, Missing-Data-Checks und vollständige Traces. Mir geht es dabei weniger darum, eure Lösung nachzubauen, sondern zu zeigen, wie ich arbeite: Problem verstehen, Hypothesen formulieren, schnell etwas Testbares bauen und anschließend mit Nutzenden und Fachexpert:innen herausfinden, was wirklich trägt.

### Short application note

> Der DigitalService ist für mich besonders spannend, weil hier Produktentwicklung, technische Umsetzung und die Realität von Verwaltung und Gesetzgebung tatsächlich zusammenkommen. Ich arbeite gern genau an dieser Schnittstelle: komplexe Systeme so zu zerlegen, dass für Nutzende ein klarer Service entsteht und für das Team trotzdem Regeln, Unsicherheiten und Wirkung messbar bleiben.
>
> Als gezielten Arbeitsnachweis habe ich – inspiriert von eurer veröffentlichten Arbeit zur zentralen Einkommensprüfung – einen kleinen unabhängigen „Income Kernel“ gebaut. Der Proof trennt wiederverwendbare Einkommensnachweise von versionierten Regelprojektionen, blockiert Ergebnisse bei fehlenden oder ungeprüften Pflichtdaten und erhält einen nachvollziehbaren Provenienz-Trace. Dazu habe ich die wichtigsten Produktannahmen und nächsten Discovery-Fragen dokumentiert.
>
> Ich würde mich freuen, diese Arbeitsweise als Product Manager in ein interdisziplinäres DigitalService-Team einzubringen: nutzerzentriert, hypothesengetrieben, pragmatisch und mit genug technischer Tiefe, um früh testbare Lösungen statt nur Konzepte zu schaffen.

### Interview proof story — STAR, compact

**Situation:** Fragmented social benefits repeatedly require income evidence and service-specific interpretation.

**Task:** Demonstrate a reusable product architecture without pretending to implement current law.

**Action:** Separated canonical evidence from versioned rule projections; added provenance, missing/unverified-data states, interactive prototype, deterministic engine and invariant tests; documented the next research hypotheses rather than declaring the prototype "solved".

**Result:** A runnable targeted proof that can demonstrate three rule projections from one evidence packet and refuses to output a result when required evidence is missing or unverified.

### Fit evidence to emphasize

- continuous discovery: hypotheses + explicit next user/domain research;
- user-centered product thinking: complexity stays behind the service boundary;
- evidence-driven delivery: rules/version/provenance + metrics;
- stakeholder work: citizen, caseworker, legal/domain, platform/infrastructure perspectives;
- pragmatic building: interactive proof + deterministic code + tests;
- political/legal context: explicitly distinguishes technical feasibility from legal harmonization;
- communication: explains a complex cross-cutting service in one short journey.

### Do not claim

- that this reproduces DigitalService's prototype;
- that the synthetic rules implement current German benefit law;
- that one technical module solves legal harmonization;
- that CARE is already a government production system.

---

## 2) Dr. Florian Theißing — Agora Digitale Transformation

### Positioning

Do **not** approach as a job request first. Approach as: "Your research question is one I am independently trying to make executable and testable; I built a small proof and would value a critical conversation."

### Targeted proof

**Rights-Safe Service Agent — Helpful enough to act. Constrained enough to trust.**

Repo demo path: `proof/agora/index.html`

Code proof:
- `engine/rights_safe_agent.py`
- `tests/test_rights_safe_agent.py`

Public problem inspiration:
- Agora project: Agentische KI für eine demokratische Verwaltung
- https://agoradigital.de/projekte/agentische-ki-fuer-eine-demokratische-verwaltung/
- Agora study/policy paper, July 2026
- https://agoradigital.de/publikation/agentische-ki-fuer-eine-demokratisch-rechtsstaatliche-verwaltung-potenziale-nutzen-grundsaetze-staerken/

### 30-second pitch

> Ihre Arbeit zu agentischer KI in der Verwaltung hat bei mir einen Nerv getroffen, weil mich dieselbe Frage beschäftigt: Wie machen wir Verwaltung proaktiv und hilfreich, ohne Verantwortung, Nachvollziehbarkeit und Bürgerautonomie wegzuautomatisieren? Ich habe dazu einen kleinen ausführbaren Proof gebaut. Der Agent kann Lebenslagen in mögliche Services übersetzen, Informationen vorbereiten, Verfahren erklären und Übergaben koordinieren; rechtsverbindliche Entscheidungen sind technisch blockiert und externe Aktionen brauchen explizite Bestätigung plus Action Receipt. Das ist natürlich kein fertiges Verwaltungssystem – aber ein Versuch, die Gestaltungsprinzipien als testbare Produktgrenzen zu operationalisieren. Ich würde sehr gern hören, wo Sie den Ansatz für zu streng, zu locker oder schlicht falsch halten.

### Email draft

**Subject:** Agentische Verwaltung: kleiner ausführbarer Proof zu Ihren Guardrails

> Guten Tag Herr Dr. Theißing,
>
> Ihre aktuelle Arbeit zu agentischer KI für eine demokratisch-rechtsstaatliche Verwaltung hat mich sehr angesprochen. Mich beschäftigt seit einiger Zeit eine ähnliche praktische Frage: Wie kann ein digitaler Staat Menschen proaktiv durch Leistungen und Verfahren helfen, ohne dabei Verantwortung, Nachvollziehbarkeit oder Bürgerautonomie wegzuautomatisieren?
>
> Ich habe deshalb einen kleinen unabhängigen Proof gebaut, der einige dieser Grenzen ausführbar macht: Orientierung, Antragsvorbereitung, Verfahrensbegleitung, verständliche Kommunikation und behördenübergreifende Koordination sind möglich; rechtsverbindliche Leistungsentscheidungen werden blockiert, und konsequenzreiche externe Aktionen benötigen explizite Bestätigung und erzeugen einen nachvollziehbaren Action Receipt.
>
> Mir geht es ausdrücklich nicht darum zu behaupten, damit das Problem gelöst zu haben. Ich möchte zeigen, dass sich die Prinzipien als Produktverhalten und testbare Invarianten konkretisieren lassen – und herausfinden, wo das Modell in der Verwaltungsrealität scheitert.
>
> Falls Sie 20–30 Minuten für einen kritischen Austausch hätten, würde ich Ihnen den Proof sehr gern zeigen. Besonders interessieren würde mich, welche Action Boundaries Sie für zu eng oder zu weit halten und welche realen Verwaltungsfälle ein sinnvoller nächster Test wären.
>
> Viele Grüße
> Michael Ninh

### LinkedIn version

> Hallo Herr Dr. Theißing, Ihre Arbeit zu agentischer KI für eine demokratisch-rechtsstaatliche Verwaltung trifft ziemlich genau eine Frage, an der ich selbst baue: Wie kann ein Agent Bürger:innen wirklich durch Leistungen/Verfahren helfen, ohne still zum Entscheider zu werden? Ich habe dazu einen kleinen unabhängigen, getesteten Proof gebaut – mit expliziten Action Boundaries, Confirmation Gates und Receipts. Kein fertiges Verwaltungssystem, sondern ein Versuch, die Prinzipien ausführbar zu machen. Ich würde Ihnen das gern einmal in 20 Minuten zeigen und bewusst kritisch auseinandernehmen lassen.

### Conversation goal

Do not optimize for "impress Florian". Optimize for one of these outcomes:

1. one concrete administrative use case to test;
2. one expert/person he recommends talking to;
3. one critique that materially changes the action model;
4. interest in a small shared experiment/workshop;
5. permission to follow up with a stronger V1 after testing.

### Questions worth asking

1. Which agent action would you consider the most valuable *and* legally/organizationally tractable first real use case?
2. Where is explicit confirmation necessary, and where would it create needless friction?
3. Which distinction between "communication", "preparation" and legally relevant action tends to break down in practice?
4. What evidence would convince you that an agent improves access/equal treatment rather than merely throughput?
5. Which public organization would be the right environment for a small adversarial pilot?

### Do not claim

- legal compliance merely because the prototype has guardrails;
- that an LLM can determine entitlement;
- autonomous cross-authority data access;
- that action receipts alone solve accountability;
- affiliation with Agora.

---

## Outreach sequence

### DigitalService
1. finish the PM application with the targeted proof as one work sample;
2. link to the proof, not the entire CARE universe;
3. use CARE/Family Guarantee only as supporting context if asked;
4. prepare the STAR story for screening/deep dive.

### Agora
1. send concise email or LinkedIn message;
2. targeted proof is the only primary link;
3. ask for a critical conversation, not employment;
4. capture critique as V1 requirements;
5. publish before/after changes with explicit acknowledgement only if permission is given.

## Shared one-line positioning

> I turn public-system problems into small, inspectable product proofs — then use research, domain expertise and tests to find out what survives contact with reality.
