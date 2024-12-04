# TODO: sed remove or reduce copyright
.DELETE_ON_ERROR:
SHELL=bash

all: TheAlgorithms-Python-hash.pdf acwj_chapters_1-2.pdf


%.d: %.tar.gz
	mkdir -p $@
	tar --strip-components=1 --directory=$@ -xvf $^

# TODO: download and install fonts
CODE2TEX=code_to_pdf --monofont "SauceCodePro Nerd Font Mono" --mainfont "SauceCodePro Nerd Font"
# CODE2TEX=code_to_pdf --monofont "Hack Nerd Font Mono" --mainfont "Hack Nerd Font"
%.tex: %.d
	$(CODE2TEX)  $^ > $@

TEX=xelatex -shell-escape
%.pdf: %.tex
	$(TEX) $^
	$(TEX) $^

TheAlgorithms-Python.tar.gz:
# the project does not have releases, but using some random commit to have an stable output
	curl -L https://github.com/TheAlgorithms/Python/tarball/fc33c505935e9927cffb6142591891f721a7bcd9 > $@

TheAlgorithms-Python-hash.tex: TheAlgorithms-Python.d
	$(CODE2TEX)  $^/data_structures/hashing --title 'TheAlgorithms/data_structures/hashing' > $@

# TODO: st.1 -> man page to pdf
simple-terminal.tar.gz:
	curl -L https://dl.suckless.org/st/st-0.9.2.tar.gz > $@


#### build your own-x

# aqui haría falta ordenar 00,01..
# es todo codigo :)
mini-arm-os.tar.gz:
	curl -L https://github.com/jserv/mini-arm-os/tarball/master > $@

# ! Dimension too large. TODO: ir añadiendo capitulos hasta que lo pille?
# tiene tanto codigo markdowns bajo la carpteta docs
raspberry-pi-os.tar.gz:
	curl -L https://github.com/s-matyukevich/raspberry-pi-os/tarball/master > $@

# ! Dimension too large. First 
acwj.tar.gz:
	curl -L https://github.com/DoctorWkt/acwj/tarball/master > $@
# TODO: include main README.md? overlapping with TOC?
acwj_chapters_1-2.d: acwj.d
	mkdir $@
	cp -R $^/0{0,1,2}_*/ $@
	./convert_bulk_markdown_to_pdf.sh $@
	find $@ -name '*.png' | xargs rm
acwj_chapters_1-2.tex: acwj_chapters_1-2.d
	$(CODE2TEX)  $^ --title 'A Compiler Writing Journey - Chapters 0-2' > $@

# es casi todo un conjunto de readmes
write-a-hash-table.tar.gz:
	curl -L https://github.com/jamesroutley/write-a-hash-table/tarball/master > $@

# es casi todo un conjunto de readmes
db_tutorial.tar.gz:
	curl -L https://github.com/cstack/db_tutorial/tarball/master > $@



clean: clean-latex-artifacts
	rm -rf *.tex *.pdf
	rm -rf *.d

# TODO: dirs are not cleaned
clean-latex-artifacts:
	rm -rf _minted-* *.aux *.log *.out

clean-sources:
	rm *.tar.gz
