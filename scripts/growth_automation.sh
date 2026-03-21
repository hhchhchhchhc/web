#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SITE_URL="${1:-https://ai-tool.indevs.in}"

echo "[growth] run migrate"
python manage.py migrate --noinput

echo "[growth] generate topic pages"
python manage.py generate_topic_pages

echo "[growth] submit sitemap"
SUBMIT_ARGS=(--site "$SITE_URL")
if [[ -n "${INDEXNOW_KEY:-}" ]]; then
  SUBMIT_ARGS+=(--indexnow-key "$INDEXNOW_KEY")
fi
if [[ -n "${INDEXNOW_KEY_LOCATION:-}" ]]; then
  SUBMIT_ARGS+=(--key-location "$INDEXNOW_KEY_LOCATION")
fi
python manage.py submit_sitemap "${SUBMIT_ARGS[@]}"

echo "[growth] done"
