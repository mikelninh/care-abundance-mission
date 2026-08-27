from dataclasses import dataclass
from typing import Sequence

# Verified public baselines for 2026 / latest published poverty threshold.
CHILD_BENEFIT_2026 = 259.0
POVERTY_SINGLE_MONTHLY_LATEST = 1446.0  # Destatis EU-SILC 2025, published 2026

REGELBEDARF_2026 = {
    "adult_single": 563.0,
    "adult_partner": 506.0,
    "child_0_5": 357.0,
    "child_6_13": 390.0,
    "child_14_17": 471.0,
}

DEFAULT_WORK_KEEP_RATE = 0.35


def child_regelbedarf(age: int) -> float:
    if age < 0:
        raise ValueError("age must be >= 0")
    if age <= 5:
        return REGELBEDARF_2026["child_0_5"]
    if age <= 13:
        return REGELBEDARF_2026["child_6_13"]
    return REGELBEDARF_2026["child_14_17"]


def modified_oecd_scale(adults: int, child_ages: Sequence[int]) -> float:
    """Modified OECD equivalence scale used for poverty comparisons.

    First adult: 1.0; additional adults: 0.5; children <14: 0.3;
    children 14+: 0.5.
    """
    if adults < 1:
        raise ValueError("a family household must contain at least one adult")
    scale = 1.0 + max(0, adults - 1) * 0.5
    scale += sum(0.3 if age < 14 else 0.5 for age in child_ages)
    return scale


def anti_poverty_floor(adults: int, child_ages: Sequence[int]) -> float:
    """Monthly household threshold using the latest published Destatis baseline."""
    return round(POVERTY_SINGLE_MONTHLY_LATEST * modified_oecd_scale(adults, child_ages), 2)


def single_parent_extra_rate(child_ages: Sequence[int]) -> float:
    """2026 SGB-II single-parent extra-need examples, simplified for minors.

    This covers the common configurations needed for the V0 family-floor guardrail.
    Complex shared-care / exceptional cases must be supplied as additional_needs.
    """
    n = len(child_ages)
    if n == 0:
        return 0.0
    if n >= 5:
        return 0.60
    if n == 4:
        return 0.48
    if n in (2, 3) and all(age < 16 for age in child_ages):
        return 0.36
    if n == 2 and all(age >= 16 for age in child_ages):
        return 0.24
    if n == 1:
        return 0.36 if child_ages[0] < 7 else 0.12
    # Conservative V0 fallback for mixed configurations; exact legal engine may override.
    return min(0.60, 0.12 * n)


def legal_minimum_floor(
    adults: int,
    child_ages: Sequence[int],
    housing_and_heating: float,
    single_parent: bool = False,
    additional_needs: float = 0.0,
) -> float:
    if adults < 1:
        raise ValueError("adults must be >= 1")
    if housing_and_heating < 0 or additional_needs < 0:
        raise ValueError("costs cannot be negative")

    adult_need = (
        REGELBEDARF_2026["adult_single"]
        if adults == 1
        else REGELBEDARF_2026["adult_partner"] * adults
    )
    child_need = sum(child_regelbedarf(age) for age in child_ages)
    single_parent_need = 0.0
    if single_parent:
        if adults != 1:
            raise ValueError("single_parent requires adults == 1")
        single_parent_need = REGELBEDARF_2026["adult_single"] * single_parent_extra_rate(child_ages)

    return round(
        adult_need
        + child_need
        + housing_and_heating
        + single_parent_need
        + additional_needs,
        2,
    )


def family_security_floor(
    adults: int,
    child_ages: Sequence[int],
    housing_and_heating: float,
    single_parent: bool = False,
    additional_needs: float = 0.0,
) -> float:
    """Use whichever floor protects the household more: legal minimum or poverty floor."""
    return max(
        anti_poverty_floor(adults, child_ages),
        legal_minimum_floor(
            adults,
            child_ages,
            housing_and_heating,
            single_parent=single_parent,
            additional_needs=additional_needs,
        ),
    )


@dataclass(frozen=True)
class FamilyCase:
    adults: int
    child_ages: tuple[int, ...]
    housing_and_heating: float
    earned_net: float = 0.0
    other_income: float = 0.0
    single_parent: bool = False
    additional_needs: float = 0.0
    child_benefit_per_child: float = CHILD_BENEFIT_2026

    @property
    def child_benefit(self) -> float:
        return self.child_benefit_per_child * len(self.child_ages)


@dataclass(frozen=True)
class GuaranteeResult:
    base_floor: float
    protected_child_base: float
    target_after_guarantee: float
    top_up: float
    disposable_after_guarantee: float
    work_bonus_retained: float
    guaranteed: bool


def calculate_family_guarantee(
    case: FamilyCase,
    *,
    protect_child_benefit: bool = True,
    work_keep_rate: float = DEFAULT_WORK_KEEP_RATE,
) -> GuaranteeResult:
    """Calculate the proposed automatic Family Guarantee.

    Design rules:
    - the household base floor is max(legal minimum, latest poverty threshold);
    - if protect_child_benefit=True, universal child benefit sits on top of that floor;
    - earned net income is tapered rather than offset 1:1, so work always raises disposable income;
    - this is a policy prototype, not current entitlement law.
    """
    if not 0 <= work_keep_rate <= 1:
        raise ValueError("work_keep_rate must be between 0 and 1")
    if case.earned_net < 0 or case.other_income < 0:
        raise ValueError("income cannot be negative")

    base_floor = family_security_floor(
        case.adults,
        case.child_ages,
        case.housing_and_heating,
        single_parent=case.single_parent,
        additional_needs=case.additional_needs,
    )
    protected_child_base = case.child_benefit if protect_child_benefit else 0.0
    target = base_floor + protected_child_base

    # Non-work income is counted fully. Earnings reduce support only by (1 - keep rate).
    countable_resources = (
        case.other_income
        + case.child_benefit
        + case.earned_net * (1.0 - work_keep_rate)
    )
    top_up = max(0.0, target - countable_resources)
    disposable = case.earned_net + case.other_income + case.child_benefit + top_up
    work_bonus = case.earned_net * work_keep_rate if top_up > 0 else max(0.0, disposable - target)

    return GuaranteeResult(
        base_floor=round(base_floor, 2),
        protected_child_base=round(protected_child_base, 2),
        target_after_guarantee=round(target, 2),
        top_up=round(top_up, 2),
        disposable_after_guarantee=round(disposable, 2),
        work_bonus_retained=round(work_bonus, 2),
        guaranteed=disposable + 1e-9 >= target,
    )


def maximum_safe_recovery(disposable_before_recovery: float, guaranteed_target: float) -> float:
    """Good-faith recovery may never push a family below the protected target."""
    return round(max(0.0, disposable_before_recovery - guaranteed_target), 2)
