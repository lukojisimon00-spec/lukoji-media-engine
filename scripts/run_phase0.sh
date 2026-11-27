#!/usr/bin/env bash
# LUKOJI MEDIA ENGINE — reproduction complète de la validation de la phase 0.
# Usage : ./scripts/run_phase0.sh            (tout)
#         SKIP_TESTS=1 ./scripts/run_phase0.sh (sans pytest)
# Sources de test (lecture seule, jamais modifiées) — surchargeables :
#   SRC_VERTICAL   : réel 1080x1920 (défaut : ../lukoji-blog/pubs/reseaux/2026-11-20-reel-ta-premiere-pub.mp4)
#   SRC_HORIZONTAL : vidéo 1920x1080 (défaut : ../Motion-design-/time-capital/renders/le-temps-est-ton-capital.mp4)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
L=./bin/lukoji
V="docs/validation"
SRC_VERTICAL="${SRC_VERTICAL:-$ROOT/../lukoji-blog/pubs/reseaux/2026-11-20-reel-ta-premiere-pub.mp4}"
SRC_HORIZONTAL="${SRC_HORIZONTAL:-$ROOT/../Motion-design-/time-capital/renders/le-temps-est-ton-capital.mp4}"

echo "== 1. Outils"
for t in ffmpeg ffprobe python3 node; do command -v "$t" >/dev/null || { echo "MANQUANT : $t"; exit 1; }; done
ENCODERS="$(ffmpeg -hide_banner -encoders 2>/dev/null)"; [[ "$ENCODERS" == *libx264* ]] || { echo "FFmpeg sans libx264"; exit 1; }
python3 -c "import PIL, numpy" || { echo "Pillow/numpy manquants"; exit 1; }
node -e "require('playwright')" || { echo "Playwright (Chromium) introuvable"; exit 1; }

echo "== 2. Base + kit de marque"
$L db-init
$L brand-build
$L brand-verify
$L profiles
$L social

mkdir -p "$V/renders"
if [ -f "$SRC_VERTICAL" ]; then
  echo "== 3. Test réel vertical 1080x1920 (source coupée avant sa propre signature)"
  $L watermark "$SRC_VERTICAL" var/out/test_vertical_1080x1920.mp4 --profile vertical_universal \
     --kind test --signature court --source-out 19.35 --slug test-phase0-vertical --title "Phase 0 — test vertical"
  $L qc var/out/test_vertical_1080x1920.mp4 --json "$V/qc_test_vertical.json"
  $L sheet var/out/test_vertical_1080x1920.mp4 "$V/planche_test_vertical.png" --times 1.5,6,12,18.5,19.9,20.6
  cp var/out/test_vertical_1080x1920.mp4 var/out/test_vertical_1080x1920.mp4.json "$V/renders/"
else
  echo "!! source verticale absente : $SRC_VERTICAL (test ignoré)"
fi
if [ -f "$SRC_HORIZONTAL" ]; then
  echo "== 4. Test réel horizontal 1920x1080 (signature documentaire)"
  $L watermark "$SRC_HORIZONTAL" var/out/test_horizontal_1920x1080.mp4 --profile youtube_16x9 \
     --kind documentaire --slug test-phase0-horizontal --title "Phase 0 — test 16:9"
  $L qc var/out/test_horizontal_1920x1080.mp4 --json "$V/qc_test_horizontal.json"
  $L sheet var/out/test_horizontal_1920x1080.mp4 "$V/planche_test_horizontal.png" --times 3,7,12,18,20.5,22.5
  cp var/out/test_horizontal_1920x1080.mp4 var/out/test_horizontal_1920x1080.mp4.json "$V/renders/"
else
  echo "!! source horizontale absente : $SRC_HORIZONTAL (test ignoré)"
fi

if [ "${SKIP_TESTS:-0}" != "1" ]; then
  echo "== 5. Tests automatisés"
  python3 -m pytest -q
fi
echo "== Phase 0 : validation terminée"
