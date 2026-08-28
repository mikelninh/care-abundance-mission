import json

from proof.openproof_family import (
    FamilyProofPolicy,
    prove_family_eligibility_local,
    verify_family_proof,
)


def synthetic_household(income=2000):
    return {
        "identity": {"resident_country": "DE", "resident_city": "Berlin", "full_name": "Synthetic Parent"},
        "household": {"children": 2, "child_birth_dates": ["2019-01-01", "2014-01-01"]},
        "finance": {"monthly_income_eur": income, "warm_rent_eur": 1100, "iban": "DE00SYNTHETIC"},
        "credential": {"valid_until_day": 21000, "source": "synthetic-authoritative-source"},
    }


def test_family_proof_passes_without_leaking_raw_claims():
    private = synthetic_household()
    proof = prove_family_eligibility_local(private, nonce="fixed-test-nonce")

    public = json.dumps(proof, sort_keys=True)
    assert "Synthetic Parent" not in public
    assert "DE00SYNTHETIC" not in public
    assert "1100" not in public
    assert '"monthly_income_eur": 2000' not in public
    assert proof["decision"] == "PASS"

    verified = verify_family_proof(proof, required_policy_id=FamilyProofPolicy().policy_id)
    assert verified == {"ok": True, "errors": []}


def test_income_failure_fails_closed():
    proof = prove_family_eligibility_local(synthetic_household(income=4000), nonce="n")
    verified = verify_family_proof(proof)
    assert proof["decision"] == "NEEDS_REVIEW"
    assert verified["ok"] is False
    assert "predicate failed: income_under_demo_ceiling" in verified["errors"]


def test_wrong_purpose_cannot_be_reused():
    proof = prove_family_eligibility_local(synthetic_household(), nonce="n")
    proof["purpose"] = "care.unrelated-purpose"
    verified = verify_family_proof(proof)
    assert verified["ok"] is False
    assert "purpose mismatch" in verified["errors"]


def test_policy_mismatch_fails_closed():
    proof = prove_family_eligibility_local(synthetic_household(), nonce="n")
    verified = verify_family_proof(proof, required_policy_id="future-policy-v99")
    assert verified["ok"] is False
    assert "policy mismatch" in verified["errors"]
