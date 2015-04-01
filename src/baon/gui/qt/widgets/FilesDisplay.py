# baon/gui/qt/widgets/FilesDisplay.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


from PyQt4.QtGui import QHeaderView, QTableWidget


class FilesDisplay(QTableWidget):
    FROM_COLUMN_TEXT = 'From'
    TO_COLUMN_TEXT = 'To'

    DEFAULT_ROW_HEIGHT = 20

    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.setShowGrid(False)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels([self.FROM_COLUMN_TEXT, self.TO_COLUMN_TEXT])
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(self.DEFAULT_ROW_HEIGHT)
