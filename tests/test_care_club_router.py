import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_routes():
    return json.loads((ROOT / "data" / "berlin_action_routes.json").read_text(encoding="utf-8"))


def test_need_routes_are_verified_and_nonempty():
    data = load_routes()
    assert data["need_help"]
    assert all(route["verified"] for route in data["need_help"])
    assert all(route["url"].startswith("https://") for route in data["need_help"])


def test_child_crisis_has_24_7_phone_route():
    routes = {r["id"]: r for r in load_routes()["need_help"]}
    child = routes["child_crisis_24_7"]
    assert child["phone"] == "+49 30 610061"
    assert "24/7" in child["availability"]


def test_care_does_not_claim_existing_network_impact():
    data = load_routes()
    assert data["public_network_snapshot"]["not_care_impact"] is True
    direct = data["care_direct_impact"]
    assert direct["verified_households_served"] == 0
    assert direct["verified_direct_euros_delivered"] == 0
    assert direct["verified_food_access_days_guaranteed"] == 0


def test_help_actions_include_money_time_food_and_company_routes():
    ids = {r["id"] for r in load_routes()["can_help"]}
    assert {"donate_money", "volunteer", "rescue_food", "corporate_volunteering"}.issubset(ids)


def test_club_page_has_three_simple_frontdoors_and_privacy_boundary():
    html = (ROOT / "club" / "index.html").read_text(encoding="utf-8")
    assert "Ich brauche Hilfe" in html
    assert "Ich kann helfen" in html
    assert "Ich will mitbauen" in html
    assert "Keine Daten werden hier gespeichert" in html
    assert "CARE DIRECT IMPACT" in html
    assert "10 Berliner Familien. 30 Tage. 0 ungeklärte Essenstage." in html
