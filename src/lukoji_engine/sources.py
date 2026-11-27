"""Gestion des sources : validation d'URL, classement A/B/C, récupération, vérification d'extraits.

Principes (aucune source inventée) :
- une URL n'est acceptée que si elle est syntaxiquement valide, publique, et a été CONSULTÉE :
  soit récupérée par le moteur (page_verifiee), soit lue par l'agent de lecture (page_lue_agent) ;
  un simple résultat de recherche (resultat_recherche) n'est jamais une preuve ;
- la catégorie vient du registre de domaines (config/research.toml) ; une catégorie déclarée pour un
  domaine inconnu est conservée mais marquée « declaree » (à revoir) ;
- un extrait n'est « verifie » que s'il est retrouvé dans le texte récupéré par le moteur.
"""
from __future__ import annotations

import hashlib
import html
import ipaddress
import json
import re
import socket
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from .config import load_config
from .log import get_logger
from .paths import ensure_dir, rel

log = get_logger("sources")

CONSULTATION_LEVELS = ("resultat_recherche", "page_lue_agent", "page_verifiee")
TRACKING_PARAMS = re.compile(r"^(utm_|fbclid$|gclid$|mc_cid$|mc_eid$|igshid$|ref_src$)")
FORBIDDEN_HOSTS = {"localhost", "example.com", "example.org", "example.net", "test", "invalid"}


class SourceError(ValueError):
    pass


# ---------------------------------------------------------------------------
# URL
# ---------------------------------------------------------------------------
def normalize_url(url: str) -> str:
    """Forme canonique : https/http conservé, hôte en minuscules, sans fragment ni paramètres de pistage."""
    u = urlparse(url.strip())
    query = urlencode([(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True) if not TRACKING_PARAMS.match(k)])
    path = u.path or "/"
    host = (u.hostname or "").lower()
    netloc = host + (f":{u.port}" if u.port and u.port not in (80, 443) else "")
    return urlunparse((u.scheme.lower(), netloc, path, "", query, ""))


def validate_url(url: str) -> list[str]:
    """Problèmes de forme d'une URL (vide = valide). Ne contacte pas le réseau."""
    problems = []
    if not isinstance(url, str) or not url.strip():
        return ["URL vide"]
    if any(c.isspace() for c in url.strip()):
        problems.append("URL contenant des espaces")
    u = urlparse(url.strip())
    if u.scheme not in ("https", "http"):
        problems.append(f"schéma non accepté : {u.scheme!r}")
    host = (u.hostname or "").lower()
    if not host or "." not in host:
        problems.append(f"hôte invalide : {host!r}")
    else:
        try:
            ip = ipaddress.ip_address(host)
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                problems.append("adresse IP privée ou réservée")
        except ValueError:
            pass
        labels = host.split(".")
        if host in FORBIDDEN_HOSTS or labels[-1] in FORBIDDEN_HOSTS or ".".join(labels[-2:]) in FORBIDDEN_HOSTS:
            problems.append(f"domaine d'exemple ou réservé : {host}")
        if not re.fullmatch(r"[a-z0-9.-]+", host) or any(not lab or lab.startswith("-") for lab in labels):
            problems.append(f"nom d'hôte mal formé : {host}")
        if not re.fullmatch(r"[a-z]{2,24}|xn--[a-z0-9-]+", labels[-1]):
            problems.append(f"extension de domaine invalide : .{labels[-1]}")
    if u.username or u.password:
        problems.append("identifiants dans l'URL")
    return problems


