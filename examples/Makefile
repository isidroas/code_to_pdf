# TODO: sed remove or reduce copyright
.DELETE_ON_ERROR:
SHELL=bash

# all: TheAlgorithms-Python-hash.pdf acwj_chapters_1-2.pdf flask_without_docs.pdf
all: TheAlgorithms-Python.pdf acwj_chapters_1-2.pdf flask_without_docs.pdf


%.d: %.tar.gz
	mkdir -p $@
	tar --strip-components=1 --directory=$@ -xvf $^
# en realidad hay unos mods comunes para todos:
# - eliminar empty
# - eliminar binary: find -type f | ./filter_binary.sh | xargs rm
# esos los puedo meter aquí incondicionalmente

# some fonts that can be downloaded from https://www.nerdfonts.com/
# REPO2TEX_FLAGS?=--monofont "SauceCodePro Nerd Font Mono" --mainfont "SauceCodePro Nerd Font"
# REPO2TEX_FLAGS?=--monofont "Hack Nerd Font Mono" --mainfont "Hack Nerd Font"
# TODO: remove SUBDIR and crate *_mod.d alterantivelly?
%.tex: %.d
	code_to_pdf $(REPO2TEX_FLAGS) --title "$(TITLE)" $^/$(SUBDIR) > $@

TEX2PDF?=xelatex
%.pdf: %.tex
	$(TEX2PDF)  -shell-escape $^
	$(TEX2PDF)  -shell-escape $^

TheAlgorithms-Python.tar.gz:
# the project does not have releases, but using some random commit to have an stable output
	curl -L https://github.com/TheAlgorithms/Python/tarball/fc33c505935e9927cffb6142591891f721a7bcd9 > $@

# TODO: find -empty -rm . Primero para ficheros y luego para dirs.
TheAlgorithms-Python.tex: TITLE = TheAlgorithms/data_structures/hashing
TheAlgorithms-Python.tex: SUBDIR = data_structures/hashing
# TheAlgorithms-Python-hash.tex: TheAlgorithms-Python.d
# $(CODE2TEX)  $^/data_structures/hashing --title 'TheAlgorithms/data_structures/hashing' > $@

# TODO: st.1 -> man page to pdf
simple-terminal.tar.gz:
	curl -L https://dl.suckless.org/st/st-0.9.2.tar.gz > $@
simple-terminal.tex: TITLE = suckless/st

flask.tar.gz:
	curl -L https://github.com/pallets/flask/tarball/3.1.0 > $@

flask_without_docs.d: flask.d
# sphinx can create better pdfs. TODO: embed pdf
	cp -R $^ $@
	rm -r $@/docs

# flask_without_docs.tex: flask_without_docs.d
# 	$(CODE2TEX)  $^ --title 'Flask' > $@
flask_without_docs.tex: TITLE = Flask

# proyecto pequeño pero que contiene varios archivos
heap_allocator.tar.gz:
	curl -L https://github.com/CCareaga/heap_allocator/tarball/master > $@

heap_allocator_reduced.d: heap_allocator.d
	cp -R $^ $@
	rm $@/LICENSE
	rm $@/heap.c
	rm $@/Makefile
	./convert_bulk_markdown_to_pdf.sh $@
	cp heap_test.stdout $@

heap_allocator_reduced.tex: TITLE=SHMALL - Simple Heap Memory ALLocator
heap_allocator_reduced_mod_embed.tex: heap_allocator_reduced.tex
	patch $^ -o $@ < heap_allocator_reduced_mod_embed.patch

# the reverse
heap_allocator_reduced_mod_embed.patch: heap_allocator_reduced.tex heap_allocator_reduced_mod_embed.tex
	diff --ignore-all-space -u $^ > $@ || test $$? -eq 1

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
# TODO: rename to chapters 0-2
acwj_chapters_1-2.d: acwj.d
	mkdir $@
	cp -R $^/0{0,1,2}_*/ $@
	./convert_bulk_markdown_to_pdf.sh $@
	find $@ -name '*.png' | xargs rm
# acwj_chapters_1-2.tex: acwj_chapters_1-2.d
# 	$(CODE2TEX)  $^ --title 'A Compiler Writing Journey - Chapters 0-2' > $@
acwj_chapters_1-2.tex: TITLE = A Compiler Writing Journey - Chapters 0-2

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
