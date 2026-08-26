from __future__ import annotations

import json
from pathlib import Path

from engine.zero_engine import (
    FundingScenario,
    ZeroHousehold,
    calculate_funding,
    calculate_zero_guarantee,
)

ROOT = Path(__file__).parents[1]


def run_households() -> list[dict]:
    payload = json.loads((ROOT / "data" / "zero_synthetic_households.json").read_text())
    rows = []
    for item in payload["households"]:
        household = ZeroHousehold(
            adults=item["adults"],
            child_ages=tuple(item["child_ages"]),
            disposable_income_monthly_eur=item["disposable_income_monthly_eur"],
            housing_cost_monthly_eur=item["housing_cost_monthly_eur"],
            city=item["city"],
        )
        result = calculate_zero_guarantee(household)
        rows.append(
            {
                "id": item["id"],
                "city": item["city"],
                "floor_eur": result.guarantee_floor_monthly_eur,
                "topup_eur": result.zero_topup_monthly_eur,
                "gap_after_eur": result.income_gap_after_zero_eur,
                "protected": result.protected,
            }
        )
    return rows


def run_funding() -> list[dict]:
    rows = []
    for cost in (15, 20, 25, 30):
        result = calculate_funding(FundingScenario(cost))
        rows.append(
            {
                "annual_zero_cost_billion_eur": cost,
                "required_with_20pct_reserve_billion_eur": result.required_with_reserve_billion_eur,
                "reference_sources_billion_eur": result.recurring_sources_billion_eur,
                "coverage_percent": round(result.coverage_ratio * 100, 1),
                "surplus_or_gap_billion_eur": result.surplus_or_gap_billion_eur,
            }
        )
    return rows


if __name__ == "__main__":
    print(json.dumps({"households": run_households(), "funding": run_funding()}, indent=2))
