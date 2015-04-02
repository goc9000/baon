# baon/ui/qt_gui/utils/WindowWithCenterOnScreenTrait.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QDesktopWidget, QWidget


class WindowWithCenterOnScreenTrait(QWidget):
    def center_on_screen(self):
        desktop = QDesktopWidget().availableGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))
