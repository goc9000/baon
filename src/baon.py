#!/usr/bin/python3

# baon.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.app_args import parse_app_args

from baon.ui.ui_info import discover_uis


if __name__ == "__main__":
    ui_info = discover_uis()

    if not any(ui.is_available for ui in ui_info):
        raise SystemError('No UI is available from among: ' + ', '.join(ui.name for ui in ui_info))

    args = parse_app_args(ui_info)

    ui = next(ui for ui in ui_info if ui.name == args.ui)

    if not ui.is_available:
        raise SystemError("The UI you selected ({0}) is not available for this reason: {1}".format(
            ui.name,
            ui.reason_not_available,
        ))

    ui.start_function(args)
