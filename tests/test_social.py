"""Comptes sociaux officiels : liens exacts, cohérence, absence de secret. Aucun accès réseau."""
import copy

import pytest

from lukoji_engine import config
from lukoji_engine.social import destinations, find_secrets, load_accounts, validate

OFFICIAL = {
    "youtube": "https://www.youtube.com/@Lukoji-officiel",
    "facebook": "https://www.facebook.com/share/1MKZxLR4Jz/",
    "instagram": "https://www.instagram.com/lukoji_officiel",
    "tiktok": "https://www.tiktok.com/@lukoji_officiel",
}


def test_official_links_are_recorded_exactly():
    accounts = load_accounts()
    assert {k: a.url for k, a in accounts.items()} == OFFICIAL


def test_config_is_valid_and_secret_free():
    data = config.load_config().social
    assert validate(data) == []
    assert find_secrets(data) == []


def test_no_publication_enabled_in_phase0():
    assert all(a.publication == "desactivee" for a in load_accounts().values())


def test_editorial_routing():
    assert {a.key for a in destinations("short")} == {"youtube", "tiktok", "instagram", "facebook"}
    assert {a.key for a in destinations("affiche")} == {"facebook", "instagram"}
    assert [a.key for a in destinations("documentaire")] == ["youtube"]


def test_facebook_link_flagged_as_share_link():
    assert load_accounts()["facebook"].is_share_link


@pytest.mark.parametrize("mutation, expected", [
    (lambda d: d["comptes"]["youtube"].update(url="http://www.youtube.com/@Lukoji-officiel"), "https"),
    (lambda d: d["comptes"]["tiktok"].update(url="https://tiktok.evil.com/@lukoji_officiel"), "domaine"),
    (lambda d: d["comptes"]["instagram"].update(access_token="EAAB" + "x" * 40), "clé suspecte"),
    (lambda d: d["comptes"]["tiktok"].update(notes="ghp_" + "a" * 36), "secret"),
    (lambda d: d["routage"].update(affiche=["facebook", "instagram", "tiktok"]), "affiche"),
    (lambda d: d["comptes"].pop("tiktok"), "plateformes attendues"),
    (lambda d: d["comptes"]["instagram"].update(identifiant="autre_compte"), "identifiant"),
])
def test_invalid_configurations_are_rejected(mutation, expected):
    data = copy.deepcopy(config.load_config().social)
    mutation(data)
    problems = validate(data)
    assert any(expected in p for p in problems), problems
