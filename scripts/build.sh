#!/bin/bash

set -e

if command -v git; then
    git clean -dfx
fi
mkdir -p dist
python3 -m zipapp -c mysql_visual_explain_cli -p '/usr/bin/env python3' -o ./dist/mysql_visual_explain_cli.pyz
unzip -l ./dist/mysql_visual_explain_cli.pyz
