#!/bin/bash
set -e

# # TODO: completion bash
# # TODO: create debian package
# if [ $UID -ne 0 -a $EUID -ne 0 ]; then
#     echo run as sudo. $UID $EUID
#     exit 1
# fi


# PREFIX=/usr/local/share/fonts
PREFIX=/usr/share/fonts
# PREFIX=~/.local/share/fonts
for font in DejaVuSansMono  Hack  SourceCodePro FiraMono FiraCode; do

    if [ -d $PREFIX/$font ]; then
        continue
    fi

    curl -L https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/${font}.zip > /tmp/${font}.zip
    mkdir -p $PREFIX/$font
    unzip -o /tmp/${font}.zip -d $PREFIX/$font
done


sudo apt install tree
tree $PREFIX
fc-match  'SauceCodePro Nerd Font'
