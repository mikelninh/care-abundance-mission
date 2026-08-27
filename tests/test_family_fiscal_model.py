from engine.family_fiscal_model import (
    HouseholdMicroRow,
    household_incremental_monthly_cost,
    simulate_fiscal_cost,
)
from engine.family_guarantee import FamilyCase, calculate_family_guarantee


def test_existing_support_reduces_incremental_cost_not_target():
    case = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        earned_net=1600,
        single_parent=True,
    )
    care = calculate_family_guarantee(case)
    row = HouseholdMicroRow(case=case, weight=1, existing_means_tested_support=1000)
    assert household_incremental_monthly_cost(row) == round(max(0, care.top_up - 1000), 2)


def test_weighted_annual_cost_is_deterministic():
    case = FamilyCase(
        adults=1,
        child_ages=(5,),
        housing_and_heating=800,
        earned_net=1000,
        single_parent=True,
    )
    care = calculate_family_guarantee(case)
    existing = 400
    result = simulate_fiscal_cost([
        HouseholdMicroRow(case=case, weight=100, existing_means_tested_support=existing)
    ])
    assert result.represented_households == 100
    assert result.annual_existing_support == existing * 12 * 100
    assert result.annual_care_topup_required == care.top_up * 12 * 100
    assert result.annual_incremental_cost == max(0, care.top_up - existing) * 12 * 100


def test_no_fake_savings_if_existing_support_exceeds_care_topup():
    case = FamilyCase(adults=2, child_ages=(4,), housing_and_heating=700, earned_net=4000)
    row = HouseholdMicroRow(case=case, weight=50, existing_means_tested_support=5000)
    assert household_incremental_monthly_cost(row) == 0
    result = simulate_fiscal_cost([row])
    assert result.annual_incremental_cost == 0
    assert result.households_requiring_incremental_topup == 0
