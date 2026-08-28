"""Canonical evidence packet for CARE public-service journeys.

This module owns structural validation, provenance-key integrity, field semantics,
missing/unverified state and safe evidence reuse. Downstream rule modules should
ask the packet for facts; they should not re-implement evidence validation.

It is still a precheck/evidence contract. A verified packet does not create a
legal entitlement or authority decision.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Mapping


@dataclass(frozen=True)
class EvidenceItem:
    key: str
    monthly_amount: float
    source: str
    as_of: str
    verified: bool = True


@dataclass(frozen=True)
class EvidenceCheck:
    required: tuple[str, ...]
    missing: tuple[str, ...] = ()
    unverified: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return not self.missing and not self.unverified


_BOOLEAN_FIELDS = frozenset({
    "registered_unemployed",
    "available_15h",
    "has_minor_child",
    "pays_income_tax",
    "pays_health_care",
    "pays_pension",
})

_INTEGER_FIELDS = frozenset({"adults", "children", "insured_months_30"})

_MAX_VALUES = {
    "insured_months_30": 30.0,
}

_MIN_VERIFIED_VALUES = {
    "adults": 1.0,
}


class EvidencePacket:
    """One validated, provenance-preserving evidence set.

    The interface is intentionally small. Validation happens at admission, then
    callers can use `require`, `value`, `boolean`, `integer` and
    `verified_keys` without repeating the packet's structural rules.
    """

    def __init__(self, items: Mapping[str, EvidenceItem] | None = None):
        self._items: dict[str, EvidenceItem] = {}
        for key, item in (items or {}).items():
            self.put(item, map_key=key)

    @classmethod
    def from_mapping(cls, items: Mapping[str, EvidenceItem] | "EvidencePacket") -> "EvidencePacket":
        if isinstance(items, cls):
            return items
        return cls(items)

    def put(self, item: EvidenceItem, *, map_key: str | None = None) -> None:
        key = item.key if map_key is None else map_key
        self._validate_item(key, item)
        self._items[key] = item

    def _validate_item(self, map_key: str, item: EvidenceItem) -> None:
        if not isinstance(item, EvidenceItem):
            raise TypeError(f"{map_key}: expected EvidenceItem")
        if not item.key or item.key != map_key:
            raise ValueError(f"evidence key mismatch: map={map_key!r}, item={item.key!r}")
        if not str(item.source).strip():
            raise ValueError(f"{map_key}: source required")
        if not str(item.as_of).strip():
            raise ValueError(f"{map_key}: as_of required")
        if type(item.verified) is not bool:
            raise ValueError(f"{map_key}: verified must be boolean")

        value = float(item.monthly_amount)
        if not math.isfinite(value):
            raise ValueError(f"{map_key} must be finite")
        if value < 0:
            raise ValueError(f"{map_key} must be >= 0")
        if map_key in _BOOLEAN_FIELDS and value not in (0.0, 1.0):
            raise ValueError(f"{map_key} must be 0 or 1")
        if map_key in _INTEGER_FIELDS and not value.is_integer():
            raise ValueError(f"{map_key} must be an integer")
        if item.verified and map_key in _MIN_VERIFIED_VALUES and value < _MIN_VERIFIED_VALUES[map_key]:
            raise ValueError(f"{map_key} must be >= {_MIN_VERIFIED_VALUES[map_key]:g}")
        if item.verified and map_key in _MAX_VALUES and value > _MAX_VALUES[map_key]:
            raise ValueError(f"{map_key} must be <= {_MAX_VALUES[map_key]:g}")

    def item(self, key: str) -> EvidenceItem | None:
        return self._items.get(key)

    def value(self, key: str) -> float:
        if key not in self._items:
            raise KeyError(key)
        return float(self._items[key].monthly_amount)

    def boolean(self, key: str) -> bool:
        if key not in _BOOLEAN_FIELDS:
            raise ValueError(f"{key} is not declared boolean evidence")
        return self.value(key) == 1.0

    def integer(self, key: str) -> int:
        if key not in _INTEGER_FIELDS:
            raise ValueError(f"{key} is not declared integer evidence")
        return int(self.value(key))

    def is_verified(self, key: str) -> bool:
        item = self._items.get(key)
        return bool(item and item.verified)

    def require(self, keys: Iterable[str]) -> EvidenceCheck:
        required = tuple(sorted(set(keys)))
        missing = tuple(key for key in required if key not in self._items)
        unverified = tuple(
            key for key in required
            if key in self._items and not self._items[key].verified
        )
        return EvidenceCheck(required=required, missing=missing, unverified=unverified)

    def verified_keys(self) -> tuple[str, ...]:
        return tuple(sorted(key for key, item in self._items.items() if item.verified))

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._items))

    def items(self) -> tuple[tuple[str, EvidenceItem], ...]:
        return tuple((key, self._items[key]) for key in sorted(self._items))

    def as_mapping(self) -> dict[str, EvidenceItem]:
        return dict(self._items)
