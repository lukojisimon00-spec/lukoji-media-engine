"""Exports complémentaires v2 (production) : storyboard avec ressources, statuts et faisabilité ; registre des visuels.

Le schéma d'export du moteur (lukoji.storyboard/1.0) ne porte pas ces champs propres à la révision v2 ;
ils sont donc exportés à part, sans modifier le moteur.

Usage : python3 research/stories/mpesa/v2/export_v2_extra.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[3] / "docs/stories/STO-20261127-001/v2"
SB = json.loads((HERE / "storyboard_v2.json").read_text(encoding="utf-8"))
RES = json.loads((HERE / "ressources_visuelles_v2.json").read_text(encoding="utf-8"))
EXP = {s["id"]: s for s in json.loads((OUT / "storyboard.json").read_text(encoding="utf-8"))["scenes"]}


def storyboard_md() -> str:
    L = ["# Storyboard v2 — fiche de production", "",
         "Complément de `storyboard.md` (export du moteur) : intention, ressource, statut réel de la ressource, faisabilité et risques. "
         "Statuts : **metadonnees_verifiees** (fichier identifié, contenu visuel à contrôler) · **a_capturer** (page publique, capture à faire) · "
         "**a_produire** (création LUKOJI) · **non_obtenue** (substitut prévu).", ""]
    seq = None
    for sc in SB["scenes"]:
        if sc["sequence"] != seq:
            seq = sc["sequence"]
            L += [f"## {seq}", ""]
        e = EXP.get(sc["id"], {})
        res = ", ".join(f"{r} ({next(x['statut'] for x in RES['ressources'] if x['id'] == r)})" for r in sc["ressources"])
        L += [f"### {sc['id']} · {e.get('debut_s', '?')}–{e.get('fin_s', '?')} s · {sc['type_visuel']} · {sc['authenticite']}"
              + (f" · mention « {sc['mention_ecran']} »" if sc.get("mention_ecran") else ""), "",
              f"- **Voix off** : {sc['voix_off']}",
              f"- **Intention** : {sc['intention']}",
              f"- **Visuel** : {sc['description']}",
              f"- **Composition / cadrage** : {sc['composition']} · {sc['cadrage']}",
              f"- **Mouvement** : caméra {sc['mouvement_camera']} · graphique : {sc['mouvement_graphique']}",
              f"- **Texte à l'écran** : {' / '.join(sc['texte_ecran']) or '—'}",
              f"- **Ressource** : {res}",
              f"- **Son** : {sc['ambiance']}" + (f" · effets : {', '.join(sc['effets_sonores'])}" if sc["effets_sonores"] else ""),
              f"- **Transition** : {sc['transition']}",
              f"- **Montage** : {sc['instructions_montage']}",
              f"- **Faisabilité** : {sc['faisabilite']}",
              f"- **Risques de représentation** : {sc['risques_representation']}", ""]
    return "\n".join(L)


def ressources_md() -> str:
    L = ["# Ressources visuelles — version 2", "", RES["methode"], "",
         "| ID | Statut | Description | Auteur | Date | Licence | URL directe | Usage | Limites |", "|---|---|---|---|---|---|---|---|---|"]
    for r in RES["ressources"]:
        L.append(f"| {r['id']} | **{r['statut']}** | {r['description']} | {r.get('auteur', '—')} | {r.get('date', '—')} | "
                 f"{r.get('licence', '—')} | {r.get('url_directe', '—')} | {r.get('usage', '—')} | {r.get('limites', '')} |")
    L += ["", "## Fichiers examinés et écartés", "", "| Fichier | Auteur | Licence | Raison |", "|---|---|---|---|"]
    for r in RES["exclues"]:
        L.append(f"| {r['fichier']} | {r['auteur']} | {r['licence']} | {r['raison']} |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    (OUT / "storyboard_production.md").write_text(storyboard_md(), encoding="utf-8")
    (OUT / "ressources_visuelles.md").write_text(ressources_md(), encoding="utf-8")
    (OUT / "ressources_visuelles.json").write_text(json.dumps(RES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"exports complémentaires → {OUT}")
