from engine.openwork_engine import FundingSource, Mission, job_transition_required, qualification_path


def test_no_funding_is_red():
    mission = Mission(name="Digital help", hours=10)
    assert mission.state == "RED"
    assert mission.startable is False


def test_nonbinding_money_never_makes_mission_green():
    mission = Mission(
        name="Accessibility checks",
        hours=10,
        funding_sources=[FundingSource("submitted grant", 10000, binding=False, liquid_now=False)],
    )
    assert mission.state == "YELLOW"
    assert mission.startable is False


def test_binding_but_illiquid_money_is_not_startable():
    mission = Mission(
        name="Document support",
        hours=10,
        funding_sources=[FundingSource("approved reimbursement grant", 10000, binding=True, liquid_now=False)],
    )
    assert mission.state == "YELLOW"
    assert mission.startable is False
    assert mission.liquidity_gap > 0


def test_fully_covered_liquid_mission_is_green():
    mission = Mission(
        name="Senior digital support",
        hours=10,
        funding_sources=[FundingSource("reserved payroll account", 10000, binding=True, liquid_now=True)],
    )
    assert mission.state == "GREEN"
    assert mission.startable is True
    assert mission.funding_gap == 0
    assert mission.liquidity_gap == 0


def test_twenty_euro_floor_math():
    mission = Mission(name="OpenWork role", hours=40 * 52, hourly_wage=20)
    assert mission.gross_wages == 41600


def test_job_transition_gate():
    assert job_transition_required(paid_hours=120, recurring_weeks=1)
    assert job_transition_required(paid_hours=20, recurring_weeks=12)
    assert not job_transition_required(paid_hours=119, recurring_weeks=11.9)


def test_regulated_work_cannot_be_unlocked_by_platform_badge():
    result = qualification_path(regulated=True, productive_sample=False)
    assert result["allowed"] is False


def test_productive_sample_is_paid():
    result = qualification_path(regulated=False, productive_sample=True)
    assert result["allowed"] is True
    assert result["sample_must_be_paid"] is True
