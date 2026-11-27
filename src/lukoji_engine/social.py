"""Comptes sociaux officiels de LUKOJI MEDIA (config/social.toml).

Phase 0 : enregistrement et validation HORS LIGNE uniquement. Aucune requête réseau,
aucune API, aucune publication. Le chargeur garantit que le fichier :
  - décrit exactement les plateformes attendues, avec des URL https sur le domaine officiel ;
  - est cohérent avec les profils de rendu et le routage éditorial ;
  - ne contient aucun secret (clé ou valeur ressemblant à un jeton / mot de passe).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .config import load_config
from .geometry import list_profiles

EXPECTED = ("youtube", "facebook", "instagram", "tiktok")
FORMATS = ("short", "affiche", "documentaire")
PUBLICATION_STATES = ("desactivee", "brouillon", "active")

# Domaine officiel et forme du chemin attendue pour chaque plateforme.
URL_RULES: dict[str, tuple[set[str], re.Pattern]] = {
    "youtube": ({"www.youtube.com", "youtube.com"}, re.compile(r"^/@[A-Za-z0-9._-]{3,30}/?$")),
    "facebook": ({"www.facebook.com", "facebook.com"}, re.compile(r"^/(share/[A-Za-z0-9]+|[A-Za-z0-9.\-]{5,})/?$")),
    "instagram": ({"www.instagram.com", "instagram.com"}, re.compile(r"^/[A-Za-z0-9._]{1,30}/?$")),
    "tiktok": ({"www.tiktok.com", "tiktok.com"}, re.compile(r"^/@[A-Za-z0-9._]{2,24}/?$")),
}

SECRET_KEY = re.compile(r"(token|secret|password|passwd|mot_de_passe|api_?key|cle_api|client_id|access|bearer|cookie)", re.I)
SECRET_VALUE = re.compile(r"(EAA[A-Za-z0-9]{20,}|ya29\.[\w-]{20,}|AIza[\w-]{30,}|sk-[\w-]{20,}|gh[pousr]_[\w]{20,}|[A-Fa-f0-9]{40,}|[A-Za-z0-9+/_-]{48,})")


@dataclass(frozen=True)
class SocialAccount:
    key: str
    platform: str
    url: str
    handle: str
    type: str
    formats: tuple[str, ...]
    render_profiles: tuple[str, ...]
    publication: str
    notes: str

    @property
    def is_share_link(self) -> bool:
        return "/share/" in urlparse(self.url).path


class SocialConfigError(ValueError):
    pass


def _walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield f"{path}.{k}" if path else k, k, v
            yield from _walk(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}[{i}]")


def find_secrets(data: dict) -> list[str]:
    hits = []
    for path, key, value in _walk(data):
        if SECRET_KEY.search(str(key)):
            hits.append(f"clé suspecte : {path}")
        if isinstance(value, str) and SECRET_VALUE.search(value) and not value.startswith("https://"):
            hits.append(f"valeur ressemblant à un secret : {path}")
    return hits


def validate(data: dict) -> list[str]:
    """Liste des problèmes (vide = configuration valide)."""
    problems = [*find_secrets(data)]
    comptes = data.get("comptes", {})
    if set(comptes) != set(EXPECTED):
        problems.append(f"plateformes attendues {sorted(EXPECTED)}, trouvées {sorted(comptes)}")
    profiles = set(list_profiles())
    for key, c in comptes.items():
        url = c.get("url", "")
        u = urlparse(url)
        rule = URL_RULES.get(key)
        if u.scheme != "https":
            problems.append(f"{key} : l'URL doit être en https ({url!r})")
        if rule:
            hosts, path_re = rule
            if u.hostname not in hosts:
                problems.append(f"{key} : domaine inattendu {u.hostname!r} (attendu {sorted(hosts)})")
            if not path_re.match(u.path or ""):
                problems.append(f"{key} : chemin d'URL inattendu {u.path!r}")
        if u.query or u.fragment:
            problems.append(f"{key} : l'URL ne doit pas contenir de paramètres ({url!r})")
        handle = c.get("identifiant", "")
        if handle and handle.lstrip("@").lower() not in url.lower():
            problems.append(f"{key} : l'identifiant {handle!r} n'apparaît pas dans l'URL")
        for f in c.get("formats", []):
            if f not in FORMATS:
                problems.append(f"{key} : format inconnu {f!r}")
        for p in c.get("profils_rendu", []):
            if p not in profiles:
                problems.append(f"{key} : profil de rendu inconnu {p!r}")
        if c.get("publication") not in PUBLICATION_STATES:
            problems.append(f"{key} : état de publication invalide {c.get('publication')!r}")
    for fmt, targets in data.get("routage", {}).items():
        if fmt not in FORMATS:
            problems.append(f"routage : format inconnu {fmt!r}")
        for t in targets:
            if t not in comptes:
                problems.append(f"routage {fmt} : compte inconnu {t!r}")
            elif fmt not in comptes[t].get("formats", []):
                problems.append(f"routage {fmt} -> {t} : format absent des formats du compte")
    # Règle éditoriale : affiches uniquement sur Facebook et Instagram.
    if set(data.get("routage", {}).get("affiche", [])) - {"facebook", "instagram"}:
        problems.append("routage : les affiches sont réservées à Facebook et Instagram")
    return problems


def load_accounts(strict: bool = True) -> dict[str, SocialAccount]:
    data = load_config().social
    problems = validate(data)
    if problems and strict:
        raise SocialConfigError("config/social.toml invalide :\n- " + "\n- ".join(problems))
    return {
        key: SocialAccount(key, c["plateforme"], c["url"], c.get("identifiant", ""), c.get("type", ""),
                           tuple(c.get("formats", [])), tuple(c.get("profils_rendu", [])),
                           c.get("publication", "desactivee"), c.get("notes", ""))
        for key, c in data["comptes"].items()
    }


def destinations(fmt: str) -> list[SocialAccount]:
    """Comptes officiels de destination d'un format (short, affiche, documentaire)."""
    accounts = load_accounts()
    return [accounts[k] for k in load_config().social["routage"].get(fmt, [])]
