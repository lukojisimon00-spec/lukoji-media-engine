"""Similarité de textes pour la détection de doublons (bibliothèque standard uniquement).

- normalisation : minuscules, accents retirés, ponctuation retirée ;
- mots vides FR/EN retirés ; racinisation légère (suffixes courants) ;
- unigrammes + bigrammes pondérés TF-IDF sur le corpus comparé, similarité cosinus ;
- entités comparées par Jaccard après normalisation.
"""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

STOP = set("""
a ai aie au aux avec ce ces cet cette ci comme dans de des du elle elles en entre est et etre eu il ils
je la le les leur leurs lui ma mais me meme mes moi mon ne nos notre nous on ont ou par pas plus pour qu que
qui sa sans se ses si son sont sur ta te tes toi ton tu un une vos votre vous y ete etait sera comment
pourquoi quand quoi dont ceux celle celui alors ainsi aussi tres tout tous toute toutes fait faire peut
the a an and or of to in on for with by from at as is are was were be been it its this that these those
how why what when who which into over under than then their there they he she his her not but
""".split())

_SUFFIXES = ("issements", "issement", "ations", "ation", "ements", "ement", "ments", "ment", "euses", "euse",
             "eurs", "eur", "ités", "ité", "ites", "ite", "iques", "ique", "ismes", "isme", "istes", "iste",
             "ances", "ance", "ences", "ence", "ings", "ing", "ies", "es", "s")


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def stem(word: str) -> str:
    for suf in _SUFFIXES:
        if len(word) > len(suf) + 3 and word.endswith(suf):
            return word[: -len(suf)]
    return word


def tokens(text: str) -> list[str]:
    t = strip_accents(text.lower())
    words = re.findall(r"[a-z0-9]+", t)
    return [stem(w) for w in words if w not in STOP and len(w) > 1]


def features(text: str) -> Counter:
    toks = tokens(text)
    feats = Counter(toks)
    feats.update(f"{a}_{b}" for a, b in zip(toks, toks[1:]))
    return feats


class Corpus:
    """Vecteurs TF-IDF d'un ensemble de documents (le corpus inclut les textes comparés)."""

    def __init__(self, docs: list[str]):
        self.feats = [features(d) for d in docs]
        df = Counter()
        for f in self.feats:
            df.update(set(f))
        n = len(docs)
        self.idf = {k: math.log((1 + n) / (1 + v)) + 1.0 for k, v in df.items()}

    def vector(self, text_or_feats) -> dict[str, float]:
        f = features(text_or_feats) if isinstance(text_or_feats, str) else text_or_feats
        v = {k: (1 + math.log(c)) * self.idf.get(k, math.log(len(self.feats) + 1) + 1.0) for k, c in f.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {k: x / norm for k, x in v.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(k, 0.0) for k, x in a.items())


def norm_entity(e: str) -> str:
    return " ".join(tokens(e)) or strip_accents(e.lower()).strip()


def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = {norm_entity(x) for x in a if x}, {norm_entity(x) for x in b if x}
    sa.discard(""); sb.discard("")
    return len(sa & sb) / len(sa | sb) if sa and sb else 0.0
