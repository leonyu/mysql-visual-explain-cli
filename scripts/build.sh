#!/bin/sh

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
DIST_DIR=$(readlink -f "$SCRIPT_DIR"/../dist)
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
python3 -m zipapp "$SCRIPT_DIR"/../src -o "$DIST_DIR"/mysql_visual_explain_cli.pyz -p '/usr/bin/env python3' -m mysql_visual_explain_cli.main:main -c
unzip -l "$DIST_DIR"/mysql_visual_explain_cli.pyz
python3 "$DIST_DIR"/mysql_visual_explain_cli.pyz || true
