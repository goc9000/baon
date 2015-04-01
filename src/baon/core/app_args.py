# baon/core/app_args.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys
import argparse

from baon.app_metadata import APP_DESCRIPTION


def parse_app_args():
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument('base_path', metavar='<base path>', nargs='?',
                        help='A path to the files that are to be renamed')
    parser.add_argument('--rules', metavar='<rule text>', dest='rules_text',
                        help='Rules to apply (separate using semicolons)')
    parser.add_argument('-r', '--scan-recursive', action='store_true', help='Scan subfolders recursively')
    parser.add_argument('-x', '--use-extension', action='store_true', help='Include extension in renaming process')
    parser.add_argument('-p', '--use-path', action='store_true', help='Include full path in renaming process')

    return parser.parse_args(sys.argv[1:])
