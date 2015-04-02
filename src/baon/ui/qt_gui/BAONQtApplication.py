# baon/ui/qt_gui/BAONQtApplication.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys

from PyQt4.QtGui import QApplication

from baon.ui.qt_gui.forms.MainWindow import MainWindow


class BAONQtApplication(QApplication):
    main_window = None

    def __init__(self, args):
        QApplication.__init__(self, sys.argv)
        self.main_window = MainWindow()
        self.main_window.show()
