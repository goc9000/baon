from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QDialog, QDesktopWidget, QFileDialog, QSyntaxHighlighter
from gui.templates.Ui_MainWindow import Ui_MainWindow

from logic.FileScanner import FileScanner
from logic.Renamer import Renamer
from logic.rules.RuleSet import RuleSet
from logic.rules.RuleParser import RuleParser
from logic.errors.RuleParseException import RuleParseException
from logic.errors.RuleCheckException import RuleCheckException

class MySyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        
    def highlightBlock(self, text):
        pass

class MainWindow(QDialog, Ui_MainWindow):
    _CHANGE_DELAY_MS = 1200
    
    _gui = None
    
    _changeTimer = None
    _highlighter = None
    
    def __init__(self, gui):
        QDialog.__init__(self)

        self._gui = gui
        self.initUi()
        self.centerOnScreen()
    
    def initUi(self):
        self.setupUi(self)
        
        self._changeTimer = QTimer(self)
        self._changeTimer.timeout.connect(self._updateAll)
        
        self.btnBrowse.clicked.connect(self._onBrowseClicked)
        
        self.txtBasePath.textEdited.connect(self._onEditing)
        self.txtBasePath.editingFinished.connect(self._updateAll)
        
        self.txtRules.textChanged.connect(self._onEditing)
        
        self._highlighter = MySyntaxHighlighter(self.txtRules.document())
        
    def setup(self, *args, **kwargs):
        if 'basePath' in kwargs:
            self.txtBasePath.setText(kwargs['basePath'])
            self._updateAll()

    def centerOnScreen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))

    def _onEditing(self):
        self._changeTimer.start(self._CHANGE_DELAY_MS)
    
    def _onBrowseClicked(self):
        path = QFileDialog.getExistingDirectory(parent=self, caption='Browse for Base Directory')
        if path is None:
            return
        
        self.txtBasePath.setText(path)
        self._updateAll()

    def _updateAll(self):
        self._changeTimer.stop()
        
        ruleset = self._parseCommands()
        files = self._scanFiles()

        if (files is None) or isinstance(files, Exception):
            filesLeft = filesRight = []
        else:
            filesLeft = filesRight = files

        if isinstance(ruleset, Exception):
                self._showError(str(ruleset))
        elif files is None:
            self._showInfo("Enter the base path for the files that are to be renamed.")
        elif isinstance(files, Exception):
            self._showError(str(files))
        elif len(files) == 0:
            self._showInfo("No files found.")
        elif ruleset.isEmpty():
            self._showInfo("{0} files found.".format(len(files)))
        else:
            renamer = Renamer(ruleset)
            filesRight = renamer.rename(filesLeft)
            
            self._showInfo("{0} files processed.".format(len(files)))
    
        self.tblFiles.showFiles(filesLeft, filesRight)
    
    def _scanFiles(self):
        try:
            txt = str(self.txtBasePath.text())
            if txt.strip() == "":
                return None
            
            scanner = FileScanner()
            files = scanner.scan(txt)
            
            return files
        except Exception as e:
            return e
    
    def _parseCommands(self):
        try:
            txt = str(self.txtRules.document().toPlainText())
            if txt.strip() == "":
                return RuleSet()
            
            parser = RuleParser()
            ruleset = parser.parse(txt)
            ruleset.semanticCheck()
            
            return ruleset
        except RuleCheckException as e:
            return e
        except RuleParseException as e:
            return e
        
    def _showInfo(self, message):
        self.lblStatus.setText(message)
        self.lblStatus.setStyleSheet("")
    
    def _showError(self, message):
        self.lblStatus.setText(message)
        self.lblStatus.setStyleSheet("QLabel { color : red; }")
        
