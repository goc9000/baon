ANTLR_JAR=./lib/antlr-3.1.3.jar

all: parsers gui

gui:
	make -C src/gui/templates

parsers:
	rm -f src/genparsers/*.pyc
	java -jar $(ANTLR_JAR) -fo src/genparsers src/grammars/Rules.g

.PHONY: parsers gui
