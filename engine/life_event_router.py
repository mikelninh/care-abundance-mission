"""Life-event routing proof for an income shock.

This module demonstrates the product idea behind a proactive social-state journey:
a citizen reports the life event (income loss) once; a shared evidence packet is
reused to prepare checks across ALG I, Kinderzuschlag, Wohngeld and
Grundsicherungsgeld.

It is intentionally a routing/precheck layer, NOT a final entitlement engine.
Final legal decisions remain with the competent service and require the full
statutory facts for that service.
"""

from dataclasses import dataclass
import math
from typing import Dict, Tuple

from engine.income_kernel import EvidenceItem
from engine.income_kernel_v2 import (
    Projection,
    project_alg1_rate,
    project_grundsicherung,
    project_kiz_minimum,
    project_wohngeld_income,
)


@dataclass(frozen=True)
class ServiceRoute:
    service: str
    state: str
    reason: str
    projection: Projection | None
    remaining_for_full_check: Tuple[str, ...] = ()


@dataclass(frozen=True)
class LifeEventPlan:
    event: str
    routes: Tuple[ServiceRoute, ...]
    reused_verified_fields: Tuple[str, ...]
    missing_shared_fields: Tuple[str, ...]
    note: str = (
        "Routing/precheck only. A route is not a legal entitlement decision."
    )


_BOOLEAN_FIELDS = frozenset({
    "registered_unemployed",
    "available_15h",
    "has_minor_child",
    "pays_income_tax",
    "pays_health_care",
    "pays_pension",
})
_INTEGER_FIELDS = frozenset({"adults", "children", "insured_months_30"})


def _validate_evidence(evidence: Dict[str, EvidenceItem]) -> None:
    """Reject structurally impossible evidence instead of silently calculating.

    Unknown or unverified is allowed and handled by the downstream NEEDS_DATA
    states. Structurally invalid values are different: negative money/counts,
    NaN/Infinity, mismatched provenance keys or non-boolean flags would poison
    every coordinated route, so the router fails closed before reuse.
    """
    for key, item in evidence.items():
        if item.key != key:
            raise ValueError(f"evidence key mismatch: map={key!r}, item={item.key!r}")
        value = float(item.monthly_amount)
        if not math.isfinite(value):
            raise ValueError(f"{key} must be finite")
        if value < 0:
            raise ValueError(f"{key} must be >= 0")
        if key in _BOOLEAN_FIELDS and value not in (0.0, 1.0):
            raise ValueError(f"{key} must be 0 or 1")
        if key in _INTEGER_FIELDS and not value.is_integer():
            raise ValueError(f"{key} must be an integer")

    if "adults" in evidence and evidence["adults"].verified and _value(evidence, "adults") < 1:
        raise ValueError("adults must be >= 1 for this household slice")
    if "insured_months_30" in evidence and evidence["insured_months_30"].verified and _value(evidence, "insured_months_30") > 30:
        raise ValueError("insured_months_30 must be <= 30")


def _verified(evidence: Dict[str, EvidenceItem], key: str) -> bool:
    return key in evidence and evidence[key].verified


def _value(evidence: Dict[str, EvidenceItem], key: str) -> float:
    return evidence[key].monthly_amount


def _alg1_precheck(evidence: Dict[str, EvidenceItem]) -> ServiceRoute:
    gate_fields = ("insured_months_30", "registered_unemployed", "available_15h")
    missing = tuple(k for k in gate_fields if not _verified(evidence, k))
    projection = project_alg1_rate(evidence)

    if missing:
        return ServiceRoute(
            "Arbeitslosengeld I",
            "NEEDS_DATA",
            "The basic ALG-I precheck needs the missing insurance/registration fact(s).",
            projection,
            remaining_for_full_check=missing,
        )

    standard_gate = (
        _value(evidence, "insured_months_30") >= 12
        and bool(round(_value(evidence, "registered_unemployed")))
        and bool(round(_value(evidence, "available_15h")))
    )
    if not standard_gate:
        return ServiceRoute(
            "Arbeitslosengeld I",
            "STANDARD_GATE_NOT_MET",
            "The standard 12-in-30-month / registration / availability precheck is not met. Special cases remain outside this slice.",
            projection,
            remaining_for_full_check=("special_cases_or_short_qualifying_period",),
        )

    return ServiceRoute(
        "Arbeitslosengeld I",
        "CHECK_NOW",
        "Standard ALG-I precheck is positive; prepare the full claim journey first.",
        projection,
        remaining_for_full_check=(
            "full_employment_history",
            "termination_and_blocking_period_facts",
        ),
    )


