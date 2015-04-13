# baon/ui/qt_gui/utils/WidgetWithSetupTabStopsTrait.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget


class WidgetWithSetupTabStopsTrait(QWidget):
    def setup_tab_stops(self, *items, focus_policy=Qt.StrongFocus):
        for item in items:
            item.setFocusPolicy(item.focusPolicy() | focus_policy)

        for i in range(len(items) - 1):
            self.setTabOrder(items[i], items[i+1])
