#!/usr/bin/env bash
# Mirror Lunar Eclipse Maestro help documentation locally (French edition).
# Source: http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MIRROR_DIR="$ROOT/mirror"
BASE_URL="http://xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help"
ENTRY="$BASE_URL/LunarEclipseMaestroHelp.html"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

mkdir -p "$MIRROR_DIR"

echo "Mirroring LEM help from $ENTRY ..."
# wget exit 8 = some URLs returned 4xx/5xx (broken gfx in the help). Pages are still usable.
set +e
wget --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --wait=0.2 \
  --user-agent="$UA" \
  -P "$MIRROR_DIR/" \
  "$ENTRY"
WGET_STATUS=$?
set -e
if [[ "$WGET_STATUS" -ne 0 && "$WGET_STATUS" -ne 8 ]]; then
  echo "wget failed with status $WGET_STATUS" >&2
  exit "$WGET_STATUS"
fi
if [[ "$WGET_STATUS" -eq 8 ]]; then
  echo "Warning: wget reported missing assets (HTTP 4xx/5xx). Continuing with downloaded pages."
fi

HELP_ROOT="$MIRROR_DIR/xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help"

if [[ ! -d "$HELP_ROOT" ]]; then
  echo "Error: expected help root not found at $HELP_ROOT" >&2
  exit 1
fi

HTML_COUNT="$(find "$HELP_ROOT" -name '*.html' | wc -l)"
FILE_COUNT="$(find "$HELP_ROOT" -type f | wc -l)"

cat > "$MIRROR_DIR/MANIFEST.txt" <<EOF
Lunar Eclipse Maestro — local mirror manifest
Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
Source: $BASE_URL/
Entry point: LunarEclipseMaestroHelp.html

Statistics:
  HTML pages: $HTML_COUNT
  Total files: $FILE_COUNT

Local help root:
  $HELP_ROOT

Pages:
EOF

find "$HELP_ROOT" -name '*.html' -printf '  %P\n' | sort >> "$MIRROR_DIR/MANIFEST.txt"

cat > "$MIRROR_DIR/index.html" <<'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html">
  <title>Aide Lunar Eclipse Maestro — miroir local</title>
</head>
<body>
  <p>Redirection vers le <a href="xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help/pgs2/btoc1.html">sommaire de l'aide LEM</a>.</p>
</body>
</html>
EOF

echo "Done. $HTML_COUNT HTML pages mirrored."
echo "Open: file://$MIRROR_DIR/index.html"
