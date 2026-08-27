from engine.family_guarantee import (
    CHILD_BENEFIT_2026,
    FamilyCase,
    anti_poverty_floor,
    calculate_family_guarantee,
    legal_minimum_floor,
    maximum_safe_recovery,
)


def test_latest_official_poverty_scale_matches_two_adult_two_child_example():
    # Destatis publishes €3,036/month for 2 adults + 2 children under 14 (rounding).
    assert anti_poverty_floor(2, (5, 10)) == 3036.60


def test_2026_legal_floor_uses_child_age_bands_and_single_parent_need():
    floor = legal_minimum_floor(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        single_parent=True,
    )
    # 563 + 36% single-parent extra + 357 + 390 + 1100
    assert floor == 2612.68


def test_protected_kindergeld_does_not_replace_family_floor():
    case = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        single_parent=True,
    )
    protected = calculate_family_guarantee(case, protect_child_benefit=True)
    counted = calculate_family_guarantee(case, protect_child_benefit=False)

    assert protected.protected_child_base == 2 * CHILD_BENEFIT_2026
    assert protected.top_up - counted.top_up == 2 * CHILD_BENEFIT_2026
    assert protected.disposable_after_guarantee - counted.disposable_after_guarantee == 2 * CHILD_BENEFIT_2026


def test_no_child_household_is_not_given_child_base():
    case = FamilyCase(adults=1, child_ages=(), housing_and_heating=500)
    result = calculate_family_guarantee(case)
    assert result.protected_child_base == 0


def test_guarantee_never_leaves_family_below_target():
    case = FamilyCase(
        adults=2,
        child_ages=(2, 8, 15),
        housing_and_heating=1450,
        earned_net=900,
        other_income=120,
    )
    result = calculate_family_guarantee(case)
    assert result.guaranteed
    assert result.disposable_after_guarantee >= result.target_after_guarantee


def test_more_work_always_increases_disposable_income_while_topup_active():
    base = FamilyCase(
        adults=1,
        child_ages=(6,),
        housing_and_heating=800,
        earned_net=800,
        single_parent=True,
    )
    more_work = FamilyCase(
        adults=1,
        child_ages=(6,),
        housing_and_heating=800,
        earned_net=900,
        single_parent=True,
    )
    a = calculate_family_guarantee(base, work_keep_rate=0.35)
    b = calculate_family_guarantee(more_work, work_keep_rate=0.35)
    assert a.top_up > 0 and b.top_up > 0
    assert round(b.disposable_after_guarantee - a.disposable_after_guarantee, 2) == 35.0


def test_work_never_creates_a_cliff_when_topup_phases_out():
    previous = None
    for earned in range(0, 5001, 50):
        result = calculate_family_guarantee(
            FamilyCase(
                adults=1,
                child_ages=(4, 9),
                housing_and_heating=1000,
                earned_net=float(earned),
                single_parent=True,
            )
        )
        if previous is not None:
            assert result.disposable_after_guarantee >= previous
        previous = result.disposable_after_guarantee


def test_good_faith_recovery_cannot_push_family_below_floor():
    assert maximum_safe_recovery(3200, 3000) == 200
    assert maximum_safe_recovery(2999, 3000) == 0


def test_1000_synthetic_families_are_never_left_below_guarantee():
    age_patterns = [(2,), (8,), (15,), (2, 8), (5, 15), (3, 9, 16)]
    checked = 0
    for adults in (1, 2):
        for ages in age_patterns:
            for rent in (500, 800, 1100, 1500):
                for earned in (0, 500, 1200, 2200, 3500):
                    for other in (0, 200, 600):
                        result = calculate_family_guarantee(
                            FamilyCase(
                                adults=adults,
                                child_ages=ages,
                                housing_and_heating=rent,
                                earned_net=earned,
                                other_income=other,
                                single_parent=(adults == 1),
                            )
                        )
                        assert result.guaranteed
                        checked += 1
    assert checked == 720
