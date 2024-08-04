#!/bin/sh

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

curl https://raw.githubusercontent.com/mysql/mysql-workbench/8.0/plugins/wb.query.analysis/explain_renderer.py -o "$SCRIPT_DIR"/../mysql_visual_explain_cli/query_analysis/explain_renderer.py
curl https://raw.githubusercontent.com/mysql/mysql-workbench/8.0/library/python/workbench/graphics/cairo_utils.py -o "$SCRIPT_DIR"/../mysql_visual_explain_cli/graphics/cairo_utils.py
curl https://raw.githubusercontent.com/mysql/mysql-workbench/8.0/library/python/workbench/graphics/canvas.py -o "$SCRIPT_DIR"/../mysql_visual_explain_cli/graphics/canvas.py
git apply "$SCRIPT_DIR"/../patches/fetch.patch
