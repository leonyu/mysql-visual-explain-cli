#!/bin/sh

python3 -m zipapp -c mysql_visual_explain_cli
gh release create --generate-notes "$(date +%Y.%m.%d)" ./mysql_visual_explain_cli.pyz
