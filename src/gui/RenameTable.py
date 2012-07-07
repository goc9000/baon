from PyQt4.Qt import Qt, QFileInfo
from PyQt4.QtGui import QColor, QTableWidget, QTableWidgetItem, QHeaderView, QFileIconProvider, QStyle
from PyQt4 import QtGui

class RenameTable(QTableWidget):
    COLOR_ERROR = QColor(255,0,0)
    COLOR_WARNING = QColor(192,128,0)
    COLOR_CHANGED = QColor(0,64,224)
    
    error_icon = None
    qfip = None
    files_from = None
    files_to = None
    
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.error_icon = QtGui.qApp.style().standardIcon(QStyle.SP_MessageBoxCritical)
        self.qfip = QFileIconProvider()

        self.setShowGrid(False)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['From','To'])
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(20)
        
    def showFiles(self, files_from, files_to):
        self.files_from = files_from
        self.files_to = files_to
        
        self.setRowCount(len(files_from))
        
        for row in xrange(len(files_from)):
            self.setItem(row, 0, self._formatFromItem(files_from[row]))
            self.setItem(row, 1, self._formatToItem(files_to[row]))
    
    def _formatFromItem(self, fref):
        item = QTableWidgetItem(fref.filename)
        item.setFlags(Qt.ItemIsEnabled)
        item.setIcon(self.qfip.icon(QFileInfo(fref.full_path)))

        return item
        
    def _formatToItem(self, fref):
        if fref.filename is None:
            text = fref.error
            icon = self.error_icon
        elif fref.error is not None:
            text = "{0} [{1}]".format(fref.filename, fref.error)
        else:
            text = fref.filename
        
        if fref.filename is None:
            icon = self.error_icon
        else:
            icon = self.qfip.icon(QFileInfo(fref.old_full_path))
        
        if fref.error is not None:
            color = self.COLOR_ERROR
        elif fref.warning is not None:
            color = self.COLOR_WARNING
        elif fref.filename != fref.old_filename:
            color = self.COLOR_CHANGED
        else:
            color = None
        
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
        item.setIcon(icon)
        if color is not None:
            item.setTextColor(color)
        
        if fref.error is not None:
            item.setToolTip("Error: {0}".format(fref.error))
        elif fref.warning is not None:
            item.setToolTip("Warning: {0}".format(fref.warning))

        return item
    