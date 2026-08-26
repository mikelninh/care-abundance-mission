import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from engine.zero_engine import (
    FundingScenario,
    ZeroGuaranteeConfig,
    ZeroHousehold,
    calculate_funding,
    calculate_zero_guarantee,
    modified_oecd_equivalence_scale,
)


def test_modified_oecd_scale_pair_two_small_children():
    assert modified_oecd_equivalence_scale(2, [4, 12]) == 2.1


def test_zero_closes_income_gap_with_65_percent_buffer():
    household = ZeroHousehold(1, (5, 10), 1900, 1100, "Berlin")
    result = calculate_zero_guarantee(household)
    assert result.guarantee_floor_monthly_eur == 2506.4
    assert result.zero_topup_monthly_eur == 606.4
    assert result.income_gap_after_zero_eur == 0
    assert result.protected is True


def test_zero_never_takes_money_away():
    household = ZeroHousehold(2, (4, 12), 5000)
    result = calculate_zero_guarantee(household)
    assert result.zero_topup_monthly_eur == 0


def test_guarantee_cannot_be_below_official_poverty_ratio():
    try:
        ZeroGuaranteeConfig(guarantee_ratio=0.59)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_inheritance_scenarios_are_mutually_exclusive_not_additive():
    balanced = calculate_funding(
        FundingScenario(20, inheritance_mode="diw_balanced")
    )
    full = calculate_funding(
        FundingScenario(20, inheritance_mode="remove_business_privileges")
    )
    assert balanced.inheritance_billion_eur == 2.3
    assert full.inheritance_billion_eur == 7.8
    assert round(
        full.recurring_sources_billion_eur
        - balanced.recurring_sources_billion_eur,
        1,
    ) == 5.5


def test_funding_includes_twenty_percent_reserve():
    result = calculate_funding(
        FundingScenario(20, general_revenue_billion_eur=10)
    )
    assert result.required_with_reserve_billion_eur == 24
    assert result.recurring_sources_billion_eur == 25.3
    assert result.fully_funded is True
