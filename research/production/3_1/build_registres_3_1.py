"""Atelier 3.1 — registres de production des ressources du pilote M-Pesa (storyboard v10 verrouillé).

Lit, sans rien modifier : le verrou, le storyboard v10 (contrôlé par empreinte), le registre des ressources v2.6.2,
le manifeste de collecte (collecte/manifeste_collecte.json) et le manifeste des photos (photos/manifeste_photos.json).

Écrit dans research/production/3_1/registres/ :
- registre_ressources_production.json / .md   registre central, relié aux scènes
- pages_pertinentes.md                          pages et passages utiles par document
- credits_droits.md                             crédits exacts et état des droits
- etat_par_scene.md / etat_par_scene.json       état de préparation des 50 scènes

Usage : python3 research/production/3_1/build_registres_3_1.py   (code retour 1 si le verrou ou le storyboard échoue)
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOCK = ROOT / "docs/stories/STO-20261127-001/VERROU_VALIDATION.json"
SB = ROOT / "research/stories/mpesa/v2_6_2/storyboard_v2_6_2.json"
RES = ROOT / "research/stories/mpesa/v2_6_2/ressources_visuelles_v2_6_2.json"
COLL = HERE / "collecte/manifeste_collecte.json"
PHOTOS = HERE / "photos/manifeste_photos.json"
OUT = HERE / "registres"

# Ressources fabriquées par LUKOJI (pas de collecte) : ce qu'il faut produire, et dans quel atelier.
PRODUITES = {
    "R20": ("carte", "Fonds de carte Natural Earth (domaine public, à télécharger et reconfirmer en atelier de motion design)"),
    "R21": ("graphique", "Gabarits graphiques et typographiques LUKOJI (polices OFL déjà dans brand/fonts)"),
    "R22": ("illustration / insert", "Dessins au trait LUKOJI et inserts de reconstitution à tourner"),
}


def sha(o) -> str:
    return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def load():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    sb = json.loads(SB.read_text(encoding="utf-8"))
    v = {x["etape"]: x for x in lock["validations"]}
    if "storyboard" not in v or v["storyboard"]["versions"]["storyboard"]["version"] != 10:
        raise SystemExit("ARRÊT : aucune validation du storyboard v10 dans le verrou")
    if sha(sb) != v["storyboard"]["versions"]["storyboard"]["sha256"]:
        raise SystemExit("ARRÊT : le storyboard ne correspond pas à la version validée (empreinte)")
    res = {r["id"]: r for r in json.loads(RES.read_text(encoding="utf-8"))["ressources"]}
    coll = json.loads(COLL.read_text(encoding="utf-8")) if COLL.exists() else {}
    photos = json.loads(PHOTOS.read_text(encoding="utf-8")) if PHOTOS.exists() else {}
    return lock, sb, res, coll, photos


def coll_index(coll) -> dict:
    items = coll.get("documents") or coll.get("entrees") or (coll if isinstance(coll, list) else [])
    if isinstance(items, dict):
        items = list(items.values())
    out = {}
    for e in items:
        rid = e.get("id") or e.get("ID")
        if rid:
            out[rid] = e
    return out


def main() -> int:
    lock, sb, res, coll, photos = load()
    ci = coll_index(coll)
    for p in (photos.get("photos") or []):
        ci.setdefault(p["id"], {}).update({"photo": p})
    scenes = sb["scenes"]
    used = {}
    for s in scenes:
        for r in s["ressources"]:
            used.setdefault(r, []).append(s["id"])
    registre = []
    for rid in sorted(set(res) | set(used), key=lambda x: int(x[1:])):
        r = res.get(rid, {})
        e = ci.get(rid, {})
        caps = e.get("captures") or []
        if rid in PRODUITES:
            prod = "a_produire_par_lukoji"
        elif rid not in used:
            prod = "non_utilise_v10"
        elif r.get("statut") == "non_obtenue":
            prod = "inaccessible_substitut_prevu"
        elif "photo" in e:
            prod = "photo_obtenue" if e["photo"].get("fichier_local") else "photo_a_telecharger"
        elif e.get("statut") == "obtenu" and caps:
            prod = "capture_obtenue"
        elif e.get("statut") == "partiel":
            prod = "capture_partielle"
        elif e:
            prod = "collecte_en_echec"
        else:
            prod = "a_collecter"
        registre.append({
            "id": rid, "description": r.get("description"), "scenes_v10": used.get(rid, []),
            "statut_registre_v2_6_2": r.get("statut"), "statut_production": prod,
            "url_source": e.get("url_finale") or e.get("url") or r.get("url_directe") or r.get("page"),
            "auteur": r.get("auteur"), "date": r.get("date"), "licence_registre": r.get("licence"),
            "licence_ou_conditions_trouvees": e.get("licence_ou_conditions") or e.get("licence") or (e.get("photo") or {}).get("LicenseShortName"),
            "sha256_original": e.get("sha256"), "taille_octets": e.get("taille") or e.get("taille_octets"), "pages": e.get("pages") or e.get("nb_pages"),
            "captures": caps, "limites": e.get("limites") or r.get("limites") or r.get("inspection"),
            "production": PRODUITES.get(rid, (None, None))[1],
        })
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "registre_ressources_production.json").write_text(json.dumps({
        "projet": "STO-20261127-001", "storyboard": 10, "storyboard_sha256": sha(sb),
        "verrou_statut": lock["statut_au_verrouillage"], "ressources": registre}, ensure_ascii=False, indent=1), encoding="utf-8")

    L = ["# Registre central des ressources de production — storyboard v10", "",
         f"Storyboard v10 (SHA-256 `{sha(sb)[:16]}…`, contrôlé contre le verrou) · statut du projet au verrou : `{lock['statut_au_verrouillage']}`", "",
         "| ID | Ressource | Scènes v10 | Statut de production | Source | Captures |", "|---|---|---|---|---|---|"]
    for e in registre:
        L.append(f"| {e['id']} | {e['description']} | {', '.join(e['scenes_v10']) or '—'} | **{e['statut_production']}** | "
                 f"{e['url_source'] or '—'} | {len(e['captures'])} |")
    (OUT / "registre_ressources_production.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    P = ["# Pages et passages pertinents par document", ""]
    for e in registre:
        if not e["captures"]:
            continue
        P += [f"## {e['id']} — {e['description']}", "", f"Source : {e['url_source']} · SHA-256 de l'original : `{e['sha256_original'] or '—'}` · pages : {e['pages'] or '—'}", "",
              "| Capture | Page / zone | Citation exacte | Scène |", "|---|---|---|---|"]
        for c in e["captures"]:
            P.append(f"| `{c.get('fichier')}` | {c.get('page') or c.get('zone') or '—'} | {c.get('citation') or '—'} | {c.get('scene') or '—'} |")
        P.append("")
    (OUT / "pages_pertinentes.md").write_text("\n".join(P), encoding="utf-8")

    C = ["# Crédits et droits", "", "Aucune licence n'est déclarée confirmée sans mention trouvée dans la source elle-même.", "",
         "## Photographies (licences libres Wikimedia Commons)", "", "| ID | Crédit à afficher | Licence | Preuve | Scènes | Fichier |", "|---|---|---|---|---|---|"]
    for e in registre:
        p = (ci.get(e["id"]) or {}).get("photo")
        if p:
            C.append(f"| {e['id']} | {p.get('credit_a_afficher', '—')} | {p.get('LicenseShortName', '—')} ({p.get('LicenseUrl', '—')}) | "
                     f"métadonnées Commons lues le {p.get('date_lecture', '—')} | {', '.join(e['scenes_v10'])} | {p.get('fichier_local') or 'à télécharger'} |")
    C += ["", "## Documents (captures d'extraits)", "", "| ID | Document | Conditions trouvées dans la source | État des droits | Scènes |", "|---|---|---|---|---|"]
    for e in registre:
        if e["captures"] or e["statut_production"] in ("collecte_en_echec", "a_collecter", "capture_partielle"):
            C.append(f"| {e['id']} | {e['description']} | {e['licence_ou_conditions_trouvees'] or 'aucune mention relevée'} | "
                     f"citation courte, droits **non confirmés** | {', '.join(e['scenes_v10'])} |")
    C += ["", "## Créations LUKOJI", "", "- Cartes (Natural Earth, domaine public à reconfirmer), graphiques, typographies (polices OFL), illustrations au trait, inserts de reconstitution : aucun droit de tiers."]
    (OUT / "credits_droits.md").write_text("\n".join(C) + "\n", encoding="utf-8")

    st_by = {e["id"]: e for e in registre}
    S, SJ = ["# État de préparation des ressources par scène — storyboard v10", "",
             "| Scène | Séq. | Type | Ressources | État | Remplacement prévu |", "|---|---|---|---|---|---|"], []
    for s in scenes:
        states = [st_by[r]["statut_production"] for r in s["ressources"]] or ["aucune_ressource (noir)"]
        if all(x in ("capture_obtenue", "photo_obtenue", "aucune_ressource (noir)") for x in states):
            etat = "prête (ressource obtenue)"
        elif all(x in ("capture_obtenue", "photo_obtenue", "a_produire_par_lukoji") for x in states):
            etat = "à produire par LUKOJI (ateliers suivants)" if "a_produire_par_lukoji" in states else "prête"
        elif any(x in ("collecte_en_echec", "a_collecter", "photo_a_telecharger", "capture_partielle") for x in states):
            etat = "en attente de ressource"
        else:
            etat = "substitut prévu"
        SJ.append({"scene": s["id"], "sequence": s["sequence"], "type": s["type_visuel"], "ressources": s["ressources"],
                   "etats": states, "etat": etat, "remplacement": s.get("plan_remplacement")})
        S.append(f"| {s['id']} | {s['sequence']} | {s['type_visuel']} | {', '.join(s['ressources']) or '—'} | {etat} | {s.get('plan_remplacement') or '—'} |")
    from collections import Counter
    cnt = Counter(x["etat"] for x in SJ)
    S += ["", "**Bilan** : " + " · ".join(f"{k} : {v}" for k, v in cnt.items())]
    (OUT / "etat_par_scene.md").write_text("\n".join(S) + "\n", encoding="utf-8")
    (OUT / "etat_par_scene.json").write_text(json.dumps(SJ, ensure_ascii=False, indent=1), encoding="utf-8")
    print("registres écrits ·", " · ".join(f"{k} : {v}" for k, v in cnt.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
