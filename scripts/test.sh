#!/bin/sh

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
TMP_DIR=/tmp/mysql-visual-explain-cli
mkdir -p "$TMP_DIR"
for f in "$SCRIPT_DIR"/../fixtures/*.json; do
    echo "Testing conversion of $f to PNG and SVG"
    output_basename="$(basename "$f" .json)"
    python3 "$SCRIPT_DIR"/../dist/mysql_visual_explain_cli.pyz "$f" "$TMP_DIR/$output_basename.png"
    python3 "$SCRIPT_DIR"/../dist/mysql_visual_explain_cli.pyz "$f" "$TMP_DIR/$output_basename.svg"
done
ls -l "$TMP_DIR"
