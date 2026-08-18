import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from engine.care_engine import (
    Household,
    RuleEvidence,
    EntitlementRule,
    calculate_household_support,
)


def test_missing_evidence_fails_closed():
    household = Household(1, 2, 2000, 1100, "Berlin")
    report = calculate_household_support(
        household,
        [EntitlementRule("Benefit", None, lambda _: 500)],
    )

    assert report["publishable_total"] is False
    assert report["verified_monthly_total_eur"] == 0


def test_verified_rule_is_publishable():
    household = Household(1, 2, 2000, 1100, "Berlin")
    evidence = RuleEvidence(
        "demo-1",
        "https://example.invalid/rule",
        "2026-01-01",
        None,
        "1",
    )
    report = calculate_household_support(
        household,
        [EntitlementRule("Demo", evidence, lambda _: 123.45)],
    )

    assert report["publishable_total"] is True
    assert report["verified_monthly_total_eur"] == 123.45
