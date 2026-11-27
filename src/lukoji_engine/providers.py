"""Collecteurs de découverte : Wikipédia (sujets intemporels), GDELT (actualité mondiale), flux RSS.

Un collecteur ne fait que DÉCOUVRIR des pistes (titre, URL, date, extrait). Un résultat de collecteur
n'est jamais une preuve (niveau « resultat_recherche »). En cas d'échec réseau, l'erreur est renvoyée
et journalisée telle quelle : aucun résultat n'est jamais fabriqué.
"""
from __future__ import annotations

import json
import socket
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from email.utils import parsedate_to_datetime

from .config import load_config
from .log import get_logger
from .sources import normalize_url, validate_url

log = get_logger("providers")


@dataclass
class Hit:
    provider: str
    query: str
    rank: int
    title: str
    url: str
    source_name: str | None = None
    published_at: str | None = None
    snippet: str | None = None


@dataclass
class ProviderResult:
    provider: str
    hits: list[Hit] = field(default_factory=list)
    error: dict | None = None


class ProviderError(RuntimeError):
    def __init__(self, kind: str, detail: str):
        super().__init__(f"{kind}: {detail}")
        self.kind, self.detail = kind, detail


def _get(url: str, opener=None) -> bytes:
    cfg = load_config().research["recherche"]
    req = urllib.request.Request(url, headers={"User-Agent": cfg["agent_utilisateur"]})
    opener = opener or urllib.request.build_opener()
    try:
        with opener.open(req, timeout=cfg["delai_reseau_s"]) as r:
            return r.read(3_000_000)
    except urllib.error.HTTPError as e:
        raise ProviderError("http", f"{e.code} {e.reason} ({urllib.parse.urlparse(url).hostname})")
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as e:
        raise ProviderError("inaccessible_environnement", f"{urllib.parse.urlparse(url).hostname} : {e}")


def _clean(hits: list[Hit]) -> list[Hit]:
    """Ne garde que des URL valides ; dédoublonne par URL normalisée."""
    seen, out = set(), []
    for h in hits:
        if validate_url(h.url):
            continue
        h.url = normalize_url(h.url)
        if h.url not in seen:
            seen.add(h.url)
            out.append(h)
    return out


def wikipedia(query: str, limit: int, opener=None) -> list[Hit]:
    cfg = load_config().research["collecteurs"]["wikipedia"]
    hits = []
    for lang in cfg["langues"]:
        host = cfg["hote"].format(lang=lang)
        url = f"https://{host}/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "list": "search", "srsearch": query, "format": "json", "srlimit": limit, "utf8": 1})
        data = json.loads(_get(url, opener))
        for i, r in enumerate(data.get("query", {}).get("search", []), start=1):
            title = r["title"]
            hits.append(Hit("wikipedia", query, i, title,
                            f"https://{host}/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
                            f"Wikipédia ({lang})", r.get("timestamp"),
                            _strip_tags(r.get("snippet", ""))))
    return hits


def gdelt(query: str, limit: int, opener=None) -> list[Hit]:
    cfg = load_config().research["collecteurs"]["gdelt"]
    url = cfg["url"] + "?" + urllib.parse.urlencode(
        {"query": query, "mode": "artlist", "format": "json", "maxrecords": limit, "timespan": cfg["periode"],
         "sort": "hybridrel"})
    raw = _get(url, opener)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ProviderError("reponse_invalide", raw[:200].decode(errors="replace"))
    hits = []
    for i, a in enumerate(data.get("articles", []), start=1):
        hits.append(Hit("gdelt", query, i, a.get("title", "").strip(), a.get("url", ""), a.get("domain"),
                        _gdelt_date(a.get("seendate")), None))
    return hits


def rss(query: str, limit: int, opener=None) -> list[Hit]:
    """Lit les flux configurés et garde les entrées contenant tous les mots de la requête."""
    from .textsim import strip_accents
    feeds = load_config().research["collecteurs"]["rss"]["flux"]
    words = [strip_accents(w.lower()) for w in query.split() if len(w) > 2]
    hits, errors = [], []
    for feed in feeds:
        try:
            root = ET.fromstring(_get(feed["url"], opener))
        except ProviderError as e:
            errors.append(f"{feed['nom']} : {e.detail}")
            continue
        except ET.ParseError as e:
            errors.append(f"{feed['nom']} : flux illisible ({e})")
            continue
        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            desc = _strip_tags(item.findtext("description") or "")
            hay = strip_accents((title + " " + desc).lower())
            if words and not all(w in hay for w in words):
                continue
            hits.append(Hit("rss", query, len(hits) + 1, title, (item.findtext("link") or "").strip(),
                            feed["nom"], _rss_date(item.findtext("pubDate")), desc[:300]))
    if errors and not hits and len(errors) == len(feeds):
        raise ProviderError("inaccessible_environnement", " ; ".join(errors))
    return hits[:limit]


PROVIDERS = {"wikipedia": wikipedia, "gdelt": gdelt, "rss": rss}


def discover(query: str, providers: list[str] | None = None, opener=None) -> list[ProviderResult]:
    cfg = load_config().research
    limit = cfg["recherche"]["max_resultats_par_requete"]
    results = []
    for name in providers or [p for p, c in cfg["collecteurs"].items() if c.get("actif")]:
        if name not in PROVIDERS:
            results.append(ProviderResult(name, error={"type": "inconnu", "detail": f"collecteur inconnu : {name}"}))
            continue
        try:
            hits = _clean(PROVIDERS[name](query, limit, opener))
            results.append(ProviderResult(name, hits))
            log.info("collecte", extra={"provider": name, "query": query, "hits": len(hits)})
        except ProviderError as e:
            results.append(ProviderResult(name, error={"type": e.kind, "detail": e.detail}))
            log.warning("collecteur en échec", extra={"provider": name, "query": query, "type": e.kind, "detail": e.detail})
    return results


def _strip_tags(s: str) -> str:
    import html
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _gdelt_date(s: str | None) -> str | None:
    if not s or len(s) < 8:
        return None
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"


def _rss_date(s: str | None) -> str | None:
    if not s:
        return None
    try:
        return parsedate_to_datetime(s).date().isoformat()
    except (TypeError, ValueError):
        return None
