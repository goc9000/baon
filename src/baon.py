import sys

from gui.Gui import Gui

if __name__ == "__main__":
    gui = Gui()
    
    setup = dict()
    
    if len(sys.argv) > 1:
        setup['base_path'] = sys.argv[1]
    
    if len(setup) > 0:
        gui.setupMainWindow(setup)
    
    gui.runBlocking()
