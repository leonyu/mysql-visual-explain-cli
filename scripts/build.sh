#!/bin/sh

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
DIST_DIR="$SCRIPT_DIR"/../dist
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
py3clean mysql_visual_explain_cli/
python3 -m zipapp -c "$SCRIPT_DIR"/../mysql_visual_explain_cli -p '/usr/bin/env python3' -o "$DIST_DIR"/mysql_visual_explain_cli.pyz
unzip -l "$DIST_DIR"/mysql_visual_explain_cli.pyz
