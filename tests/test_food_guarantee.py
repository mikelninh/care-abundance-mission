from engine.food_guarantee import FoodAccessCase, FoodGuaranteePolicy, can_claim_no_hunger_due_to_money_or_bureaucracy


def test_child_not_green_if_weekends_uncovered():
    case = FoodAccessCase(
        children=2,
        adults=1,
        cash_food_budget_adequate=False,
        school_or_kita_meals_covered=True,
        evenings_weekends_holidays_covered=False,
        same_day_emergency_access=True,
    )
    assert case.state == "YELLOW"
    assert not can_claim_no_hunger_due_to_money_or_bureaucracy(case)


def test_school_lunch_alone_is_not_a_food_guarantee():
    case = FoodAccessCase(
        children=1,
        adults=1,
        cash_food_budget_adequate=False,
        school_or_kita_meals_covered=True,
        evenings_weekends_holidays_covered=False,
        same_day_emergency_access=False,
    )
    assert case.state == "RED"


def test_full_child_and_household_backstop_is_green():
    case = FoodAccessCase(
        children=2,
        adults=1,
        cash_food_budget_adequate=True,
        school_or_kita_meals_covered=True,
        evenings_weekends_holidays_covered=True,
        same_day_emergency_access=True,
        home_delivery_if_needed=True,
        regulated_diet_supported=True,
    )
    assert case.state == "GREEN"
    assert can_claim_no_hunger_due_to_money_or_bureaucracy(case)


def test_emergency_food_can_cover_cash_failure_same_day():
    case = FoodAccessCase(
        children=0,
        adults=1,
        cash_food_budget_adequate=False,
        school_or_kita_meals_covered=False,
        evenings_weekends_holidays_covered=False,
        same_day_emergency_access=True,
    )
    assert case.household_backstop_guaranteed
    assert case.state == "GREEN"


def test_accessibility_failure_blocks_green():
    case = FoodAccessCase(
        children=1,
        adults=1,
        cash_food_budget_adequate=True,
        school_or_kita_meals_covered=True,
        evenings_weekends_holidays_covered=True,
        same_day_emergency_access=True,
        home_delivery_if_needed=False,
    )
    assert case.state == "YELLOW"


def test_medically_required_diet_failure_blocks_green():
    case = FoodAccessCase(
        children=1,
        adults=1,
        cash_food_budget_adequate=True,
        school_or_kita_meals_covered=True,
        evenings_weekends_holidays_covered=True,
        same_day_emergency_access=True,
        regulated_diet_supported=False,
    )
    assert case.state == "YELLOW"


def test_food_benefit_never_replaces_cash_floor():
    policy = FoodGuaranteePolicy()
    assert policy.cash_first
    assert policy.food_benefit_additional_not_substitute
    assert policy.same_day_emergency_without_full_application
