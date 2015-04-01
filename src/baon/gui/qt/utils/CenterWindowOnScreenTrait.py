# baon/gui/qt/utils/CenterWindowOnScreenTrait.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
#
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QDesktopWidget, QWidget


class CenterWindowOnScreenTrait(QWidget):
    def center_on_screen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))
