from engine.rights_safe_agent import (
    RightsSafeAgent,
    consequential_submit_action,
    forbidden_decision_action,
)


def test_planner_exposes_six_public_service_roles():
    agent = RightsSafeAgent()
    actions = agent.plan_for_life_event("income loss")
    roles = {a.role for a in actions}
    assert roles == {
        "ORIENTATION",
        "APPLICATION_PREP",
        "PROCEDURE",
        "COMMUNICATION",
        "ORCHESTRATION",
        "MONITORING",
    }


def test_binding_decision_is_always_blocked():
    agent = RightsSafeAgent()
    receipt = agent.execute(forbidden_decision_action(), confirmed=True)
    assert receipt.outcome == "BLOCKED_BINDING_DECISION"


def test_external_submission_requires_explicit_confirmation():
    agent = RightsSafeAgent()
    action = consequential_submit_action()
    blocked = agent.execute(action, confirmed=False)
    allowed = agent.execute(action, confirmed=True)
    assert blocked.outcome == "AWAITING_EXPLICIT_CONFIRMATION"
    assert allowed.outcome == "EXECUTED"
    assert allowed.confirmed_by_user is True


def test_every_execution_creates_provenance_receipt():
    agent = RightsSafeAgent()
    action = agent.plan_for_life_event("new child")[0]
    receipt = agent.execute(action)
    assert receipt.action_id == action.action_id
    assert receipt.source == action.source
    assert receipt.explanation
    assert agent.receipts[-1] == receipt


def test_monitoring_is_aggregate_not_individual_enforcement():
    agent = RightsSafeAgent()
    monitor = [a for a in agent.plan_for_life_event("separation") if a.role == "MONITORING"][0]
    receipt = agent.execute(monitor)
    assert receipt.outcome == "EXECUTED"
    assert "enforcement score" in receipt.explanation
