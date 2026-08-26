from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal


OECDChildAge = int


@dataclass(frozen=True)
class ZeroHousehold:
    adults: int
    child_ages: tuple[OECDChildAge, ...]
    disposable_income_monthly_eur: float
    housing_cost_monthly_eur: float = 0.0
    city: str = "Germany"

    def __post_init__(self) -> None:
        if self.adults < 1:
            raise ValueError("household must contain at least one adult")
        if any(age < 0 or age > 17 for age in self.child_ages):
            raise ValueError("child ages must be between 0 and 17")
        if self.disposable_income_monthly_eur < 0:
            raise ValueError("disposable income cannot be negative")
        if self.housing_cost_monthly_eur < 0:
            raise ValueError("housing cost cannot be negative")


@dataclass(frozen=True)
class ZeroGuaranteeConfig:
    # Destatis EU-SILC 2025 poverty-risk threshold for one person (60% median).
    official_single_threshold_monthly_eur: float = 1446.0
    official_ratio: float = 0.60
    # ZERO uses a buffer above the statistical poverty line by default.
    guarantee_ratio: float = 0.65
    version: str = "DE-EUSILC-2025-ZERO-V1"

    def __post_init__(self) -> None:
        if self.official_single_threshold_monthly_eur <= 0:
            raise ValueError("threshold must be positive")
        if not 0 < self.official_ratio <= 1:
            raise ValueError("official_ratio must be between 0 and 1")
        if self.guarantee_ratio < self.official_ratio:
            raise ValueError(
                "ZERO guarantee must not be below the official poverty threshold ratio"
            )


@dataclass(frozen=True)
class ZeroResult:
    equivalence_scale: float
    official_poverty_threshold_monthly_eur: float
    guarantee_floor_monthly_eur: float
    disposable_income_monthly_eur: float
    zero_topup_monthly_eur: float
    income_gap_after_zero_eur: float
    protected: bool
    config_version: str


def modified_oecd_equivalence_scale(adults: int, child_ages: Iterable[int]) -> float:
    """Modified OECD scale used by EU-SILC: 1.0 first adult, 0.5 other 14+, 0.3 under 14."""
    if adults < 1:
        raise ValueError("at least one adult is required")
    scale = 1.0 + 0.5 * (adults - 1)
    for age in child_ages:
        if age < 0 or age > 17:
            raise ValueError("child ages must be between 0 and 17")
        scale += 0.3 if age < 14 else 0.5
    return round(scale, 4)


def calculate_zero_guarantee(
    household: ZeroHousehold,
    config: ZeroGuaranteeConfig = ZeroGuaranteeConfig(),
) -> ZeroResult:
    """Close the household's measured income gap to the ZERO floor exactly.

    `disposable_income_monthly_eur` is deliberately an after-tax, after-existing-
    transfers input. This prevents the V1 engine from pretending it already has a
    complete legal calculator for every German benefit. CARE's existing rule engine
    remains responsible for producing that verified input as coverage expands.
    """
    scale = modified_oecd_equivalence_scale(household.adults, household.child_ages)
    official_threshold = config.official_single_threshold_monthly_eur * scale
    guarantee_single = (
        config.official_single_threshold_monthly_eur
        * config.guarantee_ratio
        / config.official_ratio
    )
    guarantee_floor = guarantee_single * scale
    topup = max(0.0, guarantee_floor - household.disposable_income_monthly_eur)
    after = household.disposable_income_monthly_eur + topup
    gap_after = max(0.0, guarantee_floor - after)
    return ZeroResult(
        equivalence_scale=scale,
        official_poverty_threshold_monthly_eur=round(official_threshold, 2),
        guarantee_floor_monthly_eur=round(guarantee_floor, 2),
        disposable_income_monthly_eur=round(household.disposable_income_monthly_eur, 2),
        zero_topup_monthly_eur=round(topup, 2),
        income_gap_after_zero_eur=round(gap_after, 2),
        protected=gap_after < 0.01,
        config_version=config.version,
    )


InheritanceMode = Literal["diw_balanced", "remove_business_privileges"]


@dataclass(frozen=True)
class FundingScenario:
    annual_zero_cost_billion_eur: float
    # Conservative reference from DIW 2021 long-run / annual-equivalent modelling:
    # €2m personal + €5m business-asset allowances -> about €13bn/year equivalent.
    # This is a reference scenario, not a 2026 revenue forecast.
    wealth_tax_reference_billion_eur: float = 13.0
    inheritance_mode: InheritanceMode = "diw_balanced"
    high_income_reform_billion_eur: float = 0.0
    admin_or_compliance_billion_eur: float = 0.0
    general_revenue_billion_eur: float = 0.0
    reserve_ratio: float = 0.20

    def __post_init__(self) -> None:
        for name in (
            "annual_zero_cost_billion_eur",
            "wealth_tax_reference_billion_eur",
            "high_income_reform_billion_eur",
            "admin_or_compliance_billion_eur",
            "general_revenue_billion_eur",
        ):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} cannot be negative")
        if self.reserve_ratio < 0:
            raise ValueError("reserve_ratio cannot be negative")
        if self.inheritance_mode not in {
            "diw_balanced",
            "remove_business_privileges",
        }:
            raise ValueError("unsupported inheritance mode")


@dataclass(frozen=True)
class FundingResult:
    required_with_reserve_billion_eur: float
    recurring_sources_billion_eur: float
    inheritance_billion_eur: float
    coverage_ratio: float
    surplus_or_gap_billion_eur: float
    fully_funded: bool


def inheritance_reference_yield(mode: InheritanceMode) -> float:
    # Mutually exclusive DIW 2026 scenarios; never add both.
    return 2.3 if mode == "diw_balanced" else 7.8


def calculate_funding(scenario: FundingScenario) -> FundingResult:
    inheritance = inheritance_reference_yield(scenario.inheritance_mode)
    recurring_sources = (
        scenario.wealth_tax_reference_billion_eur
        + inheritance
        + scenario.high_income_reform_billion_eur
        + scenario.admin_or_compliance_billion_eur
        + scenario.general_revenue_billion_eur
    )
    required = scenario.annual_zero_cost_billion_eur * (1 + scenario.reserve_ratio)
    coverage = 1.0 if required == 0 else recurring_sources / required
    balance = recurring_sources - required
    return FundingResult(
        required_with_reserve_billion_eur=round(required, 2),
        recurring_sources_billion_eur=round(recurring_sources, 2),
        inheritance_billion_eur=inheritance,
        coverage_ratio=round(coverage, 4),
        surplus_or_gap_billion_eur=round(balance, 2),
        fully_funded=balance >= -1e-9,
    )
