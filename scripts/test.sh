#!/bin/bash

set -e

for f in ./fixtures/*.json; do
    echo "Testing conversion of $f to PNG and SVG"
    output_basename="$(basename $f .json)"
    python3 ./dist/mysql_visual_explain_cli.pyz "$f" "/tmp/$output_basename.png"
    python3 ./dist/mysql_visual_explain_cli.pyz "$f" "/tmp/$output_basename.svg"
done
ls -l /tmp/*.svg
