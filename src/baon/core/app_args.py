# baon/core/app_args.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import argparse
import sys
from collections import namedtuple

from baon.app_metadata import APP_DESCRIPTION
from baon.core.utils.baon_utils import convert_raw_overrides
from baon.core.utils.lang_utils import chunked


BAONArguments = namedtuple('BAONArguments', [
    'base_path',
    'rules_text',
    'scan_recursive',
    'use_extension',
    'use_path',
    'overrides',
    'ui',
])


def parse_app_args(ui_info):
    assert len(ui_info) > 0

    known_uis = [ui.name for ui in ui_info]
    uis_help = 'The user interface to use, from among these choices: ' + ', '.join(
        "'{0}' ({1}{2})".format(
            ui.name,
            ui.description,
            '; NOT AVAILABLE' if not ui.is_available else '',
        ) for ui in ui_info
    )

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
    parser.add_argument('-u', '--ui', choices=known_uis, metavar='<ui>', dest='ui', default=ui_info[0].name,
                        help=uis_help)

    raw_args = parser.parse_args(sys.argv[1:])

    return BAONArguments(
        base_path=raw_args.base_path,
        rules_text=raw_args.rules_text,
        scan_recursive=raw_args.scan_recursive,
        use_extension=raw_args.use_extension,
        use_path=raw_args.use_path,
        overrides=_process_overrides_param(parser, raw_args.overrides, raw_args.base_path),
        ui=raw_args.ui,
    )


def _process_overrides_param(parser, raw_value, base_path):
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

    return convert_raw_overrides(result, base_path)
