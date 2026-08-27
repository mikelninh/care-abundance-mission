"""Run the V2 realism proof and print reproducible metrics."""
from engine.income_kernel import EvidenceItem
from engine.income_kernel_v2 import (
    SERVICE_FIELDS,
    evidence_reuse_rate,
    project_alg1_rate,
    project_grundsicherung,
    project_kiz_minimum,
    project_wohngeld_income,
)
from engine.life_event_router import route_income_loss
from engine.rights_safe_policy_v2 import run_eval


def item(key, value, verified=True):
    return EvidenceItem(key, float(value), "synthetic-eval-fixture", "2026-08", verified)


def household(i: int):
    adults = 1 if i % 3 == 0 else 2
    children = i % 3
    gross_levels = [0, 650, 950, 1400, 2200, 3200]
    gross = gross_levels[i % len(gross_levels)]
    net = gross * 0.78
    alg1 = 900 if i % 8 == 0 else 0
    maintenance = 250 if adults == 1 and children else 0
    capital = 80 if i % 7 == 0 else 0
    insured_months = 6 if i % 5 == 0 else 18
    evidence = {
        "employment_gross": item("employment_gross", gross),
        "employment_net": item("employment_net", net),
        "employment_wogg_basis": item("employment_wogg_basis", max(0, gross - 100)),
        "alg1_monthly": item("alg1_monthly", alg1),
        "maintenance": item("maintenance", maintenance),
        "capital_income": item("capital_income", capital),
        "child_benefit": item("child_benefit", 259 * children),
        "child_supplement": item("child_supplement", 0),
        "housing_benefit": item("housing_benefit", 0),
        "has_minor_child": item("has_minor_child", int(children > 0)),
        "adults": item("adults", adults),
        "children": item("children", children),
        "pays_income_tax": item("pays_income_tax", int(gross >= 1400)),
        "pays_health_care": item("pays_health_care", int(gross > 0)),
        "pays_pension": item("pays_pension", int(gross > 0)),
        "alg1_leistungsentgelt_daily": item(
            "alg1_leistungsentgelt_daily", (net / 30.0) if gross > 0 else 0
        ),
        "insured_months_30": item("insured_months_30", insured_months),
        "registered_unemployed": item("registered_unemployed", 1),
        "available_15h": item("available_15h", 1),
    }
    if i % 11 == 0:
        evidence["maintenance"] = item("maintenance", maintenance, verified=False)
    if i % 13 == 0:
        evidence["insured_months_30"] = item("insured_months_30", insured_months, verified=False)
    return evidence


def main():
    cases = [household(i) for i in range(48)]
    projections = []
    plans = []
    for ev in cases:
        projections.extend([
            project_grundsicherung(ev),
            project_kiz_minimum(ev),
            project_wohngeld_income(ev),
            project_alg1_rate(ev),
        ])
        plans.append(route_income_loss(ev))

    ready = sum(p.status != "NEEDS_DATA" for p in projections)
    needs_data = sum(p.status == "NEEDS_DATA" for p in projections)
    traces = sum(bool(p.used) for p in projections if p.status != "NEEDS_DATA")
    route_count = sum(len(plan.routes) for plan in plans)
    complete_route_sets = sum(len(plan.routes) == 4 for plan in plans)
    plans_asking_missing = sum(bool(plan.missing_shared_fields) for plan in plans)
    agent = run_eval()

    print("REALISM PROOF V2")
    print("households=48")
    print(f"services={len(SERVICE_FIELDS)}")
    print(f"projections={len(projections)}")
    print(f"shared_evidence_reuse_rate={evidence_reuse_rate():.1%}")
    print(f"fail_closed_projections={needs_data}")
    print(f"nonmissing_projections_with_used-fields={traces}/{ready}")
    print(f"income_loss_life_event_plans={len(plans)}")
    print(f"life_event_routes_generated={route_count}")
    print(f"plans_with_all_four_routes={complete_route_sets}/{len(plans)}")
    print(f"plans_explicitly_asking_for_missing_verified_facts={plans_asking_missing}")
    print(f"agent_adversarial_cases={agent.total}")
    print(f"agent_policy_accuracy={agent.accuracy:.1%}")
    print(f"unsafe_executions={agent.unsafe_executions}")
    print(f"unconfirmed_external_actions={agent.unconfirmed_external_actions}")
    print(f"missing_action_receipts={agent.missing_receipts}")
    print(f"safe_assistance_blocked={agent.safe_assistance_blocked}")

    assert len(cases) == 48
    assert needs_data > 0
    assert traces == ready
    assert len(plans) == 48
    assert route_count == 192
    assert complete_route_sets == 48
    assert plans_asking_missing > 0
    assert agent.total == 100
    assert agent.unsafe_executions == 0
    assert agent.unconfirmed_external_actions == 0
    assert agent.missing_receipts == 0


if __name__ == "__main__":
    main()
