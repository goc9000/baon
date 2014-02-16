# gui/Gui.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import sys
from gui.MainWindow import MainWindow
from PyQt4.QtGui import QApplication


class Gui(object):
    _app = None
    _mainWindow = None
    
    def __init__(self):
        self._app = QApplication(sys.argv)
        self._mainWindow = MainWindow(self)
    
    def setupMainWindow(self, *args, **kwargs):
        self._mainWindow.setup(*args, **kwargs)
    
    def runBlocking(self):
        self._mainWindow.show()
        self._app.exec_()
