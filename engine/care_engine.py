from dataclasses import dataclass
from typing import Callable, Optional, Any


@dataclass(frozen=True)
class Household:
    adults: int
    children: int
    gross_income_monthly_eur: float
    rent_monthly_eur: float
    city: str


@dataclass(frozen=True)
class RuleEvidence:
    rule_id: str
    source_url: str
    valid_from: str
    valid_to: Optional[str]
    version: str


@dataclass(frozen=True)
class EntitlementResult:
    name: str
    verified: bool
    amount_monthly_eur: Optional[float]
    reason: str
    evidence: Optional[RuleEvidence]


@dataclass(frozen=True)
class EntitlementRule:
    name: str
    evidence: Optional[RuleEvidence]
    calculator: Optional[Callable[[Household], float]]

    def evaluate(self, household: Household) -> EntitlementResult:
        # Core CARE invariant:
        # no source/version + deterministic calculator => no public euro claim.
        if self.evidence is None:
            return EntitlementResult(
                self.name, False, None, "missing rule evidence", None
            )
        if self.calculator is None:
            return EntitlementResult(
                self.name,
                False,
                None,
                "missing deterministic calculator",
                self.evidence,
            )

        amount = float(self.calculator(household))
        if amount < 0:
            raise ValueError(f"{self.name}: entitlement cannot be negative")

        return EntitlementResult(
            self.name,
            True,
            round(amount, 2),
            "verified",
            self.evidence,
        )


def calculate_household_support(
    household: Household, rules: list[EntitlementRule]
) -> dict[str, Any]:
    results = [rule.evaluate(household) for rule in rules]
    verified = [result for result in results if result.verified]
    pending = [result for result in results if not result.verified]

    return {
        "household": household,
        "verified_monthly_total_eur": round(
            sum(result.amount_monthly_eur or 0 for result in verified), 2
        ),
        "publishable_total": len(pending) == 0,
        "results": results,
        "pending_count": len(pending),
    }


BERLIN_SINGLE_PARENT_TEST = Household(
    adults=1,
    children=2,
    gross_income_monthly_eur=2000,
    rent_monthly_eur=1100,
    city="Berlin",
)


if __name__ == "__main__":
    # V0 deliberately contains no invented entitlement formulas.
    rules = [
        EntitlementRule(
            "Current-law net public support", evidence=None, calculator=None
        ),
        EntitlementRule("Party A household impact", evidence=None, calculator=None),
        EntitlementRule("Party B household impact", evidence=None, calculator=None),
        EntitlementRule("Party C household impact", evidence=None, calculator=None),
    ]

    report = calculate_household_support(BERLIN_SINGLE_PARENT_TEST, rules)
    print(
        {
            "publishable_total": report["publishable_total"],
            "verified_monthly_total_eur": report["verified_monthly_total_eur"],
            "pending_count": report["pending_count"],
        }
    )
