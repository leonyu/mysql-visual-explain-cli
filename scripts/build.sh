#!/bin/bash

set -e

git clean -dfx
mkdir -p dist
python3 -m zipapp -c mysql_visual_explain_cli -o ./dist/mysql_visual_explain_cli.pyz
7z l ./dist/mysql_visual_explain_cli.pyz
