"""Doublures réseau et dossier SIMULÉ pour les tests de la phase 1.

Tout ce qui est ici est FICTIF et marqué comme tel : ces données servent uniquement à tester le
comportement du moteur ; elles ne sont jamais présentées comme une recherche réelle.
"""
import copy
import io
import urllib.error


class FakeResponse(io.BytesIO):
    def __init__(self, body: bytes, status=200, url="", charset="utf-8"):
        super().__init__(body)
        self.status = status
        self._url = url
        self.headers = _Headers(charset)

    def geturl(self):
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _Headers(dict):
    def __init__(self, charset):
        super().__init__()
        self._c = charset

    def get_content_charset(self):
        return self._c


class FakeOpener:
    """routes : url -> bytes | int (code HTTP d'erreur) | Exception."""

    def __init__(self, routes: dict, default=None):
        self.routes, self.default, self.calls = routes, default, []

    def open(self, req, timeout=None):
        url = req.full_url
        self.calls.append(url)
        r = self.routes.get(url, self.default)
        if r is None:
            raise urllib.error.URLError("Tunnel connection failed: 403 Forbidden (simulé)")
        if isinstance(r, Exception):
            raise r
        if isinstance(r, int):
            raise urllib.error.HTTPError(url, r, "simulé", {}, None)
        return FakeResponse(r, 200, url)


def page(title: str, body: str, published="2026-10-01T08:00:00Z", site="Média simulé") -> bytes:
    return f"""<html><head><title>{title} | {site}</title>
<meta property="og:title" content="{title}"><meta property="og:site_name" content="{site}">
<meta property="article:published_time" content="{published}"></head>
<body><script>var x = "ne pas lire";</script><article><h1>{title}</h1><p>{body}</p></article></body></html>""".encode()


URL_A = "https://www.worldbank.org/fr/news/simule-rapport-2026"
URL_B1 = "https://www.rfi.fr/fr/afrique/simule-article?utm_source=x#haut"
URL_B2 = "https://www.lemonde.fr/afrique/article/simule.html"
URL_C = "https://medium.com/@simule/billet"
URL_404 = "https://www.jeuneafrique.com/simule-disparu/"

PAGES = {
    "https://www.worldbank.org/fr/news/simule-rapport-2026": page(
        "Rapport simulé", "Selon ce rapport simulé, le corridor fictif a transporté 1,2 million de tonnes en 2025."),
    "https://www.rfi.fr/fr/afrique/simule-article": page(
        "Article simulé RFI", "Le projet fictif Alpha a été lancé en 2019 par une coopérative de Goma."),
    "https://www.lemonde.fr/afrique/article/simule.html": page(
        "Article simulé Le Monde", "Lancé en 2019, le projet fictif Alpha réunit aujourd'hui 300 producteurs."),
    "https://medium.com/@simule/billet": page("Billet simulé", "Alpha serait le plus grand projet du continent."),
}


def make_dossier(**over) -> dict:
    d = {
        "session": {"mode": "test_simule", "chercheur": "suite de tests (données SIMULÉES)",
                    "requetes": ["requête simulée"]},
        "sources": [
            {"id": "a", "url": URL_A, "titre": "Rapport simulé", "date_publication": "2026-01-15",
             "date_consultation": "2026-11-27", "consultation": "page_lue_agent", "limites": "données simulées"},
            {"id": "b1", "url": URL_B1, "titre": "Article simulé RFI", "date_consultation": "2026-11-27",
             "consultation": "page_lue_agent"},
            {"id": "b2", "url": URL_B2, "titre": "Article simulé Le Monde", "date_consultation": "2026-11-27",
             "consultation": "page_lue_agent"},
            {"id": "c", "url": URL_C, "titre": "Billet simulé", "date_consultation": "2026-11-27",
             "consultation": "page_lue_agent"},
        ],
        "propositions": [{
            "titre": "[SIMULÉ] Le projet Alpha de Goma",
            "sujet": "Une coopérative fictive de Goma et son projet Alpha",
            "angle": "Comment une coopérative a fédéré 300 producteurs en six ans",
            "famille": "business", "territoire": "rdc", "temporalite": "tendance",
            "interet": "Exemple de structuration de filière", "accroche": "300 producteurs, une idée.",
            "resume": "Récit fictif de test.", "entites": ["Alpha", "Goma", "coopérative"],
            "formats": ["short", "affiche"], "episodes": 1, "potentiel_visuel": "Cartes, photos de terrain",
            "difficulte": {"note": 2, "justification": "sources accessibles"},
            "risque_juridique": {"note": 1, "justification": "aucune mise en cause"},
            "risques": ["données simulées"],
            "notes_editoriales": {k: {"note": 4, "justification": "test"} for k in
                                  ("potentiel_narratif", "interet_public", "originalite", "potentiel_visuel",
                                   "potentiel_hook", "pertinence_lukoji")},
            "faits": [
                {"texte": "Le projet Alpha a été lancé en 2019.", "type": "fait", "importance": "cle",
                 "preuves": [{"source": "b1", "extrait": "Le projet fictif Alpha a été lancé en 2019"},
                             {"source": "b2", "extrait": "Lancé en 2019, le projet fictif Alpha"}]},
                {"texte": "Le corridor a transporté 1,2 million de tonnes en 2025.", "type": "chiffre",
                 "importance": "cle",
                 "preuves": [{"source": "a", "extrait": "le corridor fictif a transporté 1,2 million de tonnes en 2025"}]},
                {"texte": "Alpha est le plus grand projet du continent.", "type": "fait", "importance": "secondaire",
                 "preuves": [{"source": "c", "extrait": "Alpha serait le plus grand projet du continent"}]},
            ],
        }],
    }
    for k, v in over.items():
        d[k] = v
    return copy.deepcopy(d)
