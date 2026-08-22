#!/usr/bin/env bash
# Build consolidated printable HTML and PDF from the local LEM mirror.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"

if [[ ! -d "$ROOT/mirror/xjubier.free.fr/site_pages/lunar_eclipses/Lunar_Eclipse_Maestro_Help" ]]; then
  echo "Mirror not found. Run scripts/mirror.sh first." >&2
  exit 1
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "Creating Python venv and installing dependencies..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r "$ROOT/requirements.txt"
fi

exec "$VENV/bin/python" "$ROOT/scripts/build-pdf.py"
