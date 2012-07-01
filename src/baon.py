import sys

from gui.Gui import Gui

if __name__ == "__main__":
    gui = Gui()
    if len(sys.argv) > 1:
        gui.setupMainWindow(basePath = sys.argv[1])
    gui.runBlocking()
