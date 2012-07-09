import sys, argparse

from gui.Gui import Gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mass file renamer.', argument_default=argparse.SUPPRESS)
    parser.add_argument('base_path', metavar='<base path>', nargs='?', help='A path to the files that are to be renamed')
    parser.add_argument('--rules', metavar='<rule text>', help='Rules to apply (separate using semicolons)')
    parser.add_argument('-r', '--scan-recursive', action='store_true', help='Scan subfolders recursively')
    parser.add_argument('-x', '--use-ext', action='store_true', help='Include extension in renaming process')
    parser.add_argument('-p', '--use-path', action='store_true', help='Include full path in renaming process')
    setup = vars(parser.parse_args(sys.argv[1:]))
    
    gui = Gui()
    if len(setup) > 0:
        gui.setupMainWindow(setup)
    
    gui.runBlocking()
