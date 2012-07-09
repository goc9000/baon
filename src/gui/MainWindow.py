from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QDialog, QDesktopWidget, QFileDialog, QMessageBox, QSyntaxHighlighter
from gui.templates.Ui_MainWindow import Ui_MainWindow

from logic.FileScanner import FileScanner
from logic.Renamer import Renamer
from logic.RenamePlan import RenamePlan
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
    
    _change_timer = None
    _highlighter = None
    
    _setup = None
    _disable_autoupdate = False

    _base_path = None
    _files = None
    _ruleset = None
    _renamed = None
    
    def __init__(self, gui):
        QDialog.__init__(self)

        self._gui = gui
        self.initUi()
        self.centerOnScreen()
        
        self._setup = self.getSetup()
    
    def initUi(self):
        self.setupUi(self)
        
        self._change_timer = QTimer(self)
        self._change_timer.timeout.connect(self._onUpdate) 
        trigger_change_timer = lambda: self._change_timer.start(self._CHANGE_DELAY_MS)
        
        self.txtBasePath.textEdited.connect(trigger_change_timer)
        self.txtBasePath.editingFinished.connect(self._onUpdate)
        self.btnBrowse.clicked.connect(self._onBrowseClicked)
        
        self.chkScanRecursive.stateChanged.connect(self._onUpdate)
        self.chkUseExtension.stateChanged.connect(self._onUpdate)
        self.chkUsePath.stateChanged.connect(self._onUpdate)
        
        self.txtRules.textChanged.connect(trigger_change_timer)
        
        self._highlighter = MySyntaxHighlighter(self.txtRules.document())
        
    def setup(self, setup):
        self._disable_autoupdate = True
        
        if 'base_path' in setup:
            self.txtBasePath.setText(setup['base_path'])
        if 'scan_recursive' in setup:
            self.chkScanRecursive.setChecked(setup['scan_recursive'])
        if 'use_path' in setup:
            self.chkUsePath.setChecked(setup['use_path'])
        if 'use_extension' in setup:
            self.chkUseExtension.setChecked(setup['use_extension'])
        if 'rules' in setup:
            self.txtRules.setPlainText(setup['rules'])
        
        self._disable_autoupdate = False
        
        self._onUpdate()
    
    def getSetup(self):
        setup = {}
        setup['base_path'] = str(self.txtBasePath.text())
        setup['scan_recursive'] = self.chkScanRecursive.isChecked()
        setup['use_path'] = self.chkUsePath.isChecked()
        setup['use_extension'] = self.chkUseExtension.isChecked()
        setup['rules'] = str(self.txtRules.document().toPlainText())
        
        return setup
    
    def centerOnScreen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))
    
    def accept(self):
        if self._change_timer.isActive():
            self._onUpdate()
        
        if not self._allOk():
            return
        
        try:
            plan = RenamePlan(self._base_path, self._renamed)
            
            QDialog.accept(self)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
    
    def _allOk(self):
        if self._files is None or isinstance(self._files, Exception) or len(self._files) == 0:
            return False
        if self._ruleset is None or isinstance(self._ruleset, Exception):
            return False
        if any(rfref.error is not None for rfref in self._renamed):
            return False
        
        return True

    def _onUpdate(self):
        if self._disable_autoupdate:
            return
        
        self._change_timer.stop()
        
        old_setup = self._setup
        setup = self._setup = self.getSetup()
        
        changed = set(field for field in setup.keys() if setup[field] != old_setup[field])
        files_updated = False
        rules_updated = False
        options_updated = False
        renamed_updated = False
        
        if 'base_path' in changed or 'scan_recursive' in changed:
            self._base_path = setup['base_path']
            self._files = self._scanFiles(setup['base_path'], setup['scan_recursive'])
            files_updated = True
        
        if 'rules' in changed:
            self._ruleset = self._parseRules(setup['rules'])
            rules_updated = True
        
        if 'use_path' in changed or 'use_extension' in changed:
            options_updated = True
        
        if files_updated or rules_updated or options_updated:
            self._renamed = self._renameFiles(self._files, self._ruleset, setup['use_path'], setup['use_extension'])
            renamed_updated = True
        
        if files_updated or renamed_updated:
            self._updateFilesDisplay()
        
        self._updateStatusMessage()
        
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(self._allOk())

    def _onBrowseClicked(self):
        path = QFileDialog.getExistingDirectory(parent=self, caption='Browse for Base Directory')
        if path is None:
            return
        
        self.txtBasePath.setText(path)
        self._updateAll()

    def _scanFiles(self, base_path, recursive):
        if base_path.strip() == "":
            return None
        
        try:
            scanner = FileScanner()
            files = scanner.scan(base_path, recursive)
            
            return files
        except Exception as e:
            return e

    def _parseRules(self, text):
        try:
            parser = RuleParser()
            ruleset = parser.parse(text)
            ruleset.semanticCheck()
            
            return ruleset
        except RuleCheckException as e:
            return e
        except RuleParseException as e:
            return e

    def _renameFiles(self, files, ruleset, use_path, use_extension):
        if files is None or isinstance(files, Exception):
            return None
        
        if ruleset is None or isinstance(ruleset, Exception):
            ruleset = RuleSet()
        
        renamer = Renamer(ruleset, use_extension, use_path)
        
        return renamer.rename(files)
    
    def _updateFilesDisplay(self):
        self.tblFiles.showFiles(self._renamed)
    
    def _updateStatusMessage(self):
        is_error = False
        
        if self._files is not None:
            if not isinstance(self._files, Exception):
                if not isinstance(self._ruleset, Exception):
                    if len(self._files) > 0:
                        if self._ruleset is not None:
                            message = "{0} files processed.".format(len(self._files))
                        else:
                            message = "{0} files found.".format(len(self._files))
                    else:
                        message = "No files found."
                else:
                    message = str(self._ruleset)
                    is_error = True
            else:
                message = str(self._files)
                is_error = True
        else:
            message = 'Enter the base path for the files that are to be renamed.'
        
        self.lblStatus.setText(message)
        self.lblStatus.setStyleSheet('QLabel { color : red; }' if is_error else '')
