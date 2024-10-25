#!/bin/sh

code_to_pdf $1 > out.tex

xelatex -shell-escape out.tex
xelatex -shell-escape out.tex
