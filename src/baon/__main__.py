# baon/__main__.py
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
    args = parse_app_args(ui_info)
    args.ui.start_function(args)
