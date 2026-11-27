"""Base SQLite initiale : ressources versionnées, registre des contenus, rendus, contrôles qualité.

Schéma minimal de la phase 0, migré par numéro de version (table schema_migrations).
Les contenus suivent un cycle de vie strict ; aucune transition hors du graphe n'est acceptée.
"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from .log import get_logger

log = get_logger("db")

# ---------------------------------------------------------------------------
# Cycle de vie des contenus
# ---------------------------------------------------------------------------
STATUSES = (
    "idee", "propose", "valide", "scripte", "storyboard", "production",
    "controle", "pret", "programme", "publie", "echec", "archive",
)
TRANSITIONS: dict[str, set[str]] = {
    "idee": {"propose", "archive"},
    "propose": {"valide", "idee", "archive"},
    "valide": {"scripte", "production", "archive"},
    "scripte": {"storyboard", "valide", "archive"},
    "storyboard": {"production", "scripte", "archive"},
    "production": {"controle", "storyboard", "echec", "archive"},
    "controle": {"pret", "production", "echec"},
    "pret": {"programme", "production", "archive"},
    "programme": {"publie", "pret", "echec"},
    "publie": {"archive"},
    "echec": {"production", "archive"},
    "archive": set(),
}
KINDS = ("short", "affiche", "documentaire", "test")

MIGRATIONS: list[str] = [
    # 1 — schéma initial
    """
    CREATE TABLE assets (
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL,
        version INTEGER NOT NULL,
        kind TEXT NOT NULL CHECK (kind IN ('original','derived')),
        path TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        bytes INTEGER NOT NULL,
        width INTEGER, height INTEGER,
        role TEXT,
        derived_from TEXT,
        params_json TEXT,
        created_at TEXT NOT NULL,
        UNIQUE (key, version)
    );
    CREATE TABLE contents (
        id INTEGER PRIMARY KEY,
        slug TEXT NOT NULL UNIQUE,
        kind TEXT NOT NULL CHECK (kind IN ('short','affiche','documentaire','test')),
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        meta_json TEXT NOT NULL DEFAULT '{}',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    CREATE TABLE content_events (
        id INTEGER PRIMARY KEY,
        content_id INTEGER NOT NULL REFERENCES contents(id),
        from_status TEXT, to_status TEXT NOT NULL,
        note TEXT, at TEXT NOT NULL
    );
    CREATE TABLE renders (
        id INTEGER PRIMARY KEY,
        content_id INTEGER REFERENCES contents(id),
        path TEXT NOT NULL,
        sha256 TEXT NOT NULL,
        profile TEXT NOT NULL,
        width INTEGER, height INTEGER, fps REAL, duration REAL,
        params_json TEXT NOT NULL DEFAULT '{}',
        qc_status TEXT NOT NULL DEFAULT 'non_controle',
        created_at TEXT NOT NULL
    );
    CREATE TABLE qc_results (
        id INTEGER PRIMARY KEY,
        render_id INTEGER NOT NULL REFERENCES renders(id),
        run_at TEXT NOT NULL,
        check_name TEXT NOT NULL,
        passed INTEGER NOT NULL,
        severity TEXT NOT NULL,
        value TEXT, expected TEXT, detail TEXT
    );
    CREATE INDEX idx_renders_content ON renders(content_id);
    CREATE INDEX idx_qc_render ON qc_results(render_id);
    """,
]


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class Database:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # isolation_level=None : transactions gérées explicitement par tx().
        self.conn = sqlite3.connect(self.path, isolation_level=None)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")

    # -- migrations ---------------------------------------------------------
    def migrate(self) -> int:
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        current = self.conn.execute("SELECT COALESCE(MAX(version), 0) FROM schema_migrations").fetchone()[0]
        for version, sql in enumerate(MIGRATIONS, start=1):
            if version <= current:
                continue
            with self.tx():
                for statement in _split_sql(sql):
                    self.conn.execute(statement)
                self.conn.execute("INSERT INTO schema_migrations VALUES (?, ?)", (version, now()))
            log.info("migration appliquée", extra={"version": version})
        return len(MIGRATIONS)

    @contextmanager
    def tx(self) -> Iterator[sqlite3.Connection]:
        try:
            self.conn.execute("BEGIN")
            yield self.conn
            self.conn.execute("COMMIT")
        except Exception:
            self.conn.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self.conn.close()

    # -- ressources ----------------------------------------------------------
    def register_asset(self, *, key: str, kind: str, path: str, sha256: str, bytes_: int,
                       width: int | None = None, height: int | None = None, role: str | None = None,
                       derived_from: str | None = None, params: dict | None = None) -> dict:
        """Enregistre une ressource. Nouvelle version uniquement si le contenu (sha256) change."""
        last = self.conn.execute(
            "SELECT * FROM assets WHERE key = ? ORDER BY version DESC LIMIT 1", (key,)
        ).fetchone()
        if last and last["sha256"] == sha256:
            return dict(last)
        version = (last["version"] + 1) if last else 1
        with self.tx():
            self.conn.execute(
                "INSERT INTO assets (key, version, kind, path, sha256, bytes, width, height, role, derived_from, params_json, created_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (key, version, kind, path, sha256, bytes_, width, height, role, derived_from,
                 json.dumps(params or {}, ensure_ascii=False, sort_keys=True), now()),
            )
        if last:
            log.warning("nouvelle version de ressource", extra={"key": key, "version": version})
        return dict(self.conn.execute("SELECT * FROM assets WHERE key = ? AND version = ?", (key, version)).fetchone())

    def latest_asset(self, key: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM assets WHERE key = ? ORDER BY version DESC LIMIT 1", (key,)).fetchone()
        return dict(row) if row else None

    # -- registre des contenus ----------------------------------------------
    def create_content(self, slug: str, kind: str, title: str, status: str = "idee", meta: dict | None = None) -> dict:
        if kind not in KINDS:
            raise ValueError(f"type de contenu inconnu : {kind}")
        if status not in STATUSES:
            raise ValueError(f"statut inconnu : {status}")
        ts = now()
        with self.tx():
            cur = self.conn.execute(
                "INSERT INTO contents (slug, kind, title, status, meta_json, created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
                (slug, kind, title, status, json.dumps(meta or {}, ensure_ascii=False), ts, ts),
            )
            self.conn.execute(
                "INSERT INTO content_events (content_id, from_status, to_status, note, at) VALUES (?,?,?,?,?)",
                (cur.lastrowid, None, status, "création", ts),
            )
        return self.get_content(slug)

    def get_content(self, slug: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM contents WHERE slug = ?", (slug,)).fetchone()
        return dict(row) if row else None

    def get_or_create_content(self, slug: str, kind: str, title: str, meta: dict | None = None) -> dict:
        return self.get_content(slug) or self.create_content(slug, kind, title, meta=meta)

    def list_contents(self, status: str | None = None) -> list[dict]:
        q, args = "SELECT * FROM contents", ()
        if status:
            q, args = q + " WHERE status = ?", (status,)
        return [dict(r) for r in self.conn.execute(q + " ORDER BY id", args)]

    def transition(self, slug: str, to_status: str, note: str = "") -> dict:
        content = self.get_content(slug)
        if not content:
            raise KeyError(slug)
        frm = content["status"]
        if to_status not in TRANSITIONS.get(frm, set()):
            raise ValueError(f"transition interdite : {frm} -> {to_status}")
        ts = now()
        with self.tx():
            self.conn.execute("UPDATE contents SET status = ?, updated_at = ? WHERE id = ?", (to_status, ts, content["id"]))
            self.conn.execute(
                "INSERT INTO content_events (content_id, from_status, to_status, note, at) VALUES (?,?,?,?,?)",
                (content["id"], frm, to_status, note, ts),
            )
        return self.get_content(slug)

    def history(self, slug: str) -> list[dict]:
        content = self.get_content(slug)
        if not content:
            return []
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM content_events WHERE content_id = ? ORDER BY id", (content["id"],))]

    # -- rendus & QC ---------------------------------------------------------
    def add_render(self, *, content_id: int | None, path: str, sha256: str, profile: str,
                   width: int, height: int, fps: float, duration: float, params: dict) -> int:
        with self.tx():
            cur = self.conn.execute(
                "INSERT INTO renders (content_id, path, sha256, profile, width, height, fps, duration, params_json, created_at)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (content_id, path, sha256, profile, width, height, fps, duration,
                 json.dumps(params, ensure_ascii=False, default=str), now()),
            )
        return cur.lastrowid

    def find_render(self, sha256: str) -> dict | None:
        row = self.conn.execute("SELECT * FROM renders WHERE sha256 = ? ORDER BY id DESC LIMIT 1", (sha256,)).fetchone()
        return dict(row) if row else None

    def record_qc(self, render_id: int, results: list[dict[str, Any]]) -> str:
        ts = now()
        blocking = [r for r in results if not r["passed"] and r["severity"] == "bloquant"]
        status = "echec" if blocking else ("avertissement" if any(not r["passed"] for r in results) else "conforme")
        with self.tx():
            for r in results:
                self.conn.execute(
                    "INSERT INTO qc_results (render_id, run_at, check_name, passed, severity, value, expected, detail)"
                    " VALUES (?,?,?,?,?,?,?,?)",
                    (render_id, ts, r["name"], int(r["passed"]), r["severity"],
                     _s(r.get("value")), _s(r.get("expected")), _s(r.get("detail"))),
                )
            self.conn.execute("UPDATE renders SET qc_status = ? WHERE id = ?", (status, render_id))
        return status


def _s(v: Any) -> str | None:
    if v is None:
        return None
    return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, default=str)


def _split_sql(script: str) -> list[str]:
    return [s.strip() for s in script.split(";") if s.strip()]
