#!/bin/bash
for file in $(find  $1  -name '*.md' | sort); do
    pushd $(dirname $file)
    pandoc $(basename $file) -o $(basename --suffix=.md $file).pdf
    rm $(basename $file)
    popd
done
# TODO: markdown lua plugin to decrease margin?
