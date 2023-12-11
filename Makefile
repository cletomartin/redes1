PHONY = all build  buildpdf

all: pre-commit build

pre-commit:
	pre-commit run --all

build:
	jb build -W -n .

buildpdf:
	jb build -W -n --builder pdflatex .

publish: build buildpdf
	mkdir -p _publish
	mv _build/html/* _publish/
	mv _build/latex/*.pdf _publish/redes1.pdf

clean:
	jb clean .
	find . -name "*~" -delete
	rm -rf _build _publish
