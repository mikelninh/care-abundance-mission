"""Targeted proof for reusable public-service income checks.

This is an architecture/product proof, not a calculator for current German law.
Rule definitions in this module are synthetic and exist to demonstrate how one
canonical evidence set can be projected into multiple versioned definitions
without hiding missing data or provenance.
"""

from dataclasses import dataclass, field
from typing import Dict, Iterable, Tuple


@dataclass(frozen=True)
class EvidenceItem:
    key: str
    monthly_amount: float
    source: str
    as_of: str
    verified: bool = True


@dataclass(frozen=True)
class IncomeRule:
    rule_id: str
    name: str
    version: str
    included_keys: Tuple[str, ...]
    deduction_rate: float = 0.0
    note: str = "synthetic proof rule"


@dataclass(frozen=True)
class TraceItem:
    key: str
    amount: float
    source: str
    as_of: str
    treatment: str


@dataclass(frozen=True)
class IncomeResult:
    status: str
    rule_id: str
    rule_version: str
    countable_income: float | None
    missing: Tuple[str, ...] = ()
    unverified: Tuple[str, ...] = ()
    trace: Tuple[TraceItem, ...] = ()


@dataclass
class IncomeKernel:
    evidence: Dict[str, EvidenceItem] = field(default_factory=dict)

    def put(self, item: EvidenceItem) -> None:
        if item.monthly_amount < 0:
            raise ValueError("monthly_amount must be >= 0")
        self.evidence[item.key] = item

    def evaluate(self, rule: IncomeRule) -> IncomeResult:
        missing = tuple(k for k in rule.included_keys if k not in self.evidence)
        if missing:
            return IncomeResult(
                status="NEEDS_DATA",
                rule_id=rule.rule_id,
                rule_version=rule.version,
                countable_income=None,
                missing=missing,
            )

        unverified = tuple(
            k for k in rule.included_keys if not self.evidence[k].verified
        )
        if unverified:
            return IncomeResult(
                status="NEEDS_REVIEW",
                rule_id=rule.rule_id,
                rule_version=rule.version,
                countable_income=None,
                unverified=unverified,
                trace=tuple(self._trace(rule)),
            )

        gross = sum(self.evidence[k].monthly_amount for k in rule.included_keys)
        result = gross * (1 - rule.deduction_rate)
        return IncomeResult(
            status="READY",
            rule_id=rule.rule_id,
            rule_version=rule.version,
            countable_income=round(result, 2),
            trace=tuple(self._trace(rule)),
        )

    def _trace(self, rule: IncomeRule) -> Iterable[TraceItem]:
        included = set(rule.included_keys)
        for key in sorted(self.evidence):
            item = self.evidence[key]
            yield TraceItem(
                key=key,
                amount=item.monthly_amount,
                source=item.source,
                as_of=item.as_of,
                treatment="INCLUDED" if key in included else "NOT_USED_BY_RULE",
            )


# Illustrative definitions only. Their purpose is to prove modularity,
# versioning and traceability, not to represent any named statutory benefit.
PROOF_RULES = {
    "A": IncomeRule(
        rule_id="proof-a",
        name="Illustrative definition A",
        version="2026-08-proof.1",
        included_keys=("employment_net", "maintenance"),
        deduction_rate=0.0,
    ),
    "B": IncomeRule(
        rule_id="proof-b",
        name="Illustrative definition B",
        version="2026-08-proof.1",
        included_keys=("employment_net", "maintenance", "capital_income"),
        deduction_rate=0.10,
    ),
    "C": IncomeRule(
        rule_id="proof-c",
        name="Illustrative definition C",
        version="2026-08-proof.1",
        included_keys=("employment_net",),
        deduction_rate=0.05,
    ),
}
