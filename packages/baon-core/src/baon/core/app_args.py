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
    if len(ui_info) > 0:
        uis_help = 'The user interface to use, from among these choices: ' + ', '.join(
            _format_ui_info(ui) for ui in ui_info
        )
        default_ui = next((ui.name for ui in ui_info if ui.is_available), None)
    else:
        uis_help = 'The user interface to use (none are installed)'
        default_ui = None

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
    parser.add_argument('-u', '--ui', metavar='<ui>', dest='ui', default=default_ui, help=uis_help,
                        choices=[ui.name for ui in ui_info])

    raw_args = parser.parse_args(sys.argv[1:])

    if raw_args.ui is None:
        if len(ui_info) == 0:
            parser.error('No UI packages are installed. Install one appropriate for your system and retry.')
        else:
            parser.error('No UI is available from among those installed. Address this problem and retry.')
        sys.exit(-1)
    else:
        selected_ui = next(ui for ui in ui_info if ui.name == raw_args.ui)
        if not selected_ui.is_available:
            parser.error('The UI you selected ({0}) is not available for this reason: {1}'.format(
                selected_ui.name,
                selected_ui.reason_not_available,
            ))

    return BAONArguments(
        base_path=raw_args.base_path,
        rules_text=raw_args.rules_text,
        scan_recursive=raw_args.scan_recursive,
        use_extension=raw_args.use_extension,
        use_path=raw_args.use_path,
        overrides=_process_overrides_param(parser, raw_args.overrides, raw_args.base_path),
        ui=selected_ui,
    )


def _format_ui_info(ui):
    return "'{0}' ({1}{2})".format(
        ui.name,
        ui.description,
        '; NOT AVAILABLE: {0}'.format(ui.reason_not_available) if not ui.is_available else '',
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
