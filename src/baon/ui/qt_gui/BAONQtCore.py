# baon/ui/qt_gui/BAONQtCore.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import QObject, pyqtSlot, pyqtSignal


class BAONQtCore(QObject):
    prologue_finished = pyqtSignal()
    has_shutdown = pyqtSignal()

    def __init__(self, args):
        super().__init__()

    @pyqtSlot()
    def start(self):
        self.prologue_finished.emit()

    @pyqtSlot()
    def shutdown(self):
        self.has_shutdown.emit()