def _kiz_route(evidence: Dict[str, EvidenceItem]) -> ServiceRoute:
    projection = project_kiz_minimum(evidence)
    children = int(round(_value(evidence, "children"))) if _verified(evidence, "children") else None
    if children == 0:
        return ServiceRoute(
            "Kinderzuschlag",
            "NOT_APPLICABLE",
            "No child is present in the shared household packet.",
            projection,
        )
    if projection.status == "NEEDS_DATA":
        return ServiceRoute(
            "Kinderzuschlag",
            "NEEDS_DATA",
            "The minimum-income gate cannot be checked from the current verified packet.",
            projection,
            remaining_for_full_check=projection.missing,
        )
    if projection.status == "BELOW_MINIMUM":
        return ServiceRoute(
            "Kinderzuschlag",
            "MINIMUM_GATE_NOT_MET",
            "The statutory minimum-income gate is not met in this slice; do not pretend full KiZ eligibility.",
            projection,
        )
    return ServiceRoute(
        "Kinderzuschlag",
        "CHECK_PARALLEL",
        "The minimum-income gate is met; continue with the full family/housing/assets tests.",
        projection,
        remaining_for_full_check=(
            "child_and_parent_income_taper_facts",
            "housing_and_family_need",
            "assets_if_relevant",
        ),
    )


def _wohngeld_route(evidence: Dict[str, EvidenceItem]) -> ServiceRoute:
    projection = project_wohngeld_income(evidence)
    if projection.status == "NEEDS_DATA":
        return ServiceRoute(
            "Wohngeld",
            "NEEDS_DATA",
            "The Wohngeld income slice cannot be prepared from the current verified packet.",
            projection,
            remaining_for_full_check=projection.missing,
        )
    return ServiceRoute(
        "Wohngeld",
        "CHECK_PARALLEL",
        "The reusable income projection is ready; the housing-specific facts remain for the full check.",
        projection,
        remaining_for_full_check=(
            "eligible_household_members",
            "eligible_rent_or_burden",
            "municipality_rent_level",
            "remaining_wogg_allowances",
        ),
    )


def _grundsicherung_route(evidence: Dict[str, EvidenceItem]) -> ServiceRoute:
    projection = project_grundsicherung(evidence)
    if projection.status == "NEEDS_DATA":
        return ServiceRoute(
            "Grundsicherungsgeld",
            "NEEDS_DATA",
            "The countable-income slice needs additional verified facts before a safety-net check can be prepared.",
            projection,
            remaining_for_full_check=projection.missing,
        )
    return ServiceRoute(
        "Grundsicherungsgeld",
        "SAFETY_NET_CHECK",
        "Prepare the means-tested safety-net check because ALG I can be absent or insufficient; final need is not inferred here.",
        projection,
        remaining_for_full_check=(
            "household_need",
            "housing_and_heating_costs",
            "assets_and_exemptions",
            "additional_needs_if_any",
        ),
    )


def route_income_loss(evidence: Dict[str, EvidenceItem]) -> LifeEventPlan:
    """Prepare four coordinated routes from one verified evidence packet."""
    _validate_evidence(evidence)
    routes = (
        _alg1_precheck(evidence),
        _kiz_route(evidence),
        _wohngeld_route(evidence),
        _grundsicherung_route(evidence),
    )
    reused = tuple(sorted(k for k, v in evidence.items() if v.verified))
    missing_shared = tuple(sorted({
        field
        for route in routes
        if route.state == "NEEDS_DATA"
        for field in route.remaining_for_full_check
    }))
    return LifeEventPlan(
        event="income_loss",
        routes=routes,
        reused_verified_fields=reused,
        missing_shared_fields=missing_shared,
    )
