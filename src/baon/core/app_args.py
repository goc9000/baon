# baon/core/app_args.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys
import argparse

from collections import namedtuple

from baon.core.utils.lang_utils import chunked
from baon.app_metadata import APP_DESCRIPTION


BAONArguments = namedtuple('BAONArguments', [
    'base_path',
    'rules_text',
    'scan_recursive',
    'use_extension',
    'use_path',
    'overrides',
])


def parse_app_args():
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument('base_path', metavar='<base path>', nargs='?',
                        help='A path to the files that are to be renamed')
    parser.add_argument('--rules', metavar='<rule text>', dest='rules_text',
                        help='Rules to apply (separate using semicolons)')
    parser.add_argument('-r', '--scan-recursive', action='store_true', help='Scan subfolders recursively')
    parser.add_argument('-x', '--use-extension', action='store_true', help='Include extension in renaming process')
    parser.add_argument('-p', '--use-path', action='store_true', help='Include full path in renaming process')
    parser.add_argument('-o', '--override', action='append', nargs='+', metavar='<from> <to>', dest='overrides',
                        help='Override the rename result for certain files')

    raw_args = parser.parse_args(sys.argv[1:])

    return BAONArguments(
        base_path=raw_args.base_path,
        rules_text=raw_args.rules_text,
        scan_recursive=raw_args.scan_recursive,
        use_extension=raw_args.use_extension,
        use_path=raw_args.use_path,
        overrides=_process_overrides_param(parser, raw_args.overrides)
    )


def _process_overrides_param(parser, raw_value):
    result = {}

    if raw_value is None:
        return result

    for overrides_group in raw_value:
        for filename_from, filename_to in chunked(overrides_group, 2):
            if filename_to is None:
                parser.error("No override specified for file '{0}'".format(filename_from))
            elif result.get(filename_from, filename_to) != filename_to:
                parser.error("Conflicting overrides for file '{0}'".format(filename_from))
            else:
                result[filename_from] = filename_to

    return result
