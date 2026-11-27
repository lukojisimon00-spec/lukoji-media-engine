import pytest

from lukoji_engine import config
from lukoji_engine.db import Database


@pytest.fixture
def db():
    d = Database(config.load_config().path("db"))
    d.migrate()
    yield d
    d.close()


def test_migrations_are_idempotent(db):
    db.migrate(); db.migrate()
    assert db.conn.execute("SELECT COUNT(*) FROM schema_migrations").fetchone()[0] == 1


def test_content_lifecycle_and_history(db):
    db.create_content("demo", "short", "Démo")
    for s in ("propose", "valide", "scripte", "storyboard", "production", "controle", "pret"):
        db.transition("demo", s)
    assert db.get_content("demo")["status"] == "pret"
    assert len(db.history("demo")) == 8


def test_forbidden_transition_blocks_unvalidated_publication(db):
    db.create_content("brut", "short", "Non validé")
    with pytest.raises(ValueError):
        db.transition("brut", "publie")
    with pytest.raises(ValueError):
        db.transition("brut", "programme")


def test_unknown_kind_rejected(db):
    with pytest.raises(ValueError):
        db.create_content("x", "client", "Commande client")  # CLIENT STUDIO est hors périmètre


def test_asset_versioning(db):
    a1 = db.register_asset(key="k", kind="derived", path="p", sha256="aaa", bytes_=1)
    same = db.register_asset(key="k", kind="derived", path="p", sha256="aaa", bytes_=1)
    a2 = db.register_asset(key="k", kind="derived", path="p", sha256="bbb", bytes_=1)
    assert a1["version"] == same["version"] == 1 and a2["version"] == 2
