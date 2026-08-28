"""CARE Family Eligibility × OpenProof MVP.

This module is a privacy-bound precheck proof, not an entitlement engine.
It deliberately emits predicate results instead of raw household values.

Backend boundary:
- `care-local-witness-v0` evaluates predicates locally and commits to the
  private witness with SHA-256. It is useful for integration and leakage tests.
- Production should replace this backend with the OpenProof/Midnight verifier,
  where the same predicates are proven in ZK against issuer-bound credentials.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from typing import Any

OPENPROOF_VERSION = "openproof/0.1"
PURPOSE = "care.family.precheck"
BACKEND = "care-local-witness-v0"


@dataclass(frozen=True)
class FamilyProofPolicy:
    policy_id: str = "care-family-demo-2026-08"
    resident_country: str = "DE"
    minimum_children: int = 1
    maximum_monthly_income_eur: int = 2500
    current_day: int = 20693  # 2026-08-28, explicit synthetic-demo policy clock


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _commit(private_claims: dict[str, Any], nonce: str) -> str:
    payload = f"{_canonical(private_claims)}:{nonce}".encode("utf-8")
    return f"sha256:{sha256(payload).hexdigest()}"


def prove_family_eligibility_local(
    private_claims: dict[str, Any],
    *,
    policy: FamilyProofPolicy | None = None,
    nonce: str,
) -> dict[str, Any]:
    """Create a non-ZK public projection from a private synthetic witness.

    This is intentionally local/test-only. The result shape mirrors the
    OpenProof public envelope so CARE can integrate before Midnight is live.
    """
    policy = policy or FamilyProofPolicy()

    identity = private_claims.get("identity") or {}
    household = private_claims.get("household") or {}
    finance = private_claims.get("finance") or {}
    credential = private_claims.get("credential") or {}

    predicates = [
        {
            "id": "resident_country",
            "claim": "identity.resident_country",
            "op": "eq",
            "passed": identity.get("resident_country") == policy.resident_country,
        },
        {
            "id": "minimum_children",
            "claim": "household.children",
            "op": "gte",
            "passed": isinstance(household.get("children"), int)
            and household["children"] >= policy.minimum_children,
        },
        {
            "id": "income_under_demo_ceiling",
            "claim": "finance.monthly_income_eur",
            "op": "lte",
            "passed": isinstance(finance.get("monthly_income_eur"), (int, float))
            and finance["monthly_income_eur"] <= policy.maximum_monthly_income_eur,
        },
        {
            "id": "credential_current",
            "claim": "credential.valid_until_day",
            "op": "gte",
            "passed": isinstance(credential.get("valid_until_day"), int)
            and credential["valid_until_day"] >= policy.current_day,
        },
    ]

    return {
        "openproof": OPENPROOF_VERSION,
        "backend": BACKEND,
        "purpose": PURPOSE,
        "policy": asdict(policy),
        "claims_commitment": _commit(private_claims, nonce),
        "predicate_results": predicates,
        "disclosures": {},
        "decision": "PASS" if all(item["passed"] for item in predicates) else "NEEDS_REVIEW",
        "authority_boundary": "precheck_only_official_decision_remains_official",
    }


def verify_family_proof(proof: dict[str, Any], *, required_policy_id: str | None = None) -> dict[str, Any]:
    errors: list[str] = []
    if proof.get("openproof") != OPENPROOF_VERSION:
        errors.append("openproof version mismatch")
    if proof.get("purpose") != PURPOSE:
        errors.append("purpose mismatch")
    if not str(proof.get("claims_commitment", "")).startswith("sha256:"):
        errors.append("claims commitment missing")
    if proof.get("disclosures") not in ({}, None):
        errors.append("family proof must disclose no raw claims")
    if required_policy_id and (proof.get("policy") or {}).get("policy_id") != required_policy_id:
        errors.append("policy mismatch")

    results = {item.get("id"): item for item in proof.get("predicate_results", [])}
    required = {
        "resident_country",
        "minimum_children",
        "income_under_demo_ceiling",
        "credential_current",
    }
    missing = required - set(results)
    if missing:
        errors.append(f"missing predicates: {sorted(missing)}")
    for predicate_id in required & set(results):
        if results[predicate_id].get("passed") is not True:
            errors.append(f"predicate failed: {predicate_id}")

    if proof.get("authority_boundary") != "precheck_only_official_decision_remains_official":
        errors.append("authority boundary missing")

    return {"ok": not errors, "errors": errors}
