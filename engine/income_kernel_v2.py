"""Reality proof V2 for reusable income evidence across major German benefits.

Scope deliberately stays narrow:
- SGB II / Grundsicherungsgeld: statutory standard earned-income allowance and
  a countable-income projection slice, not a full entitlement calculation.
- Kinderzuschlag: statutory minimum-income gate, not full KiZ amount.
- Wohngeld: income projection slice using a pre-adjusted employment income
  basis plus the §16 10%-deduction flags, not the full Wohngeld formula.
- Arbeitslosengeld I: official 60/67% replacement rate applied to a supplied
  Leistungsentgelt; the tax/assessment module that derives Leistungsentgelt
  from historical gross pay is intentionally outside this proof.

The purpose is to prove that one provenance-rich evidence packet can be reused
across genuinely different statutory definitions without hiding missing data.
"""

from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple

from engine.income_kernel import EvidenceItem


RULE_VERSION = "DE-2026-08-v2"

SERVICE_FIELDS: Dict[str, FrozenSet[str]] = {
    "grundsicherung": frozenset({
        "employment_gross", "employment_net", "alg1_monthly", "maintenance",
        "capital_income", "child_benefit", "child_supplement", "has_minor_child",
    }),
    "kiz_minimum": frozenset({
        "employment_gross", "alg1_monthly", "maintenance", "capital_income",
        "adults", "children",
    }),
    "wohngeld_income": frozenset({
        "employment_wogg_basis", "alg1_monthly", "maintenance", "capital_income",
        "pays_income_tax", "pays_health_care", "pays_pension",
    }),
    "alg1_rate": frozenset({
        "alg1_leistungsentgelt_daily", "children",
    }),
}


@dataclass(frozen=True)
class Projection:
    service: str
    status: str
    value: float | None
    unit: str
    rule_version: str
    used: Tuple[str, ...]
    excluded: Tuple[str, ...] = ()
    missing: Tuple[str, ...] = ()
    note: str = ""


def _amount(evidence: Dict[str, EvidenceItem], key: str) -> float:
    return evidence[key].monthly_amount


def _bool(evidence: Dict[str, EvidenceItem], key: str) -> bool:
    return bool(round(_amount(evidence, key)))


def _require(evidence: Dict[str, EvidenceItem], keys: FrozenSet[str]) -> Tuple[str, ...]:
    return tuple(sorted(k for k in keys if k not in evidence or not evidence[k].verified))


def sgb2_standard_earned_income_allowance(gross: float, has_minor_child: bool) -> float:
    """Standard §11b SGB II earned-income allowance bands, Aug 2026."""
    gross = max(0.0, gross)
    allowance = min(gross, 100.0)
    allowance += max(0.0, min(gross, 520.0) - 100.0) * 0.20
    allowance += max(0.0, min(gross, 1000.0) - 520.0) * 0.30
    upper = 1500.0 if has_minor_child else 1200.0
    allowance += max(0.0, min(gross, upper) - 1000.0) * 0.10
    return round(allowance, 2)


def project_grundsicherung(evidence: Dict[str, EvidenceItem]) -> Projection:
    required = SERVICE_FIELDS["grundsicherung"]
    missing = _require(evidence, required)
    if missing:
        return Projection("Grundsicherung", "NEEDS_DATA", None, "EUR/month",
                          RULE_VERSION, (), missing=missing,
                          note="Countable-income slice only; no final entitlement.")

    gross = _amount(evidence, "employment_gross")
    net = _amount(evidence, "employment_net")
    allowance = sgb2_standard_earned_income_allowance(
        gross, _bool(evidence, "has_minor_child")
    )
    countable_earned = max(0.0, net - allowance)
    countable = (
        countable_earned
        + _amount(evidence, "alg1_monthly")
        + _amount(evidence, "maintenance")
        + _amount(evidence, "capital_income")
        + _amount(evidence, "child_benefit")
        + _amount(evidence, "child_supplement")
    )
    return Projection(
        "Grundsicherung", "READY", round(countable, 2), "EUR/month",
        RULE_VERSION, tuple(sorted(required)),
        note=f"Standard earned-income allowance: EUR {allowance:.2f}; needs/assets/housing still required for final entitlement."
    )


