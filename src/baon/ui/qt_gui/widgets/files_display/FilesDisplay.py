# baon/ui/qt_gui/widgets/files_display/FilesDisplay.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import pyqtSlot, QSize
from PyQt4.QtGui import QAbstractItemView, QHeaderView, QTableView

from baon.ui.qt_gui.widgets.files_display.FilesDisplayModel import FilesDisplayModel


class FilesDisplay(QTableView):
    DEFAULT_ROW_HEIGHT = 20
    DEFAULT_ICON_SIZE = DEFAULT_ROW_HEIGHT - 2

    def __init__(self, parent):
        super().__init__(parent)

        self.setModel(FilesDisplayModel(self))
        self.setSelectionMode(QAbstractItemView.NoSelection)

        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setIconSize(QSize(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE))

        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.DEFAULT_ROW_HEIGHT)

    @pyqtSlot(list)
    def set_original_files(self, files):
        self.model().set_original_files(files)

    @pyqtSlot(list)
    def set_renamed_files(self, files):
        self.model().set_renamed_files(files)
