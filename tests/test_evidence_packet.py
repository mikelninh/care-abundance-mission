import math

import pytest

from engine.evidence_packet import EvidenceItem, EvidencePacket


def item(key, value, *, verified=True, source="test-source", as_of="2026-08"):
    return EvidenceItem(key, value, source, as_of, verified)


def test_packet_preserves_missing_and_unverified_as_different_states():
    packet = EvidencePacket({
        "employment_net": item("employment_net", 1600),
        "maintenance": item("maintenance", 200, verified=False),
    })
    check = packet.require(("employment_net", "maintenance", "capital_income"))
    assert check.ready is False
    assert check.missing == ("capital_income",)
    assert check.unverified == ("maintenance",)


def test_packet_is_the_single_admission_gate_for_reused_evidence():
    packet = EvidencePacket({
        "adults": item("adults", 1),
        "children": item("children", 2),
        "registered_unemployed": item("registered_unemployed", 1),
        "insured_months_30": item("insured_months_30", 12),
    })
    assert packet.integer("adults") == 1
    assert packet.integer("children") == 2
    assert packet.boolean("registered_unemployed") is True
    assert packet.verified_keys() == (
        "adults", "children", "insured_months_30", "registered_unemployed"
    )


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_non_finite_values_fail_at_packet_admission(bad):
    with pytest.raises(ValueError, match="finite"):
        EvidencePacket({"employment_net": item("employment_net", bad)})


def test_negative_values_fail_at_packet_admission():
    with pytest.raises(ValueError, match=">= 0"):
        EvidencePacket({"maintenance": item("maintenance", -1)})


def test_provenance_key_mismatch_fails_at_packet_admission():
    with pytest.raises(ValueError, match="key mismatch"):
        EvidencePacket({"children": item("adults", 1)})


@pytest.mark.parametrize("value", [0.5, 2, -1])
def test_boolean_fields_accept_only_zero_or_one(value):
    with pytest.raises(ValueError, match="0 or 1"):
        EvidencePacket({"available_15h": item("available_15h", value)})


def test_integer_and_declared_range_semantics_are_owned_by_packet():
    with pytest.raises(ValueError, match="integer"):
        EvidencePacket({"children": item("children", 1.5)})
    with pytest.raises(ValueError, match="adults must be >= 1"):
        EvidencePacket({"adults": item("adults", 0)})
    with pytest.raises(ValueError, match="insured_months_30 must be <= 30"):
        EvidencePacket({"insured_months_30": item("insured_months_30", 31)})


def test_source_and_as_of_are_required_for_reusable_evidence():
    with pytest.raises(ValueError, match="source required"):
        EvidencePacket({"employment_net": item("employment_net", 1, source="")})
    with pytest.raises(ValueError, match="as_of required"):
        EvidencePacket({"employment_net": item("employment_net", 1, as_of="")})


def test_verified_flag_cannot_use_truthy_non_boolean_value():
    with pytest.raises(ValueError, match="verified must be boolean"):
        EvidencePacket({"employment_net": item("employment_net", 1, verified=1)})
