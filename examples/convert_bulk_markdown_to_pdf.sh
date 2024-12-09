#!/bin/bash
set -e

# quita los margenes ya que el documento padre añadirá los suyos. En inferior no es 0 para no eleminar el page number
TEMPLATE_OPTS='-V geometry:bottom=1.5cm,left=0cm,top=0cm,right=0cm'

# this document will be probally printed. So cliclable links are useless
TEMPLATE_OPTS+=' -V links-as-notes=true'

for file in $(find  $1  -name '*.md' | sort); do
    pushd $(dirname $file)
    pandoc $(basename $file) ${TEMPLATE_OPTS[@]}  --from=gfm -o $(basename --suffix=.md $file).pdf
    rm $(basename $file)
    popd
done
# TODO: markdown lua plugin to decrease margin?
