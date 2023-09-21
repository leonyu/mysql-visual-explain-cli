#!/bin/bash

set -e

for f in ./fixtures/*.json; do
    json_basename="$(basename $f)"
    png_filename="${json_basename/json/png}"
    echo "Converting $json_basename to $png_filename"
    python3 ./dist/mysql_visual_explain_cli.pyz "$f" "/tmp/$png_filename"
done
ls -l /tmp/*.png
