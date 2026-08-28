"""Targeted proof for reusable public-service income checks.

This is an architecture/product proof, not a calculator for current German law.
Rule definitions in this module are synthetic and exist to demonstrate how one
canonical evidence set can be projected into multiple versioned definitions
without hiding missing data or provenance.
"""

from dataclasses import dataclass, field
from typing import Iterable, Tuple

from engine.evidence_packet import EvidenceItem, EvidencePacket


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
    packet: EvidencePacket = field(default_factory=EvidencePacket)

    @property
    def evidence(self) -> dict[str, EvidenceItem]:
        """Compatibility view. New callers should use the packet interface."""
        return self.packet.as_mapping()

    def put(self, item: EvidenceItem) -> None:
        self.packet.put(item)

    def evaluate(self, rule: IncomeRule) -> IncomeResult:
        check = self.packet.require(rule.included_keys)
        if check.missing:
            return IncomeResult(
                status="NEEDS_DATA",
                rule_id=rule.rule_id,
                rule_version=rule.version,
                countable_income=None,
                missing=check.missing,
            )

        if check.unverified:
            return IncomeResult(
                status="NEEDS_REVIEW",
                rule_id=rule.rule_id,
                rule_version=rule.version,
                countable_income=None,
                unverified=check.unverified,
                trace=tuple(self._trace(rule)),
            )

        gross = sum(self.packet.value(key) for key in rule.included_keys)
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
        for key, item in self.packet.items():
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

# Backward-compatible import surface for existing callers/tests.
__all__ = [
    "EvidenceItem",
    "EvidencePacket",
    "IncomeKernel",
    "IncomeResult",
    "IncomeRule",
    "PROOF_RULES",
    "TraceItem",
]
