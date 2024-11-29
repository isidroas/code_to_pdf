.DELETE_ON_ERROR:
# TODO: download and install fonts

all: TheAlgorithms-Python-hash.pdf

TheAlgorithms-Python.tar.gz:
# the project does not have releases, but using some random commit to have an stable output
	curl -L https://github.com/TheAlgorithms/Python/tarball/fc33c505935e9927cffb6142591891f721a7bcd9 > $@

# TODO sufix .d to make common recipe to all tars?
TheAlgorithms-Python: TheAlgorithms-Python.tar.gz
	mkdir -p $@
	tar --strip-components=1 --directory=$@ -xvf $^

TheAlgorithms-Python-hash.tex: TheAlgorithms-Python
# code2pdfbook $^/data_structures/hashing > $@
	code_to_pdf $^/data_structures/hashing --title 'TheAlgorithms/data_structures/hashing' > $@


TEX=xelatex -shell-escape
%.pdf: %.tex
	$(TEX) $^
	$(TEX) $^

clean: clean-latex-artifacts
	rm -rf *.tex *.pdf *.tar.gz
	rm -rf TheAlgorithms-Python

# TODO: dirs are not cleaned
clean-latex-artifacts:
	rm -rf _minted-* *.aux *.log *.out
