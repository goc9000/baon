from PyQt4.Qt import Qt, QFileInfo
from PyQt4.QtGui import QTableWidget, QTableWidgetItem, QHeaderView, QFileIconProvider, QStyle
from PyQt4 import QtGui

class RenameTable(QTableWidget):
    error_icon = None
    
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)

        self.error_icon = QtGui.qApp.style().standardIcon(QStyle.SP_MessageBoxCritical)
    
        self.setShowGrid(False)
        
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['From','To'])
        
        self.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(20)
        
    def showFiles(self, filesFrom, filesTo):
        qfip = QFileIconProvider()
        
        self.setRowCount(len(filesFrom))
        
        for row in xrange(len(filesFrom)):
            text = filesFrom[row].filename
            icon = qfip.icon(QFileInfo(filesFrom[row].fullPath))
            
            itemFrom = QTableWidgetItem(text)
            itemFrom.setFlags(Qt.ItemIsEnabled)
            itemFrom.setIcon(icon)
            
            if isinstance(filesTo[row], Exception):
                text = str(filesTo[row])
                editable = False
                icon = self.error_icon
            else:
                text = filesTo[row].filename
                editable = True
            
            itemTo = QTableWidgetItem(text)
            itemTo.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable if editable else Qt.ItemIsEnabled)
            itemTo.setIcon(icon)
            
            self.setItem(row, 0, itemFrom)
            self.setItem(row, 1, itemTo)
            