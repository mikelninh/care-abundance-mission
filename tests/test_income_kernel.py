from engine.income_kernel import EvidenceItem, IncomeKernel, PROOF_RULES


def kernel():
    k = IncomeKernel()
    k.put(EvidenceItem("employment_net", 1600, "payroll-feed", "2026-08", True))
    k.put(EvidenceItem("maintenance", 300, "declared+verified", "2026-08", True))
    k.put(EvidenceItem("capital_income", 100, "tax-feed", "2026-07", True))
    k.put(EvidenceItem("child_benefit", 518, "family-benefits", "2026-08", True))
    return k


def test_same_evidence_can_project_into_different_definitions():
    k = kernel()
    a = k.evaluate(PROOF_RULES["A"])
    b = k.evaluate(PROOF_RULES["B"])
    c = k.evaluate(PROOF_RULES["C"])
    assert a.status == b.status == c.status == "READY"
    assert len({a.countable_income, b.countable_income, c.countable_income}) == 3


def test_missing_required_evidence_fails_closed():
    k = IncomeKernel()
    k.put(EvidenceItem("employment_net", 1600, "payroll-feed", "2026-08", True))
    result = k.evaluate(PROOF_RULES["A"])
    assert result.status == "NEEDS_DATA"
    assert result.countable_income is None
    assert result.missing == ("maintenance",)


def test_unverified_required_evidence_never_becomes_ready():
    k = IncomeKernel()
    k.put(EvidenceItem("employment_net", 1600, "payroll-feed", "2026-08", True))
    k.put(EvidenceItem("maintenance", 300, "self-declared", "2026-08", False))
    result = k.evaluate(PROOF_RULES["A"])
    assert result.status == "NEEDS_REVIEW"
    assert result.countable_income is None
    assert "maintenance" in result.unverified


def test_trace_preserves_provenance_and_unused_evidence():
    result = kernel().evaluate(PROOF_RULES["A"])
    by_key = {t.key: t for t in result.trace}
    assert by_key["employment_net"].source == "payroll-feed"
    assert by_key["employment_net"].treatment == "INCLUDED"
    assert by_key["child_benefit"].treatment == "NOT_USED_BY_RULE"


def test_rule_version_is_always_visible():
    result = kernel().evaluate(PROOF_RULES["B"])
    assert result.rule_version == "2026-08-proof.1"
