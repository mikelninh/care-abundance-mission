# Income-Loss Life-Event Router

A deterministic public-service proof for one question:

> If a person loses income, can they describe the life event once and have the same verified evidence reused across the relevant public-service checks without an AI pretending to make the legal decision?

## Product flow

One verified evidence packet is reused to prepare four coordinated routes:

1. **Arbeitslosengeld I** — standard precheck and missing insurance/registration facts.
2. **Kinderzuschlag** — minimum-income gate only; full family/housing/assets tests remain outside this slice.
3. **Wohngeld** — reusable income projection; household, rent and municipality-specific facts remain for the full check.
4. **Grundsicherungsgeld** — safety-net check remains visible when ALG I may be absent or insufficient; final need is never inferred here.

Public interactive demo: <https://mikelninh.github.io/proof/digitalservice/life-event.html>

## Authority boundary

This is **routing/precheck**, not entitlement automation.

- `CHECK_NOW` means “prepare the full official check now”, not “approved”.
- `CHECK_PARALLEL` means “continue the official full check in parallel”, not “eligible”.
- `NEEDS_DATA` means a required verified fact is missing or unverified. Missing never becomes zero.
- `STANDARD_GATE_NOT_MET` keeps special cases and safety-net routes visible instead of pretending the journey ends.
- `NOT_APPLICABLE` is used only for a narrow explicit condition in this slice (for example, no child for KiZ).
- `SAFETY_NET_CHECK` means prepare the means-tested check; it is not an inferred benefit decision.

The competent public authority remains the decision maker.

## Fail-closed evidence contract

Before evidence is reused across multiple routes, `route_income_loss()` rejects structurally impossible packets:

- negative monetary amounts or counts;
- `NaN` / positive or negative infinity;
- provenance-key mismatches between the dictionary key and `EvidenceItem.key`;
- ambiguous boolean-like values other than `0` or `1`;
- fractional household/count fields;
- zero verified adults in this household slice;
- more than 30 insured months in a field explicitly defined over the last 30 months.

This is intentionally different from **unknown/unverified** evidence. Unknown evidence remains allowed and produces `NEEDS_DATA` rather than an invented value.

## Automated coverage

`tests/test_life_event_router.py` covers:

- one life event producing all four coordinated routes;
- missing/unverified ALG-I gate facts;
- no-child KiZ behavior without breaking other routes;
- failed standard ALG-I gate while keeping the safety net visible;
- evidence reuse across services;
- an unverified shared income fact blocking every dependent projection;
- multiple missing facts remaining explicit;
- negative values;
- `NaN` / infinity;
- provenance-key mismatch;
- invalid boolean flags;
- fractional household counts;
- zero-adult household input;
- insured-month values outside the declared 30-month window.

Supporting `tests/test_income_kernel_v2.py` covers the deterministic projection slices and their missing/unverified behavior.

The `CARE Guarantees proof` workflow runs these tests on pull requests **and again after relevant merges to `main`**.

## What this does not prove

- a complete current-law benefits calculator;
- final individual entitlement or payment amount;
- every special case in SGB II/SGB III/BKGG/WoGG;
- production integration with German authorities;
- automatic application submission or binding decisions.

Those are deliberately separate proof stages. The core invariant is: **reuse verified facts aggressively; invent nothing; preserve human/legal authority.**
