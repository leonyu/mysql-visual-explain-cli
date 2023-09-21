#!/bin/bash

set -e

for f in ./fixtures/*.json; do
    pngfile=/tmp/${f/.\/fixtures\//}.png
    python3 ./dist/mysql_visual_explain_cli.pyz "$f" "$pngfile"
done
ls -l /tmp/*.png
