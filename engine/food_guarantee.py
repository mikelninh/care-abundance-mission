from dataclasses import dataclass
from typing import Literal

FoodState = Literal["GREEN", "YELLOW", "RED"]


@dataclass(frozen=True)
class FoodAccessCase:
    children: int
    adults: int
    cash_food_budget_adequate: bool
    school_or_kita_meals_covered: bool
    evenings_weekends_holidays_covered: bool
    same_day_emergency_access: bool
    home_delivery_if_needed: bool = True
    regulated_diet_supported: bool = True

    @property
    def child_daily_access_guaranteed(self) -> bool:
        if self.children == 0:
            return True
        return (
            self.school_or_kita_meals_covered
            and self.evenings_weekends_holidays_covered
            and self.same_day_emergency_access
            and self.home_delivery_if_needed
            and self.regulated_diet_supported
        )

    @property
    def household_backstop_guaranteed(self) -> bool:
        return (
            (self.cash_food_budget_adequate or self.same_day_emergency_access)
            and self.home_delivery_if_needed
            and self.regulated_diet_supported
        )

    @property
    def state(self) -> FoodState:
        if self.child_daily_access_guaranteed and self.household_backstop_guaranteed:
            return "GREEN"
        if self.same_day_emergency_access:
            return "YELLOW"
        return "RED"


@dataclass(frozen=True)
class FoodGuaranteePolicy:
    cash_first: bool = True
    food_benefit_additional_not_substitute: bool = True
    child_meals_no_stigma: bool = True
    same_day_emergency_without_full_application: bool = True
    nutrition_standard_required: bool = True


def can_claim_no_hunger_due_to_money_or_bureaucracy(case: FoodAccessCase) -> bool:
    """Narrow system claim: access is guaranteed against financial/admin failure.

    This is intentionally not a claim that no person can ever feel hunger for any reason.
    """
    return case.state == "GREEN"
