#!/usr/bin/bash
set -xue -o pipefail

walkfind --also-dirs \
	--exclude-file '*.pdf' \
	--exclude-file '.coverage' \
	--exclude-file 'output.html' \
	--exclude-file 'LICENSE' \
	--exclude-file '*.svg' \
	--exclude-dir "venv" \
	--exclude-dir "build" \
	--exclude-dir ".git" \
	--exclude-dir "*.egg-info" \
	--exclude-dir "HTML" \
	--exclude-dir "docs" \
	--sort files_first \
	--sort alpha \
	--no-binary \
	$1 | code_to_pdf >out.tex

xelatex -shell-escape out.tex
xelatex -shell-escape out.tex
