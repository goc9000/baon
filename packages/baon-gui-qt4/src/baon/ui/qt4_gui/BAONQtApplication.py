# baon/ui/qt4_gui/BAONQtApplication.py
#
# (C) Copyright 2012-present  Cristian Dinu <goc9000@gmail.com>
# 
# This file is part of BAON.
#
# Licensed under the GPL-3


import sys

from PyQt4.QtCore import Qt, QThread, QUrl, QMetaObject, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QApplication, QMessageBox, QProgressDialog, QDesktopServices

from baon.core.plan.rename_plan_backup import get_rename_plan_backup_filename
from baon.ui.qt4_gui.BAONQtCore import BAONQtCore
from baon.ui.qt4_gui.forms.MainWindow import MainWindow


class BAONQtApplication(QApplication):
    BACKUP_DIALOG_CAPTION = 'Rename Plan Backup Detected'
    BACKUP_DIALOG_ERROR_CAPTION = 'Error'
    BACKUP_INTRO_TEXT = 'BAON has detected a backed up rename plan from a previous run of the '\
        'application. This suggests that the application crashed partway through executing a rename operation. The '\
        'files may have been left in an inconsistent state.'
    BACKUP_PROMPT_TEXT = 'What do you want to do?'

    REVERT_BACKUP_PROGRESS_TEXT = 'Reverting the rename operation'

    SUCCESS_DIALOG_CAPTION = 'Success'
    WARNING_DIALOG_CAPTION = 'Warning'

    BACKUP_DELETED_DIALOG_TEXT =\
        'The backed up plan has been deleted. Further runs of the application will proceed normally.'
    BACKUP_REVERTED_SUCCESS_DIALOG_TEXT = 'The rename operation has been reverted successfully. The directory state '\
        'should now have been completely restored.'
    BACKUP_REVERTED_WARNING_DIALOG_TEXT = 'There were inconsistencies while trying to revert the previous rename '\
        'operation. The directory state may not have been fully restored.'

    REVERT_BACKUP_BUTTON_TEXT = 'Revert the rename (recommended)'
    DELETE_BACKUP_BUTTON_TEXT = 'Delete the backup file'
    EXAMINE_BACKUP_BUTTON_TEXT = 'Examine the plan in a text editor'
    QUIT_BUTTON_TEXT = 'Quit BAON'

    request_revert_backup = pyqtSignal()
    request_delete_backup = pyqtSignal()

    _main_window = None
    _core = None
    _progress_dialog = None

    _core_thread = None

    def __init__(self, args):
        super().__init__(sys.argv)

        # Actually we do quit when the last window is closed, but we need to do this in a more controlled way
        self.setQuitOnLastWindowClosed(False)

        self._init_threads()
        self._init_main_objects(args)
        self._connect_main_objects()
        self._start_core()

    def _init_threads(self):
        self._core_thread = QThread()
        self._core_thread.start()

    def _init_main_objects(self, args):
        self._main_window = MainWindow(args)

        self._core = BAONQtCore(args)
        self._core.moveToThread(self._core_thread)

    def _connect_main_objects(self):
        self.aboutToQuit.connect(self._on_quit)

        # Core vs. application

        self._core.request_backup_decision.connect(self.backup_decision_requested)
        self._core.reverted_backup.connect(self.notify_backup_reverted)
        self._core.revert_backup_error.connect(self.handle_backup_op_error)
        self._core.deleted_backup.connect(self.notify_backup_deleted)
        self._core.delete_backup_error.connect(self.handle_backup_op_error)

        self.request_revert_backup.connect(self._core.revert_backup)
        self.request_delete_backup.connect(self._core.delete_backup)

        # Core vs. main window

        self._core.prologue_finished.connect(self._main_window.show_first_time)

        self._core.status_changed.connect(self._main_window.report_status)
        self._core.scanned_files_updated.connect(self._main_window.update_scanned_files)
        self._core.renamed_files_updated.connect(self._main_window.update_renamed_files)

        self._core.has_shutdown.connect(self.quit)

        self._main_window.base_path_edited.connect(self._core.update_base_path)
        self._main_window.scan_recursive_changed.connect(self._core.update_scan_recursive)

        self._main_window.rules_text_changed.connect(self._core.update_rules_text)
        self._main_window.use_path_changed.connect(self._core.update_use_path)
        self._main_window.use_extension_changed.connect(self._core.update_use_extension)

        self._main_window.request_add_override.connect(self._core.add_override)
        self._main_window.request_remove_override.connect(self._core.remove_override)

        self._main_window.request_do_rename.connect(self._core.do_rename)
        self._main_window.request_rescan.connect(self._core.rescan)

        self._main_window.rejected.connect(self._core.shutdown)

    def _start_core(self):
        QMetaObject.invokeMethod(self._core, 'start', Qt.QueuedConnection)

    def _on_quit(self):
        self._core_thread.quit()
        self._core_thread.wait()

    @pyqtSlot()
    def backup_decision_requested(self):
        self._show_backup_decision()

    @pyqtSlot(Exception)
    def handle_backup_op_error(self, error):
        self._close_progress_dialog()
        self._show_backup_decision(error=error)

    @pyqtSlot()
    def notify_backup_deleted(self):
        QMessageBox.information(
            None,
            self.SUCCESS_DIALOG_CAPTION,
            self.BACKUP_DELETED_DIALOG_TEXT,
        )

    @pyqtSlot(bool)
    def notify_backup_reverted(self, complete_success):
        self._close_progress_dialog()
        if complete_success:
            QMessageBox.information(
                None,
                self.SUCCESS_DIALOG_CAPTION,
                self.BACKUP_REVERTED_SUCCESS_DIALOG_TEXT,
            )
        else:
            QMessageBox.warning(
                None,
                self.WARNING_DIALOG_CAPTION,
                self.BACKUP_REVERTED_WARNING_DIALOG_TEXT,
            )

    def _show_backup_decision(self, error=None):
        text = '<p>{0}</p><p>{1}</p>'.format(
            self.BACKUP_INTRO_TEXT if error is None else error,
            self.BACKUP_PROMPT_TEXT,
        )

        dialog = QMessageBox(
            QMessageBox.Question if error is None else QMessageBox.Critical,
            self.BACKUP_DIALOG_CAPTION if error is None else self.BACKUP_DIALOG_ERROR_CAPTION,
            text,
        )

        revert_button = dialog.addButton(self.REVERT_BACKUP_BUTTON_TEXT, QMessageBox.AcceptRole)
        delete_button = dialog.addButton(self.DELETE_BACKUP_BUTTON_TEXT, QMessageBox.DestructiveRole)
        examine_button = dialog.addButton(self.EXAMINE_BACKUP_BUTTON_TEXT, QMessageBox.ActionRole)
        dialog.addButton(self.QUIT_BUTTON_TEXT, QMessageBox.RejectRole)

        dialog.exec()
        clicked_button = dialog.clickedButton()

        if clicked_button == examine_button:
            QMetaObject.invokeMethod(self, '_examine_backup', Qt.QueuedConnection)
        elif clicked_button == revert_button:
            self._progress_dialog = QProgressDialog(None)
            self._progress_dialog.setLabelText(self.REVERT_BACKUP_PROGRESS_TEXT)
            self._progress_dialog.setCancelButton(None)
            self._progress_dialog.setRange(0, 0)
            self._progress_dialog.forceShow()

            self.request_revert_backup.emit()
        elif clicked_button == delete_button:
            self.request_delete_backup.emit()
        else:
            self.quit()

    @pyqtSlot()
    def _examine_backup(self):
        error = None
        try:
            filename = get_rename_plan_backup_filename()
            QDesktopServices.openUrl(QUrl.fromLocalFile(filename))
        except Exception as err:
            error = err
        finally:
            self._show_backup_decision(error)

    def _close_progress_dialog(self):
        if self._progress_dialog is not None:
            self._progress_dialog.close()

        self._progress_dialog = None
