from engine.openwork_engine import FundingSource, Mission, job_transition_required, qualification_path

def test_no_funding_is_red():
    m=Mission(name='x',hours=10); assert m.state=='RED' and not m.startable

def test_nonbinding_never_green():
    m=Mission(name='x',hours=10,funding_sources=[FundingSource('application',10000,False,False)]); assert m.state=='YELLOW' and not m.startable

def test_binding_but_illiquid_not_green():
    m=Mission(name='x',hours=10,funding_sources=[FundingSource('approved reimbursement',10000,True,False)]); assert m.state=='YELLOW' and m.liquidity_gap>0

def test_fully_covered_liquid_is_green():
    m=Mission(name='x',hours=10,funding_sources=[FundingSource('reserved payroll',10000,True,True)]); assert m.state=='GREEN' and m.startable

def test_floor_math():
    assert Mission(name='x',hours=40*52,hourly_wage=20).gross_wages==41600

def test_transition_gate():
    assert job_transition_required(paid_hours=120,recurring_weeks=1)
    assert job_transition_required(paid_hours=1,recurring_weeks=12)
    assert not job_transition_required(paid_hours=119,recurring_weeks=11.9)

def test_regulated_boundary():
    assert qualification_path(regulated=True,productive_sample=False)['allowed'] is False

def test_productive_sample_paid():
    assert qualification_path(regulated=False,productive_sample=True)['sample_must_be_paid'] is True

def test_100_nonbinding_cases():
    for i in range(100):
        m=Mission(name=str(i),hours=10+i,hourly_wage=20+(i%5),funding_sources=[FundingSource('likely money',1_000_000,False,False)])
        assert m.state=='YELLOW' and not m.startable

def test_100_liquidity_cases():
    for i in range(100):
        probe=Mission(name='p',hours=20+i,hourly_wage=20+(i%9),training_cost=100+i,supervision_cost=200+2*i,equipment_admin_cost=50+i)
        required=probe.fully_loaded_cost
        illiquid=Mission(name='i',hours=probe.hours,hourly_wage=probe.hourly_wage,training_cost=probe.training_cost,supervision_cost=probe.supervision_cost,equipment_admin_cost=probe.equipment_admin_cost,funding_sources=[FundingSource('approved',required,True,False)])
        assert illiquid.state=='YELLOW'
        green=Mission(name='g',hours=probe.hours,hourly_wage=probe.hourly_wage,training_cost=probe.training_cost,supervision_cost=probe.supervision_cost,equipment_admin_cost=probe.equipment_admin_cost,funding_sources=[FundingSource('reserved',required,True,True)])
        assert green.state=='GREEN' and green.startable
