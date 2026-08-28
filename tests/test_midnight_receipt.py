from proof.midnight_receipt import (
    RECEIPT_SCHEMA,
    expected_family_receipt,
    verify_midnight_family_receipt,
)


def envelope(**overrides):
    base = {
        "schema": RECEIPT_SCHEMA,
        "source": {
            "kind": "midnight-indexer",
            "network": "local-ci",
            "contractAddress": "a" * 64,
            "transactionId": "00" + "b" * 64,
            "blockHeight": "16",
        },
        "nullifier": "99112233",
        "receipt": {
            "proofType": "1",
            "purposeCode": "101",
            "policyVersion": "1",
            "providerId": "1",
            "bindingHash": "55001",
            "auxiliaryBindingHash": "0",
            "verifierChallengeHash": "778899",
        },
        "disclosures": {},
    }
    if "source" in overrides:
        base["source"] = {**base["source"], **overrides.pop("source")}
    if "receipt" in overrides:
        base["receipt"] = {**base["receipt"], **overrides.pop("receipt")}
    return {**base, **overrides}


EXPECTED = expected_family_receipt(
    binding_hash="55001",
    verifier_challenge_hash="778899",
    nullifier="99112233",
)


def test_matching_caller_json_never_becomes_authoritative_by_itself():
    result = verify_midnight_family_receipt(envelope(), expected=EXPECTED)
    assert result["matched"] is True
    assert result["ok"] is False
    assert result["state"] == "MATCHED_UNTRUSTED_SOURCE"


def test_trusted_indexer_adapter_can_verify_exact_receipt():
    result = verify_midnight_family_receipt(
        envelope(), expected=EXPECTED, trusted_indexer_read=True
    )
    assert result["ok"] is True
    assert result["authoritative"] is True
    assert result["state"] == "VERIFIED_AUTHORITATIVE"


def test_wrong_purpose_rejects():
    result = verify_midnight_family_receipt(
        envelope(receipt={"purposeCode": "999"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert result["ok"] is False
    assert "purposeCode mismatch" in result["errors"]


def test_wrong_policy_rejects():
    result = verify_midnight_family_receipt(
        envelope(receipt={"policyVersion": "2"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert "policyVersion mismatch" in result["errors"]


def test_wrong_provider_rejects():
    result = verify_midnight_family_receipt(
        envelope(receipt={"providerId": "2"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert "providerId mismatch" in result["errors"]


def test_wrong_binding_rejects():
    result = verify_midnight_family_receipt(
        envelope(receipt={"bindingHash": "55002"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert "bindingHash mismatch" in result["errors"]


def test_wrong_challenge_rejects():
    result = verify_midnight_family_receipt(
        envelope(receipt={"verifierChallengeHash": "1"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert "verifierChallengeHash mismatch" in result["errors"]


def test_wrong_nullifier_rejects():
    result = verify_midnight_family_receipt(
        envelope(nullifier="5"), expected=EXPECTED, trusted_indexer_read=True
    )
    assert "nullifier mismatch" in result["errors"]


def test_source_metadata_cannot_lie_about_indexer_kind():
    result = verify_midnight_family_receipt(
        envelope(source={"kind": "browser-json"}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert result["ok"] is False
    assert "source.kind must be midnight-indexer" in result["errors"]


def test_raw_income_or_rent_never_belongs_in_family_receipt():
    result = verify_midnight_family_receipt(
        envelope(receipt={"monthlyIncomeEur": 2000}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert result["ok"] is False
    assert any("private-looking fields" in error for error in result["errors"])

    result = verify_midnight_family_receipt(
        envelope(disclosures={"rent": 1100}),
        expected=EXPECTED,
        trusted_indexer_read=True,
    )
    assert result["ok"] is False
    assert any("disclosures" in error for error in result["errors"])


def test_authority_boundary_stays_explicit():
    result = verify_midnight_family_receipt(
        envelope(), expected=EXPECTED, trusted_indexer_read=True
    )
    assert result["authority_boundary"] == "proof_receipt_is_precheck_evidence_not_official_entitlement"
