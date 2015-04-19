# baon/ui/qt_gui/widgets/FilesDisplay.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtCore import Qt, QFileInfo, QSize
from PyQt4.QtGui import QFileIconProvider, QHeaderView, QTableWidget, QTableWidgetItem


class FilesDisplay(QTableWidget):
    FROM_COLUMN_TEXT = 'From'
    TO_COLUMN_TEXT = 'To'

    DEFAULT_ROW_HEIGHT = 20
    DEFAULT_ICON_SIZE = DEFAULT_ROW_HEIGHT - 2

    def __init__(self, parent):
        super().__init__(parent)

        self.setShowGrid(False)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.FROM_COLUMN_TEXT, self.TO_COLUMN_TEXT])
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.DEFAULT_ROW_HEIGHT)

        self.setIconSize(QSize(self.DEFAULT_ICON_SIZE, self.DEFAULT_ICON_SIZE))

    def set_original_files(self, files):
        self.setRowCount(len(files))

        for row_index, file_ref in enumerate(files):
            self.setItem(row_index, 0, OriginalFileItem(file_ref))
            self.setItem(row_index, 1, OriginalFileItem(file_ref))


class OriginalFileItem(QTableWidgetItem):
    def __init__(self, file_ref):
        QTableWidgetItem.__init__(self, file_ref.filename)

        self.setFlags(Qt.ItemIsEnabled)
        self.setIcon(QFileIconProvider().icon(QFileInfo(file_ref.full_path)))
