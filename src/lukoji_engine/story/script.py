"""SCRIPT ENGINE : script documentaire séquence par séquence, relié aux faits et aux sources.

L'auteur écrit la voix off intégrale ; le moteur calcule mots et durées, rattache les références des sources
à partir des faits cités, applique le contrôle factuel et les contrôles d'écriture (phrases trop longues,
répétitions, formules creuses, transitions génériques), et vérifie la cohérence avec la structure et le hook.
"""
from __future__ import annotations

from .factcheck import check_passage
from .hooks import chosen_hook
from .text import find_cliches, long_sentences, norm, repetitions, speech_seconds, story_config, word_count

GENERIC_TRANSITIONS = ["passons maintenant", "voyons maintenant", "dans cette partie", "comme nous l'avons vu",
                       "maintenant, parlons", "dans un premier temps", "dans un second temps", "pour commencer,",
                       "abordons", "intéressons-nous"]
FIELDS = ("id", "etape", "titre", "voix_off", "objectif", "emotion")


def sources_of(refs: list[str], facts: dict) -> list[str]:
    out = []
    for r in refs:
        for p in (facts.get(r) or {}).get("preuves", []):
            if p["source"] not in out:
                out.append(p["source"])
    return out


def full_text(doc: dict) -> str:
    return "\n\n".join(s.get("voix_off", "") for s in doc.get("sequences", []))


def evaluate(doc: dict, facts: dict, structure: dict, hooks: dict, fmt: str) -> dict:
    cfg = story_config()
    ry, ec = cfg["rythme"], cfg["ecriture"]
    p: list[dict] = []
    seqs = doc.get("sequences") or []
    step_ids = {s.get("id") for s in structure.get("etapes", [])}
    computed = []
    for i, s in enumerate(seqs):
        where = f"séquence {s.get('id')}"
        sp: list[dict] = []
        for f in FIELDS:
            if not str(s.get(f) or "").strip():
                sp.append({"severite": "bloquant", "code": "champ_manquant", "message": f"champ « {f} » manquant", "ou": where})
        if i < len(seqs) - 1 and not str(s.get("transition") or "").strip():
            sp.append({"severite": "alerte", "code": "transition_manquante", "message": "transition vers la suite non décrite", "ou": where})
        if s.get("etape") not in step_ids:
            sp.append({"severite": "bloquant", "code": "etape_inconnue", "message": f"étape {s.get('etape')!r} absente de la structure", "ou": where})
        vo = s.get("voix_off", "")
        sp += check_passage(vo, s.get("faits") or [], facts, where)
        for n, sent in long_sentences(vo, ry["phrase_max_mots"]):
            sp.append({"severite": "alerte", "code": "phrase_longue", "message": f"{n} mots : « {sent[:80]}… »", "ou": where})
        cl = find_cliches(vo, ec["cliches"])
        if cl:
            sp.append({"severite": "alerte", "code": "cliche", "message": f"formules creuses : {', '.join(cl)}", "ou": where})
        gt = [g for g in GENERIC_TRANSITIONS if norm(g) in norm(vo)]
        if gt:
            sp.append({"severite": "alerte", "code": "transition_generique", "message": f"transition générique : {', '.join(gt)}", "ou": where})
        computed.append({"id": s.get("id"), "etape": s.get("etape"), "titre": s.get("titre"), "mots": word_count(vo),
                         "duree_s": speech_seconds(vo), "faits": s.get("faits") or [],
                         "sources": sources_of(s.get("faits") or [], facts), "problemes": sp})
        p += sp
    ids = [s.get("id") for s in seqs]
    if len(set(ids)) != len(ids):
        p.append({"severite": "bloquant", "code": "id_double", "message": "identifiants de séquences en double", "ou": "script"})
    hook = chosen_hook(hooks)
    if hook and seqs and not norm(seqs[0].get("voix_off", "")).startswith(norm(hook["voix_off"])[:60]):
        p.append({"severite": "bloquant", "code": "hook_absent", "message": f"la séquence 1 ne reprend pas le hook choisi ({hook['id']})", "ou": "script"})
    text = full_text(doc)
    reps = repetitions(text, ec["repetition_fenetre_mots"], ec["repetition_seuil"])
    reps = [(w, n) for w, n in reps if w not in {"mpesa", "m-pesa", "pesa", "argent", "kenya"}]
    for w, n in reps[:8]:
        p.append({"severite": "alerte", "code": "repetition", "message": f"« {w} » répété {n} fois dans une fenêtre de {ec['repetition_fenetre_mots']} mots", "ou": "script"})
    total = round(sum(c["duree_s"] for c in computed) + ry["pause_entre_sequences_s"] * max(0, len(seqs) - 1), 1)
    f = cfg["formats"][fmt]
    if not f["duree_min_s"] <= total <= f["duree_max_s"]:
        p.append({"severite": "bloquant", "code": "duree_hors_format", "message": f"durée estimée {total} s hors format {f['duree_min_s']}–{f['duree_max_s']} s", "ou": "script"})
    used_steps = {s.get("etape") for s in seqs}
    unused = [sid for sid in step_ids if sid not in used_steps]
    if unused:
        p.append({"severite": "alerte", "code": "etapes_non_couvertes", "message": f"étapes de la structure sans séquence : {', '.join(sorted(unused))}", "ou": "script"})
    return {"sequences": computed, "mots": sum(c["mots"] for c in computed), "duree_s": total,
            "debit_mpm": ry["mots_par_minute"], "repetitions": reps[:8], "problemes": p}
