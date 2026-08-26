from engine.family_guarantee import FamilyCase, calculate_family_guarantee, maximum_safe_recovery


def show(name: str, case: FamilyCase):
    result = calculate_family_guarantee(case)
    print(
        f"{name}: floor={result.base_floor:.2f} "
        f"child_base={result.protected_child_base:.2f} "
        f"top_up={result.top_up:.2f} "
        f"disposable={result.disposable_after_guarantee:.2f} "
        f"guaranteed={result.guaranteed}"
    )
    return result


def main():
    no_income = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        earned_net=0,
        single_parent=True,
    )
    working = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        earned_net=1600,
        single_parent=True,
    )
    more_work = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        earned_net=1700,
        single_parent=True,
    )

    a = show("NO_INCOME", no_income)
    b = show("WORKING", working)
    c = show("MORE_WORK", more_work)

    assert a.guaranteed and b.guaranteed and c.guaranteed
    assert c.disposable_after_guarantee > b.disposable_after_guarantee
    assert round(c.disposable_after_guarantee - b.disposable_after_guarantee, 2) == 35.0

    # Income shock: support rises automatically to keep the household protected.
    job_loss = FamilyCase(
        adults=1,
        child_ages=(5, 10),
        housing_and_heating=1100,
        earned_net=300,
        single_parent=True,
    )
    d = show("INCOME_SHOCK", job_loss)
    assert d.guaranteed
    assert d.top_up > b.top_up

    # A good-faith recovery can only use money above the protected target.
    safe_recovery = maximum_safe_recovery(
        c.disposable_after_guarantee,
        c.target_after_guarantee,
    )
    print(f"MAX_SAFE_RECOVERY={safe_recovery:.2f}")
    assert c.disposable_after_guarantee - safe_recovery >= c.target_after_guarantee

    print("FAMILY_GUARANTEE_E2E=PASS")


if __name__ == "__main__":
    main()
