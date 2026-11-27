"""Registre factuel v2 du pilote M-Pesa (STO-20261127-001).

Statuts (définis pour la révision v2, distincts des statuts calculés par le moteur) :
- confirmed     : ce que dit ou contient un document primaire consulté (citation, signature, déclaration) ;
- corroborated  : établi par au moins DEUX organisations indépendantes consultées
                  (deux pages d'une même organisation ne comptent que pour une) ;
- single_source : une seule organisation consultée (y compris un communiqué d'entreprise, jamais
                  considéré comme une vérification indépendante) ;
- uncertain     : non établi (source non consultée, indicateur inconnu, indices seulement) ;
- excluded      : retiré du script v2 (motif obligatoire).

Ce fichier ne contient aucun texte intégral d'article : uniquement des références, de courts extraits déjà
présents dans le dossier factuel du moteur, et les formulations de la voix off v2.

Usage : python3 research/stories/mpesa/v2/registre_v2.py [--db var/lukoji.sqlite3] [--out docs/stories/STO-20261127-001/v2]
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STATUSES = ("confirmed", "corroborated", "single_source", "uncertain", "excluded")

# ref : (statut v2, formulation exacte dans la voix off v2 (sous-chaîne), attribution dans la voix off, limites)
USED = {
 "F61": ("single_source", "on pouvait voyager pendant des jours. Ou confier ses billets à un chauffeur de bus",
         "à l'écran : « SOURCE DU RÉCIT : VODAFONE (2017) »",
         "Anecdote racontée par Vodafone seule (source intéressée) ; aucune date précise."),
 "F43": ("single_source", "Quelques SMS plus tard, la somme est devenue de la monnaie électronique, stockée sur sa carte SIM",
         "« raconte Vodafone » (même séquence)", "Description du fonctionnement par Vodafone seule."),
 "F51": ("single_source", "seuls 27 % des Kényans ont accès à des produits ou des services financiers",
         "« selon Agence Ecofin qui la cite » (enquête FSD Kenya / Banque centrale)",
         "Source secondaire : le rapport FinAccess 2019 n'a pas été consulté ; définition exacte de l'indicateur (formel / informel) non vérifiée."),
 "F41": ("single_source", "l'entreprise saisit l'occasion et obtient une subvention",
         "« Selon Vodafone »", "Deux pages Vodafone (2017, 2022) : une seule organisation, intéressée. Aucun document du DFID consulté."),
 "F42": ("corroborated", "le projet se monte avec l'opérateur Safaricom",
         "non requise", "Vodafone (2022) et Agence Ecofin (2023) : lancement par Safaricom et Vodafone. Le jour exact (6 mars 2007) n'est plus utilisé."),
 "F62": ("single_source", "Michael Joseph, ancien directeur général de Safaricom, raconte la suite dans un texte publié par Vodafone",
         "« raconte … dans un texte publié par Vodafone »",
         "Auteur du texte : confirmé par la page Vodafone ; « ancien directeur général de Safaricom » : Agence Ecofin seule."),
 "F8": ("single_source", "L'équipe travaille sur le microcrédit : verser de petits prêts par téléphone, et les faire rembourser de la même façon. Le prototype est testé à Thika, au nord de Nairobi",
        "« explique-t-il » (Michael Joseph, texte Vodafone)",
        "Récit des origines par Vodafone seule ; aucune corroboration indépendante trouvée (point ouvert)."),
 "F63": ("confirmed", "« Alors nous avons pris un risque », raconte Michael Joseph",
         "« raconte Michael Joseph » ; original anglais à l'écran", "Déclaration confirmée comme telle ; elle n'établit pas les faits qu'elle raconte."),
 "F9": ("single_source", "Le système de prêts est reconstruit autour d'une seule fonction : envoyer de l'argent d'un téléphone à un autre",
        "contexte : récit de Michael Joseph", "Vodafone seule."),
 "F44": ("single_source", "Ces agents, raconte Vodafone, sont souvent de petites boutiques familiales",
         "« raconte Vodafone »", "Vodafone seule."),
 "F45": ("single_source", "la Banque centrale du Kenya pose ses conditions : un plafond de dépôt contre le blanchiment, la protection des clients, la sécurité des agents",
         "aucune dans la voix off (fait de contexte) ; source à l'écran",
         "Conditions : Agence Ecofin ; enregistrement des clients : Vodafone. Chaque élément repose sur une seule organisation."),
 "F7": ("corroborated", "M-Pesa est lancé en mars 2007",
        "non requise", "Vodafone (2017) et Banque centrale citée par Agence Ecofin (« mars 2007, date de son lancement ») ; Wikipédia en appoint."),
 "F46": ("single_source", "Selon Agence Ecofin, des banques y voient une incursion dans leur métier",
         "« Selon Agence Ecofin »", "Article non daté ; banques non nommées."),
 "F66": ("single_source", "Le 27 janvier 2009, la Banque centrale publie un communiqué pour rassurer",
         "« Selon Agence Ecofin » (même séquence) ; à l'écran : « citée par Agence Ecofin »",
         "Communiqué original non consulté ; citation rapportée par Agence Ecofin (article dont un autre chiffre est erroné)."),
 "F10": ("single_source", "Vodafone annonce 1,2 million d'utilisateurs à la fin de la première année",
         "« Vodafone annonce »", "Chiffre de l'entreprise, non audité."),
 "F49": ("single_source", "l'entreprise en revendique plus de 51 millions, servis par 600 000 agents, dans sept pays",
         "« revendique »", "Chiffres de l'entreprise, non audités ; liste des sept pays non reprise (seule la RDC est nommée)."),
 "F68": ("single_source", "Selon eux, cela suggère que des enfants partis travailler soutiennent leurs parents",
         "« Selon eux »", "Interprétation des chercheurs rapportée par MIT News (« strongly suggests »)."),
 "F40": ("single_source", "41 % des transferts étudiés partent vers des parents, 8 % vers des enfants",
         "« les économistes Tavneet Suri et William Jack »", "MIT News (2010) ; working paper non consulté ; période exacte des données non précisée."),
 "F11": ("single_source", "l'accès à l'argent mobile aurait fait sortir de l'extrême pauvreté quelque 194 000 foyers, soit 2 % des ménages du pays",
         "« Leur estimation » + conditionnel", "Compte rendu MIT News de l'article de Science (2016), non consulté ; résultat discuté dans la littérature (non vérifié par l'agent)."),
 "F52": ("single_source", "Ils comparent les familles selon le nombre d'agents installés près de chez eux",
         "« Ils » (Suri et Jack)", "Méthode décrite par MIT News."),
 "F12": ("single_source", "Environ 185 000 femmes auraient quitté l'agriculture pour des activités commerciales",
         "conditionnel ; « Ce sont des estimations »", "MIT News : « from farming to business occupations »."),
 "F55": ("single_source", "certains transferts coûtent près de 7 % du montant envoyé",
         "« Selon Agence Ecofin » ; « Des médias kényans rapportent un projet »",
         "Agence Ecofin (oct. 2025) rapportant « plusieurs médias locaux » ; projet de la Banque centrale non confirmé comme adopté."),
 "F53": ("single_source", "il pèse 44,2 % des revenus de Safaricom", "« selon la même agence »",
         "Rapport annuel de Safaricom non consulté."),
 "F64": ("single_source", "En novembre 2020, des sénateurs kényans menacent à nouveau de séparer M-Pesa des activités télécoms de Safaricom, qu'ils jugent de plus en plus dominante",
         "« des sénateurs kényans … qu'ils jugent »",
         "Contenu : Agence Ecofin (extraits capturés). Date : établie par indices concordants (liens connexes datés, numérotation Ecofin, URL de The Star et Techweez datées des 17-18/11/2020, vues en résultat de recherche seulement) ; page Ecofin non relue (Cloudflare)."),
 "F65": ("single_source", "Sur l'exercice clos en mars 2022, les paris en ligne étaient devenus la deuxième source de revenus de M-Pesa",
         "« Selon Agence Ecofin » (séquence)", "Agence Ecofin (mai 2022) ; rapport annuel de Safaricom non consulté."),
 "F58": ("single_source", "Le crédit sur mobile, lui, a démocratisé l'emprunt, mais il soulève la question de la protection des plus pauvres",
         "source à l'écran (Agence Ecofin, 2019)", "Agence Ecofin (2019)."),
 "F67": ("single_source", "En 2019, FSD Kenya comptait déjà 49 plateformes de prêt, dans un secteur très peu réglementé",
         "« FSD Kenya » ; à l'écran « via Agence Ecofin »", "Agence Ecofin (2019) citant FSD Kenya."),
 "F59": ("confirmed", "Selon son auteur, l'argent mobile ne s'attaque pas aux causes systémiques de la pauvreté",
         "« Une thèse d'économie, présentée dans la Revue de la régulation … Selon son auteur »",
         "Opinion attribuée, confirmée comme telle (présentation de thèse consultée) ; l'auteur n'est pas nommé (nom non relevé)."),
}

# Corroboration apportée par la preuve d'un autre fait du dossier (même document cité).
EXTRA_CORROBORATION = {"F7": ["F66"]}

EXCLUDED = {
 "F38": ("excluded", "v1 : « seuls 22 % des adultes ont alors un compte bancaire » (présenté comme antérieur à M-Pesa)",
         "Enquête de 2008, POSTÉRIEURE au lancement ; origine du chiffre de 22 % non précisée par le MIT ; working paper non consulté."),
 "F39": ("excluded", "v1 : « 77 % des Kényans disent garder leur argent sous le matelas »",
         "Enquête de 2008 (après le lancement) ; base du pourcentage non précisée ; « so to speak » : figure de style."),
 "F47": ("excluded", "v1 : « environ 30 000 points de ce type, contre seulement 400 agences bancaires » (début 2012)",
         "« 400 agences » contredit par la Banque centrale du Kenya : 1 161 agences en décembre 2011 (communiqué vu en résultat de recherche seulement) ; comparaison retirée, y compris les 30 000 points."),
 "F54": ("excluded", "v1 : « M-Pesa détient 90,8 % des parts de marché »",
         "Indicateur non établi (abonnements, transactions ou valeur ?) ; rapport de l'Autorité des communications non consulté ; la presse kényane (Capital FM, vue en résultat de recherche) confirme le chiffre pour le trimestre clos fin mars 2025 sans préciser l'indicateur."),
 "F56": ("excluded", "v1 : « Dès 2018, des sénateurs … jugé trop dominant »",
         "Date fausse (novembre 2020) et « trop dominant » non attribuable aux sénateurs ; remplacé par F64."),
 "F57": ("excluded", "v1 : « Les paris en ligne sont devenus la deuxième source de revenus » (présent)",
         "Constat daté (exercice 2022) présenté au présent ; remplacé par F65."),
 "F48": ("excluded", "v1 : chiffres Vodafone de fin 2016 (29,5 millions, 287 400 agents, 10 pays)",
         "Retrait éditorial : un seul jeu de chiffres d'entreprise ; « 10 pays » puis « sept pays » créait une incohérence non expliquée."),
 "F13": ("excluded", "pilote financé par le DFID (Wikipédia seule)", "Wikipédia seule ; information reprise par F41 (Vodafone)."),
 "F69": ("excluded", "enquête 2008 de Suri et Jack (3 000 ménages, 92 % de la population)",
         "Fait correct, enregistré en v2 pour corriger F38/F39 ; non utilisé dans la voix off."),
 "F70": ("uncertain", "agences bancaires 2011-2012 (Banque centrale du Kenya)",
         "Source non consultée (résultat de recherche) ; sert uniquement à justifier le retrait de F47."),
 "F71": ("uncertain", "part de 90,8 % selon Capital FM", "Source non consultée ; indicateur inconnu."),
}


def load_research(db_path: Path) -> dict:
    c = sqlite3.connect(db_path)
    row = c.execute("SELECT a.content_json, a.version FROM story_artifacts a JOIN story_projects p ON p.id = a.project_id "
                    "WHERE p.sid = 'STO-20261127-001' AND a.kind = 'research' ORDER BY a.version DESC LIMIT 1").fetchone()
    doc = json.loads(row[0])
    doc["_version"] = row[1]
    return doc


def build(db_path: Path) -> dict:
    research = load_research(db_path)
    facts = {f["ref"]: f for f in research["faits"]}
    sources = {s["ref"]: s for s in research["sources"]}
    entries = []
    for ref, spec in list(USED.items()) + list(EXCLUDED.items()):
        f = facts[ref]
        srcs = []
        for p in f["preuves"]:
            s = sources.get(p["source"], {})
            srcs.append({"ref": p["source"], "organisation": p["organisation"], "categorie": p["categorie"],
                         "titre": s.get("title"), "url": s.get("url"), "date": s.get("published_at"),
                         "consultation": s.get("consultation"), "verification_extrait": p["verification"]})
        for other in EXTRA_CORROBORATION.get(ref, []):
            for p in facts[other]["preuves"]:
                s = sources.get(p["source"], {})
                srcs.append({"ref": p["source"], "organisation": p["organisation"], "categorie": p["categorie"],
                             "titre": s.get("title"), "url": s.get("url"), "date": s.get("published_at"),
                             "consultation": s.get("consultation"), "verification_extrait": p["verification"],
                             "via_fait": other})
        orgs = sorted({s["organisation"] for s in srcs if s["consultation"] == "page_verifiee"})
        if ref in USED:
            status, vo, attribution, limits = spec
            e = {"ref": ref, "statut": status, "utilise_v2": True, "formulation_voix_off": vo, "attribution": attribution,
                 "limites": limits}
        else:
            status, used_before, why = spec
            e = {"ref": ref, "statut": status, "utilise_v2": False, "formulation_v1_ou_objet": used_before,
                 "motif": why}
        e.update({"texte_dossier": f["texte"], "statut_moteur": f["statut"], "usage_moteur": f["usage"],
                  "type": f["type"], "sources": srcs, "organisations_consultees": orgs,
                  "niveau_verification": ("extraits vérifiés contre la capture du moteur" if any(s["verification_extrait"] == "verifie" for s in srcs)
                                          else "aucune page consultée")})
        entries.append(e)
    return {"projet": "STO-20261127-001", "version_editoriale": "v2", "research_version_moteur": research["_version"],
            "statuts": {"confirmed": "ce que dit un document primaire consulté", "corroborated": "≥ 2 organisations indépendantes consultées",
                        "single_source": "une seule organisation consultée", "uncertain": "non établi", "excluded": "retiré du script v2"},
            "faits": entries}


def to_markdown(reg: dict) -> str:
    L = ["# Registre factuel — version 2", "",
         f"Projet `{reg['projet']}` · dossier factuel du moteur v{reg['research_version_moteur']} · statuts v2 : "
         + " · ".join(f"**{k}** = {v}" for k, v in reg["statuts"].items()), "",
         "> Deux pages d'une même organisation ne comptent que pour une. Un communiqué d'entreprise n'est jamais une vérification indépendante. "
         "Aucune source n'est déclarée consultée si elle ne l'a pas été.", ""]
    used = [e for e in reg["faits"] if e["utilise_v2"]]
    L += ["## Faits utilisés dans la voix off v2", "", "| Réf. | Statut v2 | Formulation (voix off) | Sources | Attribution | Limites |", "|---|---|---|---|---|---|"]
    for e in used:
        src = "<br>".join(f"{s['ref']} {s['organisation']} ({s['categorie']}, {s['date'] or 'n.d.'}, {s['consultation']})" for s in e["sources"])
        L.append(f"| {e['ref']} | **{e['statut']}** | « {e['formulation_voix_off']} » | {src} | {e['attribution']} | {e['limites']} |")
    L += ["", "## Faits retirés, corrigés ou incertains", "", "| Réf. | Statut v2 | Objet | Motif |", "|---|---|---|---|"]
    for e in reg["faits"]:
        if not e["utilise_v2"]:
            L.append(f"| {e['ref']} | **{e['statut']}** | {e['formulation_v1_ou_objet']} | {e['motif']} |")
    counts = {s: sum(1 for e in reg["faits"] if e["statut"] == s) for s in STATUSES}
    L += ["", "## Bilan", "", " · ".join(f"{k} : {v}" for k, v in counts.items()), ""]
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(ROOT / "var/lukoji.sqlite3"))
    ap.add_argument("--out", default=str(ROOT / "docs/stories/STO-20261127-001/v2"))
    a = ap.parse_args()
    reg = build(Path(a.db))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "registre_factuel.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "registre_factuel.md").write_text(to_markdown(reg), encoding="utf-8")
    print(f"registre : {len(reg['faits'])} faits → {out}")
