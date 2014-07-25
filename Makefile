all: gui

gui:
	make -C src/gui/templates

install:
	sudo install/install.sh

uninstall:
	sudo install/uninstall.sh

.PHONY: gui install uninstall
