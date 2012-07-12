import os

from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QDialog, QDesktopWidget, QFileDialog, QMessageBox

from gui.templates.Ui_MainWindow import Ui_MainWindow

from RuleSyntaxHighlighter import RuleSyntaxHighlighter

from logic.FileScanner import FileScanner
from logic.Renamer import Renamer
from logic.plan.RenamePlan import RenamePlan
from logic.rules.RuleSet import RuleSet
from logic.rules.RuleParser import RuleParser
from logic.errors.RuleParseException import RuleParseException
from logic.errors.RuleCheckException import RuleCheckException
from logic.utils import format_numerals, qstr_to_unicode

class MainWindow(QDialog, Ui_MainWindow):
    _CHANGE_DELAY_MS = 1200
    
    _gui = None
    
    _change_timer = None
    _highlighter = None
    
    _setup = None
    _disable_autoupdate = False
    _force_rescan = False
    _hold_rule_error = False

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
        self._change_timer.timeout.connect(self._onDataEdited)
        
        self.txtRules.textChanged.connect(self._clearRuleError)
        self._highlighter = RuleSyntaxHighlighter(self.txtRules.document())
    
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
        self._force_rescan = 'rescan' in setup and setup['rescan'] == True
        
        self._onDataEdited()
    
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
    
    def show(self, *args, **kwargs):
        try:
            while True:
                plan_file = RenamePlan.findBackups()
                if plan_file is None:
                    break
                answer = QMessageBox.question(None, "Confirm",
                                   "A backup plan file from an interrupted rename operation\nwas found at {0}.\n\nRoll back the operation? (recommended)".format(plan_file),
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
                if answer == QMessageBox.No:
                    break
                
                plan = RenamePlan.loadFromFile(plan_file)
                plan.undo()
                os.remove(plan_file)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
        
        return QDialog.show(self, *args, **kwargs)
    
    def accept(self):
        stats = self._renameStats()
        
        if self._change_timer.isActive():
            self._onDataEdited()
        
        if not self._allOk():
            return
        
        if stats['warnings'] > 0:
            answer = QMessageBox.question(None, "Confirm",
                 "There are warnings regarding some of the filenames. Continue?",
                 QMessageBox.Yes | QMessageBox.No,
                 QMessageBox.No)
            if answer == QMessageBox.No:
                return
        
        plan_file = None
        try:
            plan = RenamePlan(self._base_path, self._renamed)
            plan_file = plan.getBackupFileName()
            plan.saveToFile(plan_file)
            try:
                os.system('sync')
            except:
                pass
            plan.execute()
            
            counts_txt = format_numerals([('file', stats['files_changed']),
                                          ('directory', stats['dirs_changed'])])
            
            answer = QMessageBox.information(self,
                "Success",
                "{0} successfully renamed. Continue with another rename operation?".format(counts_txt),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.setup({'rules': '', 'rescan': True})
                return
            
            QDialog.accept(self)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            try:
                if plan_file is not None:
                    os.remove(plan_file)
            except:
                pass
    
    def _clearRuleError(self):
        if not self._hold_rule_error:
            self._highlighter.clearError()
        self._hold_rule_error = False
    
    def _onDataTyped(self):
        self._change_timer.start(self._CHANGE_DELAY_MS)

    def _onDataEdited(self):
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
        
        if 'base_path' in changed or 'scan_recursive' in changed or self._force_rescan:
            self._base_path = setup['base_path']
            self._files = self._scanFiles(setup['base_path'], setup['scan_recursive'])
            files_updated = True
            self._force_rescan = False
        
        if 'rules' in changed:
            self._ruleset = self._parseRules(setup['rules'])
            
            if isinstance(self._ruleset, RuleParseException):
                self._hold_rule_error = True
                self._highlighter.showError(self._ruleset.line, self._ruleset.column)
            else:
                self._highlighter.clearError()
            
            rules_updated = True
        
        if 'use_path' in changed or 'use_extension' in changed:
            options_updated = True
        
        if files_updated or rules_updated or options_updated:
            if (self._files is not None) and not isinstance(self._files, Exception):
                self._renamed = self._renameFiles(self._files, self._ruleset, setup['use_path'], setup['use_extension'])
            else:
                self._renamed = None
            
            renamed_updated = True
        
        if renamed_updated:
            self._updateFilesDisplay()
        
        self._updateStatusMessage()
        
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(self._allOk())

    def _onClickedBrowse(self):
        path = QFileDialog.getExistingDirectory(parent=self, caption='Browse for Base Directory')
        
        if path == '':
            return
        
        self.txtBasePath.setText(path)
        self._onDataEdited()

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
                        stats = self._renameStats()
                        
                        if self._ruleset is not None:
                            err_txt = format_numerals([('error', stats['errors']),
                                                       ('warning', stats['warnings'])], True, '')
                            if err_txt != '':
                                err_txt = " ({0})".format(err_txt)
                                
                            chg_txt = format_numerals([('file', stats['files_changed']),
                                                       ('directory', stats['dirs_changed'])], True, 'No files')
                            
                            message = "{0} changed{1}.".format(chg_txt, err_txt)
                        else:
                            message = "{0} found.".format(format_numerals([('file', stats['files']),
                                                                           ('directory', stats['dirs'])]))
                        
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

    def _renameStats(self):
        stats = dict(files=0, dirs=0, files_changed=0, dirs_changed=0, errors=0, warnings=0)
        
        if (self._files is not None) and not isinstance(self._files, Exception):
            for fref in self._files:
                if fref.is_dir:
                    stats['dirs'] += 1
                else:
                    stats['files'] += 1
        
        if self._renamed is not None:
            for rfref in self._renamed:
                if rfref.error is not None:
                    stats['errors'] += 1
                if rfref.warning is not None:
                    stats['warnings'] += 1
                if rfref.changed():
                    if rfref.is_dir:
                        stats['dirs_changed'] += 1
                    else:
                        stats['files_changed'] += 1
        
        return stats
    
    def _allOk(self):
        if self._files is None or isinstance(self._files, Exception) or len(self._files) == 0:
            return False
        if self._ruleset is None or isinstance(self._ruleset, Exception):
            return False
        
        stats = self._renameStats()
        
        if (stats['errors'] > 0) or (stats['files_changed'] + stats['dirs_changed'] == 0):
            return False
        
        return True
