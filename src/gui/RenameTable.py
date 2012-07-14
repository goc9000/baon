# gui/RenameTable.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

from PyQt4.Qt import Qt, QFileInfo, pyqtSignal
from PyQt4.QtGui import QColor, QTableWidget, QTableWidgetItem, QHeaderView, QFileIconProvider, QStyle
from PyQt4 import QtGui

class RenameTable(QTableWidget):
    COLOR_ERROR = QColor(255,0,0)
    COLOR_WARNING = QColor(192,128,0)
    COLOR_CHANGED = QColor(0,64,224)
    
    _edit_index = None
    _read_only = False
    
    overrideAdded = pyqtSignal(str, str)
    overrideRemoved = pyqtSignal(str)
    
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.setShowGrid(False)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['From','To'])
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(20)
    
    def showFiles(self, files):
        if files is None:
            files = []
        
        self.setRowCount(len(files))
        
        for row in xrange(len(files)):
            self.setItem(row, 0, FromFileItem(files[row]))
            self.setItem(row, 1, ToFileItem(files[row]))
    
    def setReadOnly(self, ronly):
        self._read_only = ronly
    
    def edit(self, index, trigger, event):
        if self._read_only:
            return False
        
        self._edit_index =  index.row()
        
        return QTableWidget.edit(self, index, trigger, event)
    
    def commitData(self, editor):
        new_data = editor.text()
        
        if self._edit_index is None:
            return
    
        item = self.item(self._edit_index, 1)
        
        if new_data == item.ed_data:
            return
        
        if new_data == '':
            self.overrideRemoved.emit(item.ed_key)
        else:
            self.overrideAdded.emit(item.ed_key, new_data)

class FromFileItem(QTableWidgetItem):
    def __init__(self, fref):
        QTableWidgetItem.__init__(self, fref.old_filename)
        
        self.setFlags(Qt.ItemIsEnabled)
        self.setIcon(QFileIconProvider().icon(QFileInfo(fref.old_full_path)))

class ToFileItem(QTableWidgetItem):
    ed_data = None
    ed_key = None
    
    def __init__(self, fref):
        QTableWidgetItem.__init__(self)
        
        if fref.filename is None:
            text = fref.error
        elif fref.error is not None:
            text = "{0} [{1}]".format(fref.filename, fref.error)
        elif fref.warning is not None:
            text = "{0} [{1}]".format(fref.filename, fref.warning)
        else:
            text = fref.filename
        
        if fref.filename is None:
            icon = QtGui.qApp.style().standardIcon(QStyle.SP_MessageBoxCritical)
        else:
            icon = QFileIconProvider().icon(QFileInfo(fref.old_full_path))
        
        if fref.error is not None:
            color = RenameTable.COLOR_ERROR
        elif fref.warning is not None:
            color = RenameTable.COLOR_WARNING
        elif fref.changed():
            color = RenameTable.COLOR_CHANGED
        else:
            color = None
        
        self.setText(text)
        self.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
        self.setIcon(icon)
        if color is not None:
            self.setTextColor(color)
            
        if fref.override:
            font = self.font()
            font.setBold(True)
            self.setFont(font)
        
        if fref.error is not None:
            self.setToolTip("Error: {0}".format(fref.error))
        elif fref.warning is not None:
            self.setToolTip("Warning: {0}".format(fref.warning))
        
        self.ed_key = fref.old_filename
        self.ed_data = fref.filename if fref.filename is not None else ''
    
    def data(self, role):
        if role == Qt.EditRole:
            return self.ed_data
        
        return QTableWidgetItem.data(self, role)
        