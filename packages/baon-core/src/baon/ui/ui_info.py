# baon/ui/ui_info.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import pkgutil
from collections import namedtuple

import baon.ui


UIInfo = namedtuple('UIInfo', [
    'name',
    'description',
    'is_available',
    'reason_not_available',
    'priority',
    'start_function',
])


def discover_uis():
    all_uis = []

    for importer, name, is_package in pkgutil.iter_modules(baon.ui.__path__):
        if not is_package:
            continue

        try:
            ui_info = importer.find_module(name).load_module(name).get_ui_info()
        except Exception as exc:
            ui_info = UIInfo(
                name=name,
                description='(description not available)',
                is_available=False,
                reason_not_available=str(exc),
                priority=0,
                start_function=None,
            )

        all_uis.append(ui_info)

    all_uis.sort(key=lambda ui: (not ui.is_available, -ui.priority))

    return all_uis
