# gui/MainWindow.py
#
# (C) Copyright 2012  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3

import os

from PyQt4.QtCore import QTimer, QThread, pyqtSignal
from PyQt4.QtGui import QWidget, QDialog, QDesktopWidget, QFileDialog, QMessageBox

from gui.templates.Ui_MainWindow import Ui_MainWindow
from gui.qt_utils import qstr_to_unicode

from RuleSyntaxHighlighter import RuleSyntaxHighlighter

from logic.files.FileScanner import FileScanner
from logic.Renamer import Renamer
from logic.plan.RenamePlan import RenamePlan
from logic.rules.RuleSet import RuleSet
from logic.errors.RuleParseException import RuleParseException
from logic.errors.RuleCheckException import RuleCheckException
from logic.grammar_utils import format_numerals


class MainWindow(QDialog, Ui_MainWindow):
    _CHANGE_DELAY_MS = 1200
    
    _gui = None
    
    _change_timer = None
    _highlighter = None
    _worker = None
    _worker_on_finished = None
    
    _setup = None
    _disable_autoupdate = False
    _force_rescan = False
    _hold_rule_error = False
    _controls_locked = False
    _focused_control = None

    _base_path = None
    _files = None
    _ruleset = None
    _override_dict = None
    _renamed = None
    
    def __init__(self, gui):
        QDialog.__init__(self)

        self._gui = gui
        self.initUi()
        self.centerOnScreen()
        
        self._override_dict = dict()
        self._setup = self.getSetup()
        self._onDataEdited()
    
    def initUi(self):
        self.setupUi(self)
        self.progressBar.hide()
        
        self._change_timer = QTimer(self)
        self._change_timer.timeout.connect(self._onDataEdited)
        
        self.txtRules.textChanged.connect(self._clearRuleError)
        self._highlighter = RuleSyntaxHighlighter(self.txtRules.document())
        
        self.tblFiles.overrideAdded.connect(self._onOverrideAdded)
        self.tblFiles.overrideRemoved.connect(self._onOverrideRemoved)
        
        self._worker = Worker()
        self._worker.progress.connect(self._showProgress)
        self._worker.finished.connect(self._onWorkerFinished)
        
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
        if 'overrides' in setup:
            self._override_dict = dict(setup['overrides'])
        
        self._disable_autoupdate = False
        self._force_rescan = 'rescan' in setup and setup['rescan']
        
        self._onDataEdited()
    
    def getSetup(self):
        return {
            'base_path': qstr_to_unicode(self.txtBasePath.text()),
            'scan_recursive': self.chkScanRecursive.isChecked(),
            'use_path': self.chkUsePath.isChecked(),
            'use_extension': self.chkUseExtension.isChecked(),
            'rules': qstr_to_unicode(self.txtRules.document().toPlainText()),
            'overrides': dict(self._override_dict)
        }

    def centerOnScreen(self):
        desktop = QDesktopWidget().screenGeometry()
        self.move((desktop.width() / 2) - (self.frameSize().width() / 2),
                  (desktop.height() / 2) - (self.frameSize().height() / 2))
    
    def show(self, *args, **kwargs):
        self._handleBackups()
        
        return QDialog.show(self, *args, **kwargs)
    
    def accept(self):
        if self._controls_locked:
            return
        
        self._executeRename()
    
    def reject(self):
        if self._controls_locked:
            return
        
        QDialog.reject(self)
    
    def _lockControls(self):
        self._focused_control = None
        for ctrl in self.children():
            if isinstance(ctrl, QWidget) and ctrl.hasFocus():
                self._focused_control = ctrl
        
        self.txtBasePath.setReadOnly(True)
        self.txtRules.setReadOnly(True)
        self.chkScanRecursive.setDisabled(True)
        self.chkUseExtension.setDisabled(True)
        self.chkUsePath.setDisabled(True)
        self.tblFiles.setReadOnly(True)
        
        self._controls_locked = True
    
    def _unlockControls(self):
        self.txtBasePath.setReadOnly(False)
        self.txtRules.setReadOnly(False)
        self.chkScanRecursive.setDisabled(False)
        self.chkUseExtension.setDisabled(False)
        self.chkUsePath.setDisabled(False)
        self.tblFiles.setReadOnly(False)
        
        self._controls_locked = False
            
        for ctrl in self.children():
            if ctrl == self._focused_control:
                ctrl.setFocus()
    
    def _clearRuleError(self):
        if not self._hold_rule_error:
            self._highlighter.clear_error()
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
        
        if 'base_path' in changed or 'scan_recursive' in changed or self._force_rescan:
            self._force_rescan = False
            self._base_path = setup['base_path']
            
            if self._base_path.strip() == "":
                self._files = None
                self._onDataEditedContinued(changed, True)
                return
            
            base_path = self._setup['base_path']
            recursive = self._setup['scan_recursive']
            work = lambda on_progress: self._doScanFiles(base_path, recursive, on_progress)
            on_finished = lambda files: self._onScanFilesFinished(files, changed)
            self._lockControls()
            self._startWorker(work, on_finished)
        else:
            self._onDataEditedContinued(changed, False)
    
    def _doScanFiles(self, base_path, recursive, on_progress):
        # Executed in worker context
        on_prog = lambda done, total: on_progress('Scanning for files...', done, total)
        
        try:
            scanner = FileScanner()
            files = scanner.scan(base_path, recursive, on_prog)
            
            return files
        except Exception as e:
            return e
    
    def _onScanFilesFinished(self, files, changed):
        self._unlockControls()
        
        self._files = files
        self._onDataEditedContinued(changed, True)
    
    def _onDataEditedContinued(self, changed, files_updated):
        setup = self._setup
        rules_updated = ('rules' in changed)
        options_updated = ('use_path' in changed) or ('use_extension' in changed)
        overrides_updated = ('overrides' in changed)
        
        if rules_updated:
            self._ruleset = self._parseRules(setup['rules'])
            if isinstance(self._ruleset, Exception) and hasattr(self._ruleset, 'source_span'):
                self._hold_rule_error = True
                self._highlighter.show_error(self._ruleset.source_span)
            else:
                self._highlighter.clear_error()
        
        if files_updated or rules_updated or options_updated or overrides_updated:
            if (self._files is not None) and not isinstance(self._files, Exception):
                self._renamed = self._renameFiles(self._files, self._ruleset, setup['use_path'], setup['use_extension'],
                                                  setup['overrides'])
            else:
                self._renamed = None
            
            self._updateFilesDisplay()
        
        self._updateStatusMessage()
        
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(self._allOk())

    def _onClickedBrowse(self):
        if self._controls_locked:
            return
        
        path = QFileDialog.getExistingDirectory(parent=self, caption='Browse for Base Directory')
        
        if path == '':
            return
        
        self.txtBasePath.setText(path)
        self._onDataEdited()

    def _onOverrideAdded(self, key, name):
        self._override_dict[qstr_to_unicode(key)] = qstr_to_unicode(name)
        self._onDataEdited()
    
    def _onOverrideRemoved(self, key):
        key = qstr_to_unicode(key)
        if key in self._override_dict:
            del self._override_dict[key]
            self._onDataEdited()
    
    def _parseRules(self, text):
        try:
            return RuleSet.from_source(text)
        except RuleCheckException as e:
            return e
        except RuleParseException as e:
            return e

    def _renameFiles(self, files, ruleset, use_path, use_extension, overrides):
        if files is None or isinstance(files, Exception):
            return None
        
        if ruleset is None or isinstance(ruleset, Exception):
            ruleset = RuleSet()
        
        renamer = Renamer(ruleset, use_extension, use_path)
        
        return renamer.rename(files, overrides)
    
    def _executeRename(self):
        if not self._doFinalChecks():
            return
        
        work = lambda on_progress: self._doExecutePlan(on_progress)
        on_finished = lambda result: self._onExecutePlanFinished(result)
        self._lockControls()
        self._startWorker(work, on_finished)
        
    def _doExecutePlan(self, on_progress):
        # Executed in worker context
        on_prog = lambda done, total: on_progress('Executing rename plan...', done, total)
        
        plan_file = None
        error = None
        try:
            on_progress('Creating rename plan...', 0, 1)
            
            plan = RenamePlan(self._base_path, self._renamed)
            plan_file = plan.getBackupFileName()
            plan.saveToFile(plan_file)
            try:
                os.system('sync')
            except OSError:
                pass
            
            plan.execute(on_prog)
        except Exception as e:
            error = e
        finally:
            try:
                if plan_file is not None:
                    os.remove(plan_file)
            except OSError:
                pass
        
        return error
    
    def _onExecutePlanFinished(self, error):
        self._unlockControls()

        if error is not None:
            self._showStatusMessage("Error during rename operation", True)
            QMessageBox.critical(self, "Error", str(error))
            return
        
        self._showStatusMessage("Done!", False)
        
        if not self._showSuccessMessage():
            QDialog.accept(self)
    
    def _doFinalChecks(self):
        stats = self._getStats()
        
        if self._change_timer.isActive():
            self._onDataEdited()
        
        if not self._allOk():
            return False
        
        if stats['warnings'] > 0:
            answer = QMessageBox.question(
                self, "Confirm",
                "There are warnings regarding some of the filenames. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
            if answer == QMessageBox.No:
                return False
        
        return True
    
    def _showSuccessMessage(self):
        stats = self._getStats()
        counts_txt = format_numerals([('file', stats['files_changed']),
                                      ('directory', stats['dirs_changed'])])
        
        answer = QMessageBox.information(
            self, "Success",
            "{0} successfully renamed. Continue with another rename operation?".format(counts_txt),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.setup({'rules': '', 'overrides': dict(), 'rescan': True})
            return True
        
        return False
    
    def _handleBackups(self):
        try:
            while True:
                plan_file = RenamePlan.findBackups()
                if plan_file is None:
                    break
                answer = QMessageBox.question(
                    None, "Confirm",
                    ("A backup plan file from an interrupted rename operation\n"
                     "was found at {0}.\n\n"
                     "Roll back the operation? (recommended)").format(plan_file),
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes)
                if answer == QMessageBox.No:
                    break
                
                plan = RenamePlan.loadFromFile(plan_file)
                plan.undo()
                os.remove(plan_file)
        except Exception as e:
            QMessageBox.critical(None, "Error", str(e))
    
    def _updateFilesDisplay(self):
        self.tblFiles.showFiles(self._renamed)
    
    def _updateStatusMessage(self):
        message, is_error = self._getStatusMessage()
        self._showStatusMessage(message, is_error)
    
    def _getStatusMessage(self):
        if isinstance(self._ruleset, Exception):
            return str(self._ruleset), True
        if self._files is None:
            return 'Enter the base path for the files that are to be renamed.', False
        if isinstance(self._files, Exception):
            return str(self._files), True
        if len(self._files) == 0:
            return "No files found.", False
        
        stats = self._getStats()
        
        if self._ruleset is None and (stats['files_changed']+stats['dirs_changed'] == 0):
            found_txt = format_numerals([('file', stats['files']), ('directory', stats['dirs'])])
            return "{0} found.".format(found_txt), False
        
        err_txt = format_numerals([('error', stats['errors']), ('warning', stats['warnings'])], True, '')
        if err_txt != '':
            err_txt = " ({0})".format(err_txt)
            
        chg_txt = format_numerals([('file', stats['files_changed']),
                                   ('directory', stats['dirs_changed'])],
                                  True, 'No files')
        
        return "{0} changed{1}.".format(chg_txt, err_txt), (stats['errors'] > 0)
    
    def _showStatusMessage(self, message, is_error):
        self.lblStatus.setText(message)
        self.lblStatus.setStyleSheet('QLabel { color : red; }' if is_error else '')
        self.progressBar.hide()
    
    def _showProgress(self, message, done, total):
        self.lblStatus.setText(message)
        self.lblStatus.setStyleSheet('')
        self.progressBar.setValue(done)
        self.progressBar.setMaximum(total)
        self.progressBar.show()
    
    def _getStats(self):
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
        if isinstance(self._ruleset, Exception):
            return False
        
        stats = self._getStats()
        
        if (stats['errors'] > 0) or (stats['files_changed'] + stats['dirs_changed'] == 0):
            return False
        
        return True
    
    def _startWorker(self, work, on_finished):
        self._worker_on_finished = on_finished
        self._worker.start(work)
        
    def _onWorkerFinished(self, result):
        self._worker_on_finished(result)


class Worker(QThread):
    progress = pyqtSignal(str, int, int)
    finished = pyqtSignal(object)
    
    work = None 
    
    def __init__(self):
        QThread.__init__(self)
    
    def start(self, work):
        self.work = work
        QThread.start(self)

    def run(self):
        result = self.work(lambda msg, done, total: self.progress.emit(msg, done, total))
        
        self.finished.emit(result)
