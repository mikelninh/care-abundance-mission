from engine.income_kernel import EvidenceItem
from engine.income_kernel_v2 import (
    evidence_reuse_rate,
    project_alg1_rate,
    project_grundsicherung,
    project_kiz_minimum,
    project_wohngeld_income,
    sgb2_standard_earned_income_allowance,
)


def ev(**values):
    return {
        k: EvidenceItem(k, float(v), "test", "2026-08", True)
        for k, v in values.items()
    }


def full(**overrides):
    values = dict(
        employment_gross=1400,
        employment_net=1100,
        employment_wogg_basis=1300,
        alg1_monthly=0,
        maintenance=200,
        capital_income=50,
        child_benefit=259,
        child_supplement=0,
        housing_benefit=0,
        has_minor_child=1,
        adults=1,
        children=1,
        pays_income_tax=1,
        pays_health_care=1,
        pays_pension=1,
        alg1_leistungsentgelt_daily=50,
    )
    values.update(overrides)
    return ev(**values)


def test_sgb2_allowance_bands_and_child_extension():
    assert sgb2_standard_earned_income_allowance(100, False) == 100
    assert sgb2_standard_earned_income_allowance(520, False) == 184
    assert sgb2_standard_earned_income_allowance(1000, False) == 328
    assert sgb2_standard_earned_income_allowance(1200, False) == 348
    assert sgb2_standard_earned_income_allowance(1500, True) == 378


def test_grundsicherung_counts_child_benefit_and_uses_earned_allowance():
    result = project_grundsicherung(full())
    assert result.status == "READY"
    assert result.value == 1241


def test_kiz_minimum_excludes_child_benefit_wohngeld_and_kiz_itself():
    a = project_kiz_minimum(full(employment_gross=500, alg1_monthly=100))
    b = project_kiz_minimum(full(
        employment_gross=500, alg1_monthly=100,
        child_benefit=9999, housing_benefit=9999, child_supplement=9999
    ))
    assert a.status == b.status == "MEETS_MINIMUM"
    assert a.value == b.value == 850


def test_kiz_pair_needs_900():
    result = project_kiz_minimum(full(
        adults=2, employment_gross=650, alg1_monthly=0, maintenance=0, capital_income=0
    ))
    assert result.status == "BELOW_MINIMUM"


def test_wohngeld_excludes_child_benefit_and_kiz_and_applies_three_ten_percent_deductions():
    result = project_wohngeld_income(full(
        employment_wogg_basis=1000, alg1_monthly=100,
        maintenance=0, capital_income=0, child_benefit=9000, child_supplement=9000
    ))
    assert result.status == "READY"
    assert result.value == 770


def test_alg1_uses_67_percent_with_child_and_60_without():
    with_child = project_alg1_rate(full(alg1_leistungsentgelt_daily=50, children=1))
    no_child = project_alg1_rate(full(alg1_leistungsentgelt_daily=50, children=0))
    assert with_child.value == 1005
    assert no_child.value == 900


def test_missing_or_unverified_required_fact_fails_closed():
    data = full()
    data["maintenance"] = EvidenceItem("maintenance", 200, "test", "2026-08", False)
    assert project_grundsicherung(data).status == "NEEDS_DATA"
    assert project_kiz_minimum(data).status == "NEEDS_DATA"
    assert project_wohngeld_income(data).status == "NEEDS_DATA"


def test_shared_packet_avoids_repeated_field_collection():
    assert evidence_reuse_rate() > 0.30
