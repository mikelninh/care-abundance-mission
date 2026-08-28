"""Fail-closed CARE verifier for authoritative OpenProof/Midnight receipts.

This module does not query Midnight by itself. The adapter that actually owns a
successful indexer read must pass ``trusted_indexer_read=True``. A caller-supplied
JSON object can therefore match the expected receipt shape without ever becoming
an authoritative CARE proof.
"""
from __future__ import annotations

from typing import Any

RECEIPT_SCHEMA = "openproof.midnight.receipt/1"
FAMILY_PROOF_TYPE = "1"
FAMILY_PURPOSE_CODE = "101"
FAMILY_POLICY_VERSION = "1"
FAMILY_PROVIDER_ID = "1"

RECEIPT_FIELDS = (
    "proofType",
    "purposeCode",
    "policyVersion",
    "providerId",
    "bindingHash",
    "auxiliaryBindingHash",
    "verifierChallengeHash",
)

FORBIDDEN_PRIVATE_KEYS = {
    "claims",
    "rawclaims",
    "privateclaims",
    "household",
    "income",
    "monthlyincomeeur",
    "monthlygrossincome",
    "rent",
    "warmrent",
    "iban",
    "address",
    "applicant",
    "applicantname",
    "email",
    "phone",
    "diagnosis",
    "childcount",
    "children",
    "childage",
    "birthdate",
}


def _decimal(value: Any, label: str, errors: list[str]) -> str | None:
    if isinstance(value, bool):
        errors.append(f"{label} must be an unsigned decimal scalar")
        return None
    if isinstance(value, int) and value >= 0:
        return str(value)
    if isinstance(value, str) and value.isdigit():
        return value.lstrip("0") or "0"
    errors.append(f"{label} must be an unsigned decimal scalar")
    return None


def _string(value: Any, label: str, errors: list[str]) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    errors.append(f"{label} missing")
    return None


def _private_field_paths(envelope: dict[str, Any]) -> list[str]:
    leaks: set[str] = set()

    def visit(value: Any, path: str) -> None:
        if not isinstance(value, dict):
            return
        for key, nested in value.items():
            next_path = f"{path}.{key}" if path else str(key)
            if str(key).lower() in FORBIDDEN_PRIVATE_KEYS:
                leaks.add(next_path)
            visit(nested, next_path)

    visit(envelope.get("receipt"), "receipt")
    visit(envelope.get("disclosures"), "disclosures")
    for key in ("claims", "rawClaims", "privateClaims"):
        if envelope.get(key) is not None:
            leaks.add(key)
    return sorted(leaks)


def expected_family_receipt(
    *,
    binding_hash: Any | None = None,
    verifier_challenge_hash: Any | None = None,
    nullifier: Any | None = None,
) -> dict[str, Any]:
    expected: dict[str, Any] = {
        "proofType": FAMILY_PROOF_TYPE,
        "purposeCode": FAMILY_PURPOSE_CODE,
        "policyVersion": FAMILY_POLICY_VERSION,
        "providerId": FAMILY_PROVIDER_ID,
        "auxiliaryBindingHash": "0",
    }
    if binding_hash is not None:
        expected["bindingHash"] = binding_hash
    if verifier_challenge_hash is not None:
        expected["verifierChallengeHash"] = verifier_challenge_hash
    if nullifier is not None:
        expected["nullifier"] = nullifier
    return expected


def verify_midnight_family_receipt(
    envelope: dict[str, Any],
    *,
    expected: dict[str, Any],
    trusted_indexer_read: bool = False,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(envelope, dict):
        return {
            "ok": False,
            "matched": False,
            "authoritative": False,
            "state": "REJECTED",
            "errors": ["receipt envelope must be an object"],
            "warnings": warnings,
        }

    if envelope.get("schema") != RECEIPT_SCHEMA:
        errors.append("receipt schema mismatch")

    receipt = envelope.get("receipt")
    source = envelope.get("source")
    if not isinstance(receipt, dict):
        errors.append("receipt missing")
        receipt = {}
    if not isinstance(source, dict):
        errors.append("source metadata missing")
        source = {}

    nullifier = _decimal(envelope.get("nullifier"), "nullifier", errors)
    for field in RECEIPT_FIELDS:
        _decimal(receipt.get(field), f"receipt.{field}", errors)

    source_kind = source.get("kind")
    network = _string(source.get("network"), "source.network", errors)
    contract_address = _string(source.get("contractAddress"), "source.contractAddress", errors)
    transaction_id = _string(source.get("transactionId"), "source.transactionId", errors)
    block_height = _decimal(source.get("blockHeight"), "source.blockHeight", errors)

    if source_kind != "midnight-indexer":
        errors.append("source.kind must be midnight-indexer")
    if contract_address and (len(contract_address) != 64 or any(char not in "0123456789abcdefABCDEF" for char in contract_address)):
        errors.append("contract address format invalid")
    if transaction_id and (len(transaction_id) != 66 or any(char not in "0123456789abcdefABCDEF" for char in transaction_id)):
        errors.append("transaction id format invalid")
    if network and len(network) > 80:
        errors.append("network label too long")

    leaks = _private_field_paths(envelope)
    if leaks:
        errors.append(f"private-looking fields present: {', '.join(leaks)}")
    disclosures = envelope.get("disclosures")
    if isinstance(disclosures, dict) and disclosures:
        errors.append("family receipt must not carry raw disclosures")

    for field in RECEIPT_FIELDS:
        if field not in expected:
            continue
        actual = _decimal(receipt.get(field), f"receipt.{field}", errors)
        wanted = _decimal(expected.get(field), f"expected.{field}", errors)
        if actual is not None and wanted is not None and actual != wanted:
            errors.append(f"{field} mismatch")

    if "nullifier" in expected:
        wanted_nullifier = _decimal(expected.get("nullifier"), "expected.nullifier", errors)
        if nullifier is not None and wanted_nullifier is not None and nullifier != wanted_nullifier:
            errors.append("nullifier mismatch")

    matched = not errors
    authoritative = matched and trusted_indexer_read is True
    if matched and not trusted_indexer_read:
        warnings.append(
            "Receipt fields match, but CARE did not obtain them through its trusted indexer adapter."
        )

    return {
        "ok": authoritative,
        "matched": matched,
        "authoritative": authoritative,
        "state": (
            "REJECTED"
            if not matched
            else "VERIFIED_AUTHORITATIVE"
            if authoritative
            else "MATCHED_UNTRUSTED_SOURCE"
        ),
        "errors": errors,
        "warnings": warnings,
        "receipt": (
            {
                **{field: str(receipt[field]) for field in RECEIPT_FIELDS},
                "nullifier": nullifier,
            }
            if matched
            else None
        ),
        "source": (
            {
                "kind": source_kind,
                "network": network,
                "contractAddress": contract_address,
                "transactionId": transaction_id,
                "blockHeight": block_height,
            }
            if matched
            else None
        ),
        "authority_boundary": "proof_receipt_is_precheck_evidence_not_official_entitlement",
    }
