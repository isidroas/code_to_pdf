#!/bin/bash
set -e
for file in $(find  $1  -name '*.md' | sort); do
    pushd $(dirname $file)
    pandoc $(basename $file) -V geometry:bottom=1.5cm,left=0cm,top=0cm,right=0cm -V links-as-notes=true --from=gfm -o $(basename --suffix=.md $file).pdf
    rm $(basename $file)
    popd
done
# TODO: markdown lua plugin to decrease margin?
