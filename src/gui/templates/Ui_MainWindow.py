# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Sun Jul  1 13:49:37 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(838, 619)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/graphics/app_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblBasePath = QtGui.QLabel(MainWindow)
        self.lblBasePath.setObjectName(_fromUtf8("lblBasePath"))
        self.horizontalLayout.addWidget(self.lblBasePath)
        self.txtBasePath = QtGui.QLineEdit(MainWindow)
        self.txtBasePath.setObjectName(_fromUtf8("txtBasePath"))
        self.horizontalLayout.addWidget(self.txtBasePath)
        self.btnBrowse = QtGui.QPushButton(MainWindow)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gbxRules = QtGui.QGroupBox(MainWindow)
        self.gbxRules.setMaximumSize(QtCore.QSize(16777215, 112))
        self.gbxRules.setObjectName(_fromUtf8("gbxRules"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.gbxRules)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.txtRules = QtGui.QTextEdit(self.gbxRules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtRules.sizePolicy().hasHeightForWidth())
        self.txtRules.setSizePolicy(sizePolicy)
        self.txtRules.setAcceptRichText(False)
        self.txtRules.setObjectName(_fromUtf8("txtRules"))
        self.horizontalLayout_4.addWidget(self.txtRules)
        self.horizontalLayout_3.addWidget(self.gbxRules)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gbxFiles = QtGui.QGroupBox(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.gbxFiles.sizePolicy().hasHeightForWidth())
        self.gbxFiles.setSizePolicy(sizePolicy)
        self.gbxFiles.setObjectName(_fromUtf8("gbxFiles"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbxFiles)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblFiles = RenameTable(self.gbxFiles)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblFiles.sizePolicy().hasHeightForWidth())
        self.tblFiles.setSizePolicy(sizePolicy)
        self.tblFiles.setAlternatingRowColors(True)
        self.tblFiles.setWordWrap(False)
        self.tblFiles.setColumnCount(2)
        self.tblFiles.setObjectName(_fromUtf8("tblFiles"))
        self.tblFiles.setColumnCount(2)
        self.tblFiles.setRowCount(0)
        self.tblFiles.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.tblFiles, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.gbxFiles)
        self.gbxStatus = QtGui.QGroupBox(MainWindow)
        self.gbxStatus.setObjectName(_fromUtf8("gbxStatus"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbxStatus)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblStatus = QtGui.QLabel(self.gbxStatus)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.horizontalLayout_2.addWidget(self.lblStatus)
        self.verticalLayout.addWidget(self.gbxStatus)
        self.buttonBox = QtGui.QDialogButtonBox(MainWindow)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.lblBasePath.setBuddy(self.txtBasePath)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MainWindow.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MainWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "BAON", None, QtGui.QApplication.UnicodeUTF8))
        self.lblBasePath.setText(QtGui.QApplication.translate("MainWindow", "Base Path", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("MainWindow", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.gbxRules.setTitle(QtGui.QApplication.translate("MainWindow", "Rename Rules", None, QtGui.QApplication.UnicodeUTF8))
        self.gbxFiles.setTitle(QtGui.QApplication.translate("MainWindow", "Renamed Files", None, QtGui.QApplication.UnicodeUTF8))
        self.gbxStatus.setTitle(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("MainWindow", "Enter the base path for the files that are to be renamed.", None, QtGui.QApplication.UnicodeUTF8))

from gui.RenameTable import RenameTable
import resources_rc
