"""Résolution des chemins du dépôt. Tous les chemins de configuration sont relatifs à la racine."""
from __future__ import annotations

import os
from pathlib import Path

_ROOT_MARKERS = ("config/engine.toml",)


def repo_root() -> Path:
    env = os.environ.get("LUKOJI_ROOT")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if all((parent / m).exists() for m in _ROOT_MARKERS):
            return parent
    raise RuntimeError("Racine du dépôt introuvable (config/engine.toml absent). Définir LUKOJI_ROOT.")


def resolve(path: str | os.PathLike) -> Path:
    """Chemin absolu : inchangé s'il est absolu, sinon relatif à la racine du dépôt."""
    p = Path(path)
    return p if p.is_absolute() else repo_root() / p


def ensure_dir(path: str | os.PathLike) -> Path:
    p = resolve(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def rel(path: str | os.PathLike) -> str:
    """Chemin relatif à la racine pour l'affichage et la base (portable)."""
    p = Path(path).resolve()
    try:
        return str(p.relative_to(repo_root()))
    except ValueError:
        return str(p)
