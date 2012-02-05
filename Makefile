ANTLR_JAR=./antlr-3.1.3.jar

parsers:
	rm -f src/genparsers/*.pyc
	java -jar $(ANTLR_JAR) -fo src/genparsers src/grammars/Rules.g
