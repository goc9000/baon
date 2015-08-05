# baon/ui/qt_gui/BAONStatus.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from baon.core.utils.symbol import symbol


class BAONStatus:
    AVAILABLE = symbol('available')
    IN_PROGRESS = symbol('in_progress')
    PENDING = symbol('pending')
    ERROR = symbol('error')
    NOT_AVAILABLE = symbol('not_available')

    scan_status = None
    scan_status_extra = None
    rules_status = None
    rules_status_extra = None
    rename_status = None
    rename_status_extra = None
