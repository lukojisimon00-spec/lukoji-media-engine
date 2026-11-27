"""Configuration centralisée : fichiers TOML de config/ + surcharges par variables d'environnement.

Surcharge : LUKOJI_<SECTION>__<CLE>=valeur (ex. LUKOJI_ENCODE__CRF=20). Les valeurs sont
converties en int/float/bool lorsque c'est possible. Aucun secret n'est stocké en configuration :
les futurs jetons (publication, API) seront lus depuis l'environnement uniquement.
"""
from __future__ import annotations

import copy
import os
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from .paths import resolve

ENV_PREFIX = "LUKOJI_"


def _coerce(value: str) -> Any:
    low = value.lower()
    if low in ("true", "false"):
        return low == "true"
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            pass
    return value


def _apply_env(data: dict, env: dict[str, str]) -> dict:
    data = copy.deepcopy(data)
    for key, value in env.items():
        if not key.startswith(ENV_PREFIX) or "__" not in key:
            continue
        parts = [p.lower() for p in key[len(ENV_PREFIX):].split("__")]
        node = data
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = _coerce(value)
    return data


def load_toml(name: str) -> dict:
    with open(resolve(f"config/{name}.toml"), "rb") as fh:
        return tomllib.load(fh)


@dataclass(frozen=True)
class Config:
    engine: dict
    brand: dict
    platforms: dict

    def get(self, dotted: str, default: Any = None) -> Any:
        """Accès pointé dans engine.toml : cfg.get('encode.crf')."""
        node: Any = self.engine
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def path(self, key: str):
        return resolve(self.engine["paths"][key])


@lru_cache(maxsize=1)
def load_config() -> Config:
    return Config(
        engine=_apply_env(load_toml("engine"), dict(os.environ)),
        brand=load_toml("brand"),
        platforms=load_toml("platforms"),
    )
