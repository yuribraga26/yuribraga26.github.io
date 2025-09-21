#!/usr/bin/env bash
set -euo pipefail

# Backup key static export artifacts to backups/<timestamp>/
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TS=$(date -u +"%Y%m%dT%H%M%SZ")
OUT_DIR="$ROOT_DIR/backups/$TS"

mkdir -p "$OUT_DIR"

echo "Backing up static export to $OUT_DIR"

# Copy root-level HTML files
for f in "$ROOT_DIR"/*.html; do
  [ -e "$f" ] || continue
  cp -a "$f" "$OUT_DIR/"
done

# Copy top-level route index.html files
for d in "$ROOT_DIR"/*/; do
  [ -d "$d" ] || continue
  if [ -e "$d/index.html" ]; then
    mkdir -p "$OUT_DIR/$(basename "$d")"
    cp -a "$d/index.html" "$OUT_DIR/$(basename "$d")/"
  fi
done

# Copy _next, images, and CNAME if present
for p in _next images CNAME; do
  if [ -e "$ROOT_DIR/$p" ]; then
    cp -a "$ROOT_DIR/$p" "$OUT_DIR/"
  fi
done

echo "Backup completed: $OUT_DIR"