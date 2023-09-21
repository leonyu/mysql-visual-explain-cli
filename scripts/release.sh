#!/bin/bash

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

source "$SCRIPT_DIR/build.sh"
source "$SCRIPT_DIR/test.sh"
gh release create --generate-notes "$(date +%Y.%m.%d)" ./dist/mysql_visual_explain_cli.pyz