def domain_of(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def classify(url: str, declared: dict | None = None) -> dict:
    """Organisation, catégorie et nature depuis le registre (suffixe de domaine le plus long)."""
    reg = load_config().research["sources"]["domaines"]
    host = domain_of(url)
    labels = host.split(".")
    for i in range(len(labels) - 1):
        suffix = ".".join(labels[i:])
        if suffix in reg:
            e = reg[suffix]
            org, nature = e["org"], e.get("nature")
            if e.get("plateforme") and declared and declared.get("organisation"):
                org, nature = declared["organisation"], f"{nature} — hébergé par {e['org']}"
            return {"organisation": org, "category": e["cat"], "nature": nature, "category_origin": "registre"}
    if declared and declared.get("categorie") in ("A", "B", "C") and declared.get("justification_categorie"):
        return {"organisation": declared.get("organisation") or host, "category": declared["categorie"],
                "nature": declared.get("nature"), "category_origin": "declaree"}
    return {"organisation": (declared or {}).get("organisation") or host, "category": "C",
            "nature": (declared or {}).get("nature") or "non répertoriée", "category_origin": "defaut_C"}


# ---------------------------------------------------------------------------
# Récupération et analyse HTML (bibliothèque standard uniquement)
# ---------------------------------------------------------------------------
class _PageParser(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template", "iframe"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.title = ""
        self.times: list[str] = []
        self.jsonld: list[str] = []
        self._in_title = False
        self._skip = 0
        self._jsonld = False
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self._skip += 1
            if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
                self._jsonld = True
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            key = (a.get("property") or a.get("name") or a.get("itemprop") or "").lower()
            if key and a.get("content"):
                self.meta.setdefault(key, a["content"])
        if tag == "time" and a.get("datetime"):
            self.times.append(a["datetime"])
        if tag in ("p", "br", "div", "li", "h1", "h2", "h3", "h4", "tr", "section", "article"):
            self.text.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP and self._skip:
            self._skip -= 1
            self._jsonld = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._jsonld:
            self.jsonld.append(data)
            return
        if self._in_title:
            self.title += data
        if not self._skip:
            self.text.append(data)


def _jsonld_dates(blocks: list[str]) -> list[str]:
    found = []
    for b in blocks:
        for m in re.finditer(r'"date(?:Published|Created)"\s*:\s*"([^"]+)"', b):
            found.append(m.group(1))
    return found


def parse_html(raw: str) -> dict:
    p = _PageParser()
    try:
        p.feed(raw)
    except Exception:  # HTML très dégradé : on garde ce qui a été lu
        pass
    text = re.sub(r"[ \t\r\f\v]+", " ", "".join(p.text))
    text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
    published = (p.meta.get("article:published_time") or p.meta.get("datepublished")
                 or p.meta.get("og:article:published_time") or p.meta.get("date")
                 or next(iter(_jsonld_dates(p.jsonld)), None) or (p.times[0] if p.times else None))
    return {
        "title": html.unescape((p.meta.get("og:title") or p.title or "").strip()),
        "site_name": html.unescape(p.meta.get("og:site_name", "")).strip() or None,
        "published_at": published,
        "text": text,
    }


@dataclass
class FetchResult:
    url: str
    ok: bool
    availability: str                # disponible | indisponible | inaccessible_environnement
    http_status: int | None = None
    final_url: str | None = None
    title: str | None = None
    site_name: str | None = None
    published_at: str | None = None
    text: str = ""
    content_sha256: str | None = None
    error: str | None = None
    text_path: str | None = None
    meta: dict = field(default_factory=dict)


def _opener():
    return urllib.request.build_opener()


def fetch(url: str, opener=None) -> FetchResult:
    """Récupère une page. Distingue « indisponible » (le site répond 4xx/5xx) de
    « inaccessible_environnement » (réseau/proxy de l'environnement : la source n'est pas jugée)."""
    cfg = load_config().research["recherche"]
    opener = opener or _opener()
    req = urllib.request.Request(url, headers={"User-Agent": cfg["agent_utilisateur"],
                                               "Accept-Language": "fr,en;q=0.8"})
    try:
        with opener.open(req, timeout=cfg["delai_reseau_s"]) as resp:
            raw = resp.read(5_000_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            status = getattr(resp, "status", 200)
            final = resp.geturl() if hasattr(resp, "geturl") else url
    except urllib.error.HTTPError as e:
        # 403 du proxy de l'environnement ≠ 403 du site : on regarde l'en-tête de refus du proxy.
        proxy_refusal = e.code in (403, 407) and "proxy" in str(e.headers.get("Via", "") + str(e.reason)).lower()
        if e.code in (404, 410, 451) or (500 <= e.code < 600):
            return FetchResult(url, False, "indisponible", e.code, error=f"HTTP {e.code}")
        return FetchResult(url, False, "inaccessible_environnement" if proxy_refusal else "indisponible",
                           e.code, error=f"HTTP {e.code} {e.reason}")
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
        return FetchResult(url, False, "inaccessible_environnement", None, error=f"réseau : {e}")
    text_raw = raw.decode(charset, errors="replace")
    parsed = parse_html(text_raw)
    digest = hashlib.sha256(parsed["text"].encode()).hexdigest()
    store = ensure_dir(Path(load_config().engine["paths"]["cache"]) / "sources")
    tpath = store / f"{digest[:16]}.txt"
    tpath.write_text(parsed["text"], encoding="utf-8")
    return FetchResult(url, True, "disponible", status, final, parsed["title"] or None, parsed["site_name"],
                       parsed["published_at"], parsed["text"], digest, None, rel(tpath))


# ---------------------------------------------------------------------------
# Extraits
# ---------------------------------------------------------------------------
def _norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("«", '"').replace("»", '"')
    s = s.replace(" ", " ").replace(" ", " ").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r'"\s+', '"', s)
    s = re.sub(r'\s+"', '"', s)
    return s.strip().lower()


def excerpt_in_text(excerpt: str, text: str) -> bool:
    """L'extrait figure-t-il dans le texte (à la typographie près : espaces, apostrophes, guillemets) ?"""
    e = _norm_text(excerpt).strip(' ".…')
    return bool(e) and len(e) >= 12 and e in _norm_text(text)


def excerpt_status(excerpt: str, consultation: str, text: str | None) -> str:
    """verifie (retrouvé dans la page récupérée) | absent_de_la_page | rapporte_agent | non_probant."""
    if consultation == "page_verifiee":
        return "verifie" if text and excerpt_in_text(excerpt, text) else "absent_de_la_page"
    if consultation == "page_lue_agent":
        return "rapporte_agent"
    return "non_probant"


def load_cached_text(text_path: str | None) -> str | None:
    if not text_path:
        return None
    from .paths import resolve
    p = resolve(text_path)
    return p.read_text(encoding="utf-8") if p.exists() else None


def is_probative(consultation: str, check: str) -> bool:
    """Une preuve compte si la page a été consultée (agent ou moteur) et l'extrait non démenti."""
    probants = load_config().research["verification"]["niveaux_probants"]
    return consultation in probants and check in ("verifie", "rapporte_agent")


def to_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)
