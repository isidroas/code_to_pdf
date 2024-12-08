#!/bin/bash
set -e

PREFIX=~/.local/share/fonts
# other possible locations:
# PREFIX=/usr/local/share/fonts
# PREFIX=/usr/share/fonts

for font in DejaVuSansMono  Hack  SourceCodePro FiraMono FiraCode; do
    if [ -d $PREFIX/$font ]; then
        continue
    fi
    curl -L https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/${font}.zip > /tmp/${font}.zip
    mkdir -p $PREFIX/$font
    unzip -o /tmp/${font}.zip -d $PREFIX/$font
done

# fc-match  'SauceCodePro Nerd Font'