def project_kiz_minimum(evidence: Dict[str, EvidenceItem]) -> Projection:
    required = SERVICE_FIELDS["kiz_minimum"]
    missing = _require(evidence, required)
    if missing:
        return Projection("Kinderzuschlag minimum gate", "NEEDS_DATA", None, "gate",
                          RULE_VERSION, (), missing=missing,
                          note="Minimum-income gate only; no final KiZ amount.")

    adults = int(round(_amount(evidence, "adults")))
    children = int(round(_amount(evidence, "children")))
    threshold = 600.0 if adults == 1 else 900.0
    relevant_income = (
        _amount(evidence, "employment_gross")
        + _amount(evidence, "alg1_monthly")
        + _amount(evidence, "maintenance")
        + _amount(evidence, "capital_income")
    )
    status = "MEETS_MINIMUM" if children > 0 and relevant_income >= threshold else "BELOW_MINIMUM"
    return Projection(
        "Kinderzuschlag minimum gate", status, round(relevant_income, 2), "EUR/month",
        RULE_VERSION, tuple(sorted(required)),
        excluded=("child_benefit", "housing_benefit", "child_supplement"),
        note=f"Threshold EUR {threshold:.0f}; full KiZ eligibility/amount requires the remaining statutory tests."
    )


def project_wohngeld_income(evidence: Dict[str, EvidenceItem]) -> Projection:
    required = SERVICE_FIELDS["wohngeld_income"]
    missing = _require(evidence, required)
    if missing:
        return Projection("Wohngeld income", "NEEDS_DATA", None, "EUR/month",
                          RULE_VERSION, (), missing=missing,
                          note="Income slice only; no final Wohngeld amount.")

    base = (
        _amount(evidence, "employment_wogg_basis")
        + _amount(evidence, "alg1_monthly")
        + _amount(evidence, "maintenance")
        + _amount(evidence, "capital_income")
    )
    deductions = sum([
        _bool(evidence, "pays_income_tax"),
        _bool(evidence, "pays_health_care"),
        _bool(evidence, "pays_pension"),
    ])
    projected = base * (1.0 - 0.10 * deductions)
    return Projection(
        "Wohngeld income", "READY", round(projected, 2), "EUR/month",
        RULE_VERSION, tuple(sorted(required)),
        excluded=("child_benefit", "child_supplement"),
        note=f"Applied {deductions} x 10% §16 deduction(s); other WoGG allowances/freibetraege remain outside this slice."
    )


def project_alg1_rate(evidence: Dict[str, EvidenceItem]) -> Projection:
    required = SERVICE_FIELDS["alg1_rate"]
    missing = _require(evidence, required)
    if missing:
        return Projection("Arbeitslosengeld I rate", "NEEDS_DATA", None, "EUR/month",
                          RULE_VERSION, (), missing=missing,
                          note="Requires Leistungsentgelt from the upstream SGB III tax/assessment calculation.")

    daily_leistungsentgelt = _amount(evidence, "alg1_leistungsentgelt_daily")
    children = int(round(_amount(evidence, "children")))
    rate = 0.67 if children > 0 else 0.60
    monthly = daily_leistungsentgelt * rate * 30.0
    return Projection(
        "Arbeitslosengeld I rate", "READY", round(monthly, 2), "EUR/month",
        RULE_VERSION, tuple(sorted(required)),
        note=f"Applied official {'67%' if children > 0 else '60%'} rate to supplied Leistungsentgelt; not a full SGB III tax calculation."
    )


def evidence_reuse_rate() -> float:
    """Share of per-service field requests avoided by a shared evidence packet."""
    total_if_separate = sum(len(v) for v in SERVICE_FIELDS.values())
    unique_once = len(set().union(*SERVICE_FIELDS.values()))
    return round(1.0 - unique_once / total_if_separate, 4)
