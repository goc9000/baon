#!/usr/bin/python

# baon.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os, sys, argparse

# Hack: try to get ANTLR3 from adjacent lib directory if user does not have it installed
try:
    __import__('antlr3')
except:
    base, _ = os.path.split(sys.path[0])
    lib_path = os.path.join(base, 'lib')
    sys.path.append(lib_path)
    
from gui.Gui import Gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mass file renamer.', argument_default=argparse.SUPPRESS)
    parser.add_argument('base_path', metavar='<base path>', nargs='?', help='A path to the files that are to be renamed')
    parser.add_argument('--rules', metavar='<rule text>', help='Rules to apply (separate using semicolons)')
    parser.add_argument('-r', '--scan-recursive', action='store_true', help='Scan subfolders recursively')
    parser.add_argument('-x', '--use-extension', action='store_true', help='Include extension in renaming process')
    parser.add_argument('-p', '--use-path', action='store_true', help='Include full path in renaming process')
    setup = vars(parser.parse_args(sys.argv[1:]))
    
    gui = Gui()
    if len(setup) > 0:
        gui.setupMainWindow(setup)
    
    gui.runBlocking()
