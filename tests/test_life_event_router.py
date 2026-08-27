from engine.income_kernel import EvidenceItem
from engine.life_event_router import route_income_loss


def item(key, value, verified=True):
    return EvidenceItem(key, float(value), "synthetic-life-event-test", "2026-08", verified)


def base_packet(children=1, insured_months=18):
    gross = 2200
    net = 1716
    return {
        "employment_gross": item("employment_gross", gross),
        "employment_net": item("employment_net", net),
        "employment_wogg_basis": item("employment_wogg_basis", 2100),
        "alg1_monthly": item("alg1_monthly", 0),
        "maintenance": item("maintenance", 250 if children else 0),
        "capital_income": item("capital_income", 0),
        "child_benefit": item("child_benefit", 259 * children),
        "child_supplement": item("child_supplement", 0),
        "housing_benefit": item("housing_benefit", 0),
        "has_minor_child": item("has_minor_child", int(children > 0)),
        "adults": item("adults", 1),
        "children": item("children", children),
        "pays_income_tax": item("pays_income_tax", 1),
        "pays_health_care": item("pays_health_care", 1),
        "pays_pension": item("pays_pension", 1),
        "alg1_leistungsentgelt_daily": item("alg1_leistungsentgelt_daily", net / 30),
        "insured_months_30": item("insured_months_30", insured_months),
        "registered_unemployed": item("registered_unemployed", 1),
        "available_15h": item("available_15h", 1),
    }


def by_service(plan):
    return {route.service: route for route in plan.routes}


def test_one_life_event_generates_four_coordinated_routes():
    plan = route_income_loss(base_packet())
    routes = by_service(plan)
    assert set(routes) == {
        "Arbeitslosengeld I",
        "Kinderzuschlag",
        "Wohngeld",
        "Grundsicherungsgeld",
    }
    assert routes["Arbeitslosengeld I"].state == "CHECK_NOW"
    assert routes["Kinderzuschlag"].state == "CHECK_PARALLEL"
    assert routes["Wohngeld"].state == "CHECK_PARALLEL"
    assert routes["Grundsicherungsgeld"].state == "SAFETY_NET_CHECK"


def test_missing_alg1_gate_fact_is_asked_for_instead_of_invented():
    evidence = base_packet()
    evidence["insured_months_30"] = item("insured_months_30", 18, verified=False)
    plan = route_income_loss(evidence)
    alg1 = by_service(plan)["Arbeitslosengeld I"]
    assert alg1.state == "NEEDS_DATA"
    assert "insured_months_30" in plan.missing_shared_fields


def test_no_child_removes_kiz_route_without_breaking_other_checks():
    plan = route_income_loss(base_packet(children=0))
    routes = by_service(plan)
    assert routes["Kinderzuschlag"].state == "NOT_APPLICABLE"
    assert routes["Arbeitslosengeld I"].state == "CHECK_NOW"
    assert routes["Wohngeld"].projection.status == "READY"
    assert routes["Grundsicherungsgeld"].projection.status == "READY"


def test_standard_alg1_gate_failure_keeps_safety_net_visible():
    plan = route_income_loss(base_packet(insured_months=6))
    routes = by_service(plan)
    assert routes["Arbeitslosengeld I"].state == "STANDARD_GATE_NOT_MET"
    assert routes["Grundsicherungsgeld"].state == "SAFETY_NET_CHECK"


def test_verified_packet_is_reused_across_routes():
    evidence = base_packet()
    plan = route_income_loss(evidence)
    assert "employment_gross" in plan.reused_verified_fields
    assert "children" in plan.reused_verified_fields
    assert "alg1_leistungsentgelt_daily" in plan.reused_verified_fields
    assert len(plan.reused_verified_fields) >= 15
