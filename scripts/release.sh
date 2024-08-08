#!/bin/sh

set -e

check_uncommitted () {
    git update-index --refresh
    if ! git diff-index --quiet HEAD --; then
        echo 'Abort, there are uncommited files...'
        exit 1
    fi
}

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

check_uncommitted

py3clean "$SCRIPT_DIR"/../src
"$SCRIPT_DIR"/fetch.sh

check_uncommitted

"$SCRIPT_DIR"/build.sh
poetry install
poetry run pytest

check_uncommitted

gh release create --generate-notes "v$(date +%Y.%m.%d)" "$SCRIPT_DIR"/../dist/mysql_visual_explain_cli.pyz
