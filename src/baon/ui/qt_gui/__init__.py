# baon/ui/qt_gui/__init__.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.ui.ui_info import UIInfo


def get_ui_info():
    try:
        import PyQt4

        is_available = True
        reason_not_available = None
    except ImportError as e:
        is_available = False
        reason_not_available = str(e)

    return UIInfo(
        name='qt_gui',
        description='A GUI using the QT4 framework',
        is_available=is_available,
        reason_not_available=reason_not_available,
        priority=2,
        start_function=_start,
    )


def _start(args):
    from baon.ui.qt_gui.BAONQtApplication import BAONQtApplication

    BAONQtApplication(args).exec_()
