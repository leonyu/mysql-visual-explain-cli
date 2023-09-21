#!/bin/bash

set -e

if command -v git; then
    git clean -dfx
fi
mkdir -p dist
python3 -m zipapp -c mysql_visual_explain_cli -o ./dist/mysql_visual_explain_cli.pyz
7z l ./dist/mysql_visual_explain_cli.pyz
