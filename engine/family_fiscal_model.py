from dataclasses import dataclass
from typing import Iterable

from engine.family_guarantee import FamilyCase, calculate_family_guarantee


@dataclass(frozen=True)
class HouseholdMicroRow:
    """One representative household record for fiscal microsimulation.

    weight: number of real households represented by the row.
    existing_means_tested_support: current monthly public cash support that can
    be treated as funding the CARE top-up, excluding Kindergeld (already
    represented explicitly by FamilyCase.child_benefit).
    """

    case: FamilyCase
    weight: float
    existing_means_tested_support: float


@dataclass(frozen=True)
class FiscalResult:
    represented_households: float
    annual_existing_support: float
    annual_care_topup_required: float
    annual_incremental_cost: float
    households_requiring_incremental_topup: float


def household_incremental_monthly_cost(row: HouseholdMicroRow) -> float:
    if row.weight < 0 or row.existing_means_tested_support < 0:
        raise ValueError("weight/support cannot be negative")
    care = calculate_family_guarantee(row.case)
    return round(max(0.0, care.top_up - row.existing_means_tested_support), 2)


def simulate_fiscal_cost(rows: Iterable[HouseholdMicroRow]) -> FiscalResult:
    represented = 0.0
    existing_annual = 0.0
    care_annual = 0.0
    incremental_annual = 0.0
    requiring = 0.0

    for row in rows:
        if row.weight < 0 or row.existing_means_tested_support < 0:
            raise ValueError("weight/support cannot be negative")
        care = calculate_family_guarantee(row.case)
        increment = max(0.0, care.top_up - row.existing_means_tested_support)

        represented += row.weight
        existing_annual += row.existing_means_tested_support * 12 * row.weight
        care_annual += care.top_up * 12 * row.weight
        incremental_annual += increment * 12 * row.weight
        if increment > 0:
            requiring += row.weight

    return FiscalResult(
        represented_households=round(represented, 2),
        annual_existing_support=round(existing_annual, 2),
        annual_care_topup_required=round(care_annual, 2),
        annual_incremental_cost=round(incremental_annual, 2),
        households_requiring_incremental_topup=round(requiring, 2),
    )
