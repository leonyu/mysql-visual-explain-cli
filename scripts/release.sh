#!/bin/sh

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

"$SCRIPT_DIR"/build.sh
poetry install
poetry run pytest
gh release create --generate-notes "v$(date +%Y.%m.%d)" "$SCRIPT_DIR"/../dist/mysql_visual_explain_cli.pyz
