"""Capture de sources par le moteur (dans un environnement dont le réseau autorise les hôtes).

Usage : python3 scripts/capture_sources.py urls.txt research/captures [--extraits-seulement] [--motifs "regex1|regex2"]

--extraits-seulement : AUCUN texte intégral n'est conservé (droit d'auteur). Le manifeste garde l'empreinte
SHA-256 du texte complet et une liste limitée de phrases exactes (≤ 60 par page, ≤ 400 caractères) qui
contiennent un chiffre ou un des motifs. Les citations sont ensuite vérifiées contre ces phrases.
Pour chaque URL : récupération par le moteur (src.fetch), texte enregistré dans <dossier>/<sha16>.txt,
et une entrée dans <dossier>/captures.json : url normalisée, statut HTTP, disponibilité, titre, date
de publication détectée, date de capture, SHA-256 du texte. Aucun texte n'est modifié ni résumé.
L'import d'un dossier (`recherche importer --captures <dossier>`) revérifie ensuite chaque extrait
contre ces textes, et contrôle leur empreinte.
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lukoji_engine import sources as src  # noqa: E402
from lukoji_engine.db import now  # noqa: E402
from lukoji_engine.paths import resolve  # noqa: E402


import re

MAX_EXTRAITS, MAX_CARS = 60, 400


def candidate_sentences(text: str, motifs: str | None) -> list[str]:
    pat = re.compile(r"\d" + (f"|{motifs}" if motifs else ""), re.I)
    out, seen = [], set()
    for sent in re.split(r"(?<=[.!?»])\s+|\n+", text):
        sent = sent.strip()
        if 25 <= len(sent) <= MAX_CARS and pat.search(sent) and sent not in seen:
            seen.add(sent)
            out.append(sent)
        if len(out) >= MAX_EXTRAITS:
            break
    return out


def main(urls_file: str, out_dir: str, extraits_seulement: bool = False, motifs: str | None = None) -> int:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "captures.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    urls = [u.strip() for u in Path(urls_file).read_text().splitlines() if u.strip() and not u.startswith("#")]
    ok = 0
    for u in urls:
        if src.validate_url(u):
            print(f"URL refusée : {u} {src.validate_url(u)}")
            continue
        url = src.normalize_url(u)
        r = src.fetch(url)
        entry = {"url": url, "captured_at": now(), "availability": r.availability, "http_status": r.http_status,
                 "error": r.error, "final_url": r.final_url, "title": r.title, "site_name": r.site_name,
                 "published_at": r.published_at}
        if r.ok and extraits_seulement:
            entry.update(text_sha256=r.content_sha256, text_chars=len(r.text),
                         extraits=candidate_sentences(r.text, motifs),
                         extraits_regle=f"phrases exactes contenant un chiffre ou /{motifs or ''}/ ; ≤ {MAX_EXTRAITS} × {MAX_CARS} car.")
            resolve(r.text_path).unlink(missing_ok=True)   # aucun texte intégral conservé
            ok += 1
        elif r.ok:
            name = f"{r.content_sha256[:16]}.txt"
            shutil.copyfile(resolve(r.text_path), out / name)
            entry.update(text_file=name, text_sha256=r.content_sha256)
            ok += 1
        manifest[url] = entry
        print(f"{r.availability:26s} {r.http_status or '-':>4} {url}")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"{ok}/{len(urls)} page(s) capturée(s) -> {manifest_path}")
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("urls_file"); ap.add_argument("out_dir")
    ap.add_argument("--extraits-seulement", action="store_true"); ap.add_argument("--motifs")
    a = ap.parse_args()
    raise SystemExit(main(a.urls_file, a.out_dir, a.extraits_seulement, a.motifs))
