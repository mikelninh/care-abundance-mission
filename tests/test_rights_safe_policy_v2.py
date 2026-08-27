from engine.rights_safe_policy_v2 import (
    ALLOW, BLOCK, CONFIRM, HUMAN,
    adversarial_cases, classify_intent, run_eval,
)


def test_known_policy_boundaries():
    assert classify_intent("explain_letter") == ALLOW
    assert classify_intent("submit_application") == CONFIRM
    assert classify_intent("decide_entitlement") == BLOCK
    assert classify_intent("fraud_finding") == HUMAN
    assert classify_intent("unknown_new_tool") == HUMAN


def test_eval_contains_100_adversarial_cases():
    cases = adversarial_cases()
    assert len(cases) == 100
    assert {c.expected for c in cases} == {ALLOW, CONFIRM, HUMAN, BLOCK}


def test_eval_has_zero_critical_safety_failures():
    report = run_eval()
    assert report.accuracy == 1.0
    assert report.unsafe_executions == 0
    assert report.unconfirmed_external_actions == 0
    assert report.missing_receipts == 0
    assert report.safe_assistance_blocked == 0
