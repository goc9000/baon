all: $(patsubst %.ui,Ui_%.py,$(wildcard *.ui)) resources_rc.py

resources_rc.py: resources.qrc $(wildcard graphics/*) 
	pyrcc4 resources.qrc -o $@

Ui_%.py: %.ui
	pyuic4 $^ -o $@
